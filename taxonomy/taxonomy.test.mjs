/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Run with: node --test taxonomy/
 */

import test from 'node:test';
import assert from 'node:assert/strict';
import {
  DETECTORS,
  FRAMEWORKS,
  AUDIENCES,
  DEFAULT_FRAMEWORKS,
  KEEP,
  coverage,
  planFor,
  detectPatterns,
  detectorById,
  validSsn,
  validSin,
  validCard,
  validIban,
  validRouting,
  DATA_CLASSES,
  ACCURACY_TIERS,
  DEFAULT_CLASSES,
  planForClasses,
} from './taxonomy.js';

const ALL = DETECTORS.map(d => d.id);
const found = (text, ids = ALL) =>
  detectPatterns(text, ids).map(m => `${m.type}:${m.text}`);

// All test data is fictional or a published test value.
const SAMPLE = `Margaret moved $310,500.75 to her personal account 5520-114-9087. The proceeds were
deposited at Cascadia Credit Union, account 4471-889-2203, sold for $1,250,000, with $400,000 held back.
Outstanding invoice is $8,400. Dispute over a $62,000 warranty claim.
Follow up: margaret@whitfieldholdings.example or 604-555-0142.
Business number on file: 81234 5678 RT0001. Date: March 14, 2026.`;

test('structure: every reference resolves', () => {
  const ids = new Set(ALL);
  assert.equal(ids.size, ALL.length, 'detector ids are unique');
  for (const f of FRAMEWORKS) {
    assert.ok(f.cite && f.url && f.requirements.length, f.id);
    for (const r of f.requirements) {
      for (const d of r.detectors) {
        assert.ok(ids.has(d), `${f.id} ${r.ref}: unknown detector ${d}`);
      }
      if (r.keep) {
        assert.ok(KEEP[r.keep], `${f.id} ${r.ref}: unknown keep ${r.keep}`);
      }
      assert.ok(
        ['covered', 'partial', 'planned', 'none', 'na'].includes(coverage(r)),
      );
      if (coverage(r) === 'none') {
        assert.ok(r.gap, `${f.id} ${r.ref}: uncovered item needs a gap note`);
      }
    }
  }
  for (const a of AUDIENCES) {
    for (const f of a.frameworks) assert.ok(FRAMEWORKS.some(x => x.id === f));
  }
  for (const d of DETECTORS) {
    if (d.kind !== 'pattern') continue;
    assert.ok(d.rules.length, `${d.id} has no rules`);
    for (const r of d.rules) {
      assert.ok(r.re.global, `${d.id} rules must be global`);
    }
  }
});

test('HIPAA Safe Harbor lists all 18 identifiers (A)-(R)', () => {
  const refs = FRAMEWORKS.find(f => f.id === 'hipaa').requirements.map(
    r => r.ref,
  );
  assert.deepEqual(
    refs,
    [...'ABCDEFGHIJKLMNOPQR'].map(c => `(${c})`),
  );
});

test('default rules catch every structured item in the sample', () => {
  const {detectorIds, usesModel} = planFor(DEFAULT_FRAMEWORKS);
  assert.equal(usesModel, true);
  assert.deepEqual(
    found(SAMPLE, detectorIds).sort(),
    [
      'account:4471-889-2203',
      'account:5520-114-9087',
      'bn_ca:81234 5678 RT0001',
      'email:margaret@whitfieldholdings.example',
      'money:$1,250,000',
      'money:$310,500.75',
      'money:$400,000',
      'money:$62,000',
      'money:$8,400',
      'phone:604-555-0142',
    ].sort(),
  );
});

test('only the chosen rules run', () => {
  const court = planFor(['frcp52']).detectorIds;
  assert.ok(
    !court.includes('money') &&
      !court.includes('phone') &&
      !court.includes('date'),
  );
  const hits = found(SAMPLE, court);
  assert.ok(!hits.some(h => h.startsWith('money') || h.startsWith('email')));
  assert.ok(
    !hits.includes('account:604-555-0142'),
    'a phone number is not reported as an account',
  );
  const card = planFor(['pci']);
  assert.deepEqual(
    card.detectorIds.sort(),
    ['card', 'card_exp', 'card_partial', 'cvv', 'names'].sort(),
  );
  assert.ok(planFor(['hipaa']).detectorIds.includes('places'));
  assert.equal(planFor([]).usesModel, false);
  assert.equal(
    planFor(['frcp52'], {names: false}).usesModel,
    false,
    'override can switch the model off',
  );
  assert.ok(
    planFor(['frcp52'], {money: true}).detectorIds.includes('money'),
    'override can add a check',
  );
  assert.ok(planFor(['hipaa']).planned.includes('indirect'));
});

