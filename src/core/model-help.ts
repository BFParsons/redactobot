/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Works out why Chrome's on-device model is not available to a
 * visitor, so the app can say what still works and how to get the model. The
 * model (Gemini Nano) exists only in recent desktop Chrome on capable hardware.
 */

/** Chrome's answer about the on-device model, or that the API is missing. */
export type ModelStatus =
  | 'available'
  | 'downloadable'
  | 'downloading'
  | 'unavailable'
  | 'unsupported'
  | 'unresponsive';

/** Why the model cannot be used right now. */
export type ModelGap =
  /** Firefox, Safari, Edge or another browser without the built-in model. */
  | 'other-browser'
  /** A phone or tablet. */
  | 'mobile'
  /** Chrome, but older than the first version with the model. */
  | 'old-chrome'
  /** Recent desktop Chrome, yet the feature is switched off. */
  | 'switched-off'
  /** Chrome has the feature but this computer cannot run the model. */
  | 'hardware'
  /** The model has not been downloaded yet. */
  | 'download'
  /** Chrome has the feature but is not answering right now. */
  | 'not-responding';

/** The first Chrome version Redactobot supports. */
export const MIN_CHROME = 148;

/** What the app tells a visitor who cannot use the on-device model. */
export interface ModelHelp {
  gap: ModelGap;
  /** The browser's name as shown to the visitor, for example "Firefox". */
  browser: string;
}

function browserName(ua: string): string {
  if (/\bEdg(?:e|A|iOS)?\//.test(ua)) return 'Microsoft Edge';
  if (/\bOPR\/|\bOpera\b/.test(ua)) return 'Opera';
  if (/\bFirefox\/|\bFxiOS\//.test(ua)) return 'Firefox';
  if (/\bSamsungBrowser\//.test(ua)) return 'Samsung Internet';
  if (/\bChrome\/|\bCriOS\//.test(ua)) return 'Chrome';
  if (/\bSafari\//.test(ua)) return 'Safari';
  return 'This browser';
}

/**
 * Why the model is unavailable, or undefined when it is available. `ua` is the
 * browser's user-agent string.
 */
export function modelHelp(
  status: ModelStatus,
  ua: string,
): ModelHelp | undefined {
  if (status === 'available') return undefined;
  const browser = browserName(ua);
  if (status === 'downloadable' || status === 'downloading') {
    return {gap: 'download', browser};
  }
  if (status === 'unresponsive') return {gap: 'not-responding', browser};
  if (/\bAndroid\b|\biPhone\b|\biPad\b|\bMobile\b/.test(ua)) {
    return {gap: 'mobile', browser};
  }
  if (status === 'unavailable') return {gap: 'hardware', browser};
  if (browser !== 'Chrome') return {gap: 'other-browser', browser};
  const version = Number(/\bChrome\/(\d+)/.exec(ua)?.[1] ?? 0);
  return {gap: version < MIN_CHROME ? 'old-chrome' : 'switched-off', browser};
}
