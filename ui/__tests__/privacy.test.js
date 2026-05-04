import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import fs from 'fs';
import '../views/privacy.js';

const indexHtml = fs.readFileSync('ui/index.html', 'utf8');

// ── PB05-09: Data Firewall identity in index.html ─────────────────────────

describe('Privacy — Data Firewall identity (index.html)', () => {
  it('Data Firewall kicker exists in index.html', () => {
    expect(indexHtml).toContain('Data Firewall');
  });

  it('local-only by default statement exists in index.html', () => {
    expect(indexHtml).toContain('local-only by default');
  });

  it('#privacy-toggles-list exists in index.html', () => {
    expect(indexHtml).toContain('id="privacy-toggles-list"');
  });

  it('#view-data-flows-btn exists in index.html', () => {
    expect(indexHtml).toContain('id="view-data-flows-btn"');
  });

  it('#data-flows-modal exists in index.html', () => {
    expect(indexHtml).toContain('id="data-flows-modal"');
  });

  it('#delete-confirm-modal exists in index.html (two-stage delete)', () => {
    expect(indexHtml).toContain('id="delete-confirm-modal"');
  });

  it('#delete-confirm-1st-btn and #delete-confirm-2nd-btn both exist in index.html', () => {
    expect(indexHtml).toContain('id="delete-confirm-1st-btn"');
    expect(indexHtml).toContain('id="delete-confirm-2nd-btn"');
  });

  it('#export-data-btn exists in index.html', () => {
    expect(indexHtml).toContain('id="export-data-btn"');
  });

  it('#delete-data-btn exists in index.html', () => {
    expect(indexHtml).toContain('id="delete-data-btn"');
  });

  it('toggle endpoint path /week13/privacy/toggles not changed in controller', () => {
    const privacyJs = fs.readFileSync('ui/views/privacy.js', 'utf8');
    expect(privacyJs).toContain('/week13/privacy/toggles');
  });

  it('export endpoint path /week13/privacy/export not changed in controller', () => {
    const privacyJs = fs.readFileSync('ui/views/privacy.js', 'utf8');
    expect(privacyJs).toContain('/week13/privacy/export');
  });

  it('delete endpoint path /week13/privacy/delete not changed in controller', () => {
    const privacyJs = fs.readFileSync('ui/views/privacy.js', 'utf8');
    expect(privacyJs).toContain('/week13/privacy/delete');
  });
});

const { PrivacyController } = globalThis.__privacyExports ?? {};

describe('PrivacyController', () => {
  it('is exported via test hook', () => {
    expect(PrivacyController).toBeDefined();
    expect(typeof PrivacyController).toBe('function');
  });
});

describe('PrivacyController.createToggleCard', () => {
  let ctrl;

  beforeEach(() => {
    ctrl = Object.create(PrivacyController.prototype);
  });

  it('renders toggle label via textContent for a normal key', () => {
    const card = ctrl.createToggleCard('eddn_submission', {
      enabled: false,
      description: 'Submit market prices to EDDN.',
    });
    const label = card.querySelector('.toggle-label');
    expect(label).not.toBeNull();
    expect(label.textContent).toBe('EDDN Market Data');
    expect(label.innerHTML).not.toContain('<img');
    expect(label.innerHTML).not.toContain('<script');
  });

  it('defaults checkbox to unchecked when enabled is false', () => {
    const card = ctrl.createToggleCard('edsm_tracking', {
      enabled: false,
      description: 'Send system visits to EDSM.',
    });
    const checkbox = card.querySelector('input[type="checkbox"]');
    expect(checkbox).not.toBeNull();
    expect(checkbox.checked).toBe(false);
  });

  it('renders description via textContent, not innerHTML', () => {
    const card = ctrl.createToggleCard('crash_reports', {
      enabled: false,
      description: 'Send crash reports.',
    });
    const desc = card.querySelector('.toggle-description');
    expect(desc.textContent).toBe('Send crash reports.');
    expect(desc.innerHTML).not.toContain('<');
  });

  it('renders malicious description as literal text, creates no img or script nodes', () => {
    const card = ctrl.createToggleCard('usage_analytics', {
      enabled: false,
      description: '<img src=x onerror=alert(1)>',
    });
    expect(card.querySelector('img')).toBeNull();
    expect(card.querySelector('script')).toBeNull();
    const desc = card.querySelector('.toggle-description');
    expect(desc.textContent).toBe('<img src=x onerror=alert(1)>');
  });
});

describe('PrivacyController - bridge readiness', () => {
  let ctrl;
  let originalFetch;

  beforeEach(() => {
    document.body.innerHTML = '<div id="privacy-toggles-list"></div>';
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
    ctrl = Object.create(PrivacyController.prototype);
    expect(ctrl.apiBase).toBeNull();
  });

  it('apiBase uses Shell.httpBase when available', () => {
    window.Shell = { httpBase: 'http://127.0.0.1:7777' };
    ctrl = Object.create(PrivacyController.prototype);
    expect(ctrl.apiBase).toBe('http://127.0.0.1:7777');
  });

  it('apiBase uses OMNICOVAS_PORT when Shell is absent', () => {
    window.OMNICOVAS_PORT = 9001;
    ctrl = Object.create(PrivacyController.prototype);
    expect(ctrl.apiBase).toBe('http://127.0.0.1:9001');
  });

  it('apiUrl returns null when bridge is not ready', () => {
    ctrl = Object.create(PrivacyController.prototype);
    expect(ctrl.apiUrl('/week13/privacy/toggles')).toBeNull();
  });

  it('fetch is NOT called before bridge is ready', async () => {
    ctrl = Object.create(PrivacyController.prototype);
    ctrl.deleteConfirmStage = 0;
    await ctrl.init();
    expect(globalThis.fetch).not.toHaveBeenCalled();
  });

  it('init shows waiting state in privacy-toggles-list when bridge is not ready', async () => {
    ctrl = Object.create(PrivacyController.prototype);
    ctrl.deleteConfirmStage = 0;
    await ctrl.init();
    const list = document.getElementById('privacy-toggles-list');
    expect(list.textContent).toContain('Waiting for OmniCOVAS bridge');
  });

  it('post-bridge apiUrl never uses port 8000', () => {
    window.OMNICOVAS_PORT = 9001;
    ctrl = Object.create(PrivacyController.prototype);
    const url = ctrl.apiUrl('/week13/privacy/toggles');
    expect(url).not.toContain(':8000');
    expect(url).toContain('9001');
  });
});
