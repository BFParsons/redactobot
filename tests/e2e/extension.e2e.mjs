/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview End-to-end tests for the Chrome paste guard.
 *
 * Loads the real unpacked extension (a TEST build with a fake on-device model,
 * see fake-nano.js) into Playwright's Chromium. ChatGPT, Claude and Gemini are
 * served from local mock pages at their real URLs, so the content script
 * attaches exactly as it does in production. Each mock records what the SITE
 * itself receives: paste and drop events, and any send. Pastes use real
 * keyboard shortcuts (trusted events).
 *
 *   npm run test:e2e
 *
 * Everything typed here is fictional.
 */

import {test, before, after} from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtempSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, resolve} from 'node:path';
import {chromium} from 'playwright';

const root = resolve(import.meta.dirname, '../..');
const extensionDir = resolve(root, 'tests/e2e/.build');
const ALL = [
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
];

// Composer markup matching each site's selector in src/extension/editor.ts.
const SITES = {
  chatgpt: {
    url: 'https://chatgpt.com/',
    composer: '#prompt-textarea',
    markup:
      '<div id="prompt-textarea" class="ProseMirror" contenteditable="true" role="textbox"></div>',
  },
  claude: {
    url: 'https://claude.ai/new',
    composer: 'div.ProseMirror',
    markup:
      '<div class="ProseMirror" contenteditable="true" role="textbox"></div>',
  },
  gemini: {
    url: 'https://gemini.google.com/app',
    composer: '.ql-editor',
    markup:
      '<rich-textarea><div class="ql-editor" contenteditable="true"></div></rich-textarea>',
  },
  'chatgpt-textarea': {
    url: 'https://chatgpt.com/textarea',
    composer: '#prompt-textarea',
    markup: '<textarea id="prompt-textarea" rows="6"></textarea>',
  },
};
const mockPage =
  markup => `<!doctype html><html><head><meta charset="utf-8"><title>Mock chat</title>
<style>body{font:16px system-ui;margin:40px}[contenteditable],textarea{display:block;width:600px;min-height:120px;border:1px solid #888;padding:8px;white-space:pre-wrap}</style></head>
<body><p id="source" draggable="false">Drag source: Margaret Whitfield, margaret@whitfield.example</p>
<form id="chat">${markup}<button id="send" type="submit">Send</button></form>
<script>
  // The site's own handlers. The guard must stop raw pastes/drops before these run.
  window.__site = { pastes: [], drops: [], sends: 0 };
  document.addEventListener('paste', e => __site.pastes.push(e.clipboardData.getData('text/plain')));
  document.addEventListener('drop', e => { __site.drops.push(e.dataTransfer.getData('text/plain')); });
  document.addEventListener('dragover', e => e.preventDefault());
  document.getElementById('chat').addEventListener('submit', e => { e.preventDefault(); __site.sends++; });
  document.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) __site.sends++; }, true);
</script></body></html>`;

let context;
let worker;
let profile;
before(async () => {
  const built = spawnSync(
    process.execPath,
    ['tools/build_extension.mjs', '--out', extensionDir, '--fake-nano'],
    {cwd: root, encoding: 'utf8'},
  );
  assert.equal(built.status, 0, built.stderr);
  profile = mkdtempSync(join(tmpdir(), 'redactobot-e2e-'));
  context = await chromium.launchPersistentContext(profile, {
    channel: 'chromium',
    headless: !process.env.HEADED,
    args: [
      `--disable-extensions-except=${extensionDir}`,
      `--load-extension=${extensionDir}`,
    ],
  });
  for (const site of Object.values(SITES)) {
    await context.route(site.url, route =>
      route.fulfill({contentType: 'text/html', body: mockPage(site.markup)}),
    );
  }
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  worker =
    context.serviceWorkers()[0] ??
    (await context.waitForEvent('serviceworker'));
  // Close the settings tab the extension opens on install.
  await new Promise(r => setTimeout(r, 500));
  for (const page of context.pages()) {
    if (page.url().startsWith('chrome-extension://')) await page.close();
  }
});
after(async () => {
  await context?.close();
  if (profile) rmSync(profile, {recursive: true, force: true});
});

