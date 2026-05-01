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

from omnicovas.core.state_manager import (
    ModuleInfo,
    SessionState,
    StateManager,
    TelemetrySource,
)


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


def test_public_snapshot_excludes_private_fields() -> None:
    """
    public_snapshot() must not expose _field_sources or any other
    private internal field. Law 8: inspectable but not leaking internals.
    """
    state = StateManager()
    state.update_field("current_system", "Sol", TelemetrySource.JOURNAL)

    snapshot = state.public_snapshot()

    # Public field is present
    assert snapshot["current_system"] == "Sol"

    # No private fields leak through
    private_keys = [k for k in snapshot if k.startswith("_")]
    assert private_keys == [], f"Private fields leaked: {private_keys}"

    # Result is a plain dict (safe to JSON-serialise)
    assert isinstance(snapshot, dict)


# ---------------------------------------------------------------------------
# ModuleInfo dataclass
# ---------------------------------------------------------------------------


def test_module_info_can_be_constructed() -> None:
    """ModuleInfo must accept all documented fields."""
    mod = ModuleInfo(
        slot="MediumHardpoint1",
        item="hpt_pulselaser_fixed_medium",
        item_localised="Pulse Laser",
        health=0.95,
        power=0.6,
        priority=1,
        on=True,
        engineering=None,
    )
    assert mod.slot == "MediumHardpoint1"
    assert mod.health == 0.95
    assert mod.engineering is None


def test_module_info_accepts_engineering_block() -> None:
    """ModuleInfo engineering field must accept a raw dict."""
    eng = {"BlueprintName": "Weapon_LongRange", "Level": 5, "Quality": 1.0}
    mod = ModuleInfo(
        slot="MediumHardpoint1",
        item="hpt_pulselaser_fixed_medium",
        item_localised=None,
        health=1.0,
        power=0.6,
        priority=1,
        on=True,
        engineering=eng,
    )
    assert mod.engineering is not None
    assert mod.engineering["Level"] == 5


def test_module_info_optional_fields_accept_none() -> None:
    """power, priority, item_localised, and engineering can all be None."""
    mod = ModuleInfo(
        slot="Armour",
        item="sidewinder_armour_grade1",
        item_localised=None,
        health=1.0,
        power=None,
        priority=None,
        on=True,
        engineering=None,
    )
    assert mod.power is None
    assert mod.priority is None


@pytest.mark.asyncio
async def test_heat_fields_default_to_none() -> None:
    """Verify that new heat fields default to None."""
    state = StateManager()
    assert state.snapshot.heat_state is None
    assert state.snapshot.heat_last_event_at is None
    assert state.snapshot.heat_suggestion is None


@pytest.mark.asyncio
async def test_fuel_status_overrides_journal() -> None:
    """
    Phase 3.4 Patch: Status.json must be able to update fuel_main and
    fuel_reservoir even if journal previously set them.
    """
    state = StateManager()

    # Initial set by JOURNAL
    state.update_field("fuel_main", 32.0, TelemetrySource.JOURNAL)
    state.update_field("fuel_reservoir", 0.5, TelemetrySource.JOURNAL)

    # Status.json update should succeed now
    accepted_main = state.update_field("fuel_main", 31.8, TelemetrySource.STATUS_JSON)
    accepted_res = state.update_field(
        "fuel_reservoir", 0.4, TelemetrySource.STATUS_JSON
    )

    assert accepted_main is True
    assert accepted_res is True
    assert state.snapshot.fuel_main == 31.8
    assert state.snapshot.fuel_reservoir == 0.4


@pytest.mark.asyncio
async def test_fuel_none_update_rejected() -> None:
    """
    Law 5: Never overwrite known fuel value with None.
    """
    state = StateManager()
    state.update_field("fuel_main", 32.0, TelemetrySource.JOURNAL)

    # Update with None should be rejected
    accepted = state.update_field("fuel_main", None, TelemetrySource.STATUS_JSON)
    assert accepted is False
    assert state.snapshot.fuel_main == 32.0


