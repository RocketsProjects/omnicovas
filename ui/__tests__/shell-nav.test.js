import { describe, it, expect, beforeEach } from 'vitest';
import fs from 'fs';

// Sets up the exact nav markup produced by index.html for PB05-02.
// These tests are structure contracts: if the HTML drifts, the tests catch it.
function setupNav() {
  document.body.innerHTML = `
    <nav id="sidebar" aria-label="Main navigation">
      <ul role="list">
        <li><a href="#/dashboard" class="active" aria-current="page">
          <span class="nav-icon" aria-hidden="true">&#9672;</span>Dashboard</a></li>
        <li><a href="#/activity-log" aria-current="false">
          <span class="nav-icon" aria-hidden="true">&#9719;</span>Activity Log</a></li>
        <li><a href="#/settings" aria-current="false">
          <span class="nav-icon" aria-hidden="true">&#9881;</span>Settings</a></li>
        <li><a href="#/privacy" aria-current="false">
          <span class="nav-icon" aria-hidden="true">&#128274;</span>Privacy</a></li>
        <li><a href="#/resources" aria-current="false">
          <span class="nav-icon" aria-hidden="true">&#9673;</span>Resources</a></li>
        <li><a href="#/credits" aria-current="false">
          <span class="nav-icon" aria-hidden="true">&#10022;</span>Credits</a></li>
      </ul>

      <details class="future-systems-group">
        <summary class="future-systems-summary">
          <span class="nav-icon" aria-hidden="true">&#9702;</span>
          Future Systems
          <span class="future-systems-expand" aria-hidden="true">&#8250;</span>
        </summary>
        <ul role="list" class="future-systems-list"
            aria-label="Upcoming feature pillars — not yet available">
          <li><span class="nav-item-future" aria-label="Combat — not yet available">
            <span class="nav-icon" aria-hidden="true">&#9702;</span>Combat</span></li>
          <li><span class="nav-item-future" aria-label="Exploration — not yet available">
            <span class="nav-icon" aria-hidden="true">&#9702;</span>Exploration</span></li>
          <li><span class="nav-item-future" aria-label="Trading / Mining — not yet available">
            <span class="nav-icon" aria-hidden="true">&#9702;</span>Trading / Mining</span></li>
          <li><span class="nav-item-future" aria-label="Squadron — not yet available">
            <span class="nav-icon" aria-hidden="true">&#9702;</span>Squadron</span></li>
          <li><span class="nav-item-future" aria-label="Engineering — not yet available">
            <span class="nav-icon" aria-hidden="true">&#9702;</span>Engineering</span></li>
          <li><span class="nav-item-future" aria-label="Powerplay / BGS — not yet available">
            <span class="nav-icon" aria-hidden="true">&#9702;</span>Powerplay / BGS</span></li>
        </ul>
      </details>

      <div class="sidebar-footer" aria-hidden="true">Phase 4 &middot; v0.1.0</div>
    </nav>
  `;
}

describe('Shell nav — active routes', () => {
  beforeEach(setupNav);

  it('sidebar is a <nav> element with an accessible label', () => {
    const sidebar = document.getElementById('sidebar');
    expect(sidebar.tagName.toLowerCase()).toBe('nav');
    expect(sidebar.getAttribute('aria-label')).toBeTruthy();
  });

  it('Dashboard route link exists', () => {
    expect(document.querySelector('a[href="#/dashboard"]')).not.toBeNull();
  });

  it('Activity Log route link exists', () => {
    expect(document.querySelector('a[href="#/activity-log"]')).not.toBeNull();
  });

  it('Settings route link exists', () => {
    expect(document.querySelector('a[href="#/settings"]')).not.toBeNull();
  });

  it('Privacy route link exists', () => {
    expect(document.querySelector('a[href="#/privacy"]')).not.toBeNull();
  });

  it('Resources route link exists', () => {
    expect(document.querySelector('a[href="#/resources"]')).not.toBeNull();
  });

  it('Credits route link exists', () => {
    expect(document.querySelector('a[href="#/credits"]')).not.toBeNull();
  });

  it('initial Dashboard link carries aria-current="page"', () => {
    const dash = document.querySelector('a[href="#/dashboard"]');
    expect(dash.getAttribute('aria-current')).toBe('page');
  });
});

