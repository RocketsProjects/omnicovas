/**
 * OmniCOVAS Ship Schematic Registry + Component Tests
 * PB05-05: Ship Schematic Registry and Sidewinder MVP
 */

import { describe, it, expect, beforeEach } from 'vitest';
import fs from 'fs';

function loadSchematics() {
  const code = fs.readFileSync('ui/data/ship-schematics.js', 'utf8');
  eval(code);
}

function loadComponent() {
  const code = fs.readFileSync('ui/components/ship-schematic.js', 'utf8');
  eval(code);
}

// ── Registry tests ─────────────────────────────────────────────────────────

describe('OmniShipSchematics registry', () => {
  beforeEach(() => {
    delete window.OmniShipSchematics;
    loadSchematics();
  });

  it('window.OmniShipSchematics exists after loading ship-schematics.js', () => {
    expect(window.OmniShipSchematics).toBeDefined();
  });

  it('resolveShipKey("sidewinder") returns "sidewinder"', () => {
    expect(window.OmniShipSchematics.resolveShipKey('sidewinder')).toBe('sidewinder');
  });

  it('common sidewinder alias resolves to "sidewinder"', () => {
    expect(window.OmniShipSchematics.resolveShipKey('sidewinder_mk_i')).toBe('sidewinder');
  });

  it('case-variant alias SideWinder resolves to "sidewinder"', () => {
    expect(window.OmniShipSchematics.resolveShipKey('SideWinder')).toBe('sidewinder');
  });

  it('resolveShipKey with unsupported type returns "generic"', () => {
    expect(window.OmniShipSchematics.resolveShipKey('federal_corvette')).toBe('generic');
  });

  it('resolveShipKey with empty string returns "generic"', () => {
    expect(window.OmniShipSchematics.resolveShipKey('')).toBe('generic');
  });

  it('resolveShipKey with null returns "generic"', () => {
    expect(window.OmniShipSchematics.resolveShipKey(null)).toBe('generic');
  });

  it('getSchematic("sidewinder") returns the Sidewinder entry', () => {
    const s = window.OmniShipSchematics.getSchematic('sidewinder');
    expect(s.id).toBe('sidewinder');
    expect(s.displayName).toBe('Sidewinder');
  });

  it('getSchematic("unsupported_ship") returns the generic entry', () => {
    const s = window.OmniShipSchematics.getSchematic('unsupported_ship');
    expect(s.id).toBe('generic');
  });

  it('hasSchematic("sidewinder") is true', () => {
    expect(window.OmniShipSchematics.hasSchematic('sidewinder')).toBe(true);
  });

  it('hasSchematic("unsupported_ship") is false', () => {
    expect(window.OmniShipSchematics.hasSchematic('unsupported_ship')).toBe(false);
  });

  it('listSupported() includes "sidewinder" and "generic"', () => {
    const list = window.OmniShipSchematics.listSupported();
    expect(list).toContain('sidewinder');
    expect(list).toContain('generic');
  });

  it('Sidewinder entry includes all required hotspot IDs', () => {
    const s = window.OmniShipSchematics.getSchematic('sidewinder');
    const required = ['hull', 'shield', 'fuel', 'heat', 'cargo', 'modules', 'pips'];
    const ids = s.hotspots.map(h => h.id);
    required.forEach(id => {
      expect(ids).toContain(id);
    });
  });

  it('each Sidewinder hotspot has label, panelId, x, y, defaultExpanded', () => {
    const s = window.OmniShipSchematics.getSchematic('sidewinder');
    s.hotspots.forEach(h => {
      expect(typeof h.label).toBe('string');
      expect(h.label.length).toBeGreaterThan(0);
      expect(typeof h.panelId).toBe('string');
      expect(h.panelId.length).toBeGreaterThan(0);
      expect(typeof h.x).toBe('number');
      expect(typeof h.y).toBe('number');
      expect(typeof h.defaultExpanded).toBe('boolean');
    });
  });

  it('ship-schematics.js source has no unsafe rendering sinks', () => {
    const code = fs.readFileSync('ui/data/ship-schematics.js', 'utf8');
    const sinks = ['innerHTML', 'outerHTML', 'insertAdjacentHTML', 'DOMParser', 'template.innerHTML'];
    sinks.forEach(sink => {
      expect(code).not.toContain(sink);
    });
  });
});

