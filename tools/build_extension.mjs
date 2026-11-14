/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {build} from 'vite';
import {mkdir, copyFile, cp, readFile, writeFile} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
// `--out <dir> --fake-nano` makes the end-to-end TEST build (tests/e2e). It
// swaps in a deterministic stand-in for Gemini Nano and must never be loaded
// for real use.
const arg = key =>
  process.argv.includes(key)
    ? process.argv[process.argv.indexOf(key) + 1]
    : undefined;
const fakeNano = process.argv.includes('--fake-nano');
// The build that is published: no Firebase project, no debug token, and no
// network access of any kind. See tools/package_extension.mjs.
const publicBuild = process.argv.includes('--public');
const outDir = resolve(root, arg('--out') || 'extension/build');
if (fakeNano && outDir === resolve(root, 'extension/build')) {
  throw new Error('--fake-nano needs a separate --out directory.');
}
// The test build must never reach a real Firebase project: blank the settings
// Vite would read from .env.local (process.env takes precedence over .env
// files).
if (fakeNano || publicBuild) {
  for (const key of [
    'VITE_FIREBASE_API_KEY',
    'VITE_FIREBASE_AUTH_DOMAIN',
    'VITE_FIREBASE_PROJECT_ID',
    'VITE_FIREBASE_APP_ID',
    'VITE_APPCHECK_DEBUG_TOKEN',
    'VITE_RECAPTCHA_ENTERPRISE_SITE_KEY',
    'VITE_CLOUD_MODEL',
  ]) {
    process.env[key] = '';
  }
}
await mkdir(outDir, {recursive: true});
for (const entry of [
  'content',
  'background',
  'review',
  'options',
  'scanner',
  'detection-worker',
]) {
  await build({
    configFile: false,
    root,
    publicDir: false,
    build: {
      outDir,
      emptyOutDir: false,
      target: 'chrome148',
      lib: {
        entry: resolve(root, `src/extension/${entry}.ts`),
        name: 'Redactobot',
        formats: ['iife'],
        fileName: () => `${entry}.js`,
      },
    },
  });
}
for (const file of [
  'manifest.json',
  'review.html',
  'options.html',
  'scanner.html',
  'ui.css',
]) {
  await copyFile(resolve(root, 'extension', file), resolve(outDir, file));
}
await copyFile(
  resolve(root, 'taxonomy/places-data.NOTICE'),
  resolve(outDir, 'places-data.NOTICE'),
);
await cp(resolve(root, 'extension/icons'), resolve(outDir, 'icons'), {
  recursive: true,
});
await copyFile(
  resolve(root, 'public/contact-email.js'),
  resolve(outDir, 'contact-email.js'),
);
// The privacy policy is one page shared with the web app. Inside the extension
// it has no site root: drop the web-only script and icon, and point the back
// link at the settings page.
await writeFile(
  resolve(outDir, 'privacy.html'),
  (await readFile(resolve(root, 'public/privacy.html'), 'utf8'))
    .replace(/^\s*<link rel="icon"[^\n]*\n/m, '')
    .replace(/^\s*<script src="\/display-prefs\.js"><\/script>\n/m, '')
    .replace('src="/contact-email.js"', 'src="contact-email.js"')
    .replace(
      '<a class="back" href="/">&larr; Back to Redactobot</a>',
      '<a class="back" href="options.html">&larr; Back to settings</a>',
    ),
);
if (fakeNano) {
  await copyFile(
    resolve(root, 'tests/e2e/fake-nano.js'),
    resolve(outDir, 'fake-nano.js'),
  );
  const page = resolve(outDir, 'scanner.html');
  await writeFile(
    page,
    (await readFile(page, 'utf8')).replace(
      '<script src="scanner.js">',
      '<script src="fake-nano.js"></script><script src="scanner.js">',
    ),
  );
}
if (publicBuild) {
  // Ask Chrome for nothing the published build does not use: it never
  // contacts a server, so it needs no host permissions and its pages may not
  // connect anywhere.
  const file = resolve(outDir, 'manifest.json');
  const manifest = JSON.parse(await readFile(file, 'utf8'));
  delete manifest.host_permissions;
  manifest.content_security_policy.extension_pages =
    manifest.content_security_policy.extension_pages.replace(
      /connect-src [^;]*/,
      "connect-src 'none'",
    );
  await writeFile(file, `${JSON.stringify(manifest, null, 2)}\n`);
}
console.log(
  `Load unpacked extension from: ${outDir}${fakeNano ? ' (TEST BUILD with fake on-device model)' : ''}`,
);
