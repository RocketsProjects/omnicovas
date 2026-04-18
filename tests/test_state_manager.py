"""
tests.test_state_manager

Tests for StateManager source priority enforcement.

Related to: Law 7 (Telemetry Rigidity) — source priority is non-negotiable
Related to: Law 5 (Zero Hallucination) — never fabricate data
Related to: Phase 1 Development Guide Week 3, Part A

Tests:
    1. First update always succeeds
    2. Equal-priority updates overwrite (newest wins)
    3. Higher-priority updates overwrite lower-priority
    4. Lower-priority updates are rejected when higher-priority exists
    5. Unknown field names are rejected safely
    6. Private fields cannot be written via update_field
    7. reset() clears all state
    8. Initial state is all None (Law 5)
"""

from __future__ import annotations

import pytest

from omnicovas.core.state_manager import StateManager, TelemetrySource


@pytest.mark.asyncio
async def test_initial_state_is_all_none() -> None:
    """
    Law 5: StateManager never fabricates data.
    On startup, every field must be None until telemetry confirms it.
    """
    state = StateManager()

    assert state.snapshot.current_system is None
    assert state.snapshot.hull_health is None
    assert state.snapshot.fuel_main is None
    assert state.snapshot.is_docked is None


@pytest.mark.asyncio
async def test_first_update_always_succeeds() -> None:
    """
    Any source can claim an unowned field.
    """
    state = StateManager()

    accepted = state.update_field("current_system", "Sol", TelemetrySource.EDDN)

    assert accepted is True
    assert state.snapshot.current_system == "Sol"


@pytest.mark.asyncio
async def test_journal_outranks_capi() -> None:
    """
    Law 7: journal is the highest-priority source.
    A CAPI update cannot override an existing journal value.
    """
    state = StateManager()

    state.update_field("current_ship_type", "Anaconda", TelemetrySource.JOURNAL)
    accepted = state.update_field("current_ship_type", "Cutter", TelemetrySource.CAPI)

    assert accepted is False
    assert state.snapshot.current_ship_type == "Anaconda"


@pytest.mark.asyncio
async def test_higher_priority_overrides_lower() -> None:
    """
    A journal update should win over an existing EDDN value.
    """
    state = StateManager()

    state.update_field("current_system", "Eranin", TelemetrySource.EDDN)
    accepted = state.update_field("current_system", "Sol", TelemetrySource.JOURNAL)

    assert accepted is True
    assert state.snapshot.current_system == "Sol"


@pytest.mark.asyncio
async def test_equal_priority_overrides() -> None:
    """
    Two updates from the same source — newer data replaces older.
    """
    state = StateManager()

    state.update_field("fuel_main", 20.0, TelemetrySource.STATUS_JSON)
    accepted = state.update_field("fuel_main", 18.5, TelemetrySource.STATUS_JSON)

    assert accepted is True
    assert state.snapshot.fuel_main == 18.5


@pytest.mark.asyncio
async def test_unknown_field_rejected() -> None:
    """
    Attempting to set a field not in SessionState must fail safely.
    """
    state = StateManager()

    accepted = state.update_field("nonexistent_field", "value", TelemetrySource.JOURNAL)

    assert accepted is False


@pytest.mark.asyncio
async def test_private_field_rejected() -> None:
    """
    Internal fields (prefixed with _) must not be writable via update_field.
    """
    state = StateManager()

    accepted = state.update_field("_field_sources", {}, TelemetrySource.JOURNAL)

    assert accepted is False


@pytest.mark.asyncio
async def test_reset_clears_state() -> None:
    """
    reset() must return state to initial (all None).
    """
    state = StateManager()
    state.update_field("current_system", "Sol", TelemetrySource.JOURNAL)
    state.update_field("hull_health", 1.0, TelemetrySource.JOURNAL)

    state.reset()

    assert state.snapshot.current_system is None
    assert state.snapshot.hull_health is None


@pytest.mark.asyncio
async def test_get_field_source_returns_audit_trail() -> None:
    """
    Explainability: we must be able to trace which source set a field.
    """
    state = StateManager()
    state.update_field(
        "current_system",
        "Sol",
        TelemetrySource.JOURNAL,
        timestamp="2026-04-18T10:00:00Z",
    )

    source = state.get_field_source("current_system")

    assert source is not None
    assert source.source == TelemetrySource.JOURNAL
    assert source.timestamp == "2026-04-18T10:00:00Z"


@pytest.mark.asyncio
async def test_inferred_never_overrides_journal() -> None:
    """
    Law 5 + Law 7: inferred state is the lowest-priority source.
    It can never override real telemetry.
    """
    state = StateManager()
    state.update_field("hull_health", 0.85, TelemetrySource.JOURNAL)

    accepted = state.update_field("hull_health", 0.50, TelemetrySource.INFERRED)

    assert accepted is False
    assert state.snapshot.hull_health == 0.85