test('HIPAA selection catches dates, ages, URLs, IPs and record numbers', () => {
  const ids = planFor(['hipaa']).detectorIds;
  const t =
    'Seen 03/02/2026, born on July 4, 1931, a 93-year-old. MRN: A-448291. Portal https://portal.example/x from 192.168.4.20. SSN 123-45-6789.';
  assert.deepEqual(
    found(t, ids).sort(),
    [
      'date:03/02/2026',
      'dob:July 4, 1931',
      'age90:93-year-old',
      'record:A-448291',
      'url:https://portal.example/x',
      'ip:192.168.4.20',
      'ssn:123-45-6789',
    ].sort(),
  );
});

test('validators', () => {
  assert.ok(validSsn('123-45-6789'));
  assert.ok(
    !validSsn('000-12-3456') &&
      !validSsn('666-12-3456') &&
      !validSsn('900-12-3456') &&
      !validSsn('123-00-4567'),
  );
  assert.ok(validSin('123-456-782') && validSin('130 692 544'));
  assert.ok(
    !validSin('123-456-789') && !validSin('046 454 286'),
    'bad check digit; numbers starting 0 are never issued',
  );
  assert.ok(
    validCard('4111 1111 1111 1111') && !validCard('4111 1111 1111 1112'),
  );
  assert.ok(
    validIban('GB82 WEST 1234 5698 7654 32') &&
      !validIban('GB82 WEST 1234 5698 7654 33'),
  );
  assert.ok(validRouting('021000021') && !validRouting('021000022'));
});

test('number patterns', () => {
  assert.deepEqual(found('Card 4111 1111 1111 1111 exp 04/28 CVV 123'), [
    'card:4111 1111 1111 1111',
    'card_exp:04/28',
    'cvv:123',
  ]);
  assert.deepEqual(found('SIN 130 692 544 and EIN 12-3456789'), [
    'sin_ca:130 692 544',
    'ein:12-3456789',
  ]);
  assert.deepEqual(
    found(
      'Wire to GB82 WEST 1234 5698 7654 32, routing number 021000021, account no. 000123456789',
    ),
    [
      'iban:GB82 WEST 1234 5698 7654 32',
      'routing:021000021',
      'account:000123456789',
    ],
  );
  assert.deepEqual(found('Passport number: X1234567. Case No. 2:24-cv-01234'), [
    'passport_dl:X1234567',
    'record:2:24-cv-01234',
  ]);
  assert.deepEqual(
    found('Lives at 1420 West Harbour Road, Suite 200, Seattle, WA 98101.'),
    [
      'street:1420 West Harbour Road, Suite 200',
      'places:Seattle',
      'region:WA',
      'zip:98101',
    ],
  );
  assert.deepEqual(
    found('Not IDs: 123-456-789, 900-12-3456, card 1234 5678 9012 3456', [
      'sin_ca',
      'ssn',
      'card',
    ]),
    ['card:1234 5678 9012 3456'],
    'an explicit card is protected even when its checksum fails',
  );
  assert.deepEqual(
    found('Meeting on 2026-03-14.', ['account']),
    [],
    'an ISO date is not an account number',
  );
});

// Forms found by running 100 fictional documents through the app
// (evaluation/RESULTS.md).
test('money in the forms people actually write', () => {
  const money = t =>
    found(t)
      .filter(x => x.startsWith('money:'))
      .map(x => x.slice(6));
  assert.deepEqual(
    money(
      'Paid £18,000, then EUR 6,000 and C$2,300; about $1.9 million in all.',
    ),
    ['£18,000', 'EUR 6,000', 'C$2,300', '$1.9 million'],
  );
  assert.deepEqual(
    money(
      'Offer was 75k, up from $38K. Balance 134,031.48; adjustment (27,315.88).',
    ),
    ['75k', '$38K', '134,031.48', '(27,315.88)'],
  );
  assert.deepEqual(
    money('He owes twelve thousand dollars. Invoice € 18.020,00.'),
    ['twelve thousand dollars', '€ 18.020,00'],
  );
  assert.deepEqual(
    money('See paragraph (1) and (3) of the 401k summary; 12 employees.'),
    [],
  );
});

test('dates in the forms people actually write', () => {
  const dates = t =>
    found(t)
      .filter(x => /^(date|dob):/.test(x))
      .map(x => x.split(':').slice(1).join(':'));
  assert.deepEqual(
    dates(
      'Tuesday, January 20, 2026; 14-Apr-2026; 30 June; February 2025; due 06/26.',
    ),
    [
      'Tuesday, January 20, 2026',
      '14-Apr-2026',
      '30 June',
      'February 2025',
      '06/26',
    ],
  );
  assert.deepEqual(dates('Date: Wed, 04 Mar 2026 16:52:10 -0600'), [
    'Wed, 04 Mar 2026 16:52:10',
  ]);
  assert.deepEqual(
    found('license exp. 05/09/2026'),
    ['date:05/09/2026'],
    'a full date is not a card expiry',
  );
  assert.deepEqual(
    found('including $1,318.44 December dividend'),
    ['money:$1,318.44'],
    'cents are not a day of the month',
  );
});

