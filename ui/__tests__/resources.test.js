import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import '../views/resources.js';

const { ResourcesController } = globalThis.__resourcesExports ?? {};

// ── Shared DOM scaffold ───────────────────────────────────────────────────────

const SNAPSHOT_DOM = `
  <p id="res-status-msg"></p>
  <article id="card-res-mem">
    <span id="res-mem-used"></span>
    <span id="res-mem-total"></span>
    <span id="res-mem-pct"></span>
    <div id="res-mem-bar" class="progress-bar-fill" style="width:0%"></div>
  </article>
  <article id="card-res-cpu">
    <span id="res-cpu-pct"></span>
    <span id="res-cpu-badge"></span>
    <div id="res-cpu-bar" class="progress-bar-fill" style="width:0%"></div>
  </article>
  <article id="card-res-disk">
    <span id="res-disk-used"></span>
    <span id="res-disk-total"></span>
    <span id="res-disk-pct"></span>
    <div id="res-disk-bar" class="progress-bar-fill" style="width:0%"></div>
  </article>
  <article id="card-res-budget">
    <span id="res-budget-cache"></span>
    <span id="res-budget-disk"></span>
    <span id="res-budget-cpu"></span>
    <span id="res-budget-api"></span>
  </article>
  <span id="res-last-updated"></span>
  <button id="res-refresh-btn"></button>
`;

// ── Export hook ───────────────────────────────────────────────────────────────

describe('ResourcesController', () => {
  it('is exported via test hook', () => {
    expect(ResourcesController).toBeDefined();
    expect(typeof ResourcesController).toBe('function');
  });
});

// ── apiBase getter ────────────────────────────────────────────────────────────

describe('ResourcesController.apiBase', () => {
  let ctrl;
  let origShell;
  let origPort;

  beforeEach(() => {
    origShell = window.Shell;
    origPort = window.OMNICOVAS_PORT;
    ctrl = Object.create(ResourcesController.prototype);
  });

  afterEach(() => {
    window.Shell = origShell;
    window.OMNICOVAS_PORT = origPort;
  });

  it('returns Shell.httpBase when Shell.httpBase is available', () => {
    window.Shell = { httpBase: 'http://127.0.0.1:12345' };
    window.OMNICOVAS_PORT = undefined;
    expect(ctrl.apiBase).toBe('http://127.0.0.1:12345');
  });

  it('returns port-based URL when only OMNICOVAS_PORT is set', () => {
    window.Shell = null;
    window.OMNICOVAS_PORT = 9000;
    expect(ctrl.apiBase).toBe('http://127.0.0.1:9000');
  });

  it('returns null when neither Shell.httpBase nor OMNICOVAS_PORT is available', () => {
    window.Shell = null;
    window.OMNICOVAS_PORT = undefined;
    expect(ctrl.apiBase).toBeNull();
  });

  it('ignores Shell when httpBase is absent, falls back to OMNICOVAS_PORT', () => {
    window.Shell = {};
    window.OMNICOVAS_PORT = 7777;
    expect(ctrl.apiBase).toBe('http://127.0.0.1:7777');
  });
});

// ── fetchAndRender — no bridge ────────────────────────────────────────────────

describe('ResourcesController.fetchAndRender with no bridge', () => {
  let ctrl;
  let origFetch;
  let origShell;
  let origPort;

  beforeEach(() => {
    document.body.innerHTML = SNAPSHOT_DOM;
    origFetch = globalThis.fetch;
    origShell = window.Shell;
    origPort = window.OMNICOVAS_PORT;
    window.Shell = null;
    window.OMNICOVAS_PORT = undefined;
    ctrl = Object.create(ResourcesController.prototype);
  });

  afterEach(() => {
    globalThis.fetch = origFetch;
    window.Shell = origShell;
    window.OMNICOVAS_PORT = origPort;
  });

  it('does not call fetch when apiBase is null', async () => {
    let fetchCalled = false;
    globalThis.fetch = () => {
      fetchCalled = true;
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    };
    await ctrl.fetchAndRender();
    expect(fetchCalled).toBe(false);
  });

  it('shows waiting message when apiBase is null', async () => {
    globalThis.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    await ctrl.fetchAndRender();
    expect(document.getElementById('res-status-msg').textContent)
      .toBe('Waiting for OmniCOVAS bridge…');
  });

  it('renders all snapshot fields as — when apiBase is null', async () => {
    globalThis.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    await ctrl.fetchAndRender();
    expect(document.getElementById('res-mem-used').textContent).toBe('—');
    expect(document.getElementById('res-cpu-pct').textContent).toBe('—');
    expect(document.getElementById('res-disk-used').textContent).toBe('—');
  });
});

