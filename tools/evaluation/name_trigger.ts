/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Prototype: would a cheap "might contain a name" check ever skip
 * Gemini Nano on a paste that does contain a name? Measures recall on
 * paste-sized corpus pieces and the skip rate on the chat fixtures. Usage: npx
 * vite-node tools/evaluation/name_trigger.ts
 */

import {readdirSync, readFileSync} from 'node:fs';
import {join, resolve} from 'node:path';
import {chunkText} from '../../src/core/redact';
import {PASTE_FIXTURES} from '../../src/paste-fixtures';
import {mightNameSomeone} from '../../src/core/name-trigger';
const root = resolve(import.meta.dirname, '../..');
for (const corpus of ['corpus2', 'corpus3']) {
  let pieces = 0;
  let withNames = 0;
  let flagged = 0;
  const missedPieces: string[] = [];
  let cleanFlagged = 0;
  let clean = 0;
  const raw = join(
    root,
    'evaluation/results',
    corpus === 'corpus2' ? 'c2-round4' : 'c3-round4',
    'raw',
  );
  for (const f of readdirSync(raw)) {
    const {text} = JSON.parse(readFileSync(join(raw, f), 'utf8'));
    const keys = JSON.parse(
      readFileSync(join(root, 'evaluation', corpus, 'keys', f), 'utf8'),
    )
      .items.filter(
        (i: any) =>
          i.category === 'person_name' || i.category === 'organization_name',
      )
      .map((i: any) => i.value);
    for (const p of chunkText(text, 150)) {
      const piece = text.slice(p.start, p.end);
      pieces++;
      const has = keys.some((k: string) => piece.includes(k));
      const hit = mightNameSomeone(piece);
      if (has) {
        withNames++;
        if (hit) flagged++;
        else missedPieces.push(piece.slice(0, 120));
      } else {
        clean++;
        if (hit) cleanFlagged++;
      }
    }
  }
  console.log(
    `${corpus}: ${pieces} paste-sized pieces; ${withNames} contain a key name, trigger fired on ${flagged} (${((100 * flagged) / withNames).toFixed(1)}%); pieces without key names: ${clean}, trigger fired on ${cleanFlagged}`,
  );
  for (const m of missedPieces.slice(0, 3)) {
    console.log('   MISSED:', JSON.stringify(m));
  }
}
for (const f of PASTE_FIXTURES) {
  console.log(
    `fixture ${f.id.padEnd(18)} ${f.sensitive ? 'sensitive' : 'clean    '} -> ${mightNameSomeone(f.text) ? 'run Nano' : 'skip Nano'}`,
  );
}