test('ID numbers that are not labelled the expected way', () => {
  assert.deepEqual(found('07/15/2026\tINV-26-3391\tForm 1040 preparation'), [
    'date:07/15/2026',
    'record:INV-26-3391',
  ]);
  assert.deepEqual(
    found(
      'Case No.: 2:25-cv-00417-RBS-LRL, claim no. EPL-2025-0093317 under policy ODM-EPL-7704512',
    ),
    [
      'record:2:25-cv-00417-RBS-LRL',
      'record:EPL-2025-0093317',
      'record:ODM-EPL-7704512',
    ],
  );
  assert.deepEqual(
    found("Seun's passport is no. A09417726; VAT NL004471882B01"),
    ['passport_dl:A09417726', 'ein:NL004471882B01'],
  );
  assert.deepEqual(
    found('SSN xxx-xx-4388, acct x4410, card ending 2239, and ...2204'),
    [
      'ssn:xxx-xx-4388',
      'card_partial:x4410',
      'card_partial:2239',
      'card_partial:...2204',
    ],
  );
  assert.deepEqual(
    found('NI number JK 47 21 09 C. Bar No. 24081177. NPI 1548839201.'),
    [
      'passport_dl:JK 47 21 09 C',
      'passport_dl:24081177',
      'passport_dl:1548839201',
    ],
  );
  assert.deepEqual(
    found(
      'Form 1099-NEC and Schedule K-1 under 26 U.S.C. § 7216; Form 1098 received; route driver at $19.75/hr',
    ),
    ['money:$19.75/hr'],
    'tax form numbers, statute citations and hourly rates are not ID numbers',
  );
  assert.deepEqual(
    found('renewal receipt.\nThe 2025 owner draws were high.'),
    [],
    'a label must be followed by an ID, not ordinary words',
  );
});

test('contact details in the forms people actually write', () => {
  assert.deepEqual(
    found(
      'Call (757) 555-0163 x214 or 206-555-0170 ext. 12; UK 07700 900143; +31 10 555 0147.',
    ),
    [
      'phone:(757) 555-0163 x214',
      'phone:206-555-0170 ext. 12',
      'phone:07700 900143',
      'phone:+31 10 555 0147',
    ],
  );
  assert.deepEqual(found('Home: PO Box 317, Lolo, MT 59847.'), [
    'street:PO Box 317',
    'places:Lolo',
    'region:MT',
    'zip:59847',
  ]);
  assert.deepEqual(
    found(
      '600 Grant Street, 41st Floor; 745 MEDICAL CENTER PKWY STE 204; Suite 210, 1700 Riverfront Parkway',
    ).filter(x => x.startsWith('street')),
    [
      'street:600 Grant Street, 41st Floor',
      'street:745 MEDICAL CENTER PKWY STE 204',
      'street:Suite 210, 1700 Riverfront Parkway',
    ],
  );
  assert.deepEqual(
    found(
      'Leeds LS6 3BJ; Galway H91 X4K7; write to deb dot fairweather at orchards dot example',
    ),
    [
      'places:Leeds',
      'postal_ca:LS6 3BJ',
      'places:Galway',
      'postal_ca:H91 X4K7',
      'email:deb dot fairweather at orchards dot example',
    ],
  );
  assert.deepEqual(
    found(
      'Password: Tr0ub4dor&3. Reset the password you chose. MAC 00:1A:2B:3C:4D:5E, IP 2001:db8:4c2::1f.',
    ),
    [
      'credential:Tr0ub4dor&3',
      'device:00:1A:2B:3C:4D:5E',
      'ip:2001:db8:4c2::1f',
    ],
  );
  assert.deepEqual(found('She is age 94; he is ninety-one years old.'), [
    'age90:age 94',
    'age90:ninety-one years old',
  ]);
  assert.deepEqual(
    found(
      'Log in as user hunter.al, password Sweetgrass#2019; the PIN, 0834. Amex ending 34224. Enter your password to continue.',
    ),
    [
      'credential:hunter.al',
      'credential:Sweetgrass#2019',
      'credential:0834',
      'card_partial:Amex ending 34224',
    ],
  );
});

