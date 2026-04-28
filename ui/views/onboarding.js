/**
 * Phase 3 Week 13 — First-Run Onboarding Controller
 *
 * Manages the three-path onboarding flow:
 *  A. Easy Mode (60-second preset)
 *  B. Custom Setup (5-15 minute wizard)
 *  C. Power User (full Settings + Privacy)
 */

class OnboardingController {
  constructor() {
    this.apiBase = `http://127.0.0.1:${window.PORT || 8000}`;
    this.currentPath = null;
    this.customStepIndex = 0;
    this.customSteps = [
      "preset",
      "ai",
      "privacy",
      "output",
      "overlay",
    ];
    this.powerUserSeen = {
      settings: false,
      privacy: false,
    };
    this.init();
  }

  async init() {
    // Check if onboarding should display
    const status = await this.checkOnboardingStatus();
    if (!status.should_show_wizard) {
      // First-run already complete; hide onboarding entirely
      document.getElementById("onboarding-container").style.display = "none";
      return;
    }

    // Show path selection
    this.showPathSelection();
    this.bindPathButtons();
    this.bindStepButtons();
  }

  async checkOnboardingStatus() {
    try {
      const res = await fetch(`${this.apiBase}/week13/onboarding/status`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.error("Failed to check onboarding status:", err);
      // Assume not complete; show wizard
      return { should_show_wizard: true };
    }
  }

  showPathSelection() {
    this.hideAll();
    document.getElementById("onboarding-path-selection").style.display = "block";
  }

  hideAll() {
    document.getElementById("onboarding-path-selection").style.display = "none";
    document.getElementById("onboarding-easy-mode").style.display = "none";
    document.getElementById("onboarding-custom-mode").style.display = "none";
    document.getElementById("onboarding-power-user").style.display = "none";
  }

  bindPathButtons() {
    // Path A: Easy Mode
    document.getElementById("path-easy-btn")?.addEventListener("click", () => {
      this.currentPath = "easy";
      this.showEasyMode();
    });

    // Path B: Custom Setup
    document.getElementById("path-custom-btn")?.addEventListener("click", () => {
      this.currentPath = "custom";
      this.showCustomStep(0);
    });

    // Path C: Power User
    document.getElementById("path-power-user-btn")?.addEventListener("click", () => {
      this.currentPath = "power";
      this.showPowerUser();
    });

    // Skip button (applies Easy Mode defaults)
    document.getElementById("onboarding-skip-btn")?.addEventListener("click", () => {
      this.completeOnboarding();
    });
  }

  // ── EASY MODE ──

  showEasyMode() {
    this.hideAll();
    document.getElementById("onboarding-easy-mode").style.display = "block";
    document.querySelector('input[name="easy-preset"]')?.focus();
  }

  bindStepButtons() {
    // Easy Mode
    document.getElementById("onboarding-easy-complete-btn")?.addEventListener("click", () => {
      const preset = document.querySelector('input[name="easy-preset"]:checked')?.value
        || "casual";
      this.completeWithPreset(preset);
    });

    document.getElementById("onboarding-easy-back-btn")?.addEventListener("click", () => {
      this.showPathSelection();
    });

    // Custom Mode — Preset step
    document.getElementById("onboarding-custom-preset-next-btn")?.addEventListener("click", () => {
      this.customStepIndex = 1;
      this.showCustomStep(1);
    });

    document.getElementById("onboarding-custom-preset-skip-btn")?.addEventListener("click", () => {
      this.customStepIndex = 1;
      this.showCustomStep(1);
    });

    // Custom Mode — AI step
    document.getElementById("onboarding-custom-ai-next-btn")?.addEventListener("click", () => {
      this.customStepIndex = 2;
      this.showCustomStep(2);
    });

    document.getElementById("onboarding-custom-ai-back-btn")?.addEventListener("click", () => {
      this.customStepIndex = 0;
      this.showCustomStep(0);
    });

    // Custom Mode — Privacy step
    document.getElementById("onboarding-custom-privacy-next-btn")?.addEventListener("click", () => {
      this.customStepIndex = 3;
      this.showCustomStep(3);
    });

    document.getElementById("onboarding-custom-privacy-back-btn")?.addEventListener("click", () => {
      this.customStepIndex = 1;
      this.showCustomStep(1);
    });

    // Custom Mode — Output step
    document.getElementById("onboarding-custom-output-next-btn")?.addEventListener("click", () => {
      this.customStepIndex = 4;
      this.showCustomStep(4);
    });

    document.getElementById("onboarding-custom-output-back-btn")?.addEventListener("click", () => {
      this.customStepIndex = 2;
      this.showCustomStep(2);
    });

    // Custom Mode — Overlay step
    document.getElementById("onboarding-custom-complete-btn")?.addEventListener("click", () => {
      this.completeCustomSetup();
    });

    document.getElementById("onboarding-custom-overlay-back-btn")?.addEventListener("click", () => {
      this.customStepIndex = 3;
      this.showCustomStep(3);
    });

    // Power User
    document.getElementById("onboarding-power-user-settings-btn")?.addEventListener("click", () => {
      this.powerUserSeen.settings = true;
      this.updatePowerUserProgress();
      // In a real app, navigate to /settings; here we simulate
      window.location.hash = "#/settings";
    });

    document.getElementById("onboarding-power-user-privacy-btn")?.addEventListener("click", () => {
      this.powerUserSeen.privacy = true;
      this.updatePowerUserProgress();
      // In a real app, navigate to /privacy
      window.location.hash = "#/privacy";
    });

    document.getElementById("onboarding-power-user-complete-btn")?.addEventListener("click", () => {
      this.completeOnboarding();
    });
  }

  showCustomStep(stepIndex) {
    const steps = [
      "onboarding-custom-preset",
      "onboarding-custom-ai",
      "onboarding-custom-privacy",
      "onboarding-custom-output",
      "onboarding-custom-overlay",
    ];

    this.hideAll();
    document.getElementById("onboarding-custom-mode").style.display = "block";

    // Hide all steps
    steps.forEach((stepId) => {
      const el = document.getElementById(stepId);
      if (el) el.style.display = "none";
    });

    // Show current step
    const currentStepId = steps[stepIndex];
    if (currentStepId) {
      document.getElementById(currentStepId).style.display = "block";
    }
  }

  completeWithPreset(preset) {
    this.savePreset(preset).then(() => {
      this.completeOnboarding();
    });
  }

  async completeCustomSetup() {
    const preset = document.querySelector('input[name="custom-preset"]:checked')?.value
      || "casual";
    const aiProvider = document.querySelector('input[name="custom-ai"]:checked')?.value
      || "null";
    const overlayAnchor = document.querySelector('input[name="custom-overlay"]:checked')?.value
      || "center";

    // Save privacy toggles
    const toggles = document.querySelectorAll(".privacy-toggle:checked");
    for (const toggle of toggles) {
      const key = toggle.dataset.toggle;
      await this.setPrivacyToggle(key, true);
    }

    // Save settings
    await this.saveSettings({
      preset,
      ai_provider: aiProvider,
      overlay: {
        anchor: overlayAnchor,
      },
    });

    this.completeOnboarding();
  }

  updatePowerUserProgress() {
    const settingsCheck = document.getElementById("power-user-settings-check");
    const privacyCheck = document.getElementById("power-user-privacy-check");
    const completeBtn = document.getElementById("onboarding-power-user-complete-btn");

    if (settingsCheck && this.powerUserSeen.settings) {
      settingsCheck.textContent = "✓ Settings opened";
    }
    if (privacyCheck && this.powerUserSeen.privacy) {
      privacyCheck.textContent = "✓ Privacy opened";
    }

    // Enable complete button only if both are seen
    if (completeBtn) {
      completeBtn.disabled = !(this.powerUserSeen.settings && this.powerUserSeen.privacy);
    }
  }

  showPowerUser() {
    this.hideAll();
    document.getElementById("onboarding-power-user").style.display = "block";
  }

  // ── API CALLS ──

  async savePreset(preset) {
    try {
      const res = await fetch(`${this.apiBase}/week13/settings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ preset }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.error("Failed to save preset:", err);
    }
  }

  async setPrivacyToggle(key, enabled) {
    try {
      const res = await fetch(`${this.apiBase}/week13/privacy/toggles/${key}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.error(`Failed to set privacy toggle ${key}:`, err);
    }
  }

  async saveSettings(settings) {
    try {
      const res = await fetch(`${this.apiBase}/week13/settings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.error("Failed to save settings:", err);
    }
  }

  async completeOnboarding() {
    try {
      const res = await fetch(`${this.apiBase}/week13/onboarding/complete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      // Hide onboarding and navigate to dashboard
      document.getElementById("onboarding-container").style.display = "none";
      window.location.hash = "#/dashboard";
    } catch (err) {
      console.error("Failed to complete onboarding:", err);
    }
  }
}

// Initialize on page load
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    new OnboardingController();
  });
} else {
  new OnboardingController();
}
