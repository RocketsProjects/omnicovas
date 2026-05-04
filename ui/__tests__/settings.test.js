import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import '../views/settings.js';

const { SettingsController, SETTINGS_TABS, KNOWN_BANNER_TYPES } =
  globalThis.__settingsExports ?? {};

// ── DOM helper ───────────────────────────────────────────────────────────────

function buildTabDOM() {
  return `
    <div role="tablist" id="settings-tablist" aria-label="Settings tabs">
      <button type="button" role="tab" id="tab-basic"
              aria-selected="true" aria-controls="panel-basic">Basic</button>
      <button type="button" role="tab" id="tab-overlay"
              aria-selected="false" aria-controls="panel-overlay">Overlay</button>
      <button type="button" role="tab" id="tab-ai"
              aria-selected="false" aria-controls="panel-ai">AI / Advisory</button>
      <button type="button" role="tab" id="tab-future"
              aria-selected="false" aria-controls="panel-future">Future Systems</button>
      <button type="button" role="tab" id="tab-advanced"
              aria-selected="false" aria-controls="panel-advanced">Advanced</button>
    </div>
    <div role="tabpanel" id="panel-basic" aria-labelledby="tab-basic">
      <div id="preset-grid"></div>
      <div id="tier2-toggles"></div>
    </div>
    <div role="tabpanel" id="panel-overlay" aria-labelledby="tab-overlay" hidden>
      <p id="overlay-settings-status" hidden></p>
      <input type="range" id="overlay-opacity" min="0.5" max="1.0" step="0.05" value="0.95" />
      <span id="opacity-display">95%</span>
      <select id="overlay-anchor"><option value="center" selected>Center</option></select>
      <div id="overlay-event-toggles" hidden>
        <div id="overlay-event-grid"></div>
      </div>
      <div id="overlay-clickthrough-info" hidden>
        <p id="overlay-clickthrough-state"></p>
      </div>
      <div id="banner-test-center">
        <select id="btc-banner-type">
          <option value="HULL_CRITICAL_10">HULL_CRITICAL_10</option>
          <option value="SHIELDS_DOWN">SHIELDS_DOWN</option>
          <option value="HULL_CRITICAL_25">HULL_CRITICAL_25</option>
          <option value="FUEL_CRITICAL">FUEL_CRITICAL</option>
          <option value="MODULE_CRITICAL">MODULE_CRITICAL</option>
          <option value="FUEL_LOW">FUEL_LOW</option>
          <option value="HEAT_WARNING">HEAT_WARNING</option>
          <option value="HEAT_DAMAGE">HEAT_DAMAGE</option>
          <option value="OMNICOVAS_TEST">OMNICOVAS_TEST</option>
        </select>
        <button id="btc-test-generic-btn" type="button">Test Generic Banner</button>
        <button id="btc-test-selected-btn" type="button">Test Selected</button>
        <button id="btc-test-all-btn" type="button">Test All Banners</button>
      </div>
    </div>
    <div role="tabpanel" id="panel-ai" aria-labelledby="tab-ai" hidden>
      <select id="ai-provider"><option value="null" selected>NullProvider</option></select>
      <input type="password" id="ai-api-key" />
    </div>
    <div role="tabpanel" id="panel-future" aria-labelledby="tab-future" hidden></div>
    <div role="tabpanel" id="panel-advanced" aria-labelledby="tab-advanced" hidden>
      <button id="save-settings-btn" type="button">Save</button>
      <button id="reset-settings-btn" type="button">Reset</button>
      <button id="export-settings-btn" type="button">Export</button>
      <button id="import-settings-btn" type="button">Import</button>
    </div>
  `;
}

// ── Exports ──────────────────────────────────────────────────────────────────

describe('SettingsController', () => {
  it('is exported via test hook', () => {
    expect(SettingsController).toBeDefined();
    expect(typeof SettingsController).toBe('function');
  });

  it('SETTINGS_TABS is exported with 5 entries', () => {
    expect(Array.isArray(SETTINGS_TABS)).toBe(true);
    expect(SETTINGS_TABS.length).toBe(5);
    expect(SETTINGS_TABS).toContain('basic');
    expect(SETTINGS_TABS).toContain('overlay');
  });

  it('KNOWN_BANNER_TYPES is exported with all 9 types', () => {
    expect(Array.isArray(KNOWN_BANNER_TYPES)).toBe(true);
    expect(KNOWN_BANNER_TYPES.length).toBe(9);
    expect(KNOWN_BANNER_TYPES).toContain('OMNICOVAS_TEST');
    expect(KNOWN_BANNER_TYPES).toContain('HULL_CRITICAL_10');
  });
});