test('second round: partial cards, unlabelled birth dates, ages, places and non-US addresses', () => {
  const pci = planFor(['pci']).detectorIds;
  assert.deepEqual(
    found('Visa ending 3637, sec code 406; card ****1234 exp 04/28', pci),
    [
      'card_partial:Visa ending 3637',
      'cvv:406',
      'card_partial:****1234',
      'card_exp:04/28',
    ],
  );
  const court = planFor(['frcp52']).detectorIds;
  assert.deepEqual(
    found(
      'Hearing set for 02/10/2026. The witness (03/14/1934) testified.',
      court,
    ),
    ['dob:03/14/1934'],
    'under the court rule an old date is treated as a birth date and recent dates are left alone',
  );
  assert.deepEqual(
    found('Mrs Kowalczyk, 91, turned 92 in May.').filter(x =>
      x.startsWith('age'),
    ),
    ['age90:91', 'age90:turned 92'],
  );
  const tax = planFor(['irc7216']).detectorIds;
  assert.deepEqual(
    found('She lives in Wenatchee and moved to Tofino in March.', tax),
    ['places:Wenatchee', 'places:Tofino'],
  );
  assert.deepEqual(
    found(
      '3 Toft Green; Unit 6, Ballybrit Business Park; Keizersgracht 418-II',
    ).map(x => x.split(':')[0]),
    ['street', 'street', 'street'],
  );
});

test('a state is replaced only when a selected rule covers it', () => {
  const text = 'She moved from Dallas, TX 75201 to Spokane, Washington.';
  // HIPAA lists "geographic subdivisions smaller than a State", so the state
  // itself may stay.
  const hipaa = planFor(['hipaa']).detectorIds;
  assert.ok(!hipaa.includes('region'));
  assert.deepEqual(found(text, hipaa), [
    'places:Dallas',
    'zip:75201',
    'places:Spokane',
  ]);
  // Tax return information, GLBA, GDPR and NIST cover the address or location
  // with no such exception.
  for (const rule of ['irc7216', 'glba', 'gdpr', 'nist']) {
    const ids = planFor([rule]).detectorIds;
    assert.ok(ids.includes('region'), `${rule} covers states`);
    assert.deepEqual(
      found(text, ids).filter(x => /^(places|region)/.test(x)),
      ['places:Dallas', 'region:TX', 'places:Spokane', 'region:Washington'],
    );
  }
  // HIPAA together with any of those: the stricter rule wins.
  assert.ok(planFor(['hipaa', 'irc7216']).detectorIds.includes('region'));
  // The court-filing and payment-card rules say nothing about places.
  assert.deepEqual(found(text, planFor(['frcp52']).detectorIds), []);
});

// Third round: every miss in a sub-category is looked at and fixed with a
// general rule.
test('dates: the remaining written forms', () => {
  const dates = t =>
    found(t)
      .filter(x => /^(date|dob):/.test(x))
      .map(x => x.split(':').slice(1).join(':'));
  assert.deepEqual(
    dates('DATED this 19th day of February, 2026. Answers by Friday the 23rd.'),
    ['19th day of February, 2026', 'Friday the 23rd'],
  );
  assert.deepEqual(
    dates('THE OPERATION -- JANUARY 23, 2025; passport exp. 14 FEB 2029'),
    ['JANUARY 23, 2025', '14 FEB 2029'],
  );
  assert.deepEqual(dates('Date: Oct 5/26; permit runs out 3/2027'), [
    'Oct 5/26',
    '3/2027',
  ]);
  assert.deepEqual(
    dates(
      'Logs for June 1-4, 2025. Available November 10 or 12, at our office.',
    ),
    ['June 1-4, 2025', 'November 10 or 12'],
  );
  assert.deepEqual(dates('Signed 10/27/2026 4:52 PM'), ['10/27/2026 4:52 PM']);
  assert.deepEqual(
    dates('He took a loan in May. You may go; it may rain.'),
    ['May'],
    'a month after "in", never the verb "may"',
  );
  assert.deepEqual(dates('born in the summer of 1959'), ['the summer of 1959']);
  assert.deepEqual(
    found('**Start date:** 2026-05-18'),
    ['date:2026-05-18'],
    'Markdown bold is not a masked number',
  );
});

test('money described as a share of pay', () => {
  assert.deepEqual(
    found('a role paying roughly sixty percent of her former salary').filter(
      x => x.startsWith('money'),
    ),
    ['money:sixty percent of her former salary'],
  );
  assert.deepEqual(
    found('Sixty percent of respondents agreed; a 5% discount applies.').filter(
      x => x.startsWith('money'),
    ),
    [],
  );
});

test('what a rule lets you keep', () => {
  assert.equal(KEEP.last4.apply('123-45-6789'), 'ending 6789');
  assert.equal(KEEP.last4.apply('4471-889-2203'), 'ending 2203');
  assert.equal(KEEP.year.apply('July 4, 1931'), '1931');
  assert.equal(KEEP.zip3.apply('98101'), '981XX');
  assert.equal(KEEP.initials.apply('Tom Whitfield'), 'T.W.');
  const req = planFor(['frcp52']).requiredBy;
  assert.equal(req.ssn[0].keep, 'last4');
  assert.equal(detectorById('ssn').placeholder, 'SSN');
});

