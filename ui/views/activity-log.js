/**
 * Phase 3 Week 13 — Activity Log Controller
 *
 * Full-featured activity log with:
 *  - Filtering by category
 *  - Free-text search
 *  - Pagination (50 rows per page)
 *  - Export to JSON
 *  - Clear with confirmation
 */

class ActivityLogController {
  constructor() {
    this.allEntries = [];
    this.filteredEntries = [];
    this.currentPage = 0;
    this.pageSize = 50;
    this.init();
  }

  get apiBase() {
    if (window.Shell?.httpBase) return window.Shell.httpBase;
    if (window.OMNICOVAS_PORT) return `http://127.0.0.1:${window.OMNICOVAS_PORT}`;
    return null;
  }

  apiUrl(path) {
    const base = this.apiBase;
    return base ? `${base}${path}` : null;
  }

  async init() {
    this.bindEvents();
    if (!this.apiBase) {
      this._showWaiting();
      window.OmniEvents?.addEventListener('bridge-connected', () => this._loadAndRender(), { once: true });
      return;
    }
    await this._loadAndRender();
  }

  _showWaiting() {
    const tbody = document.getElementById('log-body');
    if (!tbody) return;
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan = 5;
    td.className = 'log-waiting';
    td.textContent = 'Waiting for OmniCOVAS bridge…';
    tr.appendChild(td);
    tbody.replaceChildren(tr);
  }

  async _loadAndRender() {
    await this.loadActivityLog();
    this.renderPage();
  }

  async loadActivityLog() {
    const url = this.apiUrl('/activity-log');
    if (!url) return;
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      this.allEntries = data.entries || [];
      this.filteredEntries = [...this.allEntries];
    } catch (err) {
      console.error("Failed to load activity log:", err);
      this.allEntries = [];
      this.filteredEntries = [];
    }
  }

  bindEvents() {
    // Search
    document.getElementById("log-search")?.addEventListener("input", (e) => {
      this.filterAndRender(e.target.value);
    });

    // Filters
    document.querySelectorAll(".log-filter").forEach((checkbox) => {
      checkbox.addEventListener("change", () => {
        this.applyFilters();
      });
    });

    // Actions
    document.getElementById("log-export-btn")?.addEventListener("click", () => {
      this.exportLog();
    });

    document.getElementById("log-clear-btn")?.addEventListener("click", () => {
      this.showClearConfirm();
    });

    // Clear modal
    document.getElementById("log-clear-confirm-btn")?.addEventListener("click", () => {
      this.clearLog();
    });

    document.getElementById("log-clear-cancel-btn")?.addEventListener("click", () => {
      document.getElementById("log-clear-modal").style.display = "none";
    });

    // Pagination
    document.getElementById("log-prev-btn")?.addEventListener("click", () => {
      if (this.currentPage > 0) {
        this.currentPage--;
        this.renderPage();
      }
    });

    document.getElementById("log-next-btn")?.addEventListener("click", () => {
      const maxPage = Math.ceil(this.filteredEntries.length / this.pageSize) - 1;
      if (this.currentPage < maxPage) {
        this.currentPage++;
        this.renderPage();
      }
    });
  }

  filterAndRender(searchText) {
    const text = searchText.toLowerCase();
    this.filteredEntries = this.allEntries.filter((entry) => {
      const eventType = (entry.event_type || "").toLowerCase();
      const summary = (entry.summary || "").toLowerCase();
      return eventType.includes(text) || summary.includes(text);
    });

    this.applyFilters();
  }

  applyFilters() {
    const selectedCategories = new Set();
    document.querySelectorAll(".log-filter:checked").forEach((checkbox) => {
      selectedCategories.add(checkbox.value);
    });

    if (selectedCategories.size > 0) {
      this.filteredEntries = this.filteredEntries.filter((entry) => {
        const category = this.getEventCategory(entry.event_type);
        return selectedCategories.has(category);
      });
    }

    this.currentPage = 0;
    this.renderPage();
  }

  getEventCategory(eventType) {
    if (!eventType) return "telemetry";

    const type = eventType.toUpperCase();
    if (type.includes("CRITICAL") || type.includes("DESTROYED")) return "critical";
    if (type.includes("DOCKED") || type.includes("WANTED") || type.includes("FSD"))
      return "extended";
    if (type.includes("TIER_3") || type.includes("CONFIRMATION")) return "ai";
    return "telemetry";
  }

  renderPage() {
    const tbody = document.getElementById("log-body");
    if (!tbody) return;

    const start = this.currentPage * this.pageSize;
    const end = start + this.pageSize;
    const pageEntries = this.filteredEntries.slice(start, end);

    tbody.innerHTML = "";
    for (const entry of pageEntries) {
      const row = this.createLogRow(entry);
      tbody.appendChild(row);
    }

    this.updatePagination();
  }

  createLogRow(entry) {
    const row = document.createElement("tr");

    const timestamp = entry.timestamp || "";
    const eventType = entry.event_type || "unknown";
    const source = entry.source || "system";
    const summary = entry.summary || "—";
    const aiTier = entry.ai_tier || "—";

    const category = this.getEventCategory(eventType);

    const timestampCell = document.createElement("td");
    timestampCell.className = "log-timestamp";
    timestampCell.textContent = this.formatTimestamp(timestamp);

    const typeCell = document.createElement("td");
    typeCell.className = `log-event-type ${category}`;
    typeCell.textContent = eventType;

    const sourceCell = document.createElement("td");
    sourceCell.className = "log-source";
    sourceCell.textContent = source;

    const summaryCell = document.createElement("td");
    summaryCell.className = "log-summary";
    summaryCell.textContent = summary;

    const tierCell = document.createElement("td");
    tierCell.textContent = aiTier;

    row.append(timestampCell, typeCell, sourceCell, summaryCell, tierCell);

    return row;
  }

  formatTimestamp(ts) {
    if (!ts) return "";
    try {
      const date = new Date(ts);
      return date.toLocaleString([], {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
    } catch {
      return ts;
    }
  }

  updatePagination() {
    const maxPage = Math.ceil(this.filteredEntries.length / this.pageSize);
    const pageInfo = document.getElementById("log-page-info");
    if (pageInfo) {
      pageInfo.textContent = `Page ${this.currentPage + 1} of ${maxPage}`;
    }

    const prevBtn = document.getElementById("log-prev-btn");
    const nextBtn = document.getElementById("log-next-btn");

    if (prevBtn) prevBtn.disabled = this.currentPage === 0;
    if (nextBtn) nextBtn.disabled = this.currentPage >= maxPage - 1;
  }

  async exportLog() {
    const json = JSON.stringify(
      {
        total: this.filteredEntries.length,
        entries: this.filteredEntries,
        exported_at: new Date().toISOString(),
      },
      null,
      2
    );

    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `omnicovas-activity-log-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  showClearConfirm() {
    document.getElementById("log-clear-modal").style.display = "flex";
  }

  async clearLog() {
    try {
      // In Phase 3, there's no /activity-log/clear endpoint
      // This is a placeholder for future implementation
      this.allEntries = [];
      this.filteredEntries = [];
      this.currentPage = 0;

      document.getElementById("log-clear-modal").style.display = "none";
      this.renderPage();
      alert("Activity log cleared!");
    } catch (err) {
      console.error("Failed to clear log:", err);
      alert("Failed to clear log. See console for details.");
    }
  }
}

// Test hook for Vitest; keeps this browser-compatible without changing production module/script loading.
globalThis.__activityLogExports = { ActivityLogController };

// Initialize on page load
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    new ActivityLogController();
  });
} else {
  new ActivityLogController();
}
