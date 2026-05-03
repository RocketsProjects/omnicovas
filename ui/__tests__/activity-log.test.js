import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import '../views/activity-log.js';

const { ActivityLogController } = globalThis.__activityLogExports ?? {};

describe('ActivityLogController — bridge readiness', () => {
  let ctrl;

  beforeEach(() => {
    delete window.Shell;
    delete window.OMNICOVAS_PORT;
    ctrl = Object.create(ActivityLogController.prototype);
  });

  afterEach(() => {
    delete window.Shell;
    delete window.OMNICOVAS_PORT;
  });

  it('apiBase returns null when no bridge globals are set', () => {
    expect(ctrl.apiBase).toBeNull();
  });

  it('apiUrl returns null when bridge is not ready', () => {
    expect(ctrl.apiUrl('/activity-log')).toBeNull();
  });

  it('apiBase returns Shell.httpBase when available', () => {
    window.Shell = { httpBase: 'http://127.0.0.1:7654' };
    expect(ctrl.apiBase).toBe('http://127.0.0.1:7654');
  });

  it('apiBase uses OMNICOVAS_PORT when Shell.httpBase is absent', () => {
    window.OMNICOVAS_PORT = '9876';
    expect(ctrl.apiBase).toBe('http://127.0.0.1:9876');
  });

  it('apiUrl builds correct URL from OMNICOVAS_PORT', () => {
    window.OMNICOVAS_PORT = '9876';
    expect(ctrl.apiUrl('/activity-log')).toBe('http://127.0.0.1:9876/activity-log');
  });

  it('apiUrl never contains :8000', () => {
    window.OMNICOVAS_PORT = '9876';
    expect(ctrl.apiUrl('/activity-log')).not.toContain(':8000');
  });

  it('loadActivityLog does not call fetch when bridge is not ready', async () => {
    global.fetch = vi.fn();
    await ctrl.loadActivityLog();
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('_showWaiting renders a waiting cell in log-body', () => {
    document.body.innerHTML = '<table><tbody id="log-body"></tbody></table>';
    ctrl._showWaiting();
    const td = document.querySelector('#log-body .log-waiting');
    expect(td).not.toBeNull();
    expect(td.textContent).toContain('Waiting');
    expect(td.colSpan).toBe(5);
  });

  it('bridge-connected listener triggers _loadAndRender', async () => {
    const events = new EventTarget();
    window.OmniEvents = events;
    window.OMNICOVAS_PORT = undefined;
    delete window.OMNICOVAS_PORT;

    document.body.innerHTML = '<table><tbody id="log-body"></tbody></table>';
    ctrl.allEntries = [];
    ctrl.filteredEntries = [];
    ctrl.currentPage = 0;
    ctrl.pageSize = 50;

    const loadAndRender = vi.fn().mockResolvedValue(undefined);
    ctrl._loadAndRender = loadAndRender;
    ctrl._showWaiting = vi.fn();

    await ctrl.init();

    expect(ctrl._showWaiting).toHaveBeenCalled();
    expect(loadAndRender).not.toHaveBeenCalled();

    events.dispatchEvent(new Event('bridge-connected'));
    await Promise.resolve();

    expect(loadAndRender).toHaveBeenCalledTimes(1);

    delete window.OmniEvents;
  });
});

describe('ActivityLogController.createLogRow', () => {
  let ctrl;

  beforeEach(() => {
    ctrl = Object.create(ActivityLogController.prototype);
  });

  it('renders malicious timestamp as literal text or safe fallback and creates no img node', () => {
    const row = ctrl.createLogRow({
      timestamp: '<img src=x onerror=alert(1)>',
      event_type: 'STATUS_UPDATE',
      source: 'system',
      summary: 'normal summary',
      ai_tier: null,
    });
    expect(row.querySelector('img')).toBeNull();
    const cell = row.querySelector('.log-timestamp');
    // textContent must be a plain string — no img/script nodes regardless of fallback path
    expect(typeof cell.textContent).toBe('string');
    expect(cell.innerHTML).not.toContain('<img');
  });

  it('renders malicious summary and event_type as literal text, creates no script or img nodes', () => {
    const row = ctrl.createLogRow({
      timestamp: '2024-01-01T00:00:00Z',
      event_type: '<script>xss()</script>',
      source: 'system',
      summary: '<img src=x onerror=alert(2)>',
      ai_tier: null,
    });
    expect(row.querySelector('script')).toBeNull();
    expect(row.querySelector('img')).toBeNull();
    expect(row.querySelector('.log-event-type').textContent).toBe('<script>xss()</script>');
    expect(row.querySelector('.log-summary').textContent).toBe('<img src=x onerror=alert(2)>');
  });

  it('renders event type cell with correct category class and text for a normal event', () => {
    const row = ctrl.createLogRow({
      timestamp: '2024-01-01T00:00:00Z',
      event_type: 'STATUS_UPDATE',
      source: 'system',
      summary: 'Normal status',
      ai_tier: 'tier1',
    });
    const typeCell = row.querySelector('.log-event-type');
    expect(typeCell).not.toBeNull();
    expect(typeCell.classList.contains('telemetry')).toBe(true);
    expect(typeCell.textContent).toBe('STATUS_UPDATE');
  });
});