// Rules added while taking each sub-category of the evaluation to 100%. All
// values are fictional.
test('record numbers: court numbers, confirmation codes, check numbers', () => {
  assert.deepEqual(
    found(
      'Lindqvist v. Larkfield, No. CI 26-4471, Douglas County District Court',
    ).filter(x => x.startsWith('record')),
    ['record:CI 26-4471'],
  );
  assert.deepEqual(
    found('He filed Chapter 7 (Bankr. E.D. Wis.,\nNo. 16-24817-gmh).').filter(
      x => x.startsWith('record'),
    ),
    ['record:16-24817-gmh'],
  );
  assert.deepEqual(
    found('Airfare, Economy Plus, conf. QK7M2X').filter(x =>
      x.startsWith('record'),
    ),
    ['record:QK7M2X'],
  );
  assert.deepEqual(
    found('the largest is ck #20841 for $1,950.00').filter(x =>
      x.startsWith('record'),
    ),
    ['record:20841'],
  );
});

test('a longer number is not cut up by the tax-ID or masked-card rules', () => {
  assert.deepEqual(found('paid on crop policy MPCI-19-0044817 and holds'), [
    'record:MPCI-19-0044817',
  ]);
  assert.deepEqual(
    found('loan # 0048-771203-9, bal.').map(x => x.split(':')[1]),
    ['0048-771203-9'],
  );
  assert.deepEqual(found('EIN 81-4472093.'), ['ein:81-4472093']);
  assert.deepEqual(found('member services (1-800-555-0177 x4402).'), [
    'phone:1-800-555-0177 x4402',
  ]);
  assert.deepEqual(found('card x4410 on file'), ['card_partial:x4410']);
});

test('places: cities before a state or country, counties in capitals, court towns', () => {
  const places = t =>
    found(t)
      .filter(x => x.startsWith('places'))
      .map(x => x.slice(7));
  assert.deepEqual(
    places('1375 East Ninth Street, 21st Floor\nCleveland, Ohio 44114'),
    ['Cleveland'],
  );
  assert.deepEqual(places('DOB: 22 Feb 1994, Đà Nẵng, Vietnam'), ['Đà Nẵng']);
  assert.deepEqual(places('SUPERIOR COURT OF WASHINGTON FOR KING COUNTY'), [
    'KING COUNTY',
  ]);
  assert.deepEqual(
    places('Court:    Flagstaff Justice Court, Coconino County'),
    ['Flagstaff', 'Coconino County'],
  );
  assert.deepEqual(
    places(
      'UNITED STATES DISTRICT COURT\nWESTERN DISTRICT OF WASHINGTON AT SEATTLE',
    ),
    ['SEATTLE'],
  );
  assert.deepEqual(
    places('In Kansas City the United States District Court sat.'),
    ['Kansas City'],
  );
  assert.deepEqual(
    places('She moved\nback to Durban; the sub banks in Lyon.'),
    ['Durban', 'Lyon'],
  );
});

test('dates, money, web and postal forms from the second pass', () => {
  const only = (t, p) =>
    found(t)
      .filter(x => x.startsWith(p))
      .map(x => x.slice(p.length + 1));
  assert.deepEqual(only('due the 13th of October; paid 2026/10/05', 'date'), [
    'the 13th of October',
    '2026/10/05',
  ]);
  assert.deepEqual(only('wire of EUR 1.240,00 sent', 'money'), [
    'EUR 1.240,00',
  ]);
  assert.deepEqual(
    only('log in at vpn.brightwaterbenefits.example today', 'url'),
    ['vpn.brightwaterbenefits.example'],
  );
  assert.deepEqual(only('Agrippinaufer 41 | 50678 Köln', 'zip'), ['50678']);
  assert.deepEqual(only('SIN on the old record (9XX XXX 118)', 'sin_ca'), [
    '9XX XXX 118',
  ]);
  assert.deepEqual(only('Laptop serial **PF4XK2M9**, Windows 11', 'device'), [
    'PF4XK2M9',
  ]);
});

