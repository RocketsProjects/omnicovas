mod overlay;

use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::io::{BufRead, BufReader};
use std::process::{Command, Stdio};
use std::sync::{Mutex, OnceLock};
use std::thread;
use tauri::{Emitter, Manager};

#[derive(Clone, Debug, Serialize, Deserialize)]
struct BridgeInfo {
  port: u64,
  httpBase: String,
  wsBase: String,
}

static BRIDGE_INFO: OnceLock<Mutex<Option<BridgeInfo>>> = OnceLock::new();

fn bridge_store() -> &'static Mutex<Option<BridgeInfo>> {
  BRIDGE_INFO.get_or_init(|| Mutex::new(None))
}

#[tauri::command]
fn get_bridge_info() -> Option<BridgeInfo> {
  bridge_store().lock().ok()?.clone()
}

#[tauri::command]
async fn show_overlay_test_banner(app: tauri::AppHandle) -> Result<(), String> {
  println!("[tauri] show_overlay_test_banner requested");
  app.emit("overlay:show_test_banner", ()).map_err(|e| e.to_string())?;
  overlay::show_overlay(app).await
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .setup(|app| {
      if cfg!(debug_assertions) {
        app.handle().plugin(
          tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build(),
        )?;
      }

      app.handle().plugin(
        tauri_plugin_window_state::Builder::default().build(),
      )?;

      app.handle().plugin(
        tauri_plugin_global_shortcut::Builder::default().build(),
      )?;

      app.manage(overlay::OverlayState::default());
      overlay::init_overlay(app.handle())?;

      let app_handle = app.handle().clone();

      thread::spawn(move || {
        let mut child = Command::new("cmd")
          .args(["/C", "uv run python -m omnicovas.core.main"])
          .current_dir("C:\\Projects\\OmniCOVAS")
          .stdout(Stdio::piped())
          .stderr(Stdio::inherit())
          .spawn()
          .expect("failed to launch OmniCOVAS Python core");

        let stdout = child
          .stdout
          .take()
          .expect("failed to capture OmniCOVAS Python stdout");

        let reader = BufReader::new(stdout);

        for line in reader.lines().map_while(Result::ok) {
          println!("[omnicovas-core] {}", line);

          if let Ok(json) = serde_json::from_str::<Value>(&line) {
            if json.get("status").and_then(|v| v.as_str()) == Some("ready") {
              if let Some(port) = json.get("port").and_then(|v| v.as_u64()) {
                let info = BridgeInfo {
                  port,
                  httpBase: format!("http://127.0.0.1:{port}"),
                  wsBase: format!("ws://127.0.0.1:{port}"),
                };

                if let Ok(mut store) = bridge_store().lock() {
                  *store = Some(info.clone());
                }

                app_handle
                  .emit("bridge-ready", info)
                  .expect("failed to emit bridge-ready");

                println!("OmniCOVAS bridge ready on port {}", port);
              }
            }
          }
        }
      });

      Ok(())
    })
    .invoke_handler(tauri::generate_handler![
      overlay::show_overlay,
      overlay::hide_overlay,
      show_overlay_test_banner,
      get_bridge_info
    ])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
