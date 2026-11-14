/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Local visual preview only; not included in the extension
 * bundle.
 */

import {renderReview} from './review';
import {fallbackTheme} from './themes';
import {makeReport} from './policy';
import {NO_TOPICS} from '../core/redact';
import type {Site} from './protocol';
const template = new DOMParser().parseFromString(
  await (await fetch('/extension/review.html')).text(),
  'text/html',
);
template.querySelectorAll('script').forEach(node => node.remove());
document.body.replaceChildren(...template.body.childNodes);
const params = new URLSearchParams(location.search);
const site = (
  ['chatgpt', 'claude', 'gemini'].includes(params.get('site') || '')
    ? params.get('site')
    : 'chatgpt'
) as Site;
const text =
  'Jordan can be reached at jordan@example.com. The note mentions a diagnosis of diabetes.';
const report = makeReport(
  text,
  {people: [], companies: []},
  {...NO_TOPICS, names: ['Jordan'], health: ['diabetes']},
  [{text: 'Jordan', reason: 'This could be a person or a place.'}],
  'DEMO',
);
renderReview({
  name: 'preview',
  disconnect() {},
  onDisconnect: {addListener() {}},
  onMessage: {
    addListener(fn) {
      fn({
        type: 'review-state',
        text,
        report,
        theme: fallbackTheme(site, params.get('mode') === 'dark'),
        contextChanged: false,
      });
    },
  },
  postMessage(message) {
    document.querySelector('#status')!.textContent =
      message.type === 'approve'
        ? 'Preview only. Nothing was pasted or sent.'
        : 'This is a visual preview with fictional details.';
  },
});
