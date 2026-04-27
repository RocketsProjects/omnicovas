# tests/test_loadout_awareness.py
"""
tests/test_loadout_awareness.py

Tests for omnicovas.features.loadout — Feature 4 (Loadout Awareness).

Uses pytest + pytest-asyncio. Writes JSON literals directly in tests
(no file reads). Uses plausible but simple values only.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import SHIP_STATE_CHANGED
from omnicovas.core.state_manager import StateManager
from omnicovas.features.loadout import handle_loadout


@pytest.fixture
def state() -> StateManager:
    return StateManager()


@pytest.fixture
def broadcaster() -> ShipStateBroadcaster:
    return ShipStateBroadcaster()


@pytest.fixture
def loadout_event_two_modules() -> dict[str, Any]:
    return {
        "timestamp": "2024-01-01T00:00:00Z",
        "Modules": [
            {
                "Slot": "TinyHardpoint1",
                "Item": "hpt_pulselaser_fixed_small",
                "Health": 1.0,
                "On": True,
                "Engineering": {
                    "BlueprintName": "pulse_laser_small_1",
                },
            },
            {
                "Slot": "TinyHardpoint2",
                "Item": "hpt_pulselaser_fixed_small",
                "Health": 0.95,
                "On": True,
            },
        ],
    }


@pytest.fixture
def loadout_event_empty_modules() -> dict[str, Any]:
    return {
        "timestamp": "2024-01-01T00:00:00Z",
        "Modules": [],
    }


@pytest.fixture
def loadout_event_no_modules_key() -> dict[str, Any]:
    return {
        "timestamp": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def loadout_event_minimal_module() -> dict[str, Any]:
    return {
        "timestamp": "2024-01-01T00:00:00Z",
        "Modules": [
            {
                "Slot": "TinyHardpoint1",
                "Item": "hpt_pulselaser_fixed_small",
            },
        ],
    }


@pytest.fixture
def loadout_event_mixed_modules() -> dict[str, Any]:
    return {
        "timestamp": "2024-01-01T00:00:00Z",
        "Modules": [
            {
                "Slot": "TinyHardpoint1",
                "Item": "hpt_pulselaser_fixed_small",
                "Health": 1.0,
            },
            "invalid_string_entry",
        ],
    }


async def test_modules_populated_from_loadout(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    loadout_event_two_modules: dict[str, Any],
) -> None:
    await handle_loadout(loadout_event_two_modules, state, broadcaster)
    assert len(state.snapshot.modules) == 2
    assert "TinyHardpoint1" in state.snapshot.modules
    assert "TinyHardpoint2" in state.snapshot.modules
    assert state.snapshot.modules["TinyHardpoint1"].health == 1.0
    assert state.snapshot.modules["TinyHardpoint2"].health == 0.95
    assert state.snapshot.modules["TinyHardpoint1"].engineering is not None
    assert state.snapshot.modules["TinyHardpoint2"].engineering is None


async def test_empty_modules_clears_state(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    loadout_event_empty_modules: dict[str, Any],
) -> None:
    await handle_loadout(loadout_event_empty_modules, state, broadcaster)
    assert state.snapshot.modules == {}


async def test_missing_modules_key(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    loadout_event_no_modules_key: dict[str, Any],
) -> None:
    await handle_loadout(loadout_event_no_modules_key, state, broadcaster)
    assert state.snapshot.modules == {}


async def test_optional_fields_default_correctly(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    loadout_event_minimal_module: dict[str, Any],
) -> None:
    await handle_loadout(loadout_event_minimal_module, state, broadcaster)
    module = state.snapshot.modules["TinyHardpoint1"]
    assert module.health == 1.0
    assert module.power is None
    assert module.priority is None
    assert module.on is True
    assert module.engineering is None
    assert module.item_localised is None


async def test_ship_state_changed_published(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    loadout_event_two_modules: dict[str, Any],
) -> None:
    captured: list[ShipStateEvent] = []

    async def _capture(event: ShipStateEvent) -> None:
        captured.append(event)

    broadcaster.subscribe(SHIP_STATE_CHANGED, _capture)
    await handle_loadout(loadout_event_two_modules, state, broadcaster)
    await asyncio.sleep(0)
    assert len(captured) == 1
    assert captured[0].payload["module_count"] == 2


async def test_non_dict_module_entry_skipped(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    loadout_event_mixed_modules: dict[str, Any],
) -> None:
    await handle_loadout(loadout_event_mixed_modules, state, broadcaster)
    assert len(state.snapshot.modules) == 1
