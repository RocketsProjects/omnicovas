/**
 * OmniCOVAS Shell — navigation, routing, connection management.
 *
 * Responsibilities:
 *  - Single-page routing via hash (#/dashboard, #/activity-log, etc.)
 *  - Autoconnect to Python FastAPI bridge when Tauri emits "bridge-ready"
 *  - Fallback command lookup via get_bridge_info if UI missed the event
 *  - WebSocket connection to /ws/events with exponential-backoff reconnect
 *  - HTTP /state polling fallback every 2 seconds while disconnected
 *  - Publishes events to a global bus (window.OmniEvents) for views to consume
 *  - Connection status dot in topbar
 */

'use strict';

/* ── Event bus ── */
window.OmniEvents = window.OmniEvents || new EventTarget();

function emit(type, detail) {
  window.OmniEvents.dispatchEvent(new CustomEvent(type, { detail }));
}

/* ── State ── */
const Shell = {
  port: null,
  httpBase: null,
  wsBase: null,
  ws: null,
  wsReconnectDelay: 1000,
  wsReconnectTimer: null,
  pollTimer: null,
  connected: false,
  booting: false,
};

/* ── Small helpers ── */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function normalizeBridge(payload) {
  if (!payload) return null;

  const port = Number(payload.port);

  if (!Number.isInteger(port) || port <= 0) {
    return null;
  }

  return {
    port,
    httpBase: payload.httpBase || `http://127.0.0.1:${port}`,
    wsBase: payload.wsBase || `ws://127.0.0.1:${port}`,
  };
}

/* ── Connection status UI ── */
function setConnected(yes, portNum) {
  Shell.connected = yes;

  const dot = document.getElementById('status-dot');
  const text = document.getElementById('status-text');
  const portLabel = document.getElementById('port-label');

  if (!dot || !text) return;

  if (yes) {
    dot.className = 'status-dot connected';
    dot.setAttribute('aria-label', 'Connected');
    text.textContent = 'Connected';

    if (portLabel && portNum) {
      portLabel.textContent = `port ${portNum}`;
    }
  } else {
    dot.className = 'status-dot';
    dot.setAttribute('aria-label', 'Disconnected');
    text.textContent = 'Connecting…';

    if (portLabel) {
      portLabel.textContent = '';
    }
  }
}

function setCoreNotFound() {
  const text = document.getElementById('status-text');
  const dot = document.getElementById('status-dot');
  const portLabel = document.getElementById('port-label');

  if (dot) {
    dot.className = 'status-dot';
    dot.setAttribute('aria-label', 'Disconnected');
  }

  if (text) {
    text.textContent = 'Core not found';
  }

  if (portLabel) {
    portLabel.textContent = '';
  }
}

/* ── Timer cleanup ── */
function clearReconnectTimer() {
  if (Shell.wsReconnectTimer) {
    clearTimeout(Shell.wsReconnectTimer);
    Shell.wsReconnectTimer = null;
  }
}

function stopPolling() {
  if (Shell.pollTimer) {
    clearInterval(Shell.pollTimer);
    Shell.pollTimer = null;
  }
}

function startPolling() {
  stopPolling();
  Shell.pollTimer = setInterval(fetchState, 2000);
}

/* ── Bridge configuration ── */
function setBridge(port, httpBase, wsBase) {
  Shell.port = port;
  Shell.httpBase = httpBase || `http://127.0.0.1:${port}`;
  Shell.wsBase = wsBase || `ws://127.0.0.1:${port}`;
  window.OMNICOVAS_PORT = port;
}

/* ── Tauri bridge-ready listener ── */
function waitForTauriBridgeReady(timeoutMs = 10000) {
  return new Promise((resolve) => {
    let resolved = false;
    let unlistenPromise = null;

    function finish(payload) {
      if (resolved) return;
      resolved = true;

      if (unlistenPromise) {
        unlistenPromise
          .then((unlisten) => {
            if (typeof unlisten === 'function') unlisten();
          })
          .catch(() => {});
      }

      resolve(normalizeBridge(payload));
    }

    if (window.OMNICOVAS_PORT) {
      finish({ port: window.OMNICOVAS_PORT });
      return;
    }

    const params = new URLSearchParams(window.location.search);
    if (params.has('port')) {
      finish({ port: parseInt(params.get('port'), 10) });
      return;
    }

    const tauriListen = window.__TAURI__?.event?.listen;

    if (typeof tauriListen === 'function') {
      unlistenPromise = tauriListen('bridge-ready', (event) => {
        finish(event?.payload || null);
      });
    }

    setTimeout(() => finish(null), timeoutMs);
  });
}

/* ── Tauri command fallback ── */
async function getBridgeFromTauriCommand() {
  const invoke = window.__TAURI__?.core?.invoke;

  if (typeof invoke !== 'function') {
    return null;
  }

  for (let i = 0; i < 20; i += 1) {
    try {
      const bridge = normalizeBridge(await invoke('get_bridge_info'));

      if (bridge) {
        return bridge;
      }
    } catch {
      /* command unavailable or not ready yet */
    }

    await sleep(500);
  }

  return null;
}

