"""
tests.test_state_contract

Phase 3.1.2 — /state endpoint contract tests.

These tests verify that dispatching real journal/Status events updates
StateManager fields AND that those changes are visible through the
ApiBridge GET /state endpoint.

This proves the full propagation chain:
    event dispatch → handlers.py → StateManager → /state response

Tests:
    1. FSDJump → current_system updated in /state
    2. Undocked → is_docked=False in /state
    3. Docked → is_docked=True in /state
    4. Status pips → sys_pips/eng_pips/wep_pips in /state
    5. Status heat → heat_level in /state
    6. ShieldsDown → shield_up=False in /state
    7. ShieldsUp → shield_up=True in /state
    8. Loadout → current_ship_type in /state
    9. Cargo event → cargo_count in /state
"""

from __future__ import annotations

import asyncio
import json

import pytest
from fastapi.testclient import TestClient

from omnicovas.core.api_bridge import ApiBridge
from omnicovas.core.broadcaster import ShipStateBroadcaster
from omnicovas.core.dispatcher import EventDispatcher
from omnicovas.core.handlers import make_handlers
from omnicovas.core.state_manager import StateManager
from omnicovas.features import cargo as _cargo
from omnicovas.features import extended_events as _extended
from omnicovas.features import fuel as _fuel
from omnicovas.features import heat_management as _heat
from omnicovas.features import hull_triggers as _hull
from omnicovas.features import loadout as _loadout
from omnicovas.features import module_health as _module_health
from omnicovas.features import power_distribution as _pips
from omnicovas.features import ship_state as _ship_state

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_stack() -> tuple[StateManager, EventDispatcher, TestClient]:
    """
    Wire the full Pillar 1 handler stack and expose /state via ApiBridge._app.
    Mirrors build_full_stack() from test_phase2_integration.py, then wraps
    the FastAPI app in a TestClient for synchronous endpoint assertions.
    """
    state = StateManager()
    broadcaster = ShipStateBroadcaster()
    dispatcher = EventDispatcher()

    # Phase 1 core handlers
    handlers = make_handlers(state, broadcaster)
    for event_type, handler in handlers.items():
        dispatcher.register(event_type, handler)

    # Phase 2 feature handlers (own the ShieldsDown/Up, Loadout, Cargo events)
    _ship_state.register(dispatcher.register, state, broadcaster)
    _loadout.register(dispatcher.register, state, broadcaster)
    _fuel.register(dispatcher.register, state, broadcaster)
    _cargo.register(dispatcher.register, state, broadcaster)
    _module_health.register_subscriber(state, broadcaster)
    _hull.register(dispatcher.register, state, broadcaster)
    _extended.register(dispatcher.register, state, broadcaster)
    _pips.register(dispatcher.register, state, broadcaster)
    _heat.register(dispatcher.register, state, broadcaster)

    bridge = ApiBridge(state_manager=state)
    client = TestClient(bridge._app)
    return state, dispatcher, client


async def _dispatch(dispatcher: EventDispatcher, event: dict) -> None:
    """Dispatch a single event dict and flush async tasks."""
    await dispatcher.dispatch(json.dumps(event))
    await asyncio.sleep(0)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_state_after_fsd_jump() -> None:
    """FSDJump must update current_system visible through /state."""
    state, dispatcher, client = _build_stack()

    await _dispatch(
        dispatcher,
        {
            "event": "FSDJump",
            "timestamp": "2026-04-29T14:42:00Z",
            "StarSystem": "Wolf 397",
        },
    )

    resp = client.get("/state")
    assert resp.status_code == 200
    body = resp.json()
    assert body["current_system"] == "Wolf 397"


@pytest.mark.asyncio
async def test_state_after_undocked() -> None:
    """Undocked must set is_docked=False in /state."""
    state, dispatcher, client = _build_stack()

    await _dispatch(
        dispatcher,
        {
            "event": "Undocked",
            "timestamp": "2026-04-29T14:42:01Z",
            "StationName": "Jameson Memorial",
        },
    )

    resp = client.get("/state")
    assert resp.status_code == 200
    assert resp.json()["is_docked"] is False


