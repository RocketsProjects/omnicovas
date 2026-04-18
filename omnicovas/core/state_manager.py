"""
omnicovas.core.state_manager

In-memory current state of the commander's session.

Holds the live truth of "right now": current ship, system, cargo, fuel, etc.
This is NOT a database — it is pure in-memory state for zero-latency reads.
The database (omnicovas.db) persists history; this class holds "now".

Law 7 (Telemetry Rigidity):
    Source priority enforced. When multiple sources report conflicting state,
    the higher-priority source always wins. Local journal is the ultimate truth.

    Priority order (lowest number = highest priority):
        1. journal       — local, authoritative game events
        2. status_json   — local, live hardware/UI state
        3. capi          — remote, Frontier API
        4. eddn          — remote, crowdsourced
        5. inferred      — OmniCOVAS-derived, never overrides real telemetry

Law 5 (Zero Hallucination Doctrine):
    StateManager NEVER fabricates data to fill gaps.
    Missing fields stay missing (None) until real telemetry arrives.

See: Master Blueprint v4.0 Section 2 (Data Pipeline)
See: Phase 1 Development Guide Week 3, Part A
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any

logger = logging.getLogger(__name__)


class TelemetrySource(IntEnum):
    """
    Source priority for state updates.

    Lower value = higher priority. A lower-numbered source always
    wins a conflict against a higher-numbered source.
    """

    JOURNAL = 1
    STATUS_JSON = 2
    CAPI = 3
    EDDN = 4
    INFERRED = 5


@dataclass
class FieldSource:
    """
    Records which source last set a given field, for conflict resolution.
    """

    source: TelemetrySource
    timestamp: str | None = None


@dataclass
class SessionState:
    """
    The current state of the commander's session.

    All fields default to None — unknown until telemetry confirms them.
    Law 5 forbids filling gaps with assumptions.
    """

    current_system: str | None = None
    current_station: str | None = None
    current_ship_type: str | None = None
    current_ship_name: str | None = None
    hull_health: float | None = None
    shield_up: bool | None = None
    fuel_main: float | None = None
    fuel_capacity: float | None = None
    cargo_count: int | None = None
    cargo_capacity: int | None = None
    is_docked: bool | None = None
    is_in_supercruise: bool | None = None
    target_cmdr: str | None = None
    target_ship: str | None = None
    commander_name: str | None = None

    _field_sources: dict[str, FieldSource] = field(default_factory=dict)


class StateManager:
    """
    Manages the live in-memory session state.

    Provides update methods that enforce Law 7 (source priority).
    Updates from lower-priority sources are rejected if a higher-priority
    source has already set that field.

    Usage:
        state = StateManager()
        state.update_field("current_system", "Sol", TelemetrySource.JOURNAL)
        state.update_field("fuel_main", 16.0, TelemetrySource.STATUS_JSON)
        print(state.snapshot.current_system)

    See: Phase 1 Development Guide Week 3, Part A
    """

    def __init__(self) -> None:
        self._state = SessionState()

    @property
    def snapshot(self) -> SessionState:
        """
        Read-only snapshot of current state.
        All mutations must go through update_field() to respect source priority.
        """
        return self._state

    def update_field(
        self,
        field_name: str,
        value: Any,
        source: TelemetrySource,
        timestamp: str | None = None,
    ) -> bool:
        """
        Update a single state field, respecting source priority.

        Args:
            field_name: Name of the SessionState field to update
            value: New value to set
            source: Which telemetry source produced this value
            timestamp: Optional journal timestamp for audit

        Returns:
            True if the update was accepted. False if rejected due to
            a higher-priority source already owning this field.
        """
        if not hasattr(self._state, field_name) or field_name.startswith("_"):
            logger.warning("Rejected update to unknown field: %s", field_name)
            return False

        existing = self._state._field_sources.get(field_name)

        if existing is not None and existing.source < source:
            logger.debug(
                "Rejected %s update to %r: existing source %s outranks %s",
                field_name,
                value,
                existing.source.name,
                source.name,
            )
            return False

        setattr(self._state, field_name, value)
        self._state._field_sources[field_name] = FieldSource(
            source=source, timestamp=timestamp
        )
        logger.debug(
            "Updated %s = %r (source: %s)",
            field_name,
            value,
            source.name,
        )
        return True

    def reset(self) -> None:
        """
        Reset all state to initial (all None).
        Use only at session boundaries or for tests.
        """
        self._state = SessionState()
        logger.info("StateManager reset.")

    def get_field_source(self, field_name: str) -> FieldSource | None:
        """
        Return the source metadata for a field, for audit/explainability.
        """
        return self._state._field_sources.get(field_name)