/* ── Last-resort dev probe ── */
async function probeForBridge() {
  for (let p = 50000; p <= 65000; p += 500) {
    try {
      const response = await fetch(`http://127.0.0.1:${p}/health`, {
        signal: AbortSignal.timeout(300),
      });

      if (response.ok) {
        return normalizeBridge({ port: p });
      }
    } catch {
      /* try next candidate port */
    }
  }

  return null;
}

/* ── Port discovery ── */
async function discover() {
  const fromTauriEvent = await waitForTauriBridgeReady();

  if (fromTauriEvent) {
    return fromTauriEvent;
  }

  const fromTauriCommand = await getBridgeFromTauriCommand();

  if (fromTauriCommand) {
    return fromTauriCommand;
  }

  return probeForBridge();
}

/* ── Onboarding status check ── */
async function checkOnboardingStatus() {
  try {
    const response = await fetch(`${Shell.httpBase}/week13/onboarding/status`);
    if (!response.ok) return;
    const status = await response.json();
    if (status.should_show_wizard === true) {
      if (typeof window.OmniOnboarding?.show === 'function') {
        window.OmniOnboarding.show();
      } else {
        /* onboarding.js not yet initialized; drain when it loads */
        window.__pendingOnboardingShow = true;
      }
    }
  } catch (err) {
    console.warn('onboarding_status_unavailable', err);
  }
}

/* ── HTTP state fetch ── */
async function fetchState() {
  if (!Shell.httpBase) return;

  try {
    const response = await fetch(`${Shell.httpBase}/state`);

    if (response.ok) {
      emit('state', await response.json());
    }
  } catch {
    /* silent — WebSocket is primary, polling is safety net */
  }
}

/* ── WebSocket ── */
function closeExistingWebSocket() {
  if (!Shell.ws) return;

  Shell.ws.onopen = null;
  Shell.ws.onmessage = null;
  Shell.ws.onclose = null;
  Shell.ws.onerror = null;

  try {
    Shell.ws.close();
  } catch {
    /* ignore close failure */
  }

  Shell.ws = null;
}

function openWebSocket() {
  if (!Shell.wsBase || !Shell.port) return;

  clearReconnectTimer();
  closeExistingWebSocket();

  const ws = new WebSocket(`${Shell.wsBase}/ws/events`);
  Shell.ws = ws;

  ws.onopen = () => {
    Shell.wsReconnectDelay = 1000;
    setConnected(true, Shell.port);
    stopPolling();

    emit('bridge-connected', {
      port: Shell.port,
      httpBase: Shell.httpBase,
      wsBase: Shell.wsBase,
    });
  };

  ws.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data);

      if (message.type === 'initial_state') {
        emit('state', message.state ?? message);
      } else if (message.type === 'event') {
        emit('event', message);
      } else if (message.state) {
        emit('state', message.state);
      } else {
        emit('event', message);
      }
    } catch {
      /* malformed WebSocket frame; ignore */
    }
  };

  ws.onclose = () => {
    setConnected(false, null);
    emit('bridge-disconnected', { port: Shell.port });

    startPolling();

    Shell.wsReconnectTimer = setTimeout(() => {
      Shell.wsReconnectDelay = Math.min(Shell.wsReconnectDelay * 2, 16000);
      openWebSocket();
    }, Shell.wsReconnectDelay);
  };

  ws.onerror = () => {
    try {
      ws.close();
    } catch {
      /* ignore */
    }
  };
}

/* ── Boot ── */
async function boot() {
  if (Shell.booting) return;

  Shell.booting = true;
  setConnected(false, null);

  const bridge = await discover();

  if (!bridge?.port) {
    Shell.booting = false;
    setCoreNotFound();

    setTimeout(boot, 5000);
    return;
  }

  setBridge(bridge.port, bridge.httpBase, bridge.wsBase);

  await fetchState();
  openWebSocket();
  checkOnboardingStatus(); /* fire-and-forget; non-fatal */

  Shell.booting = false;
}

/* ── Routing ── */
const ROUTES = {
  '/dashboard': 'view-dashboard',
  '/activity-log': 'view-activity-log',
  '/settings': 'view-settings',
  '/privacy': 'view-privacy',
  '/resources': 'view-resources',
  '/credits': 'view-credits',
};

function navigate(hash) {
  const route = hash.replace(/^#/, '') || '/dashboard';
  const viewId = ROUTES[route] || ROUTES['/dashboard'];

  document.querySelectorAll('.view').forEach((view) => {
    view.classList.remove('active');
  });

  const target = document.getElementById(viewId);
  if (target) {
    target.classList.add('active');
  }

  document.querySelectorAll('#sidebar nav a').forEach((anchor) => {
    const isActive = anchor.getAttribute('href') === `#${route}`;

    anchor.classList.toggle('active', isActive);
    anchor.setAttribute('aria-current', isActive ? 'page' : 'false');
  });
}

window.addEventListener('hashchange', () => {
  navigate(window.location.hash);
});

/* ── DOM ready ── */
document.addEventListener('DOMContentLoaded', () => {
  navigate(window.location.hash || '#/dashboard');
  boot();
});

/* ── Expose for views/devtools ── */
window.Shell = Shell;
