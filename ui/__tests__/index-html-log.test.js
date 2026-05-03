import { describe, it, expect, beforeEach, vi } from 'vitest';

let renderLog, addLogEntry;

beforeEach(async () => {
  document.body.innerHTML =
    '<input id="log-search">' +
    '<button id="log-clear-btn"></button>' +
    '<div id="log-entries"></div>';
  vi.resetModules();
  ({ renderLog, addLogEntry } = await import('../scripts/inline-event-log.js'));
});

describe('renderLog — safe DOM rendering', () => {
  it('renders empty state as literal text with no HTML injection', () => {
    renderLog('');
    const container = document.getElementById('log-entries');
    const p = container.querySelector('p');
    expect(p).not.toBeNull();
    expect(p.textContent).toBe('No events yet.');
    expect(p.className).toBe('field-value unknown');
    expect(container.querySelector('script')).toBeNull();
    expect(container.querySelector('img')).toBeNull();
  });

  it('renders malicious event_type as literal text, no img element injected', () => {
    addLogEntry({ event_type: '<img src=x onerror=alert(1)>', summary: 'safe summary' });
    const container = document.getElementById('log-entries');
    expect(container.querySelector('img')).toBeNull();
    const typeSpan = container.querySelector('.log-type');
    expect(typeSpan).not.toBeNull();
    expect(typeSpan.textContent).toBe('<img src=x onerror=alert(1)>');
  });

  it('renders malicious summary as literal text, no script element injected', () => {
    addLogEntry({ event_type: 'TEST_EVENT', summary: '<script>alert(1)<\/script>' });
    const container = document.getElementById('log-entries');
    expect(container.querySelector('script')).toBeNull();
    const msgSpan = container.querySelector('.log-msg');
    expect(msgSpan).not.toBeNull();
    expect(msgSpan.textContent).toBe('<script>alert(1)</script>');
  });

  it('renders both malicious fields together, no injected elements', () => {
    addLogEntry({
      event_type: '<img src=x onerror=alert(1)>',
      summary: '<script>alert(1)<\/script>',
    });
    const container = document.getElementById('log-entries');
    expect(container.querySelector('img')).toBeNull();
    expect(container.querySelector('script')).toBeNull();
    expect(container.querySelector('.log-type').textContent).toBe('<img src=x onerror=alert(1)>');
    expect(container.querySelector('.log-msg').textContent).toBe('<script>alert(1)</script>');
  });

  it('creates a log-entry div with role listitem', () => {
    addLogEntry({ event_type: 'HULL_DAMAGE', summary: 'Hull at 75%' });
    const entry = document.querySelector('.log-entry');
    expect(entry).not.toBeNull();
    expect(entry.getAttribute('role')).toBe('listitem');
  });

  it('applies warn class for warn event types', () => {
    addLogEntry({ event_type: 'HULL_DAMAGE', summary: '' });
    expect(document.querySelector('.log-entry.warn')).not.toBeNull();
  });

  it('applies critical class for critical event types', () => {
    addLogEntry({ event_type: 'SHIELDS_DOWN', summary: '' });
    expect(document.querySelector('.log-entry.critical')).not.toBeNull();
  });
});
