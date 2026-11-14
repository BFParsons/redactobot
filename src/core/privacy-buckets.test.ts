/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';
import {identityContexts} from './privacy-buckets';
import {makeReport} from '../extension/policy';
import {NO_TOPICS} from './redact';
import {prepareCloudInput} from './cloud-gate';
import {GENERAL_TEST_TEXT} from '../extension/fixtures';
const none = {people: [], companies: []};

describe('ordinary paste requests are not identifying facts', () => {
  it('preserves the public economic paragraph despite a generic industry warning', () => {
    const report = makeReport(
      GENERAL_TEST_TEXT,
      none,
      NO_TOPICS,
      [
        {
          text: 'artificial intelligence companies',
          reason: 'Could refer to specific companies, needs clarification',
        },
      ],
      'TEST',
    );
    expect(report.findings).toEqual([]);
    expect(report.cleaned).toBe(GENERAL_TEST_TEXT);
    expect(report.needsReview).toBe(false);
  });
  it('protects a small town in meeting context even when the model omits it', () => {
    const text = 'We met in Tofino before driving to Seattle.';
    const report = makeReport(text, none, NO_TOPICS, [], 'TEST');
    expect(report.cleaned).toBe(
      'We met in [PLACE_TEST_1] before driving to [PLACE_TEST_2].',
    );
    expect(report.findings.every(d => d.kind === 'places')).toBe(true);
  });
  it.each([
    'Company: artificial intelligence',
    'We work for artificial intelligence LLC.',
    'Our business is called artificial intelligence.',
  ])(
    'retains an uncertain company name even when its words resemble an industry: %s',
    text => {
      const report = makeReport(
        text,
        none,
        NO_TOPICS,
        [{text: 'artificial intelligence', reason: 'Possible company name.'}],
        'TEST',
      );
      expect(report.needsReview).toBe(true);
      expect(report.cleaned).not.toBe(text);
    },
  );
  it.each([
    'I want a short summary of this article.',
    'We need to make this paragraph easier to read.',
    'Please revise my draft and keep the tone friendly.',
    'Only return JSON.',
    'Use only unique keys in the JSON object.',
    'Explain how a rare event differs from an impossible event.',
    'I need help understanding diabetes.',
    'I have a question about diabetes.',
    'I am learning about cancer treatments.',
    'Can you improve my essay about diabetes?',
    'What is a private key?',
    'I want to understand private key encryption.',
    'for (let i = 0; i < items.length; i++) { process(items[i]); }',
    'My diagnosis is [HEALTH_TEST_1].',
  ])('preserves %s', text => {
    expect(identityContexts(text)).toEqual([]);
    const report = makeReport(text, none, NO_TOPICS, [], 'TEST');
    // General health questions may still have eligible topic terms, but must
    // not become a mandatory whole-paragraph identity removal or review hold.
    expect(
      report.findings.some(d => d.kind === 'other' && d.text === text),
    ).toBe(false);
    expect(report.needsReview).toBe(false);
  });

  it('keeps instructions around a genuinely identifying sentence', () => {
    const text =
      'Please summarize this note. I have diabetes. Keep the reply concise.';
    expect(identityContexts(text).map(d => d.text)).toEqual([
      'I have diabetes.',
    ]);
    const report = makeReport(text, none, NO_TOPICS, [], 'TEST');
    expect(report.cleaned).toContain('Please summarize this note.');
    expect(report.cleaned).toContain('Keep the reply concise.');
    expect(report.cleaned).not.toContain('diabetes');
    expect(report.needsReview).toBe(true);
    expect(() => prepareCloudInput(text, report, 'TEST')).toThrow('Review');
    expect(prepareCloudInput(text, report, 'TEST', true).text).not.toContain(
      'diabetes',
    );
  });

  it.each([
    'Can you explain my diabetes diagnosis?',
    'The sole transplant surgeon has diabetes.',
    'Her mother has diabetes.',
    'My private key is fixture-secret-value.',
    'I have\ndiabetes.',
    'Explain this DNA sequence:\nACGTACGTACGTACGTACGTACGTACGT.',
  ])('still holds an actual personal fact or secret: %s', text => {
    const report = makeReport(text, none, NO_TOPICS, [], 'TEST');
    expect(report.needsReview).toBe(true);
    expect(() => prepareCloudInput(text, report, 'TEST')).toThrow('Review');
    expect(
      identityContexts(prepareCloudInput(text, report, 'TEST', true).text),
    ).toEqual([]);
  });

  it('automatically removes the email while preserving an ordinary first-person request', () => {
    const text =
      'I need a short reply sent to support@example.com. Only use three bullet points.';
    const report = makeReport(text, none, NO_TOPICS, [], 'TEST');
    expect(report.needsReview).toBe(false);
    expect(report.cleaned).toBe(
      'I need a short reply sent to [EMAIL_TEST_1]. Only use three bullet points.',
    );
  });
  it('keeps a general topic even when Nano lists the word as sensitive', () => {
    const text = 'Please explain diabetes in simple terms.';
    const report = makeReport(
      text,
      none,
      {...NO_TOPICS, health: ['diabetes']},
      [
        {text: 'diabetes', reason: 'Potential medical condition.'},
        {text, reason: 'Discussion of a health condition.'},
      ],
      'TEST',
    );
    expect(report.cleaned).toBe(text);
    expect(report.needsReview).toBe(false);
  });
  it('resolves a model warning about a standalone pronoun', () => {
    const text = 'I want to understand private key encryption.';
    const report = makeReport(
      text,
      none,
      NO_TOPICS,
      [{text: 'I', reason: 'Pronoun, needs context.'}],
      'TEST',
    );
    expect(report.cleaned).toBe(text);
    expect(report.needsReview).toBe(false);
  });
  it.each([
    'I want a short summary of this article.',
    'Only return JSON with unique keys.',
    'Keep the reply concise.',
  ])(
    'resolves captured model uncertainty about an ordinary instruction: %s',
    text => {
      const report = makeReport(
        text,
        none,
        NO_TOPICS,
        [
          {
            text,
            reason: 'Possible personal perspective or formatting instruction.',
          },
        ],
        'TEST',
      );
      expect(report.cleaned).toBe(text);
      expect(report.needsReview).toBe(false);
    },
  );
  it.each([
    'I want a short summary of this article for Zephyr Hollow.',
    'Only return JSON with key fixture-secret-value.',
    'Keep the reply concise. My diagnosis is diabetes.',
  ])(
    'retains uncertainty when an instruction also contains an unknown value or personal fact: %s',
    text => {
      const report = makeReport(
        text,
        none,
        NO_TOPICS,
        [{text, reason: 'Could contain identifying details.'}],
        'TEST',
      );
      expect(report.needsReview).toBe(true);
      expect(report.cleaned).not.toBe(text);
    },
  );
  it('retains exact categories for redundant warnings about already protected labeled fields', () => {
    const text = 'Record number: 42. City: seattle. Card: 4242 4242 4242 4242.';
    const report = makeReport(
      text,
      none,
      {...NO_TOPICS, places: ['seattle']},
      [{text: 'seattle', reason: 'City name.'}],
      'TEST',
      true,
      undefined,
      [
        {
          text: 'Record number: 42',
          reason: 'Record number can identify someone.',
        },
        {
          text: 'Card: 4242 4242 4242 4242.',
          reason: 'Card numbers can identify someone.',
        },
      ],
    );
    expect(report.needsReview).toBe(false);
    expect(report.findings.map(d => d.kind)).toEqual([
      'record',
      'places',
      'card',
    ]);
    expect(report.cleaned).toBe(
      'Record number: [RECORD_TEST_1]. City: [PLACE_TEST_1]. Card: [CARD_TEST_1].',
    );
  });
  it('does not dismiss an unknown name or additional fact in an educational request', () => {
    const text = 'Please explain diabetes for Zephyr Hollow.';
    const report = makeReport(
      text,
      none,
      {...NO_TOPICS, health: ['diabetes']},
      [{text, reason: 'May refer to a patient.'}],
      'TEST',
    );
    expect(report.needsReview).toBe(true);
    expect(report.cleaned).not.toContain('Zephyr Hollow');
  });
  it('still removes a personal diagnosis in an explanation request', () => {
    const text = 'Please explain why my diagnosis is diabetes.';
    const report = makeReport(
      text,
      none,
      {...NO_TOPICS, health: ['diabetes']},
      [],
      'TEST',
    );
    expect(report.cleaned).not.toContain('diabetes');
    expect(report.needsReview).toBe(true);
  });
  it('keeps indirect identifying descriptions in the local bucket', () => {
    const text = 'The only hospice physician in Cedar County called.';
    const report = makeReport(text, none, NO_TOPICS, [], 'TEST');
    expect(
      report.findings
        .filter(d => d.label.includes('Identifying'))
        .every(d => d.bucket === 'local-only'),
    ).toBe(true);
  });
});
