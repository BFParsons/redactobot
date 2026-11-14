/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';

import {COMMON_WORDS, GEOGRAPHY, isLargePlace} from './common-words';
import {NO_TOPICS} from './redact';
import {makeReport} from '../extension/policy';

const found = (text: string) =>
  makeReport(text, {people: [], companies: []}, NO_TOPICS, [], 'T').findings;

describe('everyday words and large places', () => {
  it('keeps common first names out of the everyday list', () => {
    for (const name of ['hope', 'grace', 'rose', 'mark', 'will', 'summer']) {
      expect(COMMON_WORDS.has(name), name).toBe(false);
    }
    for (const name of ['jordan', 'georgia', 'chad', 'israel']) {
      expect(GEOGRAPHY.has(name), name).toBe(false);
    }
  });

  it('recognises countries, continents and regions of them', () => {
    for (const place of [
      'America',
      'South America',
      'Western Europe',
      'the United States',
      'New Zealand',
      'Saudi Arabia',
    ]) {
      expect(isLargePlace(place), place).toBe(true);
    }
    for (const place of [
      'Boulder',
      'New York',
      'Georgia',
      'Payworks Midwest',
    ]) {
      expect(isLargePlace(place), place).toBe(false);
    }
  });

  it('does not treat a country or continent as a small place or a person', () => {
    expect(found('We flew back to America on Friday.')).toEqual([]);
    expect(
      found('He moved to North America in 2019 and loves the United States.'),
    ).toEqual([]);
  });

  it('still removes cities and unfamiliar company names', () => {
    const kinds = (text: string) => found(text).map(f => `${f.kind}:${f.text}`);
    expect(kinds('She lives near Denver and works in New Zealand.')).toEqual([
      'places:Denver',
    ]);
    expect(
      kinds('We switched payroll to Payworks Midwest and they filed late.'),
    ).toContain('person:Payworks Midwest');
  });
});
