/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Re-run local code against an immutable import snapshot and
 * saved Nano evidence. This is a development replay, never another
 * independent/held-out evaluation.
 */

import {createServer} from 'vite';
import {readFile, writeFile, mkdir, copyFile} from 'node:fs/promises';
import {resolve, join} from 'node:path';
import {createHash} from 'node:crypto';
const root = resolve(import.meta.dirname, '../..');
const original = resolve(process.argv[2]);
const localOnly = process.argv.includes('--local-only');
const out = join(
  original,
  `replay-${new Date().toISOString().replace(/[:.]/g, '-')}`,
);
const read = async path => JSON.parse(await readFile(path, 'utf8'));
const manifest = await read(join(original, 'manifest.json'));
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const sourceHashes = Object.fromEntries(
  await Promise.all(
    Object.keys(manifest.sourceHashes).map(async path => [
      path,
      hash(await readFile(join(root, path))),
    ]),
  ),
);
if (
  !localOnly &&
  (sourceHashes['src/extension/model.ts'] !==
    manifest.sourceHashes['src/extension/model.ts'] ||
    sourceHashes['src/core/firebase-local.ts'] !==
      manifest.sourceHashes['src/core/firebase-local.ts'])
) {
  throw new Error('Inference changed; a replay is not a fresh model test.');
}
await mkdir(join(out, 'local'), {recursive: true});
await mkdir(join(out, 'nano'), {recursive: true});
await copyFile(join(original, 'answerkey.csv'), join(out, 'answerkey.csv'));
await writeFile(
  join(out, 'manifest.json'),
  JSON.stringify(
    {
      ...manifest,
      sourceHashes,
      replayOf: original,
      replayCreated: new Date().toISOString(),
      note: localOnly
        ? 'Local-only development replay. No Nano inference, evidence replay or cloud requests.'
        : 'Development replay after inspecting this corpus. Nano evidence is unchanged from the original run; no new inference or cloud requests.',
    },
    null,
    2,
  ),
);
const server = await createServer({
  root,
  configFile: false,
  appType: 'custom',
  server: {middlewareMode: true, hmr: false, watch: null, ws: false},
});
try {
  const {localFindings, makeReport} = await server.ssrLoadModule(
    '/src/extension/policy.ts',
  );
  const {applyRedactions, NO_TOPICS} = await server.ssrLoadModule(
    '/src/core/redact.ts',
  );
  const {prepareCloudInput} = await server.ssrLoadModule(
    '/src/core/cloud-gate.ts',
  );
  let nano = 0;
  for (const file of manifest.files.filter(file => file.index != null)) {
    const local = await read(join(original, 'local', `${file.index}.json`));
    const at = performance.now();
    const findings = localFindings(local.text);
    const elapsedMs = performance.now() - at;
    await writeFile(
      join(out, 'local', `${file.index}.json`),
      JSON.stringify(
        {
          ...local,
          findings,
          elapsedMs,
          cleaned: applyRedactions(local.text, findings).cleaned,
        },
        null,
        2,
      ),
    );
    if (localOnly) continue;
    let saved;
    try {
      saved = await read(join(original, 'nano', `${file.index}.json`));
    } catch (error) {
      if (error.code === 'ENOENT') continue;
      throw error;
    }
    const evidence = saved.evidence ?? {
      names: {people: [], companies: []},
      topics: NO_TOPICS,
      ambiguous: [],
      identifying: [],
    };
    const replayAt = performance.now();
    const report = makeReport(
      local.text,
      evidence.names,
      evidence.topics,
      evidence.ambiguous,
      'CORPUS',
      saved.report.complete,
      saved.failure,
      evidence.identifying,
    );
    let gate = report.needsReview ? 'held-for-review' : 'eligible';
    let gateReason;
    if (!report.needsReview) {
      try {
        prepareCloudInput(local.text, report, 'CORPUS');
      } catch (error) {
        gate = 'held-by-final-check';
        gateReason = error.message;
      }
    }
    await writeFile(
      join(out, 'nano', `${file.index}.json`),
      JSON.stringify(
        {
          ...saved,
          report,
          gate,
          gateReason,
          replayMs: performance.now() - replayAt,
        },
        null,
        2,
      ),
    );
    nano++;
  }
  await writeFile(
    join(root, 'evaluation/results/work/desktop-replay.json'),
    JSON.stringify({out, original, nano}, null, 2),
  );
  console.log(
    JSON.stringify({
      out,
      local: manifest.files.length,
      savedNanoReplayed: nano,
    }),
  );
} finally {
  await server.close();
}
