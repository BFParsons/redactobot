/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Detection must never throw, whatever the text. A name followed
 * directly by a hyphen ("John Smith- the client") once crashed the name rules,
 * which left the app's main button looking dead. These tests feed the detector
 * deliberately mangled text.
 */

import {describe, expect, it} from 'vitest';

import {makeReport} from '../extension/policy';
import {DEFAULT_CLASSES, planForClasses} from '../../taxonomy/taxonomy.js';

import {
  applyRedactions,
  buildDetections,
  NO_TOPICS,
  unexplainedCapitals,
} from './redact';
import {SAMPLES} from './samples';

const ids: string[] = planForClasses(DEFAULT_CLASSES).detectorIds;
const none = {people: [] as string[], companies: [] as string[]};

function runAll(text: string, names = none) {
  const detections = buildDetections(
    text,
    ids,
    names,
    [],
    new Set(),
    NO_TOPICS,
  );
  applyRedactions(text, detections);
  unexplainedCapitals(text, detections);
  makeReport(text, names, NO_TOPICS, [], 'T');
  return detections;
}

describe('detection never throws', () => {
  it('handles a name followed directly by a hyphen or apostrophe', () => {
    for (const text of [
      'I spoke with his partner John Smith- the client was happy.',
      'Yesterday Dr. Maria Lopez- said hello.',
      'We met Anna de la Cruz- and Nik van der Giesen- at noon.',
      'Prepared by: Renee Calloway-\nnext line',
      "Her son Tom O'- called. Notes by Jean-- Luc and Mr. Brown--.",
    ]) {
      expect(() => runAll(text), text).not.toThrow();
      expect(
        () =>
          runAll(text, {
            people: ['John Smith-', 'Maria Lopez-', "Tom O'-", 'Jean--', 'A -'],
            companies: ['Brown--'],
          }),
        text,
      ).not.toThrow();
    }
  });

  it('still finds the name when a hyphen follows it', () => {
    const found = runAll('I spoke with his partner John Smith- the client.');
    expect(
      found.some(d => d.kind === 'person' && d.text.startsWith('John Smith')),
    ).toBe(true);
  });

  it('survives 150 mangled texts', {timeout: 60_000}, () => {
    // A fixed seed, so a failure can be reproduced.
    let seed = 20261115;
    const random = () => {
      seed = (seed * 1103515245 + 12345) & 0x7fffffff;
      return seed / 0x7fffffff;
    };
    const pick = <T>(list: T[]) => list[Math.floor(random() * list.length)];
    const junk = [
      '-',
      '--',
      "'",
      '’',
      '.',
      ',',
      ' -',
      '- ',
      '\n',
      '\t',
      '(',
      ')',
      '/',
      '&',
      '"',
      ':',
      '—',
      '–',
      ' ',
      '[',
      ']',
      '|',
      '\r\n',
      ' van ',
      ' de ',
      ' Jr.',
      ' III',
      'Mc',
      "O'",
      '..',
      '-\n',
      'é',
      '?',
    ];
    const failures: string[] = [];
    for (let i = 0; i < 150; i++) {
      const source = pick(SAMPLES).text;
      let text = source.slice(Math.floor(random() * source.length * 0.6));
      text = text.slice(0, 80 + Math.floor(random() * 400));
      for (let edits = 1 + Math.floor(random() * 12); edits > 0; edits--) {
        const words = [...text.matchAll(/\p{Lu}[\p{L}'’-]*/gu)];
        const word = words.length ? pick(words) : undefined;
        const at =
          word && random() < 0.75
            ? word.index + (random() < 0.7 ? word[0].length : 0)
            : Math.floor(random() * text.length);
        text =
          random() < 0.7
            ? text.slice(0, at) + pick(junk) + text.slice(at)
            : text.slice(0, at) + text.slice(at + 1 + Math.floor(random() * 3));
      }
      const names =
        random() < 0.5
          ? none
          : {
              people: [
                ...text.matchAll(/\p{Lu}[\p{L}'’-]*(?: \p{Lu}[\p{L}'’-]*)?/gu),
              ]
                .slice(0, 6)
                .map(m => m[0]),
              companies: [],
            };
      try {
        runAll(text, names);
      } catch (error) {
        failures.push(`${(error as Error).message} :: ${JSON.stringify(text)}`);
      }
    }
    expect(failures.slice(0, 3)).toEqual([]);
  });
});
