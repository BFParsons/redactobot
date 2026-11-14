/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Simulate when the paste gate should call Gemini Nano, using the rules' own coverage as the
 * confidence signal (no second model). Needs pg-det-paste-SUFFIX and
 * pg-nano-paste-SUFFIX from paste_gate_compare.ts. For each ~150-word piece a
 * policy decides "call Nano"; routed pieces use rules + Nano findings, the rest
 * rules only. Writes pg-<policy>-paste-SUFFIX runs for score.py.
 *   npx vite-node tools/evaluation/routing_compare.ts SUFFIX
 */

import {mkdirSync, readdirSync, readFileSync, writeFileSync} from 'node:fs';
import {join, resolve} from 'node:path';
import {chunkText} from '../../src/core/redact';
import {
  mightNameSomeone,
  unexplainedNameCandidates,
} from '../../src/core/name-trigger';
import {sensitiveTerms} from '../../src/core/sensitive-terms';
import {identityContexts} from '../../src/core/privacy-buckets';
import {GIVEN_NAMES} from '../../src/core/given-names';
import {SSA_GIVEN_NAMES} from '../../src/core/given-names-ssa';
const nameLooking = (w: string) =>
  /^(?:\p{Lu}\.){1,3}$/u.test(w) ||
  /^\p{Lu}{2,3}$/u.test(w) ||
  GIVEN_NAMES.has(w.toLowerCase()) ||
  SSA_GIVEN_NAMES.has(w.toLowerCase());

const root = resolve(import.meta.dirname, '../..');
const suffix = process.argv[2];
const results = join(root, 'evaluation/results');
interface Span {
  start: number;
  end: number;
}
const sensitive = (t: string) =>
  sensitiveTerms(t, true).length > 0 || identityContexts(t).length > 0;
const POLICIES: Record<string, (piece: string, rules: Span[]) => boolean> = {
  always: () => true, // rules + Nano on every paste
  // today's modelNeeded()
  gate: piece => mightNameSomeone(piece) || sensitive(piece),
  unexplained: (piece, rules) =>
    unexplainedNameCandidates(piece, rules).length > 0,
  'unexplained+sens': (piece, rules) =>
    unexplainedNameCandidates(piece, rules).length > 0 || sensitive(piece),
  'unexplained2+sens': (piece, rules) =>
    unexplainedNameCandidates(piece, rules).length >= 2 || sensitive(piece),
};
const calls: Record<string, number> = Object.fromEntries(
  Object.keys(POLICIES).map(k => [k, 0]),
);
let pieces = 0;
for (const file of readdirSync(
  join(results, `pg-det-paste-${suffix}`, 'raw'),
).sort()) {
  const det = JSON.parse(
    readFileSync(join(results, `pg-det-paste-${suffix}`, 'raw', file), 'utf8'),
  );
  const nano = JSON.parse(
    readFileSync(join(results, `pg-nano-paste-${suffix}`, 'raw', file), 'utf8'),
  );
  const text: string = det.text;
  const out: Record<string, any[]> = Object.fromEntries(
    Object.keys(POLICIES).map(k => [k, []]),
  );
  for (const p of chunkText(text, 150)) {
    pieces++;
    const inPiece = (d: Span) => d.start >= p.start && d.start < p.end;
    const rules = det.detections.filter(inPiece);
    const withNano = nano.detections.filter(inPiece);
    const local = rules.map((d: Span) => ({
      start: d.start - p.start,
      end: d.end - p.start,
    }));
    const piece = text.slice(p.start, p.end);
    for (const [name, policy] of Object.entries(POLICIES)) {
      const routed = policy(piece, local);
      if (routed) calls[name]++;
      out[name].push(...(routed ? withNano : rules));
    }
  }
  for (const name of Object.keys(POLICIES)) {
    const dir = join(
      results,
      `pg-r-${name.replace(/\+/g, 'S')}-paste-${suffix}`,
      'raw',
    );
    mkdirSync(dir, {recursive: true});
    writeFileSync(
      join(dir, file),
      JSON.stringify({id: det.id, text, detections: out[name]}),
    );
  }
}
// Budgeted variants: rank pieces by how many possible names the rules left
// unexplained, and call Nano only on the top share; a seeded random ranking at
// the same budget is the control.
interface Piece {
  file: string;
  start: number;
  end: number;
  score: number;
}
const all: Piece[] = [];
for (const file of readdirSync(
  join(results, `pg-det-paste-${suffix}`, 'raw'),
).sort()) {
  const det = JSON.parse(
    readFileSync(join(results, `pg-det-paste-${suffix}`, 'raw', file), 'utf8'),
  );
  for (const p of chunkText(det.text, 150)) {
    const local = det.detections
      .filter((d: Span) => d.start >= p.start && d.start < p.end)
      .map((d: Span) => ({start: d.start - p.start, end: d.end - p.start}));
    all.push({
      file,
      start: p.start,
      end: p.end,
      score: unexplainedNameCandidates(
        det.text.slice(p.start, p.end),
        local,
      ).filter(c =>
        process.env.SIGNAL === 'names' ? nameLooking(c.word) : true,
      ).length,
    });
  }
}
let seed = 7;
const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const randomOrder = all
  .map(p => ({p, r: rand()}))
  .sort((a, b) => a.r - b.r)
  .map(x => x.p);
const ranked = [...all].sort((a, b) => b.score - a.score);
for (const [label, order] of [
  ['rank', ranked],
  ['rand', randomOrder],
] as const) {
  for (const pct of [10, 25, 50]) {
    const routed = new Set(
      order.slice(0, Math.round((order.length * pct) / 100)),
    );
    const byFile = new Map<string, Piece[]>();
    for (const p of all) byFile.set(p.file, [...(byFile.get(p.file) ?? []), p]);
    for (const [file, ps] of byFile) {
      const det = JSON.parse(
        readFileSync(
          join(results, `pg-det-paste-${suffix}`, 'raw', file),
          'utf8',
        ),
      );
      const nano = JSON.parse(
        readFileSync(
          join(results, `pg-nano-paste-${suffix}`, 'raw', file),
          'utf8',
        ),
      );
      const dets: Span[] = [];
      for (const p of ps) {
        const inP = (d: Span) => d.start >= p.start && d.start < p.end;
        dets.push(
          ...(routed.has(p)
            ? nano.detections.filter(inP)
            : det.detections.filter(inP)),
        );
      }
      const dir = join(results, `pg-${label}${pct}-paste-${suffix}`, 'raw');
      mkdirSync(dir, {recursive: true});
      writeFileSync(
        join(dir, file),
        JSON.stringify({id: det.id, text: det.text, detections: dets}),
      );
    }
  }
}
for (const [name, n] of Object.entries(calls)) {
  console.log(
    `${suffix} ${name.padEnd(18)} Nano on ${n}/${pieces} pieces (${((100 * n) / pieces).toFixed(0)}%) -> run pg-r-${name.replace(/\+/g, 'S')}-paste-${suffix}`,
  );
}
