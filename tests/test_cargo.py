# tests/test_cargo.py
"""Tests for omnicovas/features/cargo.py — Feature 6 (Cargo Monitoring)."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import CARGO_CHANGED
from omnicovas.core.state_manager import StateManager
from omnicovas.features.cargo import handle_cargo


@pytest.fixture
def state() -> StateManager:
    return StateManager()


@pytest.fixture
def broadcaster() -> ShipStateBroadcaster:
    return ShipStateBroadcaster()


@pytest.fixture
def cargo_event_ship() -> dict[str, Any]:
    return {
        "timestamp": "2026-04-26T12:00:00Z",
        "Vessel": "Ship",
        "Count": 10,
        "Inventory": [
            {"Name": "gold", "Count": 5},
            {"Name": "silver", "Count": 5},
        ],
    }


@pytest.fixture
def cargo_event_srv() -> dict[str, Any]:
    return {
        "timestamp": "2026-04-26T12:00:00Z",
        "Vessel": "SRV",
        "Inventory": [{"Name": "gold", "Count": 5}],
    }


@pytest.fixture
def cargo_event_suit() -> dict[str, Any]:
    return {
        "timestamp": "2026-04-26T12:00:00Z",
        "Vessel": "Suit",
        "Inventory": [{"Name": "suits", "Count": 1}],
    }


@pytest.fixture
def cargo_event_no_vessel() -> dict[str, Any]:
    return {
        "timestamp": "2026-04-26T12:00:00Z",
        "Inventory": [{"Name": "gold", "Count": 3}],
    }


@pytest.fixture
def cargo_event_invalid() -> dict[str, Any]:
    return {
        "timestamp": "2026-04-26T12:00:00Z",
        "Vessel": "Ship",
        "Inventory": [
            {"Name": "gold", "Count": 5},
            {"Count": 10},
            "not a dict",
        ],
    }


async def test_cargo_populated_from_event(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    cargo_event_ship: dict[str, Any],
) -> None:
    await handle_cargo(cargo_event_ship, state, broadcaster)
    assert state.snapshot.cargo_inventory == {"gold": 5, "silver": 5}
    assert state.snapshot.cargo_count == 10


async def test_srv_cargo_skipped(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    cargo_event_srv: dict[str, Any],
) -> None:
    await handle_cargo(cargo_event_srv, state, broadcaster)
    assert state.snapshot.cargo_inventory == {}


async def test_suit_cargo_skipped(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    cargo_event_suit: dict[str, Any],
) -> None:
    await handle_cargo(cargo_event_suit, state, broadcaster)
    assert state.snapshot.cargo_inventory == {}


async def test_absent_vessel_treated_as_ship(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    cargo_event_no_vessel: dict[str, Any],
) -> None:
    await handle_cargo(cargo_event_no_vessel, state, broadcaster)
    assert state.snapshot.cargo_inventory == {"gold": 3}


async def test_cargo_changed_published(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    cargo_event_ship: dict[str, Any],
) -> None:
    captured: list[ShipStateEvent] = []

    async def _capture(event: ShipStateEvent) -> None:
        captured.append(event)

    broadcaster.subscribe(CARGO_CHANGED, _capture)
    await handle_cargo(cargo_event_ship, state, broadcaster)
    await asyncio.sleep(0)
    assert len(captured) == 1
    assert captured[0].payload["commodity_types"] == 2


async def test_invalid_inventory_entries_skipped(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
    cargo_event_invalid: dict[str, Any],
) -> None:
    await handle_cargo(cargo_event_invalid, state, broadcaster)
    assert state.snapshot.cargo_inventory == {"gold": 5}