@pytest.mark.asyncio
async def test_state_after_docked() -> None:
    """Docked event must set is_docked=True and current_station in /state."""
    state, dispatcher, client = _build_stack()

    await _dispatch(
        dispatcher,
        {
            "event": "Docked",
            "timestamp": "2026-04-29T14:43:00Z",
            "StationName": "Daedalus",
            "StarSystem": "Sol",
        },
    )

    resp = client.get("/state")
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_docked"] is True
    assert body["current_station"] == "Daedalus"


@pytest.mark.asyncio
async def test_state_after_status_pips() -> None:
    """
    A Status event containing Pips must update sys_pips/eng_pips/wep_pips in /state.

    This confirms the handlers.py handle_status path correctly writes pips to
    StateManager via TelemetrySource.STATUS_JSON.
    """
    state, dispatcher, client = _build_stack()

    await _dispatch(
        dispatcher,
        {
            "event": "Status",
            "timestamp": "2026-04-29T14:42:05Z",
            "Flags": 0,
            "Pips": [8, 2, 2],
            "Heat": 0.3,
            "Fuel": {},
            "SubEvents": [],
        },
    )

    resp = client.get("/state")
    assert resp.status_code == 200
    body = resp.json()
    assert body["sys_pips"] == 8
    assert body["eng_pips"] == 2
    assert body["wep_pips"] == 2


@pytest.mark.asyncio
async def test_state_after_status_heat() -> None:
    """Status event heat value must reach heat_level in /state."""
    state, dispatcher, client = _build_stack()

    await _dispatch(
        dispatcher,
        {
            "event": "Status",
            "timestamp": "2026-04-29T14:42:06Z",
            "Flags": 0,
            "Pips": [],
            "Heat": 0.85,
            "Fuel": {},
            "SubEvents": [],
        },
    )

    resp = client.get("/state")
    assert resp.status_code == 200
    assert resp.json()["heat_level"] == pytest.approx(0.85)


@pytest.mark.asyncio
async def test_state_after_shields_down() -> None:
    """ShieldsDown journal event must set shield_up=False in /state."""
    state, dispatcher, client = _build_stack()

    # Start with shields up via Status so there's a known baseline
    await _dispatch(
        dispatcher,
        {
            "event": "Status",
            "timestamp": "2026-04-29T14:42:07Z",
            "Flags": 1 << 3,
            "Pips": [4, 4, 4],
            "Heat": 0.2,
            "Fuel": {},
            "SubEvents": [],
        },
    )

    await _dispatch(
        dispatcher,
        {"event": "ShieldsDown", "timestamp": "2026-04-29T14:42:08Z"},
    )

    resp = client.get("/state")
    assert resp.status_code == 200
    assert resp.json()["shield_up"] is False


@pytest.mark.asyncio
async def test_state_after_shields_up() -> None:
    """ShieldsUp journal event must set shield_up=True in /state."""
    state, dispatcher, client = _build_stack()

    await _dispatch(
        dispatcher,
        {"event": "ShieldsUp", "timestamp": "2026-04-29T14:42:09Z"},
    )

    resp = client.get("/state")
    assert resp.status_code == 200
    assert resp.json()["shield_up"] is True


@pytest.mark.asyncio
async def test_state_after_loadout() -> None:
    """Loadout event must update current_ship_type in /state."""
    state, dispatcher, client = _build_stack()

    # Minimal Loadout payload — only fields handlers.py reads
    await _dispatch(
        dispatcher,
        {
            "event": "Loadout",
            "timestamp": "2026-04-29T14:42:10Z",
            "Ship": "Python",
            "ShipID": 1,
            "ShipIdent": "PY-01",
            "ShipName": "The Snake",
            "MaxJumpRange": 22.5,
            "HullValue": 56_000_000,
            "ModulesValue": 40_000_000,
            "Modules": [],
        },
    )

    resp = client.get("/state")
    assert resp.status_code == 200
    body = resp.json()
    assert body["current_ship_type"] == "Python"


@pytest.mark.asyncio
async def test_state_after_cargo_event() -> None:
    """
    Cargo journal event must update cargo_count in /state.

    The Cargo event carries a Count field; handlers.py writes cargo_count.
    """
    state, dispatcher, client = _build_stack()

    await _dispatch(
        dispatcher,
        {
            "event": "Cargo",
            "timestamp": "2026-04-29T14:42:11Z",
            "Vessel": "Ship",
            "Count": 48,
            "Inventory": [],
        },
    )

    resp = client.get("/state")
    assert resp.status_code == 200
    assert resp.json()["cargo_count"] == 48
