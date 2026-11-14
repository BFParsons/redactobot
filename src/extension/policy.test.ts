/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, it, expect} from 'vitest';
import {makeReport, localFindings, cleanedText} from './policy';
import {NO_TOPICS} from '../core/redact';
const empty = {people: [], companies: []};
describe('paste decisions', () => {
  it('automatically scrubs clear email and full names only after a complete scan', () => {
    const report = makeReport(
      'Contact Avery Bennett at avery@example.com.',
      {people: ['Avery Bennett'], companies: []},
      NO_TOPICS,
      [],
      'TEST',
    );
    expect(report.complete).toBe(true);
    expect(report.needsReview).toBe(false);
    expect(report.cleaned).not.toContain('Avery Bennett');
    expect(report.cleaned).not.toContain('avery@example.com');
  });
  it('holds a clean-looking paste if the model could not finish', () => {
    expect(
      makeReport('Explain photosynthesis.', empty, NO_TOPICS, [], 'TEST', false)
        .needsReview,
    ).toBe(true);
  });
  it('automatically removes the contact sample despite redundant Nano uncertainty', () => {
    const text =
      'Please send the meeting summary to support@example.com.\n\nFor follow-up questions, call (202) 555-0147.\n\nKeep the summary brief and organize the next steps as bullet points.';
    // Evidence captured from the actual on-device scanner, which previously
    // opened review in four of five runs for this otherwise clear sample.
    const ambiguous = [
      {
        text: 'support@example.com',
        reason:
          'Email address could contain sensitive information depending on the context.',
      },
      {
        text: '(202) 555-0147',
        reason:
          'Phone number could be considered sensitive depending on context.',
      },
    ];
    const report = makeReport(
      text,
      {people: [], companies: ['example.com']},
      {...NO_TOPICS, places: ['example.com']},
      ambiguous,
      'TEST',
    );
    expect(report.needsReview).toBe(false);
    expect(report.findings.map(d => d.kind)).toEqual(['email', 'phone']);
    expect(report.cleaned).toBe(
      text
        .replace('support@example.com', '[EMAIL_TEST_1]')
        .replace('(202) 555-0147', '[PHONE_TEST_1]'),
    );
    expect(
      makeReport(text, empty, NO_TOPICS, ambiguous, 'TEST', false).needsReview,
    ).toBe(true);
  });
  it('resolves only contact-contained uncertainties, not the same phrase elsewhere', () => {
    const inside = makeReport(
      'Email Jordan@example.com.',
      empty,
      NO_TOPICS,
      [{text: 'Jordan', reason: 'Possible first name.'}],
      'TEST',
    );
    expect(inside.needsReview).toBe(false);
    expect(inside.cleaned).not.toContain('Jordan');
    const outside = makeReport(
      'Ask Jordan at Jordan@example.com.',
      empty,
      NO_TOPICS,
      [{text: 'Jordan', reason: 'Possible first name.'}],
      'TEST',
    );
    expect(outside.needsReview).toBe(true);
    expect(outside.cleaned).not.toContain('Jordan');
  });
  it('keeps review for ambiguous non-contact details and overlapping contact phrases', () => {
    expect(
      makeReport(
        'Contact Avery Bennett.',
        {people: ['Avery Bennett'], companies: []},
        NO_TOPICS,
        [{text: 'Avery Bennett', reason: 'Could be an organization.'}],
        'TEST',
      ).needsReview,
    ).toBe(true);
    const text = 'Reach the client at support@example.com.';
    for (const ambiguous of [
      [
        {
          text: 'client at support@example.com',
          reason: 'Uncertain relationship.',
        },
        {text: 'support@example.com', reason: 'Possible private contact.'},
      ],
      [
        {text: 'support@example.com', reason: 'Possible private contact.'},
        {
          text: 'client at support@example.com',
          reason: 'Uncertain relationship.',
        },
      ],
    ]) {
      const report = makeReport(text, empty, NO_TOPICS, ambiguous, 'TEST');
      expect(report.needsReview).toBe(true);
      expect(report.cleaned).not.toContain('client');
      expect(report.cleaned).not.toContain('support@example.com');
    }
  });
  it('keeps exact contact categories when the model labels them as both people and organizations', () => {
    const email = 'support@example.com';
    const report = makeReport(
      email,
      {people: [email], companies: [email]},
      NO_TOPICS,
      [],
      'TEST',
    );
    expect(report.needsReview).toBe(false);
    expect(report.findings[0].kind).toBe('email');
    expect(report.cleaned).toBe('[EMAIL_TEST_1]');
    expect(
      makeReport(
        'Avery Bennett',
        {people: ['Avery Bennett'], companies: ['Avery Bennett']},
        NO_TOPICS,
        [],
        'TEST',
      ).needsReview,
    ).toBe(true);
  });
  it('retains coverage of local matches regardless of model evidence', () => {
    const text = 'Avery Bennett uses avery@example.com and lives in Seattle.';
    const local = localFindings(text);
    expect(local.length).toBeGreaterThan(0);
    const report = makeReport(
      text,
      {people: ['Seattle', 'Avery Bennett'], companies: ['avery@example.com']},
      NO_TOPICS,
      [],
      'TEST',
    );
    for (const d of local) {
      expect(
        report.findings.some(x => x.start <= d.start && x.end >= d.end),
      ).toBe(true);
    }
  });
  it('covers the entire ambiguous phrase when it overlaps a smaller match', () => {
    const text = 'Ask Jordan at jordan@example.com about it.';
    const report = makeReport(
      text,
      empty,
      NO_TOPICS,
      [{text: 'Jordan at jordan@example.com', reason: 'Uncertain identity.'}],
      'TEST',
    );
    expect(report.needsReview).toBe(true);
    expect(report.cleaned).not.toContain('Jordan');
    expect(report.cleaned).not.toContain('jordan@example.com');
    expect(report.findings.every(d => d.enabled)).toBe(true);
  });
  it('requests review for ambiguous ungrounded output, first names and health details', () => {
    expect(
      makeReport(
        'A note.',
        empty,
        NO_TOPICS,
        [{text: 'missing phrase', reason: 'Unsure'}],
        'TEST',
      ).needsReview,
    ).toBe(true);
    expect(
      makeReport(
        'Alex called.',
        empty,
        {...NO_TOPICS, names: ['Alex']},
        [],
        'TEST',
      ).needsReview,
    ).toBe(true);
    const health = makeReport(
      'Their diagnosis is diabetes.',
      empty,
      {...NO_TOPICS, health: ['diabetes']},
      [],
      'TEST',
    );
    expect(health.needsReview).toBe(false);
    expect(health.findings[0].bucket).toBe('cloud-cleanup');
  });
  it('keeps placeholder identities stable when the user keeps an earlier detail', () => {
    const text = '[PERSON_OLD_1] knows Avery Bennett and Morgan Ellis.';
    const report = makeReport(
      text,
      {people: ['Avery Bennett', 'Morgan Ellis'], companies: []},
      NO_TOPICS,
      [],
      'TEST',
    );
    const first = report.findings.find(d => d.text === 'Avery Bennett')!;
    const second = report.findings.find(d => d.text === 'Morgan Ellis')!;
    expect(report.replacements[first.id]).toBe('PERSON_TEST_1');
    expect(report.replacements[second.id]).toBe('PERSON_TEST_2');
    expect(cleanedText(text, report.findings, 'TEST', [first.id])).toBe(
      '[PERSON_OLD_1] knows Avery Bennett and [PERSON_TEST_2].',
    );
  });
});
