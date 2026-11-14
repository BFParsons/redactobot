/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {beforeEach, describe, expect, it, vi} from 'vitest';
import {themeFor, applyTheme} from './themes';
beforeEach(() => {
  document.body.innerHTML = '<main><textarea></textarea></main>';
  document.documentElement.removeAttribute('class');
  document.documentElement.removeAttribute('style');
  document.documentElement.removeAttribute('data-theme');
  vi.stubGlobal(
    'matchMedia',
    vi.fn(() => ({matches: false})),
  );
});
describe.each(['chatgpt', 'claude', 'gemini'] as const)('%s themes', site => {
  it.each([false, true])(
    'follows the actual composer surface, dark=%s, independently of the OS',
    dark => {
      vi.stubGlobal(
        'matchMedia',
        vi.fn(() => ({matches: !dark})),
      );
      const parent = document.querySelector('main')!;
      parent.style.backgroundColor = dark
        ? 'rgb(35, 35, 35)'
        : 'rgb(250, 250, 245)';
      const composer = document.querySelector('textarea')!;
      composer.style.backgroundColor = 'transparent';
      composer.style.color = dark ? 'rgb(240, 240, 240)' : 'rgb(30, 30, 30)';
      composer.style.fontFamily = 'Georgia';
      const theme = themeFor(site, composer);
      expect(theme.dark).toBe(dark);
      expect(theme.surface).toBe(parent.style.backgroundColor);
      expect(theme.font).toBe('Georgia');
      const panel = document.createElement('div');
      applyTheme(panel, theme);
      expect(panel.style.colorScheme).toBe(dark ? 'dark' : 'light');
      expect(panel.style.getPropertyValue('--rb-text')).toBe(
        composer.style.color,
      );
    },
  );
  it('updates an existing panel when the site switches modes', () => {
    const composer = document.querySelector('textarea')!;
    const panel = document.createElement('div');
    composer.style.backgroundColor = 'white';
    applyTheme(panel, themeFor(site, composer));
    expect(panel.style.colorScheme).toBe('light');
    composer.style.backgroundColor = '#202020';
    applyTheme(panel, themeFor(site, composer));
    expect(panel.style.colorScheme).toBe('dark');
  });
  it('uses the editor typography and the service text token', () => {
    const composer = document.querySelector('textarea')!;
    composer.style.cssText =
      'font-family:Georgia;font-size:18px;font-weight:500;font-style:italic;line-height:28px;letter-spacing:0.2px';
    const token = {
      chatgpt: '--text-secondary',
      claude: '--text-400',
      gemini: '--gem-sys-color--on-surface-variant',
    }[site];
    composer.style.setProperty(token, '#445566');
    const theme = themeFor(site, composer);
    const panel = document.createElement('div');
    applyTheme(panel, theme);
    expect(theme.muted).toBe('rgb(68, 85, 102)');
    expect(panel.style.getPropertyValue('--rb-fontSize')).toBe('18px');
    expect(panel.style.getPropertyValue('--rb-fontWeight')).toBe('500');
    expect(panel.style.getPropertyValue('--rb-fontStyle')).toBe('italic');
    expect(panel.style.getPropertyValue('--rb-lineHeight')).toBe('28px');
    expect(panel.style.getPropertyValue('--rb-letterSpacing')).toBe('0.2px');
  });
});