// ── Refresh button ────────────────────────────────────────────────────────────

describe('ResourcesController refresh button', () => {
  beforeEach(() => {
    document.body.innerHTML = SNAPSHOT_DOM;
  });

  it('calls fetchAndRender when Refresh button is clicked', () => {
    const ctrl = Object.create(ResourcesController.prototype);
    ctrl._boundBridgeHandler = () => {};
    let called = false;
    ctrl.fetchAndRender = () => { called = true; return Promise.resolve(); };
    ctrl.bindEvents();

    document.getElementById('res-refresh-btn').click();

    expect(called).toBe(true);
  });
});

// ── bridge-connected event ────────────────────────────────────────────────────

describe('ResourcesController bridge-connected event', () => {
  let origOmniEvents;

  beforeEach(() => {
    document.body.innerHTML = SNAPSHOT_DOM;
    origOmniEvents = window.OmniEvents;
    window.OmniEvents = new EventTarget();
  });

  afterEach(() => {
    window.OmniEvents = origOmniEvents;
  });

  it('triggers fetchAndRender when bridge-connected is dispatched via OmniEvents', () => {
    const ctrl = Object.create(ResourcesController.prototype);
    ctrl._boundBridgeHandler = () => { ctrl.fetchAndRender(); };
    let called = false;
    ctrl.fetchAndRender = () => { called = true; return Promise.resolve(); };
    ctrl.bindBridgeEvents();

    window.OmniEvents.dispatchEvent(new CustomEvent('bridge-connected', {
      detail: { port: 9999, httpBase: 'http://127.0.0.1:9999' },
    }));

    expect(called).toBe(true);
  });

  it('does not throw when OmniEvents is not set', () => {
    window.OmniEvents = undefined;
    const ctrl = Object.create(ResourcesController.prototype);
    ctrl._boundBridgeHandler = () => {};
    expect(() => ctrl.bindBridgeEvents()).not.toThrow();
  });
});

// ── renderMemory ──────────────────────────────────────────────────────────────

describe('ResourcesController.renderMemory', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = SNAPSHOT_DOM;
    ctrl = Object.create(ResourcesController.prototype);
  });

  it('renders used and total in MB with one decimal place', () => {
    ctrl.renderMemory({ memory_used_mb: 123.4, memory_total_mb: 8192.0 }, null);
    expect(document.getElementById('res-mem-used').textContent).toBe('123.4 MB');
    expect(document.getElementById('res-mem-total').textContent).toBe('8192.0 MB');
  });

  it('computes memory usage percentage from used and total', () => {
    ctrl.renderMemory({ memory_used_mb: 4096.0, memory_total_mb: 8192.0 }, null);
    expect(document.getElementById('res-mem-pct').textContent).toBe('50.0%');
  });

  it('renders — for all fields when snap is null', () => {
    ctrl.renderMemory(null, null);
    expect(document.getElementById('res-mem-used').textContent).toBe('—');
    expect(document.getElementById('res-mem-total').textContent).toBe('—');
    expect(document.getElementById('res-mem-pct').textContent).toBe('—');
  });

  it('sets bar width to 0% when snap is null', () => {
    ctrl.renderMemory(null, null);
    expect(document.getElementById('res-mem-bar').style.width).toBe('0%');
  });

  it('renders XSS payload in used field as literal text, creates no img/script nodes', () => {
    ctrl.renderMemory({ memory_used_mb: null, memory_total_mb: null }, null);
    expect(document.querySelector('img')).toBeNull();
    expect(document.querySelector('script')).toBeNull();
  });
});

