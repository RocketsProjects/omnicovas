# tests/test_extended_broadcaster.py
import asyncio

import pytest

from omnicovas.core.broadcaster import (  # noqa: E402
    ShipStateBroadcaster,
    ShipStateEvent,
)
from omnicovas.core.event_types import DESTROYED, DOCKED, FSD_JUMP, UNDOCKED, WANTED
from omnicovas.core.state_manager import StateManager
from omnicovas.features.extended_events import (
    handle_commit_crime,
    handle_docked,
    handle_fsd_jump,
    handle_ship_destroyed,
    handle_undocked,
)

captured: list[ShipStateEvent] = []


async def _capture(event: ShipStateEvent) -> None:
    captured.append(event)


@pytest.fixture(autouse=True)
def _reset_captured() -> None:  # noqa: PT004
    """Reset captured events before each test."""
    captured.clear()


@pytest.mark.asyncio
async def test_docked_publishes_docked() -> None:
    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    broadcaster.subscribe(DOCKED, _capture)

    event = {
        "timestamp": "2026-04-27T12:00:00Z",
        "StationName": "Jameson Memorial",
        "StationType": "Coriolis",
        "StarSystem": "Shinrarta Dezhra",
        "MarketID": 123456,
    }

    await handle_docked(event, state, broadcaster)
    await asyncio.sleep(0)

    assert len(captured) == 1
    assert captured[0].event_type == DOCKED
    assert captured[0].payload["station"] == "Jameson Memorial"
    assert state.snapshot.is_docked is True


@pytest.mark.asyncio
async def test_undocked_publishes_undocked() -> None:
    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    broadcaster.subscribe(UNDOCKED, _capture)

    event = {
        "timestamp": "2026-04-27T12:00:00Z",
        "StationName": "Jameson Memorial",
    }

    await handle_undocked(event, state, broadcaster)
    await asyncio.sleep(0)

    assert len(captured) == 1
    assert captured[0].event_type == UNDOCKED
    assert state.snapshot.is_docked is False


@pytest.mark.asyncio
async def test_fsd_jump_publishes_fsd_jump() -> None:
    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    broadcaster.subscribe(FSD_JUMP, _capture)

    last_holder: dict[str, str | None] = {"value": None}

    event = {
        "timestamp": "2026-04-27T12:00:00Z",
        "StarSystem": "Sol",
        "SystemAddress": 10477373803,
        "Population": 22780871671,
    }

    await handle_fsd_jump(event, state, broadcaster, last_holder)
    await asyncio.sleep(0)

    assert len(captured) == 1
    assert captured[0].event_type == FSD_JUMP
    assert captured[0].payload["system"] == "Sol"
    assert state.snapshot.current_system == "Sol"


@pytest.mark.asyncio
async def test_wanted_set_on_commit_crime() -> None:
    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    broadcaster.subscribe(WANTED, _capture)

    event = {
        "timestamp": "2026-04-27T12:00:00Z",
        "CrimeType": "murder",
    }

    await handle_commit_crime(event, state, broadcaster)
    await asyncio.sleep(0)

    assert len(captured) == 1
    assert captured[0].event_type == WANTED
    assert state.snapshot.is_wanted_in_system is True


@pytest.mark.asyncio
async def test_wanted_cleared_on_fsd_jump_to_new_system() -> None:
    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    broadcaster.subscribe(FSD_JUMP, _capture)

    last_holder: dict[str, str | None] = {"value": "OldSystem"}
    state._state.is_wanted_in_system = True

    event = {
        "timestamp": "2026-04-27T12:00:00Z",
        "StarSystem": "NewSystem",
    }

    await handle_fsd_jump(event, state, broadcaster, last_holder)
    await asyncio.sleep(0)

    assert state.snapshot.is_wanted_in_system is False


@pytest.mark.asyncio
async def test_wanted_not_cleared_on_fsd_jump_to_same_system() -> None:
    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    broadcaster.subscribe(FSD_JUMP, _capture)

    last_holder: dict[str, str | None] = {"value": "SameSystem"}
    state._state.is_wanted_in_system = True

    event = {
        "timestamp": "2026-04-27T12:00:00Z",
        "StarSystem": "SameSystem",
    }

    await handle_fsd_jump(event, state, broadcaster, last_holder)
    await asyncio.sleep(0)

    assert state.snapshot.is_wanted_in_system is True


@pytest.mark.asyncio
async def test_destroyed_publishes_destroyed_and_resets_state() -> None:
    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    broadcaster.subscribe(DESTROYED, _capture)

    state._state.hull_health = 0.05
    state._state.current_ship_type = "Python"
    state._state.current_system = "Shinrarta Dezhra"

    event = {"timestamp": "2026-04-27T12:00:00Z"}

    await handle_ship_destroyed(event, state, broadcaster)
    await asyncio.sleep(0)

    assert len(captured) == 1
    assert captured[0].event_type == DESTROYED
    assert captured[0].payload["ship_type"] == "Python"
    assert captured[0].payload["system"] == "Shinrarta Dezhra"
    assert state.snapshot.hull_health is None
    assert state.snapshot.modules == {}
