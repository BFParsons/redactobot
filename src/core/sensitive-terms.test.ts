/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';
import {sensitiveTerms} from './sensitive-terms';
import {NO_TOPICS, applyRedactions, buildDetections} from './redact';
import {DETECTORS} from '../../taxonomy/taxonomy.js';
import {makeReport} from '../extension/policy';
import {APPLIANCE_TEST_TEXT} from '../extension/fixtures';
const names = {people: [], companies: []};

const words = (t: string) =>
  sensitiveTerms(t).map(m => `${m.kind}:${t.slice(m.start, m.end)}`);

// All examples are fictional.
describe('words that point to a sensitive fact', () => {
  it('finds conditions, drugs by their endings, doses and lab values', () => {
    expect(
      words(
        'Dx type 2 diabetes and gastritis; on losartan 50 mg daily, metformin; creatinine 1.9 mg/dL.',
      ),
    ).toEqual([
      'health:diabetes',
      'health:gastritis',
      'health:losartan',
      'health:50 mg daily',
      'health:metformin',
      'health:creatinine',
      'health:1.9 mg/dL',
    ]);
  });
  it('finds mental health, substance use and pregnancy', () => {
    expect(
      words('He is sober, goes to AA, and has PTSD. She is 14 weeks pregnant.'),
    ).toEqual([
      'health:sober',
      'health:AA',
      'health:PTSD',
      'health:14 weeks pregnant',
    ]);
  });
  it('finds the special categories', () => {
    expect(
      words(
        'Her asylum claim is pending; he is on probation; she tithes at a Baptist church; union dues; filed Chapter 13.',
      ),
    ).toEqual([
      'sensitive:asylum',
      'sensitive:probation',
      'sensitive:tithes',
      'sensitive:Baptist',
      'sensitive:union dues',
      'sensitive:Chapter 13',
    ]);
  });
  it('finds relatives, one-of-a-kind roles and vehicles', () => {
    expect(
      words(
        "Chase's younger sister is the only hospice physician in Door County and drives a 2019 Toyota Corolla.",
      ),
    ).toEqual([
      "sensitive:Chase's younger sister",
      'sensitive:the only hospice physician in Door County',
      'sensitive:2019 Toyota Corolla',
    ]);
  });
  it('leaves ordinary words alone', () => {
    expect(
      words(
        'Paid by Visa in April. The MS Word file is in Mass. A cash infusion; photography and geography; the account will be disabled.',
      ),
    ).toEqual([]);
  });
  it('only flags: nothing found this way is replaced unless the user asks', () => {
    const text = 'She has diabetes and her brother is on probation.';
    const ids = [
      'names',
      'sensitive_topics',
      ...DETECTORS.map((d: {id: string}) => d.id),
    ];
    const dets = buildDetections(text, ids, {people: [], companies: []});
    expect(dets.map(d => d.text)).toEqual([
      'diabetes',
      'her brother',
      'probation',
    ]);
    expect(dets.every(d => !d.defaultOn && !d.enabled)).toBe(true);
    expect(applyRedactions(text, dets).cleaned).toBe(text);
  });
});

it.each([
  'Uses only cold water.',
  'Use only hot water.',
  'Only the final rinse will be warm.',
  'The sole filter needs cleaning.',
  'Use only mild detergent.',
  'The only washer is running.',
  'Keep only the larger container.',
  'Use only the timer.',
  'Only the computer needs a restart.',
  'Only the sensor is active.',
  'Select only the parameter.',
  'This is only a comparison.',
  'The only cold water in the washer drains away.',
  'The only filter in the machine needs cleaning.',
])('does not infer a person from a non-personal word ending: %s', text => {
  expect(sensitiveTerms(text).filter(d => d.topic === 'identifying')).toEqual(
    [],
  );
  const report = makeReport(text, names, NO_TOPICS, [], 'TEST');
  expect(report.cleaned).toBe(text);
  expect(report.needsReview).toBe(false);
});
it('preserves the complete appliance instructions with no local findings', () => {
  const report = makeReport(APPLIANCE_TEST_TEXT, names, NO_TOPICS, [], 'TEST');
  expect(report.findings).toEqual([]);
  expect(report.cleaned).toBe(APPLIANCE_TEST_TEXT);
  expect(report.needsReview).toBe(false);
});
it.each([
  'the only hospice physician in Cedar County',
  'the last surviving charter resident',
  'the sole helicopter pilot',
  'only pediatric nurse',
  'the only employee',
  'the only student in the village',
  'the only retired carpenter',
  'the only archaeologist',
  'the only female transplant surgeon',
  'the sole partner',
])('still protects a uniquely identifying human role: %s', text => {
  expect(sensitiveTerms(text).some(d => d.topic === 'identifying')).toBe(true);
  const report = makeReport(text, names, NO_TOPICS, [], 'TEST');
  expect(report.needsReview).toBe(true);
  expect(report.cleaned).not.toBe(text);
  expect(
    report.findings
      .filter(d => d.reviewReason)
      .every(d => d.bucket === 'local-only'),
  ).toBe(true);
});
it('keeps identifiers protected when mixed into ordinary appliance instructions', () => {
  const text =
    APPLIANCE_TEST_TEXT +
    '\nContact Avery Bennett at avery@example.com. Record number: 42.';
  const report = makeReport(text, names, NO_TOPICS, [], 'TEST');
  expect(report.cleaned.startsWith(APPLIANCE_TEST_TEXT)).toBe(true);
  expect(report.cleaned).not.toMatch(/Avery Bennett|avery@example.com|\b42\b/);
});
it.each([
  'the only vineyard in Cedar Valley',
  'the last surviving schooner in the harbour',
])('still protects distinctive possessions with location context: %s', text => {
  const report = makeReport(text, names, NO_TOPICS, [], 'TEST');
  expect(report.needsReview).toBe(true);
  expect(report.cleaned).not.toBe(text);
  expect(
    report.findings.some(d => d.bucket === 'local-only' && d.reviewReason),
  ).toBe(true);
});