@pytest.mark.asyncio
async def test_status_cannot_override_other_journal_fields() -> None:
    """
    Ensure the fuel override is narrow and doesn't break Law 7 for other fields.
    """
    state = StateManager()
    state.update_field("current_system", "Sol", TelemetrySource.JOURNAL)

    # Other field should still reject STATUS_JSON
    accepted = state.update_field(
        "current_system", "HIP 2797", TelemetrySource.STATUS_JSON
    )
    assert accepted is False
    assert state.snapshot.current_system == "Sol"


def test_phase2_ship_identity_fields_default_none() -> None:
    """All Phase 2 ship identity fields must start as None (Law 5)."""
    state = SessionState()
    assert state.current_ship_type is None
    assert state.current_ship_id is None
    assert state.current_ship_ident is None
    assert state.current_ship_name is None


def test_phase2_hull_shield_additions_default_none() -> None:
    """shield_strength_pct must default to None."""
    state = SessionState()
    assert state.shield_strength_pct is None


@pytest.mark.asyncio
async def test_status_json_updates_shield_up_after_journal_set() -> None:
    """STATUS_JSON must always update shield_up even after JOURNAL set it.

    hull_triggers sets shield_up=False via JOURNAL on ShieldsDown. The next
    Status.json poll (STATUS_JSON) must be able to restore shield_up=True
    when the shields are back up. Without this pass-through, STATUS_JSON
    would be permanently blocked by the prior JOURNAL write.
    """
    state = StateManager()

    # Simulate journal ShieldsDown setting shield_up=False (JOURNAL priority)
    accepted = state.update_field("shield_up", False, TelemetrySource.JOURNAL)
    assert accepted is True
    assert state.snapshot.shield_up is False

    # Simulate next Status.json poll with shields back up (STATUS_JSON priority)
    accepted = state.update_field("shield_up", True, TelemetrySource.STATUS_JSON)
    assert accepted is True
    assert state.snapshot.shield_up is True


@pytest.mark.asyncio
async def test_status_json_updates_shield_up_false_after_journal_set_true() -> None:
    """STATUS_JSON can set shield_up=False even after JOURNAL set it True."""
    state = StateManager()

    state.update_field("shield_up", True, TelemetrySource.JOURNAL)
    accepted = state.update_field("shield_up", False, TelemetrySource.STATUS_JSON)
    assert accepted is True
    assert state.snapshot.shield_up is False


def test_phase2_fuel_fields_default_none() -> None:
    """fuel_reservoir and jump_range_ly must default to None."""
    state = SessionState()
    assert state.fuel_reservoir is None
    assert state.jump_range_ly is None


def test_phase2_cargo_inventory_defaults_empty() -> None:
    """cargo_inventory must default to an empty dict (not None)."""
    state = SessionState()
    assert state.cargo_inventory == {}
    assert isinstance(state.cargo_inventory, dict)


def test_phase2_modules_defaults_empty() -> None:
    """modules must default to an empty dict (not None)."""
    state = SessionState()
    assert state.modules == {}
    assert isinstance(state.modules, dict)


def test_phase2_loadout_hash_defaults_none() -> None:
    """loadout_hash must default to None."""
    state = SessionState()
    assert state.loadout_hash is None


def test_phase2_pip_fields_default_none() -> None:
    """sys_pips, eng_pips, wep_pips must all default to None."""
    state = SessionState()
    assert state.sys_pips is None
    assert state.eng_pips is None
    assert state.wep_pips is None


def test_phase2_heat_level_defaults_none() -> None:
    """heat_level must default to None."""
    state = SessionState()
    assert state.heat_level is None


# ---------------------------------------------------------------------------
# update_field() works for all new Phase 2 fields
# ---------------------------------------------------------------------------


def test_update_ship_identity_fields() -> None:
    """update_field() must accept all four ship identity fields."""
    state = StateManager()
    state.update_field("current_ship_type", "Python", TelemetrySource.JOURNAL)
    state.update_field("current_ship_id", 42, TelemetrySource.JOURNAL)
    state.update_field("current_ship_ident", "QE-01", TelemetrySource.JOURNAL)
    state.update_field("current_ship_name", "HMCS Bonaventure", TelemetrySource.JOURNAL)

    snap = state.snapshot
    assert snap.current_ship_type == "Python"
    assert snap.current_ship_id == 42
    assert snap.current_ship_ident == "QE-01"
    assert snap.current_ship_name == "HMCS Bonaventure"


