"""
tests.test_api_pillar1

Tests for Phase 3 Pillar 1 HTTP endpoints (omnicovas/api/pillar1.py).

Each endpoint is tested for:
    - 200 happy path with a seeded StateManager
    - Correct shape (all required keys present)
    - Correct values from known state
    - Null/empty state (no crash, correct null returns)

Law 5 (Zero Hallucination): None fields must come back as null, not fabricated.
Law 8 (Sovereignty & Transparency): every endpoint is read-only and local-only.

See: Phase 3 Development Guide Week 11, Part B
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from omnicovas.api import pillar1 as pillar1_module
from omnicovas.core.state_manager import ModuleInfo, StateManager, TelemetrySource

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_app(state: StateManager) -> TestClient:
    """Build a minimal FastAPI app with the pillar1 router mounted."""
    from fastapi import FastAPI

    pillar1_module.set_state_manager(state)
    app = FastAPI()
    app.include_router(pillar1_module.router)
    return TestClient(app)


def seed_state(state: StateManager) -> None:
    """Populate a StateManager with known test values."""
    ts = "2026-04-28T12:00:00Z"
    src = TelemetrySource.JOURNAL

    state.update_field("current_ship_type", "Federation_Corvette", src, ts)
    state.update_field("current_ship_name", "ISS Caspian", src, ts)
    state.update_field("current_ship_ident", "CAS-01", src, ts)
    state.update_field("hull_health", 0.85, src, ts)
    state.update_field("shield_up", True, src, ts)
    state.update_field("shield_strength_pct", 92.5, src, ts)
    state.update_field("fuel_main", 16.0, src, ts)
    state.update_field("fuel_capacity_main", 32.0, src, ts)
    state.update_field("jump_range_ly", 14.72, src, ts)
    state.update_field("cargo_count", 48, src, ts)
    state.update_field("cargo_capacity", 96, src, ts)
    state.update_field("cargo_inventory", {"Gold": 32, "Palladium": 16}, src, ts)
    state.update_field("heat_level", 0.45, src, ts)
    state.update_field("sys_pips", 4, TelemetrySource.STATUS_JSON, ts)
    state.update_field("eng_pips", 2, TelemetrySource.STATUS_JSON, ts)
    state.update_field("wep_pips", 2, TelemetrySource.STATUS_JSON, ts)
    state.update_field("hull_value", 40_000_000, src, ts)
    state.update_field("modules_value", 200_000_000, src, ts)
    state.update_field("is_docked", False, src, ts)
    state.update_field("current_system", "Shinrarta Dezhra", src, ts)
    state.update_field("is_wanted_in_system", False, src, ts)

    mods = {
        "Armour": ModuleInfo(
            slot="Armour",
            item="Federation_Corvette_Armour_Grade3",
            item_localised="Military Grade Composite",
            health=1.0,
            power=None,
            priority=None,
            on=True,
            engineering=None,
        ),
        "PowerPlant": ModuleInfo(
            slot="PowerPlant",
            item="Int_PowerPlant_Size8_Class5",
            item_localised="8E Power Plant",
            health=0.72,
            power=0.0,
            priority=1,
            on=True,
            engineering=None,
        ),
        "Thrusters": ModuleInfo(
            slot="Thrusters",
            item="Int_Engine_Size7_Class5",
            item_localised="7A Thrusters",
            health=0.15,
            power=6.0,
            priority=0,
            on=True,
            engineering=None,
        ),
    }
    state.update_field("modules", mods, src, ts)
    state.update_field("loadout_hash", "abc123deadbeef", src, ts)


# ---------------------------------------------------------------------------
# /pillar1/ship-state
# ---------------------------------------------------------------------------


class TestShipState:
    def test_happy_path_shape(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        r = client.get("/pillar1/ship-state")
        assert r.status_code == 200
        data = r.json()

        required_keys = [
            "ship_type",
            "ship_name",
            "ship_ident",
            "hull_health",
            "shield_up",
            "shield_strength_pct",
            "fuel_main",
            "fuel_capacity",
            "fuel_pct",
            "jump_range_ly",
            "cargo_count",
            "cargo_capacity",
            "heat_level",
            "sys_pips",
            "eng_pips",
            "wep_pips",
            "is_docked",
            "current_system",
            "current_station",
            "is_wanted_in_system",
        ]
        for key in required_keys:
            assert key in data, f"Missing key: {key}"

    def test_happy_path_values(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        data = client.get("/pillar1/ship-state").json()

        assert data["ship_type"] == "Federation_Corvette"
        assert data["ship_name"] == "ISS Caspian"
        assert data["ship_ident"] == "CAS-01"
        assert data["hull_health"] == pytest.approx(85.0, abs=0.1)
        assert data["shield_up"] is True
        assert data["shield_strength_pct"] == pytest.approx(92.5, abs=0.1)
        assert data["fuel_pct"] == pytest.approx(50.0, abs=0.1)
        assert data["jump_range_ly"] == pytest.approx(14.72, abs=0.01)
        assert data["cargo_count"] == 48
        assert data["sys_pips"] == 4
        assert data["is_docked"] is False
        assert data["current_system"] == "Shinrarta Dezhra"

    def test_empty_state_returns_nulls(self) -> None:
        state = StateManager()
        client = make_app(state)

        data = client.get("/pillar1/ship-state").json()

        assert data["ship_type"] is None
        assert data["hull_health"] is None
        assert data["fuel_pct"] is None
        # is_docked is None on empty state (Law 5 — not fabricated as False)
        assert data["is_docked"] is None
        assert data["is_wanted_in_system"] is False

    def test_fuel_pct_null_when_capacity_zero(self) -> None:
        state = StateManager()
        ts = "2026-04-28T12:00:00Z"
        state.update_field("fuel_main", 10.0, TelemetrySource.JOURNAL, ts)
        state.update_field("fuel_capacity_main", 0.0, TelemetrySource.JOURNAL, ts)
        client = make_app(state)

        data = client.get("/pillar1/ship-state").json()
        assert data["fuel_pct"] is None


# ---------------------------------------------------------------------------
# /pillar1/loadout
# ---------------------------------------------------------------------------


class TestLoadout:
    def test_shape(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        data = client.get("/pillar1/loadout").json()

        assert "ship_type" in data
        assert "loadout_hash" in data
        assert "modules" in data
        assert isinstance(data["modules"], list)

    def test_module_fields(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        data = client.get("/pillar1/loadout").json()
        mods = {m["slot"]: m for m in data["modules"]}

        assert "Armour" in mods
        armour = mods["Armour"]
        assert armour["item"] == "Federation_Corvette_Armour_Grade3"
        assert armour["health_pct"] == pytest.approx(100.0, abs=0.1)

        thrusters = mods["Thrusters"]
        assert thrusters["health_pct"] == pytest.approx(15.0, abs=0.1)

    def test_empty_state(self) -> None:
        state = StateManager()
        client = make_app(state)

        data = client.get("/pillar1/loadout").json()
        assert data["ship_type"] is None
        assert data["modules"] == []


# ---------------------------------------------------------------------------
# /pillar1/cargo
# ---------------------------------------------------------------------------


class TestCargo:
    def test_shape(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        data = client.get("/pillar1/cargo").json()
        assert "cargo_count" in data
        assert "cargo_capacity" in data
        assert "inventory" in data

    def test_inventory_sorted_descending(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        data = client.get("/pillar1/cargo").json()
        counts = [item["count"] for item in data["inventory"]]
        assert counts == sorted(counts, reverse=True)

    def test_inventory_names(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        data = client.get("/pillar1/cargo").json()
        names = {item["name"] for item in data["inventory"]}
        assert "Gold" in names
        assert "Palladium" in names

    def test_empty_state(self) -> None:
        state = StateManager()
        client = make_app(state)

        data = client.get("/pillar1/cargo").json()
        assert data["cargo_count"] is None
        assert data["inventory"] == []


# ---------------------------------------------------------------------------
# /pillar1/heat
# ---------------------------------------------------------------------------


class TestHeat:
    def test_shape(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        data = client.get("/pillar1/heat").json()
        assert "level" in data
        assert "level_pct" in data
        assert "trend" in data
        assert "samples" in data
        assert "state" in data

    def test_heat_state_normal(self) -> None:
        state = StateManager()
        seed_state(state)  # heat_level = 0.45
        client = make_app(state)

        data = client.get("/pillar1/heat").json()
        assert data["state"] == "normal"
        assert data["level"] == pytest.approx(0.45, abs=0.01)
        assert data["level_pct"] == pytest.approx(45.0, abs=0.1)

    def test_heat_state_warning(self) -> None:
        state = StateManager()
        state.update_field(
            "heat_level",
            0.85,
            TelemetrySource.STATUS_JSON,
            "2026-04-28T12:00:00Z",
        )
        client = make_app(state)

        data = client.get("/pillar1/heat").json()
        assert data["state"] == "warning"

    def test_heat_state_critical(self) -> None:
        state = StateManager()
        state.update_field(
            "heat_level",
            0.97,
            TelemetrySource.STATUS_JSON,
            "2026-04-28T12:00:00Z",
        )
        client = make_app(state)

        data = client.get("/pillar1/heat").json()
        assert data["state"] == "critical"

    def test_heat_state_damage(self) -> None:
        state = StateManager()
        state.update_field(
            "heat_level",
            1.25,
            TelemetrySource.STATUS_JSON,
            "2026-04-28T12:00:00Z",
        )
        client = make_app(state)

        data = client.get("/pillar1/heat").json()
        assert data["state"] == "damage"

    def test_empty_state(self) -> None:
        state = StateManager()
        client = make_app(state)

        data = client.get("/pillar1/heat").json()
        assert data["level"] is None
        assert data["state"] is None
        assert isinstance(data["samples"], list)


# ---------------------------------------------------------------------------
# /pillar1/pips
# ---------------------------------------------------------------------------


class TestPips:
    def test_shape(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        data = client.get("/pillar1/pips").json()
        assert "sys" in data
        assert "eng" in data
        assert "wep" in data

    def test_values(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        data = client.get("/pillar1/pips").json()
        assert data["sys"] == 4
        assert data["eng"] == 2
        assert data["wep"] == 2

    def test_empty_state(self) -> None:
        state = StateManager()
        client = make_app(state)

        data = client.get("/pillar1/pips").json()
        assert data["sys"] is None
        assert data["eng"] is None
        assert data["wep"] is None


# ---------------------------------------------------------------------------
# /pillar1/modules/summary
# ---------------------------------------------------------------------------


class TestModulesSummary:
    def test_shape(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        data = client.get("/pillar1/modules/summary").json()
        assert "total" in data
        assert "ok" in data
        assert "warning" in data
        assert "critical" in data

    def test_counts(self) -> None:
        state = StateManager()
        seed_state(state)
        client = make_app(state)

        # Seeded: Armour=1.0 (ok), PowerPlant=0.72 (warning), Thrusters=0.15 (critical)
        data = client.get("/pillar1/modules/summary").json()
        assert data["ok"] == 1
        assert data["warning"] == 1
        assert data["critical"] == 1
        assert data["total"] == 3

    def test_empty_state(self) -> None:
        state = StateManager()
        client = make_app(state)

        data = client.get("/pillar1/modules/summary").json()
        assert data["total"] == 0
        assert data["ok"] == 0
        assert data["warning"] == 0
        assert data["critical"] == 0
