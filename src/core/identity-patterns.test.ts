/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';
import {detectionView, viewOccurrences} from '../../taxonomy/normalize.js';
import {detectPatterns} from '../../taxonomy/taxonomy.js';
import {applyRedactions, buildDetections, NO_TOPICS, restore} from './redact';
import {GUARD_DETECTORS, localFindings, makeReport} from '../extension/policy';
import {prepareCloudInput} from './cloud-gate';

const none = {people: [], companies: []};
const full = (
  text: string,
  target: string,
  kind: string,
  places: string[] = [],
) => {
  const ds = buildDetections(text, GUARD_DETECTORS, none, [], new Set(), {
    ...NO_TOPICS,
    places,
  });
  const start = text.indexOf(target);
  const end = start + target.length;
  expect(start).toBeGreaterThanOrEqual(0);
  expect(
    ds.some(
      d => d.start <= start && d.end >= end && d.kind === kind && d.enabled,
    ),
    JSON.stringify(ds),
  ).toBe(true);
  for (const d of ds) expect(text.slice(d.start, d.end)).toBe(d.text);
  expect(applyRedactions(text, ds).cleaned).not.toContain(target);
  return ds;
};

describe('original offsets through Unicode folding', () => {
  it('maps composed accents, surrogate pairs, compatibility expansions and hidden marks', () => {
    const text = '😀 A\u030A 𝟜４٢\u200B2 ﬃ';
    const view = detectionView(text);
    expect(view.text).toBe('😀 Å 4422 ffi');
    expect(
      viewOccurrences(view, '4422').map(([s, e]) => text.slice(s, e)),
    ).toEqual(['𝟜４٢\u200B2']);
    expect(
      viewOccurrences(view, 'Å').map(([s, e]) => text.slice(s, e)),
    ).toEqual(['A\u030A']);
    expect(
      viewOccurrences(view, 'ffi').map(([s, e]) => text.slice(s, e)),
    ).toEqual(['ﬃ']);
  });
});

describe('record fields and document-local evidence', () => {
  const labels = [
    'MRN:',
    'Record number:',
    'Case:',
    'Claim ID:',
    'Invoice number:\n',
    'Encounter key:',
    'Accession ID ',
    'Reference:',
  ];
  const values = [
    '42',
    'Q',
    'INTAKEBLUE',
    'cobalt-fern',
    'abc-00421-z',
    'AB\u200B-7412',
    'ZX / 75104 / Q',
    'ＡＢ—７４１２',
    'אב-42',
  ];
  for (const label of labels) {
    for (const value of values) {
      it(`${label.trim()} ${JSON.stringify(value)}`, () => {
        full(`Before. ${label} ${value}. After.`, value, 'record');
      });
    }
  }
  it('retains quoted multiword references and propagates exact repeats', () => {
    const text = 'Reference: "BLUE FERN". Find BLUE FERN later.';
    full(text, 'BLUE FERN', 'record');
    expect(applyRedactions(text, localFindings(text)).cleaned).not.toContain(
      'BLUE FERN',
    );
  });
  it('holds an unquoted multiword record field without leaving part behind', () => {
    const text = 'Reference: blue fern. This needs filing.';
    const ds = full(text, 'blue fern', 'record');
    expect(ds.find(d => d.text === 'blue fern')?.reviewReason).toBeTruthy();
    expect(makeReport(text, none, NO_TOPICS, [], 'TEST').needsReview).toBe(
      true,
    );
  });
  it('learns a format in this document and requires review for new values', () => {
    const text = 'Reference: zz-31. Follow up zz-72 tomorrow.';
    const report = makeReport(text, none, NO_TOPICS, [], 'TEST');
    expect(report.findings.find(d => d.text === 'zz-72')).toMatchObject({
      kind: 'record',
      bucket: 'local-only',
      enabled: true,
      reviewReason: expect.any(String),
    });
    expect(report.needsReview).toBe(true);
    expect(() => prepareCloudInput(text, report, 'TEST')).toThrow(/Review/);
    expect(
      localFindings('Follow up zz-72 tomorrow.').some(d => d.kind === 'record'),
    ).toBe(false);
  });
  it('reads short and letters-only IDs from table columns', () => {
    const text = 'Record ID\tCity\nQ\t南投\nINTAKEBLUE\tÅ';
    full(text, 'Q', 'record');
    full(text, 'INTAKEBLUE', 'record');
    full(text, '南投', 'places');
    full(text, 'Å', 'places');
  });
  it('does not split a complete ID at an overlapping date-like fragment', () => {
    full('Record number: 2026-03-14-abc.', '2026-03-14-abc', 'record');
  });
  it('keeps names, email addresses, URLs and public references in their own categories', () => {
    full('Reference: avery@example.test.', 'avery@example.test', 'email');
    expect(
      detectPatterns('Reference: https://example.test/path', [
        'record',
        'url',
      ]).map(d => d.type),
    ).toEqual(['url']);
    expect(
      localFindings('Case: Kowalczyk v. Brightpath Home Care, LLC').find(
        d => d.text === 'Kowalczyk',
      )?.kind,
    ).toBe('person');
    expect(
      detectPatterns(
        'Reference: none. Record number: N/A. Form 1099-NEC. 29 C.F.R. § 1601.12.',
        ['record'],
      ),
    ).toEqual([]);
  });
  it('does not treat an address on file as a record-number field', () => {
    for (const address of ['1234 Elm Ave', 'Unit 432, 1234 Elm Ave']) {
      full(
        `Address on file: ${address}, Seattle, WA 98101.`,
        address,
        'street',
      );
    }
    full('File: cobalt-fern.', 'cobalt-fern', 'record');
  });
  it('protects an uppercase unit prefix with the full street address', () => {
    full(
      'Address: UNIT 432, 1234 ELM AVE, SEATTLE, WA 98101.',
      'UNIT 432, 1234 ELM AVE',
      'street',
    );
  });
});

