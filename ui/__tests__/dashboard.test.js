import { describe, it, expect, beforeEach } from 'vitest';
import '../views/dashboard.js';

const renderCargo = globalThis.__dashboardExports?.renderCargo;

describe('renderCargo', () => {
  beforeEach(() => {
    document.body.innerHTML =
      '<ul id="dash-cargo-count"></ul>' +
      '<ul id="dash-cargo-list"></ul>';
  });

  it('renders No cargo detected placeholder when inventory is empty', () => {
    renderCargo({}, []);
    const list = document.getElementById('dash-cargo-list');
    const li = list.querySelector('li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('No cargo detected');
    expect(li.className).toBe('field-value unknown');
  });

  it('renders malicious cargo name as literal text, not HTML', () => {
    renderCargo({}, [{ name: '<img src=x onerror=alert(1)>', count: 1 }]);
    const list = document.getElementById('dash-cargo-list');
    expect(list.querySelector('img')).toBeNull();
    const nameSpan = list.querySelector('.field-label');
    expect(nameSpan.textContent).toBe('<img src=x onerror=alert(1)>');
  });

  it('renders cargo count as text and preserves field-value class', () => {
    renderCargo({}, [{ name: 'Gold', count: 42 }]);
    const list = document.getElementById('dash-cargo-list');
    const countSpan = list.querySelector('.field-value');
    expect(countSpan).not.toBeNull();
    expect(countSpan.textContent).toBe('42');
  });

  it('preserves field-row, field-label, and field-value classes on cargo items', () => {
    renderCargo({}, [{ name: 'Tritium', count: 10 }]);
    const list = document.getElementById('dash-cargo-list');
    const li = list.querySelector('li');
    expect(li.className).toBe('field-row');
    expect(li.querySelector('.field-label')).not.toBeNull();
    expect(li.querySelector('.field-value')).not.toBeNull();
  });
});
