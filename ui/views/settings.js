/**
 * Phase 3 Week 13 — Settings Controller
 * PB05-08 — Configuration Bay: tabs, overlay bridge, banner test center.
 *
 * Three-tier customization:
 *  - Tier 1: Preset profiles (quick starts)
 *  - Tier 2: Pillar categories (enable/disable entire features)
 *  - Tier 3: Granular settings (per-feature fine-tuning)
 */

const SETTINGS_TABS = ['basic', 'overlay', 'ai', 'future', 'advanced'];

const KNOWN_BANNER_TYPES = [
  'HULL_CRITICAL_10',
  'SHIELDS_DOWN',
  'HULL_CRITICAL_25',
  'FUEL_CRITICAL',
  'MODULE_CRITICAL',
  'FUEL_LOW',
  'HEAT_WARNING',
  'HEAT_DAMAGE',
  'OMNICOVAS_TEST',
];

class SettingsController {
  constructor() {
    this.currentSettings = {};
    this.init();
  }

  get apiBase() {
    if (window.Shell?.httpBase) return window.Shell.httpBase;
    if (window.OMNICOVAS_PORT) return `http://127.0.0.1:${window.OMNICOVAS_PORT}`;
    return null;
  }

  apiUrl(path) {
    const base = this.apiBase;
    return base ? `${base}${path}` : null;
  }

  async init() {
    this._initTabs();
    this.bindEvents();
    if (!this.apiBase) {
      this._showWaiting();
      window.OmniEvents?.addEventListener('bridge-connected', () => this._loadAndRender(), { once: true });
      return;
    }
    await this._loadAndRender();
  }

  // ── Tab management ────────────────────────────────