def test_update_fuel_phase2_fields() -> None:
    """update_field() must accept fuel_reservoir and jump_range_ly."""
    state = StateManager()
    state.update_field("fuel_reservoir", 0.25, TelemetrySource.STATUS_JSON)
    state.update_field("jump_range_ly", 38.4, TelemetrySource.JOURNAL)

    snap = state.snapshot
    assert snap.fuel_reservoir == 0.25
    assert snap.jump_range_ly == 38.4


def test_update_pip_fields() -> None:
    """update_field() must accept sys_pips, eng_pips, wep_pips."""
    state = StateManager()
    state.update_field("sys_pips", 2, TelemetrySource.STATUS_JSON)
    state.update_field("eng_pips", 4, TelemetrySource.STATUS_JSON)
    state.update_field("wep_pips", 6, TelemetrySource.STATUS_JSON)

    snap = state.snapshot
    assert snap.sys_pips == 2
    assert snap.eng_pips == 4
    assert snap.wep_pips == 6


def test_update_heat_level() -> None:
    """update_field() must accept heat_level as a 0.0-1.0 float."""
    state = StateManager()
    state.update_field("heat_level", 0.72, TelemetrySource.STATUS_JSON)

    assert state.snapshot.heat_level == 0.72


def test_update_loadout_hash() -> None:
    """update_field() must accept loadout_hash."""
    state = StateManager()
    state.update_field(
        "loadout_hash",
        "abc123def456",
        TelemetrySource.JOURNAL,
    )
    assert state.snapshot.loadout_hash == "abc123def456"


# ---------------------------------------------------------------------------
# Source priority applies to new Phase 2 fields
# ---------------------------------------------------------------------------


def test_journal_outranks_status_json_for_ship_type() -> None:
    """Journal must win over status_json for ship identity fields."""
    state = StateManager()
    state.update_field("current_ship_type", "Sidewinder", TelemetrySource.STATUS_JSON)
    accepted = state.update_field(
        "current_ship_type", "Python", TelemetrySource.JOURNAL
    )
    assert accepted is True
    assert state.snapshot.current_ship_type == "Python"


def test_status_json_cannot_override_journal_for_heat() -> None:
    """If journal sets heat_level, status_json cannot override it."""
    state = StateManager()
    state.update_field("heat_level", 0.50, TelemetrySource.JOURNAL)
    accepted = state.update_field("heat_level", 0.90, TelemetrySource.STATUS_JSON)
    assert accepted is False
    assert state.snapshot.heat_level == 0.50


# ---------------------------------------------------------------------------
# reset() clears all Phase 2 fields
# ---------------------------------------------------------------------------


def test_reset_clears_phase2_fields() -> None:
    """reset() must return all Phase 2 fields to their initial defaults."""
    state = StateManager()
    state.update_field("current_ship_type", "Anaconda", TelemetrySource.JOURNAL)
    state.update_field("jump_range_ly", 55.0, TelemetrySource.JOURNAL)
    state.update_field("heat_level", 0.3, TelemetrySource.STATUS_JSON)
    state.update_field("sys_pips", 4, TelemetrySource.STATUS_JSON)

    state.reset()

    snap = state.snapshot
    assert snap.current_ship_type is None
    assert snap.jump_range_ly is None
    assert snap.heat_level is None
    assert snap.sys_pips is None
    assert snap.modules == {}
    assert snap.cargo_inventory == {}


# ---------------------------------------------------------------------------
# public_snapshot() includes Phase 2 fields
# ---------------------------------------------------------------------------


def test_public_snapshot_includes_phase2_fields() -> None:
    """public_snapshot() must expose all new Phase 2 public fields."""
    state = StateManager()
    state.update_field("current_ship_type", "Krait_MkII", TelemetrySource.JOURNAL)
    state.update_field("jump_range_ly", 30.0, TelemetrySource.JOURNAL)

    snap = state.public_snapshot()

    assert "current_ship_type" in snap
    assert snap["current_ship_type"] == "Krait_MkII"
    assert "jump_range_ly" in snap
    assert snap["jump_range_ly"] == 30.0
    assert "heat_level" in snap
    assert "sys_pips" in snap
    assert "modules" in snap
    assert "cargo_inventory" in snap
    # Private fields must still be absent
    assert "_field_sources" not in snap