test('street addresses: one line, one cell, and the less common forms', () => {
  const streets = t =>
    found(t)
      .filter(x => x.startsWith('street'))
      .map(x => x.slice(7));
  assert.deepEqual(
    streets(
      'State Bar No. 284471\n1900 Soquel Avenue, Suite 410, Santa Cruz, CA 95062',
    ),
    ['1900 Soquel Avenue, Suite 410'],
  );
  assert.deepEqual(
    streets('218 555 0125\t600 Garfield Ave\tDuluth, MN 55802'),
    ['600 Garfield Ave'],
  );
  assert.deepEqual(
    streets('address:\n418 1/2 Cass St, Upper, La Crosse, WI 54601'),
    ['418 1/2 Cass St, Upper'],
  );
  assert.deepEqual(
    streets('Addr: #1204 - 13618 100 Avenue, Surrey BC  V3T 0A8'),
    ['#1204 - 13618 100 Avenue'],
  );
  assert.deepEqual(
    streets('2150 South 1300 East, Suite 500, Salt Lake City, Utah 84106'),
    ['2150 South 1300 East, Suite 500'],
  );
  assert.deepEqual(
    streets(
      'Address N3172 County Road K, Viroqua, WI 54665; shop at 4402 Highway 53',
    ),
    ['N3172 County Road K', '4402 Highway 53'],
  );
  assert.deepEqual(
    streets('home address\nR.R. 2 Box 118, Mifflinburg PA 17844'),
    ['R.R. 2 Box 118'],
  );
  assert.deepEqual(
    streets('at 1184 chemin Kamiskotia Road, Timmins ON  P4N 7C3'),
    ['1184 chemin Kamiskotia Road'],
  );
  assert.deepEqual(
    found('rent of $400 Park Avenue; on June 14 Main Street closed').map(
      x => x.split(':')[0],
    ),
    ['money', 'places', 'date', 'places'],
    'an amount or a date is not a house number; the street name is a place',
  );
});

test('states: codes without a comma, on plates and in captions', () => {
  const regions = t =>
    found(t)
      .filter(x => x.startsWith('region'))
      .map(x => x.slice(7));
  assert.deepEqual(
    regions('Mesa Verde Pharmacy, 2101 E. 20th St, Farmington NM 87401'),
    ['NM'],
  );
  assert.deepEqual(regions('VIN 1FTBR1C82NKA40917, AZ plate CKH7R42.'), ['AZ']);
  assert.deepEqual(regions('SUPERIOR COURT OF WASHINGTON FOR KING COUNTY'), [
    'WASHINGTON',
  ]);
  assert.deepEqual(
    regions(
      'Court of Common Pleas, Westmoreland County, Pa., No. 2025-CV-03381',
    ),
    ['Pa.'],
  );
  assert.deepEqual(regions('CITY: MURFREESBORO STATE: TN ZIP: 37129'), ['TN']);
});

test('money: rows of figures, spoken amounts, rates and continental forms', () => {
  const money = t =>
    found(t)
      .filter(x => x.startsWith('money'))
      .map(x => x.slice(6));
  assert.deepEqual(
    money(
      '1017    BILL   $34.10   88.0   3,137.20   41.50   156.86   --   2,207.55',
    ),
    ['$34.10', '3,137.20', '41.50', '156.86', '2,207.55'],
  );
  assert.deepEqual(
    money('Version 2.10 of the app shipped.'),
    [],
    'a lone decimal in a sentence is not money',
  );
  assert.deepEqual(
    money(
      'worth "around six fifty"; about 2.8 million in revenue, eighteen hundred a month',
    ),
    ['six fifty', '2.8 million', 'eighteen hundred a month'],
  );
  assert.deepEqual(
    money('quoted $89/mo; VAT 0% € 0,00; French copy shows 41 280,16 $'),
    ['$89/mo', '€ 0,00', '41 280,16 $'],
  );
  assert.deepEqual(money('union dues 28.50 plus garnishment 383.50'), [
    '28.50',
    '383.50',
  ]);
});

test('passwords, user names and codes', () => {
  const creds = t =>
    found(t)
      .filter(x => x.startsWith('credential'))
      .map(x => x.slice(11));
  assert.deepEqual(creds('he recited it as Polka1934! and left'), [
    'Polka1934!',
  ]);
  assert.deepEqual(creds('(user ID kravchukelec1, password Volts&Amps2024)'), [
    'kravchukelec1',
    'Volts&Amps2024',
  ]);
  assert.deepEqual(
    creds('Windows login is coadmin / Winter2026$. signed in as tboone.'),
    ['coadmin', 'Winter2026$', 'tboone'],
  );
  assert.deepEqual(
    creds('The login page is required; see the user manual.'),
    [],
  );
  assert.deepEqual(
    creds(
      'PIN issued to Tevita by the IRS for this season: 604417. Lockbox on side door, code **1930**.',
    ),
    ['604417', '1930'],
  );
  assert.deepEqual(
    found('ZIP code 17801, area code 604').filter(x =>
      x.startsWith('credential'),
    ),
    [],
  );
  assert.deepEqual(
    found('read them the CVV (406); SSN ends 6134; transit 40418  inst 889'),
    ['cvv:406', 'ssn:6134', 'routing:40418', 'routing:889'],
  );
});

test('reference numbers after the word that says what they are', () => {
  const records = t =>
    found(t)
      .filter(x => x.startsWith('record'))
      .map(x => x.slice(7));
  assert.deepEqual(
    records(
      'unit T5512; lot 203-B; box #214; folio 88104-2; tracking no. KQ 4471 8802 3GB',
    ),
    ['T5512', '203-B', '214', '88104-2', 'KQ 4471 8802 3GB'],
  );
  assert.deepEqual(records('a lot of 1200 people; company 2025 revenue'), []);
  assert.deepEqual(
    found(
      'Calloway Jefferson-Ruiz, #68214MO; Marguerite Oyelaran (P71443); CRPO # 009417',
    ),
    ['passport_dl:68214MO', 'passport_dl:P71443', 'passport_dl:009417'],
  );
});

