/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Types, limits and helpers shared by the extension's background,
 * content, offscreen and review contexts.
 */

import type {Detection} from '../core/redact';
import type {PrivacyBucket} from '../core/privacy-buckets';
import type {PasteCategory} from './categories';

/** A chat site the extension supports. */
export type Site = 'chatgpt' | 'claude' | 'gemini';
/** A detection plus its review reason and privacy bucket, when set. */
export interface Finding extends Detection {
  /** Why the user should check this finding before pasting. */
  reviewReason?: string;
  bucket?: PrivacyBucket;
}
/** An excerpt that the model, or a rule, could not classify with confidence. */
export interface Ambiguous {
  /** The excerpt, as it appears in the scanned text. */
  text: string;
  /** User-facing explanation of the doubt. */
  reason: string;
  /** Model kind, such as `person`; absent when the doubt has no category. */
  kind?: string;
}
/** The result of scanning one paste. */
export interface ScanReport {
  findings: Finding[];
  /** The text with every finding replaced by its placeholder. */
  cleaned: string;
  /** Placeholder for each finding, keyed by finding id. */
  replacements: Record<string, string>;
  /**
   * True when the scan is incomplete, a reason was recorded or any finding has
   * a review reason.
   */
  needsReview: boolean;
  /** User-facing reasons for review that are not tied to one finding. */
  reasons: string[];
  /** False when the scan did not finish. */
  complete: boolean;
  /** Stage-one output; eligible sensitive facts may remain. */
  cloudText?: string;
  /** Scope actually checked. Omitted only by legacy full-scope callers. */
  categories?: readonly PasteCategory[];
}
/**
 * Colours and typography taken from a chat site so that the extension's UI
 * matches it. Values are CSS strings.
 */
export interface Theme {
  site: Site;
  dark: boolean;
  /** Background colour. */
  surface: string;
  text: string;
  /** Colour of secondary text. */
  muted: string;
  border: string;
  accent: string;
  /** Text colour for use on top of `accent`. */
  onAccent: string;
  font: string;
  radius: string;
  fontSize: string;
  fontWeight: string;
  fontStyle: string;
  lineHeight: string;
  letterSpacing: string;
}
/**
 * A value handed over by an untyped boundary: a `chrome.*` API result (the
 * project carries no `@types/chrome`), a runtime message from another
 * extension context, or JSON parsed from the on-device model. Each handler
 * checks the fields it reads.
 *
 * Every `any` in the extension goes through this one alias so that the
 * remaining untyped surface can be found and narrowed in one place.
 */
// oxlint-disable-next-line typescript/no-explicit-any -- documented above.
export type Untyped = any;

/** The parts of `chrome.runtime.Port` that the extension uses. */
export interface RuntimePort {
  name: string;
  sender?: {id?: string; url?: string; tab?: {id?: number}; frameId?: number};
  postMessage(message: Untyped): void;
  disconnect(): void;
  onMessage: {addListener(fn: (message: Untyped) => void): void};
  onDisconnect: {addListener(fn: () => void): void};
}
/**
 * The `chrome` extension API. Chrome is supplied by the browser, not by a
 * remotely loaded library.
 */
export const browser = (globalThis as unknown as {chrome: Untyped}).chrome;
/** Longest paste, in characters, that the extension will scan. */
export const MAX_PASTE = 100_000;
/**
 * Waking a model Chrome unloaded while idle (measured 1-3+ minutes). Startup,
 * not a scan timeout.
 */
export const WAKE_BUDGET_MS = 300_000;
/**
 * Returns the time allowed for scanning `text`, in milliseconds: 15 seconds per
 * 840 words, between 30 seconds and 3 minutes. Covers waiting, model startup
 * and all local work; no 4,000-character cliff.
 */
export function scanBudget(text: string): number {
  const words = text.match(/\S+/g)?.length ?? 0;
  return Math.min(180_000, Math.max(30_000, Math.ceil(words / 840) * 15_000));
}
/** Supported hostnames and the site each one belongs to. */
export const SITE_HOSTS: Record<string, Site> = {
  'chatgpt.com': 'chatgpt',
  'chat.openai.com': 'chatgpt',
  'claude.ai': 'claude',
  'gemini.google.com': 'gemini',
};
/**
 * Returns the supported site for an `https:` URL on a known host, or undefined
 * for any other URL, including one that does not parse.
 */
export function siteFor(url: string): Site | undefined {
  try {
    const u = new URL(url);
    return u.protocol === 'https:' ? SITE_HOSTS[u.hostname] : undefined;
  } catch {
    return;
  }
}
/**
 * Returns eight random uppercase letters. Callers use them as the prefix that
 * names one scan's placeholders.
 */
export function namespace() {
  return [...crypto.getRandomValues(new Uint8Array(8))]
    .map(n => String.fromCharCode(65 + (n % 26)))
    .join('');
}

/**
 * Whether a runtime message came from one of the extension's own contexts (the
 * background worker or an extension page) and not from a content script.
 *
 * Content scripts share the extension's id, so the id alone does not separate
 * them: they run inside chatgpt.com, claude.ai and gemini.google.com, where a
 * compromised page is the threat. A content script always reports the web
 * page as its origin and URL, and always has a tab.
 */
export function fromExtensionContext(sender: Untyped): boolean {
  const base = `chrome-extension://${browser.runtime.id}`;
  if (sender?.id !== browser.runtime.id) return false;
  if (sender.origin !== undefined && sender.origin !== base) return false;
  if (sender.url !== undefined && !String(sender.url).startsWith(`${base}/`)) {
    return false;
  }
  // No origin or URL to check: a sender with a tab is a page, not the worker.
  return !(
    sender.tab &&
    sender.origin === undefined &&
    sender.url === undefined
  );
}
