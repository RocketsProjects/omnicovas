import { describe, it, expect, beforeEach, vi } from 'vitest';
import '../views/onboarding.js';

const { OnboardingController, _initOnboarding } = globalThis.__onboardingExports ?? {};

const FULL_DOM = `
  <div id="onboarding-container" style="display:none">
    <div id="onboarding-path-selection" style="display:none"></div>
    <div id="onboarding-easy-mode" style="display:none"></div>
    <div id="onboarding-custom-mode" style="display:none"></div>
    <div id="onboarding-power-user" style="display:none">
      <span id="power-user-settings-check">☐ Settings opened</span>
      <span id="power-user-privacy-check">☐ Privacy opened</span>
      <button id="onboarding-power-user-complete-btn" disabled></button>
    </div>
  </div>
`;

describe('OnboardingController', () => {
  it('is exported via test hook', () => {
    expect(OnboardingController).toBeDefined();
    expect(typeof OnboardingController).toBe('function');
  });

  it('_initOnboarding is exported via test hook', () => {
    expect(_initOnboarding).toBeDefined();
    expect(typeof _initOnboarding).toBe('function');
  });
});

describe('OnboardingController.show', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = FULL_DOM;
    ctrl = Object.create(OnboardingController.prototype);
    ctrl.powerUserSeen = { settings: false, privacy: false };
    ctrl.customStepIndex = 0;
  });

  it('sets container display to flex', () => {
    ctrl.show();
    const container = document.getElementById('onboarding-container');
    expect(container.style.display).toBe('flex');
  });

  it('makes path selection panel visible', () => {
    ctrl.show();
    const pathSel = document.getElementById('onboarding-path-selection');
    expect(pathSel.style.display).toBe('block');
  });

  it('hides easy-mode panel', () => {
    ctrl.show();
    const easy = document.getElementById('onboarding-easy-mode');
    expect(easy.style.display).toBe('none');
  });
});

describe('OnboardingController.completeOnboarding', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = '<div id="onboarding-container" style="display:flex"></div>';
    ctrl = Object.create(OnboardingController.prototype);
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ status: 'ok' }),
    });
  });

  it('calls the complete endpoint', async () => {
    await ctrl.completeOnboarding();
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/week13/onboarding/complete'),
      expect.objectContaining({ method: 'POST' })
    );
  });

  it('hides container after successful completion', async () => {
    await ctrl.completeOnboarding();
    const container = document.getElementById('onboarding-container');
    expect(container.style.display).toBe('none');
  });
});

describe('OnboardingController path routing', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = FULL_DOM;
    ctrl = Object.create(OnboardingController.prototype);
    ctrl.powerUserSeen = { settings: false, privacy: false };
    ctrl.customStepIndex = 0;
  });

  it('showPathSelection hides all sub-panels', () => {
    document.getElementById('onboarding-easy-mode').style.display = 'block';
    ctrl.showPathSelection();
    expect(document.getElementById('onboarding-easy-mode').style.display).toBe('none');
    expect(document.getElementById('onboarding-path-selection').style.display).toBe('block');
  });

  it('showEasyMode shows easy-mode panel', () => {
    ctrl.showEasyMode();
    expect(document.getElementById('onboarding-easy-mode').style.display).toBe('block');
    expect(document.getElementById('onboarding-path-selection').style.display).toBe('none');
  });

  it('showPowerUser shows power-user panel', () => {
    ctrl.showPowerUser();
    expect(document.getElementById('onboarding-power-user').style.display).toBe('block');
  });
});

describe('OnboardingController.updatePowerUserProgress', () => {
  let ctrl;

  beforeEach(() => {
    document.body.innerHTML = FULL_DOM;
    ctrl = Object.create(OnboardingController.prototype);
    ctrl.powerUserSeen = { settings: false, privacy: false };
  });

  it('complete button stays disabled when neither page visited', () => {
    ctrl.updatePowerUserProgress();
    const btn = document.getElementById('onboarding-power-user-complete-btn');
    expect(btn.disabled).toBe(true);
  });

  it('complete button stays disabled when only settings visited', () => {
    ctrl.powerUserSeen.settings = true;
    ctrl.updatePowerUserProgress();
    const btn = document.getElementById('onboarding-power-user-complete-btn');
    expect(btn.disabled).toBe(true);
  });

  it('complete button is enabled when both pages visited', () => {
    ctrl.powerUserSeen.settings = true;
    ctrl.powerUserSeen.privacy = true;
    ctrl.updatePowerUserProgress();
    const btn = document.getElementById('onboarding-power-user-complete-btn');
    expect(btn.disabled).toBe(false);
  });

  it('settings check renders as literal text, not HTML', () => {
    ctrl.powerUserSeen.settings = true;
    ctrl.updatePowerUserProgress();
    const el = document.getElementById('power-user-settings-check');
    expect(el.textContent).toBe('✓ Settings opened');
    expect(el.querySelector('script')).toBeNull();
    expect(el.querySelector('img')).toBeNull();
  });

  it('privacy check renders as literal text, not HTML', () => {
    ctrl.powerUserSeen.privacy = true;
    ctrl.updatePowerUserProgress();
    const el = document.getElementById('power-user-privacy-check');
    expect(el.textContent).toBe('✓ Privacy opened');
    expect(el.querySelector('script')).toBeNull();
    expect(el.querySelector('img')).toBeNull();
  });
});

describe('_initOnboarding pending flag drain', () => {
  it('drains __pendingOnboardingShow flag and shows wizard', () => {
    document.body.innerHTML = FULL_DOM;
    window.__pendingOnboardingShow = true;
    _initOnboarding();
    expect(window.__pendingOnboardingShow).toBe(false);
    const container = document.getElementById('onboarding-container');
    expect(container.style.display).toBe('flex');
  });

  it('does not show wizard when pending flag is false', () => {
    document.body.innerHTML = FULL_DOM;
    window.__pendingOnboardingShow = false;
    _initOnboarding();
    const container = document.getElementById('onboarding-container');
    expect(container.style.display).toBe('none');
  });

  it('exposes window.OmniOnboarding.show as a function', () => {
    document.body.innerHTML = FULL_DOM;
    _initOnboarding();
    expect(typeof window.OmniOnboarding?.show).toBe('function');
  });
});
