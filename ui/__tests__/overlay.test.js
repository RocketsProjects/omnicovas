import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { renderBanner, showBanner, dismissBanner, CRITICAL_EVENTS, _resetState } from '../overlay.js';

beforeEach(() => {
  _resetState();
  document.body.innerHTML = '<div id="overlay-container"></div>';
});

describe('renderBanner', () => {
  it('renders numeric value with percent sign', () => {
    renderBanner({
      eventType: 'HULL_CRITICAL_10',
      config: { icon: '⚠', label: 'HULL CRITICAL', severity: 'critical', priority: 1, duration: 30000 },
      value: 10,
    });
    expect(document.querySelector('.banner-value').textContent).toBe('10%');
  });

  it('renders <script> payload as text, no script element injected', () => {
    renderBanner({
      eventType: 'OMNICOVAS_TEST',
      config: { icon: '⚙', label: 'TEST', severity: 'warning', priority: 99, duration: 1000 },
      value: '<script>alert("xss")</script>',
    });
    expect(document.querySelector('.banner-value').textContent).toBe('<script>alert("xss")</script>');
    expect(document.querySelector('.banner-value script')).toBeNull();
    expect(document.querySelectorAll('script').length).toBe(0);
  });

  it('renders <img onerror> payload as text, no img element injected', () => {
    renderBanner({
      eventType: 'OMNICOVAS_TEST',
      config: { icon: '⚙', label: 'TEST', severity: 'warning', priority: 99, duration: 1000 },
      value: '<img src=x onerror=alert(1)>',
    });
    expect(document.querySelector('.banner-value').textContent).toBe('<img src=x onerror=alert(1)>');
    expect(document.querySelector('.banner-value img')).toBeNull();
    expect(document.querySelectorAll('img').length).toBe(0);
  });

  it('renders null value as empty string, not literal "null"', () => {
    renderBanner({
      eventType: 'OMNICOVAS_TEST',
      config: { icon: '⚙', label: 'TEST', severity: 'warning', priority: 99, duration: 1000 },
      value: null,
    });
    expect(document.querySelector('.banner-value').textContent).toBe('');
  });
});

describe('CRITICAL_EVENTS', () => {
  const KNOWN = [
    'HULL_CRITICAL_10', 'SHIELDS_DOWN', 'HULL_CRITICAL_25', 'FUEL_CRITICAL',
    'MODULE_CRITICAL', 'FUEL_LOW', 'HEAT_WARNING', 'HEAT_DAMAGE', 'OMNICOVAS_TEST',
  ];

  it('exports CRITICAL_EVENTS with all 9 known types', () => {
    expect(CRITICAL_EVENTS).toBeDefined();
    KNOWN.forEach(type => expect(CRITICAL_EVENTS).toHaveProperty(type));
  });

  it('each event config has icon, label, severity, duration, priority', () => {
    KNOWN.forEach(type => {
      const cfg = CRITICAL_EVENTS[type];
      expect(typeof cfg.icon).toBe('string');
      expect(typeof cfg.label).toBe('string');
      expect(typeof cfg.severity).toBe('string');
      expect(typeof cfg.duration).toBe('number');
      expect(typeof cfg.priority).toBe('number');
    });
  });
});

describe('showBanner and rendering', () => {
  it('renders a banner with expected structure and text', () => {
    showBanner('OMNICOVAS_TEST', 'READY');
    const banner = document.querySelector('.banner');
    expect(banner).not.toBeNull();
    expect(banner.querySelector('.banner-source').textContent).toBe('OmniCOVAS');
    expect(banner.querySelector('.banner-label').textContent).toBe('OMNICOVAS TEST BANNER');
    expect(banner.querySelector('.banner-value').textContent).toBe('READY');
  });

  it('renders hostile values as text, not HTML', () => {
    showBanner('OMNICOVAS_TEST', '<b>XSS</b>');
    const value = document.querySelector('.banner-value');
    expect(value.textContent).toBe('<b>XSS</b>');
    expect(value.innerHTML).not.toContain('<b>');
  });
});

describe('dismissBanner', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    document.body.innerHTML = '<div id="overlay-container"></div>';
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('removes the banner element from the DOM on dismiss', () => {
    showBanner('OMNICOVAS_TEST', 'READY');
    expect(document.querySelector('.banner')).not.toBeNull();

    dismissBanner();
    expect(document.querySelector('.banner')).toBeNull();
  });

  it('leaves overlay-container empty after dismiss with no queued banners', () => {
    showBanner('OMNICOVAS_TEST', 'READY');
    dismissBanner();
    expect(document.getElementById('overlay-container').children.length).toBe(0);
  });
});
