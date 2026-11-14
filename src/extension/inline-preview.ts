/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Visual harness only; never bundled in the extension and never
 * runs an AI model.
 */

import {installPasteGuard} from './content';
import {applyTheme, fallbackTheme} from './themes';
import type {RuntimePort, Site, Untyped} from './protocol';
const params = new URLSearchParams(location.search);
const site = (
  ['chatgpt', 'claude', 'gemini'].includes(params.get('site') || '')
    ? params.get('site')
    : 'chatgpt'
) as Site;
const theme = fallbackTheme(site, params.has('dark'));
applyTheme(document.documentElement, theme);
document.documentElement.style.setProperty(
  {
    chatgpt: '--text-secondary',
    claude: '--text-400',
    gemini: '--gem-sys-color--on-surface-variant',
  }[site],
  theme.muted,
);
const editor = document.querySelector<HTMLElement>('[contenteditable]')!;
// Capture only this demo's own shadow root to verify rendered font parity in
// Chrome.
const attach = Element.prototype.attachShadow;
let demoRoot: ShadowRoot | undefined;
Element.prototype.attachShadow = function (init) {
  const root = attach.call(this, init);
  if (this.tagName === 'REDACTOBOT-PASTE-GUARD') demoRoot = root;
  return root;
};
let id = '';
let receive = (_message: Untyped) => {};
let canceled = false;
function connect(): RuntimePort {
  return {
    name: 'demo',
    onMessage: {
      addListener(fn) {
        receive = fn;
      },
    },
    onDisconnect: {addListener() {}},
    disconnect() {},
    postMessage(message) {
      if (message.type === 'start') {
        id = message.id;
        canceled = false;
        setTimeout(
          () =>
            receive({type: 'progress', id, label: 'Removing private details…'}),
          250,
        );
      }
      if (message.type === 'cancel') canceled = true;
    },
  };
}
const guard = installPasteGuard(
  site,
  {connect, reviewUrl: () => 'about:blank', settings() {}},
  false,
);
Element.prototype.attachShadow = attach;
const verification = document.createElement('small');
verification.style.cssText =
  'display:block;font:11px/16px system-ui;margin-top:10px;color:var(--rb-muted)';
document.body.append(verification);
setTimeout(() => {
  const status = demoRoot?.querySelector<HTMLElement>('.status');
  if (!status) {
    verification.textContent = 'Status missing';
    return;
  }
  const a = getComputedStyle(editor);
  const b = getComputedStyle(status);
  const same = [
    'fontFamily',
    'fontSize',
    'fontWeight',
    'fontStyle',
    'lineHeight',
    'letterSpacing',
  ].every(
    key =>
      a[key as keyof CSSStyleDeclaration] ===
      b[key as keyof CSSStyleDeclaration],
  );
  verification.textContent = same
    ? 'Typography matches input · draft unchanged'
    : `Font mismatch: ${a.font} / ${b.font}`;
}, 600);
function start() {
  if (id && !canceled) receive({type: 'canceled', id});
  editor.textContent = '';
  const range = document.createRange();
  range.selectNodeContents(editor);
  range.collapse(false);
  window.getSelection()!.removeAllRanges();
  window.getSelection()!.addRange(range);
  const data = new DataTransfer();
  data.setData('text/plain', 'Email: avery@example.com.');
  editor.dispatchEvent(
    new ClipboardEvent('paste', {
      clipboardData: data,
      bubbles: true,
      cancelable: true,
      composed: true,
    }),
  );
}
document.querySelector('#again')!.addEventListener('click', start);
document.querySelector('#finish')!.addEventListener('click', () => {
  if (id && !canceled) {
    receive({type: 'insert', id, cleaned: 'Email: [EMAIL_DEMO_1].', count: 1});
  }
});
window.addEventListener('pagehide', () => guard.dispose());
start();