test('ages over 89 and phone numbers in their spoken and shorthand forms', () => {
  const ages = t =>
    found(t)
      .filter(x => x.startsWith('age90'))
      .map(x => x.slice(6));
  assert.deepEqual(
    ages(
      'she is 91 now. DOB 02/11/1933 (93 y/o M). My mother is 92 years old. died in 2026 at 97.',
    ),
    ['91', '93 y/o', '92 years old', 'at 97'],
  );
  assert.deepEqual(
    ages('He is 95 percent sure; she is 91 days late; she is 45.'),
    [],
  );
  assert.deepEqual(
    found(
      'called (nine two eight, 555-0164). DDI 01904 555 0117; direct\n010-555 01 62',
    ).filter(x => x.startsWith('phone')),
    [
      'phone:nine two eight, 555-0164',
      'phone:01904 555 0117',
      'phone:010-555 01 62',
    ],
  );
});

// Rules added from the third test set (documents written without sight of the
// detectors).
test('dates outside the US and in hurried notes', () => {
  const dates = t =>
    found(t)
      .filter(x => /^(date|dob):/.test(x))
      .map(x => x.split(':').slice(1).join(':'));
  assert.deepEqual(
    dates(
      'Sarlat, le 12 novembre 2025. Signature mardi 9 décembre; reçu le 14 nov.',
    ),
    ['le 12 novembre 2025', 'mardi 9 décembre', 'le 14 nov.'],
  );
  assert.deepEqual(
    dates('Fecha: 5 de noviembre de 2025; cita martes 18 de noviembre'),
    ['5 de noviembre de 2025', 'martes 18 de noviembre'],
  );
  assert.deepEqual(
    dates(
      'moved aug 15. appt sat 2/28 9am. ring him Fri 14th. letter of 29/10/25; paid 30/10',
    ),
    ['aug 15', 'sat 2/28', 'Fri 14th', '29/10/25', '30/10'],
  );
  assert.deepEqual(
    dates('surgery on the 22nd; docs due by the 20th; on the 2nd floor'),
    ['the 22nd', 'the 20th'],
  );
  assert.deepEqual(
    dates('Fee: 33 1/3% pre-suit'),
    [],
    'a fraction is not a date',
  );
});

test('street addresses and towns outside the US', () => {
  const some = (t, kinds) =>
    found(t).filter(x => kinds.includes(x.split(':')[0]));
  assert.deepEqual(
    some('4418, avenue du Mont-Royal Est\tMontréal', ['street']),
    ['street:4418, avenue du Mont-Royal Est'],
  );
  assert.deepEqual(
    some('1150, 3e Avenue, bureau 210, Québec (Québec) G1L 2X8', ['street']),
    ['street:1150, 3e Avenue, bureau 210'],
  );
  assert.deepEqual(
    some('Old address: Calle Licenciado Poza 44, 3º Izda., 48011 Bilbao', [
      'street',
      'zip',
      'places',
    ]),
    ['street:Calle Licenciado Poza 44, 3º Izda.', 'zip:48011', 'places:Bilbao'],
  );
  assert.deepEqual(
    some('still at Flat 3, 27 Stricklandgate til the move', ['street']),
    ['street:Flat 3, 27 Stricklandgate'],
  );
  assert.deepEqual(
    some('Unit 4, 18 Wattle Grove Road, Marrickville NSW 2204', [
      'street',
      'places',
      'region',
      'zip',
    ]),
    [
      'street:Unit 4, 18 Wattle Grove Road',
      'places:Marrickville',
      'region:NSW',
      'zip:2204',
    ],
  );
  assert.deepEqual(
    some('old adress 2218 w tioga st phila; traffic stop on rivers ave', [
      'street',
      'places',
    ]),
    ['street:2218 w tioga st', 'places:rivers ave'],
  );
  assert.deepEqual(some('IN AND FOR THE COUNTY OF PIMA', ['places']), [
    'places:PIMA',
  ]);
});

