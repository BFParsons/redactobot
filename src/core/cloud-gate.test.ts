/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {afterEach, describe, expect, it, vi} from 'vitest';
import {
  applyCloudCleanup,
  approveCleanedResult,
  prepareCloudInput,
  takeCloudText,
  type CloudInput,
} from './cloud-gate';
import {identityContexts, privacyBucket} from './privacy-buckets';
import {makeReport} from '../extension/policy';
import {NO_TOPICS} from './redact';

const names = {people: ['Avery Bennett'], companies: []};
const text =
  'Avery Bennett can be reached at avery@example.com.\n\nThe diagnosis is diabetes. The treatment is metformin.';
const report = () =>
  makeReport(text, names, {...NO_TOPICS, health: ['diabetes']}, [], 'TEST');
const approved = () => prepareCloudInput(text, report(), 'TEST');
afterEach(() => {
  vi.useRealTimers();
});

describe('the identity boundary', () => {
  it('defaults new categories and ambiguous health to local removal', () => {
    for (const kind of [
      'person',
      'email',
      'phone',
      'place',
      'other',
      'future-kind',
    ]) {
      expect(privacyBucket({kind})).toBe('local-only');
    }
    expect(privacyBucket({kind: 'health'})).toBe('cloud-cleanup');
    expect(privacyBucket({kind: 'sensitive'})).toBe('cloud-cleanup');
    expect(
      privacyBucket({
        kind: 'health',
        reviewReason: 'Rare diagnosis may identify this patient.',
      }),
    ).toBe('local-only');
  });
  it('removes identities while preserving common sensitive facts for the second pass', () => {
    const input = approved();
    expect(input.text).not.toContain('Avery');
    expect(input.text).not.toContain('avery@example.com');
    expect(input.text).toContain('diabetes');
    expect(input.text).toContain('metformin');
    expect(input.text).toContain('[PERSON_TEST_1]');
    expect(Object.isFrozen(input)).toBe(true);
  });
  it('can also remove eligible facts locally before the cloud pass', () => {
    const r = report();
    const input = prepareCloudInput(
      text,
      r,
      'TEST',
      false,
      r.findings.filter(d => d.kind === 'health').map(d => d.id),
    );
    expect(input.text).not.toContain('diabetes');
  });
  it.each([
    'I have diabetes.',
    'The sole transplant surgeon has diabetes.',
    'Her mother has diabetes.',
    'The genome sequence identifies a rare condition.',
  ])('holds identifying context locally: %s', source => {
    const r = makeReport(
      source,
      {people: [], companies: []},
      {...NO_TOPICS, health: ['diabetes']},
      [],
      'TEST',
    );
    expect(r.needsReview).toBe(true);
    expect(() => prepareCloudInput(source, r, 'TEST')).toThrow('Review');
    expect(prepareCloudInput(source, r, 'TEST', true).text).not.toContain(
      source,
    );
    expect(
      identityContexts(prepareCloudInput(source, r, 'TEST', true).text),
    ).toEqual([]);
  });
  it('rejects incomplete, ungrounded, missing and stale local evidence', () => {
    expect(() =>
      prepareCloudInput(text, {...report(), complete: false}, 'TEST', true),
    ).toThrow();
    expect(() =>
      prepareCloudInput(
        text,
        {...report(), reasons: ['Unmatched model finding']},
        'TEST',
        true,
      ),
    ).toThrow();
    expect(() =>
      prepareCloudInput(text, {...report(), findings: []}, 'TEST', true),
    ).toThrow('uncovered');
    expect(() =>
      prepareCloudInput('changed ' + text, report(), 'TEST', true),
    ).toThrow('changed');
    const r = report();
    r.findings[0].end++;
    expect(() => prepareCloudInput(text, r, 'TEST', true)).toThrow('changed');
  });
  it('rejects residual author linkage even when omitted from the report', () => {
    const source = 'My diagnosis is diabetes.';
    expect(() =>
      prepareCloudInput(
        source,
        {
          findings: [],
          cleaned: source,
          complete: true,
          reasons: [],
          replacements: {},
          needsReview: false,
        },
        'TEST',
      ),
    ).toThrow('could identify someone');
  });
  it('rejects forged, copied, reused and expired approvals', () => {
    expect(() => takeCloudText({text, kind: 'approved-cloud-input'})).toThrow(
      'local privacy check',
    );
    const input = approved();
    expect(() => takeCloudText({...input})).toThrow();
    expect(takeCloudText(input)).toBe(input.text);
    expect(() => takeCloudText(input)).toThrow('already');
    vi.useFakeTimers();
    const expires = approved();
    vi.advanceTimersByTime(300001);
    expect(() => takeCloudText(expires)).toThrow('local privacy check');
  });
});

