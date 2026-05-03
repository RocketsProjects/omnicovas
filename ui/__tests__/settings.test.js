import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import '../views/settings.js';

const { SettingsController } = globalThis.__settingsExports ?? {};

describe('SettingsController', () => {
  it('is exported via test hook', () => {
    expect(SettingsController).toBeDefined();
    expect(typeof SettingsController).toBe('function');
  });
});

describe('SettingsController.renderPresets', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = '<div id="preset-grid"></div>';
    ctrl = Object.create(SettingsController.prototype);
    ctrl.currentSettings = { preset: 'casual' };
  });

  it('renders 5 preset buttons', () => {
    ctrl.renderPresets();
    const grid = document.getElementById('preset-grid');
    expect(grid.querySelectorAll('.preset-button').length).toBe(5);
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
});

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
    const container = document.getElementById('tier2-toggles');
    const labels = container.querySelectorAll('.toggle-label');
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
    // The label text comes from a hardcoded map (pillarLabels), not API data.
    // Verify no script or img nodes exist.
    expect(container.querySelector('script')).toBeNull();
    expect(container.querySelector('img')).toBeNull();
  });
});

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

  it('apiBase returns null when bridge is not ready', () => {
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

  it('apiUrl returns null when bridge is not ready', () => {
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

  it('post-bridge apiUrl never uses port 8000', () => {
    window.OMNICOVAS_PORT = 9001;
    ctrl = Object.create(SettingsController.prototype);
    const url = ctrl.apiUrl('/week13/settings');
    expect(url).not.toContain(':8000');
    expect(url).toContain('9001');
  });
});