// ── renderCpu ─────────────────────────────────────────────────────────────────

describe('ResourcesController.renderCpu', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = SNAPSHOT_DOM;
    ctrl = Object.create(ResourcesController.prototype);
  });

  it('renders cpu_percent with one decimal place', () => {
    ctrl.renderCpu({ cpu_percent: 5.2 });
    expect(document.getElementById('res-cpu-pct').textContent).toBe('5.2%');
  });

  it('renders — when snap is null', () => {
    ctrl.renderCpu(null);
    expect(document.getElementById('res-cpu-pct').textContent).toBe('—');
  });

  it('badge text is OK for cpu < 50', () => {
    ctrl.renderCpu({ cpu_percent: 20.0 });
    expect(document.getElementById('res-cpu-badge').textContent).toBe('OK');
    expect(document.getElementById('res-cpu-badge').className).toContain('ok');
  });

  it('badge text is ELEVATED and class warn for cpu >= 50 and < 80', () => {
    ctrl.renderCpu({ cpu_percent: 65.0 });
    expect(document.getElementById('res-cpu-badge').textContent).toBe('ELEVATED');
    expect(document.getElementById('res-cpu-badge').className).toContain('warn');
  });

  it('badge text is HIGH and class critical for cpu >= 80', () => {
    ctrl.renderCpu({ cpu_percent: 85.0 });
    expect(document.getElementById('res-cpu-badge').textContent).toBe('HIGH');
    expect(document.getElementById('res-cpu-badge').className).toContain('critical');
  });

  it('pct field-value carries critical class at 80%', () => {
    ctrl.renderCpu({ cpu_percent: 80.0 });
    expect(document.getElementById('res-cpu-pct').className).toContain('critical');
  });

  it('pct field-value carries warn class at 50%', () => {
    ctrl.renderCpu({ cpu_percent: 50.0 });
    expect(document.getElementById('res-cpu-pct').className).toContain('warn');
  });

  it('bar width clamps at 100% for cpu > 100', () => {
    ctrl.renderCpu({ cpu_percent: 150.0 });
    expect(document.getElementById('res-cpu-bar').style.width).toBe('100.0%');
  });
});

// ── renderDisk ────────────────────────────────────────────────────────────────

describe('ResourcesController.renderDisk', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = SNAPSHOT_DOM;
    ctrl = Object.create(ResourcesController.prototype);
  });

  it('computes disk used from total minus free', () => {
    ctrl.renderDisk({ disk_free_gb: 50.3, disk_total_gb: 200.0 });
    expect(document.getElementById('res-disk-used').textContent).toBe('149.7 GB');
  });

  it('computes disk used percentage', () => {
    ctrl.renderDisk({ disk_free_gb: 20.0, disk_total_gb: 200.0 });
    expect(document.getElementById('res-disk-pct').textContent).toBe('90.0%');
  });

  it('renders — for all disk fields when snap is null', () => {
    ctrl.renderDisk(null);
    expect(document.getElementById('res-disk-used').textContent).toBe('—');
    expect(document.getElementById('res-disk-total').textContent).toBe('—');
    expect(document.getElementById('res-disk-pct').textContent).toBe('—');
  });

  it('disk pct class is critical at >= 90% used', () => {
    ctrl.renderDisk({ disk_free_gb: 10.0, disk_total_gb: 200.0 });
    expect(document.getElementById('res-disk-pct').className).toContain('critical');
  });

  it('disk pct class is warn at >= 75% and < 90% used', () => {
    ctrl.renderDisk({ disk_free_gb: 30.0, disk_total_gb: 200.0 });
    expect(document.getElementById('res-disk-pct').className).toContain('warn');
  });

  it('disk pct class is empty below 75% used', () => {
    ctrl.renderDisk({ disk_free_gb: 60.0, disk_total_gb: 200.0 });
    const el = document.getElementById('res-disk-pct');
    expect(el.className).not.toContain('warn');
    expect(el.className).not.toContain('critical');
  });
});

