/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Score the paste gate's own findings (src/extension/policy.ts
 * makeReport) with and without on-device model evidence, on whole documents and
 * on paste-sized pieces.
 *
 *   npx vite-node tools/evaluation/paste_gate_compare.ts SOURCE_RUN SUFFIX
 *   REDACTOBOT_CORPUS=evaluation/corpus2 python3 -P tools/evaluation/score.py pg-det-doc-SUFFIX --json
 *
 * SOURCE_RUN supplies the imported text and the saved model output (names,
 * topics) from an earlier live run, e.g. c2-round4. Writes four runs the
 * standard scorer can read:
 *   pg-det-doc-*   rules only, whole document
 *   pg-det-paste-* rules only, each ~150-word piece checked on its own
 *   pg-nano-doc-*  rules + saved model names/places/topics, whole document
 *   pg-nano-paste-* the same per piece, with model output limited to what occurs in the piece
 * The saved model output comes from the document app's prompts, not the paste
 * gate's single-prompt extract(); treat the "nano" runs as an approximation of
 * that path.
 */

import {readdirSync, readFileSync, mkdirSync, writeFileSync} from 'node:fs';
import {join, resolve} from 'node:path';
import {makeReport} from '../../src/extension/policy';
import {
  chunkText,
  NO_TOPICS,
  type Names,
  type Topics,
} from '../../src/core/redact';

const root = resolve(import.meta.dirname, '../..');
const [source, suffix] = process.argv.slice(2);
if (!source || !suffix) {
  throw new Error('Usage: paste_gate_compare.ts SOURCE_RUN SUFFIX');
}
const rawDir = join(root, 'evaluation/results', source, 'raw');
const EMPTY: Names = {people: [], companies: []};
const PASTE_WORDS = 150;

interface Detection {
  start: number;
  end: number;
  text: string;
  kind: string;
  source: string;
  review?: boolean;
}
function scan(
  text: string,
  names: Names,
  topics: Topics,
): {detections: Detection[]; review: boolean; ms: number} {
  const started = performance.now();
  const report = makeReport(text, names, topics, [], 'EVAL');
  return {
    ms: performance.now() - started,
    review: report.needsReview,
    detections: report.findings.map(d => ({
      start: d.start,
      end: d.end,
      text: d.text,
      kind: d.kind,
      source: d.source,
      review: !!d.reviewReason,
    })),
  };
}
const within = (list: string[], piece: string) =>
  list.filter(v => piece.includes(v));

const runs = {
  'det-doc': [],
  'det-paste': [],
  'nano-doc': [],
  'nano-paste': [],
} as Record<string, any[]>;
for (const file of readdirSync(rawDir)
  .filter(f => f.endsWith('.json'))
  .sort()) {
  const saved = JSON.parse(readFileSync(join(rawDir, file), 'utf8'));
  const text: string = saved.text;
  const names: Names = saved.names ?? EMPTY;
  const topics: Topics = {...NO_TOPICS, ...(saved.topics ?? {})};
  const pieces = chunkText(text, PASTE_WORDS);
  for (const variant of Object.keys(runs)) {
    const nano = variant.startsWith('nano');
    const paste = variant.endsWith('paste');
    let detections: Detection[] = [];
    let reviews = 0;
    let ms = 0;
    if (!paste) {
      const r = scan(text, nano ? names : EMPTY, nano ? topics : NO_TOPICS);
      detections = r.detections;
      reviews = r.review ? 1 : 0;
      ms = r.ms;
    } else {
      for (const p of pieces) {
        const piece = text.slice(p.start, p.end);
        const n = nano
          ? {
              people: within(names.people, piece),
              companies: within(names.companies, piece),
            }
          : EMPTY;
        const t = nano
          ? {
              places: within(topics.places, piece),
              health: within(topics.health, piece),
              sensitive: within(topics.sensitive, piece),
              names: within(topics.names, piece),
            }
          : NO_TOPICS;
        const r = scan(piece, n, t);
        detections.push(
          ...r.detections.map(d => ({
            ...d,
            start: d.start + p.start,
            end: d.end + p.start,
          })),
        );
        reviews += r.review ? 1 : 0;
        ms += r.ms;
      }
    }
    const out = {
      id: saved.id ?? file.replace('.json', ''),
      text,
      detections,
      pieces: paste ? pieces.length : 1,
      reviews,
      ms: Math.round(ms),
    };
    const dir = join(
      root,
      'evaluation/results',
      `pg-${variant}-${suffix}`,
      'raw',
    );
    mkdirSync(dir, {recursive: true});
    writeFileSync(join(dir, file), JSON.stringify(out));
    runs[variant].push(out);
  }
}
for (const [variant, docs] of Object.entries(runs)) {
  const pieces = docs.reduce((n, d) => n + d.pieces, 0);
  const reviews = docs.reduce((n, d) => n + d.reviews, 0);
  const ms = docs.reduce((n, d) => n + d.ms, 0);
  console.log(
    `${variant}: ${docs.length} docs, ${pieces} checks, ${reviews} would ask for review (${((100 * reviews) / pieces).toFixed(1)}%), local time ${(ms / pieces).toFixed(1)} ms per check`,
  );
}
