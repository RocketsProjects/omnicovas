/**
 * Phase 3 Week 13 — Privacy Page Controller
 *
 * Manages privacy toggles, data export, and data deletion.
 * All toggles default OFF (Law 8: Privacy-by-Default).
 */

class PrivacyController {
  constructor() {
    this.deleteConfirmStage = 0;
    this.init();
  }

  get apiBase() {
    return `http://127.0.0.1:${window.OMNICOVAS_PORT || 8000}`;
  }

  async init() {
    await this.loadToggles();
    this.bindButtons();
  }

  async loadToggles() {
    try {
      const res = await fetch(`${this.apiBase}/week13/privacy/toggles`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      const container = document.getElementById("privacy-toggles-list");
      if (!container) return;

      container.innerHTML = "";
      for (const [key, info] of Object.entries(data)) {
        const card = this.createToggleCard(key, info);
        container.appendChild(card);
      }
    } catch (err) {
      console.error("Failed to load privacy toggles:", err);
    }
  }

  createToggleCard(key, info) {
    const card = document.createElement("div");
    card.className = "toggle-card";
    card.setAttribute("role", "region");
    card.setAttribute("aria-labelledby", `toggle-label-${key}`);

    const header = document.createElement("div");
    header.className = "toggle-header";

    const label = document.createElement("label");
    label.className = "toggle-label";
    label.id = `toggle-label-${key}`;
    label.textContent = this.formatToggleLabel(key);

    const toggleSwitch = document.createElement("label");
    toggleSwitch.className = "toggle-switch";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = info.enabled || false;
    checkbox.setAttribute("aria-label", `Toggle ${label.textContent}`);
    checkbox.addEventListener("change", () => {
      this.setToggle(key, checkbox.checked);
    });

    const slider = document.createElement("span");
    slider.className = "toggle-slider";

    toggleSwitch.appendChild(checkbox);
    toggleSwitch.appendChild(slider);

    header.appendChild(label);
    header.appendChild(toggleSwitch);

    const desc = document.createElement("p");
    desc.className = "toggle-description";
    desc.textContent = info.description || "";

    card.appendChild(header);
    card.appendChild(desc);

    return card;
  }

  formatToggleLabel(key) {
    const labels = {
      eddn_submission: "EDDN Market Data",
      edsm_tracking: "EDSM Tracking",
      squadron_telemetry: "Squadron Telemetry",
      ai_provider_calls: "AI Provider API Calls",
      crash_reports: "Crash Reports",
      usage_analytics: "Usage Analytics",
    };
    return labels[key] || key;
  }

  async setToggle(key, enabled) {
    try {
      const res = await fetch(`${this.apiBase}/week13/privacy/toggles/${key}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      console.log(`Privacy toggle ${key} set to ${enabled}`);
    } catch (err) {
      console.error(`Failed to set toggle ${key}:`, err);
      // Reload toggles to sync UI with server
      await this.loadToggles();
    }
  }

  async loadDataFlows() {
    try {
      // In Phase 3, all flows return 0 because nothing sends outbound data
      return {
        flows: [
          {
            destination: "EDDN (Elite Dangerous Data Network)",
            status: "not_shipped",
            frequency: "Per market visit (Phase 5+)",
            purpose: "Market price data",
            call_count: 0,
          },
          {
            destination: "EDSM (Elite Dangerous Star Map)",
            status: "not_shipped",
            frequency: "Per system visit (Phase 5+)",
            purpose: "Exploration tracking",
            call_count: 0,
          },
          {
            destination: "Squadron Servers",
            status: "not_shipped",
            frequency: "Per flight session (Phase 7+)",
            purpose: "Ship state sync",
            call_count: 0,
          },
          {
            destination: "AI Provider API (Gemini/OpenAI/Local LLM)",
            status: "not_shipped",
            frequency: "On-demand (Phase 4+)",
            purpose: "Advisory recommendations",
            call_count: 0,
          },
        ],
      };
    } catch (err) {
      console.error("Failed to load data flows:", err);
      return { flows: [] };
    }
  }

  async showDataFlowsModal() {
    const data = await this.loadDataFlows();
    const container = document.getElementById("data-flows-list");
    const noBanner = document.getElementById("no-flows-banner");

    if (!container) return;

    const flows = data.flows || [];
    const hasActiveFlows = flows.some((f) => f.status === "active");

    if (noBanner) {
      noBanner.style.display = hasActiveFlows ? "none" : "block";
    }

    container.innerHTML = "";
    for (const flow of flows) {
      const card = this.createFlowCard(flow);
      container.appendChild(card);
    }

    document.getElementById("data-flows-modal").style.display = "flex";
  }

  createFlowCard(flow) {
    const card = document.createElement("div");
    card.className = "flow-card";

    const dest = document.createElement("div");
    dest.className = "flow-destination";
    dest.textContent = flow.destination;

    const status = document.createElement("span");
    status.className = `flow-status ${flow.status}`;
    status.textContent = this.formatFlowStatus(flow.status);

    const freq = document.createElement("div");
    freq.className = "flow-frequency";
    freq.textContent = `Frequency: ${flow.frequency}`;

    const purpose = document.createElement("div");
    purpose.className = "flow-purpose";
    purpose.textContent = `Purpose: ${flow.purpose}`;

    card.appendChild(dest);
    card.appendChild(status);
    card.appendChild(freq);
    card.appendChild(purpose);

    return card;
  }

  formatFlowStatus(status) {
    const labels = {
      active: "ACTIVE",
      disabled: "DISABLED",
      not_shipped: "NOT YET SHIPPED",
    };
    return labels[status] || status;
  }

  bindButtons() {
    // Data Flows
    document.getElementById("view-data-flows-btn")?.addEventListener("click", () => {
      this.showDataFlowsModal();
    });

    document.getElementById("close-flows-modal-btn")?.addEventListener("click", () => {
      document.getElementById("data-flows-modal").style.display = "none";
    });

    // Export Data
    document.getElementById("export-data-btn")?.addEventListener("click", () => {
      this.exportData();
    });

    // Delete Data (Two-stage confirmation)
    document.getElementById("delete-data-btn")?.addEventListener("click", () => {
      this.showDeleteConfirmModal();
    });

    document.getElementById("delete-confirm-cancel-btn")?.addEventListener("click", () => {
      this.deleteConfirmStage = 0;
      document.getElementById("delete-confirm-modal").style.display = "none";
    });

    document.getElementById("delete-confirm-1st-btn")?.addEventListener("click", () => {
      this.deleteConfirmStage = 1;
      document.getElementById("delete-confirm-buttons").style.display = "none";
      document.getElementById("delete-confirm-2nd-buttons").style.display = "block";
    });

    document.getElementById("delete-confirm-cancel-2nd-btn")?.addEventListener("click", () => {
      this.deleteConfirmStage = 0;
      document.getElementById("delete-confirm-modal").style.display = "none";
      document.getElementById("delete-confirm-buttons").style.display = "block";
      document.getElementById("delete-confirm-2nd-buttons").style.display = "none";
    });

    document.getElementById("delete-confirm-2nd-btn")?.addEventListener("click", () => {
      this.permanentlyDeleteData();
    });
  }

  showDeleteConfirmModal() {
    this.deleteConfirmStage = 0;
    document.getElementById("delete-confirm-buttons").style.display = "flex";
    document.getElementById("delete-confirm-2nd-buttons").style.display = "none";
    document.getElementById("delete-confirm-modal").style.display = "flex";
  }

  async exportData() {
    try {
      const res = await fetch(`${this.apiBase}/week13/privacy/export`, {
        method: "POST",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      // Create JSON blob and download
      const json = JSON.stringify(data, null, 2);
      const blob = new Blob([json], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `omnicovas-export-${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      console.log("Data exported successfully");
    } catch (err) {
      console.error("Failed to export data:", err);
      alert("Failed to export data. See console for details.");
    }
  }

  async permanentlyDeleteData() {
    try {
      const res = await fetch(`${this.apiBase}/week13/privacy/delete`, {
        method: "POST",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      // Close modal
      document.getElementById("delete-confirm-modal").style.display = "none";

      // Show success message and reload
      alert("All OmniCOVAS data has been permanently deleted. Please restart the app.");
      window.location.reload();
    } catch (err) {
      console.error("Failed to delete data:", err);
      alert("Failed to delete data. See console for details.");
    }
  }
}

// Initialize on page load
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    new PrivacyController();
  });
} else {
  new PrivacyController();
}

// Test hook for Vitest; keeps this browser-compatible without changing production module/script loading.
globalThis.__privacyExports = { PrivacyController };
