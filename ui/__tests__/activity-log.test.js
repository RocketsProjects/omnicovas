import { describe, it, expect, beforeEach } from 'vitest';
import '../views/activity-log.js';

const { ActivityLogController } = globalThis.__activityLogExports ?? {};

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
