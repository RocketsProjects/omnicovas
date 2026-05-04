import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
import '../views/dashboard.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

const exports = globalThis.__dashboardExports;
const renderCommandSummary = exports?.renderCommandSummary;
const renderShipSchematic  = exports?.renderShipSchematic;
const renderHeat           = exports?.renderHeat;
const resetCache           = exports?.__resetSchematicCache;

// ─── Command summary band ──────────────────────────────────────────────────

describe('renderCommandSummary', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div id="dash-command-summary">
        <span id="dash-summary-ship"></span>
        <span id="dash-summary-location"></span>
        <span id="dash-summary-hull"></span>
        <span id="dash-summary-shields"></span>
        <span id="dash-summary-fuel"></span>
        <span id="dash-summary-heat"></span>
        <span id="dash-summary-alerts"></span>
      </div>`;
  });

  it('renders ship name and location from state', () => {
    renderCommandSummary({ ship_name: 'My Ship', current_system: 'Sol' }, null);
    expect(document.getElementById('dash-summary-ship').textContent).toBe('My Ship');
    expect(document.getElementById('dash-summary-location').textContent).toBe('Sol');
  });

  it('falls back to ship_type when ship_name is absent', () => {
    renderCommandSummary({ ship_type: 'Sidewinder' }, null);
    expect(document.getElementById('dash-summary-ship').textContent).toBe('Sidewinder');
  });

  it('shows Unknown ship when no identity data', () => {
    renderCommandSummary({}, null);
    expect(document.getElementById('dash-summary-ship').textContent).toBe('Unknown ship');
  });

  it('shows Unknown system when current_system is absent', () => {
    renderCommandSummary({}, null);
    expect(document.getElementById('dash-summary-location').textContent).toBe('Unknown system');
  });

  it('shows hull percentage when available', () => {
    renderCommandSummary({ hull_health: 85.0 }, null);
    expect(document.getElementById('dash-summary-hull').textContent).toBe('85.0%');
  });

  it('shows dash for hull when hull_health is absent', () => {
    renderCommandSummary({}, null);
    expect(document.getElementById('dash-summary-hull').textContent).toBe('—');
  });

  it('shows shields UP with ok class', () => {
    renderCommandSummary({ shield_up: true }, null);
    const el = document.getElementById('dash-summary-shields');
    expect(el.textContent).toBe('UP');
    expect(el.className).toContain('ok');
  });

  it('shows shields DOWN with critical class', () => {
    renderCommandSummary({ shield_up: false }, null);
    const el = document.getElementById('dash-summary-shields');
    expect(el.textContent).toBe('DOWN');
    expect(el.className).toContain('critical');
  });

  it('shows shields dash with unknown class when shield_up is null', () => {
    renderCommandSummary({ shield_up: null }, null);
    const el = document.getElementById('dash-summary-shields');
    expect(el.textContent).toBe('—');
    expect(el.className).toContain('unknown');
  });

  it('shows heat percentage when heat data is present', () => {
    renderCommandSummary({}, { level_pct: 42 });
    expect(document.getElementById('dash-summary-heat').textContent).toBe('42%');
  });

  it('shows heat dash when heat is null', () => {
    renderCommandSummary({}, null);
    expect(document.getElementById('dash-summary-heat').textContent).toBe('—');
  });

  it('does not update heat summary when heat is undefined (partial refresh)', () => {
    const el = document.getElementById('dash-summary-heat');
    el.textContent = 'preserved';
    renderCommandSummary({}, undefined);
    expect(el.textContent).toBe('preserved');
  });

  it('shows WANTED alert when is_wanted_in_system', () => {
    renderCommandSummary({ is_wanted_in_system: true }, null);
    const el = document.getElementById('dash-summary-alerts');
    expect(el.textContent).toBe('WANTED');
    expect(el.className).toContain('critical');
  });

  it('shows HULL CRITICAL alert at or below 10%', () => {
    renderCommandSummary({ hull_health: 10, is_wanted_in_system: false }, null);
    const el = document.getElementById('dash-summary-alerts');
    expect(el.textContent).toBe('HULL CRITICAL');
  });

  it('shows dash alert when status is nominal', () => {
    renderCommandSummary({ hull_health: 90, is_wanted_in_system: false }, null);
    expect(document.getElementById('dash-summary-alerts').textContent).toBe('—');
  });
});

// ─── Schematic integration ────────────────────────────────────────────────

describe('renderShipSchematic', () => {
  beforeEach(() => {
    resetCache?.();
    document.body.innerHTML = `
      <div id="dash-ship-schematic"></div>
      <p id="dash-schematic-status"></p>`;

    globalThis.OmniShipSchematics = {
      resolveShipKey(raw) {
        if (!raw) return 'generic';
        const l = String(raw).toLowerCase();
        if (l === 'sidewinder') return 'sidewinder';
        return 'generic';
      },
      getSchematic(raw) {
        const key = this.resolveShipKey(raw);
        return { id: key, shapes: [], hotspots: [], viewBox: '0 0 100 100', displayName: key };
      },
      hasSchematic(raw) {
        const key = this.resolveShipKey(raw);
        return key !== 'generic';
      },
    };

    globalThis.OmniShipSchematic = {
      mount(container, shipType) {
        const div = document.createElement('div');
        div.setAttribute('data-ship-schematic', globalThis.OmniShipSchematics.resolveShipKey(shipType));
        container.appendChild(div);
      },
    };
  });

  afterEach(() => {
    delete globalThis.OmniShipSchematics;
    delete globalThis.OmniShipSchematic;
  });

  it('mounts generic schematic when ship_type is absent', () => {
    renderShipSchematic({});
    const mounted = document.querySelector('[data-ship-schematic]');
    expect(mounted).not.toBeNull();
    expect(mounted.getAttribute('data-ship-schematic')).toBe('generic');
  });

  it('sets generic fallback status text for unknown ship', () => {
    renderShipSchematic({ ship_type: 'UnknownShip999' });
    expect(document.getElementById('dash-schematic-status').textContent)
      .toContain('Generic schematic active');
  });

  it('sets Sidewinder status text when ship resolves to Sidewinder', () => {
    resetCache?.();
    renderShipSchematic({ ship_type: 'Sidewinder' });
    const status = document.getElementById('dash-schematic-status').textContent;
    expect(status).toContain('Sidewinder');
    expect(status).not.toContain('not yet available');
  });

  it('shows unavailable message when OmniShipSchematic is absent', () => {
    delete globalThis.OmniShipSchematic;
    resetCache?.();
    renderShipSchematic({ ship_type: 'Sidewinder' });
    expect(document.getElementById('dash-schematic-status').textContent)
      .toBe('Ship schematic unavailable');
  });

  it('does not throw when frame element is absent', () => {
    document.body.innerHTML = '';
    expect(() => renderShipSchematic({ ship_type: 'Sidewinder' })).not.toThrow();
  });

  it('does not re-mount when ship type has not changed', () => {
    renderShipSchematic({ ship_type: 'Sidewinder' });
    renderShipSchematic({ ship_type: 'Sidewinder' });
    const mounted = document.querySelectorAll('[data-ship-schematic]');
    expect(mounted.length).toBe(1);
  });
});

// ─── index.html DOM structure ────────────────────────────────────────────

describe('index.html dashboard DOM structure', () => {
  let html;
  beforeEach(() => {
    html = readFileSync(resolve(__dirname, '../index.html'), 'utf8');
  });

  it('has schematic frame container', () => {
    expect(html).toContain('id="dash-schematic-frame"');
  });

  it('has ship schematic mount point', () => {
    expect(html).toContain('id="dash-ship-schematic"');
  });

  it('has schematic status element', () => {
    expect(html).toContain('id="dash-schematic-status"');
  });

  it('has Hull & Shields callout panel', () => {
    expect(html).toContain('id="dash-panel-hull-shields"');
  });

  it('has Fuel & Jump callout panel', () => {
    expect(html).toContain('id="dash-panel-fuel-jump"');
  });

  it('has Heat / Core callout panel', () => {
    expect(html).toContain('id="dash-panel-heat-core"');
  });

  it('has Cargo callout panel', () => {
    expect(html).toContain('id="dash-panel-cargo"');
  });

  it('has Power Distribution callout panel', () => {
    expect(html).toContain('id="dash-panel-pips"');
  });

  it('has Module Health callout panel', () => {
    expect(html).toContain('id="dash-panel-modules"');
  });

  it('has Rebuy / Insurance callout panel', () => {
    expect(html).toContain('id="dash-panel-rebuy"');
  });

  it('has command summary band', () => {
    expect(html).toContain('id="dash-command-summary"');
  });

  it('has dashboard.css stylesheet link', () => {
    expect(html).toContain('styles/dashboard.css');
  });
});

// ─── Heat absence truthfulness ──────────────────────────────────────────

describe('renderHeat absence states', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <span id="dash-heat-value"></span>
      <div id="dash-heat-bar" style="width:0%"></div>
      <span id="dash-heat-trend"></span>
      <span id="dash-heat-state"></span>
      <canvas id="dash-heat-sparkline"></canvas>
      <p id="dash-heat-absence"></p>`;
  });

  it('does not show NORMAL badge when heat data is fully absent', () => {
    renderHeat({ level_pct: null, state: null, samples: [], trend: null });
    expect(document.getElementById('dash-heat-state').textContent).toBe('');
  });

  it('shows NORMAL badge when heat pct is present but state is null', () => {
    renderHeat({ level_pct: 45, state: null, samples: [], trend: null });
    expect(document.getElementById('dash-heat-state').textContent).toBe('NORMAL');
  });

  it('shows WARNING badge when state is warning', () => {
    renderHeat({ level_pct: 82, state: 'warning', samples: [], trend: null });
    expect(document.getElementById('dash-heat-state').textContent).toBe('WARNING');
  });

  it('hides heat absence element when heat data is rendered', () => {
    const absenceEl = document.getElementById('dash-heat-absence');
    absenceEl.style.display = '';
    renderHeat({ level_pct: 50, state: null, samples: [], trend: null });
    expect(absenceEl.style.display).toBe('none');
  });
});

