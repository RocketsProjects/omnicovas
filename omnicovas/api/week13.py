"""
omnicovas.api.week13

Phase 3 Week 13 endpoints: onboarding, privacy, settings, confirmations.

Onboarding:
  - GET /onboarding/status — check if first-run wizard should fire
  - POST /onboarding/complete — mark first-run as complete

Privacy:
  - GET /privacy/toggles — get all privacy toggle state
  - POST /privacy/toggles/{key} — set a privacy toggle
  - POST /privacy/export — export commander data as JSON
  - POST /privacy/delete — wipe all local data

Settings:
  - GET /settings — get full settings config
  - POST /settings — save full settings config
  - POST /settings/reset — reset to defaults

Confirmations (Law 1 — Confirmation Gate):
  - GET /confirmations/pending — get queued advisories
  - POST /confirmations/{id} — respond to an advisory

Law 8 (Sovereignty & Transparency): every setting is auditable.
Privacy toggles default OFF; no exceptions.

See: Phase 3 Development Guide Week 13
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from omnicovas.config.vault import ConfigVault

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/week13", tags=["week13"])

_vault: ConfigVault | None = None


def set_config_vault(vault: ConfigVault) -> None:
    """Inject the ConfigVault instance."""
    global _vault  # noqa: PLW0603
    _vault = vault


def _ensure_vault() -> ConfigVault:
    """Raise if vault is not yet injected."""
    if _vault is None:
        raise HTTPException(
            status_code=500,
            detail="ConfigVault not yet initialized",
        )
    return _vault


@router.get("/onboarding/status")  # type: ignore[untyped-decorator]
async def get_onboarding_status() -> dict[str, Any]:
    """Check if first-run wizard should display."""
    vault = _ensure_vault()

    completed_str = vault.get("first_run_completed")
    should_show = completed_str != "true"

    timestamp = None
    if not should_show:
        try:
            ts_str = vault.get("first_run_completed_at")
            if ts_str:
                timestamp = ts_str
        except Exception:
            pass

    return {
        "should_show_wizard": should_show,
        "completed_at": timestamp,
    }


@router.post("/onboarding/complete")  # type: ignore[untyped-decorator]
async def complete_onboarding(
    body: dict[str, Any] | None = None,
) -> dict[str, str]:
    """Mark first-run wizard as complete."""
    vault = _ensure_vault()
    vault.set("first_run_completed", "true")
    vault.set("first_run_completed_at", datetime.utcnow().isoformat() + "Z")
    logger.info("first_run_completed")
    return {"status": "ok"}


PRIVACY_TOGGLES = frozenset(
    {
        "eddn_submission",
        "edsm_tracking",
        "squadron_telemetry",
        "ai_provider_calls",
        "crash_reports",
        "usage_analytics",
    }
)

PRIVACY_DESCRIPTIONS = {
    "eddn_submission": (
        "Allow OmniCOVAS to submit market prices and other data to the Elite "
        "Dangerous Data Network (EDDN). This helps the community keep market "
        "data current. (Activates in Phase 5)"
    ),
    "edsm_tracking": (
        "Allow OmniCOVAS to submit your visited systems to EDSM (Elite "
        "Dangerous Star Map). Lets you see your exploration progress "
        "publicly. (Activates in Phase 5)"
    ),
    "squadron_telemetry": (
        "Allow OmniCOVAS to sync ship telemetry with your squadron (if you "
        "are in one). Lets squadron members see your ship status in real time. "
        "(Activates in Phase 7)"
    ),
    "ai_provider_calls": (
        "Allow OmniCOVAS to send game context to an external AI provider "
        "(Gemini, OpenAI, or local LLM) for advisory features like tactical "
        "threat assessment. Disabled by default. (Activates in Phase 4+)"
    ),
    "crash_reports": (
        "Allow OmniCOVAS to send crash reports to the maintainers for "
        "debugging. Reports include only the error message and stack trace, "
        "never commander name or personal data."
    ),
    "usage_analytics": (
        "Allow OmniCOVAS to send anonymous aggregate usage metrics (e.g., "
        "'how many commanders use the overlay'). No individual data is "
        "collected."
    ),
}


@router.get("/privacy/toggles")  # type: ignore[untyped-decorator]
async def get_privacy_toggles() -> dict[str, Any]:
    """Get all privacy toggle state."""
    vault = _ensure_vault()

    result = {}
    for toggle_key in sorted(PRIVACY_TOGGLES):
        enabled_str = vault.get(f"privacy_{toggle_key}")
        enabled = enabled_str == "true"
        result[toggle_key] = {
            "enabled": enabled,
            "description": PRIVACY_DESCRIPTIONS.get(toggle_key, ""),
        }

    return result


@router.post("/privacy/toggles/{toggle_key}")  # type: ignore[untyped-decorator]
async def set_privacy_toggle(
    toggle_key: str,
    body: dict[str, Any],
) -> dict[str, str]:
    """Set a privacy toggle on or off."""
    if toggle_key not in PRIVACY_TOGGLES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown toggle: {toggle_key}",
        )

    enabled = body.get("enabled", False)
    vault = _ensure_vault()
    vault.set(f"privacy_{toggle_key}", "true" if enabled else "false")

    logger.info(
        "privacy_toggle_changed | key=%s enabled=%s",
        toggle_key,
        enabled,
    )
    return {"status": "ok"}


@router.post("/privacy/export")  # type: ignore[untyped-decorator]
async def export_privacy_data() -> dict[str, Any]:
    """Export all commander data as a JSON blob."""
    vault = _ensure_vault()

    config_export = {}
    for key in vault.list_keys():
        if not key.endswith("_api_key"):
            try:
                value = vault.get(key)
                config_export[key] = value
            except Exception:
                pass

    kb_count = 0
    activity_log_count = 0

    return {
        "config": config_export,
        "kb_entries": kb_count,
        "activity_log_entries": activity_log_count,
        "exported_at": datetime.utcnow().isoformat() + "Z",
    }


@router.post("/privacy/delete")  # type: ignore[untyped-decorator]
async def delete_all_data(body: dict[str, Any] | None = None) -> dict[str, str]:
    """Delete all local OmniCOVAS data."""
    vault = _ensure_vault()
    vault.clear_all()

    logger.warning("privacy_data_deleted")
    return {"status": "ok"}


PRESET_PROFILES = {
    "casual": {
        "name": "Casual Pilot",
        "pillar_1_enabled": True,
        "overlay_enabled": True,
        "overlay_opacity": 0.85,
        "overlay_anchor": "center",
        "ai_provider": "null",
    },
    "combat": {
        "name": "Combat Pilot",
        "pillar_1_enabled": True,
        "overlay_enabled": True,
        "overlay_opacity": 0.95,
        "overlay_anchor": "center",
        "ai_provider": "null",
    },
    "explorer": {
        "name": "Explorer",
        "pillar_1_enabled": True,
        "overlay_enabled": False,
        "overlay_opacity": 0.85,
        "overlay_anchor": "center",
        "ai_provider": "null",
    },
    "trader": {
        "name": "Trader",
        "pillar_1_enabled": True,
        "overlay_enabled": False,
        "overlay_opacity": 0.85,
        "overlay_anchor": "center",
        "ai_provider": "null",
    },
    "miner": {
        "name": "Miner",
        "pillar_1_enabled": True,
        "overlay_enabled": False,
        "overlay_opacity": 0.85,
        "overlay_anchor": "center",
        "ai_provider": "null",
    },
}


@router.get("/settings")  # type: ignore[untyped-decorator]
async def get_settings() -> dict[str, Any]:
    """Get full settings config."""
    vault = _ensure_vault()

    preset = vault.get("settings_preset") or "casual"
    ai_provider = vault.get("settings_ai_provider") or "null"
    overlay_opacity = float(vault.get("settings_overlay_opacity") or 0.95)
    overlay_anchor = vault.get("settings_overlay_anchor") or "center"

    return {
        "preset": preset,
        "pillar_categories": {
            "pillar_1": {"enabled": True, "phase_ready": True},
            "pillar_2": {"enabled": False, "phase_ready": False, "phase": 4},
            "pillar_3": {"enabled": False, "phase_ready": False, "phase": 5},
            "pillar_5": {"enabled": False, "phase_ready": False, "phase": 6},
            "pillar_7": {"enabled": False, "phase_ready": False, "phase": 7},
            "pillar_6": {"enabled": False, "phase_ready": False, "phase": 8},
            "pillar_4": {"enabled": False, "phase_ready": False, "phase": 9},
        },
        "output_modes": {
            "ship_telemetry": "overlay",
            "combat": "overlay",
            "exploration": "overlay",
        },
        "ai_provider": ai_provider,
        "overlay": {
            "opacity": overlay_opacity,
            "anchor": overlay_anchor,
            "event_toggles": {
                "HULL_CRITICAL_10": True,
                "SHIELDS_DOWN": True,
                "HULL_CRITICAL_25": True,
                "FUEL_CRITICAL": True,
                "MODULE_CRITICAL": True,
                "FUEL_LOW": True,
                "HEAT_WARNING": True,
            },
        },
    }


@router.post("/settings")  # type: ignore[untyped-decorator]
async def update_settings(body: dict[str, Any]) -> dict[str, str]:
    """Save settings config."""
    vault = _ensure_vault()

    if "preset" in body:
        preset = body["preset"]
        if preset in PRESET_PROFILES:
            vault.set("settings_preset", preset)

    if "ai_provider" in body:
        vault.set("settings_ai_provider", body["ai_provider"])

    if "overlay" in body:
        overlay = body["overlay"]
        if "opacity" in overlay:
            vault.set("settings_overlay_opacity", str(overlay["opacity"]))
        if "anchor" in overlay:
            vault.set("settings_overlay_anchor", overlay["anchor"])

    logger.info("settings_updated")
    return {"status": "ok"}


@router.post("/settings/reset")  # type: ignore[untyped-decorator]
async def reset_settings_to_default() -> dict[str, str]:
    """Reset all settings to defaults."""
    vault = _ensure_vault()

    for key in [
        "settings_preset",
        "settings_ai_provider",
        "settings_overlay_opacity",
        "settings_overlay_anchor",
    ]:
        try:
            vault.delete(key)
        except Exception:
            pass

    logger.info("settings_reset_to_default")
    return {"status": "ok"}


@router.post("/settings/export")  # type: ignore[untyped-decorator]
async def export_settings() -> dict[str, Any]:
    """Export settings as JSON."""
    vault = _ensure_vault()

    settings = {}
    for key in vault.list_keys():
        if "settings_" in key:
            try:
                settings[key] = vault.get(key)
            except Exception:
                pass

    return {"settings": settings}


@router.post("/settings/import")  # type: ignore[untyped-decorator]
async def import_settings(body: dict[str, Any]) -> dict[str, str]:
    """Import settings from an exported JSON file."""
    vault = _ensure_vault()

    if "settings" not in body:
        raise HTTPException(status_code=400, detail="Missing 'settings' key")

    for key, value in body["settings"].items():
        if key.startswith("settings_"):
            vault.set(key, str(value))

    logger.info("settings_imported")
    return {"status": "ok"}


_pending_confirmations: dict[str, dict[str, Any]] = {}


@router.get("/confirmations/pending")  # type: ignore[untyped-decorator]
async def get_pending_confirmations() -> dict[str, Any]:
    """Get all pending confirmation requests."""
    confirmations = []
    now = datetime.utcnow().isoformat() + "Z"

    for conf_id, conf in list(_pending_confirmations.items()):
        if conf.get("timeout_at") and conf["timeout_at"] < now:
            del _pending_confirmations[conf_id]
            continue

        confirmations.append(
            {
                "id": conf_id,
                "suggestion_text": conf.get("suggestion_text", ""),
                "why_text": conf.get("why_text", ""),
                "timeout_at": conf.get("timeout_at"),
            }
        )

    return {"confirmations": confirmations}


@router.post("/confirmations/{confirmation_id}")  # type: ignore[untyped-decorator]
async def respond_to_confirmation(
    confirmation_id: str,
    body: dict[str, Any],
) -> dict[str, str]:
    """Respond to a confirmation request."""
    response = body.get("response", "").lower()

    if response not in ("confirm", "decline"):
        raise HTTPException(
            status_code=400,
            detail="response must be 'confirm' or 'decline'",
        )

    if confirmation_id in _pending_confirmations:
        conf = _pending_confirmations[confirmation_id]
        logger.info(
            "confirmation_response | confirmation_id=%s response=%s suggestion=%s",
            confirmation_id,
            response,
            conf.get("suggestion_text", ""),
        )
        del _pending_confirmations[confirmation_id]

    return {"status": "ok"}