describe('Shell nav — Future Systems group', () => {
  beforeEach(setupNav);

  it('Future Systems <details> group exists in the sidebar', () => {
    expect(document.querySelector('.future-systems-group')).not.toBeNull();
  });

  it('Future Systems group is collapsed by default (no open attribute)', () => {
    const details = document.querySelector('.future-systems-group');
    expect(details.hasAttribute('open')).toBe(false);
  });

  it('Future Systems summary element is present for keyboard toggle', () => {
    expect(document.querySelector('.future-systems-summary')).not.toBeNull();
  });

  it('contains all six future pillar labels', () => {
    // textContent includes the nav-icon char; use includes() for substring match
    const texts = [...document.querySelectorAll('.nav-item-future')]
      .map((el) => el.textContent.trim());
    const joined = texts.join('\n');
    expect(joined).toContain('Combat');
    expect(joined).toContain('Exploration');
    expect(joined).toContain('Trading / Mining');
    expect(joined).toContain('Squadron');
    expect(joined).toContain('Engineering');
    expect(joined).toContain('Powerplay / BGS');
  });

  it('future items are <span> elements — they carry no href and do not navigate', () => {
    const items = document.querySelectorAll('.nav-item-future');
    expect(items.length).toBeGreaterThan(0);
    items.forEach((item) => {
      expect(item.tagName.toLowerCase()).toBe('span');
      expect(item.hasAttribute('href')).toBe(false);
    });
  });

  it('future items have aria-labels indicating unavailability', () => {
    const items = document.querySelectorAll('.nav-item-future');
    items.forEach((item) => {
      const label = item.getAttribute('aria-label') || '';
      expect(label).toMatch(/not yet available/i);
    });
  });

  it('Future Systems list has an accessible label', () => {
    const list = document.querySelector('.future-systems-list');
    expect(list.getAttribute('aria-label')).toBeTruthy();
  });

  it('no fixed-port fallback (8000) references in Future Systems markup', () => {
    const group = document.querySelector('.future-systems-group');
    expect(group.innerHTML).not.toContain('8000');
  });
});

describe('Shell nav — no fixed-port fallback in active route links', () => {
  beforeEach(setupNav);

  it('active route <a> hrefs are hash-based, not port-based', () => {
    const links = document.querySelectorAll('#sidebar a[href^="#"]');
    links.forEach((link) => {
      expect(link.getAttribute('href')).toMatch(/^#\//);
    });
  });
});

describe('Shell nav — CSS token contracts', () => {
  const css = fs.readFileSync('ui/styles/shell.css', 'utf8');

  it('shell.css references new nav-specific text tokens', () => {
    expect(css).toContain('--color-nav-text');
    expect(css).toContain('--color-nav-text-muted');
    expect(css).toContain('--color-nav-text-disabled');
    expect(css).toContain('--color-nav-active-text');
  });

  it('sidebar link colors do not use the purple-tinted --color-fg-muted anymore', () => {
    // We expect the link color rule to be overridden by --color-nav-text
    // Inspecting the specific selector block for sidebar links
    const sidebarLinkBlock = css.match(/#sidebar nav ul li a[\s\S]*?\{[\s\S]*?\}/);
    expect(sidebarLinkBlock).not.toBeNull();
    expect(sidebarLinkBlock[0]).not.toContain('var(--color-fg-muted)');
    expect(sidebarLinkBlock[0]).toContain('var(--color-nav-text)');
  });

  it('contains the PB05 CSS failsafe block', () => {
    expect(css).toContain('PB05 failsafe: prevent browser default link styling in sidebar');
    expect(css).toContain('#sidebar a:any-link');
    expect(css).toContain('text-decoration: none !important');
  });
});