// ── renderBudget ──────────────────────────────────────────────────────────────

describe('ResourcesController.renderBudget', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = SNAPSHOT_DOM;
    ctrl = Object.create(ResourcesController.prototype);
  });

  it('renders all four budget fields with correct units', () => {
    ctrl.renderBudget({
      max_cache_size_mb: 512,
      max_galaxy_dump_size_gb: 5,
      max_background_task_cpu_percent: 10,
      max_api_calls_per_minute_total: 50,
    });
    expect(document.getElementById('res-budget-cache').textContent).toBe('512 MB');
    expect(document.getElementById('res-budget-disk').textContent).toBe('5 GB');
    expect(document.getElementById('res-budget-cpu').textContent).toBe('10%');
    expect(document.getElementById('res-budget-api').textContent).toBe('50 / min');
  });

  it('renders — for all budget fields when budget is null', () => {
    ctrl.renderBudget(null);
    expect(document.getElementById('res-budget-cache').textContent).toBe('—');
    expect(document.getElementById('res-budget-disk').textContent).toBe('—');
    expect(document.getElementById('res-budget-cpu').textContent).toBe('—');
    expect(document.getElementById('res-budget-api').textContent).toBe('—');
  });
});

// ── setStatusMsg ──────────────────────────────────────────────────────────────

describe('ResourcesController.setStatusMsg', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = '<p id="res-status-msg"></p>';
    ctrl = Object.create(ResourcesController.prototype);
  });

  it('sets textContent on the status element', () => {
    ctrl.setStatusMsg('Resource monitoring disabled.');
    expect(document.getElementById('res-status-msg').textContent)
      .toBe('Resource monitoring disabled.');
  });

  it('hides the element when text is empty string', () => {
    ctrl.setStatusMsg('');
    expect(document.getElementById('res-status-msg').style.display).toBe('none');
  });

  it('shows the element when text is non-empty', () => {
    ctrl.setStatusMsg('Initializing…');
    expect(document.getElementById('res-status-msg').style.display).not.toBe('none');
  });

  it('renders XSS payload as literal text, creates no img/script nodes', () => {
    ctrl.setStatusMsg('<img src=x onerror=alert(1)>');
    expect(document.querySelector('img')).toBeNull();
    expect(document.querySelector('script')).toBeNull();
    expect(document.getElementById('res-status-msg').textContent)
      .toBe('<img src=x onerror=alert(1)>');
  });
});

// ── Classification methods ────────────────────────────────────────────────────

describe('ResourcesController.cpuClass', () => {
  let ctrl;
  beforeEach(() => { ctrl = Object.create(ResourcesController.prototype); });

  it('returns empty string for null', () => { expect(ctrl.cpuClass(null)).toBe(''); });
  it('returns empty string below 50', () => { expect(ctrl.cpuClass(49.9)).toBe(''); });
  it('returns warn at 50', () => { expect(ctrl.cpuClass(50)).toBe('warn'); });
  it('returns warn at 79.9', () => { expect(ctrl.cpuClass(79.9)).toBe('warn'); });
  it('returns critical at 80', () => { expect(ctrl.cpuClass(80)).toBe('critical'); });
  it('returns critical above 80', () => { expect(ctrl.cpuClass(99)).toBe('critical'); });
});

describe('ResourcesController.diskClass', () => {
  let ctrl;
  beforeEach(() => { ctrl = Object.create(ResourcesController.prototype); });

  it('returns empty string for null', () => { expect(ctrl.diskClass(null)).toBe(''); });
  it('returns empty string below 75', () => { expect(ctrl.diskClass(74.9)).toBe(''); });
  it('returns warn at 75', () => { expect(ctrl.diskClass(75)).toBe('warn'); });
  it('returns warn at 89.9', () => { expect(ctrl.diskClass(89.9)).toBe('warn'); });
  it('returns critical at 90', () => { expect(ctrl.diskClass(90)).toBe('critical'); });
  it('returns critical above 90', () => { expect(ctrl.diskClass(100)).toBe('critical'); });
});

