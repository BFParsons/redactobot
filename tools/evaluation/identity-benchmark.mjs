/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Synthetic timing only: no corpus text, cloud calls, or Nano
 * inference.
 */

import {createServer} from 'vite';
import {mkdir, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {detectPatterns} from '../../taxonomy/taxonomy.js';
const root = resolve(import.meta.dirname, '../..');
const server = await createServer({
  root,
  configFile: false,
  appType: 'custom',
  server: {middlewareMode: true, hmr: false, watch: null, ws: false},
});
try {
  const {localFindings} = await server.ssrLoadModule(
    '/src/extension/policy.ts',
  );
  const filler =
    'The team reviewed the draft and discussed the next steps for the project. ';
  const words = filler.repeat(160).trim().split(/\s+/).slice(0, 1960).join(' ');
  const seed =
    'Record number: 42. The appointment is in seattle. Use ４２４２\u200B４２４２\u200B４２４２\u200B４２４２ for payment.';
  const samples = {
    short: seed,
    longStart: seed + '\n' + words,
    longEnd: words + '\n' + seed,
    longClean: words,
  };
  const results = [];
  for (const [name, text] of Object.entries(samples)) {
    for (const [stage, scan] of [
      [
        'threeCategories',
        t => detectPatterns(t, ['record', 'card', 'card_partial', 'places']),
      ],
      ['allLocalChecks', localFindings],
    ]) {
      const cold = performance.now();
      const findings = scan(text);
      const firstMs = performance.now() - cold;
      for (let i = 0; i < 5; i++) scan(text);
      const times = [];
      for (let i = 0; i < 40; i++) {
        const at = performance.now();
        scan(text);
        times.push(performance.now() - at);
      }
      times.sort((a, b) => a - b);
      results.push({
        name,
        stage,
        words: text.split(/\s+/).length,
        findings: findings.length,
        firstMs: +firstMs.toFixed(2),
        medianMs: +times[20].toFixed(2),
        p95Ms: +times[37].toFixed(2),
      });
    }
  }
  const path = resolve(root, 'evaluation/results/work/identity-timing.json');
  await mkdir(resolve(root, 'evaluation/results/work'), {recursive: true});
  await writeFile(
    path,
    JSON.stringify(
      {
        created: new Date().toISOString(),
        mode: 'Node deterministic checks, not browser/Nano end-to-end',
        results,
      },
      null,
      2,
    ),
  );
  console.log(JSON.stringify(results, null, 2));
} finally {
  await server.close();
}
