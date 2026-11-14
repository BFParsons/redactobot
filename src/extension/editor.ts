/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Finds each chat site's message composer, records its draft and
 * selection when a paste is held, and inserts the cleaned text into it.
 */

import type {Site} from './protocol';

const selectors: Record<Site, string> = {
  // ChatGPT's current ProseMirror composer has no ID. Its accessible label is
  // the stable identifier; keep the older ID selectors for other composer
  // versions.
  chatgpt:
    '#prompt-textarea, textarea[data-id="root"], [contenteditable="true"][role="textbox"][aria-label="Ask ChatGPT" i], textarea[aria-label="Ask ChatGPT" i], [contenteditable="true"][data-placeholder*="Message"]',
  claude:
    'div.ProseMirror[contenteditable="true"], [contenteditable="true"][role="textbox"], textarea[placeholder*="Reply"], textarea[placeholder*="Message"]',
  gemini:
    'rich-textarea [contenteditable="true"], .ql-editor[contenteditable="true"], [contenteditable="true"][aria-label*="prompt" i], textarea[aria-label*="prompt" i]',
};
/** A chat site's message input: a textarea or a contenteditable element. */
export type Composer = HTMLTextAreaElement | HTMLElement;
/**
 * Returns the site's visible, editable composers in the document, leaving out
 * any that contain another match.
 */
export function composersFor(site: Site): Composer[] {
  const matches = [
    ...document.querySelectorAll<HTMLElement>(selectors[site]),
  ].filter(
    found =>
      (found instanceof HTMLTextAreaElement
        ? !found.disabled && !found.readOnly
        : found.getAttribute('contenteditable') === 'true') &&
      !found.closest(
        '[hidden], [inert], [aria-hidden="true"], .ql-clipboard, redactobot-paste-toggle, redactobot-paste-guard',
      ) &&
      getComputedStyle(found).display !== 'none' &&
      getComputedStyle(found).visibility !== 'hidden',
  );
  // Gemini can expose nested editable wrappers for one input. Match the inner
  // editor, as composerFor does for the paste target, and mount just one
  // switch.
  return matches.filter(
    found => !matches.some(other => other !== found && found.contains(other)),
  );
}
/** A composer's draft and selection, recorded when a paste is held. */
export interface Snapshot {
  composer: Composer;
  /** The draft text when recorded. */
  value: string;
  /** Selection start, as a character offset in `value`. */
  start: number;
  /** Selection end, as a character offset in `value`. */
  end: number;
  /** Copy of the selection range; contenteditable composers only. */
  range?: Range;
  /** `location.href` when recorded. */
  page: string;
}
/**
 * Returns the site's composer that the event was dispatched in, or undefined
 * when the event path holds no usable composer.
 */
export function composerFor(event: Event, site: Site): Composer | undefined {
  for (const node of event.composedPath()) {
    if (!(node instanceof HTMLElement)) continue;
    const found = node.closest<HTMLElement>(selectors[site]);
    if (
      !found ||
      found.closest(
        '[hidden], [inert], [aria-hidden="true"], .ql-clipboard, redactobot-paste-guard',
      )
    ) {
      continue;
    }
    if (
      !(found instanceof HTMLTextAreaElement) &&
      found.getAttribute('contenteditable') !== 'true'
    ) {
      continue;
    }
    if (
      found instanceof HTMLTextAreaElement &&
      (found.disabled || found.readOnly)
    ) {
      continue;
    }
    if (getComputedStyle(found).display === 'none') continue;
    return found;
  }
}
/** Returns the composer's current text. */
export const editorValue = (el: Composer) =>
  el instanceof HTMLTextAreaElement ? el.value : el.textContent || '';
/**
 * Records the composer's text and selection. Returns undefined when a
 * contenteditable composer does not contain the selection.
 */
