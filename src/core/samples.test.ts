/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';

import {makeReport} from '../extension/policy';

import {NO_TOPICS} from './redact';
import {SAMPLES} from './samples';

describe('sample documents', () => {
  it('offers ten distinct documents', () => {
    expect(SAMPLES).toHaveLength(10);
    expect(new Set(SAMPLES.map(s => s.title)).size).toBe(10);
    expect(new Set(SAMPLES.map(s => s.text)).size).toBe(10);
  });

  it.each(SAMPLES.map(s => [s.title, s.text]))(
    '%s gives the rules plenty to find',
    (_title, text) => {
      const report = makeReport(
        text,
        {people: [], companies: []},
        NO_TOPICS,
        [],
        'T',
      );
      const kinds = new Set(report.findings.map(f => f.kind));
      expect(report.findings.length).toBeGreaterThanOrEqual(15);
      for (const kind of ['person', 'email', 'phone', 'money', 'date']) {
        expect(kinds.has(kind), kind).toBe(true);
      }
    },
  );

  it('uses only reserved, fictional contact details', () => {
    for (const {text} of SAMPLES) {
      for (const email of text.match(/[\w.+-]+@[\w.-]+/g) ?? []) {
        expect(email.replace(/\.$/, '')).toMatch(/\.example$/);
      }
      for (const phone of text.match(/\b\d{3}-\d{3}-\d{4}\b/g) ?? []) {
        expect(phone).toMatch(/^\d{3}-555-01\d{2}$/);
      }
    }
  });
});