async function settings({categories = ALL, cloudCleanup = false} = {}) {
  await worker.evaluate(value => chrome.storage.sync.set(value), {
    pasteCategories: categories,
    cloudCleanup,
    sites: {},
  });
}
/** Run a function on the Redactobot switch's closed shadow root, via CDP. */
async function onToggle(page, fn) {
  const cdp = await page.context().newCDPSession(page);
  try {
    const {root: doc} = await cdp.send('DOM.getDocument', {
      depth: -1,
      pierce: true,
    });
    const host = (function find(node) {
      if (node.localName === 'redactobot-paste-toggle') return node;
      for (const child of [
        ...(node.children || []),
        ...(node.shadowRoots || []),
      ]) {
        const hit = find(child);
        if (hit) return hit;
      }
    })(doc);
    const {object} = await cdp.send('DOM.resolveNode', {
      backendNodeId: host.shadowRoots[0].backendNodeId,
    });
    const {result} = await cdp.send('Runtime.callFunctionOn', {
      objectId: object.objectId,
      functionDeclaration: fn,
      returnByValue: true,
    });
    return result.value;
  } finally {
    await cdp.detach();
  }
}
const switchState = page =>
  onToggle(
    page,
    'function(){return this.querySelector("[role=switch]").getAttribute("aria-checked")}',
  );
const flipSwitch = page =>
  onToggle(page, 'function(){this.querySelector("[role=switch]").click()}');
/**
 * Open a mock chat page. Redactobot starts off on every page; switch it on
 * unless asked not to.
 */
async function open(name, {on = true} = {}) {
  const page = await context.newPage();
  await page.goto(SITES[name].url);
  await page.waitForFunction(
    () => !!document.querySelector('redactobot-paste-toggle'),
  );
  assert.equal(
    await switchState(page),
    'false',
    'Redactobot must start switched off',
  );
  if (on) {
    await flipSwitch(page);
    assert.equal(await switchState(page), 'true');
  }
  return page;
}
const composer = (page, name) => page.locator(SITES[name].composer);
const composerText = (page, name) =>
  composer(page, name).evaluate(el =>
    el instanceof HTMLTextAreaElement ? el.value : el.innerText,
  );
const site = page => page.evaluate(() => window.__site);

/**
 * Put text (and optionally an image, as Excel and Word do) on the clipboard and
 * press Ctrl+V.
 */
async function paste(page, name, text, {image = false} = {}) {
  await page.bringToFront();
  await page.evaluate(
    async ({text, image}) => {
      const items = {'text/plain': new Blob([text], {type: 'text/plain'})};
      if (image) {
        const canvas = Object.assign(document.createElement('canvas'), {
          width: 8,
          height: 8,
        });
        items['image/png'] = await new Promise(r =>
          canvas.toBlob(r, 'image/png'),
        );
      }
      await navigator.clipboard.write([new ClipboardItem(items)]);
    },
    {text, image},
  );
  await composer(page, name).click();
  await page.keyboard.press('Control+V');
}
async function waitForText(page, name, predicate, timeout = 15000) {
  const started = Date.now();
  let value = '';
  while (Date.now() - started < timeout) {
    value = await composerText(page, name);
    if (predicate(value)) return value;
    await page.waitForTimeout(100);
  }
  assert.fail(`Composer never matched. Last value: ${JSON.stringify(value)}`);
}
const reviewFrame = page =>
  page.frames().find(frame => frame.url().includes('/review.html'));
async function waitForReview(page, timeout = 15000) {
  const started = Date.now();
  while (Date.now() - started < timeout) {
    const frame = reviewFrame(page);
    if (
      frame &&
      (
        await frame
          .locator('#explanation')
          .textContent()
          .catch(() => '')
      )?.trim()
    ) {
      return frame;
    }
    await page.waitForTimeout(100);
  }
  assert.fail('The review never opened.');
}
/**
 * Read the guard's inline status. Its shadow root is closed, so pierce it with
 * CDP.
 */
