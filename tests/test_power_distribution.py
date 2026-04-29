# tests/test_power_distribution.py
"""
tests/test_power_distribution

Tests for omnicovas.features.power_distribution.

Uses real ShipStateBroadcaster with subscription capture.
No AsyncMock — tests verify actual broadcast behavior.
"""

from __future__ import annotations

import asyncio

import pytest

from omnicovas.core.broadcaster import ShipStateBroadcaster, ShipStateEvent
from omnicovas.core.event_types import PIPS_CHANGED
from omnicovas.features.power_distribution import handle_status_pips


@pytest.fixture
def broadcaster() -> ShipStateBroadcaster:
    """Create a fresh broadcaster for each test."""
    return ShipStateBroadcaster()


@pytest.fixture
def prev_holder() -> dict[str, tuple[int, int, int] | None]:
    """Create a fresh prev_holder for each test."""
    return {"value": None}


@pytest.fixture
def captured() -> list[ShipStateEvent]:
    """Create a fresh captured list for each test."""
    return []


@pytest.fixture
def _capture(captured: list[ShipStateEvent]) -> None:
    """Capture callback for broadcaster subscription."""

    def _capture(event: ShipStateEvent) -> None:
        captured.append(event)

    return _capture


async def test_first_status_publishes_pips_changed(
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, tuple[int, int, int] | None],
    captured: list[ShipStateEvent],
    _capture: None,
) -> None:
    """Test that first status event with pips publishes PIPS_CHANGED."""
    broadcaster.subscribe(PIPS_CHANGED, _capture)
    await asyncio.sleep(0)

    event = {"timestamp": "...", "Pips": [4, 4, 4]}
    await handle_status_pips(event, broadcaster, prev_holder)
    await asyncio.sleep(0)

    assert len(captured) == 1
    assert captured[0].payload == {"sys": 4, "eng": 4, "wep": 4}


async def test_identical_pips_no_broadcast(
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, tuple[int, int, int] | None],
    captured: list[ShipStateEvent],
    _capture: None,
) -> None:
    """Test that identical pips do not trigger broadcast."""
    prev_holder["value"] = (4, 4, 4)  # simulate previous reading
    broadcaster.subscribe(PIPS_CHANGED, _capture)
    await asyncio.sleep(0)

    event = {"Pips": [4, 4, 4]}
    await handle_status_pips(event, broadcaster, prev_holder)
    await asyncio.sleep(0)

    assert len(captured) == 0


async def test_changed_pips_publishes_pips_changed(
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, tuple[int, int, int] | None],
    captured: list[ShipStateEvent],
    _capture: None,
) -> None:
    """Test that changed pips trigger PIPS_CHANGED broadcast."""
    prev_holder["value"] = (4, 4, 4)
    broadcaster.subscribe(PIPS_CHANGED, _capture)
    await asyncio.sleep(0)

    event = {"Pips": [6, 2, 4]}
    await handle_status_pips(event, broadcaster, prev_holder)
    await asyncio.sleep(0)

    assert len(captured) == 1
    assert captured[0].payload == {"sys": 6, "eng": 2, "wep": 4}


async def test_absent_pips_no_broadcast(
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, tuple[int, int, int] | None],
    captured: list[ShipStateEvent],
    _capture: None,
) -> None:
    """Test that absent pips (on-foot) do not trigger broadcast."""
    broadcaster.subscribe(PIPS_CHANGED, _capture)
    await asyncio.sleep(0)

    event = {"timestamp": "...", "Flags": 0}  # no "Pips" key — on-foot scenario
    await handle_status_pips(event, broadcaster, prev_holder)
    await asyncio.sleep(0)

    assert len(captured) == 0


async def test_absent_pips_does_not_clear_previous(
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, tuple[int, int, int] | None],
    captured: list[ShipStateEvent],
    _capture: None,
) -> None:
    """Test that absent pips do not clear previous value."""
    prev_holder["value"] = (4, 4, 4)
    broadcaster.subscribe(PIPS_CHANGED, _capture)
    await asyncio.sleep(0)

    event = {"Flags": 0}  # no Pips key
    await handle_status_pips(event, broadcaster, prev_holder)
    await asyncio.sleep(0)

    assert prev_holder["value"] == (4, 4, 4)  # unchanged


# ---------------------------------------------------------------------------
# Phase 3.1.2 — broadcast payload correctness
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_pips_changed_broadcasts_correct_values(
    broadcaster: ShipStateBroadcaster,
    prev_holder: dict[str, tuple[int, int, int] | None],
    captured: list[ShipStateEvent],
    _capture: None,
) -> None:
    """
    PIPS_CHANGED payload must contain the exact sys/eng/wep values from the
    Status.json Pips array.

    Phase 3.1.2 audit: confirms the broadcast carries the right data so
    downstream UI and tests can rely on payload shape.
    """
    broadcaster.subscribe(PIPS_CHANGED, _capture)
    await asyncio.sleep(0)

    await handle_status_pips({"Pips": [8, 2, 2]}, broadcaster, prev_holder)
    await asyncio.sleep(0)

    assert len(captured) == 1
    payload = captured[0].payload
    assert payload["sys"] == 8
    assert payload["eng"] == 2
    assert payload["wep"] == 2