  _initTabs() {
    SETTINGS_TABS.forEach(tabId => {
      const btn = document.getElementById(`tab-${tabId}`);
      if (!btn) return;
      btn.addEventListener('click', () => this._activateTab(tabId));
      btn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          this._activateTab(tabId);
        }
      });
    });
  }

  _activateTab(tabId) {
    SETTINGS_TABS.forEach(id => {
      const btn = document.getElementById(`tab-${id}`);
      const panel = document.getElementById(`panel-${id}`);
      const isActive = id === tabId;
      if (btn) btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
      if (panel) {
        if (isActive) panel.removeAttribute('hidden');
        else panel.setAttribute('hidden', '');
      }
    });

    if (tabId === 'overlay') {
      this._loadOverlaySettings();
    }
  }

  // ── Overlay settings bridge ───────────────────────

  async _loadOverlaySettings() {
    const url = this.apiUrl('/pillar1/overlay/settings');
    if (!url) {
      this._showOverlaySettingsStatus('Bridge not ready — overlay settings unavailable.');
      return;
    }
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      this._renderOverlaySettings(data);
      const statusEl = document.getElementById('overlay-settings-status');
      if (statusEl) statusEl.setAttribute('hidden', '');
    } catch (e) {
      console.warn('[Settings] Failed to load overlay settings:', e);
      this._showOverlaySettingsStatus('Overlay settings currently unavailable.');
    }
  }

  _showOverlaySettingsStatus(msg) {
    const el = document.getElementById('overlay-settings-status');
    if (!el) return;
    el.textContent = msg;
    el.removeAttribute('hidden');
  }

  _renderOverlaySettings(data) {
    const opacitySlider = document.getElementById('overlay-opacity');
    const opacityDisplay = document.getElementById('opacity-display');
    if (opacitySlider && data.opacity != null) {
      opacitySlider.value = data.opacity;
      if (opacityDisplay) opacityDisplay.textContent = `${Math.round(data.opacity * 100)}%`;
    }

    const anchorSelect = document.getElementById('overlay-anchor');
    if (anchorSelect && data.anchor) {
      anchorSelect.value = data.anchor;
    }

    if (data.click_through != null) {
      const infoDiv = document.getElementById('overlay-clickthrough-info');
      const stateEl = document.getElementById('overlay-clickthrough-state');
      if (infoDiv) infoDiv.removeAttribute('hidden');
      if (stateEl) {
        stateEl.textContent = data.click_through
          ? 'Click-through enabled'
          : 'Click-through disabled (input grabbed)';
      }
    }

    if (data.events && typeof data.events === 'object') {
      this._renderEventToggles(data.events);
    }
  }

  _renderEventToggles(events) {
    const container = document.getElementById('overlay-event-toggles');
    const grid = document.getElementById('overlay-event-grid');
    if (!container || !grid) return;

    container.removeAttribute('hidden');
    grid.replaceChildren();

    for (const [eventType, enabled] of Object.entries(events)) {
      const item = document.createElement('label');
      item.className = 'overlay-event-item';

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.checked = Boolean(enabled);
      checkbox.setAttribute('aria-label', `Toggle ${eventType} event`);
      checkbox.dataset.eventType = eventType;

      const nameSpan = document.createElement('span');
      nameSpan.textContent = eventType;

      item.appendChild(checkbox);
      item.appendChild(nameSpan);
      grid.appendChild(item);
    }
  }

  async _saveOverlaySettings() {
    const url = this.apiUrl('/pillar1/overlay/settings');
    if (!url) return;

    const opacity = parseFloat(document.getElementById('overlay-opacity')?.value || 0.95);
    const anchor = document.getElementById('overlay-anchor')?.value || 'center';
    const payload = { opacity, anchor };

    const eventCheckboxes = document.querySelectorAll('#overlay-event-grid input[type="checkbox"]');
    if (eventCheckboxes.length > 0) {
      payload.events = {};
      eventCheckboxes.forEach(cb => {
        if (cb.dataset.eventType) payload.events[cb.dataset.eventType] = cb.checked;
      });
    }

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      console.log('[Settings] Overlay settings saved.');
    } catch (e) {
      console.error('[Settings] Failed to save overlay settings:', e);
    }
  }

  // ── Banner Test Center ────────────────────────────

  async _testGenericBanner() {
    const invoke = window.__TAURI__?.core?.invoke;
    if (typeof invoke !== 'function') {
      console.warn('[Settings] Tauri not available; banner test requires desktop app.');
      return;
    }
    await invoke('show_overlay_test_banner').catch(e =>
      console.warn('[Settings] Generic banner test failed:', e)
    );
  }

  async _testSelectedBanner() {
    const select = document.getElementById('btc-banner-type');
    const eventType = select?.value;
    if (!eventType || !KNOWN_BANNER_TYPES.includes(eventType)) return;

    const invoke = window.__TAURI__?.core?.invoke;
    if (typeof invoke !== 'function') {
      console.warn('[Settings] Tauri not available; banner test requires desktop app.');
      return;
    }
    await invoke('show_overlay_named_test_banner', { eventType }).catch(e =>
      console.warn('[Settings] Named banner test failed:', e)
    );
  }

  async _testAllBanners() {
    const invoke = window.__TAURI__?.core?.invoke;
    if (typeof invoke !== 'function') {
      console.warn('[Settings] Tauri not available; banner test requires desktop app.');
      return;
    }
    for (const eventType of KNOWN_BANNER_TYPES) {
      await invoke('show_overlay_named_test_banner', { eventType }).catch(e =>
        console.warn(`[Settings] Named banner test failed for ${eventType}:`, e)
      );
    }
  }

  // ── Load / render ─────────────────────────────────

  async _loadAndRender() {
    await this.loadSettings();
    this.renderUI();
  }

  _showWaiting() {
    const grid = document.getElementById('preset-grid');
    if (!grid) return;
    const p = document.createElement('p');
    p.className = 'field-value unknown';
    p.textContent = 'Waiting for OmniCOVAS bridge…';
    grid.replaceChildren(p);
  }

  async loadSettings() {
    if (!this.apiBase) return;
    try {
      const res = await fetch(`${this.apiBase}/week13/settings`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      this.currentSettings = await res.json();
    } catch (err) {
      console.error('Failed to load settings:', err);
      this.currentSettings = this.getDefaults();
    }
  }

  getDefaults() {
    return {
      preset: 'casual',
      pillar_categories: {
        pillar_1: { enabled: true, phase_ready: true },
        pillar_2: { enabled: false, phase_ready: false, phase: 4 },
        pillar_3: { enabled: false, phase_ready: false, phase: 5 },
        pillar_5: { enabled: false, phase_ready: false, phase: 6 },
        pillar_7: { enabled: false, phase_ready: false, phase: 7 },
        pillar_6: { enabled: false, phase_ready: false, phase: 8 },
        pillar_4: { enabled: false, phase_ready: false, phase: 9 },
      },
      ai_provider: 'null',
      overlay: { opacity: 0.95, anchor: 'center' },
    };
  }

  renderUI() {
    this.renderPresets();
    this.renderPillarToggles();
    this.renderGranularSettings();
  }

  renderPresets() {
    const grid = document.getElementById('preset-grid');
    if (!grid) return;

    const presets = [
      { key: 'casual',   name: 'Casual',   icon: '\u{1F60E}' },
      { key: 'combat',   name: 'Combat',   icon: '⚔️' },
      { key: 'explorer', name: 'Explorer', icon: '\u{1F52D}' },
      { key: 'trader',   name: 'Trader',   icon: '\u{1F4E6}' },
      { key: 'miner',    name: 'Miner',    icon: '⛏️' },
    ];

    grid.innerHTML = '';
    for (const preset of presets) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'preset-button';
      if (preset.key === this.currentSettings.preset) btn.classList.add('active');
      btn.setAttribute('aria-label', `Select ${preset.name} preset`);

      const iconDiv = document.createElement('div');
      iconDiv.className = 'preset-icon';
      iconDiv.textContent = preset.icon;

      const nameDiv = document.createElement('div');
      nameDiv.className = 'preset-name';
      nameDiv.textContent = preset.name;

      btn.appendChild(iconDiv);
      btn.appendChild(nameDiv);
      btn.addEventListener('click', () => this.setPreset(preset.key));
      grid.appendChild(btn);
    }
  }

  renderPillarToggles() {
    const container = document.getElementById('tier2-toggles');
    if (!container) return;

    const cats = this.currentSettings.pillar_categories || {};
    container.innerHTML = '';

    const pillarLabels = {
      pillar_1: 'Ship Telemetry',
      pillar_2: 'Combat',
      pillar_3: 'Exploration',
      pillar_5: 'Trading & Mining',
      pillar_7: 'Squadron',
      pillar_6: 'Engineering',
      pillar_4: 'Powerplay 2.0',
    };

    for (const [key, info] of Object.entries(cats)) {
      const item = document.createElement('label');
      item.className = 'toggle-item';

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.checked = info.enabled || false;
      checkbox.disabled = !info.phase_ready;
      checkbox.setAttribute('aria-label', `Toggle ${pillarLabels[key]}`);

      const label = document.createElement('span');
      label.className = 'toggle-label';
      label.textContent = pillarLabels[key];

      const phase = document.createElement('span');
      phase.className = 'toggle-phase';
      if (!info.phase_ready) phase.textContent = `Phase ${info.phase}`;

      item.appendChild(checkbox);
      item.appendChild(label);
      if (!info.phase_ready) item.appendChild(phase);

      container.appendChild(item);
    }
  }

  renderGranularSettings() {
    const opacitySlider = document.getElementById('overlay-opacity');
    const opacityDisplay = document.getElementById('opacity-display');
    if (opacitySlider) {
      opacitySlider.value = this.currentSettings.overlay?.opacity || 0.95;
      opacitySlider.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        if (opacityDisplay) opacityDisplay.textContent = `${Math.round(val * 100)}%`;
      });
    }

    const anchorSelect = document.getElementById('overlay-anchor');
    if (anchorSelect) anchorSelect.value = this.currentSettings.overlay?.anchor || 'center';

    const aiSelect = document.getElementById('ai-provider');
    if (aiSelect) aiSelect.value = this.currentSettings.ai_provider || 'null';

    const outputRadios = document.querySelectorAll('input[name="output-mode"]');
    outputRadios.forEach((radio) => {
      if (radio.value === 'overlay') radio.checked = true;
    });
  }

  bindEvents() {
    document.getElementById('save-settings-btn')?.addEventListener('click', () => this.saveSettings());
    document.getElementById('reset-settings-btn')?.addEventListener('click', () => this.resetSettings());
    document.getElementById('export-settings-btn')?.addEventListener('click', () => this.exportSettings());
    document.getElementById('import-settings-btn')?.addEventListener('click', () => this.importSettings());
    document.getElementById('save-overlay-settings-btn')?.addEventListener('click', () => this._saveOverlaySettings());
    document.getElementById('btc-test-generic-btn')?.addEventListener('click', () => this._testGenericBanner());
    document.getElementById('btc-test-selected-btn')?.addEventListener('click', () => this._testSelectedBanner());
    document.getElementById('btc-test-all-btn')?.addEventListener('click', () => this._testAllBanners());
  }

  setPreset(preset) {
    this.currentSettings.preset = preset;
    this.renderPresets();
  }

  async saveSettings() {
    const url = this.apiUrl('/week13/settings');
    if (!url) return;

    const overlay = {
      opacity: parseFloat(document.getElementById('overlay-opacity')?.value || 0.95),
      anchor: document.getElementById('overlay-anchor')?.value || 'center',
    };
    const aiProvider = document.getElementById('ai-provider')?.value || 'null';
    const payload = { preset: this.currentSettings.preset, overlay, ai_provider: aiProvider };

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      alert('Settings saved!');
      await this.loadSettings();
      this.renderUI();
    } catch (err) {
      console.error('Failed to save settings:', err);
      alert('Failed to save settings. See console for details.');
    }
  }

  async resetSettings() {
    if (!confirm('Reset all settings to defaults?')) return;
    const url = this.apiUrl('/week13/settings/reset');
    if (!url) return;
    try {
      const res = await fetch(url, { method: 'POST' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      await this.loadSettings();
      this.renderUI();
      alert('Settings reset to defaults!');
    } catch (err) {
      console.error('Failed to reset settings:', err);
      alert('Failed to reset settings. See console for details.');
    }
  }

  async exportSettings() {
    const url = this.apiUrl('/week13/settings/export');
    if (!url) return;
    try {
      const res = await fetch(url, { method: 'POST' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const json = JSON.stringify(data, null, 2);
      const blob = new Blob([json], { type: 'application/json' });
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = `omnicovas-settings-${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(blobUrl);
    } catch (err) {
      console.error('Failed to export settings:', err);
      alert('Failed to export settings. See console for details.');
    }
  }

  async importSettings() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.addEventListener('change', async (e) => {
      const file = e.target.files?.[0];
      if (!file) return;
      try {
        const text = await file.text();
        const data = JSON.parse(text);
        if (!confirm('This will overwrite your current settings. Continue?')) return;
        const url = this.apiUrl('/week13/settings/import');
        if (!url) return;
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        await this.loadSettings();
        this.renderUI();
        alert('Settings imported!');
      } catch (err) {
        console.error('Failed to import settings:', err);
        alert('Failed to import settings. See console for details.');
      }
    });
    input.click();
  }
}

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new SettingsController());
} else {
  new SettingsController();
}

// Test hook for Vitest; keeps this browser-compatible without changing production module/script loading.
globalThis.__settingsExports = { SettingsController, SETTINGS_TABS, KNOWN_BANNER_TYPES };
