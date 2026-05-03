/**
 * OmniCOVAS Dashboard View — Week 11 Part C
 *
 * Renders all 8 Pillar 1 cards:
 *  1. LiveShipState   — ship identity, system, docked, wanted
 *  2. Hull & Shields  — hull bar with 25%/10% threshold marks, shield badge
 *  3. Fuel & Jump     — fuel bar, jump range
 *  4. Cargo           — count/capacity, top-5 commodity list
 *  5. Heat            — level bar, trend arrow, 10-sample sparkline
 *  6. Power (PIPS)    — SYS / ENG / WEP pip dots
 *  7. Module Health   — ok/warning/critical counts, link to loadout
 *  8. Rebuy Estimate  — single credit figure
 *
 * Pattern 1 (WebSocket-First): all cards subscribe to window.OmniEvents.
 * HTTP /pillar1/ship-state is the initial-load path; WS events keep it live.
 */

'use strict';

/* ── Utility helpers ── */
const fmt = {
  pct: (v, dp = 1) => v == null ? '—' : `${v.toFixed(dp)}%`,
  num: (v) => v == null ? '—' : v.toLocaleString(),
  ly:  (v) => v == null ? '—' : `${v.toFixed(2)} ly`,
  t:   (v) => v == null ? '—' : `${v.toFixed(1)} t`,
  credits: (v) => v == null ? '—' : `${v.toLocaleString()} cr`,
};

function el(id) { return document.getElementById(id); }

function hullClass(pct) {
  if (pct == null) return '';
  if (pct <= 10) return 'critical';
  if (pct <= 25) return 'warn';
  return 'ok';
}

function fuelClass(pct) {
  if (pct == null) return '';
  if (pct <= 10) return 'critical';
  if (pct <= 25) return 'warn';
  return '';
}

function heatClass(pct) {
  if (pct == null) return '';
  if (pct >= 120) return 'critical';
  if (pct >= 95)  return 'critical';
  if (pct >= 80)  return 'warn';
  return '';
}