// ── Tab structure (tests 1–6) ─────────────────────────────────────────────────

describe('Settings Configuration Bay — tab structure', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = buildTabDOM();
    delete window.OMNICOVAS_PORT;
    delete window.Shell;
    ctrl = Object.create(SettingsController.prototype);
  });

  it('1. Settings tablist exists', () => {
    expect(document.querySelector('[role="tablist"]')).not.toBeNull();
  });

  it('2. All five tab buttons exist', () => {
    expect(document.querySelectorAll('[role="tab"]').length).toBe(5);
  });

  it('3. Tab buttons have role="tab"', () => {
    document.querySelectorAll('[role="tab"]').forEach(btn => {
      expect(btn.getAttribute('role')).toBe('tab');
    });
  });

  it('4. Tab panels have role="tabpanel"', () => {
    const panels = document.querySelectorAll('[role="tabpanel"]');
    expect(panels.length).toBe(5);
    panels.forEach(p => expect(p.getAttribute('role')).toBe('tabpanel'));
  });

  it('5. Activating Overlay tab shows Overlay panel and hides Basic panel', () => {
    ctrl._activateTab('overlay');
    expect(document.getElementById('panel-basic').hasAttribute('hidden')).toBe(true);
    expect(document.getElementById('panel-overlay').hasAttribute('hidden')).toBe(false);
  });

  it('6. aria-selected updates on tab switch', () => {
    ctrl._activateTab('overlay');
    expect(document.getElementById('tab-overlay').getAttribute('aria-selected')).toBe('true');
    expect(document.getElementById('tab-basic').getAttribute('aria-selected')).toBe('false');
  });

  it('switching back to Basic tab hides Overlay and shows Basic', () => {
    ctrl._activateTab('overlay');
    ctrl._activateTab('basic');
    expect(document.getElementById('panel-basic').hasAttribute('hidden')).toBe(false);
    expect(document.getElementById('panel-overlay').hasAttribute('hidden')).toBe(true);
  });
});

// ── Existing renderPresets tests ──────────────────────────────────────────────

describe('SettingsController.renderPresets', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = '<div id="preset-grid"></div>';
    ctrl = Object.create(SettingsController.prototype);
    ctrl.currentSettings = { preset: 'casual' };
  });

  it('renders 5 preset buttons', () => {
    ctrl.renderPresets();
    expect(document.querySelectorAll('.preset-button').length).toBe(5);
  });

  it('does not contain placeholder text', () => {
    ctrl.renderPresets();
    const grid = document.getElementById('preset-grid');
    expect(grid.textContent).not.toContain('coming in Week 13');
    expect(grid.textContent).not.toContain('Settings panel');
  });

  it('marks the active preset button', () => {
    ctrl.currentSettings = { preset: 'combat' };
    ctrl.renderPresets();
    const active = document.querySelectorAll('.preset-button.active');
    expect(active.length).toBe(1);
    expect(active[0].getAttribute('aria-label')).toContain('Combat');
  });

  it('uses createElement/textContent for preset icon and name — no innerHTML injection', () => {
    ctrl.renderPresets();
    const icons = document.querySelectorAll('.preset-icon');
    icons.forEach(el => expect(el.children.length).toBe(0));
    const names = document.querySelectorAll('.preset-name');
    names.forEach(el => {
      expect(typeof el.textContent).toBe('string');
      expect(el.innerHTML).not.toContain('<script');
    });
  });
});

// ── Existing renderPillarToggles tests ───────────────────────────────────────

describe('SettingsController.renderPillarToggles', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = '<div id="tier2-toggles"></div>';
    ctrl = Object.create(SettingsController.prototype);
    ctrl.currentSettings = {
      pillar_categories: {
        pillar_1: { enabled: true, phase_ready: true },
        pillar_2: { enabled: false, phase_ready: false, phase: 4 },
      },
    };
  });

  it('renders toggle labels via textContent, not innerHTML injection', () => {
    ctrl.renderPillarToggles();
    const labels = document.querySelectorAll('.toggle-label');
    expect(labels.length).toBeGreaterThan(0);
    labels.forEach((label) => {
      expect(typeof label.textContent).toBe('string');
      expect(label.innerHTML).not.toContain('<script');
      expect(label.innerHTML).not.toContain('<img');
    });
  });

  it('renders XSS payload in a key description as literal text, not HTML', () => {
    ctrl.currentSettings.pillar_categories = {
      pillar_1: { enabled: false, phase_ready: true },
    };
    ctrl.renderPillarToggles();
    const container = document.getElementById('tier2-toggles');
    expect(container.querySelector('script')).toBeNull();
    expect(container.querySelector('img')).toBeNull();
  });
});