export function capture(composer: Composer): Snapshot | undefined {
  const value = editorValue(composer);
  if (composer instanceof HTMLTextAreaElement) {
    return {
      composer,
      value,
      start: composer.selectionStart,
      end: composer.selectionEnd,
      page: location.href,
    };
  }
  const selection = window.getSelection();
  if (!selection?.rangeCount) return;
  const range = selection.getRangeAt(0);
  if (
    !composer.contains(range.startContainer) ||
    !composer.contains(range.endContainer)
  ) {
    return;
  }
  const before = range.cloneRange();
  before.selectNodeContents(composer);
  before.setEnd(range.startContainer, range.startOffset);
  const through = range.cloneRange();
  through.selectNodeContents(composer);
  through.setEnd(range.endContainer, range.endOffset);
  return {
    composer,
    value,
    start: before.toString().length,
    end: through.toString().length,
    range: range.cloneRange(),
    page: location.href,
  };
}
function rangeAt(composer: HTMLElement, start: number, end: number) {
  const range = document.createRange();
  const walker = document.createTreeWalker(composer, NodeFilter.SHOW_TEXT);
  let offset = 0;
  let began = false;
  let node: Node | null;
  while ((node = walker.nextNode())) {
    const length = node.textContent?.length || 0;
    if (!began && start <= offset + length) {
      range.setStart(node, Math.max(0, start - offset));
      began = true;
    }
    if (began && end <= offset + length) {
      range.setEnd(node, Math.max(0, end - offset));
      return range;
    }
    offset += length;
  }
  if (!began && start === 0 && end === 0) {
    range.selectNodeContents(composer);
    range.collapse(false);
    return range;
  }
  return undefined;
}
/**
 * Returns whether the composer is still attached, on the same page and holding
 * the text it had when recorded.
 */
export function unchanged(snapshot: Snapshot) {
  return (
    snapshot.composer.isConnected &&
    location.href === snapshot.page &&
    editorValue(snapshot.composer) === snapshot.value
  );
}

/**
 * Use the editor's native editing command so React/ProseMirror/Quill see an
 * ordinary edit.
 */
export function insert(snapshot: Snapshot, cleaned: string): boolean {
  if (!unchanged(snapshot)) return false;
  const composer = snapshot.composer;
  // Do not move text into a different editor after a navigation or a site
  // re-render.
  composer.focus({preventScroll: true});
  if (composer instanceof HTMLTextAreaElement) {
    composer.setSelectionRange(snapshot.start, snapshot.end);
  } else {
    const range =
      snapshot.range?.startContainer.isConnected &&
      composer.contains(snapshot.range.startContainer)
        ? snapshot.range.cloneRange()
        : rangeAt(composer, snapshot.start, snapshot.end);
    if (!range) return false;
    const selection = window.getSelection();
    if (!selection) return false;
    selection.removeAllRanges();
    selection.addRange(range);
  }
  const expected =
    snapshot.value.slice(0, snapshot.start) +
    cleaned +
    snapshot.value.slice(snapshot.end);
  let inserted = false;
  try {
    inserted = document.execCommand('insertText', false, cleaned);
  } catch {
    /* fall back below */
  }
  if (!inserted && editorValue(composer) === snapshot.value) {
    if (composer instanceof HTMLTextAreaElement) {
      const setter = Object.getOwnPropertyDescriptor(
        HTMLTextAreaElement.prototype,
        'value',
      )!.set!;
      setter.call(composer, expected);
      composer.setSelectionRange(
        snapshot.start + cleaned.length,
        snapshot.start + cleaned.length,
      );
    } else {
      const range = rangeAt(composer, snapshot.start, snapshot.end);
      if (!range) return false;
      range.deleteContents();
      const node = document.createTextNode(cleaned);
      range.insertNode(node);
      range.setStartAfter(node);
      range.collapse(true);
      window.getSelection()?.removeAllRanges();
      window.getSelection()?.addRange(range);
    }
    composer.dispatchEvent(
      new InputEvent('input', {
        bubbles: true,
        composed: true,
        inputType: 'insertFromPaste',
        data: cleaned,
      }),
    );
  }
  // Rich editors represent inserted line breaks with blocks or <br> elements.
  // textContent omits those breaks; compare characters while accepting that
  // representation.
  return composer instanceof HTMLTextAreaElement
    ? editorValue(composer) === expected
    : editorValue(composer).replace(/\r?\n/g, '') ===
        expected.replace(/\r?\n/g, '');
}