// ── Component tests ────────────────────────────────────────────────────────

describe('OmniShipSchematic component', () => {
  beforeEach(() => {
    delete window.OmniShipSchematics;
    delete window.OmniShipSchematic;
    while (document.body.firstChild) {
      document.body.removeChild(document.body.firstChild);
    }
    loadSchematics();
    loadComponent();
  });

  it('window.OmniShipSchematic exists after loading ship-schematic.js', () => {
    expect(window.OmniShipSchematic).toBeDefined();
  });

  it('create("sidewinder") returns a wrapper div containing an SVG', () => {
    const el = window.OmniShipSchematic.create('sidewinder');
    expect(el).not.toBeNull();
    expect(el.tagName.toLowerCase()).toBe('div');
    expect(el.className).toContain('ship-schematic');
    expect(el.querySelector('svg')).not.toBeNull();
  });

  it('SVG uses the Sidewinder viewBox', () => {
    const el = window.OmniShipSchematic.create('sidewinder');
    const svg = el.querySelector('svg');
    expect(svg.getAttribute('viewBox')).toBe('0 0 1000 560');
  });

  it('create("unsupported_ship") renders the generic fallback schematic', () => {
    const el = window.OmniShipSchematic.create('unsupported_ship');
    expect(el.getAttribute('data-ship-schematic')).toBe('generic');
    expect(el.querySelector('svg')).not.toBeNull();
  });

  it('hotspot buttons are real button elements', () => {
    const el = window.OmniShipSchematic.create('sidewinder');
    const buttons = el.querySelectorAll('button');
    expect(buttons.length).toBeGreaterThan(0);
    buttons.forEach(btn => {
      expect(btn.tagName.toLowerCase()).toBe('button');
    });
  });

  it('hotspot buttons carry aria-label, aria-controls, aria-expanded, data-hotspot-id', () => {
    const el = window.OmniShipSchematic.create('sidewinder');
    const buttons = el.querySelectorAll('button');
    expect(buttons.length).toBeGreaterThan(0);
    buttons.forEach(btn => {
      expect(btn.getAttribute('aria-label')).toBeTruthy();
      expect(btn.getAttribute('aria-controls')).toBeTruthy();
      expect(btn.getAttribute('aria-expanded')).not.toBeNull();
      expect(btn.getAttribute('data-hotspot-id')).toBeTruthy();
    });
  });

  it('createHotspotButton does not throw for a valid hotspot', () => {
    const hotspot = {
      id: 'hull',
      panelId: 'panel-hull',
      label: 'Toggle hull integrity telemetry',
      x: 155,
      y: 195,
      defaultExpanded: true,
      className: 'ship-schematic-hotspot--hull'
    };
    expect(() => window.OmniShipSchematic.createHotspotButton(hotspot, {})).not.toThrow();
  });

  it('createHotspotButton returns a button with correct attributes', () => {
    const hotspot = {
      id: 'fuel',
      panelId: 'panel-fuel',
      label: 'Toggle fuel and jump telemetry',
      x: 845,
      y: 195,
      defaultExpanded: true,
      className: 'ship-schematic-hotspot--fuel'
    };
    const btn = window.OmniShipSchematic.createHotspotButton(hotspot, { viewBox: '0 0 1000 560' });
    expect(btn.tagName.toLowerCase()).toBe('button');
    expect(btn.getAttribute('data-hotspot-id')).toBe('fuel');
    expect(btn.getAttribute('aria-controls')).toBe('panel-fuel');
    expect(btn.getAttribute('aria-expanded')).toBe('true');
  });

  it('ship-schematic.js source has no unsafe rendering sinks', () => {
    const code = fs.readFileSync('ui/components/ship-schematic.js', 'utf8');
    const sinks = ['innerHTML', 'outerHTML', 'insertAdjacentHTML', 'DOMParser', 'template.innerHTML'];
    sinks.forEach(sink => {
      expect(code).not.toContain(sink);
    });
  });
});