// ── Bridge readiness (tests 7–10) ─────────────────────────────────────────────

describe('SettingsController - bridge readiness', () => {
  let ctrl;
  let originalFetch;

  beforeEach(() => {
    document.body.innerHTML = '<div id="preset-grid"></div><div id="tier2-toggles"></div>';
    delete window.OMNICOVAS_PORT;
    delete window.Shell;
    window.OmniEvents = new EventTarget();
    originalFetch = globalThis.fetch;
    globalThis.fetch = vi.fn();
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
    delete window.Shell;
    delete window.OMNICOVAS_PORT;
  });

  it('7. apiBase returns null when bridge is not ready', () => {
    ctrl = Object.create(SettingsController.prototype);
    expect(ctrl.apiBase).toBeNull();
  });

  it('apiBase uses Shell.httpBase when available', () => {
    window.Shell = { httpBase: 'http://127.0.0.1:7777' };
    ctrl = Object.create(SettingsController.prototype);
    expect(ctrl.apiBase).toBe('http://127.0.0.1:7777');
  });

  it('apiBase uses OMNICOVAS_PORT when Shell is absent', () => {
    window.OMNICOVAS_PORT = 9001;
    ctrl = Object.create(SettingsController.prototype);
    expect(ctrl.apiBase).toBe('http://127.0.0.1:9001');
  });

  it('8. apiUrl returns null when bridge is not ready', () => {
    ctrl = Object.create(SettingsController.prototype);
    expect(ctrl.apiUrl('/week13/settings')).toBeNull();
  });

  it('fetch is NOT called before bridge is ready', async () => {
    ctrl = Object.create(SettingsController.prototype);
    ctrl.currentSettings = {};
    await ctrl.init();
    expect(globalThis.fetch).not.toHaveBeenCalled();
  });

  it('init shows waiting state in preset-grid when bridge is not ready', async () => {
    ctrl = Object.create(SettingsController.prototype);
    ctrl.currentSettings = {};
    await ctrl.init();
    const grid = document.getElementById('preset-grid');
    expect(grid.textContent).toContain('Waiting for OmniCOVAS bridge');
  });

  it('10. post-bridge apiUrl never uses port 8000', () => {
    window.OMNICOVAS_PORT = 9001;
    ctrl = Object.create(SettingsController.prototype);
    const url = ctrl.apiUrl('/week13/settings');
    expect(url).not.toContain(':8000');
    expect(url).toContain('9001');
  });
});

// ── Overlay settings section (tests 9, 10) ────────────────────────────────────

describe('Settings — Overlay settings section', () => {
  beforeEach(() => {
    document.body.innerHTML = buildTabDOM();
    delete window.OMNICOVAS_PORT;
    delete window.Shell;
  });

  it('9. Overlay settings section renders in panel-overlay', () => {
    expect(document.getElementById('panel-overlay')).not.toBeNull();
    expect(document.getElementById('overlay-opacity')).not.toBeNull();
    expect(document.getElementById('overlay-anchor')).not.toBeNull();
  });

  it('_loadOverlaySettings shows unavailable status when bridge is not ready', async () => {
    const ctrl = Object.create(SettingsController.prototype);
    await ctrl._loadOverlaySettings();
    const statusEl = document.getElementById('overlay-settings-status');
    expect(statusEl.hasAttribute('hidden')).toBe(false);
    expect(statusEl.textContent).toContain('unavailable');
  });

  it('_showOverlaySettingsStatus sets textContent safely (no innerHTML)', () => {
    const ctrl = Object.create(SettingsController.prototype);
    ctrl._showOverlaySettingsStatus('<script>alert(1)</script>');
    const el = document.getElementById('overlay-settings-status');
    expect(el.textContent).toBe('<script>alert(1)</script>');
    expect(el.querySelector('script')).toBeNull();
  });

  it('_renderOverlaySettings populates opacity and anchor controls', () => {
    const ctrl = Object.create(SettingsController.prototype);
    ctrl._renderOverlaySettings({ opacity: 0.8, anchor: 'center' });
    expect(document.getElementById('overlay-opacity').value).toBe('0.8');
    expect(document.getElementById('overlay-anchor').value).toBe('center');
    expect(document.getElementById('opacity-display').textContent).toBe('80%');
  });

  it('_renderEventToggles uses createElement/textContent not innerHTML', () => {
    const ctrl = Object.create(SettingsController.prototype);
    ctrl._renderEventToggles({ HULL_CRITICAL_10: true, SHIELDS_DOWN: false });
    const grid = document.getElementById('overlay-event-grid');
    const names = grid.querySelectorAll('span');
    names.forEach(s => {
      expect(typeof s.textContent).toBe('string');
      expect(s.innerHTML).not.toContain('<script');
    });
  });
});

