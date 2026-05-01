from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB_RS = ROOT / "src-tauri" / "src" / "lib.rs"


def test_tauri_bridge_command_is_registered() -> None:
    text = LIB_RS.read_text(encoding="utf-8")

    assert "#[tauri::command]" in text
    assert "fn get_bridge_info()" in text
    assert "get_bridge_info" in text
    assert "tauri::generate_handler!" in text


def test_tauri_bridge_stores_and_emits_ready_port() -> None:
    text = LIB_RS.read_text(encoding="utf-8")

    assert "BridgeInfo" in text
    assert "BRIDGE_INFO" in text
    assert "bridge_store()" in text
    assert '.emit("bridge-ready"' in text
    assert '"port"' in text
    assert "httpBase" in text
    assert "wsBase" in text


def test_tauri_overlay_test_banner_command_is_registered() -> None:
    text = LIB_RS.read_text(encoding="utf-8")

    assert "#[tauri::command]" in text
    assert "async fn show_overlay_test_banner" in text
    assert 'app.emit("overlay:show_test_banner"' in text
    assert "overlay::show_overlay(app).await" in text
    assert "show_overlay_test_banner" in text
    assert "tauri::generate_handler!" in text


def test_tauri_dev_launcher_uses_verified_python_command() -> None:
    text = LIB_RS.read_text(encoding="utf-8")

    assert 'Command::new("cmd")' in text
    assert "uv run python -m omnicovas.core.main" in text
    assert '.current_dir("C:\\\\Projects\\\\OmniCOVAS")' in text
    assert "stdout(Stdio::piped())" in text
