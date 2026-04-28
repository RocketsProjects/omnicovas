/**
 * Phase 3 Week 13 — Settings Controller
 *
 * Three-tier customization:
 *  - Tier 1: Preset profiles (quick starts)
 *  - Tier 2: Pillar categories (enable/disable entire features)
 *  - Tier 3: Granular settings (per-feature fine-tuning)
 */

class SettingsController {
  constructor() {
    this.apiBase = `http://127.0.0.1:${window.PORT || 8000}`;
    this.currentSettings = {};
    this.init();
  }

  async init() {
    await this.loadSettings();
    this.renderUI();
    this.bindEvents();
  }

  async loadSettings() {
    try {
      const res = await fetch(`${this.apiBase}/week13/settings`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      this.currentSettings = await res.json();
    } catch (err) {
      console.error("Failed to load settings:", err);
      this.currentSettings = this.getDefaults();
    }
  }

  getDefaults() {
    return {
      preset: "casual",
      pillar_categories: {
        pillar_1: { enabled: true, phase_ready: true },
        pillar_2: { enabled: false, phase_ready: false, phase: 4 },
        pillar_3: { enabled: false, phase_ready: false, phase: 5 },
        pillar_5: { enabled: false, phase_ready: false, phase: 6 },
        pillar_7: { enabled: false, phase_ready: false, phase: 7 },
        pillar_6: { enabled: false, phase_ready: false, phase: 8 },
        pillar_4: { enabled: false, phase_ready: false, phase: 9 },
      },
      ai_provider: "null",
      overlay: {
        opacity: 0.95,
        anchor: "center",
      },
    };
  }

  renderUI() {
    this.renderPresets();
    this.renderPillarToggles();
    this.renderGranularSettings();
  }

  renderPresets() {
    const grid = document.getElementById("preset-grid");
    if (!grid) return;

    const presets = [
      { key: "casual", name: "Casual", icon: "😎" },
      { key: "combat", name: "Combat", icon: "⚔️" },
      { key: "explorer", name: "Explorer", icon: "🔭" },
      { key: "trader", name: "Trader", icon: "📦" },
      { key: "miner", name: "Miner", icon: "⛏️" },
    ];

    grid.innerHTML = "";
    for (const preset of presets) {
      const btn = document.createElement("button");
      btn.className = "preset-button";
      if (preset.key === this.currentSettings.preset) {
        btn.classList.add("active");
      }
      btn.setAttribute("aria-label", `Select ${preset.name} preset`);

      btn.innerHTML = `
        <div class="preset-icon">${preset.icon}</div>
        <div class="preset-name">${preset.name}</div>
      `;

      btn.addEventListener("click", () => {
        this.setPreset(preset.key);
      });

      grid.appendChild(btn);
    }
  }

  renderPillarToggles() {
    const container = document.getElementById("tier2-toggles");
    if (!container) return;

    const cats = this.currentSettings.pillar_categories || {};
    container.innerHTML = "";

    const pillarLabels = {
      pillar_1: "Ship Telemetry",
      pillar_2: "Combat",
      pillar_3: "Exploration",
      pillar_5: "Trading & Mining",
      pillar_7: "Squadron",
      pillar_6: "Engineering",
      pillar_4: "Powerplay 2.0",
    };

    for (const [key, info] of Object.entries(cats)) {
      const item = document.createElement("label");
      item.className = "toggle-item";

      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = info.enabled || false;
      checkbox.disabled = !info.phase_ready;
      checkbox.setAttribute("aria-label", `Toggle ${pillarLabels[key]}`);

      const label = document.createElement("span");
      label.className = "toggle-label";
      label.textContent = pillarLabels[key];

      const phase = document.createElement("span");
      phase.className = "toggle-phase";
      if (!info.phase_ready) {
        phase.textContent = `Phase ${info.phase}`;
      }

      item.appendChild(checkbox);
      item.appendChild(label);
      if (!info.phase_ready) {
        item.appendChild(phase);
      }

      container.appendChild(item);
    }
  }

  renderGranularSettings() {
    // Overlay opacity
    const opacitySlider = document.getElementById("overlay-opacity");
    const opacityDisplay = document.getElementById("opacity-display");
    if (opacitySlider) {
      opacitySlider.value = this.currentSettings.overlay?.opacity || 0.95;
      opacitySlider.addEventListener("input", (e) => {
        const val = parseFloat(e.target.value);
        opacityDisplay.textContent = `${Math.round(val * 100)}%`;
      });
    }

    // Overlay anchor
    const anchorSelect = document.getElementById("overlay-anchor");
    if (anchorSelect) {
      anchorSelect.value = this.currentSettings.overlay?.anchor || "center";
    }

    // AI provider
    const aiSelect = document.getElementById("ai-provider");
    if (aiSelect) {
      aiSelect.value = this.currentSettings.ai_provider || "null";
    }

    // Output mode
    const outputRadios = document.querySelectorAll('input[name="output-mode"]');
    outputRadios.forEach((radio) => {
      if (radio.value === "overlay") {
        radio.checked = true;
      }
    });
  }

  bindEvents() {
    document.getElementById("save-settings-btn")?.addEventListener("click", () => {
      this.saveSettings();
    });

    document.getElementById("reset-settings-btn")?.addEventListener("click", () => {
      this.resetSettings();
    });

    document.getElementById("export-settings-btn")?.addEventListener("click", () => {
      this.exportSettings();
    });

    document.getElementById("import-settings-btn")?.addEventListener("click", () => {
      this.importSettings();
    });
  }

  setPreset(preset) {
    this.currentSettings.preset = preset;
    this.renderPresets();
  }

  async saveSettings() {
    const overlay = {
      opacity: parseFloat(document.getElementById("overlay-opacity")?.value || 0.95),
      anchor: document.getElementById("overlay-anchor")?.value || "center",
    };

    const aiProvider = document.getElementById("ai-provider")?.value || "null";

    const payload = {
      preset: this.currentSettings.preset,
      overlay,
      ai_provider: aiProvider,
    };

    try {
      const res = await fetch(`${this.apiBase}/week13/settings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      alert("Settings saved!");
      await this.loadSettings();
      this.renderUI();
    } catch (err) {
      console.error("Failed to save settings:", err);
      alert("Failed to save settings. See console for details.");
    }
  }

  async resetSettings() {
    if (!confirm("Reset all settings to defaults?")) return;

    try {
      const res = await fetch(`${this.apiBase}/week13/settings/reset`, {
        method: "POST",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      await this.loadSettings();
      this.renderUI();
      alert("Settings reset to defaults!");
    } catch (err) {
      console.error("Failed to reset settings:", err);
      alert("Failed to reset settings. See console for details.");
    }
  }

  async exportSettings() {
    try {
      const res = await fetch(`${this.apiBase}/week13/settings/export`, {
        method: "POST",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      const json = JSON.stringify(data, null, 2);
      const blob = new Blob([json], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `omnicovas-settings-${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Failed to export settings:", err);
      alert("Failed to export settings. See console for details.");
    }
  }

  async importSettings() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".json";
    input.addEventListener("change", async (e) => {
      const file = e.target.files?.[0];
      if (!file) return;

      try {
        const text = await file.text();
        const data = JSON.parse(text);

        if (!confirm("This will overwrite your current settings. Continue?")) {
          return;
        }

        const res = await fetch(`${this.apiBase}/week13/settings/import`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        await this.loadSettings();
        this.renderUI();
        alert("Settings imported!");
      } catch (err) {
        console.error("Failed to import settings:", err);
        alert("Failed to import settings. See console for details.");
      }
    });
    input.click();
  }
}

// Initialize on page load
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    new SettingsController();
  });
} else {
  new SettingsController();
}
