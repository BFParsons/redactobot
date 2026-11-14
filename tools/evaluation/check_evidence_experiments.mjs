/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Behavioral controls for the offline proposals. Run with Node
 * from the repository root.
 */

import assert from 'node:assert/strict';
import {writeFile, mkdir} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createServer} from 'vite';

const root = resolve(import.meta.dirname, '../..');
const server = await createServer({
  root,
  configFile: false,
  appType: 'custom',
  server: {middlewareMode: true, hmr: false, watch: null, ws: false},
});
try {
  const {buildDetections, NO_TOPICS, applyRedactions, restore, chunkText} =
    await server.ssrLoadModule('/src/core/redact.ts');
  const {repairEvidence, VARIANTS, normalizedOccurrences, boundedChunks} =
    await server.ssrLoadModule('/tools/evaluation/evidence-experiments.ts');
  const ids = ['names', 'places'];
  const empty = {people: [], companies: []};
  const measure = (text, names, topics = NO_TOPICS) => {
    const base = buildDetections(text, ids, names, [], new Set(), topics);
    return Object.fromEntries(
      VARIANTS.map(v => [v, repairEvidence(text, ids, names, topics, base, v)]),
    );
  };
  const covered = (ds, start, end) =>
    Array.from({length: end - start}, (_, i) => start + i).every(i =>
      ds.some(d => d.enabled && d.start <= i && d.end > i),
    );
  const positive = [];
  const negative = [];
  const people = [
    'Orla M. Fenwick',
    'Noé D’Arvieux',
    'Zélie Hart‐Ellison',
    'Inez J. Bellamy',
  ];
  const changes = {
    original: s => s,
    lowercase: s => s.toLowerCase(),
    uppercase: s => s.toUpperCase(),
    decomposed: s => s.normalize('NFD'),
    apostrophe: s => s.replaceAll('’', "'"),
    hyphen: s => s.replaceAll('‐', '-'),
    linebreak: s => s.replaceAll(' ', '\n'),
    nonbreaking_space: s => s.replaceAll(' ', '\u00a0'),
  };
  for (const person of people) {
    for (const [form, change] of Object.entries(changes)) {
      const actual = change(person);
      for (const output of ['verbatim', 'normalized']) {
        const text = `we spoke with ${actual} yesterday.`;
        const ds = measure(text, {
          people: [output === 'verbatim' ? actual : person],
          companies: [],
        });
        positive.push({
          label: `${person}/${form}/${output}`,
          results: Object.fromEntries(
            VARIANTS.map(v => [v, covered(ds[v], 14, 14 + actual.length)]),
          ),
        });
      }
    }
  }
  for (const [kind, value, prefix] of [
    ['company', 'elm lantern childcare', 'payment for '],
    ['company', 'hollow fern joinery', 'paid '],
    ['places', 'brindlewick', 'the move to '],
    ['places', 'new thornhaven', 'resident in '],
  ]) {
    const text = `${prefix}${value} was recorded.`;
    const ds = measure(
      text,
      kind === 'company' ? {people: [], companies: [value]} : empty,
      kind === 'places' ? {...NO_TOPICS, places: [value]} : NO_TOPICS,
    );
    positive.push({
      label: value,
      results: Object.fromEntries(
        VARIANTS.map(v => [
          v,
          covered(ds[v], prefix.length, prefix.length + value.length),
        ]),
      ),
    });
  }
  for (const [kind, value, text] of [
    ['person', 'family doctor', 'the family doctor called.'],
    ['person', 'regular meeting', 'the regular meeting ended.'],
    ['person', 'May', 'Payment is due in May.'],
    ['person', 'will', 'the will was filed.'],
    ['person', 'bill', 'please pay the bill.'],
    ['person', 'none', 'Client: none'],
    ['company', 'trust company', 'choose a trust company.'],
    ['company', 'petty cash', 'we reviewed petty cash.'],
    ['company', 'university bookstore', 'visit the university bookstore.'],
    [
      'company',
      'United States District Court',
      'Filed in United States District Court.',
    ],
    ['places', 'reading', 'her reading improved.'],
    ['places', 'union hall', 'meet at the union hall.'],
    ['person', 'Orla M. Fenwick', 'The document contains no person names.'],
  ]) {
    const names = {
      people: kind === 'person' ? [value] : [],
      companies: kind === 'company' ? [value] : [],
    };
    const ds = measure(
      text,
      names,
      kind === 'places' ? {...NO_TOPICS, places: [value]} : NO_TOPICS,
    );
    const start = text.indexOf(value);
    negative.push({
      label: value,
      results: Object.fromEntries(
        VARIANTS.map(v => [
          v,
          start >= 0 &&
            ds[v].some(
              d => d.enabled && d.start < start + value.length && d.end > start,
            ),
        ]),
      ),
    });
  }

  // Offset correctness includes astral characters, decomposed accents, and
  // whitespace expansion.
  const unicode = '🪴 client: Zoe\u0308 D’Arvieux\n  Fenwick.';
  const [[a, b]] = normalizedOccurrences(unicode, "Zoë D'Arvieux Fenwick");
  assert.equal(unicode.slice(a, b), 'Zoe\u0308 D’Arvieux\n  Fenwick');
  assert.deepEqual(normalizedOccurrences('Fenwicker', 'Fenwick'), []);
  // accents are not blindly stripped
  assert.deepEqual(normalizedOccurrences('é', 'e'), []);

  const text = 'orla m. fenwick signed.';
  const names = {people: ['orla m. fenwick'], companies: []};
  const manual = buildDetections(text, ids, empty, [
    {text: 'orla', kind: 'person'},
  ]);
  const protectedManual = repairEvidence(
    text,
    ids,
    names,
    NO_TOPICS,
    manual,
    'combined',
  );
  assert.equal(protectedManual.find(d => d.text === 'orla')?.source, 'manual');
  assert.ok(!protectedManual.some(d => d.text === 'orla m. fenwick'));
  const off = manual.map(d => ({...d, source: 'model', enabled: false}));
  assert.ok(
    !repairEvidence(text, ids, names, NO_TOPICS, off, 'combined').some(
      d => d.enabled,
    ),
  );
  assert.deepEqual(
    repairEvidence(text, [], names, NO_TOPICS, [], 'combined'),
    [],
  );
  assert.deepEqual(
    repairEvidence(
      'resident in Virginia.',
      ['places'],
      empty,
      {...NO_TOPICS, places: ['Virginia']},
      [],
      'combined',
    ),
    [],
  );
  const fixed = repairEvidence(
    text,
    ids,
    names,
    NO_TOPICS,
    buildDetections(text, ids, names),
    'combined',
  );
  const redacted = applyRedactions(text, fixed);
  assert.equal(restore(redacted.cleaned, redacted.map), text);

  const long = Array.from({length: 2000}, (_, i) => `word${i}`).join(' ');
  const old = chunkText(long);
  const chunks = boundedChunks(long);
  assert.equal(old.length, 1);
  assert.ok(
    chunks.every(c => long.slice(c.start, c.end).split(' ').length <= 350),
  );
  assert.equal(chunks[0].start, 0);
  assert.equal(chunks.at(-1).end, long.length);
  for (let i = 1; i < chunks.length; i++) {
    assert.ok(chunks[i].start < chunks[i - 1].end);
  }
  assert.deepEqual(boundedChunks(''), []);
  assert.throws(() => boundedChunks(long, 24, 24));

  const references =
    'File QZ-2026-001. File QZ-2026-002. Follow-ups QZ-2026-003 and QZ-26-004. Quote AB-2026-005.';
  // Supply only explicitly labelled seeds to isolate the memory mechanism from
  // generic ID rules.
  const referencesBase = buildDetections(references, ['record'], empty).filter(
    d => d.text === 'QZ-2026-001' || d.text === 'QZ-2026-002',
  );
  const referencesFixed = repairEvidence(
    references,
    ['record'],
    empty,
    NO_TOPICS,
    referencesBase,
    'identifier-memory',
  );
  assert.ok(referencesFixed.some(d => d.text === 'QZ-2026-003'));
  assert.ok(
    !referencesFixed.some(
      d => d.text === 'QZ-26-004' || d.text === 'AB-2026-005',
    ),
  );
  const single = 'File QZ-2026-001. Follow-up QZ-2026-003.';
  assert.deepEqual(
    repairEvidence(
      single,
      ['record'],
      empty,
      NO_TOPICS,
      buildDetections(single, ['record'], empty),
      'identifier-memory',
    ),
    buildDetections(single, ['record'], empty),
  );

  const summary = Object.fromEntries(
    VARIANTS.map(v => [
      v,
      {
        positive_caught: positive.filter(p => p.results[v]).length,
        positive_total: positive.length,
        negative_false_hits: negative.filter(p => p.results[v]).length,
        negative_total: negative.length,
      },
    ]),
  );
  const out = resolve(root, 'evaluation/experiments/evidence-repair');
  await mkdir(out, {recursive: true});
  await writeFile(
    resolve(out, 'behavioral.json'),
    JSON.stringify(
      {
        summary,
        positive,
        negative,
        invariants: 'passed',
        chunking: {
          old_max_words: 2000,
          bounded_max_words: 350,
          chunks: chunks.length,
        },
      },
      null,
      2,
    ) + '\n',
  );
  console.log(JSON.stringify({summary, invariants: 'passed'}, null, 2));
} finally {
  await server.close();
}
