import { describe, it, expect, beforeEach } from 'vitest';
import { escapeHtml, setSafeText, appendTextChild } from '../utils/safe-dom.js';

describe('escapeHtml', () => {
  it('encodes script tags', () => {
    expect(escapeHtml('<script>alert("xss")</script>')).toBe('&lt;script&gt;alert("xss")&lt;/script&gt;');
  });

  it('encodes ampersands and img onerror payloads', () => {
    const result = escapeHtml('<img src=x onerror=alert(1)> & foo');
    expect(result).toContain('&lt;img');
    expect(result).toContain('&amp;');
    expect(result).not.toContain('<img');
  });

  it('returns empty string for null and undefined', () => {
    expect(escapeHtml(null)).toBe('');
    expect(escapeHtml(undefined)).toBe('');
  });

  it('coerces numbers to string', () => {
    expect(escapeHtml(0)).toBe('0');
    expect(escapeHtml(42)).toBe('42');
  });
});

describe('setSafeText', () => {
  it('sets text content without HTML parsing', () => {
    const el = document.createElement('div');
    setSafeText(el, '<b>bold</b>');
    expect(el.textContent).toBe('<b>bold</b>');
    expect(el.querySelector('b')).toBeNull();
  });
});

describe('appendTextChild', () => {
  it('appends child with correct tag, class, and text without HTML parsing', () => {
    const parent = document.createElement('ul');
    const child = appendTextChild(parent, 'li', '<script>xss</script>', 'item-class');
    expect(child.tagName.toLowerCase()).toBe('li');
    expect(child.className).toBe('item-class');
    expect(child.textContent).toBe('<script>xss</script>');
    expect(child.querySelector('script')).toBeNull();
    expect(parent.children.length).toBe(1);
  });
});
