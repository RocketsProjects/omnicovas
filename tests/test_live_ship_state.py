"""
tests.test_live_ship_state

Tests for Feature 1 -- Live Ship State (Week 7 Part C).

Verifies that LoadGame, Loadout, and ShipyardSwap handlers:
    - Update the correct StateManager fields
    - Publish the correct broadcaster events
    - Compute stable loadout hashes
    - Suppress LOADOUT_CHANGED on repair events (hash unchanged)
    - Clear state cleanly on ShipyardSwap

Related to: Phase 2 Development Guide Week 7, Part C
Related to: Law 5 (Zero Hallucination) -- only write fields present in event
Related to: Law 7 (Telemetry Rigidity) -- journal is authoritative source
"""

from __future__ import annotations

from typing import Any

import pytest

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import LOADOUT_CHANGED, SHIP_STATE_CHANGED
from omnicovas.core.state_manager import StateManager
from omnicovas.features.ship_state import (
    compute_loadout_hash,
    handle_load_game,
    handle_loadout,
    handle_shipyard_swap,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def state() -> StateManager:
    return StateManager()


@pytest.fixture
def broadcaster() -> ShipStateBroadcaster:
    return ShipStateBroadcaster()


def make_load_game(
    ship: str = "Python",
    ship_id: int = 1,
    ship_name: str = "The Longbow",
    ship_ident: str = "PY-01",
    commander: str = "TestCmdr",
) -> dict[str, Any]:
    return {
        "timestamp": "2026-04-19T12:00:00Z",
        "event": "LoadGame",
        "Ship": ship,
        "ShipID": ship_id,
        "ShipName": ship_name,
        "ShipIdent": ship_ident,
        "Commander": commander,
    }


def make_loadout(
    ship: str = "Python",
    ship_id: int = 1,
    hull_health: float = 1.0,
    max_jump: float = 30.5,
    fuel_main: float = 16.0,
    modules: list[Any] | None = None,
) -> dict[str, Any]:
    if modules is None:
        modules = [
            {"Slot": "FrameShiftDrive", "Item": "int_hyperdrive_size5_class5"},
            {"Slot": "PowerPlant", "Item": "int_powerplant_size6_class5"},
        ]
    return {
        "timestamp": "2026-04-19T12:00:01Z",
        "event": "Loadout",
        "Ship": ship,
        "ShipID": ship_id,
        "ShipName": "The Longbow",
        "ShipIdent": "PY-01",
        "HullHealth": hull_health,
        "MaxJumpRange": max_jump,
        "FuelCapacity": {"Main": fuel_main, "Reserve": 0.5},
        "Modules": modules,
    }


# ---------------------------------------------------------------------------
# handle_load_game
# ---------------------------------------------------------------------------


async def test_load_game_sets_ship_identity(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """LoadGame must populate all four ship identity fields."""
    await handle_load_game(make_load_game(), state, broadcaster)

    snap = state.snapshot
    assert snap.current_ship_type == "Python"
    assert snap.current_ship_id == 1
    assert snap.current_ship_name == "The Longbow"
    assert snap.current_ship_ident == "PY-01"
    assert snap.commander_name == "TestCmdr"


async def test_load_game_publishes_ship_state_changed(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """LoadGame must broadcast SHIP_STATE_CHANGED."""
    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(SHIP_STATE_CHANGED, capture)
    await handle_load_game(make_load_game(), state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 1
    assert received[0].event_type == SHIP_STATE_CHANGED
    assert received[0].payload["trigger"] == "LoadGame"
    assert received[0].source == "journal"


async def test_load_game_missing_optional_fields(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """LoadGame without ShipName/ShipIdent must not fabricate those fields."""
    event = {
        "timestamp": "2026-04-19T12:00:00Z",
        "event": "LoadGame",
        "Ship": "SideWinder",
        "ShipID": 0,
        "Commander": "TestCmdr",
        # ShipName and ShipIdent deliberately absent
    }
    await handle_load_game(event, state, broadcaster)

    snap = state.snapshot
    assert snap.current_ship_type == "SideWinder"
    assert snap.current_ship_name is None  # not fabricated
    assert snap.current_ship_ident is None  # not fabricated


# ---------------------------------------------------------------------------
# handle_loadout
# ---------------------------------------------------------------------------


async def test_loadout_sets_hull_and_jump(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """Loadout must populate hull_health and jump_range_ly."""
    await handle_loadout(
        make_loadout(hull_health=0.95, max_jump=38.4), state, broadcaster
    )

    snap = state.snapshot
    assert snap.hull_health == pytest.approx(0.95)
    assert snap.jump_range_ly == pytest.approx(38.4)


async def test_loadout_sets_fuel_capacity(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """Loadout must extract fuel capacity from FuelCapacity.Main."""
    await handle_loadout(make_loadout(fuel_main=32.0), state, broadcaster)
    assert state.snapshot.fuel_capacity == pytest.approx(32.0)


async def test_loadout_publishes_ship_state_changed(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """Loadout must always broadcast SHIP_STATE_CHANGED."""
    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(SHIP_STATE_CHANGED, capture)
    await handle_loadout(make_loadout(), state, broadcaster)
    await _drain(broadcaster)

    assert any(e.payload.get("trigger") == "Loadout" for e in received)


async def test_loadout_broadcasts_loadout_changed_on_first_load(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """First Loadout (hash was None) must broadcast LOADOUT_CHANGED."""
    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(LOADOUT_CHANGED, capture)
    await handle_loadout(make_loadout(), state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 1
    assert received[0].event_type == LOADOUT_CHANGED


async def test_loadout_suppresses_loadout_changed_on_repair(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """Repair (same modules, different health) must NOT broadcast LOADOUT_CHANGED."""
    modules = [
        {"Slot": "FrameShiftDrive", "Item": "int_hyperdrive_size5_class5"},
        {"Slot": "PowerPlant", "Item": "int_powerplant_size6_class5"},
    ]
    # First loadout -- establishes hash
    await handle_loadout(
        make_loadout(hull_health=0.7, modules=modules), state, broadcaster
    )
    await _drain(broadcaster)

    # Second loadout -- same modules, higher health (repair) -- hash unchanged
    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(LOADOUT_CHANGED, capture)
    await handle_loadout(
        make_loadout(hull_health=1.0, modules=modules), state, broadcaster
    )
    await _drain(broadcaster)

    assert len(received) == 0  # no LOADOUT_CHANGED for repair


async def test_loadout_broadcasts_loadout_changed_on_refit(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """Changing a module must broadcast LOADOUT_CHANGED."""
    modules_before = [
        {"Slot": "FrameShiftDrive", "Item": "int_hyperdrive_size5_class5"},
    ]
    modules_after = [
        {"Slot": "FrameShiftDrive", "Item": "int_hyperdrive_size6_class5"},  # upgraded
    ]
    await handle_loadout(make_loadout(modules=modules_before), state, broadcaster)
    await _drain(broadcaster)

    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(LOADOUT_CHANGED, capture)
    await handle_loadout(make_loadout(modules=modules_after), state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 1


# ---------------------------------------------------------------------------
# handle_shipyard_swap
# ---------------------------------------------------------------------------


async def test_shipyard_swap_updates_ship_type(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """ShipyardSwap must update ship type and ID."""
    # Pre-populate with Python
    await handle_loadout(make_loadout(ship="Python", ship_id=1), state, broadcaster)
    await _drain(broadcaster)

    swap_event = {
        "timestamp": "2026-04-19T12:05:00Z",
        "event": "ShipyardSwap",
        "ShipType": "Anaconda",
        "ShipID": 2,
    }
    await handle_shipyard_swap(swap_event, state, broadcaster)

    snap = state.snapshot
    assert snap.current_ship_type == "Anaconda"
    assert snap.current_ship_id == 2


async def test_shipyard_swap_clears_ship_specific_state(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """ShipyardSwap must clear hull, jump range, and loadout hash."""
    await handle_loadout(
        make_loadout(hull_health=0.8, max_jump=30.0), state, broadcaster
    )
    await _drain(broadcaster)

    assert state.snapshot.hull_health is not None
    assert state.snapshot.jump_range_ly is not None
    assert state.snapshot.loadout_hash is not None

    swap_event = {
        "timestamp": "2026-04-19T12:05:00Z",
        "event": "ShipyardSwap",
        "ShipType": "Anaconda",
        "ShipID": 2,
    }
    await handle_shipyard_swap(swap_event, state, broadcaster)

    snap = state.snapshot
    assert snap.hull_health is None
    assert snap.jump_range_ly is None
    assert snap.loadout_hash is None
    assert snap.modules == {}


async def test_shipyard_swap_publishes_ship_state_changed(
    state: StateManager, broadcaster: ShipStateBroadcaster
) -> None:
    """ShipyardSwap must broadcast SHIP_STATE_CHANGED."""
    received: list[ShipStateEvent] = []

    async def capture(e: ShipStateEvent) -> None:
        received.append(e)

    broadcaster.subscribe(SHIP_STATE_CHANGED, capture)

    swap_event = {
        "timestamp": "2026-04-19T12:05:00Z",
        "event": "ShipyardSwap",
        "ShipType": "Anaconda",
        "ShipID": 2,
    }
    await handle_shipyard_swap(swap_event, state, broadcaster)
    await _drain(broadcaster)

    assert len(received) == 1
    assert received[0].payload["trigger"] == "ShipyardSwap"


# ---------------------------------------------------------------------------
# compute_loadout_hash
# ---------------------------------------------------------------------------


def test_hash_is_stable() -> None:
    """Same modules in same order must produce same hash."""
    modules = [
        {"Slot": "PowerPlant", "Item": "int_powerplant_size6_class5"},
        {"Slot": "FrameShiftDrive", "Item": "int_hyperdrive_size5_class5"},
    ]
    assert compute_loadout_hash(modules) == compute_loadout_hash(modules)


def test_hash_is_order_independent() -> None:
    """Modules in different order must produce same hash (sorted by slot)."""
    a = [
        {"Slot": "PowerPlant", "Item": "int_powerplant_size6_class5"},
        {"Slot": "FrameShiftDrive", "Item": "int_hyperdrive_size5_class5"},
    ]
    b = [
        {"Slot": "FrameShiftDrive", "Item": "int_hyperdrive_size5_class5"},
        {"Slot": "PowerPlant", "Item": "int_powerplant_size6_class5"},
    ]
    assert compute_loadout_hash(a) == compute_loadout_hash(b)


def test_hash_changes_on_item_change() -> None:
    """Swapping an item must change the hash."""
    before = [{"Slot": "FrameShiftDrive", "Item": "int_hyperdrive_size5_class5"}]
    after = [{"Slot": "FrameShiftDrive", "Item": "int_hyperdrive_size6_class5"}]
    assert compute_loadout_hash(before) != compute_loadout_hash(after)


def test_hash_stable_on_health_change() -> None:
    """Changing only module health must NOT change the hash."""
    before = [
        {
            "Slot": "PowerPlant",
            "Item": "int_powerplant_size6_class5",
            "Health": 1.0,
        }
    ]
    after = [
        {
            "Slot": "PowerPlant",
            "Item": "int_powerplant_size6_class5",
            "Health": 0.6,  # took damage
        }
    ]
    assert compute_loadout_hash(before) == compute_loadout_hash(after)


def test_hash_empty_modules() -> None:
    """Empty module list must return empty string (not crash)."""
    assert compute_loadout_hash([]) == ""


def test_hash_changes_on_engineering() -> None:
    """Adding engineering to a module must change the hash."""
    base = [{"Slot": "FrameShiftDrive", "Item": "int_hyperdrive_size5_class5"}]
    engineered = [
        {
            "Slot": "FrameShiftDrive",
            "Item": "int_hyperdrive_size5_class5",
            "Engineering": {"BlueprintName": "FSD_LongRange", "Level": 5},
        }
    ]
    assert compute_loadout_hash(base) != compute_loadout_hash(engineered)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _drain(broadcaster: ShipStateBroadcaster) -> None:
    """Wait for all in-flight broadcast tasks to complete."""
    import asyncio

    pending = list(broadcaster._tasks)
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)