async function guardStatus(page) {
  const cdp = await page.context().newCDPSession(page);
  try {
    const {root: doc} = await cdp.send('DOM.getDocument', {
      depth: -1,
      pierce: true,
    });
    const host = (function find(node) {
      if (node.localName === 'redactobot-paste-guard') return node;
      for (const child of [
        ...(node.children || []),
        ...(node.shadowRoots || []),
      ]) {
        const hit = find(child);
        if (hit) return hit;
      }
    })(doc);
    if (!host?.shadowRoots?.length) return '';
    const {object} = await cdp.send('DOM.resolveNode', {
      backendNodeId: host.shadowRoots[0].backendNodeId,
    });
    const {result} = await cdp.send('Runtime.callFunctionOn', {
      objectId: object.objectId,
      functionDeclaration: 'function(){return this.textContent}',
      returnByValue: true,
    });
    return result.value || '';
  } finally {
    await cdp.detach();
  }
}
async function assertNoLeak(page, raw) {
  const seen = await site(page);
  for (const value of [...seen.pastes, ...seen.drops]) {
    for (const secret of raw) {
      assert.ok(!value.includes(secret), `The site received raw "${secret}"`);
    }
  }
  assert.equal(seen.sends, 0, 'The guard must never send a message');
}

const IDENTIFIERS =
  'Email margaret@whitfield.example or call 604-555-0142. Card 4111 1111 1111 1111.';
const RAW = [
  'margaret@whitfield.example',
  '604-555-0142',
  '4111 1111 1111 1111',
];

for (const name of Object.keys(SITES)) {
  test(`${name}: scrubs identifiers and names and inserts automatically, never sending`, async () => {
    await settings();
    const page = await open(name);
    await paste(
      page,
      name,
      `Margaret Whitfield asked about the Harbourline Marine Supply sale. ${IDENTIFIERS}`,
    );
    const value = await waitForText(page, name, v => v.includes('[PERSON_'));
    for (const secret of [
      ...RAW,
      'Margaret Whitfield',
      'Harbourline Marine Supply',
    ]) {
      assert.ok(
        !value.includes(secret),
        `"${secret}" reached the composer: ${value}`,
      );
    }
    assert.match(value, /\[EMAIL_[A-Z_]+\d*\]/);
    await assertNoLeak(page, [...RAW, 'Margaret Whitfield']);
    await page.close();
  });
}

test('clean text is inserted unchanged', async () => {
  await settings();
  const page = await open('claude');
  const clean = 'Summarize the main causes of inflation in plain language.';
  assert.equal(
    await waitForText(page, 'claude', v => v.length > 0, 1).catch(() => ''),
    '',
  );
  await paste(page, 'claude', clean);
  assert.equal(
    (await waitForText(page, 'claude', v => v.includes('inflation'))).trim(),
    clean,
  );
  await assertNoLeak(page, []);
  await page.close();
});

test('text copied with an image (Excel/Word) is scrubbed, not passed through', async () => {
  await settings();
  const page = await open('chatgpt');
  await paste(
    page,
    'chatgpt',
    `Client\tMargaret Whitfield\nEmail\tmargaret@whitfield.example`,
    {image: true},
  );
  const value = await waitForText(page, 'chatgpt', v => v.includes('[EMAIL_'));
  assert.ok(
    !value.includes('margaret@whitfield.example') &&
      !value.includes('Margaret Whitfield'),
    value,
  );
  await assertNoLeak(page, [
    'margaret@whitfield.example',
    'Margaret Whitfield',
  ]);
  await page.close();
});

test('control: the mixed clipboard really carries a file', async () => {
  await settings();
  const page = await open('chatgpt', {on: false});
  await page.waitForTimeout(300);
  await page.evaluate(() =>
    document.addEventListener('paste', e => {
      window.__files = e.clipboardData.files.length;
    }),
  );
  await paste(page, 'chatgpt', 'probe', {image: true});
  await page.waitForTimeout(300);
  assert.ok(
    (await page.evaluate(() => window.__files)) > 0,
    'Chromium did not expose the image as a file',
  );
  await page.close();
});

test('dragged text is scrubbed before it reaches the composer', async () => {
  await settings();
  const page = await open('claude');
  // Select the fictional source line, then drag it into the composer with the
  // mouse.
  await page.evaluate(() => {
    const range = document.createRange();
    range.selectNodeContents(document.getElementById('source'));
    getSelection().removeAllRanges();
    getSelection().addRange(range);
  });
  const from = await page.locator('#source').boundingBox();
  const to = await composer(page, 'claude').boundingBox();
  await page.mouse.move(from.x + 40, from.y + from.height / 2);
  await page.mouse.down();
  await page.mouse.move(to.x + 40, to.y + 30, {steps: 10});
  await page.mouse.up();
  const value = await waitForText(
    page,
    'claude',
    v => v.includes('[EMAIL_') || v.includes('margaret@'),
  );
  assert.ok(
    !value.includes('margaret@whitfield.example'),
    `Raw dragged text reached the composer: ${value}`,
  );
  await assertNoLeak(page, ['margaret@whitfield.example']);
  await page.close();
});

