"""
tests.test_phase2_integration

Phase 2 Full-Session Integration Test (Week 10, Part C).

Feeds the recorded session journal (tests/fixtures/session_replay/) line-by-line
through the full Pillar 1 handler stack and asserts:

    - All 11 Phase 2 features produce expected state updates
    - Critical and extended broadcasts fire at the correct events
    - Latency budgets hold under replay load (no breaches)
    - Activity Log captures every critical and extended event
    - Phase 1 state (current_system, is_docked) remains consistent
    - Rebuy cost computes correctly after Loadout

Session arc in Journal.replay.log:
    LoadGame -> Loadout (Python, HullValue=56978012, ModulesValue=48500000)
    -> Undocked (Shinrarta Dezhra)
    -> StartJump + FSDJump (-> Wolf 397)
    -> FuelScoop
    -> FSDJump (-> Sol)
    -> HullDamage x2 (82%, 61%)
    -> ShieldsDown
    -> HullDamage x2 (22%, 8%)  -- crosses HULL_CRITICAL_25 and HULL_CRITICAL_10
    -> ShieldsUp
    -> Docked (Daedalus / Sol)
    -> RefuelAll
    -> Loadout (after repair)
    -> Undocked
    -> CommitCrime
    -> FSDJump (-> Alpha Centauri) -- clears wanted flag

Related to: Phase 2 Development Guide Week 10, Part C
Related to: Law 6 (Performance) -- latency budgets hold under replay load
Related to: Law 8 (Sovereignty) -- Activity Log captures every critical event
"""

from __future__ import annotations

import asyncio
import time
from pathlib import Path

import pytest

from omnicovas.core.activity_log import ActivityLog, subscribe_critical_events
from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.dispatcher import EventDispatcher
from omnicovas.core.event_types import (
    CARGO_CHANGED,
    DESTROYED,
    DOCKED,
    FSD_JUMP,
    FUEL_CRITICAL,
    FUEL_LOW,
    HULL_CRITICAL_10,
    HULL_CRITICAL_25,
    HULL_DAMAGE,
    LOADOUT_CHANGED,
    MODULE_CRITICAL,
    MODULE_DAMAGED,
    PIPS_CHANGED,
    SHIELDS_DOWN,
    SHIELDS_UP,
    SHIP_STATE_CHANGED,
    UNDOCKED,
    WANTED,
)
from omnicovas.core.state_manager import StateManager
from omnicovas.features import (
    cargo as _cargo,
)
from omnicovas.features import (
    extended_events as _extended,
)
from omnicovas.features import (
    fuel as _fuel,
)
from omnicovas.features import (
    heat_management as _heat,
)
from omnicovas.features import (
    hull_triggers as _hull,
)
from omnicovas.features import (
    loadout as _loadout,
)
from omnicovas.features import (
    module_health as _module_health,
)
from omnicovas.features import (
    power_distribution as _pips,
)
from omnicovas.features import (
    ship_state as _ship_state,
)
from omnicovas.features.rebuy import calculate_rebuy

