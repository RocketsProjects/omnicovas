from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARGO_TOML = ROOT / "src-tauri" / "Cargo.toml"


def test_tauri_shell_dependency_is_declared() -> None:
    text = CARGO_TOML.read_text(encoding="utf-8")

    assert "tauri-plugin-shell" in text
    assert "serde_json" in text
    assert "tauri-plugin-window-state" in text
    assert "tauri-plugin-global-shortcut" in text
