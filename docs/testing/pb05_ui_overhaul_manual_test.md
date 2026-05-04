# PB05 UI Overhaul — Manual Smoke Test Plan

## Prerequisites
- OmniCOVAS Backend running (`python -m omnicovas.core.main`)
- OmniCOVAS Frontend running in Tauri or Dev Browser
- (Optional) Elite Dangerous running for live telemetry

## Checklist

### 1. Launch & Bridge
- [ ] App launches without white-screen or hanging.
- [ ] Connection bar shows "Connected" once backend is detected.
- [ ] Correct port is displayed in the top-bar.

### 2. Navigation Shell
- [ ] Sidebar links navigate to correct views.
- [ ] Active link is visually highlighted.
- [ ] Sidebar can be navigated using Tab/Enter.

### 3. Dashboard (Ship Systems Schematic)
- [ ] Sidewinder technical wireframe renders correctly.
- [ ] Hotspots (Cargo, Modules, Fuel, etc.) are visible.
- [ ] Clicking a hotspot toggles the corresponding data panel.
- [ ] Panels display "Unknown" or "—" if telemetry is missing.
- [ ] "Reset Panels" button works.

### 4. Activity Log (Flight Recorder)
- [ ] Log entries load and display in the table.
- [ ] Category checkboxes (Combat, Exploration, etc.) filter the list.
- [ ] Search bar filters the list in real-time.
- [ ] Pagination (Next/Prev) works.
- [ ] Clear Log button opens a confirmation modal.

### 5. Resources (Diagnostics)
- [ ] CPU, Memory, Disk, and Budget cards render.
- [ ] Values update or show "—" if unavailable.
- [ ] Refresh button works.

### 6. Settings (Configuration Bay)
- [ ] Tabs (Basic, AI, Overlay) switch correctly.
- [ ] Presets can be selected.
- [ ] Overlay toggles and Opacity slider work.
- [ ] "Test Banner" triggers the overlay.

### 7. Overlay (HUD Projection)
- [ ] Overlay window is transparent.
- [ ] Test banners appear in the correct anchor position.
- [ ] Overlay does not steal focus from the main window.
- [ ] Critical banners (e.g., Hull < 10%) pulse and stay visible.

### 8. Privacy & Credits
- [ ] Data Firewall toggles work.
- [ ] Export/Delete buttons work.
- [ ] Credits (Registry Plaque) renders correctly.

### 9. Future Systems
- [ ] Future Systems group is collapsed by default.
- [ ] Expanding shows disabled/muted items.
- [ ] Items cannot be clicked/navigated.

## Performance & Safety
- [ ] No red errors in DevTools console.
- [ ] UI remains responsive during telemetry bursts.
- [ ] Memory usage remains stable.
