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

See: Master Blueprint v4.1 Section 2 (Data Pipeline)
See: Phase 2 Development Guide Week 7, Part B
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
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
class ModuleInfo:
    """
    State of a single ship module, populated from the Loadout journal event.

    Health is 0.0-1.0 (matching the journal field directly -- do NOT convert
    to percent). power and priority are None for modules that lack those
    fields in the Loadout payload (e.g. Fighter Hangar bays).

    The engineering field carries the raw Engineering block from the journal
    verbatim. Phase 2 does not parse engineer effects -- that is Pillar 6
    work in Phase 8. We preserve the raw block so Phase 8 has it available.

    See: Phase 2 Development Guide Week 8, Part A (Loadout Awareness)
    """

    slot: str
    item: str
    item_localised: str | None
    # 0.0 (destroyed) -> 1.0 (intact). Matches journal Module.Health directly.
    health: float
    power: float | None
    priority: int | None
    on: bool
    # Raw engineering block from journal -- parsed in Phase 8 (Pillar 6).
    # None when module has no engineering modifications.
    engineering: dict[str, Any] | None


@dataclass
class SessionState:
    """
    The current state of the commander's session.

    All fields default to None -- unknown until telemetry confirms them.
    Law 5 forbids filling gaps with assumptions.

    Phase 2 additions are grouped by feature so future readers can see which
    feature owns which fields. All new fields are nullable (None = unknown).
    """

    # --- Phase 1 fields (unchanged) -----------------------------------------

    current_system: str | None = None
    current_station: str | None = None

    # Tri-state: None = unknown (not yet confirmed by telemetry), True = docked,
    # False = not docked. None is correct on startup per Law 5 -- do not default
    # to False, which would fabricate knowledge we don't have yet.
    is_docked: bool | None = None
    is_in_supercruise: bool | None = None

    # 0.0 (destroyed) -> 1.0 (full health). Matches the journal HullDamage.Health
    # field exactly -- do NOT convert to percent on ingest. KB threshold entries
    # use the same 0.0-1.0 scale (e.g. hull_critical_threshold = 0.10, not 10.0).
    hull_health: float | None = None

    shield_up: bool | None = None
    fuel_main: float | None = None
    # fuel_capacity_main: total fuel capacity in main tank (tons)
    # fuel_capacity_reserve: total fuel capacity in reservoir tank (tons)
    fuel_capacity_main: float | None = None
    fuel_capacity_reserve: float | None = None
    cargo_count: int | None = None
    cargo_capacity: int | None = None
    target_cmdr: str | None = None
    target_ship: str | None = None
    commander_name: str | None = None

    # --- Phase 2 -- Ship Identity (Feature 1: Live Ship State) ---------------
    # Populated from LoadGame, Loadout, and ShipyardSwap journal events.

    # internal type string e.g. "Python", "SideWinder"
    current_ship_type: str | None = None
    # numeric ID assigned by the game to distinguish multiple ships of the
    # same type in the commander's fleet
    current_ship_id: int | None = None
    # pilot-assigned call sign e.g. "QE-01"
    current_ship_ident: str | None = None
    # pilot-assigned name e.g. "HMCS Bonaventure"
    current_ship_name: str | None = None

    # --- Phase 2 -- Hull & Shield additions (Features 1, 3, 7) --------------

    # 0.0-100.0. Populated from Status.json when available. Distinct from
    # shield_up (boolean). None until first Status read.
    shield_strength_pct: float | None = None

    # --- Phase 2 -- Fuel & Jump Range (Feature 5) ---------------------------
    # fuel_reservoir: the small supplemental tank that feeds the main tank.
    # Sourced from Status.json Fuel.FuelReservoir. Units: tons.
    fuel_reservoir: float | None = None
    # jump_range_ly: maximum jump range at current load.
    # Sourced from Loadout.MaxJumpRange -- NOT recomputed from physics.
    # Phase 5 (Exploration pillar) owns first-principles jump math.
    jump_range_ly: float | None = None

    # --- Phase 2 -- Cargo (Feature 6) ---------------------------------------
    # commodity internal name -> unit count.
    # Populated from Cargo.json, not from Loadout.
    # SRV cargo is excluded -- Phase 2 tracks Ship cargo only.
    cargo_inventory: dict[str, int] = field(default_factory=dict)

    # --- Phase 2 -- Loadout & Modules (Features 2, 4) -----------------------
    # slot name -> ModuleInfo. Ground truth from Loadout event.
    # Delta updates arrive from ModuleInfo.json during combat (Week 8).
    modules: dict[str, ModuleInfo] = field(default_factory=dict)
    # SHA-256 of the sorted Modules array.
    # Used to detect genuine loadout changes vs cosmetic re-fires of Loadout.
    loadout_hash: str | None = None

    # omnicovas/core/state_manager.py
    # Phase 2 -- Extended Events (Feature 8) --------------------------------
    # True when commander has a bounty or crime in the current system.
    # Cleared automatically on FSDJump to a different system.
    is_wanted_in_system: bool = False

    # --- Phase 2 -- Power Distribution (Feature 9) --------------------------
    # Pip values are on a 0-8 scale where total always equals 12 when in a
    # flyable ship. Status.json reports them as a [SYS, ENG, WEP] list.
    # All three are None when on-foot (Odyssey) or before first Status read.
    sys_pips: int | None = None
    eng_pips: int | None = None
    wep_pips: int | None = None

    # --- Phase 2 -- Heat (Feature 10) ---------------------------------------
    # 0.0-1.0 from Status.json Heat field. NOT a percentage.
    # 1.0 = 100% heat (damage threshold). Values above 1.0 are possible
    # during fuel scoop overheat. None until first Status read.
    heat_level: float | None = None

    # --- Internal audit (NOT public) ----------------------------------------
    _field_sources: dict[str, FieldSource] = field(default_factory=dict)


class StateManager:
    """
    Manages the live in-memory session state.

    Provides update methods that enforce Law 7 (source priority).
    Updates from lower-priority sources are rejected if a higher-priority
    source has already set that field.

    Source priority is automatically enforced for all SessionState fields via
    update_field(). The Phase 1 implementation covers every field -- Phase 2
    fields inherit this for free without any additional wiring.

    Usage:
        state = StateManager()
        state.update_field("current_system", "Sol", TelemetrySource.JOURNAL)
        state.update_field("fuel_main", 16.0, TelemetrySource.STATUS_JSON)
        print(state.snapshot.current_system)

    See: Phase 2 Development Guide Week 7, Part B
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
        Reset all state to initial (all None / empty dicts).
        Use only at session boundaries or for tests.
        """
        self._state = SessionState()
        logger.info("StateManager reset.")

    def get_field_source(self, field_name: str) -> FieldSource | None:
        """
        Return the source metadata for a field, for audit/explainability.
        """
        return self._state._field_sources.get(field_name)

    def public_snapshot(self) -> dict[str, Any]:
        """
        Return session state as a plain dict with all private fields stripped.

        Safe to serialise and send to the UI or API clients. Use this
        everywhere state is serialised -- never call asdict() directly on the
        snapshot and then pop() private fields at each call site.

        Law 8 (Sovereignty & Transparency): state is inspectable by the
        commander, but internal audit metadata (_field_sources) is an
        implementation detail that must not appear in the public API surface.

        Returns:
            Dict of all public SessionState fields. Keys starting with '_'
            are excluded regardless of what future internal fields are added.
        """
        return {k: v for k, v in asdict(self._state).items() if not k.startswith("_")}
