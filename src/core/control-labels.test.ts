/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';
import {discoverNames} from './names';
import {applyRedactions, buildDetections, NO_TOPICS} from './redact';
import {localFindings, makeReport} from '../extension/policy';
import {CONTROL_LABEL_TEST_TEXT} from '../extension/fixtures';

const empty = {people: [], companies: []};

describe('quoted controls and the partnership-name heuristic', () => {
  it.each([
    CONTROL_LABEL_TEST_TEXT,
    'Turn the dial past "Pots & Pans".',
    'Set the knob to “Pots & Pans”.',
    "Choose the 'Rinse & Hold' cycle.",
    'Choose the ‘Rinse & Hold’ mode.',
    'Press the "Wash & Dry" button.',
    'Use the setting labelled "Wash & Dry".',
    'Use the menu option "Save & Close".',
    'Cycle: "Rinse & Spin".',
    'Turn the dial past "Pots and Pans" to the "Sub-Zero Gentle" setting.',
  ])('leaves a control label unchanged: %s', text => {
    expect(discoverNames(text).companies).toEqual([]);
    expect(localFindings(text)).toEqual([]);
    // A completed model check with no findings must preserve the local
    // decision.
    const report = makeReport(text, empty, NO_TOPICS, [], 'TEST');
    expect(report.cleaned).toBe(text);
    expect(report.needsReview).toBe(false);
  });

  it.each([
    'Invoice from "Pots & Pans".',
    'Client: "Pots & Pans".',
    'Contact Pellegrino & Yoo.',
    'Use the "Pots & Pans LLC" setting.',
    'Use the "Pots & Pans, LLC" setting.',
    'Company: "Pots & Pans" setting up a new account.',
    'The "Pots & Pans" invoice includes a new setting.',
    'Select "Pots & Pans" as the vendor.',
    'Select "Pots & Pans customer" button.',
  ])('retains company cues outside the narrow label context: %s', text => {
    const report = makeReport(text, empty, NO_TOPICS, [], 'TEST');
    expect(report.findings.some(d => d.kind === 'company')).toBe(true);
    expect(report.cleaned).not.toMatch(/Pots & Pans|Pellegrino & Yoo/);
  });

  it('retains a real business occurrence even when the same words label a control', () => {
    const text = 'Choose the "Pots & Pans" cycle. Invoice from "Pots & Pans".';
    const report = makeReport(text, empty, NO_TOPICS, [], 'TEST');
    const start = text.lastIndexOf('Pots & Pans');
    expect(
      report.findings.some(
        d => d.start <= start && d.end >= start + 'Pots & Pans'.length,
      ),
    ).toBe(true);
  });

  it('does not overrule independent model evidence or uncertainty', () => {
    const text = 'Press the "Pots & Pans" button.';
    const known = makeReport(
      text,
      {people: [], companies: ['Pots & Pans']},
      NO_TOPICS,
      [],
      'TEST',
    );
    expect(known.cleaned).not.toContain('Pots & Pans');
    const uncertain = makeReport(
      text,
      empty,
      NO_TOPICS,
      [{text: 'Pots & Pans', reason: 'Possible company.'}],
      'TEST',
    );
    expect(uncertain.needsReview).toBe(true);
    expect(uncertain.cleaned).not.toContain('Pots & Pans');
  });

  it('protects people and structured identifiers inside quoted controls', () => {
    const text =
      'Select "Avery Bennett" as the customer. Press the "avery@example.com" button. Use the "Record number: 42" setting.';
    const report = makeReport(text, empty, NO_TOPICS, [], 'TEST');
    expect(report.cleaned).not.toMatch(
      /Avery Bennett|avery@example.com|\b42\b/,
    );
    expect(report.findings.map(d => d.kind)).toEqual(
      expect.arrayContaining(['person', 'email', 'record']),
    );
  });

  it('respects an explicit manual selection of a control label', () => {
    const text = 'Use the "Pots & Pans" cycle.';
    const findings = buildDetections(text, ['names'], empty, [
      {text: 'Pots & Pans', kind: 'other'},
    ]);
    expect(applyRedactions(text, findings).cleaned).not.toContain(
      'Pots & Pans',
    );
  });

  it('still scrubs identifiers mixed into the complete appliance passage', () => {
    const text =
      CONTROL_LABEL_TEST_TEXT +
      '\nContact Avery Bennett at avery@example.com. Record number: 42.';
    const report = makeReport(text, empty, NO_TOPICS, [], 'TEST');
    expect(report.cleaned.startsWith(CONTROL_LABEL_TEST_TEXT)).toBe(true);
    expect(report.cleaned).not.toMatch(
      /Avery Bennett|avery@example.com|\b42\b/,
    );
  });
});
