/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';
import {planFor, DEFAULT_FRAMEWORKS} from '../../taxonomy/taxonomy.js';
import {
  applyRedactions,
  buildDetections,
  chunkText,
  findOccurrences,
  nameCandidates,
  restore,
  unexplainedCapitals,
} from './redact';
import {SAMPLE} from './sample';

// What the on-device model actually returned in the benchmark
// (bench/RESULTS.md): full names only, plus one invented company.
const MODEL = {
  people: [
    'Priya Raman',
    'Margaret Whitfield',
    'Tom Whitfield',
    'Daniel Okafor',
  ],
  companies: [
    'Whitfield & Daughters Holdings Ltd.',
    'Harbourline Marine Supply',
    'Cascadia Credit Union',
    'Northgate Bookkeeping',
    'Whitfield Holdings',
  ],
};
const ids = planFor(DEFAULT_FRAMEWORKS).detectorIds;

describe('finding names', () => {
  it('matches across a line break', () => {
    expect(findOccurrences(SAMPLE, 'Cascadia Credit Union')).toHaveLength(1);
  });
  it('does not match inside a longer word', () => {
    expect(findOccurrences('Tomorrow Tom left.', 'Tom')).toEqual([[9, 12]]);
  });
  it('adds the short forms the model misses', () => {
    const texts = nameCandidates(MODEL).map(c => c.text);
    expect(texts).toEqual(
      expect.arrayContaining([
        'D. Okafor',
        'Okafor',
        'Margaret',
        'Tom',
        'Harbourline',
        'Northgate',
        'Cascadia',
      ]),
    );
    // shared surname: ambiguous, left to the user
    expect(texts).not.toContain('Whitfield');
  });
});

describe('the sample document', () => {
  const dets = buildDetections(SAMPLE, ids, MODEL);
  const {cleaned, map} = applyRedactions(SAMPLE, dets);

  it('drops a name the model invented', () => {
    expect(dets.some(d => d.canonical === 'Whitfield Holdings')).toBe(false);
  });
  it('leaves no name, account, amount, phone or email in what is sent', () => {
    for (const leak of [
      'Margaret',
      'Whitfield',
      'Okafor',
      'Tom ',
      'Priya',
      'Harbourline',
      'Northgate',
      'Cascadia',
      '4471',
      '5520',
      '$',
      '604-555',
      '@',
      '81234',
    ]) {
      expect(cleaned, leak).not.toContain(leak);
    }
  });
  it('keeps ordinary words and protects a city found in the offline dictionary', () => {
    expect(cleaned).not.toContain('Victoria');
    expect(dets.find(d => d.text === 'Victoria')?.kind).toBe('places');
    expect(cleaned).toContain('marine parts division');
  });
  it('gives every form of one person the same placeholder', () => {
    const ph = (t: string) =>
      applyRedactions(SAMPLE, dets).placeholders.get(
        dets.find(d => d.text === t)!.id,
      );
    expect(ph('D. Okafor')).toBe(ph('Daniel Okafor'));
    expect(ph('Margaret')).toBe(ph('Margaret Whitfield'));
    expect(ph('Harbourline')).toBe(ph('Harbourline Marine Supply'));
    expect(ph('Tom Whitfield')).not.toBe(ph('Margaret Whitfield'));
  });
  it('restores real values in an answer', () => {
    const person = [...map].find(([, v]) => v === 'Margaret Whitfield')![0];
    const amount = [...map].find(([, v]) => v === '$310,500.75')![0];
    expect(
      restore(`[${person}] moved [${amount}]. [UNKNOWN_9] stays.`, map),
    ).toBe('Margaret Whitfield moved $310,500.75. [UNKNOWN_9] stays.');
  });
  it('round-trips: restoring the cleaned text gives back every detail', () => {
    const back = restore(cleaned, map);
    for (const v of [
      'Margaret Whitfield',
      'Daniel Okafor',
      '4471-889-2203',
      '$1,250,000',
    ]) {
      expect(back).toContain(v);
    }
  });
  it('links a short form to its full name even when the model returns both', () => {
    const both = {
      people: [...MODEL.people, 'D. Okafor', 'Margaret'],
      companies: [...MODEL.companies, 'Harbourline', 'Northgate'],
    };
    const d2 = buildDetections(SAMPLE, ids, both);
    const red = applyRedactions(SAMPLE, d2);
    const ph = (t: string) =>
      red.placeholders.get(d2.find(d => d.text === t)!.id);
    expect(ph('Harbourline')).toBe(ph('Harbourline Marine Supply'));
    expect(ph('Northgate')).toBe(ph('Northgate Bookkeeping'));
    expect(ph('D. Okafor')).toBe(ph('Daniel Okafor'));
    expect(ph('Margaret')).toBe(ph('Margaret Whitfield'));
    expect(
      [...red.map.values()].filter(v => /Harbourline|Northgate/.test(v)),
    ).toEqual(['Harbourline Marine Supply', 'Northgate Bookkeeping']);
  });
  it('respects items the user switched off', () => {
    const victim = dets.find(d => d.text === '$62,000')!;
    const again = buildDetections(SAMPLE, ids, MODEL, [], new Set([victim.id]));
    expect(applyRedactions(SAMPLE, again).cleaned).toContain('$62,000');
  });
  it('lets the user add something by hand, everywhere it appears', () => {
    const again = buildDetections(SAMPLE, ids, MODEL, [
      {text: 'Victoria', kind: 'other'},
    ]);
    expect(applyRedactions(SAMPLE, again).cleaned).not.toContain('Victoria');
  });
  it('with no model at all, still finds numbers and the names that have a clear cue', () => {
    const only = applyRedactions(
      SAMPLE,
      buildDetections(SAMPLE, ids, {people: [], companies: []}),
    ).cleaned;
    expect(only).not.toContain('4471-889-2203');
    // "Prepared by Priya Raman, CPA", "Her son Tom Whitfield", "... Holdings
    // Ltd.", "... Credit Union"
    for (const cued of [
      'Priya Raman',
      'Tom Whitfield',
      'Whitfield & Daughters Holdings Ltd.',
      'Cascadia Credit',
      'Daniel Okafor',
    ]) {
      expect(only, cued).not.toContain(cued);
    }
  });
  it('finds no names when names are not part of the selected rules', () => {
    const noNames = ids.filter((id: string) => id !== 'names');
    const only = applyRedactions(
      SAMPLE,
      buildDetections(SAMPLE, noNames, {people: [], companies: []}),
    ).cleaned;
    expect(only).toContain('Margaret Whitfield');
    expect(only).not.toContain('4471-889-2203');
  });
  it('points out capitalized words nothing explained', () => {
    const left = unexplainedCapitals(SAMPLE, dets);
    expect(left).not.toContain('Victoria');
    // "the Tofino property" is now caught as a place
    expect(applyRedactions(SAMPLE, dets).cleaned).not.toContain('Tofino');
    expect(left).not.toContain('May');
  });
});