describe('full and partial cards in original formatting', () => {
  const digits = '4242424242424242';
  const scripts = [0x30, 0xff10, 0x660, 0x6f0, 0x966, 0x1d7d8];
  const separators = [
    '',
    ' ',
    '-',
    '\n',
    '\r\n',
    ' / ',
    '\u200B',
    '\u2060',
    '\u00A0',
    '\u2011',
  ];
  for (const zero of scripts) {
    for (const separator of separators) {
      it(`digit range ${zero.toString(16)}, separator ${JSON.stringify(separator)}`, () => {
        const value = [...digits]
          .map(d => String.fromCodePoint(zero + Number(d)))
          .join('');
        const groups = [...value].reduce<string[]>((arr, d, i) => {
          const g = Math.floor(i / 4);
          arr[g] = (arr[g] ?? '') + d;
          return arr;
        }, []);
        const target = groups.join(separator);
        full(`😀 Use ${target} for payment.`, target, 'card');
      });
    }
  }
  it('protects an explicitly identified card with an invalid checksum', () => {
    full('Use 4242 4242 4242 4243 for payment.', '4242 4242 4242 4243', 'card');
  });
  it('holds malformed short and overlong card fields in full, never just the suffix', () => {
    for (const value of ['4242 4242 4242', '4242 4242 4242 4242 4242']) {
      const ds = full(`Card: ${value}.`, value, 'card');
      expect(ds.find(d => d.text === value)?.reviewReason).toBeTruthy();
    }
  });
  it('protects spoken digits and masked prefixes in full', () => {
    full(
      'Payment card ends with seven three one nine.',
      'seven three one nine',
      'card_partial',
    );
    full(
      'Card: four two four two four two four two four two four two four two four two.',
      'four two four two four two four two four two four two four two four two',
      'card',
    );
    full(
      'Debit card 4769 15•• •••• 2996.',
      '4769 15•• •••• 2996',
      'card_partial',
    );
  });
  it('corrects a full card in a table without cutting its span', () => {
    full(
      'Card\tAmount\n４２４２ ４２４２ ４２４２ ４２４２\t12.00',
      '４２４２ ４２４２ ４２４２ ４２４２',
      'card',
    );
  });
  it('does not assemble across table columns, sentences or separate identifiers', () => {
    for (const text of [
      '218 555 0125\t600 Garfield Ave',
      '123-456-789, 900-12-3456',
      'Counts: 4242. Then 4242. Then 4242. Then 4242.',
    ]) {
      expect(detectPatterns(text, ['card']), text).toEqual([]);
    }
  });
  it('distinguishes a health card from a payment card', () => {
    const text = 'Health card PHN 9876 543 210. Visa card 4242 4242 4242 4242.';
    full(text, '9876 543 210', 'passport_dl');
    full(text, '4242 4242 4242 4242', 'card');
  });
  it('does not carry a previous date-column label onto a health identifier', () => {
    const text =
      'CHECKUP  NOTE\nPatient:  Avery,  Rowan\nDOB: 02/07/1998  (53 y)\nPHN 9876 543 210   Patient ID 7319042';
    full(text, '9876 543 210', 'passport_dl');
    full(text, '7319042', 'record');
  });
});

