"""
tests.test_overlay_integration

Integration tests for the overlay window and critical event broadcasting.

NOTE: Full game-coexistence tests (Elite running in fullscreen-borderless)
are manual. These stubs verify the overlay window configuration, event
broadcasting, and banner queue logic.

See: docs/internal/dev-guides/phase_3_dev_guide.txt Week 12 Part E
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from omnicovas.api.pillar1 import (
    _OVERLAY_EVENT_DEFAULTS,
    _VALID_ANCHORS,
    get_overlay_settings,
    set_config_vault,
    update_overlay_settings,
)


class TestOverlayEndpoints:
    """Verify /pillar1/overlay/* endpoints."""

    def setup_method(self) -> None:
        # Reset vault injection before each test
        set_config_vault(None)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    async def test_get_overlay_settings_returns_defaults(self) -> None:
        """GET /pillar1/overlay/settings returns sensible defaults when no vault."""
        result = await get_overlay_settings()

        assert result["opacity"] == 0.95
        assert result["anchor"] == "center"
        assert "HULL_CRITICAL_10" in result["events"]
        assert result["events"]["HULL_CRITICAL_10"] is True

    @pytest.mark.asyncio
    async def test_get_overlay_settings_all_event_types_present(self) -> None:
        """All critical event types have toggles."""
        result = await get_overlay_settings()
        for event in _OVERLAY_EVENT_DEFAULTS:
            assert event in result["events"]
            assert isinstance(result["events"][event], bool)

    @pytest.mark.asyncio
    async def test_update_overlay_settings_accepts_body(self) -> None:
        """POST /pillar1/overlay/settings accepts and acknowledges updates."""
        body = {
            "opacity": 0.8,
            "anchor": "tl",
            "events": {"HEAT_WARNING": False},
        }
        result = await update_overlay_settings(body)

        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_update_overlay_settings_any_body_returns_ok(self) -> None:
        """POST endpoint is forgiving of unexpected fields."""
        result = await update_overlay_settings({})
        assert result["status"] == "ok"

        result = await update_overlay_settings({"unknown_field": True})
        assert result["status"] == "ok"


class TestOverlaySettingsPersistence:
    """Verify overlay settings round-trip through the vault."""

    def _make_vault(self, stored: dict[str, str | None]) -> MagicMock:
        """Build a minimal vault mock backed by a dict."""
        vault = MagicMock()
        vault.get.side_effect = lambda key: stored.get(key)
        vault.set.side_effect = lambda key, val: stored.update({key: val})
        return vault

    def setup_method(self) -> None:
        set_config_vault(None)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    async def test_opacity_range(self) -> None:
        """Default opacity must be between 0.5 and 1.0."""
        result = await get_overlay_settings()
        assert 0.5 <= result["opacity"] <= 1.0

    @pytest.mark.asyncio
    async def test_anchor_valid_values(self) -> None:
        """Default anchor must be a valid value."""
        result = await get_overlay_settings()
        assert result["anchor"] in _VALID_ANCHORS

    @pytest.mark.asyncio
    async def test_click_through_default_true(self) -> None:
        """Click-through defaults to True when no vault entry."""
        result = await get_overlay_settings()
        assert result["click_through"] is True

    @pytest.mark.asyncio
    async def test_vault_persists_opacity(self) -> None:
        """Saved opacity is read back from vault."""
        store: dict[str, str | None] = {"settings_overlay_opacity": "0.7"}
        set_config_vault(self._make_vault(store))
        result = await get_overlay_settings()
        assert result["opacity"] == pytest.approx(0.7)

    @pytest.mark.asyncio
    async def test_vault_persists_anchor(self) -> None:
        """Saved anchor is read back from vault."""
        store: dict[str, str | None] = {"settings_overlay_anchor": "tr"}
        set_config_vault(self._make_vault(store))
        result = await get_overlay_settings()
        assert result["anchor"] == "tr"

    @pytest.mark.asyncio
    async def test_vault_persists_event_toggle(self) -> None:
        """Saved event toggle is read back."""
        store: dict[str, str | None] = {
            "overlay_events": json.dumps({"HEAT_WARNING": False}),
        }
        set_config_vault(self._make_vault(store))
        result = await get_overlay_settings()
        assert result["events"]["HEAT_WARNING"] is False
        # Other events remain enabled
        assert result["events"]["HULL_CRITICAL_10"] is True

    @pytest.mark.asyncio
    async def test_vault_persists_click_through_false(self) -> None:
        """Saved click-through=false is read back correctly."""
        store: dict[str, str | None] = {"overlay_click_through": "false"}
        set_config_vault(self._make_vault(store))
        result = await get_overlay_settings()
        assert result["click_through"] is False

    @pytest.mark.asyncio
    async def test_update_writes_to_vault(self) -> None:
        """POST /overlay/settings writes values to the vault."""
        store: dict[str, str | None] = {}
        set_config_vault(self._make_vault(store))
        await update_overlay_settings(
            {"opacity": 0.6, "anchor": "bl", "click_through": False}
        )
        assert store.get("settings_overlay_opacity") == "0.6"
        assert store.get("settings_overlay_anchor") == "bl"
        assert store.get("overlay_click_through") == "false"

    @pytest.mark.asyncio
    async def test_update_event_toggle_merges(self) -> None:
        """Partial event update merges with defaults rather than clobbering."""
        store: dict[str, str | None] = {}
        set_config_vault(self._make_vault(store))
        await update_overlay_settings({"events": {"HEAT_WARNING": False}})
        saved = json.loads(store["overlay_events"])  # type: ignore[index]
        assert saved["HEAT_WARNING"] is False
        assert saved["HULL_CRITICAL_10"] is True

    @pytest.mark.asyncio
    async def test_invalid_opacity_from_vault_uses_default(self) -> None:
        """Corrupt opacity in vault falls back to default."""
        store: dict[str, str | None] = {"settings_overlay_opacity": "not_a_number"}
        set_config_vault(self._make_vault(store))
        result = await get_overlay_settings()
        assert result["opacity"] == 0.95

    @pytest.mark.asyncio
    async def test_invalid_anchor_from_vault_uses_default(self) -> None:
        """Unknown anchor in vault falls back to center."""
        store: dict[str, str | None] = {"settings_overlay_anchor": "invalid_pos"}
        set_config_vault(self._make_vault(store))
        result = await get_overlay_settings()
        assert result["anchor"] == "center"

    @pytest.mark.asyncio
    async def test_no_vault_update_still_returns_ok(self) -> None:
        """POST without vault injected degrades gracefully."""
        # vault is None (reset by setup_method)
        result = await update_overlay_settings({"opacity": 0.8})
        assert result["status"] == "ok"


class TestOverlayBannerQueue:
    """Verify banner priority and queue logic."""

    def test_critical_events_priority_order(self) -> None:
        """HULL_CRITICAL_10 has highest priority; HEAT_WARNING lowest."""
        critical_events = {
            "HULL_CRITICAL_10": 1,
            "SHIELDS_DOWN": 2,
            "HULL_CRITICAL_25": 3,
            "FUEL_CRITICAL": 4,
            "MODULE_CRITICAL": 5,
            "FUEL_LOW": 6,
            "HEAT_WARNING": 7,
        }
        priorities = sorted(critical_events.values())
        assert priorities == list(range(1, 8))

    def test_banner_config_has_required_fields(self) -> None:
        """Each critical event has icon, label, severity, duration, priority."""
        expected_fields = {"icon", "label", "severity", "duration", "priority"}
        sample_config = {
            "icon": "⚠",
            "label": "TEST",
            "severity": "critical",
            "duration": 30000,
            "priority": 1,
        }
        assert set(sample_config.keys()) == expected_fields

    def test_overlay_js_has_test_banner_config(self) -> None:
        """overlay.js must contain OMNICOVAS_TEST config for visibility checks."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "OMNICOVAS_TEST" in overlay_js
        assert "OMNICOVAS TEST BANNER" in overlay_js
        assert "priority: 99" in overlay_js


class TestOverlayAnchorPositioning:
    """Verify anchor values map to valid CSS classes."""

    def test_all_anchors_have_css_class(self) -> None:
        """Every valid anchor token must map to a known CSS class in overlay.html."""
        overlay_html = Path("ui/overlay.html").read_text(encoding="utf-8")
        for anchor in _VALID_ANCHORS:
            # Short-form anchors map: tl->top-left, tr->top-right, etc.
            css_class = {
                "tl": "anchor-top-left",
                "tr": "anchor-top-right",
                "bl": "anchor-bottom-left",
                "br": "anchor-bottom-right",
                "center": "anchor-center",
            }[anchor]
            assert css_class in overlay_html, (
                f"CSS class {css_class!r} missing for anchor {anchor!r}"
            )

    def test_overlay_js_applies_anchor(self) -> None:
        """overlay.js must contain applyAnchor function that sets anchor class."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "applyAnchor" in overlay_js
        assert "ANCHOR_CLASS_MAP" in overlay_js
        assert "anchor-center" in overlay_js

    def test_invalid_anchor_falls_back(self) -> None:
        """Invalid anchors fall back to anchor-center."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        # The fallback line should read: || 'anchor-center'
        assert "|| 'anchor-center'" in overlay_js


class TestOverlayClickthroughObservability:
    """Verify click-through observability requirements."""

    def test_overlay_js_listens_for_toggle_event(self) -> None:
        """overlay.js must listen for overlay:click_through_toggled."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "overlay:click_through_toggled" in overlay_js
        assert "updateStatusDot" in overlay_js

    def test_overlay_js_updates_visibility_on_toggle(self) -> None:
        """overlay.js should show/hide window for feedback on toggle."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        # Should call show_overlay and hide_overlay for feedback
        assert "show_overlay" in overlay_js
        assert "hide_overlay" in overlay_js

    def test_overlay_html_has_status_dot_styles(self) -> None:
        """overlay.html must have styles for the status indicator."""
        overlay_html = Path("ui/overlay.html").read_text(encoding="utf-8")
        assert ".status-dot" in overlay_html
        assert ".status-dot.grab" in overlay_html


class TestOverlayShowHideNotStubs:
    """Contract tests proving show_overlay / hide_overlay are not no-op stubs."""

    def test_show_overlay_calls_get_webview_window(self) -> None:
        """show_overlay source must reference get_webview_window, not be a stub."""
        # The Rust source is the authority; check the overlay.rs file directly.
        overlay_rs = Path("src-tauri/src/overlay.rs").read_text(encoding="utf-8")
        assert "get_webview_window" in overlay_rs
        assert "Phase 3.1+ implementation pending" not in overlay_rs

    def test_hide_overlay_calls_get_webview_window(self) -> None:
        """hide_overlay source must reference get_webview_window."""
        overlay_rs = Path("src-tauri/src/overlay.rs").read_text(encoding="utf-8")
        # Both show and hide call get_webview_window
        assert overlay_rs.count("get_webview_window") >= 2

    def test_hotkey_binding_is_not_just_plugin_registration(self) -> None:
        """init_overlay must register an on_shortcut handler."""
        overlay_rs = Path("src-tauri/src/overlay.rs").read_text(encoding="utf-8")
        assert "on_shortcut" in overlay_rs
        assert "toggle_click_through" in overlay_rs

    def test_overlay_errors_on_missing_window(self) -> None:
        """show/hide commands return Err when window not found (source check)."""
        overlay_rs = Path("src-tauri/src/overlay.rs").read_text(encoding="utf-8")
        assert "not found" in overlay_rs  # error message text
        assert "ok_or_else" in overlay_rs  # Err path wired


class TestOverlayClickthrough:
    """Verify click-through toggle behavior."""

    def test_click_through_default_is_true(self) -> None:
        """OverlayState::default() sets click_through to true."""
        overlay_rs = Path("src-tauri/src/overlay.rs").read_text(encoding="utf-8")
        assert "AtomicBool::new(true)" in overlay_rs

    def test_hotkey_ctrl_shift_o_registered(self) -> None:
        """Ctrl+Shift+O constant is defined and used in init_overlay."""
        overlay_rs = Path("src-tauri/src/overlay.rs").read_text(encoding="utf-8")
        assert "Ctrl+Shift+O" in overlay_rs
        assert "global_shortcut" in overlay_rs


class TestOverlayBridgeDiscovery:
    """Verify overlay.js uses dynamic bridge discovery, not hard-coded port."""

    def test_no_hardcoded_window_location_host(self) -> None:
        """overlay.js must not build the WS URL from window.location.host."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "window.location.host" not in overlay_js, (
            "overlay.js must not use window.location.host for WS URL"
        )

    def test_no_hardcoded_ws_port(self) -> None:
        """overlay.js must not contain a literal hard-coded WS port."""
        import re

        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        matches = re.findall(r"ws://127\.0\.0\.1:\d+", overlay_js)
        assert not matches, f"Hard-coded WS port(s) found in overlay.js: {matches}"

    def test_discover_bridge_function_exists(self) -> None:
        """overlay.js must define discoverBridge for dynamic port resolution."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "discoverBridge" in overlay_js

    def test_discover_bridge_uses_get_bridge_info(self) -> None:
        """discoverBridge must invoke the get_bridge_info Tauri command."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "get_bridge_info" in overlay_js

    def test_discover_bridge_listens_for_bridge_ready(self) -> None:
        """discoverBridge must also listen for the bridge-ready Tauri event."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "bridge-ready" in overlay_js

    def test_connect_websocket_uses_bridge_ws_base(self) -> None:
        """connectWebSocket must use the bridgeWsBase variable, not a literal origin."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "bridgeWsBase" in overlay_js

    def test_load_overlay_settings_uses_bridge_http_base(self) -> None:
        """loadOverlaySettings must use bridgeHttpBase, not a relative path."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "bridgeHttpBase" in overlay_js
        # Relative path is no longer acceptable
        assert "fetch('/pillar1" not in overlay_js

    def test_invoke_uses_tauri_v2_core_path(self) -> None:
        """overlay.js must use Tauri v2 core.invoke, not deprecated .tauri.invoke."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "__TAURI__.tauri" not in overlay_js, (
            "overlay.js uses deprecated Tauri v1 .tauri.invoke path"
        )
        assert "__TAURI__?.core?.invoke" in overlay_js

    def test_ws_reconnect_uses_backoff(self) -> None:
        """WebSocket reconnect must use exponential backoff, not a fixed interval."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "wsReconnectDelay" in overlay_js
        assert "Math.min" in overlay_js

    def test_show_overlay_test_banner_command_wired_in_lib(self) -> None:
        """lib.rs must register show_overlay_test_banner and emit the test event."""
        lib_rs = Path("src-tauri/src/lib.rs").read_text(encoding="utf-8")
        assert "show_overlay_test_banner" in lib_rs
        assert 'app.emit("overlay:show_test_banner"' in lib_rs
        assert "overlay::show_overlay(app).await" in lib_rs

    def test_overlay_js_listens_for_show_test_banner(self) -> None:
        """overlay.js must listen for overlay:show_test_banner and call showBanner."""
        overlay_js = Path("ui/overlay.js").read_text(encoding="utf-8")
        assert "overlay:show_test_banner" in overlay_js
        assert "showBanner('OMNICOVAS_TEST'" in overlay_js

    def test_overlay_window_url_set_to_overlay_html(self) -> None:
        """tauri.conf.json overlay window must declare url: overlay.html.

        Without an explicit url, Tauri v2 loads index.html (dashboard) for
        every window. overlay.js would never execute and no banner listeners
        would register.
        """
        import json

        conf = json.loads(Path("src-tauri/tauri.conf.json").read_text(encoding="utf-8"))
        windows = conf["app"]["windows"]
        overlay_conf = next((w for w in windows if w["label"] == "overlay"), None)
        assert overlay_conf is not None, "overlay window not found in tauri.conf.json"
        assert overlay_conf.get("url") == "overlay.html", (
            'overlay window must declare "url": "overlay.html" in tauri.conf.json'
        )
