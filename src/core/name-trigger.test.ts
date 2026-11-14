/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {expect, it} from 'vitest';
import {mightNameSomeone} from './name-trigger';
import {PASTE_FIXTURES} from '../paste-fixtures';

it.each([
  'I met with Mira Calder about the draft.',
  'Could you tell Amity that her appointment moved?',
  'please tell maria the file is ready',
  'Larkspur Fabrication LLC is our client.',
  'Signed, D.K.',
  'Notes from R. Tanaka.',
  'Client: MARGARET WHITFIELD',
  'Ask Quillon to call.',
])('fires when a name is possible: %s', text =>
  expect(mightNameSomeone(text)).toBe(true),
);

it.each([
  'Please rewrite this paragraph in plain language and suggest a clearer title.',
  'Explain why this function returns the sum: function add(left, right) { return left + right; }',
  'Please summarize the meeting between [PERSON_1] and [COMPANY_1]. Reply using those same placeholders.',
  'The applicant supplied SSN 123-45-6789 for the confidential intake form.',
  'Return only JSON. Keep the reply short. I need it ASAP.',
  'My daughter has asthma and needs help discussing it with her school.',
])('stays quiet when no word could be a name: %s', text =>
  expect(mightNameSomeone(text)).toBe(false),
);

it('fires on every chat fixture that names someone', () => {
  for (const f of PASTE_FIXTURES.filter(f =>
    /Mira|Amity|Larkspur/.test(f.text),
  )) {
    expect(mightNameSomeone(f.text), f.id).toBe(true);
  }
});
it('ignores names inside email addresses and URLs, which the rules remove whole', () => {
  expect(
    mightNameSomeone(
      'Please email avery@example.com or see https://example.com/mira-calder today.',
    ),
  ).toBe(false);
  expect(mightNameSomeone('Please email Avery at avery@example.com.')).toBe(
    true,
  );
});
it.each([
  'Quillon will call tomorrow.',
  'Amity called about the file.',
  'Seattle.',
  'Harbourline sent the invoice.',
])(
  'fires on an unfamiliar capitalized first word, which may be a name: %s',
  text => expect(mightNameSomeone(text)).toBe(true),
);
