# tests/test_module_health.py
"""Tests for omnicovas/features/module_health.py — Feature 2 (Module Health)."""

from __future__ import annotations

import asyncio

import pytest

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import LOADOUT_CHANGED, MODULE_CRITICAL, MODULE_DAMAGED
from omnicovas.core.state_manager import ModuleInfo, StateManager
from omnicovas.features.module_health import register_subscriber


def _mod(slot: str, health: float) -> ModuleInfo:
    return ModuleInfo(
        slot=slot,
        item="test_item",
        item_localised=None,
        health=health,
        power=None,
        priority=None,
        on=True,
        engineering=None,
    )


@pytest.fixture
def state() -> StateManager:
    return StateManager()


@pytest.fixture
def broadcaster() -> ShipStateBroadcaster:
    return ShipStateBroadcaster()


async def _trigger(broadcaster: ShipStateBroadcaster) -> None:
    await broadcaster.publish(
        LOADOUT_CHANGED,
        ShipStateEvent.now(LOADOUT_CHANGED, {}, source="journal"),
    )
    await asyncio.sleep(0)  # let _on_loadout_changed run
    await asyncio.sleep(0)  # let MODULE_DAMAGED/CRITICAL _capture tasks run


async def test_healthy_modules_produce_no_events(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    captured: list[tuple[str, ShipStateEvent]] = []

    async def _capture(event: ShipStateEvent) -> None:
        captured.append((event.event_type, event))

    register_subscriber(state, broadcaster)
    broadcaster.subscribe(MODULE_DAMAGED, _capture)
    broadcaster.subscribe(MODULE_CRITICAL, _capture)

    state._state.modules = {"slot1": _mod("slot1", 1.0), "slot2": _mod("slot2", 1.0)}
    await _trigger(broadcaster)
    assert captured == []


async def test_damaged_module_fires_module_damaged(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    captured: list[tuple[str, ShipStateEvent]] = []

    async def _capture(event: ShipStateEvent) -> None:
        captured.append((event.event_type, event))

    register_subscriber(state, broadcaster)
    broadcaster.subscribe(MODULE_DAMAGED, _capture)
    broadcaster.subscribe(MODULE_CRITICAL, _capture)

    state._state.modules = {"slot1": _mod("slot1", 0.5)}
    await _trigger(broadcaster)
    assert len(captured) == 1
    assert captured[0][0] == MODULE_DAMAGED
    assert captured[0][1].payload["health"] == 0.5


async def test_critical_module_fires_module_critical_only(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    captured: list[tuple[str, ShipStateEvent]] = []

    async def _capture(event: ShipStateEvent) -> None:
        captured.append((event.event_type, event))

    register_subscriber(state, broadcaster)
    broadcaster.subscribe(MODULE_DAMAGED, _capture)
    broadcaster.subscribe(MODULE_CRITICAL, _capture)

    state._state.modules = {"slot1": _mod("slot1", 0.1)}
    await _trigger(broadcaster)
    assert len(captured) == 1
    assert captured[0][0] == MODULE_CRITICAL
    assert MODULE_DAMAGED not in [e[0] for e in captured]


async def test_mixed_modules_correct_events(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    captured: list[tuple[str, ShipStateEvent]] = []

    async def _capture(event: ShipStateEvent) -> None:
        captured.append((event.event_type, event))

    register_subscriber(state, broadcaster)
    broadcaster.subscribe(MODULE_DAMAGED, _capture)
    broadcaster.subscribe(MODULE_CRITICAL, _capture)

    state._state.modules = {
        "healthy": _mod("healthy", 1.0),
        "damaged": _mod("damaged", 0.6),
        "critical": _mod("critical", 0.15),
    }
    await _trigger(broadcaster)
    assert len(captured) == 2
    event_types = [e[0] for e in captured]
    assert MODULE_DAMAGED in event_types
    assert MODULE_CRITICAL in event_types


async def test_empty_modules_no_events(
    state: StateManager,
    broadcaster: ShipStateBroadcaster,
) -> None:
    captured: list[tuple[str, ShipStateEvent]] = []

    async def _capture(event: ShipStateEvent) -> None:
        captured.append((event.event_type, event))

    register_subscriber(state, broadcaster)
    broadcaster.subscribe(MODULE_DAMAGED, _capture)
    broadcaster.subscribe(MODULE_CRITICAL, _capture)

    state._state.modules = {}
    await _trigger(broadcaster)
    assert captured == []
