from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL_JS = ROOT / "ui" / "components" / "shell.js"


def test_shell_listens_for_tauri_bridge_ready_event() -> None:
    text = SHELL_JS.read_text(encoding="utf-8")

    assert "waitForTauriBridgeReady" in text
    assert "window.__TAURI__?.event?.listen" in text
    assert "'bridge-ready'" in text or '"bridge-ready"' in text


def test_shell_has_command_fallback_for_missed_event() -> None:
    text = SHELL_JS.read_text(encoding="utf-8")

    assert "getBridgeFromTauriCommand" in text
    assert "window.__TAURI__?.core?.invoke" in text
    assert "get_bridge_info" in text


def test_shell_connects_to_state_and_websocket_endpoints() -> None:
    text = SHELL_JS.read_text(encoding="utf-8")

    assert "/state" in text
    assert "/ws/events" in text
    assert "new WebSocket" in text
    assert "fetchState" in text
    assert "openWebSocket" in text


def test_shell_exposes_global_event_bus_for_views() -> None:
    text = SHELL_JS.read_text(encoding="utf-8")

    assert "window.OmniEvents" in text
    assert "new EventTarget()" in text
    assert "CustomEvent" in text
    assert "emit('state'" in text
    assert "emit('event'" in text
