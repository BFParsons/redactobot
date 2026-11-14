/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Builds the extension for publication and zips it for the
 * Chrome Web Store and for GitHub releases.
 *
 *   npm run package:extension
 *
 * The published build has no Firebase project and no App Check debug token,
 * asks for no host permissions and cannot connect to any server: it checks
 * pastes on the device only. Cloud cleanup is offered on redactobot.org.
 */

import {spawnSync} from 'node:child_process';
import {
  mkdirSync,
  readdirSync,
  readFileSync,
  rmSync,
  statSync,
  writeFileSync,
} from 'node:fs';
import {dirname, join, relative, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {zipSync} from 'fflate';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const outDir = resolve(root, 'extension/public-build');
rmSync(outDir, {recursive: true, force: true});
const built = spawnSync(
  process.execPath,
  ['tools/build_extension.mjs', '--public', '--out', outDir],
  {cwd: root, stdio: 'inherit'},
);
if (built.status !== 0) process.exit(built.status ?? 1);

const files = {};
const walk = dir => {
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) {
      walk(path);
    } else {
      files[relative(outDir, path).replaceAll('\\', '/')] = readFileSync(path);
    }
  }
};
walk(outDir);

// Never ship a secret: refuse if any build output mentions a debug token value
// or a Firebase key.
for (const [name, bytes] of Object.entries(files)) {
  const text = bytes.toString('latin1');
  if (/AIza[0-9A-Za-z_-]{35}/.test(text)) {
    throw new Error(`${name} contains a Firebase API key. Not packaging.`);
  }
}
const manifest = JSON.parse(files['manifest.json'].toString('utf8'));
if (manifest.host_permissions) {
  throw new Error('The published manifest must not ask for host permissions.');
}

const releases = resolve(root, 'extension/releases');
mkdirSync(releases, {recursive: true});
const zipPath = join(releases, `redactobot-extension-${manifest.version}.zip`);
writeFileSync(zipPath, zipSync(files, {level: 9}));
console.log(
  `Packaged ${Object.keys(files).length} files, version ${manifest.version}: ${zipPath}`,
);