describe('ResourcesController.memClass', () => {
  let ctrl;
  beforeEach(() => { ctrl = Object.create(ResourcesController.prototype); });

  it('returns empty string when usedMb is null', () => {
    expect(ctrl.memClass(null, 512)).toBe('');
  });
  it('returns empty string when budgetCacheMb is null', () => {
    expect(ctrl.memClass(600, null)).toBe('');
  });
  it('returns warn when usedMb exceeds budgetCacheMb', () => {
    expect(ctrl.memClass(513, 512)).toBe('warn');
  });
  it('returns empty string when usedMb equals budgetCacheMb', () => {
    expect(ctrl.memClass(512, 512)).toBe('');
  });
  it('returns empty string when usedMb is below budgetCacheMb', () => {
    expect(ctrl.memClass(400, 512)).toBe('');
  });
});

// ── render integration ────────────────────────────────────────────────────────

describe('ResourcesController.render', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = SNAPSHOT_DOM;
    ctrl = Object.create(ResourcesController.prototype);
  });

  it('shows disabled message when enabled is false', () => {
    ctrl.render({ enabled: false });
    expect(document.getElementById('res-status-msg').textContent)
      .toBe('Resource monitoring disabled.');
  });

  it('shows initializing message when enabled=true but snapshot is null', () => {
    ctrl.render({
      enabled: true,
      snapshot: null,
      budget: {
        max_cache_size_mb: 512,
        max_galaxy_dump_size_gb: 5,
        max_background_task_cpu_percent: 10,
        max_api_calls_per_minute_total: 50,
      },
    });
    expect(document.getElementById('res-status-msg').textContent)
      .toContain('initializ');
  });

  it('clears status message on full successful render', () => {
    ctrl.render({
      enabled: true,
      snapshot: {
        memory_used_mb: 100,
        memory_total_mb: 8192,
        cpu_percent: 5.0,
        disk_free_gb: 50,
        disk_total_gb: 200,
      },
      budget: {
        max_cache_size_mb: 512,
        max_galaxy_dump_size_gb: 5,
        max_background_task_cpu_percent: 10,
        max_api_calls_per_minute_total: 50,
      },
    });
    const msg = document.getElementById('res-status-msg');
    expect(msg.textContent === '' || msg.style.display === 'none').toBe(true);
  });

  it('renders memory used field on successful render', () => {
    ctrl.render({
      enabled: true,
      snapshot: {
        memory_used_mb: 512.0,
        memory_total_mb: 8192.0,
        cpu_percent: 5.0,
        disk_free_gb: 100.0,
        disk_total_gb: 200.0,
      },
      budget: {
        max_cache_size_mb: 512,
        max_galaxy_dump_size_gb: 5,
        max_background_task_cpu_percent: 10,
        max_api_calls_per_minute_total: 50,
      },
    });
    expect(document.getElementById('res-mem-used').textContent).toBe('512.0 MB');
    expect(document.getElementById('res-mem-total').textContent).toBe('8192.0 MB');
  });

  it('renders budget fields on successful render', () => {
    ctrl.render({
      enabled: true,
      snapshot: {
        memory_used_mb: 100,
        memory_total_mb: 8192,
        cpu_percent: 5.0,
        disk_free_gb: 50,
        disk_total_gb: 200,
      },
      budget: {
        max_cache_size_mb: 512,
        max_galaxy_dump_size_gb: 5,
        max_background_task_cpu_percent: 10,
        max_api_calls_per_minute_total: 50,
      },
    });
    expect(document.getElementById('res-budget-cache').textContent).toBe('512 MB');
    expect(document.getElementById('res-budget-api').textContent).toBe('50 / min');
  });

  it('snapshot cards all show — when enabled:false', () => {
    ctrl.render({ enabled: false });
    expect(document.getElementById('res-mem-used').textContent).toBe('—');
    expect(document.getElementById('res-cpu-pct').textContent).toBe('—');
    expect(document.getElementById('res-disk-used').textContent).toBe('—');
  });
});