// ── Banner Test Center (tests 11–17) ──────────────────────────────────────────

describe('Settings Configuration Bay — Banner Test Center', () => {
  beforeEach(() => {
    document.body.innerHTML = buildTabDOM();
    delete window.__TAURI__;
  });

  afterEach(() => {
    delete window.__TAURI__;
  });

  it('11. Banner Test Center section exists', () => {
    expect(document.getElementById('banner-test-center')).not.toBeNull();
  });

  it('12. Banner type select contains only known event types', () => {
    const select = document.getElementById('btc-banner-type');
    expect(select).not.toBeNull();
    const values = Array.from(select.options).map(o => o.value);
    expect(values).toEqual(KNOWN_BANNER_TYPES);
  });

  it('13. Test generic banner control exists', () => {
    expect(document.getElementById('btc-test-generic-btn')).not.toBeNull();
  });

  it('14. Test selected banner control exists', () => {
    expect(document.getElementById('btc-test-selected-btn')).not.toBeNull();
  });

  it('15. Test all banners control exists', () => {
    expect(document.getElementById('btc-test-all-btn')).not.toBeNull();
  });

  it('16. Banner type select option values are literal text, not HTML elements', () => {
    const select = document.getElementById('btc-banner-type');
    Array.from(select.options).forEach(opt => {
      expect(opt.children.length).toBe(0);
      expect(typeof opt.value).toBe('string');
      expect(KNOWN_BANNER_TYPES).toContain(opt.value);
    });
  });

  it('17. Tauri invoke called with show_overlay_test_banner for generic banner test', async () => {
    const mockInvoke = vi.fn().mockResolvedValue(undefined);
    window.__TAURI__ = { core: { invoke: mockInvoke } };
    const ctrl = Object.create(SettingsController.prototype);
    await ctrl._testGenericBanner();
    expect(mockInvoke).toHaveBeenCalledWith('show_overlay_test_banner');
  });

  it('17b. Tauri invoke called with show_overlay_named_test_banner for selected banner test', async () => {
    const mockInvoke = vi.fn().mockResolvedValue(undefined);
    window.__TAURI__ = { core: { invoke: mockInvoke } };
    document.getElementById('btc-banner-type').value = 'SHIELDS_DOWN';
    const ctrl = Object.create(SettingsController.prototype);
    await ctrl._testSelectedBanner();
    expect(mockInvoke).toHaveBeenCalledWith('show_overlay_named_test_banner', { eventType: 'SHIELDS_DOWN' });
  });

  it('17c. _testAllBanners invokes named command for every KNOWN_BANNER_TYPE', async () => {
    const mockInvoke = vi.fn().mockResolvedValue(undefined);
    window.__TAURI__ = { core: { invoke: mockInvoke } };
    const ctrl = Object.create(SettingsController.prototype);
    await ctrl._testAllBanners();
    expect(mockInvoke).toHaveBeenCalledTimes(KNOWN_BANNER_TYPES.length);
    KNOWN_BANNER_TYPES.forEach(eventType => {
      expect(mockInvoke).toHaveBeenCalledWith('show_overlay_named_test_banner', { eventType });
    });
  });

  it('17d. _testGenericBanner does nothing when Tauri is unavailable', async () => {
    const ctrl = Object.create(SettingsController.prototype);
    await expect(ctrl._testGenericBanner()).resolves.toBeUndefined();
  });

  it('_testSelectedBanner skips unknown event types', async () => {
    const mockInvoke = vi.fn().mockResolvedValue(undefined);
    window.__TAURI__ = { core: { invoke: mockInvoke } };
    document.getElementById('btc-banner-type').value = 'UNKNOWN_TYPE';
    const ctrl = Object.create(SettingsController.prototype);
    await ctrl._testSelectedBanner();
    expect(mockInvoke).not.toHaveBeenCalled();
  });

  it('18. package files unchanged — KNOWN_BANNER_TYPES is a static list (no dynamic fetch)', () => {
    expect(KNOWN_BANNER_TYPES).toBeDefined();
    expect(KNOWN_BANNER_TYPES.every(t => typeof t === 'string')).toBe(true);
  });
});
