import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAURI_CONF = ROOT / "src-tauri" / "tauri.conf.json"


def test_tauri_exposes_global_js_api_for_shell_autoconnect() -> None:
    config = json.loads(TAURI_CONF.read_text(encoding="utf-8"))

    assert config["app"]["withGlobalTauri"] is True


def test_tauri_has_main_and_overlay_windows() -> None:
    config = json.loads(TAURI_CONF.read_text(encoding="utf-8"))
    windows = {window["label"]: window for window in config["app"]["windows"]}

    assert "main" in windows
    assert "overlay" in windows
    assert windows["overlay"]["transparent"] is True
    assert windows["overlay"]["alwaysOnTop"] is True
    assert windows["overlay"]["visible"] is False
