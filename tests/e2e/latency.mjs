/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Measures paste-to-insert latency of the real extension (test build, fake on-device model)
 * on a mock chat composer. Isolates the extension's own overhead from Gemini
 * Nano time.
 *   node tests/e2e/latency.mjs [runs]
 */

import {chromium} from 'playwright';
import {mkdtempSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, resolve} from 'node:path';
const ext = resolve(import.meta.dirname, '.build');
const runs = Number(process.argv[2] || 8);
const ctx = await chromium.launchPersistentContext(
  mkdtempSync(join(tmpdir(), 'redactobot-lat-')),
  {
    channel: 'chromium',
    headless: true,
    args: [`--disable-extensions-except=${ext}`, `--load-extension=${ext}`],
  },
);
await ctx.route('https://claude.ai/**', r =>
  r.fulfill({
    contentType: 'text/html',
    body: '<!doctype html><div class="ProseMirror" contenteditable="true" role="textbox" style="min-height:80px"></div>',
  }),
);
await ctx.grantPermissions(['clipboard-read', 'clipboard-write']);
const worker =
  ctx.serviceWorkers()[0] ?? (await ctx.waitForEvent('serviceworker'));
await new Promise(r => setTimeout(r, 500));
for (const p of ctx.pages()) {
  if (p.url().startsWith('chrome-extension://')) await p.close();
}
const cases = {
  'pattern-only, clean': {
    categories: ['contact', 'payments'],
    text: 'Please rewrite this paragraph in plain language.',
  },
  'pattern-only, email': {
    categories: ['contact', 'payments'],
    text: 'Email margaret@whitfield.example about it.',
  },
  'all categories, clean': {
    categories: null,
    text: 'Please rewrite this paragraph in plain language.',
  },
  'all categories, name+email': {
    categories: null,
    text: 'Margaret Whitfield asked: email margaret@whitfield.example.',
  },
  'all categories, 2,000 words clean': {
    categories: null,
    text: 'Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms. Please improve the clarity of this draft while preserving its meaning. Keep the wording direct and easy to read. Use short paragraphs and explain any unfamiliar terms.',
  },
};
const page = await ctx.newPage();
await page.goto('https://claude.ai/new');
await page.waitForFunction(
  () => !!document.querySelector('redactobot-paste-toggle'),
);
const results = {};
for (const [label, c] of Object.entries(cases)) {
  await worker.evaluate(v => chrome.storage.sync.set(v), {
    pasteCategories: c.categories ?? [
      'names',
      'contact',
      'places',
      'records',
      'payments',
      'credentials',
      'online',
      'dates',
      'money',
      'health',
      'sensitive',
      'context',
    ],
    cloudCleanup: false,
    sites: {},
  });
  const times = [];
  for (let i = 0; i < runs + 1; i++) {
    await page.evaluate(() => {
      const el = document.querySelector('.ProseMirror');
      el.textContent = '';
    });
    await page.evaluate(t => navigator.clipboard.writeText(t), c.text);
    await page.click('.ProseMirror');
    const t0 = Date.now();
    await page.keyboard.press('Control+V');
    await page.waitForFunction(
      () => document.querySelector('.ProseMirror').innerText.trim().length > 0,
      null,
      {timeout: 20000, polling: 5},
    );
    const ms = Date.now() - t0;
    if (i > 0) times.push(ms);
    else results[label + ' (first)'] = ms; // first run warms everything
  }
  results[label + ' text'] = await page.evaluate(() =>
    document.querySelector('.ProseMirror').innerText.trim().slice(0, 70),
  );
  times.sort((a, b) => a - b);
  results[label] = {
    median: times[Math.floor(times.length / 2)],
    min: times[0],
    max: times.at(-1),
  };
}
console.log(JSON.stringify(results, null, 1));
await ctx.close();
