/**
 * OmniCOVAS Icon System Tests
 */

import { describe, it, expect, beforeEach } from 'vitest';
import fs from 'fs';

// Helper to load icons.js into the happy-dom environment
function loadIcons() {
  const code = fs.readFileSync('ui/components/icons.js', 'utf8');
  // eval the code in the current context which has window/document from happy-dom
  eval(code);
}

describe('OmniIcons', () => {
  beforeEach(() => {
    // Clear document body between tests
    document.body.innerHTML = '';
    loadIcons();
  });

  it('export exists after loading icons.js', () => {
    expect(window.OmniIcons).toBeDefined();
  });

  it('names includes all required names', () => {
    const required = [
      'dashboard', 'activity-log', 'settings', 'privacy', 'resources',
      'credits', 'future-systems', 'combat', 'exploration', 'trade-mining',
      'squadron', 'engineering', 'powerplay-bgs', 'ship', 'shield', 'fuel',
      'heat', 'cargo', 'modules', 'pips', 'rebuy', 'connection', 'warning',
      'critical', 'lock', 'chevron', 'test-banner'
    ];
    const names = window.OmniIcons.names;
    required.forEach(name => {
      expect(names).toContain(name);
    });
  });

  it('has("dashboard") returns true', () => {
    expect(window.OmniIcons.has('dashboard')).toBe(true);
  });

  it('create("dashboard") returns an SVG element', () => {
    const svg = window.OmniIcons.create('dashboard');
    expect(svg.tagName.toLowerCase()).toBe('svg');
    // Namespace check
    expect(svg.namespaceURI).toContain('svg');
  });

  it('SVG uses viewBox="0 0 24 24"', () => {
    const svg = window.OmniIcons.create('dashboard');
    expect(svg.getAttribute('viewBox')).toBe('0 0 24 24');
  });

  it('SVG uses currentColor', () => {
    const svg = window.OmniIcons.create('dashboard');
    expect(svg.getAttribute('stroke')).toBe('currentColor');
  });

  it('unknown icon name does not throw', () => {
    expect(() => window.OmniIcons.create('non-existent')).not.toThrow();
  });

  it('unknown icon returns a safe fallback marked with data-icon-fallback', () => {
    const svg = window.OmniIcons.create('non-existent');
    expect(svg).not.toBeNull();
    expect(svg.getAttribute('data-icon-fallback')).toBe('true');
  });

  it('mountAll() replaces placeholders with SVG child', () => {
    const container = document.createElement('div');
    container.innerHTML = '<span class="ocv-icon" data-icon="dashboard">Old Content</span>';
    document.body.appendChild(container);

    window.OmniIcons.mountAll(container);

    const span = container.querySelector('.ocv-icon');
    expect(span.querySelector('svg')).not.toBeNull();
    expect(span.textContent).not.toContain('Old Content');
  });

  it('no dynamic HTML path exists in icons.js', () => {
    const code = fs.readFileSync('ui/components/icons.js', 'utf8');
    const sinks = ['innerHTML', 'outerHTML', 'insertAdjacentHTML', 'DOMParser'];
    sinks.forEach(sink => {
      expect(code).not.toContain(sink);
    });
  });
});
