/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Compare labels and verify identical redaction coverage against an unchanged checkout.
 * node tools/evaluation/check_categories.mjs --baseline C:/path/to/baseline --corpora 1,3 [--out review.json]
 * Corpus 2 is aggregate-only: its text, IDs and individual changes are never
 * exported.
 */

import {createServer} from 'vite';
import {readFile, readdir, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';

const arg = (flag, fallback) =>
  process.argv.includes(flag)
    ? process.argv[process.argv.indexOf(flag) + 1]
    : fallback;
const baselineRoot = arg('--baseline');
if (!baselineRoot) {
  throw new Error('Pass --baseline with an unchanged checkout.');
}
const root = resolve(import.meta.dirname, '../..');
const corpora = arg('--corpora', '1,3').split(',').map(Number);
if (corpora.some(c => ![1, 2, 3].includes(c))) {
  throw new Error('Corpora must be 1, 2 or 3.');
}
const servers = [];
const review = [];
const summary = [];
try {
  for (const location of [baselineRoot, root]) {
    servers.push(
      await createServer({
        root: resolve(location),
        configFile: false,
        cacheDir: resolve(location, 'node_modules/.vite-category-check'),
        appType: 'custom',
        server: {middlewareMode: true, hmr: false, watch: null, ws: false},
      }),
    );
  }
  const [before, after] = await Promise.all(
    servers.map(s => s.ssrLoadModule('/src/core/redact.ts')),
  );
  const coverage = ds =>
    JSON.stringify(ds.map(d => [d.id, d.start, d.end, d.defaultOn, d.enabled]));
  // Entities already share placeholders across capitalization and whitespace
  // variants. Compare their meaning, not whether "SEATTLE" restores with the
  // case of "Seattle".
  const valueKey = s => s?.replace(/\s+/g, ' ').trim().toLowerCase();
  for (const corpus of corpora) {
    const dir = resolve(root, `evaluation/results/c${corpus}-round4/raw`);
    const totals = {
      corpus,
      documents: 0,
      runs: 0,
      replacements: 0,
      categoryChanges: 0,
      transitions: {},
      elapsedMs: {},
    };
    let oldMs = 0;
    let newMs = 0;
    for (const file of (await readdir(dir))
      .filter(f => /^doc-.*\.json$/.test(f))
      .sort()) {
      const saved = JSON.parse(await readFile(resolve(dir, file), 'utf8'));
      if (
        typeof saved.text !== 'string' ||
        saved.importError ||
        saved.harnessError
      ) {
        throw new Error(`Invalid input in corpus ${corpus}`);
      }
      totals.documents++;
      for (const mode of ['model', 'patterns']) {
        const names =
          mode === 'model' ? saved.names : {people: [], companies: []};
        const topics =
          mode === 'model'
            ? {...before.NO_TOPICS, ...saved.topics}
            : before.NO_TOPICS;
        let started = performance.now();
        const old = before.buildDetections(
          saved.text,
          saved.detectors,
          names,
          [],
          new Set(),
          topics,
        );
        oldMs += performance.now() - started;
        started = performance.now();
        const now = after.buildDetections(
          saved.text,
          saved.detectors,
          names,
          [],
          new Set(),
          topics,
        );
        newMs += performance.now() - started;
        if (coverage(old) !== coverage(now)) {
          throw new Error(
            `Redaction coverage or selection changed in corpus ${corpus} (${mode}).`,
          );
        }
        const red = after.applyRedactions(saved.text, now);
        const oldRed = before.applyRedactions(saved.text, old);
        if (red.placeholders.size !== now.filter(d => d.enabled).length) {
          throw new Error('A replacement was skipped.');
        }
        for (const d of now) {
          if (d.text !== saved.text.slice(d.start, d.end)) {
            throw new Error('Invalid span.');
          }
          const ph = red.placeholders.get(d.id);
          if (
            ph &&
            (!ph.startsWith(d.base + '_') ||
              valueKey(red.map.get(ph)) !== valueKey(d.canonical))
          ) {
            const previous = old.find(x => x.id === d.id);
            const oldPh = oldRed.placeholders.get(d.id);
            const wasConflicting =
              oldPh &&
              (!oldPh.startsWith(previous.base + '_') ||
                valueKey(oldRed.map.get(oldPh)) !==
                  valueKey(previous.canonical));
            if (!wasConflicting) {
              throw new Error(
                'New conflicting placeholder identity.' +
                  (corpus === 2
                    ? ''
                    : JSON.stringify({
                        file,
                        mode,
                        detection: d,
                        restored: red.map.get(ph),
                      })),
              );
            }
          }
        }
        totals.runs++;
        totals.replacements += now.filter(d => d.enabled).length;
        for (let i = 0; i < old.length; i++) {
          if (old[i].kind === now[i].kind) continue;
          totals.categoryChanges++;
          const transition = `${old[i].kind} -> ${now[i].kind}`;
          totals.transitions[transition] =
            (totals.transitions[transition] ?? 0) + 1;
          if (corpus !== 2) {
            review.push({
              corpus,
              file,
              mode,
              transition,
              text: now[i].text,
              oldCanonical: old[i].canonical,
              canonical: now[i].canonical,
              context: saved.text.slice(
                Math.max(0, now[i].start - 60),
                Math.min(saved.text.length, now[i].end + 60),
              ),
            });
          }
        }
      }
    }
    totals.elapsedMs = {
      baseline: Math.round(oldMs),
      candidate: Math.round(newMs),
    };
    summary.push(totals);
    console.log(JSON.stringify(totals));
  }
  if (arg('--out')) {
    await writeFile(
      resolve(arg('--out')),
      JSON.stringify({summary, review}, null, 2),
    );
  }
} finally {
  await Promise.all(servers.map(s => s.close()));
}
