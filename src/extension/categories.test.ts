/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {expect, it} from 'vitest';
import {
  ALL_CATEGORIES,
  COMMON_CATEGORIES,
  normalizeCategories,
  selectedDetectors,
  selectedModelKinds,
  type PasteCategory,
} from './categories';
import {GUARD_DETECTORS, localFindings, makeReport} from './policy';
import {NO_TOPICS} from '../core/redact';
import {prepareCloudInput} from '../core/cloud-gate';

const names = {people: ['Avery Bennett'], companies: []};
const report = (text: string, categories: readonly PasteCategory[]) =>
  makeReport(
    text,
    names,
    NO_TOPICS,
    [],
    'TEST',
    true,
    undefined,
    [],
    categories,
  );

it('preserves every existing detector by default and gives every model category a home', () => {
  expect(selectedDetectors(ALL_CATEGORIES).sort()).toEqual(
    [...GUARD_DETECTORS].sort(),
  );
  expect(selectedModelKinds(ALL_CATEGORIES).sort()).toEqual(
    [
      'person',
      'company',
      'place',
      'health',
      'sensitive',
      'identifying',
      'uncertain',
    ].sort(),
  );
});
it.each([undefined, null, {}, 'contact', ['unknown'], ['contact', 1]])(
  'keeps coverage for absent or corrupt preferences: %j',
  value => {
    expect(normalizeCategories(value)).toEqual(ALL_CATEGORIES);
  },
);
it('accepts an intentional empty selection and copies saved arrays into an immutable snapshot', () => {
  expect(normalizeCategories([])).toEqual([]);
  const saved = ['contact', 'contact'];
  const snapshot = normalizeCategories(saved);
  saved.push('names');
  expect(snapshot).toEqual(['contact']);
  expect(Object.isFrozen(snapshot)).toBe(true);
});
it.each([
  ['names', 'Contact: Avery Bennett.', 'Avery Bennett'],
  ['contact', 'Email: avery@example.com.', 'avery@example.com'],
  ['places', 'City: Seattle.', 'Seattle'],
  ['records', 'MRN: 42.', '42'],
  ['payments', 'Card: 4111 1111 1111 1111.', '4111 1111 1111 1111'],
  ['credentials', 'Password: Maple_42!', 'Maple_42'],
  ['online', 'See https://example.com/private.', 'https://example.com/private'],
  ['dates', 'Date: March 14, 2026.', 'March 14, 2026'],
  ['money', 'The fee is $1,250.', '$1,250'],
  ['health', 'The patient has diabetes.', 'diabetes'],
  ['sensitive', 'The client is Catholic.', 'Catholic'],
  ['context', 'My daughter works nearby.', 'My daughter works nearby'],
] as const)(
  'screens %s when selected, leaving it alone when no checks are selected',
  (category, text, value) => {
    expect(report(text, [category]).cleaned).not.toContain(value);
    expect(report(text, []).cleaned).toBe(text);
    expect(report(text, []).needsReview).toBe(false);
  },
);
it('keeps names, dates, places, money and health unchanged in a contact-only scan', () => {
  const text =
    'Avery Bennett lives in Seattle. The patient has diabetes. March 14, 2026: $1,250. Email: avery@example.com.';
  const result = report(text, ['contact']);
  expect(result.findings.map(d => d.kind)).toEqual(['email']);
  expect(result.cleaned).toContain(
    'Avery Bennett lives in Seattle. The patient has diabetes. March 14, 2026: $1,250.',
  );
  expect(result.needsReview).toBe(false);
});
it('separates health, other sensitive facts and broad identifying context before spans can swallow one another', () => {
  const text = 'I have diabetes. My daughter is Catholic.';
  const health = report(text, ['health']);
  const sensitive = report(text, ['sensitive']);
  expect(health.findings.map(d => d.kind)).toEqual(['health']);
  expect(health.cleaned).toContain('My daughter is Catholic.');
  expect(sensitive.cleaned).toContain('I have diabetes. My daughter is');
  expect(sensitive.findings.map(d => d.kind)).toEqual(['sensitive']);
  expect(health.needsReview).toBe(false);
  expect(sensitive.needsReview).toBe(false);
});
it('does not let model output or broad uncertainties re-enable an unchecked category', () => {
  const text =
    'Avery Bennett has diabetes in Seattle. Email: avery@example.com.';
  const result = makeReport(
    text,
    names,
    {...NO_TOPICS, places: ['Seattle'], health: ['diabetes']},
    [{text, reason: 'Private?'}],
    'TEST',
    true,
    undefined,
    [{text, reason: 'Identifying?'}],
    ['contact'],
  );
  expect(result.findings.map(d => d.kind)).toEqual(['email']);
  expect(result.needsReview).toBe(false);
});
it('automatically removes a corroborated full name despite a generic scoped model doubt', () => {
  const text = 'Avery Bennett called.';
  const result = makeReport(
    text,
    names,
    NO_TOPICS,
    [{text: 'Avery Bennett', kind: 'person', reason: 'Uncertain name'}],
    'TEST',
    true,
    undefined,
    [],
    ['names'],
  );
  expect(result.needsReview).toBe(false);
  expect(result.cleaned).not.toContain('Avery Bennett');
});
it('still reviews ambiguous short names and person/company disagreements', () => {
  const short = makeReport(
    'Ask Jordan.',
    {people: ['Jordan'], companies: []},
    NO_TOPICS,
    [{text: 'Jordan', kind: 'person', reason: 'Uncertain name'}],
    'TEST',
    true,
    undefined,
    [],
    ['names'],
  );
  expect(short.needsReview).toBe(true);
  const conflict = makeReport(
    'Contact Avery Bennett.',
    {people: ['Avery Bennett'], companies: ['Avery Bennett']},
    NO_TOPICS,
    [{text: 'Avery Bennett', kind: 'person', reason: 'Uncertain name'}],
    'TEST',
    true,
    undefined,
    [],
    ['names'],
  );
  expect(conflict.needsReview).toBe(true);
});
it('leaves a place corrected from an incorrect name label alone when places are disabled', () => {
  const text = 'The client lives in Seattle.';
  const result = makeReport(
    text,
    {people: ['Seattle'], companies: []},
    NO_TOPICS,
    [],
    'TEST',
    true,
    undefined,
    [],
    ['names'],
  );
  expect(result.cleaned).toBe(text);
});
it('automatically inserts the mixed sample after removing only the selected full name', () => {
  const text =
    'Avery Bennett lives in Seattle. The patient has diabetes. Budget: $1,250. Email: avery@example.com. Record number: 42.';
  // Live Nano marked Seattle as an uncertain person. Name alias expansion also
  // used to redact "avery" inside the unchecked email category.
  const result = makeReport(
    text,
    {people: ['Avery Bennett', 'Seattle'], companies: []},
    NO_TOPICS,
    [{text: 'Seattle', kind: 'person', reason: 'Uncertain name'}],
    'TEST',
    true,
    undefined,
    [],
    ['names'],
  );
  expect(result.cleaned).toBe(text.replace('Avery Bennett', '[PERSON_TEST_1]'));
  expect(result.findings).toHaveLength(1);
  expect(result.needsReview).toBe(false);
});
it('keeps full-name aliases out of unchecked URLs and email addresses', () => {
  const text =
    'Contact Avery Bennett. Email: Avery@example.com. See https://example.com/Avery.';
  const result = report(text, ['names']);
  expect(result.cleaned).toBe(text.replace('Avery Bennett', '[PERSON_TEST_1]'));
  expect(result.needsReview).toBe(false);
});
it('still protects selected payment numbers inside an unchecked URL', () => {
  const result = report('https://example.com/4111111111111111', ['payments']);
  expect(result.cleaned).not.toContain('4111111111111111');
});
it('blocks cloud approval for narrower scans even when the selected checks finished cleanly', () => {
  for (const categories of [COMMON_CATEGORIES, ['contact'] as const, []]) {
    const text = 'A general paragraph.';
    const result = report(text, categories);
    expect(result.complete).toBe(true);
    expect(() => prepareCloudInput(text, result, 'TEST', true)).toThrow(
      'all paste categories',
    );
  }
});
it('can run the selected local checks without model evidence', () => {
  const result = localFindings('Avery Bennett, avery@example.com; MRN: 42.', [
    'contact',
    'records',
  ]);
  expect(result.map(d => d.kind).sort()).toEqual(['email', 'record']);
});
