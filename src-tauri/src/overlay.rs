use std::sync::atomic::AtomicBool;

/// Initialize the overlay window and register the global hotkey handler.
///
/// Note: Full global shortcut integration requires the tauri-plugin-global-shortcut
/// API to be fully wired. This is Phase 3.1+ work; Phase 3 stubs the handler.
pub fn init_overlay(_app: &tauri::AppHandle) -> Result<(), Box<dyn std::error::Error>> {
    log::debug!("Overlay initialized (Ctrl+Shift+O hotkey Phase 3.1+)");
    Ok(())
}

/// Show the overlay window (called when a critical event fires).
/// Note: Phase 3.1+ implementation requires Tauri API access via app handle.
#[tauri::command]
pub async fn show_overlay(_app: tauri::AppHandle) -> Result<(), String> {
    log::debug!("show_overlay command (Phase 3.1+ implementation pending)");
    Ok(())
}

/// Hide the overlay window.
#[tauri::command]
pub async fn hide_overlay(_app: tauri::AppHandle) -> Result<(), String> {
    log::debug!("hide_overlay command (Phase 3.1+ implementation pending)");
    Ok(())
}

/// Global state for the overlay window.
pub struct OverlayState {
    pub click_through: AtomicBool,
}

impl Default for OverlayState {
    fn default() -> Self {
        OverlayState {
            click_through: AtomicBool::new(true),
        }
    }
}