describe('cloud responses are evidence, never replacement prose', () => {
  it('unions local sensitive findings with grounded cloud findings and preserves identity placeholders', () => {
    const input = approved();
    takeCloudText(input);
    const result = applyCloudCleanup(input, {
      complete: true,
      findings: [{text: 'metformin', category: 'health'}],
    });
    expect(result.report.cleaned).not.toMatch(
      /diabetes|metformin|Avery|avery@example/,
    );
    expect(result.report.cleaned).toContain('[PERSON_TEST_1]');
    expect(result.report.cleaned).toContain('[HEALTH_TEST_CLOUD_1]');
    expect(takeCloudText(approveCleanedResult(result))).toBe(
      result.report.cleaned,
    );
  });
  it.each([
    null,
    {},
    {complete: false, findings: []},
    {
      complete: true,
      findings: [{text: 'invented disease', category: 'health'}],
    },
    {complete: true, findings: [{text: 'metformin', category: 'unknown'}]},
    {
      complete: true,
      findings: [{text: '[PERSON_TEST_1]', category: 'identifying'}],
    },
  ])('holds invalid or invented responses', value => {
    expect(() => applyCloudCleanup(approved(), value)).toThrow();
  });
  it('requires review for a newly discovered identifier even if the public report is modified', () => {
    const result = applyCloudCleanup(approved(), {
      complete: true,
      findings: [{text: 'metformin', category: 'identifying'}],
    });
    expect(result.report.needsReview).toBe(true);
    result.report.needsReview = false;
    result.report.cleaned = text;
    expect(() => approveCleanedResult(result)).toThrow('Review');
    expect(takeCloudText(approveCleanedResult(result, true))).not.toContain(
      'metformin',
    );
    expect(() => approveCleanedResult({...result}, true)).toThrow('Review');
  });
  it('does not accept a string cast in place of a runtime-issued input', () => {
    expect(() => takeCloudText(text as unknown as CloudInput)).toThrow();
  });
});

describe('cloud excerpts that span a placeholder', () => {
  it('redacts the text around the placeholder and keeps the placeholder restorable', () => {
    const local = makeReport(
      'Avery Bennett has diabetes.',
      names,
      NO_TOPICS,
      [],
      'TEST',
    );
    const input = prepareCloudInput(
      'Avery Bennett has diabetes.',
      local,
      'TEST',
    );
    expect(input.text).toBe('[PERSON_TEST_1] has diabetes.');
    const result = applyCloudCleanup(input, {
      complete: true,
      findings: [{text: '[PERSON_TEST_1] has diabetes', category: 'health'}],
    });
    expect(result.report.cleaned).toContain('[PERSON_TEST_1]');
    expect(result.report.cleaned).not.toContain('diabetes');
  });
  it('still rejects an excerpt that is only a placeholder', () => {
    expect(() =>
      applyCloudCleanup(approved(), {
        complete: true,
        findings: [{text: '[PERSON_TEST_1]', category: 'health'}],
      }),
    ).toThrow();
  });
});

describe('what the gate will and will not block', () => {
  const none = {people: [], companies: []};
  const prepare = (source: string) =>
    prepareCloudInput(
      source,
      makeReport(source, none, NO_TOPICS, [], 'T'),
      'T',
      true,
    );

  it('does not mistake its own placeholders for identifiers', () => {
    // After redaction this reads "user name: [CREDENTIAL_T_1], password:
    // [CREDENTIAL_T_2]" and "file number [RECORD_T_1]", which the credential
    // and record checks would match again.
    const input = prepare(
      'The server login was user name: admin, password: Tr0ub4dor-99. See file number EPA-0042-NY.',
    );
    expect(input.text).not.toContain('Tr0ub4dor-99');
    expect(input.text).toMatch(/\[CREDENTIAL_T_\d\]/);
  });

  it('removes a fragment the first pass left behind, instead of refusing', () => {
    const source =
      'Hill Valley Mutual Insurance paid the claim. Visiting from New York, NY 10001 next week.';
    const input = prepare(source);
    expect(input.text).not.toContain('Mutual Insurance');
    expect(input.text).not.toMatch(/\bNew\b/);
    expect(input.text).not.toContain('York');
  });

  it('lets every sample document through', async () => {
    const {SAMPLES} = await import('./samples');
    for (const sample of SAMPLES) {
      const source = `DOCUMENT:\n${sample.text}\n\nQUESTION:\nSummarise this.`;
      expect(() => prepare(source), sample.title).not.toThrow();
    }
  });
});