/* ── Sparkline (canvas) ── */
function drawSparkline(canvasEl, samples) {
  if (!canvasEl || !samples || samples.length < 2) return;
  const ctx = canvasEl.getContext('2d');
  const w = canvasEl.offsetWidth || 200;
  const h = canvasEl.offsetHeight || 32;
  canvasEl.width = w;
  canvasEl.height = h;
  ctx.clearRect(0, 0, w, h);

  const max = Math.max(...samples, 1.0);
  const step = w / (samples.length - 1);

  ctx.beginPath();
  ctx.strokeStyle = samples[samples.length - 1] >= 0.80
    ? 'var(--color-critical, #ff3333)'
    : 'var(--color-accent, #ff8800)';
  ctx.lineWidth = 1.5;

  samples.forEach((s, i) => {
    const x = i * step;
    const y = h - (s / max) * (h - 4) - 2;
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.stroke();
}

/* ── Card border state ── */
function setCardState(cardId, state) {
  const card = el(cardId);
  if (!card) return;
  card.classList.remove('ok', 'warn', 'critical', 'destroyed');
  if (state) card.classList.add(state);
}

/* ─────────────────────────────────────────────
   CARD 1 — Live Ship State
───────────────────────────────────────────── */
function renderShipState(s) {
  const set = (id, val) => { const e = el(id); if (e) e.textContent = val ?? '—'; };

  const sanitizedShipName = (s.ship_name && s.ship_name.trim().length > 0)
    ? s.ship_name.trim()
    : (s.ship_type || 'UNKNOWN');

  set('dash-ship-type',   s.ship_type);
  set('dash-ship-name',   sanitizedShipName);
  set('dash-ship-ident',  s.ship_ident);
  set('dash-system',      s.current_system);
  set('dash-station',     s.current_station);

  const dockedEl = el('dash-docked');
  if (dockedEl) {
    dockedEl.textContent = s.is_docked ? 'YES' : 'NO';
    dockedEl.className = 'field-value ' + (s.is_docked ? 'ok' : '');
  }

  const wantedEl = el('dash-wanted');
  if (wantedEl) {
    wantedEl.textContent = s.is_wanted_in_system ? 'WANTED' : '—';
    wantedEl.className = 'field-value ' + (s.is_wanted_in_system ? 'critical' : 'unknown');
  }
}

/* ─────────────────────────────────────────────
   CARD 2 — Hull & Shields
───────────────────────────────────────────── */
function renderHullShields(s) {
  const hullPct = s.hull_health;
  const cls = hullClass(hullPct);

  const hullVal = el('dash-hull-value');
  if (hullVal) {
    hullVal.textContent = fmt.pct(hullPct);
    hullVal.className = 'field-value ' + cls;
  }

  const bar = el('dash-hull-bar');
  if (bar) {
    bar.style.width = (hullPct ?? 0) + '%';
    bar.className = 'progress-bar-fill ' + cls;
  }

  setCardState('card-hull', cls || null);

  const shieldEl = el('dash-shield');
  if (shieldEl) {
    if (s.shield_up == null) {
      shieldEl.textContent = '—';
      shieldEl.className = 'badge muted';
    } else if (s.shield_up) {
      shieldEl.textContent = 'UP';
      shieldEl.className = 'badge ok';
    } else {
      shieldEl.textContent = 'DOWN';
      shieldEl.className = 'badge critical';
    }
  }

  const shieldPctEl = el('dash-shield-pct');
  if (shieldPctEl) {
    shieldPctEl.textContent = s.shield_strength_pct != null ? fmt.pct(s.shield_strength_pct) : '—';
    shieldPctEl.className = 'field-value' + (s.shield_strength_pct == null ? ' unknown' : '');
  }
}

/* ─────────────────────────────────────────────
   CARD 3 — Fuel & Jump Range
───────────────────────────────────────────── */
function renderFuel(s) {
  const fuelPct = s.fuel_pct;
  const cls = fuelClass(fuelPct);

  const fuelVal = el('dash-fuel-value');
  if (fuelVal) {
    fuelVal.textContent = fmt.pct(fuelPct);
    fuelVal.className = 'field-value ' + cls;
  }

  const bar = el('dash-fuel-bar');
  if (bar) {
    bar.style.width = (fuelPct ?? 0) + '%';
    bar.className = 'progress-bar-fill ' + cls;
  }

  const fuelRaw = el('dash-fuel-raw');
  if (fuelRaw) fuelRaw.textContent = `${fmt.t(s.fuel_main)} / ${fmt.t(s.fuel_capacity)}`;

  const jump = el('dash-jump');
  if (jump) jump.textContent = fmt.ly(s.jump_range_ly);

  setCardState('card-fuel', cls || null);
}

/* ─────────────────────────────────────────────
   CARD 4 — Cargo
───────────────────────────────────────────── */
function renderCargo(s, inventory) {
  const countEl = el('dash-cargo-count');
  if (countEl) countEl.textContent =
    s.cargo_count != null && s.cargo_capacity != null
      ? `${s.cargo_count} / ${s.cargo_capacity}`
      : '—';

  const listEl = el('dash-cargo-list');
  if (listEl) {
    const items = (inventory || []).slice(0, 5);
    if (items.length === 0) {
      const emptyLi = document.createElement('li');
      emptyLi.className = 'field-value unknown';
      emptyLi.textContent = 'Empty';
      listEl.replaceChildren(emptyLi);
    } else {
      const nodes = items.map(item => {
        const li = document.createElement('li');
        li.className = 'field-row';
        const nameSpan = document.createElement('span');
        nameSpan.className = 'field-label';
        nameSpan.textContent = item.name;
        const countSpan = document.createElement('span');
        countSpan.className = 'field-value';
        countSpan.textContent = item.count;
        li.appendChild(nameSpan);
        li.appendChild(countSpan);
        return li;
      });
      listEl.replaceChildren(...nodes);
    }
  }
}

/* ─────────────────────────────────────────────
   CARD 5 — Heat
───────────────────────────────────────────── */
function renderHeat(heat) {
  const heatPct = Number.isFinite(heat?.level_pct) ? heat.level_pct : null;
  const state = heat?.state ?? null;
  const samples = Array.isArray(heat?.samples) ? heat.samples : [];
  const trend = samples.length > 0 ? (heat?.trend ?? null) : null;
  const cls = heatClass(heatPct);

  const heatVal = el('dash-heat-value');
  if (heatVal) {
    heatVal.textContent = heatPct != null ? fmt.pct(heatPct, 0) : 'UNKNOWN';
    heatVal.className = 'field-value ' + cls;
  }

  const bar = el('dash-heat-bar');
  if (bar) {
    bar.style.width = heatPct != null ? (Math.min(heatPct, 150) / 1.5 + '%') : '0%';
    bar.className = 'progress-bar-fill ' + cls;
  }

  const trendEl = el('dash-heat-trend');
  if (trendEl && trend) {
    const arrows = { rising: '↑', falling: '↓', steady: '→' };
    trendEl.textContent = (arrows[trend] || '') + ' ' + trend;
    trendEl.className = 'trend ' + (trend || 'steady');
  }

  const stateEl = el('dash-heat-state');
  if (stateEl) {
    stateEl.textContent = state ? state.toUpperCase() : 'NORMAL';
    stateEl.className = 'badge ' + (state === 'warning' ? 'warn' : (state === 'damage' || state === 'critical' ? 'critical' : 'ok'));
  }

  drawSparkline(el('dash-heat-sparkline'), samples);
  setCardState('card-heat', cls || null);
}

/* ─────────────────────────────────────────────
   CARD 6 — Power Distribution (PIPS)
───────────────────────────────────────────── */
function renderPips(s) {
  renderPipsGroup('pips-sys', s.sys_pips);
  renderPipsGroup('pips-eng', s.eng_pips);
  renderPipsGroup('pips-wep', s.wep_pips);
}

function renderPipsGroup(groupId, value) {
  const group = el(groupId);
  if (!group) return;
  const dotsEl = group.querySelector('.pips-dots');
  if (!dotsEl) return;
  dotsEl.innerHTML = '';
  for (let i = 0; i < 8; i++) {
    const pip = document.createElement('span');
    pip.className = 'pip' + (value != null && i < value ? ' filled' : '');
    pip.setAttribute('aria-hidden', 'true');
    dotsEl.appendChild(pip);
  }
}

/* ─────────────────────────────────────────────
   CARD 7 — Module Health Summary
───────────────────────────────────────────── */
function renderModules(summary) {
  const set = (id, val) => { const e = el(id); if (e) e.textContent = val ?? '—'; };
  set('dash-mod-ok',       summary?.ok);
  set('dash-mod-warning',  summary?.warning);
  set('dash-mod-critical', summary?.critical);
  set('dash-mod-total',    summary?.total);

  const critEl = el('dash-mod-critical');
  if (critEl) critEl.className = 'field-value' + (summary?.critical > 0 ? ' critical' : ' ok');

  const warnEl = el('dash-mod-warning');
  if (warnEl) warnEl.className = 'field-value' + (summary?.warning > 0 ? ' warn' : '');

  if (summary?.critical > 0) setCardState('card-modules', 'critical');
  else if (summary?.warning > 0) setCardState('card-modules', 'warn');
  else setCardState('card-modules', null);
}

/* ─────────────────────────────────────────────
   CARD 8 — Rebuy Estimate
───────────────────────────────────────────── */
function renderRebuy(rebuy) {
  const rebuyEl = el('dash-rebuy');
  if (rebuyEl) {
    rebuyEl.textContent = fmt.credits(rebuy?.rebuy_cost);
    rebuyEl.className = 'field-value' + (rebuy?.rebuy_cost == null ? ' unknown' : '');
  }
}

/* ─────────────────────────────────────────────
   Full state render (called on initial load and /state poll)
───────────────────────────────────────────── */
function renderFullState(state) {
  renderShipState(state);
  renderHullShields(state);
  renderFuel(state);
}

/* ── Fetch helpers ── */
async function fetchJSON(path) {
  if (!window.OMNICOVAS_PORT) return null;
  try {
    const r = await fetch(`http://127.0.0.1:${window.OMNICOVAS_PORT}${path}`);
    return r.ok ? await r.json() : null;
  } catch { return null; }
}

async function refreshShipState() {
  const s = await fetchJSON('/pillar1/ship-state');
  if (s) {
    window._lastShipState = s;
    renderShipState(s);
    renderHullShields(s);
    renderFuel(s);
    renderPips(s);
  }
  return s;
}

async function refreshPips() {
  const p = await fetchJSON('/pillar1/pips');
  if (!p) return false;
  if (p.sys != null) renderPipsGroup('pips-sys', p.sys);
  if (p.eng != null) renderPipsGroup('pips-eng', p.eng);
  if (p.wep != null) renderPipsGroup('pips-wep', p.wep);
  return true;
}

async function loadDashboard() {
  const [ship, cargo, heat, mods, rebuy] = await Promise.all([
    refreshShipState(),
    fetchJSON('/pillar1/cargo'),
    fetchJSON('/pillar1/heat'),
    fetchJSON('/pillar1/modules/summary'),
    fetchJSON('/rebuy'),
  ]);

  if (cargo) renderCargo(ship || {}, cargo.inventory);
  if (heat)  renderHeat(heat);
  if (mods)  renderModules(mods);
  if (rebuy) renderRebuy(rebuy);
}

let shipRefreshTimer = null;
let heatTtlTimer = null;

function requestShipStateRefresh(reason) {
  if (shipRefreshTimer) return;
  console.log(`Dashboard: scheduling refresh, reason: ${reason}`);
  shipRefreshTimer = setTimeout(() => {
    refreshShipState();
    shipRefreshTimer = null;
  }, 250);
}

function scheduleDashboardLoad(attempts = 20) {
  if (window.OMNICOVAS_PORT) {
    loadDashboard();
  } else if (attempts > 0) {
    setTimeout(() => scheduleDashboardLoad(attempts - 1), 1000);
  } else {
    console.warn('Dashboard: Bridge not ready after multiple retries.');
  }
}

/* ─────────────────────────────────────────────
   WebSocket event handlers
───────────────────────────────────────────── */
function onStateUpdate(state) {
  requestShipStateRefresh('state_update');
}

function onEvent(msg) {
  const { event_type, payload } = msg;
  // Handle case where payload might be missing or event is raw Status
  const type = event_type || msg.event;

  switch (type) {
    case 'SHIP_STATE_CHANGED':
    case 'LOADOUT_CHANGED':
      loadDashboard();
      break;

    case 'Status':
    case 'HULL_DAMAGE':
    case 'HullDamage':
    case 'HULL_CRITICAL_25':
    case 'HULL_CRITICAL_10':
      requestShipStateRefresh(type);
      break;

    case 'SHIELDS_DOWN':
    case 'ShieldsDown':
    case 'ShieldDown':
    case 'SHIELDS_UP':
    case 'ShieldsUp':
    case 'ShieldUp':
      requestShipStateRefresh(type);
      break;

    case 'FUEL_LOW':
    case 'FUEL_CRITICAL':
      requestShipStateRefresh(type);
      break;

    case 'HEAT_WARNING':
    case 'HEAT_DAMAGE':
      fetchJSON('/pillar1/heat').then(h => {
        if (h) renderHeat(h);
      });
      // Re-fetch after backend TTL + buffer (60s TTL + 7s) because no event
      // is emitted when heat state expires; clears stale WARNING display.
      if (heatTtlTimer) clearTimeout(heatTtlTimer);
      heatTtlTimer = setTimeout(() => {
        heatTtlTimer = null;
        fetchJSON('/pillar1/heat').then(h => { if (h) renderHeat(h); });
      }, 67000);
      break;

    case 'PIPS_CHANGED':
    case 'PipsChanged':
      refreshPips();
      requestShipStateRefresh(type);
      break;

    case 'CARGO_CHANGED':
      fetchJSON('/pillar1/cargo').then(c => {
        if (c) renderCargo(window._lastShipState || {}, c.inventory);
      });
      break;

    case 'MODULE_DAMAGED':
    case 'MODULE_CRITICAL':
      fetchJSON('/pillar1/modules/summary').then(m => { if (m) renderModules(m); });
      break;

    case 'DESTROYED':
      document.querySelectorAll('.card').forEach(c => c.classList.add('destroyed'));
      ['dash-hull-value','dash-shield','dash-fuel-value'].forEach(id => {
        const e = el(id); if (e) e.textContent = '—';
      });
      el('dash-ship-type') && (el('dash-ship-type').textContent = 'DESTROYED');
      break;

    case 'FSD_JUMP':
    case 'FSDJump':
    case 'DOCKED':
    case 'Docked':
    case 'UNDOCKED':
    case 'Undocked':
      requestShipStateRefresh(type);
      break;
  }
}

/* ─────────────────────────────────────────────
   Init
───────────────────────────────────────────── */
window.OmniEvents?.addEventListener('state', (ev) => {
  onStateUpdate(ev.detail);
});

window.OmniEvents?.addEventListener('event', (ev) => {
  onEvent(ev.detail);
});

// Load immediately if port already known; also re-load when view becomes active
window.addEventListener('hashchange', () => {
  if (window.location.hash === '#/dashboard' || !window.location.hash) loadDashboard();
});

// Hydration listener
window.OmniEvents?.addEventListener('bridge-connected', loadDashboard);
scheduleDashboardLoad();

// Test hook for Vitest; keeps this browser-compatible without changing production module/script loading.
if (typeof globalThis.__dashboardExports === 'undefined') {
  globalThis.__dashboardExports = { renderCargo };
}