describe('chunking', () => {
  it('covers the text in order without overlap', () => {
    const text = Array.from(
      {length: 12},
      (_, i) => `Paragraph ${i} ` + 'word '.repeat(120),
    ).join('\n\n');
    const chunks = chunkText(text, 350);
    expect(chunks.length).toBeGreaterThan(3);
    for (let i = 1; i < chunks.length; i++) {
      expect(chunks[i].start).toBeGreaterThanOrEqual(chunks[i - 1].end);
    }
    expect(chunks[0].start).toBe(0);
    expect(chunks.at(-1)!.end).toBe(text.length);
  });
  it('splits one oversized paragraph, such as a spreadsheet, at line breaks and words', () => {
    const sheet = Array.from(
      {length: 200},
      (_, i) => `Row ${i}\tMargaret Whitfield\t$1,250`,
    ).join('\n');
    const long = 'word '.repeat(1000).trim();
    for (const text of [sheet, long]) {
      const chunks = chunkText(text, 350);
      expect(chunks.length).toBeGreaterThan(1);
      for (const c of chunks) {
        expect(
          (text.slice(c.start, c.end).match(/\S+/g) || []).length,
        ).toBeLessThanOrEqual(350);
      }
      for (let i = 1; i < chunks.length; i++) {
        expect(chunks[i].start).toBeGreaterThanOrEqual(chunks[i - 1].end);
      }
    }
    // Rows are never cut in half.
    for (const c of chunkText(sheet, 350)) {
      expect(sheet.slice(c.start, c.end)).toMatch(/^Row \d+[\s\S]*\$1,250$/);
    }
  });
  it('keeps a short document in one piece', () => {
    expect(chunkText(SAMPLE)).toHaveLength(1);
  });
});
