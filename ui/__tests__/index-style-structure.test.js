import { describe, it, expect, beforeAll } from 'vitest';
import fs from 'fs';

const indexHtml = fs.readFileSync('ui/index.html', 'utf8');

const NEW_STYLESHEETS = [
  'styles/forms.css',
  'styles/modals.css',
  'styles/pages.css',
  'styles/command-deck.css',
  'styles/confirmation-gate.css',
];

const LOAD_ORDER = [
  'styles/tokens.css',
  'styles/shell.css',
  'styles/components.css',
  'styles/forms.css',
  'styles/modals.css',
  'styles/pages.css',
  'styles/command-deck.css',
  'styles/confirmation-gate.css',
];

const REQUIRED_IDS = [
  'view-dashboard',
  'view-activity-log',
  'view-settings',
  'view-privacy',
  'view-resources',
  'view-credits',
  'onboarding-container',
];

const COMMAND_DECK_CLASSES = [
  '.ocv-page',
  '.ocv-page-header',
  '.ocv-page-title',
  '.ocv-page-kicker',
  '.ocv-page-subtitle',
  '.ocv-panel',
  '.ocv-panel-header',
  '.ocv-panel-title',
  '.ocv-panel-body',
  '.ocv-chip',
  '.ocv-chip-muted',
  '.ocv-chip-accent',
  '.ocv-chip-telemetry',
  '.ocv-chip-warning',
  '.ocv-chip-critical',
  '.ocv-command-summary',
  '.ocv-command-summary-grid',
  '.ocv-callout-panel',
  '.ocv-callout-line',
  '.ocv-schematic-frame',
  '.ocv-schematic-hotspot',
  '.ocv-hotspot-button',
  '.ocv-panel-zone',
  '.ocv-recorder-timeline',
  '.ocv-diagnostics-grid',
  '.ocv-firewall-map',
  '.ocv-config-tabs',
  '.ocv-registry-plaque',
];

// ─────────────────────────────────────────
describe('index.html — PB05-04 stylesheet links', () => {
  it('links all new PB05-04 stylesheets', () => {
    for (const sheet of NEW_STYLESHEETS) {
      expect(indexHtml, `missing href="${sheet}"`).toContain(`href="${sheet}"`);
    }
  });

  it('loads stylesheets in the correct cascade order', () => {
    const positions = LOAD_ORDER.map(s => indexHtml.indexOf(`href="${s}"`));
    for (let i = 1; i < positions.length; i++) {
      expect(
        positions[i],
        `${LOAD_ORDER[i]} must appear after ${LOAD_ORDER[i - 1]}`
      ).toBeGreaterThan(positions[i - 1]);
    }
  });

  it('preserves all route-critical view IDs', () => {
    for (const id of REQUIRED_IDS) {
      expect(indexHtml, `missing id="${id}"`).toContain(`id="${id}"`);
    }
  });
});

// ─────────────────────────────────────────
describe('command-deck.css — required primitive classes', () => {
  let css;

  beforeAll(() => {
    css = fs.readFileSync('ui/styles/command-deck.css', 'utf8');
  });

  it('defines all required primitive class selectors', () => {
    for (const cls of COMMAND_DECK_CLASSES) {
      expect(css, `missing selector ${cls}`).toContain(cls);
    }
  });

  it('uses only token variables — no hard-coded hex colors', () => {
    const hardcoded = css.match(/#[0-9a-fA-F]{3,6}(?![0-9a-fA-F])/g) || [];
    expect(hardcoded, 'found hard-coded hex colors: ' + hardcoded.join(', ')).toHaveLength(0);
  });
});

// ─────────────────────────────────────────
describe('new CSS files — exist on disk', () => {
  for (const sheet of NEW_STYLESHEETS) {
    it(`${sheet} exists`, () => {
      expect(() => fs.readFileSync(`ui/${sheet}`, 'utf8')).not.toThrow();
    });
  }
});

// ─────────────────────────────────────────
describe('extracted inline styles — no regressions', () => {
  it('log-clear-btn carries ocv-btn-ghost class (inline style extracted)', () => {
    expect(indexHtml).toContain('id="log-clear-btn" class="ocv-btn-ghost"');
  });

  it('res-refresh-btn carries ocv-btn-ghost class (inline style extracted)', () => {
    expect(indexHtml).toContain('id="res-refresh-btn" class="ocv-btn-ghost"');
  });

  it('log-search carries ocv-search-input class (inline style extracted)', () => {
    expect(indexHtml).toContain('id="log-search" class="ocv-search-input"');
  });

  it('log-controls carries ocv-form-row class (inline style extracted)', () => {
    expect(indexHtml).toContain('id="log-controls" class="ocv-form-row"');
  });
});

// ─────────────────────────────────────────
describe('PB05-09R — Route Visibility Repair', () => {
  it('pages.css contains .view.ocv-page:not(.active) guard', () => {
    const pagesCss = fs.readFileSync('ui/styles/pages.css', 'utf8');
    expect(pagesCss).toContain('.view.ocv-page:not(.active)');
    expect(pagesCss).toContain('display: none');
  });

  it('route sections with ocv-page are direct children of #content-area', () => {
    const mainMatch = indexHtml.match(/<main id="content-area" role="main">([\s\S]*?)<\/main>/);
    expect(mainMatch).not.toBeNull();
    const mainContent = mainMatch[1];

    // Assert they are present in the main content area
    expect(mainContent).toContain('id="view-activity-log" class="view ocv-page"');
    expect(mainContent).toContain('id="view-privacy" class="view ocv-page"');
    expect(mainContent).toContain('id="view-resources" class="view ocv-page"');

    // Heuristic: check they are not nested inside another div within main
    // Since we are doing a string match on raw HTML, we can check for direct-child-like appearance
    // In index.html they are at the first indentation level under <main>
    expect(mainContent).toMatch(/^\s+<section id="view-activity-log"/m);
    expect(mainContent).toMatch(/^\s+<section id="view-privacy"/m);
    expect(mainContent).toMatch(/^\s+<section id="view-resources"/m);
  });

  it('PB05-09 identity strings exist in index.html', () => {
    expect(indexHtml).toContain('Flight Recorder');
    expect(indexHtml).toContain('Diagnostics Console');
    expect(indexHtml).toContain('Data Firewall');
  });

  it('CSS route hiding contract: inactive .view.ocv-page must not be forced visible', () => {
    const pagesCss = fs.readFileSync('ui/styles/pages.css', 'utf8');
    // Ensure no plain .ocv-page { display: flex } in pages.css
    // We allow .ocv-page-wrap, .ocv-page-section etc, but not .ocv-page by itself
    const plainOcvPage = pagesCss.match(/\.ocv-page\s*{[^}]*display\s*:\s*flex/);
    expect(plainOcvPage, 'pages.css must not contain plain .ocv-page display:flex').toBeNull();
  });
});
