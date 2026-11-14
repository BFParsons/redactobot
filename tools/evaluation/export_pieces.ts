/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Export the ~150-word paste pieces used by paste_gate_compare.ts, for outside experiments.
 * Usage: npx vite-node tools/evaluation/export_pieces.ts SOURCE_RUN OUT.json
 */

import {readdirSync, readFileSync, writeFileSync} from 'node:fs';
import {join, resolve} from 'node:path';
import {chunkText} from '../../src/core/redact';
const root = resolve(import.meta.dirname, '../..');
const [source, out] = process.argv.slice(2);
const dir = join(root, 'evaluation/results', source, 'raw');
const docs = readdirSync(dir)
  .filter(f => f.endsWith('.json'))
  .sort()
  .map(f => {
    const {text} = JSON.parse(readFileSync(join(dir, f), 'utf8'));
    return {file: f, pieces: chunkText(text, 150)};
  });
writeFileSync(out, JSON.stringify(docs));
console.log(
  `${docs.length} docs, ${docs.reduce((n, d) => n + d.pieces.length, 0)} pieces`,
);
