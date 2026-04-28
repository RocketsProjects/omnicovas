/**
 * OmniCOVAS Overlay — Critical Event Banner Handler
 *
 * Subscribes to the /ws/events endpoint and renders critical events
 * as transient banners. Handles banner queue, priority preemption, and
 * auto-dismiss timers.
 */

const CRITICAL_EVENTS = {
  HULL_CRITICAL_10: {
    icon: '⚠',
    label: 'HULL CRITICAL',
    severity: 'critical',
    duration: 30000,
    priority: 1,
  },
  SHIELDS_DOWN: {
    icon: '▼',
    label: 'SHIELDS DOWN',
    severity: 'critical',
    duration: 5000,
    priority: 2,
  },
  HULL_CRITICAL_25: {
    icon: '⚡',
    label: 'HULL WARNING',
    severity: 'warning',
    duration: 10000,
    priority: 3,
  },
  FUEL_CRITICAL: {
    icon: '🛢',
    label: 'FUEL CRITICAL',
    severity: 'critical',
    duration: 30000,
    priority: 4,
  },
  MODULE_CRITICAL: {
    icon: '🔧',
    label: 'MODULE CRITICAL',
    severity: 'critical',
    duration: 15000,
    priority: 5,
  },
  FUEL_LOW: {
    icon: '⚠',
    label: 'FUEL LOW',
    severity: 'warning',
    duration: 10000,
    priority: 6,
  },
  HEAT_WARNING: {
    icon: '🔥',
    label: 'HEAT WARNING',
    severity: 'warning',
    duration: 8000,
    priority: 7,
  },
};

let currentBanner = null;
let bannerQueue = [];
let clickThrough = true;
let wsConnection = null;
let statusDotTimeout = null;

// Overlay settings (persisted via Tauri config vault)
let overlaySettings = {
  opacity: 0.95,
  anchor: 'center',
  events: {
    HULL_CRITICAL_10: true,
    SHIELDS_DOWN: true,
    HULL_CRITICAL_25: true,
    FUEL_CRITICAL: true,
    MODULE_CRITICAL: true,
    FUEL_LOW: true,
    HEAT_WARNING: true,
  },
};

/**
 * Show a banner with auto-dismiss. Preempt lower-priority banners.
 */
function showBanner(eventType, value) {
  const config = CRITICAL_EVENTS[eventType];
  if (!config) return;

  // Check if this event type is enabled in settings
  if (overlaySettings.events[eventType] === false) return;

  const banner = {
    eventType,
    config,
    value,
    id: Date.now(),
  };

  if (currentBanner && config.priority < currentBanner.config.priority) {
    // Preempt: clear current and show new
    clearTimeout(currentBanner.timeoutId);
    renderBanner(banner);
    currentBanner = banner;
  } else if (!currentBanner) {
    // No banner active: show immediately
    renderBanner(banner);
    currentBanner = banner;
  } else {
    // Lower priority: queue
    bannerQueue.push(banner);
  }

  currentBanner.timeoutId = setTimeout(() => {
    dismissBanner();
  }, config.duration);
}

/**
 * Render a banner to the DOM with opacity applied.
 */
function renderBanner(banner) {
  const container = document.getElementById('overlay-container');
  const existing = container.querySelector('.banner');
  if (existing) existing.remove();

  const bannerEl = document.createElement('div');
  bannerEl.className = `banner ${banner.config.severity}`;
  bannerEl.style.opacity = overlaySettings.opacity.toString();
  bannerEl.innerHTML = `
    <span class="banner-icon">${banner.config.icon}</span>
    <span class="banner-label">${banner.config.label}</span>
    <span class="banner-value">${
      typeof banner.value === 'number'
        ? banner.value.toFixed(0) + '%'
        : banner.value
    }</span>
  `;

  container.appendChild(bannerEl);
}

/**
 * Dismiss current banner and show next in queue if available.
 */
function dismissBanner() {
  if (!currentBanner) return;

  const container = document.getElementById('overlay-container');
  const banner = container.querySelector('.banner');
  if (banner) banner.remove();

  currentBanner = null;

  if (bannerQueue.length > 0) {
    const next = bannerQueue.shift();
    showBanner(next.eventType, next.value);
  }
}

/**
 * Connect to /ws/events and subscribe to critical events.
 */
async function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws/events`;

  try {
    wsConnection = new WebSocket(wsUrl);

    wsConnection.onopen = () => {
      console.log('[Overlay] WebSocket connected');
    };

    wsConnection.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.type === 'event' && CRITICAL_EVENTS[message.event_type]) {
          // Extract the most relevant value from the payload
          const value = message.payload.hull_health
            || message.payload.fuel_percent
            || message.payload.heat_level
            || message.payload.module_health
            || (message.payload.shields_down !== undefined ? 'DOWN' : '—');

          showBanner(message.event_type, value);

          // Show the overlay window when a critical event fires
          if (window.__TAURI__) {
            const { invoke } = window.__TAURI__.tauri;
            invoke('show_overlay').catch(e =>
              console.error('[Overlay] Failed to show overlay:', e)
            );
          }
        }
      } catch (e) {
        console.error('[Overlay] Failed to parse message:', e);
      }
    };

    wsConnection.onerror = (error) => {
      console.error('[Overlay] WebSocket error:', error);
    };

    wsConnection.onclose = () => {
      console.log('[Overlay] WebSocket closed, reconnecting in 3s...');
      setTimeout(connectWebSocket, 3000);
    };
  } catch (e) {
    console.error('[Overlay] Failed to connect WebSocket:', e);
    setTimeout(connectWebSocket, 3000);
  }
}

/**
 * Show or update the status dot to indicate click-through state.
 */
function updateStatusDot(isClickThrough) {
  // Remove existing status dot
  const existing = document.querySelector('.status-dot');
  if (existing) existing.remove();

  // Create new status dot
  const dot = document.createElement('div');
  dot.className = 'status-dot';
  dot.style.background = isClickThrough ? '#4ade80' : '#ff6b6b';
  dot.title = isClickThrough ? 'Click-through enabled' : 'Overlay grabbing input';
  document.body.appendChild(dot);

  // Fade out after 3 seconds if no banner is active
  if (statusDotTimeout) clearTimeout(statusDotTimeout);
  statusDotTimeout = setTimeout(() => {
    const dot = document.querySelector('.status-dot');
    if (dot && !document.querySelector('.banner')) {
      dot.remove();
    }
  }, 3000);
}

/**
 * Load overlay settings from the API.
 */
async function loadOverlaySettings() {
  try {
    const response = await fetch('/pillar1/overlay/settings');
    if (response.ok) {
      const settings = await response.json();
      overlaySettings = { ...overlaySettings, ...settings };
      console.log('[Overlay] Settings loaded:', overlaySettings);
    }
  } catch (e) {
    console.warn('[Overlay] Failed to load settings, using defaults:', e);
  }
}

/**
 * Initialize overlay on page load.
 */
document.addEventListener('DOMContentLoaded', async () => {
  // Load settings first
  await loadOverlaySettings();

  connectWebSocket();

  // Listen for click-through toggle event from Tauri
  if (window.__TAURI__) {
    const { listen } = window.__TAURI__.event;
    await listen('overlay:click_through_toggled', (event) => {
      clickThrough = event.payload;
      updateStatusDot(clickThrough);
      console.log('[Overlay] Click-through toggled:', clickThrough);
    });
  }

  console.log('[Overlay] Ready. Click-through enabled by default.');
});
