/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';
import {
  boxFill,
  defaultExemption,
  exemptionFor,
  exemptionsUsed,
  type FoiaSettings,
  foiaText,
  RELEASE,
} from './foia';
import type {Detection} from './redact';

const det = (
  text: string,
  whole: string,
  kind: string,
  enabled = true,
): Detection => {
  const start = whole.indexOf(text);
  return {
    id: `${kind}:${start}`,
    start,
    end: start + text.length,
    text,
    kind,
    label: kind,
    base: kind.toUpperCase(),
    entity: `${kind}:${text}`,
    canonical: text,
    source: 'pattern',
    defaultOn: true,
    enabled,
  };
};
const plain: FoiaSettings = {lawEnforcement: false, overrides: {}};
const TEXT = 'Jane Roe of Acme Corp paid $5,000. Call 555-0100.';

describe('FOIA markings', () => {
  it('defaults personal details to (b)(6) and business details to (b)(4)', () => {
    expect(defaultExemption('person', false)).toBe('(b)(6)');
    expect(defaultExemption('company', false)).toBe('(b)(4)');
    expect(defaultExemption('money', false)).toBe('(b)(4)');
  });
  it('adds (b)(7)(C) to privacy in law enforcement records', () => {
    expect(defaultExemption('person', true)).toBe('(b)(6), (b)(7)(C)');
    expect(defaultExemption('credential', true)).toBe('(b)(7)(E)');
  });
  it('uses overrides, and never leaves a withheld box unlabelled', () => {
    const s = {
      lawEnforcement: false,
      overrides: {person: '(b)(7)(F)', phone: RELEASE},
    };
    expect(exemptionFor('person', s)).toBe('(b)(7)(F)');
    expect(exemptionFor('phone', s)).toBe('(b)(6)');
  });
  it('lists each exemption used once, in statutory order', () => {
    const dets = [
      det('Jane Roe', TEXT, 'person'),
      det('Acme Corp', TEXT, 'company'),
      det('555-0100', TEXT, 'phone'),
    ];
    expect(exemptionsUsed(dets, {lawEnforcement: true, overrides: {}})).toEqual(
      ['(b)(4)', '(b)(6)', '(b)(7)(C)'],
    );
  });
  it('marks the amount withheld and the exemption at the place of each deletion', () => {
    const dets = [
      det('Jane Roe', TEXT, 'person'),
      det('$5,000', TEXT, 'money', false),
    ];
    const out = foiaText(TEXT, dets, plain);
    expect(out).toBe(
      'RELEASED IN PART — (b)(6)\n\n████████ (b)(6) of Acme Corp paid $5,000. Call 555-0100.',
    );
  });
  it('stamps a record with nothing withheld as released in full', () => {
    expect(foiaText('Nothing here.', [], plain)).toBe(
      'RELEASED IN FULL\n\nNothing here.',
    );
  });
  it('makes each box exactly as long as the text it hides, with no cap', () => {
    const code = '(b)(6)';
    for (const withheld of [
      'Jane Roe',
      'x'.repeat(200),
      '12 Palace Road, Arrakeen',
    ]) {
      expect(code.length + boxFill(withheld, code).length).toBe(
        withheld.length,
      );
    }
    expect(boxFill('Jo', code)).toBe(''); // shorter than its label: label width
    expect(boxFill('12 Palace Road, Arrakeen', code)).toBe(
      '███ █████ ████████',
    );
    expect(boxFill('secret words here', code)).not.toMatch(/[a-z]/);
    const long = 'A'.repeat(120);
    const out = foiaText(
      `Call ${long} now.`,
      [det(long, `Call ${long} now.`, 'person')],
      plain,
    );
    expect(out).toContain(`${'█'.repeat(120)} (b)(6)`);
  });
});
