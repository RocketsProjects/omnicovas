import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import '../components/confirmation-gate.js';

const { ConfirmationGateComponent } = globalThis.__confirmationGateExports ?? {};

describe('ConfirmationGateComponent — bridge readiness', () => {
  let gate;

  beforeEach(() => {
    gate = new ConfirmationGateComponent();
    delete window.Shell;
    delete window.OMNICOVAS_PORT;
  });

  afterEach(() => {
    delete window.Shell;
    delete window.OMNICOVAS_PORT;
  });

  it('apiBase returns null when no bridge globals are set', () => {
    expect(gate.apiBase).toBeNull();
  });

  it('apiUrl returns null when bridge is not ready', () => {
    expect(gate.apiUrl('/week13/confirmations/pending')).toBeNull();
  });

  it('apiBase returns Shell.httpBase when available', () => {
    window.Shell = { httpBase: 'http://127.0.0.1:7654' };
    expect(gate.apiBase).toBe('http://127.0.0.1:7654');
  });

  it('apiBase uses OMNICOVAS_PORT when Shell.httpBase is absent', () => {
    window.OMNICOVAS_PORT = '9876';
    expect(gate.apiBase).toBe('http://127.0.0.1:9876');
  });

  it('apiUrl builds correct URL from OMNICOVAS_PORT', () => {
    window.OMNICOVAS_PORT = '9876';
    expect(gate.apiUrl('/week13/confirmations/pending')).toBe(
      'http://127.0.0.1:9876/week13/confirmations/pending'
    );
  });

  it('apiUrl never contains :8000', () => {
    window.OMNICOVAS_PORT = '9876';
    expect(gate.apiUrl('/week13/confirmations/pending')).not.toContain(':8000');
  });

  it('fetchPending does not call fetch when bridge is not ready', async () => {
    global.fetch = vi.fn();
    await gate.fetchPending();
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('respond does not call fetch when bridge is not ready', async () => {
    global.fetch = vi.fn();
    await gate.respond('abc123', 'confirm');
    expect(global.fetch).not.toHaveBeenCalled();
  });
});

describe('ConfirmationGateComponent — safe why_text rendering', () => {
  let gate;
  let container;

  beforeEach(() => {
    document.body.innerHTML = '<div id="gate-container"></div>';
    container = document.getElementById('gate-container');
    gate = new ConfirmationGateComponent();
    gate.containerEl = container;
    container.className = 'confirmation-gate-container';
  });

  function renderCard(whyText) {
    const conf = {
      suggestion_text: 'Test suggestion',
      why_text: whyText,
      timeout_at: null,
    };
    const card = gate.createConfirmationCard('test-id', conf);
    container.appendChild(card);
    return card;
  }

  it('renders malicious <img> why_text as literal text, no img element injected', () => {
    renderCard('<img src=x onerror=alert(1)>');
    expect(container.querySelector('img')).toBeNull();
    const small = container.querySelector('small');
    expect(small).not.toBeNull();
    expect(small.textContent).toBe('<img src=x onerror=alert(1)>');
  });

  it('renders malicious <script> why_text as literal text, no script element injected', () => {
    renderCard('<script>alert(1)<\/script>');
    expect(container.querySelector('script')).toBeNull();
    const small = container.querySelector('small');
    expect(small).not.toBeNull();
    expect(small.textContent).toBe('<script>alert(1)</script>');
  });

  it('renders fallback text when why_text is null', () => {
    renderCard(null);
    const small = container.querySelector('small');
    expect(small).not.toBeNull();
    expect(small.textContent).toBe('See docs/ai/phase4_advisories.md');
  });

  it('renders fallback text when why_text is empty string', () => {
    renderCard('');
    const small = container.querySelector('small');
    expect(small).not.toBeNull();
    expect(small.textContent).toBe('See docs/ai/phase4_advisories.md');
  });

  it('preserves p.confirmation-why-placeholder with correct id and hidden by default', () => {
    renderCard('test text');
    const p = container.querySelector('p.confirmation-why-placeholder');
    expect(p).not.toBeNull();
    expect(p.id).toBe('confirmation-why-test-id');
    expect(p.style.display).toBe('none');
  });

  it('contains em, br, and small children in correct order', () => {
    renderCard('test text');
    const p = container.querySelector('p.confirmation-why-placeholder');
    const children = p.childNodes;
    expect(children[0].tagName).toBe('EM');
    expect(children[1].tagName).toBe('BR');
    expect(children[2].tagName).toBe('SMALL');
  });

  it('em element contains Tier 3 explainability text', () => {
    renderCard('test text');
    const em = container.querySelector('em');
    expect(em.textContent).toBe('Tier 3 explainability coming in Phase 4+.');
  });

  it('clicking Why? toggle reveals the placeholder', () => {
    renderCard('test text');
    const btn = container.querySelector('.confirmation-why-btn');
    expect(btn).not.toBeNull();
    const p = document.getElementById('confirmation-why-test-id');
    expect(p.style.display).toBe('none');
    btn.click();
    expect(p.style.display).toBe('block');
  });

  it('clicking Why? toggle twice hides the placeholder again', () => {
    renderCard('test text');
    const btn = container.querySelector('.confirmation-why-btn');
    btn.click();
    btn.click();
    const p = document.getElementById('confirmation-why-test-id');
    expect(p.style.display).toBe('none');
  });
});