test('money, tax numbers, phones and codes outside the US', () => {
  const only = (t, p) =>
    found(t)
      .filter(x => x.startsWith(p))
      .map(x => x.slice(p.length + 1));
  assert.deepEqual(
    only(
      'Price 92 000 €, deposit 4 600 €; profit 112.480,17 €; chèque NSF (1 200 $)',
      'money',
    ),
    ['92 000 €', '4 600 €', '112.480,17 €', '1 200 $'],
  );
  assert.deepEqual(
    only("about R$ 61.000 and CHF 61'000; mom has maybe 2 grand", 'money'),
    ['R$ 61.000', "CHF 61'000", '2 grand'],
  );
  assert.deepEqual(only('ABN 51 824 753 556   TFN 481 207 339', 'ein'), [
    '51 824 753 556',
    '481 207 339',
  ]);
  assert.deepEqual(
    only(
      'Tél. 05 55 55 01 42; second phone (02) 5550 0142; Adjuster, ext 4418',
      'phone',
    ),
    ['05 55 55 01 42', '(02) 5550 0142', '4418'],
  );
  assert.deepEqual(
    only('BSB 641-800, acct 10447 2218; sort 60-44-18', 'routing'),
    ['641-800', '60-44-18'],
  );
  assert.deepEqual(only('your Octavia as YK21 HXT; car rego 448 KT7', 'vin'), [
    'YK21 HXT',
    '448 KT7',
  ]);
});

test('SSN endings, card codes, passwords and handles in more forms', () => {
  assert.deepEqual(
    found('Last four only, Lottie.\n A.  4570.').filter(x =>
      x.startsWith('ssn'),
    ),
    ['ssn:4570'],
  );
  assert.deepEqual(
    found('SSNs ending 4983 (Everett) and 8373 (Noor)').filter(x =>
      x.startsWith('ssn'),
    ),
    ['ssn:4983', 'ssn:8373'],
  );
  assert.deepEqual(
    found('code on the back 771; debit card 4769 15•• •••• 2996').filter(x =>
      /^(cvv|card_partial)/.test(x),
    ),
    ['cvv:771', 'card_partial:4769 15•• •••• 2996'],
  );
  const creds = t =>
    found(t)
      .filter(x => x.startsWith('credential'))
      .map(x => x.slice(11));
  assert.deepEqual(
    creds(
      'the password he was using, Ruffin1958, is weak; admin pw Rainbow2Brown.',
    ),
    ['Ruffin1958', 'Rainbow2Brown'],
  );
  assert.deepEqual(
    creds('her running account, @shirin.g.runs; cashapp $tavi_L'),
    ['@shirin.g.runs', '$tavi_L'],
  );
  assert.deepEqual(
    creds('Email me at deb@orchards.example about the $250 fee'),
    [],
  );
});

test("numbers that are not anybody's data", () => {
  assert.deepEqual(
    found('See 29 C.F.R. § 1601.12 and Wis. Stat. § 853.03; RCW 7.105.100.'),
    ['region:Wis.'],
    'only the state is taken, not the section numbers',
  );
  assert.deepEqual(
    found('Get 2022-2024 joint returns').filter(x => x.startsWith('account')),
    [],
  );
  assert.deepEqual(
    found('shows $15,220.04 and 31,870 online miles').filter(x =>
      x.startsWith('money'),
    ),
    ['money:$15,220.04'],
  );
});

// The second way to choose what is replaced: by class of data, ranked by
// measured accuracy.
test('classes of data: every ready check belongs to one class, and the ranking is the measured one', () => {
  const ready = DETECTORS.filter(d => d.status === 'ready')
    .map(d => d.id)
    .sort();
  assert.deepEqual(
    DATA_CLASSES.flatMap(c => c.detectors).sort(),
    ready,
    'each check is switched on by exactly one class',
  );
  const replaced = DATA_CLASSES.filter(c => c.action === 'replace');
  for (let i = 1; i < replaced.length; i++) {
    assert.ok(
      replaced[i - 1].rate >= replaced[i].rate,
      `${replaced[i - 1].id} ranks above ${replaced[i].id}`,
    );
  }
  assert.equal(
    DATA_CLASSES[DATA_CLASSES.length - 1].action,
    'flag',
    'the flag-only class comes last',
  );
  for (const c of replaced) {
    assert.ok(c.of > 0, `${c.id} has a measurement`);
    assert.equal(c.tier, ACCURACY_TIERS.find(t => c.rate >= t.min).id);
  }
  assert.deepEqual(
    ACCURACY_TIERS.map(t => t.label),
    ['Highly accurate', 'Accurate', 'Less accurate'],
  );
});

test('a plan made from classes runs only the checks of the classes chosen', () => {
  assert.deepEqual(planForClasses(['email', 'phone']).detectorIds, [
    'email',
    'phone',
  ]);
  assert.equal(planForClasses(['email', 'phone']).usesModel, false);
  assert.equal(planForClasses(['names']).usesModel, true);
  assert.deepEqual(planForClasses([]).detectorIds, []);
  assert.equal(
    planForClasses(DEFAULT_CLASSES).detectorIds.length,
    DETECTORS.filter(d => d.status === 'ready').length,
  );
  assert.deepEqual(
    found(
      'Call 604-555-0142 about $8,400 on March 14, 2026',
      planForClasses(['phone']).detectorIds,
    ),
    ['phone:604-555-0142'],
  );
});
