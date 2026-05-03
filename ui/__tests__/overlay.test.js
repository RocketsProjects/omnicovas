import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { renderBanner, showBanner, dismissBanner } from '../overlay.js';

beforeEach(() => {
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