test('ambiguous findings open a review; Use this text pastes the scrubbed text', async () => {
  await settings();
  const page = await open('gemini');
  await paste(page, 'gemini', 'Ask Quillon whether the filing is ready.');
  const frame = await waitForReview(page);
  assert.equal(
    await composerText(page, 'gemini'),
    '',
    'Nothing may be inserted before review',
  );
  assert.match(await frame.locator('#preview').inputValue(), /\[/);
  assert.equal(
    await frame.locator('#approve').isVisible(),
    false,
    'Without cloud cleanup, Use this text is the action',
  );
  await frame.locator('#use').click();
  const value = await waitForText(page, 'gemini', v => v.includes('['));
  assert.ok(!value.includes('Quillon'), value);
  await assertNoLeak(page, ['Quillon']);
  await page.close();
});

test('a model failure holds the paste; Scan again recovers', async () => {
  await settings();
  const page = await open('chatgpt');
  await paste(
    page,
    'chatgpt',
    'E2E_MODEL_FAIL Margaret Whitfield, margaret@whitfield.example',
  );
  const frame = await waitForReview(page);
  assert.equal(
    await composerText(page, 'chatgpt'),
    '',
    'An incomplete scan must not insert',
  );
  assert.equal(await frame.locator('#approve').textContent(), 'Scan again');
  // Edit out the failure marker. The edited text gets a fresh local check; a
  // clear result is inserted without another review.
  await frame
    .locator('#preview')
    .fill('Margaret Whitfield, margaret@whitfield.example');
  assert.equal(
    await frame.locator('#approve').textContent(),
    'Check edited text',
  );
  await frame.locator('#approve').click();
  const value = await waitForText(page, 'chatgpt', v => v.includes('[EMAIL_'));
  assert.ok(!value.includes('margaret@whitfield.example'), value);
  await assertNoLeak(page, ['margaret@whitfield.example']);
  await page.close();
});

test('pattern-only categories never call the on-device model', async () => {
  await settings({categories: ['contact', 'payments']});
  const page = await open('claude');
  // The fake model would fail on this marker; pattern-only checks must not
  // reach it.
  await paste(page, 'claude', `E2E_MODEL_FAIL ${IDENTIFIERS}`);
  const value = await waitForText(page, 'claude', v => v.includes('[EMAIL_'));
  for (const secret of RAW) assert.ok(!value.includes(secret), value);
  assert.ok(value.includes('E2E_MODEL_FAIL'));
  await page.close();
});

test('unchecked categories are left alone', async () => {
  await settings({categories: ['contact']});
  const page = await open('chatgpt');
  await paste(
    page,
    'chatgpt',
    'Margaret Whitfield: margaret@whitfield.example',
  );
  const value = await waitForText(page, 'chatgpt', v => v.includes('[EMAIL_'));
  assert.ok(
    value.includes('Margaret Whitfield'),
    'Names were not selected, so they stay',
  );
  await page.close();
});

test('cloud cleanup that cannot run falls back to an explicit local-only paste', async () => {
  await settings({cloudCleanup: true});
  const page = await open('gemini');
  await paste(
    page,
    'gemini',
    'Margaret Whitfield has diabetes. margaret@whitfield.example',
  );
  const frame = await waitForReview(page);
  assert.match(
    await frame.locator('#status').textContent(),
    /local removal only/i,
  );
  assert.equal(
    await frame.locator('#approve').isVisible(),
    false,
    'No cloud retry after a failure',
  );
  await frame.locator('#use').click();
  const value = await waitForText(page, 'gemini', v => v.includes('['));
  for (const secret of [
    'Margaret Whitfield',
    'margaret@whitfield.example',
    'diabetes',
  ]) {
    assert.ok(!value.includes(secret), value);
  }
  await page.close();
});

test('two quick pastes are both scrubbed and inserted in order', async () => {
  await settings();
  const page = await open('claude');
  await paste(page, 'claude', 'First: margaret@whitfield.example. ');
  await paste(page, 'claude', 'Second: 604-555-0142.');
  const value = await waitForText(page, 'claude', v => v.includes('Second'));
  assert.ok(value.indexOf('First') < value.indexOf('Second'), value);
  for (const secret of ['margaret@whitfield.example', '604-555-0142']) {
    assert.ok(!value.includes(secret), value);
  }
  await page.close();
});

test('an oversized paste is refused without blocking the next one', async () => {
  await settings();
  const page = await open('chatgpt');
  await paste(page, 'chatgpt', 'x'.repeat(100_001));
  await page.waitForTimeout(300);
  assert.match(await guardStatus(page), /too large/i);
  assert.equal(await composerText(page, 'chatgpt'), '');
  await paste(page, 'chatgpt', 'Next: margaret@whitfield.example');
  await waitForText(page, 'chatgpt', v => v.includes('[EMAIL_'));
  await page.close();
});

test('typing while a scan runs does not overwrite the draft', async () => {
  await settings();
  const page = await open('chatgpt');
  await paste(page, 'chatgpt', 'E2E_MODEL_SLOW margaret@whitfield.example');
  await page.keyboard.type('typed meanwhile');
  const frame = await waitForReview(page, 20000);
  assert.match(
    await frame.locator('#explanation').textContent(),
    /draft changed/i,
  );
  assert.doesNotMatch(
    await frame.locator('#preview').inputValue(),
    /margaret@whitfield/,
  );
  // Use this text adds the reviewed text after what the user typed.
  await frame.locator('#use').click();
  const after = await waitForText(page, 'chatgpt', v => v.includes('[EMAIL_'));
  assert.ok(after.indexOf('typed meanwhile') < after.indexOf('[EMAIL_'), after);
  assert.ok(!after.includes('margaret@whitfield.example'), after);
  const value = await composerText(page, 'chatgpt');
  assert.ok(
    value.includes('typed meanwhile') &&
      !value.includes('margaret@whitfield.example'),
    value,
  );
  await page.close();
});

test('Redactobot starts off: a paste goes straight through to the site', async () => {
  await settings();
  const page = await open('claude', {on: false});
  await page.waitForTimeout(300);
  await paste(page, 'claude', 'Unprotected: margaret@whitfield.example');
  await page.waitForTimeout(500);
  const seen = await site(page);
  assert.ok(
    seen.pastes.some(p => p.includes('margaret@whitfield.example')),
    'With protection off, the site handles the paste itself',
  );
  await page.close();
});

test('switched on in one tab, a new page still starts off', async () => {
  await settings();
  const first = await open('gemini');
  const second = await open('gemini', {on: false});
  assert.equal(await switchState(first), 'true');
  assert.equal(await switchState(second), 'false');
  await first.close();
  await second.close();
});

test('Use this text pastes an edited review exactly as written, without another check', async () => {
  await settings();
  const page = await open('claude');
  await paste(page, 'claude', 'Ask Quillon whether the filing is ready.');
  const frame = await waitForReview(page);
  // Tom Whitfield would be removed by a fresh check; Use this text must not run
  // one.
  await frame
    .locator('#preview')
    .fill('Ask Tom Whitfield whether the filing is ready.');
  await frame.locator('#use').click();
  const value = await waitForText(page, 'claude', v => v.includes('filing'));
  assert.equal(value.trim(), 'Ask Tom Whitfield whether the filing is ready.');
  await assertNoLeak(page, ['Quillon']);
  await page.close();
});

test('Ignore pastes the original text unchanged and it is not checked again', async () => {
  await settings();
  const page = await open('gemini');
  const original = 'Ask Quillon to email margaret@whitfield.example.';
  await paste(page, 'gemini', original);
  const frame = await waitForReview(page);
  await frame.locator('#ignore').click();
  const value = await waitForText(page, 'gemini', v => v.includes('Quillon'));
  assert.equal(value.trim(), original);
  await page.waitForTimeout(1000);
  assert.equal(
    (await composerText(page, 'gemini')).trim(),
    original,
    'The ignored text must not be rescanned or replaced',
  );
  assert.equal((await site(page)).sends, 0);
  await page.close();
});
