/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview node tools/evaluation/run_evidence_experiments.mjs [--corpora 1,3] [--out PATH]
 * Freeze proposals using corpora 1/3 before running the aggregate-only corpus 2
 * check.
 */

import {createServer} from 'vite';
import {readFile, readdir, mkdir, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {gzipSync} from 'node:zlib';

const root = resolve(import.meta.dirname, '../..');
const arg = (flag, fallback) =>
  process.argv.includes(flag)
    ? process.argv[process.argv.indexOf(flag) + 1]
    : fallback;
const corpora = arg('--corpora', '1,3').split(',').map(Number);
const out = resolve(
  root,
  arg('--out', 'evaluation/experiments/evidence-repair'),
);
const server = await createServer({
  root,
  configFile: false,
  appType: 'custom',
  server: {middlewareMode: true, hmr: false, watch: null, ws: false},
});
try {
  const {buildDetections, applyRedactions, NO_TOPICS, chunkText} =
    await server.ssrLoadModule('/src/core/redact.ts');
  const {repairEvidence, VARIANTS, boundedChunks} = await server.ssrLoadModule(
    '/tools/evaluation/evidence-experiments.ts',
  );
  await mkdir(out, {recursive: true});
  const sourceHash = createHash('sha256')
    .update(
      await readFile(resolve(root, 'tools/evaluation/evidence-experiments.ts')),
    )
    .digest('hex');
  const head = (await readFile(resolve(root, '.git/HEAD'), 'utf8')).trim();
  const commit = head.startsWith('ref: ')
    ? (await readFile(resolve(root, '.git', head.slice(5)), 'utf8')).trim()
    : head;
  for (const corpus of corpora) {
    const dir = resolve(root, `evaluation/results/c${corpus}-round4/raw`);
    const records = [];
    const timing = Object.fromEntries(VARIANTS.map(v => [v, 0]));
    let baselineDifferences = 0;
    for (const file of (await readdir(dir))
      .filter(f => /^doc-.*\.json$/.test(f))
      .sort()) {
      const saved = JSON.parse(await readFile(resolve(dir, file), 'utf8'));
      if (
        typeof saved.text !== 'string' ||
        saved.importError ||
        saved.harnessError
      ) {
        throw new Error(`Invalid saved input: ${file}`);
      }
      const {text, names, detectors: ids} = saved;
      const topics = {...NO_TOPICS, ...saved.topics};
      let started = performance.now();
      const baseline = buildDetections(text, ids, names, [], new Set(), topics);
      timing.baseline += performance.now() - started;
      const shape = ds =>
        ds.map(d => [
          d.start,
          d.end,
          d.kind,
          d.enabled ?? d.defaultOn ?? !['health', 'sensitive'].includes(d.kind),
        ]);
      if (
        JSON.stringify(shape(baseline)) !==
        JSON.stringify(shape(saved.detections))
      ) {
        baselineDifferences++;
      }
      const variants = {};
      for (const variant of VARIANTS) {
        started = performance.now();
        const detections = repairEvidence(
          text,
          ids,
          names,
          topics,
          baseline,
          variant,
        );
        timing[variant] += performance.now() - started;
        let end = 0;
        for (const d of detections) {
          if (
            d.start < end ||
            d.end > text.length ||
            d.start >= d.end ||
            text.slice(d.start, d.end) !== d.text
          ) {
            throw new Error(`Invalid span: ${file}/${variant}`);
          }
          end = d.end;
        }
        const redaction = applyRedactions(text, detections);
        if (
          redaction.placeholders.size !==
          detections.filter(d => d.enabled).length
        ) {
          throw new Error('Skipped replacement');
        }
        // Python indexes Unicode code points, JS uses UTF-16. Convert before
        // scoring.
        const cp = offset => [...text.slice(0, offset)].length;
        variants[variant] = detections.map(d => ({
          ...d,
          start: cp(d.start),
          end: cp(d.end),
        }));
      }
      const counts = cs =>
        cs.map(c => (text.slice(c.start, c.end).match(/\S+/g) ?? []).length);
      records.push({
        id: saved.id,
        variants,
        chunks: {
          old: counts(chunkText(text)),
          bounded: counts(boundedChunks(text)),
        },
      });
    }
    const result = {
      corpus,
      sourceHash,
      commit,
      baselineDifferences,
      timingMs: timing,
      records,
    };
    await writeFile(
      resolve(out, `c${corpus}.json.gz`),
      gzipSync(JSON.stringify(result)),
    );
    console.log(
      JSON.stringify({
        corpus,
        documents: records.length,
        baselineDifferences,
        sourceHash,
        timingMs: timing,
      }),
    );
  }
} finally {
  await server.close();
}
