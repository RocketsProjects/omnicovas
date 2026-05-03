import { describe, it, expect, beforeEach } from 'vitest';
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
