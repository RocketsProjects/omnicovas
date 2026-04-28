"""
tests.test_week13_endpoints

Phase 3 Week 13 endpoint tests: onboarding, privacy, settings, confirmations.

Tests Law 1 (Confirmation Gate), Law 8 (Sovereignty & Transparency), and
Principle 7 (Privacy-by-Default).

See: Phase 3 Development Guide Week 13
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from omnicovas.config.vault import ConfigVault
from omnicovas.core.api_bridge import ApiBridge
from omnicovas.core.state_manager import StateManager


@pytest.fixture
def temp_vault(tmp_path: Path) -> ConfigVault:
    """Create a temporary config vault for testing."""
    vault_path = tmp_path / "test.vault"
    return ConfigVault(vault_path=vault_path)


@pytest.fixture
def state_manager() -> StateManager:
    """Create a test StateManager."""
    return StateManager()


@pytest.fixture
def api_bridge(state_manager: StateManager, temp_vault: ConfigVault) -> ApiBridge:
    """Create a test ApiBridge with injected vault."""
    bridge = ApiBridge(state_manager, config_vault=temp_vault)
    return bridge


@pytest.fixture
def client(api_bridge: ApiBridge) -> TestClient:
    """Create a test client."""
    return TestClient(api_bridge._app)


# ============================================================================
# ONBOARDING ENDPOINTS
# ============================================================================


class TestOnboardingEndpoints:
    """Test first-run onboarding flow."""

    def test_onboarding_status_first_run(self, client: TestClient) -> None:
        """First launch should show wizard."""
        res = client.get("/week13/onboarding/status")
        assert res.status_code == 200
        data = res.json()
        assert data["should_show_wizard"] is True
        assert data["completed_at"] is None

    def test_complete_onboarding(self, client: TestClient) -> None:
        """Marking first-run complete should set flag."""
        res = client.post("/week13/onboarding/complete")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

        # Verify flag is set
        res2 = client.get("/week13/onboarding/status")
        assert res2.status_code == 200
        data = res2.json()
        assert data["should_show_wizard"] is False
        assert data["completed_at"] is not None

    def test_onboarding_idempotent(self, client: TestClient) -> None:
        """Calling complete twice should be safe."""
        res1 = client.post("/week13/onboarding/complete")
        assert res1.status_code == 200

        res2 = client.post("/week13/onboarding/complete")
        assert res2.status_code == 200

        # Should still be marked complete
        res3 = client.get("/week13/onboarding/status")
        assert res3.json()["should_show_wizard"] is False


# ============================================================================
# PRIVACY ENDPOINTS
# ============================================================================


class TestPrivacyEndpoints:
    """Test privacy toggles and data management (Law 8, Principle 7)."""

    def test_privacy_toggles_default_off(self, client: TestClient) -> None:
        """All privacy toggles must default OFF (Principle 7)."""
        res = client.get("/week13/privacy/toggles")
        assert res.status_code == 200
        data = res.json()

        # All toggles present
        assert "eddn_submission" in data
        assert "edsm_tracking" in data
        assert "squadron_telemetry" in data
        assert "ai_provider_calls" in data
        assert "crash_reports" in data
        assert "usage_analytics" in data

        # All disabled by default
        for key, info in data.items():
            assert info["enabled"] is False, f"{key} should default OFF"
            assert info["description"], f"{key} should have description"

    def test_set_privacy_toggle(self, client: TestClient) -> None:
        """Setting a toggle should persist."""
        res = client.post(
            "/week13/privacy/toggles/eddn_submission",
            json={"enabled": True},
        )
        assert res.status_code == 200

        # Verify it's set
        res2 = client.get("/week13/privacy/toggles")
        data = res2.json()
        assert data["eddn_submission"]["enabled"] is True

    def test_set_privacy_toggle_off(self, client: TestClient) -> None:
        """Disabling a toggle should work."""
        # Enable first
        client.post("/week13/privacy/toggles/edsm_tracking", json={"enabled": True})

        # Disable
        res = client.post(
            "/week13/privacy/toggles/edsm_tracking",
            json={"enabled": False},
        )
        assert res.status_code == 200

        # Verify disabled
        res2 = client.get("/week13/privacy/toggles")
        assert res2.json()["edsm_tracking"]["enabled"] is False

    def test_privacy_toggle_invalid_key(self, client: TestClient) -> None:
        """Invalid toggle key should fail."""
        res = client.post(
            "/week13/privacy/toggles/invalid_key",
            json={"enabled": True},
        )
        assert res.status_code == 400

    def test_export_privacy_data(self, client: TestClient) -> None:
        """Exporting data should return structured JSON."""
        res = client.post("/week13/privacy/export")
        assert res.status_code == 200
        data = res.json()

        assert "config" in data
        assert "kb_entries" in data
        assert "activity_log_entries" in data
        assert "exported_at" in data

        # exported_at should be ISO 8601
        assert data["exported_at"].endswith("Z")

    def test_delete_all_data(self, client: TestClient) -> None:
        """Deleting data should wipe vault (destructive operation)."""
        # Set some data first
        client.post("/week13/privacy/toggles/eddn_submission", json={"enabled": True})

        # Delete all
        res = client.post("/week13/privacy/delete")
        assert res.status_code == 200

        # Verify toggles reset
        res2 = client.get("/week13/privacy/toggles")
        data = res2.json()
        for info in data.values():
            assert info["enabled"] is False


# ============================================================================
# SETTINGS ENDPOINTS
# ============================================================================


class TestSettingsEndpoints:
    """Test three-tier settings customization."""

    def test_get_settings_defaults(self, client: TestClient) -> None:
        """Getting settings should return defaults."""
        res = client.get("/week13/settings")
        assert res.status_code == 200
        data = res.json()

        assert data["preset"] == "casual"
        assert data["ai_provider"] == "null"
        assert data["overlay"]["opacity"] == 0.95
        assert data["overlay"]["anchor"] == "center"
        assert "pillar_categories" in data

    def test_save_preset(self, client: TestClient) -> None:
        """Saving a preset should persist."""
        res = client.post(
            "/week13/settings",
            json={"preset": "combat"},
        )
        assert res.status_code == 200

        # Verify saved
        res2 = client.get("/week13/settings")
        assert res2.json()["preset"] == "combat"

    def test_save_ai_provider(self, client: TestClient) -> None:
        """Saving AI provider should persist."""
        res = client.post(
            "/week13/settings",
            json={"ai_provider": "gemini"},
        )
        assert res.status_code == 200

        res2 = client.get("/week13/settings")
        assert res2.json()["ai_provider"] == "gemini"

    def test_save_overlay_settings(self, client: TestClient) -> None:
        """Saving overlay settings should persist."""
        res = client.post(
            "/week13/settings",
            json={"overlay": {"opacity": 0.75, "anchor": "top-left"}},
        )
        assert res.status_code == 200

        res2 = client.get("/week13/settings")
        data = res2.json()
        assert data["overlay"]["opacity"] == 0.75
        assert data["overlay"]["anchor"] == "top-left"

    def test_reset_settings(self, client: TestClient) -> None:
        """Resetting should clear all settings."""
        # Set some data
        client.post("/week13/settings", json={"preset": "explorer"})

        # Reset
        res = client.post("/week13/settings/reset")
        assert res.status_code == 200

        # Verify reset
        res2 = client.get("/week13/settings")
        data = res2.json()
        assert data["preset"] == "casual"

    def test_export_settings(self, client: TestClient) -> None:
        """Exporting settings should return JSON."""
        client.post("/week13/settings", json={"preset": "miner"})

        res = client.post("/week13/settings/export")
        assert res.status_code == 200
        data = res.json()
        assert "settings" in data

    def test_import_settings(self, client: TestClient) -> None:
        """Importing settings should apply them."""
        settings_to_import = {
            "settings": {
                "settings_preset": "trader",
                "settings_ai_provider": "local_llm",
            }
        }

        res = client.post("/week13/settings/import", json=settings_to_import)
        assert res.status_code == 200

        # Verify imported
        res2 = client.get("/week13/settings")
        data = res2.json()
        assert data["preset"] == "trader"
        assert data["ai_provider"] == "local_llm"


# ============================================================================
# CONFIRMATION GATE ENDPOINTS
# ============================================================================


class TestConfirmationGateEndpoints:
    """Test Law 1: Confirmation Gate framework."""

    def test_get_pending_confirmations_empty(self, client: TestClient) -> None:
        """Getting pending when none exist should return empty list."""
        res = client.get("/week13/confirmations/pending")
        assert res.status_code == 200
        data = res.json()
        assert data["confirmations"] == []

    def test_respond_to_confirmation_confirm(self, client: TestClient) -> None:
        """Responding with 'confirm' should work."""
        # In Phase 3, there are no real advisories to respond to
        # This test verifies the endpoint signature
        res = client.post(
            "/week13/confirmations/nonexistent",
            json={"response": "confirm"},
        )
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

    def test_respond_to_confirmation_decline(self, client: TestClient) -> None:
        """Responding with 'decline' should work."""
        res = client.post(
            "/week13/confirmations/nonexistent",
            json={"response": "decline"},
        )
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

    def test_respond_with_invalid_response(self, client: TestClient) -> None:
        """Invalid response value should fail."""
        res = client.post(
            "/week13/confirmations/test",
            json={"response": "invalid"},
        )
        assert res.status_code == 400


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


class TestWeek13Integration:
    """Integration tests across Week 13 endpoints."""

    def test_full_onboarding_flow(self, client: TestClient) -> None:
        """Test complete first-run experience."""
        # 1. Check wizard should show
        res = client.get("/week13/onboarding/status")
        assert res.json()["should_show_wizard"] is True

        # 2. Adjust privacy settings
        client.post(
            "/week13/privacy/toggles/ai_provider_calls",
            json={"enabled": True},
        )

        # 3. Save settings preset
        client.post("/week13/settings", json={"preset": "combat"})

        # 4. Complete onboarding
        res = client.post("/week13/onboarding/complete")
        assert res.status_code == 200

        # 5. Verify settings persisted
        settings = client.get("/week13/settings").json()
        assert settings["preset"] == "combat"

        privacy = client.get("/week13/privacy/toggles").json()
        assert privacy["ai_provider_calls"]["enabled"] is True

        # 6. Verify wizard won't show again
        status = client.get("/week13/onboarding/status").json()
        assert status["should_show_wizard"] is False

    def test_privacy_by_default_enforced(self, client: TestClient) -> None:
        """Verify privacy toggles NEVER default ON (Principle 7, Law 8)."""
        # Load 5 times and verify consistency
        for _ in range(5):
            res = client.get("/week13/privacy/toggles")
            for key, info in res.json().items():
                assert info["enabled"] is False, f"{key} violated privacy-by-default"

    def test_settings_roundtrip(self, client: TestClient) -> None:
        """Test export → import roundtrip."""
        # Set initial state
        client.post("/week13/settings", json={"preset": "explorer"})
        client.post("/week13/settings", json={"ai_provider": "local_llm"})

        # Export
        export = client.post("/week13/settings/export").json()

        # Reset
        client.post("/week13/settings/reset")

        # Import
        client.post("/week13/settings/import", json=export)

        # Verify state restored
        settings = client.get("/week13/settings").json()
        assert settings["preset"] == "explorer"
        assert settings["ai_provider"] == "local_llm"
