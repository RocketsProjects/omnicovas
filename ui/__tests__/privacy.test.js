import { describe, it, expect, beforeEach } from 'vitest';
import '../views/privacy.js';

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