// ─── Safe rendering (XSS guard) ─────────────────────────────────────────

describe('safe rendering guards', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <span id="dash-cargo-count"></span>
      <ul id="dash-cargo-list"></ul>`;
  });

  it('renders malicious cargo name as literal text, not HTML', () => {
    const { renderCargo } = globalThis.__dashboardExports;
    renderCargo({}, [{ name: '<img src=x onerror=alert(1)>', count: 1 }]);
    const list = document.getElementById('dash-cargo-list');
    expect(list.querySelector('img')).toBeNull();
    expect(list.querySelector('.field-label').textContent)
      .toBe('<img src=x onerror=alert(1)>');
  });
});

// ─── Bridge hydration (existing behaviour) ──────────────────────────────

describe('bridge hydration', () => {
  it('__dashboardExports is defined after module load', () => {
    expect(globalThis.__dashboardExports).toBeDefined();
    expect(typeof globalThis.__dashboardExports.renderCargo).toBe('function');
    expect(typeof globalThis.__dashboardExports.renderCommandSummary).toBe('function');
    expect(typeof globalThis.__dashboardExports.renderShipSchematic).toBe('function');
    expect(typeof globalThis.__dashboardExports.renderHeat).toBe('function');
  });
});

// ─── PB05-07: Panel toggle behaviour ───────────────────────────────────

const initializeDashboardPanelToggles = exports?.initializeDashboardPanelToggles;
const setDashboardPanelVisibility      = exports?.setDashboardPanelVisibility;
const showAllDashboardPanels           = exports?.showAllDashboardPanels;
const resetToggleState                 = exports?.__resetToggleState;

function buildToggleDom() {
  document.body.innerHTML = `
    <div id="dash-schematic-frame">
      <div id="dash-ship-schematic">
        <div class="ship-schematic">
          <div class="ship-schematic-hotspots">
            <button class="ship-schematic-hotspot-button"
                    aria-controls="dash-panel-hull-shields"
                    aria-expanded="true"
                    data-hotspot-id="hull">
              <span class="ship-schematic-hotspot-label">HULL</span>
            </button>
            <button class="ship-schematic-hotspot-button"
                    aria-controls="dash-panel-hull-shields"
                    aria-expanded="true"
                    data-hotspot-id="shield">
              <span class="ship-schematic-hotspot-label">SHIELD</span>
            </button>
            <button class="ship-schematic-hotspot-button"
                    aria-controls="dash-panel-fuel-jump"
                    aria-expanded="true"
                    data-hotspot-id="fuel">
              <span class="ship-schematic-hotspot-label">FUEL</span>
            </button>
            <button class="ship-schematic-hotspot-button"
                    aria-controls="dash-panel-heat-core"
                    aria-expanded="true"
                    data-hotspot-id="heat">
              <span class="ship-schematic-hotspot-label">HEAT</span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <button id="dash-show-all-systems-btn" type="button">Show all systems</button>
    <article id="dash-panel-hull-shields"></article>
    <article id="dash-panel-fuel-jump"></article>
    <article id="dash-panel-heat-core"></article>
    <article id="dash-panel-cargo"></article>
    <article id="dash-panel-modules"></article>
    <article id="dash-panel-pips"></article>`;
}

describe('PB05-07 panel toggle behaviour', () => {
  beforeEach(() => {
    resetToggleState?.();
    buildToggleDom();
    initializeDashboardPanelToggles?.();
  });

  it('all callout panels are visible by default (no hidden attribute or hidden class)', () => {
    ['dash-panel-hull-shields', 'dash-panel-fuel-jump', 'dash-panel-heat-core'].forEach(id => {
      const panel = document.getElementById(id);
      expect(panel.hasAttribute('hidden')).toBe(false);
      expect(panel.classList.contains('dashboard-panel-hidden')).toBe(false);
    });
  });

  it('clicking the fuel hotspot hides the Fuel & Jump panel', () => {
    const fuelBtn = document.querySelector('[data-hotspot-id="fuel"]');
    fuelBtn.click();
    const panel = document.getElementById('dash-panel-fuel-jump');
    expect(panel.hasAttribute('hidden') || panel.classList.contains('dashboard-panel-hidden')).toBe(true);
  });

  it('fuel hotspot aria-expanded becomes false when panel is hidden', () => {
    const fuelBtn = document.querySelector('[data-hotspot-id="fuel"]');
    fuelBtn.click();
    expect(fuelBtn.getAttribute('aria-expanded')).toBe('false');
  });

  it('clicking the fuel hotspot again shows the Fuel & Jump panel', () => {
    const fuelBtn = document.querySelector('[data-hotspot-id="fuel"]');
    fuelBtn.click();
    fuelBtn.click();
    const panel = document.getElementById('dash-panel-fuel-jump');
    expect(panel.hasAttribute('hidden')).toBe(false);
    expect(panel.classList.contains('dashboard-panel-hidden')).toBe(false);
  });

  it('fuel hotspot aria-expanded returns to true when panel is shown again', () => {
    const fuelBtn = document.querySelector('[data-hotspot-id="fuel"]');
    fuelBtn.click();
    fuelBtn.click();
    expect(fuelBtn.getAttribute('aria-expanded')).toBe('true');
  });

  it('Show all systems button restores all panels to visible', () => {
    const fuelBtn = document.querySelector('[data-hotspot-id="fuel"]');
    const hullBtn = document.querySelector('[data-hotspot-id="hull"]');
    fuelBtn.click();
    hullBtn.click();
    document.getElementById('dash-show-all-systems-btn').click();
    ['dash-panel-hull-shields', 'dash-panel-fuel-jump'].forEach(id => {
      const panel = document.getElementById(id);
      expect(panel.hasAttribute('hidden')).toBe(false);
      expect(panel.classList.contains('dashboard-panel-hidden')).toBe(false);
    });
  });

  it('Show all systems button sets all hotspot aria-expanded to true', () => {
    const fuelBtn = document.querySelector('[data-hotspot-id="fuel"]');
    fuelBtn.click();
    document.getElementById('dash-show-all-systems-btn').click();
    document.querySelectorAll('.ship-schematic-hotspot-button').forEach(btn => {
      expect(btn.getAttribute('aria-expanded')).toBe('true');
    });
  });

  it('clicking a hotspot with a missing target panel does not throw', () => {
    const orphanBtn = document.createElement('button');
    orphanBtn.className = 'ship-schematic-hotspot-button';
    orphanBtn.setAttribute('aria-controls', 'panel-does-not-exist');
    orphanBtn.setAttribute('aria-expanded', 'true');
    document.getElementById('dash-ship-schematic').appendChild(orphanBtn);
    expect(() => orphanBtn.click()).not.toThrow();
  });

  it('both hull and shield hotspots control the hull-shields panel', () => {
    const shieldBtn = document.querySelector('[data-hotspot-id="shield"]');
    shieldBtn.click();
    const panel = document.getElementById('dash-panel-hull-shields');
    expect(panel.hasAttribute('hidden') || panel.classList.contains('dashboard-panel-hidden')).toBe(true);
    const hullBtn = document.querySelector('[data-hotspot-id="hull"]');
    expect(hullBtn.getAttribute('aria-expanded')).toBe('false');
  });

  it('toggle initialization does not add duplicate listeners on repeated calls', () => {
    resetToggleState?.();
    buildToggleDom();
    initializeDashboardPanelToggles?.();
    initializeDashboardPanelToggles?.();
    initializeDashboardPanelToggles?.();
    const fuelBtn = document.querySelector('[data-hotspot-id="fuel"]');
    fuelBtn.click();
    const panel = document.getElementById('dash-panel-fuel-jump');
    expect(panel.hasAttribute('hidden') || panel.classList.contains('dashboard-panel-hidden')).toBe(true);
    fuelBtn.click();
    expect(panel.hasAttribute('hidden')).toBe(false);
    expect(panel.classList.contains('dashboard-panel-hidden')).toBe(false);
  });

  it('setDashboardPanelVisibility hides and shows a panel without throwing', () => {
    setDashboardPanelVisibility?.('dash-panel-heat-core', false);
    const panel = document.getElementById('dash-panel-heat-core');
    expect(panel.hasAttribute('hidden') || panel.classList.contains('dashboard-panel-hidden')).toBe(true);
    setDashboardPanelVisibility?.('dash-panel-heat-core', true);
    expect(panel.hasAttribute('hidden')).toBe(false);
  });

  it('setDashboardPanelVisibility with a missing id does not throw', () => {
    expect(() => setDashboardPanelVisibility?.('panel-nonexistent', false)).not.toThrow();
  });
});

// ─── PB05-07: Safe rendering and persistence guards ─────────────────────

describe('PB05-07 safe rendering and persistence guards', () => {
  it('dashboard.js source has no localStorage or sessionStorage references for toggle state', () => {
    const code = readFileSync('ui/views/dashboard.js', 'utf8');
    expect(code).not.toContain('localStorage');
    expect(code).not.toContain('sessionStorage');
  });

  it('dashboard.js source introduces no new unsafe HTML sinks beyond the existing classified innerHTML clear', () => {
    const code = readFileSync('ui/views/dashboard.js', 'utf8');
    expect(code).not.toContain('insertAdjacentHTML');
    expect(code).not.toContain('outerHTML');
  });

  it('hotspot controls in the schematic are real button elements', () => {
    buildToggleDom();
    const btns = document.querySelectorAll('.ship-schematic-hotspot-button');
    expect(btns.length).toBeGreaterThan(0);
    btns.forEach(btn => {
      expect(btn.tagName.toLowerCase()).toBe('button');
    });
  });
});
