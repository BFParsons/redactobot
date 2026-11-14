/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Reads colours and typography from a chat site's composer so
 * that the extension's controls match the page, with a fixed palette per site
 * as the fallback.
 */

import type {Site, Theme} from './protocol';

const palettes: Record<
  Site,
  {light: string[]; dark: string[]; radius: string}
> = {
  chatgpt: {
    light: ['#ffffff', '#171717', '#686868', '#dedede', '#171717', '#ffffff'],
    dark: ['#2f2f2f', '#f5f5f5', '#b4b4b4', '#4b4b4b', '#f5f5f5', '#171717'],
    radius: '18px',
  },
  claude: {
    light: ['#faf9f5', '#30302e', '#73726b', '#deddd5', '#c96442', '#ffffff'],
    dark: ['#30302e', '#eeede8', '#b6b5ae', '#4b4b46', '#d97757', '#1c1b19'],
    radius: '12px',
  },
  gemini: {
    light: ['#f0f4f9', '#1f1f1f', '#5f6368', '#d7dbe0', '#0b57d0', '#ffffff'],
    dark: ['#282a2c', '#e3e3e3', '#c4c7c5', '#444746', '#a8c7fa', '#062e6f'],
    radius: '24px',
  },
};
function rgb(value: string): number[] | undefined {
  if (/^#[\da-f]{6}$/i.test(value)) {
    return [1, 3, 5].map(at => parseInt(value.slice(at, at + 2), 16));
  }
  const m = value.match(
    /^rgba?\(\s*([\d.]+)[, ]+([\d.]+)[, ]+([\d.]+)(?:\s*[,/]\s*([\d.]+))?\s*\)$/,
  );
  if (m) {
    return m[4] != null && Number(m[4]) < 0.85
      ? undefined
      : m.slice(1, 4).map(Number);
  }
  // Modern site styles can compute to oklch(), lab() or color(srgb ...).
  if (/^(oklch|oklab|lab|lch|color)\(/.test(value)) {
    const canvas = document.createElement('canvas');
    canvas.height = 1;
    canvas.width = 1;
    const context = canvas.getContext('2d', {willReadFrequently: true});
    if (context) {
      context.fillStyle = value;
      context.fillRect(0, 0, 1, 1);
      const pixel = context.getImageData(0, 0, 1, 1).data;
      if (pixel[3] >= 217) return [...pixel.slice(0, 3)];
    }
  }
  return;
}
const tokens: Record<
  Site,
  {muted: string[]; border: string[]; accent: string[]}
> = {
  chatgpt: {
    muted: ['--text-secondary', '--text-tertiary'],
    border: ['--border-light', '--border-default'],
    accent: ['--text-primary'],
  },
  claude: {
    muted: ['--text-400', '--text-500'],
    border: ['--border-300', '--border-200'],
    accent: ['--accent-main-100'],
  },
  gemini: {
    muted: [
      '--gem-sys-color--on-surface-variant',
      '--sys-color-on-surface-variant',
    ],
    border: ['--gem-sys-color--outline-variant', '--sys-color-outline-variant'],
    accent: ['--gem-sys-color--primary', '--sys-color-primary'],
  },
};
function colorToken(
  style: CSSStyleDeclaration,
  names: string[],
): string | undefined {
  const probe = document.createElement('span');
  for (const name of names) {
    const raw = style.getPropertyValue(name).trim();
    if (!raw || raw.includes('var(')) continue;
    // Some sites store HSL/RGB channels in tokens, others store complete
    // colors.
    for (const color of [raw, `hsl(${raw})`, `rgb(${raw})`]) {
      probe.style.color = '';
      probe.style.color = color;
      if (
        probe.style.color &&
        probe.style.color !== 'transparent' &&
        probe.style.color !== 'currentcolor'
      ) {
        return probe.style.color;
      }
    }
  }
}
function placeholderColor(composer: HTMLElement): string | undefined {
  if (typeof CSS === 'undefined' || !CSS.supports('selector(::placeholder)')) {
    return;
  }
  const node =
    composer instanceof HTMLTextAreaElement
      ? composer
      : composer.querySelector<HTMLElement>('[data-placeholder]') || composer;
  const style = getComputedStyle(
    node,
    composer instanceof HTMLTextAreaElement ? '::placeholder' : '::before',
  );
  if (
    !(composer instanceof HTMLTextAreaElement) &&
    (!style.content || ['none', 'normal', '""'].includes(style.content))
  ) {
    return;
  }
  return rgb(style.color) ? style.color : undefined;
}
/**
 * Builds a theme from the computed styles of the composer and its ancestors,
 * using the site's palette for any value it cannot read.
 */
export function themeFor(site: Site, composer: HTMLElement): Theme {
  let surface: string | undefined;
  let radius: string | undefined;
  let border: string | undefined;
  let node: HTMLElement | null = composer;
  while (node) {
    const computed = getComputedStyle(node);
    if (parseFloat(computed.borderRadius) > 0) radius ??= computed.borderRadius;
    if (
      parseFloat(computed.borderTopWidth) > 0 &&
      rgb(computed.borderTopColor)
    ) {
      border ??= computed.borderTopColor;
    }
    const color = computed.backgroundColor;
    if (rgb(color)) {
      surface = color;
      break;
    }
    node = node.parentElement;
  }
  const channels = surface ? rgb(surface) : undefined;
  const root = document.documentElement;
  const declared =
    root.dataset.theme ||
    root.dataset.mode ||
    root.dataset.colorScheme ||
    getComputedStyle(root).colorScheme;
  const dark = channels
    ? channels[0] * 0.2126 + channels[1] * 0.7152 + channels[2] * 0.0722 < 130
    : declared === 'dark' ||
      (declared !== 'light' &&
        (root.classList.contains('dark') ||
          matchMedia('(prefers-color-scheme: dark)').matches));
  const p = palettes[site][dark ? 'dark' : 'light'];
  const style = getComputedStyle(composer);
  const accent = colorToken(style, tokens[site].accent) || p[4];
  const accentRGB = rgb(accent);
  const onAccent = accentRGB
    ? accentRGB[0] * 0.2126 + accentRGB[1] * 0.7152 + accentRGB[2] * 0.0722 <
      140
      ? '#ffffff'
      : '#171717'
    : p[5];
  return {
    site,
    dark,
    surface: surface || p[0],
    text: rgb(style.color) ? style.color : p[1],
    muted:
      colorToken(style, tokens[site].muted) ||
      placeholderColor(composer) ||
      p[2],
    border: border || colorToken(style, tokens[site].border) || p[3],
    accent,
    onAccent,
    radius: radius || palettes[site].radius,
    font: style.fontFamily || 'system-ui, sans-serif',
    fontSize: style.fontSize || '16px',
    fontWeight: style.fontWeight || '400',
    fontStyle: style.fontStyle || 'normal',
    lineHeight:
      style.lineHeight === 'normal' || !style.lineHeight
        ? '1.5'
        : style.lineHeight,
    letterSpacing: style.letterSpacing || 'normal',
  };
}
/**
 * Sets the theme's values as `--rb-*` custom properties on `element` and sets
 * its colour scheme.
 */
export function applyTheme(element: HTMLElement, theme: Theme) {
  for (const key of [
    'surface',
    'text',
    'muted',
    'border',
    'accent',
    'onAccent',
    'radius',
    'font',
    'fontSize',
    'fontWeight',
    'fontStyle',
    'lineHeight',
    'letterSpacing',
  ] as const) {
    element.style.setProperty(`--rb-${key}`, theme[key]);
  }
  element.style.colorScheme = theme.dark ? 'dark' : 'light';
}
/** Returns the site's fixed light or dark palette with default typography. */
export function fallbackTheme(site: Site, dark: boolean): Theme {
  const p = palettes[site][dark ? 'dark' : 'light'];
  return {
    site,
    dark,
    surface: p[0],
    text: p[1],
    muted: p[2],
    border: p[3],
    accent: p[4],
    onAccent: p[5],
    radius: palettes[site].radius,
    font: 'system-ui, sans-serif',
    fontSize: '16px',
    fontWeight: '400',
    fontStyle: 'normal',
    lineHeight: '1.5',
    letterSpacing: 'normal',
  };
}