FIXTURE_JOURNAL = (
    Path(__file__).parent / "fixtures" / "session_replay" / "Journal.replay.log"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def build_full_stack() -> tuple[
    StateManager, ShipStateBroadcaster, EventDispatcher, ActivityLog
]:
    """Wire the complete Pillar 1 handler stack as in main()."""
    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    dispatcher = EventDispatcher()
    activity_log = ActivityLog(maxlen=200)

    # Activity log subscriber MUST be registered before feature handlers
    # so no critical broadcasts are missed.
    subscribe_critical_events(activity_log, broadcaster)

    # Register all Phase 2 feature handlers
    _ship_state.register(dispatcher.register, state, broadcaster)
    _loadout.register(dispatcher.register, state, broadcaster)
    _fuel.register(dispatcher.register, state, broadcaster)
    _cargo.register(dispatcher.register, state, broadcaster)
    _module_health.register_subscriber(state, broadcaster)
    _hull.register(dispatcher.register, state, broadcaster)
    _extended.register(dispatcher.register, state, broadcaster)
    _pips.register(dispatcher.register, state, broadcaster)
    _heat.register(dispatcher.register, state, broadcaster)

    return state, broadcaster, dispatcher, activity_log


async def replay_journal(dispatcher: EventDispatcher, path: Path) -> int:
    """Feed every non-empty line from path to dispatcher. Returns line count.

    Calls ``asyncio.sleep(0)`` after each dispatch so that broadcast subscriber
    tasks (created via ``asyncio.create_task`` inside the broadcaster) have a
    chance to execute before the next event is dispatched. Without this flush,
    tasks accumulate in the event loop queue and may not run until after test
    assertions complete.
    """
    count = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                await dispatcher.dispatch(line)
                await asyncio.sleep(0)  # flush queued subscriber tasks
                count += 1
    return count


# ---------------------------------------------------------------------------
# Collector subscriber
# ---------------------------------------------------------------------------


class EventCollector:
    """Subscribes to a broadcaster and records every received event."""

    def __init__(self) -> None:
        self._events: list[ShipStateEvent] = []

    async def handle(self, event: ShipStateEvent) -> None:
        self._events.append(event)

    def of_type(self, event_type: str) -> list[ShipStateEvent]:
        return [e for e in self._events if e.event_type == event_type]

    def count(self, event_type: str) -> int:
        return len(self.of_type(event_type))

    def has(self, event_type: str) -> bool:
        return self.count(event_type) > 0


# ---------------------------------------------------------------------------
# Integration test
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_full_session_replay_all_features() -> None:
    """Feed the full session replay and assert all 11 features fire correctly."""
    state, broadcaster, dispatcher, activity_log = build_full_stack()
    collector = EventCollector()

    # Subscribe collector to every Phase 2 event type
    for et in [
        SHIP_STATE_CHANGED,
        LOADOUT_CHANGED,
        HULL_DAMAGE,
        HULL_CRITICAL_25,
        HULL_CRITICAL_10,
        SHIELDS_DOWN,
        SHIELDS_UP,
        FUEL_LOW,
        FUEL_CRITICAL,
        FSD_JUMP,
        DOCKED,
        UNDOCKED,
        WANTED,
        DESTROYED,
        PIPS_CHANGED,
        CARGO_CHANGED,
        MODULE_DAMAGED,
        MODULE_CRITICAL,
    ]:
        broadcaster.subscribe(et, collector.handle)

    lines_replayed = await replay_journal(dispatcher, FIXTURE_JOURNAL)
    assert lines_replayed >= 10, "Fixture journal too short"

    snap = state.snapshot

    # Feature 1 -- Live Ship State
    assert snap.current_ship_type == "Python"
    assert snap.current_ship_id == 1
    assert snap.current_ship_name == "HMCS Taranis"
    assert snap.current_ship_ident == "PY-01"
    assert snap.commander_name == "TestCmdr"
    assert collector.has(SHIP_STATE_CHANGED)

    # Feature 4 -- Loadout Awareness: Loadout parsed and hashed
    assert snap.loadout_hash is not None
    assert len(snap.loadout_hash) == 64  # SHA-256 hex
    assert snap.jump_range_ly == pytest.approx(22.3)

    # Feature 2 -- Module Health: modules dict populated
    assert "PowerPlant" in snap.modules
    assert "FrameShiftDrive" in snap.modules
    assert snap.modules["PowerPlant"].health == pytest.approx(1.0)

    # Feature 5 -- Fuel & Jump Range
    assert snap.fuel_capacity_main == pytest.approx(32.0)
    assert snap.fuel_capacity_reserve == pytest.approx(0.63)
    # FSDJump to Alpha Centauri sets FuelMain=12.36
    assert snap.fuel_main == pytest.approx(12.36)

    # Feature 6 -- Cargo Monitoring (no cargo events in this replay -> None)
    # Capacity from Loadout (no cargorack summing without cargo.json)
    assert snap.cargo_count is None  # no Cargo journal event in replay

    # Feature 3 -- Hull & Integrity Triggers
    # Hull sequence: 82% -> 61% -> 22% -> 8%
    # 22% is below 25% -> HULL_CRITICAL_25 should have fired
    # 8% is below 10% -> HULL_CRITICAL_10 should have fired
    assert collector.has(HULL_DAMAGE)
    assert collector.count(HULL_DAMAGE) >= 4
    assert collector.has(HULL_CRITICAL_25)
    assert collector.count(HULL_CRITICAL_25) == 1  # once per crossing
    assert collector.has(HULL_CRITICAL_10)
    assert collector.count(HULL_CRITICAL_10) == 1  # once per crossing

    # Feature 7 -- Critical Event Broadcaster: Activity Log captures criticals
    activity_types = {e.event_type for e in activity_log.entries()}
    assert HULL_CRITICAL_25 in activity_types
    assert HULL_CRITICAL_10 in activity_types
    assert SHIELDS_DOWN in activity_types

    # Feature 8 -- Extended Event Broadcaster
    assert collector.has(FSD_JUMP)
    # Two FSDJumps in replay (Wolf 397 + Sol + Alpha Centauri)
    assert collector.count(FSD_JUMP) >= 2
    assert collector.has(DOCKED)
    assert collector.has(UNDOCKED)
    assert collector.has(WANTED)
    assert snap.current_system == "Alpha Centauri"
    # Wanted cleared by FSDJump to Alpha Centauri
    assert snap.is_wanted_in_system is False

    # Feature 3 -- Shields
    assert collector.has(SHIELDS_DOWN)
    assert collector.has(SHIELDS_UP)
    assert snap.shield_up is True  # ShieldsUp fired after damage

    # Feature 11 -- Rebuy Calculator
    rebuy = calculate_rebuy(state)
    assert rebuy is not None
    # hull=56978012, modules=48500000, total=105478012, 5% = 5273900
    expected_rebuy = int((56_978_012 + 48_500_000) * 0.05)
    assert rebuy == expected_rebuy

    # Feature 9 -- Power Distribution: no Status.json in replay; pips stay None
    # (Status events arrive via StatusReader in production, not journal replay)
    assert snap.sys_pips is None  # expected: no pip events in journal

    # Feature 10 -- Heat Management: similarly no Status.json heat
    assert snap.heat_level is None

    # Docked state after RefuelAll -> then Undocked -> then FSDJump -> not docked
    assert snap.is_docked is False


@pytest.mark.asyncio
async def test_latency_budgets_hold_under_replay() -> None:
    """All dispatched events complete within 2x their local latency budgets.

    Tolerance 2x matches the CI multiplier defined in latency.py.
    Budgets (ms): HullDamage=100, FSDJump=200, Docked=200, Loadout=500.
    """
    from omnicovas.core.latency import BUDGETS

    state, _, dispatcher, _ = build_full_stack()

    with open(FIXTURE_JOURNAL, encoding="utf-8") as f:
        lines = [raw.strip() for raw in f if raw.strip()]

    tolerance = 2.0  # CI multiplier

    for line in lines:
        import json as _json

        try:
            ev = _json.loads(line)
        except Exception:
            continue
        event_type = ev.get("event", "")
        budget = BUDGETS.get(event_type)

        start = time.perf_counter()
        await dispatcher.dispatch(line)
        await asyncio.sleep(0)
        elapsed_ms = (time.perf_counter() - start) * 1000

        if budget is not None:
            assert elapsed_ms <= budget.budget_ms * tolerance, (
                f"{event_type} took {elapsed_ms:.1f}ms, "
                f"budget={budget.budget_ms}ms * {tolerance}x"
            )


@pytest.mark.asyncio
async def test_phase1_fields_remain_consistent() -> None:
    """Phase 1 state fields (current_system, is_docked) update correctly."""
    state, _, dispatcher, _ = build_full_stack()
    await replay_journal(dispatcher, FIXTURE_JOURNAL)
    snap = state.snapshot

    # Final system after last FSDJump
    assert snap.current_system == "Alpha Centauri"
    # Final docked state: Undocked event fires after RefuelAll
    assert snap.is_docked is False


@pytest.mark.asyncio
async def test_loadout_changed_only_on_real_change() -> None:
    """LOADOUT_CHANGED fires on first Loadout and on configuration change only.

    The replay fires the identical Loadout twice (pre-combat and post-repair).
    The second Loadout has the same modules list -> same hash -> no broadcast.
    """
    state, broadcaster, dispatcher, _ = build_full_stack()
    collector = EventCollector()
    broadcaster.subscribe(LOADOUT_CHANGED, collector.handle)

    await replay_journal(dispatcher, FIXTURE_JOURNAL)

    # First Loadout: hash changes from None -> broadcasts LOADOUT_CHANGED.
    # Second Loadout: same modules list -> same hash -> no broadcast.
    assert collector.count(LOADOUT_CHANGED) == 1


@pytest.mark.asyncio
async def test_rebuy_cost_matches_loadout_values() -> None:
    """calculate_rebuy() result matches (hull_value + modules_value) * 5%."""
    state, _, dispatcher, _ = build_full_stack()
    await replay_journal(dispatcher, FIXTURE_JOURNAL)

    snap = state.snapshot
    assert snap.hull_value == 56_978_012
    assert snap.modules_value == 48_500_000

    rebuy = calculate_rebuy(state)
    assert rebuy == int((56_978_012 + 48_500_000) * 0.05)
