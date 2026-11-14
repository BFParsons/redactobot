/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The review page: lists the findings in a held paste, previews
 * the text to insert and sends the user's decision to the background.
 */

import {
  browser,
  type ScanReport,
  type Theme,
  type RuntimePort,
} from './protocol';
import {applyTheme} from './themes';
import {BUCKET_LABELS, privacyBucket} from '../core/privacy-buckets';

/** What the background sends the review page about one held paste. */
export interface ReviewState {
  /** The pasted text before cleaning. */
  text: string;
  report: ScanReport;
  theme: Theme;
  /** True when the draft changed while the paste was checked. */
  contextChanged: boolean;
  /** True when the preview is the text that cloud cleanup would receive. */
  cloudCleanup?: boolean;
  /** Message for the status line. */
  error?: string;
}
/**
 * Connects the review page's controls to `port`: shows each review state that
 * arrives and posts the user's choice back.
 */
export function renderReview(port: RuntimePort) {
  const title = document.querySelector<HTMLElement>('#title')!;
  const explanation = document.querySelector<HTMLElement>('#explanation')!;
  const list = document.querySelector<HTMLElement>('#findings')!;
  const preview = document.querySelector<HTMLTextAreaElement>('#preview')!;
  const original = document.querySelector<HTMLElement>('#original')!;
  const approve = document.querySelector<HTMLButtonElement>('#approve')!;
  const use = document.querySelector<HTMLButtonElement>('#use')!;
  const ignore = document.querySelector<HTMLButtonElement>('#ignore')!;
  const status = document.querySelector<HTMLElement>('#status')!;
  const kept = new Set<string>();
  let state: ReviewState | undefined;
  let edited = false;
  // The primary button only appears when it does more than "Use this text": a
  // cloud cleanup pass, or another scan of an incomplete or edited cloud
  // preview.
  function updateActions() {
    if (!state) return;
    const label = !state.report.complete
      ? edited
        ? 'Check edited text'
        : 'Scan again'
      : state.cloudCleanup
        ? edited
          ? 'Check edited text'
          : 'Clean up this preview in cloud'
        : '';
    approve.textContent = label;
    approve.hidden = !label || state.contextChanged;
    use.className = approve.hidden ? 'primary' : 'secondary';
  }
  function setBusy(busy: boolean) {
    ignore.disabled = busy;
    use.disabled = busy;
    approve.disabled = busy;
  }
  function updatePreview() {
    if (!state || edited) return;
    let result = '';
    let at = 0;
    for (const finding of state.report.findings) {
      if (kept.has(finding.id)) continue;
      result +=
        state.text.slice(at, finding.start) +
        `[${state.report.replacements[finding.id]}]`;
      at = finding.end;
    }
    preview.value = result + state.text.slice(at);
  }
  port.onMessage.addListener(message => {
    if (message.type === 'busy') {
      setBusy(true);
      status.textContent = message.label;
      return;
    }
    if (message.type === 'error') {
      setBusy(!state);
      status.textContent = message.message;
      return;
    }
    if (message.type === 'insert-failed') {
      setBusy(false);
      preview.focus();
      preview.select();
      status.textContent =
        'Could not place the text in the chat box. It is selected below; copy it with Ctrl+C (or Command+C).';
      return;
    }
    if (message.type === 'theme') {
      applyTheme(document.documentElement, message.theme);
      return;
    }
    if (message.type === 'closed') {
      setBusy(true);
      status.textContent = 'This paste has finished or was canceled.';
      return;
    }
    if (message.type !== 'review-state' || !message.report) return;
    state = message as ReviewState;
    edited = false;
    kept.clear();
    if (state.cloudCleanup) {
      for (const finding of state.report.findings) {
        if (privacyBucket(finding) === 'cloud-cleanup') kept.add(finding.id);
      }
    }
    applyTheme(document.documentElement, state.theme);
    title.textContent = state.report.complete
      ? 'A quick check before pasting'
      : 'The scan needs your help';
    explanation.textContent = state.contextChanged
      ? 'Your draft changed while this was checked. Use this text adds it at the end of your draft.'
      : state.report.reasons.join(' ') ||
        (state.cloudCleanup
          ? 'Identifiers must be removed locally. The preview below will go to Gemini through Firebase to remove remaining sensitive details. You can also select those details for local removal.'
          : 'Identifying and uncertain details must be removed locally. Check the scrubbed text before pasting.');
    setBusy(false);
    updateActions();
    document.querySelector('label[for="preview"]')!.textContent =
      state.cloudCleanup
        ? 'Exact text the cloud will receive'
        : 'Text to paste';
    status.textContent = state.error || '';
    original.textContent = state.text;
    list.replaceChildren();
    for (const finding of state.report.findings) {
      const row = document.createElement('label');
      row.className = 'finding';
      const bucket = privacyBucket(finding);
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.checked = !kept.has(finding.id);
      checkbox.disabled = bucket === 'local-only';
      checkbox.dataset.locked = String(bucket === 'local-only');
      const words = document.createElement('span');
      const value = document.createElement('strong');
      value.textContent = finding.text;
      const reason = document.createElement('small');
      reason.textContent = `${BUCKET_LABELS[bucket]} · ${finding.label}${finding.reviewReason ? ' · ' + finding.reviewReason : ''}`;
      words.append(value, reason);
      row.append(checkbox, words);
      list.append(row);
      checkbox.addEventListener('change', () => {
        if (checkbox.checked) kept.delete(finding.id);
        else kept.add(finding.id);
        updatePreview();
      });
    }
    updatePreview();
  });
  preview.addEventListener('input', () => {
    edited = true;
    list.querySelectorAll<HTMLInputElement>('input').forEach(input => {
      input.disabled = true;
    });
    status.textContent = state?.cloudCleanup
      ? 'Edited text gets another local check before cloud cleanup. Use this text pastes it as written.'
      : 'Use this text pastes your edited text as written.';
    updateActions();
  });
  document.querySelector('#reset')!.addEventListener('click', () => {
    edited = false;
    updatePreview();
    status.textContent = '';
    updateActions();
    list.querySelectorAll<HTMLInputElement>('input').forEach(input => {
      input.disabled = input.dataset.locked === 'true';
    });
  });
  approve.addEventListener('click', () => {
    if (!state) return;
    setBusy(true);
    port.postMessage({
      type: 'approve',
      kept: [...kept],
      edited: edited ? preview.value : undefined,
      rescan: !edited && !state.report.complete,
    });
  });
  // User overrides. Both paste directly; the inserted text is not checked
  // again.
  use.addEventListener('click', () => {
    if (state) {
      setBusy(true);
      port.postMessage({type: 'use', text: preview.value});
    }
  });
  ignore.addEventListener('click', () => {
    if (state) {
      setBusy(true);
      port.postMessage({type: 'ignore'});
    }
  });
  document
    .querySelector('#cancel')!
    .addEventListener('click', () => port.postMessage({type: 'cancel'}));
  document
    .querySelector('#settings')!
    .addEventListener('click', () => port.postMessage({type: 'settings'}));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') port.postMessage({type: 'cancel'});
  });
  port.onDisconnect.addListener(() => {
    setBusy(true);
    status.textContent =
      'This review disconnected. Copy your reviewed text or paste again.';
  });
}
if (browser?.runtime?.id) {
  renderReview(
    browser.runtime.connect({name: `review:${location.hash.slice(1)}`}),
  );
}