describe('places with context and on-device model evidence', () => {
  for (const value of ['seattle', 'el paso', '南投', 'Łódź', 'Å', 'A\u030A']) {
    it(`accepts model place ${value}`, () => {
      full(`The appointment is near ${value}.`, value, 'places', [
        value.normalize('NFC'),
      ]);
    });
    it(`accepts place field ${value}`, () => {
      full(`Town: ${value}.`, value, 'places');
    });
  }
  for (const value of [
    'seattle',
    'el paso',
    'Łódź',
    'lodz',
    'tokyo',
    'São Paulo',
  ]) {
    it(`uses the offline gazetteer for ${value}`, () => {
      full(`The appointment is near ${value}.`, value, 'places');
    });
  }
  it('holds close spellings in residential context for review', () => {
    const text = 'The client lives in seattlle.';
    const report = makeReport(text, none, NO_TOPICS, [], 'TEST');
    expect(report.findings.find(d => d.text === 'seattlle')).toMatchObject({
      kind: 'places',
      enabled: true,
      reviewReason: expect.any(String),
    });
    expect(report.needsReview).toBe(true);
  });
  it('protects coordinates and rejects impossible latitude/longitude pairs', () => {
    full(
      'Pickup location: 47.6062, -122.3321.',
      '47.6062, -122.3321',
      'places',
    );
    expect(
      detectPatterns('Measurements: 91.1234, 181.1234.', ['places']),
    ).toEqual([]);
  });
  it('does not turn ordinary words and a spoken email domain into a place', () => {
    expect(
      detectPatterns(
        'We are in order. There is a sale at work. The report is in progress.',
        ['places'],
      ),
    ).toEqual([]);
    full(
      'Email deb dot fairweather at orchards dot example.',
      'deb dot fairweather at orchards dot example',
      'email',
    );
  });
  it('leaves company names intact as a single protected organization', () => {
    const text = 'Visit Seattle Logistics LLC in seattle.';
    const ds = buildDetections(text, GUARD_DETECTORS, {
      ...none,
      companies: ['Seattle Logistics LLC'],
    });
    expect(ds.find(d => d.text === 'Seattle Logistics LLC')?.kind).toBe(
      'company',
    );
    expect(ds.find(d => d.text === 'seattle')?.kind).toBe('places');
  });
  it('labels a city before a province and postal code correctly without Nano', () => {
    full('Home: 1234 Elm Dr\nCalgary AB  T2P1J9', 'Calgary', 'places');
  });
  it('does not treat an inline location field as the value of a date column', () => {
    full(
      'Date 14 Mar 2026  Location: 1234 Elm Dr, Calgary, AB T2P1J9',
      '1234 Elm Dr',
      'street',
    );
  });
});

describe('identity gate and round trip', () => {
  it('removes all three categories from the exact cloud payload and restores original forms', () => {
    const text =
      'Record number: 42. Appointment in seattle. Card: ４２４２\u200B４２４２\u200B４２４２\u200B４２４２.';
    const report = makeReport(text, none, NO_TOPICS, [], 'TEST');
    const input = prepareCloudInput(text, report, 'TEST', true);
    expect(input.text).not.toMatch(/42|seattle|４２/);
    const red = applyRedactions(text, localFindings(text));
    expect(restore(red.cleaned, red.map)).toBe(text);
  });
  it('rejects a stale report that omits a newly detectable record', () => {
    const text = 'Record number: 42.';
    const report = makeReport(
      'No private details.',
      none,
      NO_TOPICS,
      [],
      'TEST',
    );
    expect(() => prepareCloudInput(text, report, 'TEST', true)).toThrow(
      /uncovered/,
    );
  });
  it('still respects which detector categories the caller selected', () => {
    expect(
      buildDetections(
        'Record number: 42. Card: 4242 4242 4242 4242. City: seattle.',
        [],
        none,
      ),
    ).toEqual([]);
  });
});

it('keeps a spaced ID whole after a record label', () => {
  const t = 'Business number on file: 81234 5678 RT0001.';
  expect(
    detectPatterns(t, ['record', 'bn_ca'], []).map(
      (m: {start: number; end: number}) => t.slice(m.start, m.end),
    ),
  ).toEqual(['81234 5678 RT0001']);
});
