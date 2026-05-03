'use strict';

let logEntries = [];
const MAX_LOG = 500;

function formatTime(ts) {
  if (!ts) return '—';
  try { return new Date(ts).toLocaleTimeString(); } catch (e) { return ts; }
}

function isCritical(t) {
  return ['HULL_CRITICAL_10', 'HULL_CRITICAL_25', 'SHIELDS_DOWN',
          'FUEL_CRITICAL', 'MODULE_CRITICAL'].includes(t);
}

function isWarn(t) {
  return ['HULL_DAMAGE', 'FUEL_LOW', 'HEAT_WARNING', 'MODULE_DAMAGED'].includes(t);
}

function renderLog(filter) {
  var container = document.getElementById('log-entries');
  if (!container) return;
  var items = filter
    ? logEntries.filter(function(e) {
        return (e.event_type || '').toLowerCase().indexOf(filter) !== -1 ||
               (e.summary || '').toLowerCase().indexOf(filter) !== -1;
      })
    : logEntries;

  container.replaceChildren();

  if (items.length === 0) {
    var p = document.createElement('p');
    p.className = 'field-value unknown';
    p.style.padding = 'var(--space-3)';
    p.textContent = 'No events yet.';
    container.appendChild(p);
    return;
  }

  items.slice(0, MAX_LOG).forEach(function(e) {
    var cls = isCritical(e.event_type) ? 'critical' : isWarn(e.event_type) ? 'warn' : '';
    var div = document.createElement('div');
    div.className = 'log-entry' + (cls ? ' ' + cls : '');
    div.setAttribute('role', 'listitem');

    var timeSpan = document.createElement('span');
    timeSpan.className = 'log-time';
    timeSpan.textContent = formatTime(e.timestamp);

    var typeSpan = document.createElement('span');
    typeSpan.className = 'log-type';
    typeSpan.textContent = e.event_type || '—';

    var msgSpan = document.createElement('span');
    msgSpan.className = 'log-msg';
    msgSpan.textContent = e.summary || '';

    div.appendChild(timeSpan);
    div.appendChild(typeSpan);
    div.appendChild(msgSpan);
    container.appendChild(div);
  });
}

function addLogEntry(entry) {
  logEntries.unshift(entry);
  if (logEntries.length > MAX_LOG) logEntries.length = MAX_LOG;
  var searchEl = document.getElementById('log-search');
  renderLog(searchEl ? searchEl.value.toLowerCase().trim() : '');
}

async function fetchLog() {
  if (!window.OMNICOVAS_PORT) return;
  try {
    var r = await fetch('http://127.0.0.1:' + window.OMNICOVAS_PORT + '/activity-log');
    if (!r.ok) return;
    var data = await r.json();
    logEntries = (data.entries || []).reverse();
    renderLog('');
  } catch (e) { /* silent */ }
}

function hydrateLogForCurrentRoute(attempt) {
  if (attempt === undefined) attempt = 0;
  if (window.location.hash !== '#/activity-log') return;
  if (window.OMNICOVAS_PORT) { fetchLog(); return; }
  if (attempt >= 20) return;
  setTimeout(function () { hydrateLogForCurrentRoute(attempt + 1); }, 100);
}

// Module runs after DOM is parsed — wire search and clear at top-level
var searchEl = document.getElementById('log-search');
if (searchEl) {
  searchEl.addEventListener('input', function () {
    renderLog(searchEl.value.toLowerCase().trim());
  });
}
var clearBtn = document.getElementById('log-clear-btn');
if (clearBtn) {
  clearBtn.addEventListener('click', function () {
    if (confirm('Clear the activity log display? (Does not affect stored history.)')) {
      logEntries = [];
      renderLog('');
    }
  });
}

window.addEventListener('hashchange', function () {
  if (window.location.hash === '#/activity-log') fetchLog();
});

if (window.OmniEvents && typeof window.OmniEvents.addEventListener === 'function') {
  window.OmniEvents.addEventListener('bridge-connected', function () {
    hydrateLogForCurrentRoute();
  });
}

window._addLogEntry = addLogEntry;

hydrateLogForCurrentRoute();

export { renderLog, addLogEntry, fetchLog, hydrateLogForCurrentRoute };
