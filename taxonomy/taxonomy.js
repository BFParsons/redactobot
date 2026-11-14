/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Sensitive-information taxonomy for Redactobot, organized by
 * rulebook.
 *
 * The user picks which rules apply to them (FRAMEWORKS). Each rule lists what
 * it says must be protected, in its own words (requirements), and each
 * requirement points at the DETECTORS that find it. Only the detectors needed
 * by the chosen rules are run, so no compute is spent on things the user's
 * rules do not cover.
 *
 * Plain ES module, no build step. Runs in the browser and in Node (see
 * taxonomy.test.mjs). How each source was verified: SOURCES.md.
 */

import {
  PATTERN_DETECTORS,
  isRegion,
  luhn,
  validSsn,
  validSin,
  validCard,
  validIban,
  validRouting,
} from './detectors.js';
import {MEASURED} from './accuracy.js';
import {identityCandidates} from './identity-patterns.js';

export {isRegion, luhn, validSsn, validSin, validCard, validIban, validRouting};
const digits = s => s.replace(/\D/g, '');

// ---------- what a rule lets you keep ----------
/**
 * Forms a rule lets stay in place of the full value. Some rules say what may
 * stay; the app can offer these forms. Each entry has a label and
 * apply(value), which returns the reduced form, or null when the value has
 * none.
 */
export const KEEP = {
  last4: {
    label: 'last four digits',
    apply: s => {
      const d = digits(s);
      return d.length > 4 ? `ending ${d.slice(-4)}` : null;
    },
  },
  year: {
    label: 'the year only',
    apply: s => (s.match(/\b(?:19|20)\d{2}\b/) || [null])[0],
  },
  zip3: {
    label:
      'first three digits of the ZIP code (only where that area has more than 20,000 people)',
    apply: s => {
      const d = digits(s);
      return d.length >= 5 ? `${d.slice(0, 3)}XX` : null;
    },
  },
  initials: {
    label: "a minor's initials",
    apply: s =>
      s
        .split(/\s+/)
        .filter(Boolean)
        .map(w => w[0].toUpperCase() + '.')
        .join(''),
  },
  age90: {label: 'a single "90 or older" group', apply: () => '90 or older'},
};

// ---------- detectors ----------
/**
 * Every detector: the pattern detectors, then the model and review ones.
 * - kind: 'pattern' (instant, deterministic; defined in detectors.js) |
 *   'model' (on-device model) | 'review' (cloud second look at text the user
 *   already approved)
 * - action: 'replace' (swap for a placeholder) | 'warn' (tell the user it is
 *   present)
 * - status: 'ready' | 'planned' (listed so coverage gaps are visible; not
 *   built yet)
 */
export const DETECTORS = [
  ...PATTERN_DETECTORS,
  {
    id: 'names',
    group: 'Names',
    label: 'Names of people and organizations',
    placeholder: 'PERSON / COMPANY',
    kind: 'model',
  },
  {
    id: 'sensitive_topics',
    group: 'Sensitive topics',
    label:
      'Sensitive personal topics (health, ethnicity, religion, politics, union membership, sexual orientation, immigration status, genetic data, criminal history)',
    kind: 'model',
    action: 'warn',
  },
  {
    id: 'indirect',
    group: 'Sensitive topics',
    label:
      'Details that identify someone indirectly (relationships, distinctive deals or property)',
    kind: 'review',
    action: 'warn',
    status: 'planned',
  },
].map(d => ({action: 'replace', status: 'ready', ...d}));

const TAX_IDS = ['ssn', 'ein', 'sin_ca', 'bn_ca'];
const ACCOUNTS = ['account', 'iban', 'routing', 'card', 'card_partial'];

// ---------- frameworks ----------
/**
 * The rulebooks the user can choose from.
 * - kind: 'redaction' (the rule lists what to remove) | 'definition' (the
 *   rule defines what must be protected).
 * - Each requirement: ref, text (the rule's wording, shortened), detectors,
 *   and optionally keep (what the rule lets remain), gap (what we do not
 *   catch), na (not applicable to text).
 */
export const FRAMEWORKS = [
  {
    id: 'frcp52',
    short: 'Federal court filings',
    audience: 'Lawyers',
    kind: 'redaction',
    name: 'Federal Rules of Civil Procedure, Rule 5.2',
    cite: 'Fed. R. Civ. P. 5.2(a)',
    jurisdiction: 'US',
    url: 'https://www.law.cornell.edu/rules/frcp/rule_5.2',
    summary:
      'What must be cut down before a document is filed in federal court.',
    requirements: [
      {
        ref: '5.2(a)(1)',
        text: 'Social-security number',
        detectors: ['ssn'],
        keep: 'last4',
      },
      {
        ref: '5.2(a)(1)',
        text: 'Taxpayer-identification number',
        detectors: ['ein', 'sin_ca', 'bn_ca'],
        keep: 'last4',
      },
      {
        ref: '5.2(a)(2)',
        text: 'Birth date',
        detectors: ['dob'],
        keep: 'year',
        gap: 'Dates labelled as a birth date are caught, and so are dates at least 16 years older than the newest date in the document. Other dates are left alone.',
      },
      {
        ref: '5.2(a)(3)',
        text: 'Name of an individual known to be a minor',
        detectors: ['names'],
        keep: 'initials',
        gap: 'All names are found; you decide which belong to minors.',
      },
      {
        ref: '5.2(a)(4)',
        text: 'Financial-account number',
        detectors: ACCOUNTS,
        keep: 'last4',
      },
    ],
  },
  {
    id: 'irc7216',
    short: 'Tax return information',
    audience: 'Accountants',
    kind: 'definition',
    name: 'Internal Revenue Code § 7216 regulations',
    cite: '26 CFR § 301.7216-1(b)(3)',
    jurisdiction: 'US',
    url: 'https://www.law.cornell.edu/cfr/text/26/301.7216-1',
    summary:
      'Tax preparers may not disclose information furnished for preparing a return.',
    requirements: [
      {ref: '(b)(3)(i)', text: "A taxpayer's name", detectors: ['names']},
      {
        ref: '(b)(3)(i)',
        text: "A taxpayer's address",
        detectors: ['street', 'zip', 'postal_ca', 'places', 'region'],
        gap: 'City names are caught when written with a state or after a clear cue such as "lives in".',
      },
      {
        ref: '(b)(3)(i)',
        text: "A taxpayer's identifying number",
        detectors: TAX_IDS,
      },
      {
        ref: '(b)(3)(i)',
        text: 'Any other information furnished for, or in connection with, the preparation of a tax return',
        detectors: ['money', ...ACCOUNTS, 'email', 'phone'],
        gap: 'This is open-ended. Amounts, accounts and contact details are caught; review the rest yourself.',
      },
    ],
  },
  {
    id: 'glba',
    short: 'Customer financial information',
    audience: 'Accountants',
    kind: 'definition',
    name: 'Gramm-Leach-Bliley Act, FTC Safeguards Rule',
    cite: '16 CFR § 314.2(l), (o)',
    jurisdiction: 'US',
    url: 'https://www.law.cornell.edu/cfr/text/16/314.2',
    summary:
      'Covers tax preparers and other financial businesses. Defines the customer information they must safeguard.',
    requirements: [
      {
        ref: '(o)(2)(i)(C)',
        text: 'The fact that an individual is or has been one of your customers',
        detectors: ['names'],
      },
      {
        ref: '(o)(2)(i)(A)',
        text: 'Information a consumer provides on an application for a financial product or service',
        detectors: [
          'email',
          'phone',
          'street',
          'zip',
          'postal_ca',
          'places',
          'region',
          ...TAX_IDS,
        ],
        gap: 'Contact details and ID numbers are caught; other application answers are not.',
      },
      {
        ref: '(o)(2)(i)(B)',
        text: 'Account balance information, payment history, overdraft history, and credit or debit card purchase information',
        detectors: ['money', ...ACCOUNTS],
      },
      {
        ref: '(o)(2)(i)(G)',
        text: 'Information from a consumer report',
        detectors: [],
        gap: 'Not detected. Check for credit report details yourself.',
      },
    ],
  },
  {
    id: 'hipaa',
    short: 'Health information',
    audience: 'Health',
    kind: 'redaction',
    name: 'HIPAA Privacy Rule, Safe Harbor de-identification',
    cite: '45 CFR § 164.514(b)(2)(i)',
    jurisdiction: 'US',
    url: 'https://www.law.cornell.edu/cfr/text/45/164.514',
    summary:
      'The 18 identifiers to remove so health information no longer identifies a person.',
    requirements: [
      {ref: '(A)', text: 'Names', detectors: ['names']},
      {
        ref: '(B)',
        text: 'All geographic subdivisions smaller than a State',
        detectors: ['street', 'zip', 'postal_ca', 'places'],
        keep: 'zip3',
        gap: 'This rule lets the State itself stay, so states are left as written unless another selected rule covers them. Cities are caught when written with a state or county, after a cue such as "lives in", or when the on-device model names them.',
      },
      {
        ref: '(C)',
        text: 'All elements of dates (except year) for dates directly related to an individual, and ages over 89',
        detectors: ['dob', 'date', 'age90'],
        keep: 'year',
      },
      {ref: '(D)', text: 'Telephone numbers', detectors: ['phone']},
      {ref: '(E)', text: 'Fax numbers', detectors: ['phone']},
      {ref: '(F)', text: 'Electronic mail addresses', detectors: ['email']},
      {
        ref: '(G)',
        text: 'Social security numbers',
        detectors: ['ssn', 'sin_ca'],
      },
      {
        ref: '(H)',
        text: 'Medical record numbers',
        detectors: ['record'],
        gap: 'Caught only when labelled (for example "MRN" or "medical record no.").',
      },
      {
        ref: '(I)',
        text: 'Health plan beneficiary numbers',
        detectors: ['record'],
        gap: 'Caught only when labelled (for example "member ID").',
      },
      {ref: '(J)', text: 'Account numbers', detectors: ACCOUNTS},
      {
        ref: '(K)',
        text: 'Certificate/license numbers',
        detectors: ['passport_dl'],
        gap: 'Caught only when labelled (for example "license no.").',
      },
      {
        ref: '(L)',
        text: 'Vehicle identifiers and serial numbers, including license plate numbers',
        detectors: ['vin'],
        gap: 'VINs are caught. License plates are caught only when labelled.',
      },
      {
        ref: '(M)',
        text: 'Device identifiers and serial numbers',
        detectors: ['device'],
        gap: 'Hardware addresses and labelled serial numbers are caught.',
      },
      {
        ref: '(N)',
        text: 'Web Universal Resource Locators (URLs)',
        detectors: ['url'],
      },
      {
        ref: '(O)',
        text: 'Internet Protocol (IP) address numbers',
        detectors: ['ip'],
      },
      {
        ref: '(P)',
        text: 'Biometric identifiers, including finger and voice prints',
        detectors: [],
        na: true,
      },
      {
        ref: '(Q)',
        text: 'Full face photographic images and any comparable images',
        detectors: [],
        na: true,
      },
      {
        ref: '(R)',
        text: 'Any other unique identifying number, characteristic, or code',
        detectors: ['record', 'indirect'],
        gap: 'Open-ended. Labelled record numbers are caught; review the rest yourself.',
      },
    ],
  },
  {
    id: 'ccpa',
    short: 'California sensitive personal information',
    audience: 'General',
    kind: 'definition',
    name: 'California Consumer Privacy Act',
    cite: 'Cal. Civ. Code § 1798.140(ae)',
    jurisdiction: 'US (California)',
    url: 'https://cppa.ca.gov/regulations/pdf/ccpa_statute.pdf',
    summary: "California's list of sensitive personal information.",
    requirements: [
      {
        ref: '(ae)(1)(A)',
        text: "Social security, driver's license, state identification card, or passport number",
        detectors: ['ssn', 'passport_dl'],
      },
      {
        ref: '(ae)(1)(B)',
        text: 'Account log-in, financial account, debit card, or credit card number in combination with any required security or access code, password, or credentials',
        detectors: [...ACCOUNTS, 'cvv', 'card_exp', 'credential'],
        gap: 'Account and card numbers are caught. Passwords and PINs are caught only when labelled.',
      },
      {ref: '(ae)(1)(C)', text: 'Precise geolocation', detectors: [], na: true},
      {
        ref: '(ae)(1)(D)',
        text: 'Racial or ethnic origin, citizenship or immigration status, religious or philosophical beliefs, or union membership',
        detectors: ['sensitive_topics'],
      },
      {
        ref: '(ae)(1)(E)',
        text: "The contents of a consumer's mail, email, and text messages",
        detectors: [],
        gap: "Not detected. If you paste a client's messages, the whole text is sensitive.",
      },
      {
        ref: '(ae)(1)(F)',
        text: 'Genetic data',
        detectors: ['sensitive_topics'],
      },
      {ref: '(ae)(1)(G)', text: 'Neural data', detectors: [], na: true},
      {
        ref: '(ae)(2)(A)',
        text: 'Biometric information processed to uniquely identify a consumer',
        detectors: [],
        na: true,
      },
      {
        ref: '(ae)(2)(B)',
        text: "Personal information collected and analyzed concerning a consumer's health",
        detectors: ['sensitive_topics'],
      },
      {
        ref: '(ae)(2)(C)',
        text: "Personal information collected and analyzed concerning a consumer's sex life or sexual orientation",
        detectors: ['sensitive_topics'],
      },
    ],
  },
  {
    id: 'pci',
    short: 'Payment card data',
    audience: 'General',
    kind: 'definition',
    name: 'PCI Data Security Standard v4.0.1',
    cite: 'PCI DSS v4.0.1, account data',
    jurisdiction: 'Industry standard',
    url: 'https://www.pcisecuritystandards.org/document_library/',
    summary:
      'The card data that businesses handling payment cards must protect.',
    requirements: [
      {
        ref: 'Cardholder data',
        text: 'Primary account number',
        detectors: ['card', 'card_partial'],
      },
      {ref: 'Cardholder data', text: 'Cardholder name', detectors: ['names']},
      {
        ref: 'Cardholder data',
        text: 'Expiration date',
        detectors: ['card_exp'],
        gap: 'Caught only when labelled (for example "exp 04/28").',
      },
      {ref: 'Cardholder data', text: 'Service code', detectors: [], na: true},
      {
        ref: 'Sensitive authentication data',
        text: 'Card verification code',
        detectors: ['cvv'],
        gap: 'Caught only when labelled (for example "CVV").',
      },
      {
        ref: 'Sensitive authentication data',
        text: 'Full track data; PINs and PIN blocks',
        detectors: [],
        na: true,
      },
    ],
  },
  {
    id: 'gdpr',
    short: 'EU personal data',
    audience: 'General',
    kind: 'definition',
    name: 'EU General Data Protection Regulation',
    cite: 'GDPR Art. 4(1), 9(1), 10',
    jurisdiction: 'EU',
    url: 'https://gdpr-info.eu/art-9-gdpr/',
    summary:
      'The EU definition of personal data and its specially protected categories.',
    requirements: [
      {ref: 'Art. 4(1)', text: 'A name', detectors: ['names']},
      {
        ref: 'Art. 4(1)',
        text: 'An identification number',
        detectors: [...TAX_IDS, 'passport_dl', ...ACCOUNTS, 'record'],
      },
      {
        ref: 'Art. 4(1)',
        text: 'Location data',
        detectors: ['street', 'zip', 'postal_ca', 'places', 'region'],
        gap: 'Cities are caught only when written with a state, province or county.',
      },
      {
        ref: 'Art. 4(1)',
        text: 'An online identifier',
        detectors: ['email', 'url', 'ip', 'device', 'credential'],
      },
      {
        ref: 'Art. 4(1)',
        text: 'Factors specific to the physical, physiological, genetic, mental, economic, cultural or social identity of the person',
        detectors: ['indirect'],
      },
      {
        ref: 'Art. 9(1)',
        text: 'Racial or ethnic origin, political opinions, religious or philosophical beliefs, trade union membership',
        detectors: ['sensitive_topics'],
      },
      {
        ref: 'Art. 9(1)',
        text: 'Genetic data; biometric data used to uniquely identify a person',
        detectors: ['sensitive_topics'],
      },
      {
        ref: 'Art. 9(1)',
        text: 'Data concerning health, sex life or sexual orientation',
        detectors: ['sensitive_topics'],
      },
      {
        ref: 'Art. 10',
        text: 'Criminal convictions and offences',
        detectors: ['sensitive_topics'],
      },
    ],
  },
  {
    id: 'nist',
    short: 'US federal PII guidance',
    audience: 'General',
    kind: 'definition',
    name: 'NIST SP 800-122, Guide to Protecting the Confidentiality of PII',
    cite: 'NIST SP 800-122 § 2.1–2.2',
    jurisdiction: 'US',
    url: 'https://csrc.nist.gov/pubs/sp/800/122/final',
    summary:
      "The US government's general definition of personally identifiable information.",
    requirements: [
      {
        ref: '§ 2.2',
        text: "Name, such as full name, maiden name, mother's maiden name, or alias",
        detectors: ['names'],
      },
      {
        ref: '§ 2.2',
        text: "Personal identification number, such as SSN, passport number, driver's license number, taxpayer identification number, or financial account or credit card number",
        detectors: [...TAX_IDS, 'passport_dl', ...ACCOUNTS],
      },
      {
        ref: '§ 2.2',
        text: 'Address information, such as street address or email address',
        detectors: ['street', 'zip', 'postal_ca', 'places', 'region', 'email'],
      },
      {
        ref: '§ 2.2',
        text: 'Personal characteristics, including photographic image, fingerprints, handwriting, or other biometric data',
        detectors: [],
        na: true,
      },
      {
        ref: '§ 2.1',
        text: 'Date and place of birth',
        detectors: ['dob', 'places', 'region'],
        gap: 'Places are caught only when written with a state, province or county.',
      },
      {
        ref: '§ 2.1',
        text: 'Information linked or linkable to an individual, such as medical, educational, financial, and employment information',
        detectors: ['money', 'sensitive_topics', 'indirect'],
      },
    ],
  },
];

/**
 * Professional duties are broader than any list: they cover everything about a
 * client. They are the reason the user always reviews before sending, so they
 * are shown, not selected.
 */
export const PROFESSIONAL_DUTIES = [
  {
    id: 'aba16',
    audience: 'Lawyers',
    name: 'ABA Model Rule 1.6',
    cite: 'ABA Model Rule 1.6(a), (c)',
    url: 'https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_6_confidentiality_of_information/',
    summary:
      'A lawyer must not reveal information relating to the representation of a client, and must make reasonable efforts to prevent unauthorized disclosure.',
  },
  {
    id: 'aicpa',
    audience: 'Accountants',
    name: 'AICPA Confidential Client Information Rule',
    cite: 'AICPA ET § 1.700.001',
    url: 'https://pub.aicpa.org/codeofconduct/',
    summary:
      'A member in public practice must not disclose confidential client information without the specific consent of the client.',
  },
];

/** Quick picks shown at the top of the selector. */
export const AUDIENCES = [
  {id: 'lawyer', label: 'Law practice', frameworks: ['frcp52']},
  {
    id: 'accountant',
    label: 'Accounting and tax',
    frameworks: ['irc7216', 'glba'],
  },
  {id: 'health', label: 'Health records', frameworks: ['hipaa']},
  {id: 'all', label: 'All rules', frameworks: FRAMEWORKS.map(f => f.id)},
];
/** The default selection of framework ids. */
export const DEFAULT_FRAMEWORKS = ['frcp52', 'irc7216', 'glba'];

// ---------- classes of data ---------- The second way to choose what is
// replaced: by the kind of value, not by the rule that calls for it. Each class
// names the checks it switches on and the answer-key categories its accuracy is
// measured by. The figures come from ./accuracy.js (the test set nobody has
// inspected), so the ranking shown to the user is the measured one, and changes
// when the measurement does. action 'flag': the values are underlined for
// review and sent as written unless ticked.
const CLASS_LIST = [
  {
    id: 'email',
    label: 'Email addresses',
    example: 'margaret@whitfieldholdings.example',
    detectors: ['email'],
    measuredBy: ['email'],
  },
  {
    id: 'online',
    label: 'Web and IP addresses',
    example: 'portal.firm.example/c/4471, 203.0.113.57',
    detectors: ['url', 'ip'],
    measuredBy: ['url', 'ip_address'],
  },
  {
    id: 'phone',
    label: 'Phone and fax numbers',
    example: '604-555-0142',
    detectors: ['phone'],
    measuredBy: ['phone'],
  },
  {
    id: 'postal',
    label: 'ZIP and postal codes',
    example: '98118, V3T 0A8',
    detectors: ['zip', 'postal_ca'],
    measuredBy: ['postal_code'],
  },
  {
    id: 'dob',
    label: 'Birth dates',
    example: 'DOB 05/09/1979',
    detectors: ['dob'],
    measuredBy: ['date_of_birth'],
  },
  {
    id: 'money',
    label: 'Money amounts',
    example: '$310,500.75, 75k, 46 000 €',
    detectors: ['money'],
    measuredBy: ['money_amount'],
  },
  {
    id: 'bank',
    label: 'Bank account, routing and IBAN numbers',
    example: 'account 4471-889-2203',
    detectors: ['account', 'iban', 'routing'],
    measuredBy: ['bank_account', 'routing_number', 'iban'],
  },
  {
    id: 'gov_id',
    label: 'Passport, license and other government IDs',
    example: 'passport no. A09417726',
    detectors: ['passport_dl'],
    measuredBy: ['government_id'],
  },
  {
    id: 'names',
    label: 'Names of people and organizations',
    example: 'Margaret Whitfield, Harbourline Marine Supply',
    detectors: ['names'],
    measuredBy: ['person_name', 'organization_name'],
  },
  {
    id: 'tax_id',
    label: 'Social Security and tax ID numbers',
    example: 'SSN 542-17-7388, EIN 91-1740226',
    detectors: ['ssn', 'ein', 'sin_ca', 'bn_ca'],
    measuredBy: ['ssn', 'tax_id'],
  },
  {
    id: 'date',
    label: 'Dates',
    example: 'March 14, 2026',
    detectors: ['date'],
    measuredBy: ['date'],
  },
  {
    id: 'record',
    label: 'Case, file, claim and other reference numbers',
    example: 'claim no. EPL-2025-0093317',
    detectors: ['record'],
    measuredBy: ['record_number'],
  },
  {
    id: 'place',
    label: 'Cities, counties and states',
    example: 'Tofino, Boulder County, TX',
    detectors: ['places', 'region'],
    measuredBy: ['place'],
  },
  {
    id: 'card',
    label: 'Payment card numbers, expiry dates and security codes',
    example: 'Visa ending 3637, exp 08/29',
    detectors: ['card', 'card_partial', 'card_exp', 'cvv'],
    measuredBy: ['payment_card', 'card_expiry', 'card_security_code'],
  },
  {
    id: 'device',
    label: 'Device serial numbers and hardware addresses',
    example: 'serial PF4XK2M9',
    detectors: ['device'],
    measuredBy: ['device_id'],
  },
  {
    id: 'street',
    label: 'Street addresses',
    example: '918 Juniper Court, Unit B',
    detectors: ['street'],
    measuredBy: ['street_address'],
  },
  {
    id: 'vehicle',
    label: 'Vehicle identification and plate numbers',
    example: 'VIN 1FTBR1C82NKA40917',
    detectors: ['vin'],
    measuredBy: ['vehicle_id'],
  },
  {
    id: 'credential',
    label: 'Passwords, PINs and user names',
    example: 'password Maple!4471',
    detectors: ['credential'],
    measuredBy: ['credential'],
  },
  {
    id: 'age90',
    label: 'Ages over 89',
    example: 'she is 91 now',
    detectors: ['age90'],
    measuredBy: ['age_over_89'],
  },
  {
    id: 'topics',
    label: 'Health details and other sensitive topics',
    example: 'a diagnosis, immigration status, religion',
    detectors: ['sensitive_topics'],
    measuredBy: ['flagged'],
    action: 'flag',
  },
];

/**
 * Accuracy tiers, best first. `min` is the lowest share of test values fully
 * caught.
 */
export const ACCURACY_TIERS = [
  {
    id: 'high',
    label: 'Highly accurate',
    min: 0.97,
    note: 'At least 97 in 100 test values were fully replaced.',
  },
  {
    id: 'medium',
    label: 'Accurate',
    min: 0.9,
    note: 'Between 90 and 97 in 100. Look over the highlights.',
  },
  {
    id: 'low',
    label: 'Less accurate',
    min: 0,
    note: 'Fewer than 90 in 100. Read the document for these yourself.',
  },
];

/**
 * The classes of data, each with its measured accuracy and tier, ranked from
 * most to least accurate.
 */
export const DATA_CLASSES = CLASS_LIST.map(c => {
  const caught = c.measuredBy.reduce(
    (n, k) => n + (MEASURED[k]?.caught ?? 0),
    0,
  );
  const of = c.measuredBy.reduce((n, k) => n + (MEASURED[k]?.of ?? 0), 0);
  const rate = of ? caught / of : 0;
  const action = c.action ?? 'replace';
  const tier =
    action === 'flag' ? 'flag' : ACCURACY_TIERS.find(t => rate >= t.min).id;
  return {...c, action, caught, of, rate, tier};
}).sort(
  (a, b) =>
    (a.action === 'flag') - (b.action === 'flag') ||
    b.rate - a.rate ||
    b.of - a.of,
);

/**
 * Finds a class of data by its id.
 * @param {string} id An id from DATA_CLASSES.
 * @return {(typeof DATA_CLASSES[number])|undefined} The class, or undefined
 *     when no class has that id.
 */
export const dataClassById = id => DATA_CLASSES.find(c => c.id === id);
/**
 * Every class is on to begin with: leaving something out is the user's
 * decision, not the default.
 */
export const DEFAULT_CLASSES = DATA_CLASSES.map(c => c.id);

/**
 * The same shape as planFor(), for a choice made by class of data instead of by
 * rule.
 * @param {!Array<string>} classIds Ids of the chosen DATA_CLASSES.
 * @return {{detectorIds: !Array<string>, planned: !Array<string>,
 *     usesModel: boolean, requiredBy: !Object}} The ready detectors to run,
 *     the chosen ones that are not built yet, whether a ready one needs the
 *     on-device model, and a requiredBy that is always empty.
 */
export function planForClasses(classIds) {
  const wanted = new Set(
    DATA_CLASSES.filter(c => classIds.includes(c.id)).flatMap(c => c.detectors),
  );
  const active = DETECTORS.filter(d => wanted.has(d.id));
  return {
    detectorIds: active.filter(d => d.status === 'ready').map(d => d.id),
    planned: active.filter(d => d.status !== 'ready').map(d => d.id),
    usesModel: active.some(d => d.kind === 'model' && d.status === 'ready'),
    requiredBy: {},
  };
}

// ---------- helpers ----------
/**
 * Finds a detector by its id.
 * @param {string} id An id from DETECTORS.
 * @return {(typeof DETECTORS[number])|undefined} The detector, or undefined
 *     when none has that id.
 */
export const detectorById = id => DETECTORS.find(d => d.id === id);
/**
 * Finds a framework by its id.
 * @param {string} id An id from FRAMEWORKS.
 * @return {(typeof FRAMEWORKS[number])|undefined} The framework, or
 *     undefined when none has that id.
 */
export const frameworkById = id => FRAMEWORKS.find(f => f.id === id);

/**
 * How well one requirement is covered: 'covered' | 'partial' | 'planned' |
 * 'none' | 'na'.
 * @param {!Object} req A framework requirement; its detectors, gap and na
 *     fields are read.
 * @return {string} 'na' when the requirement does not apply to text, 'none'
 *     when it lists no detectors, 'planned' when none of them is ready,
 *     'partial' when some are not ready or a gap is recorded, otherwise
 *     'covered'.
 */
export function coverage(req) {
  if (req.na) return 'na';
  const ds = req.detectors.map(detectorById);
  const ready = ds.filter(d => d.status === 'ready');
  if (!ready.length) return ds.length ? 'planned' : 'none';
  return req.gap || ready.length < ds.length ? 'partial' : 'covered';
}

/**
 * Work out what to run for a set of chosen rules. overrides: { detectorId:
 * true|false } lets the user switch single checks on or off. Returns {
 * detectorIds, requiredBy, usesModel, planned }.
 * @param {!Array<string>} frameworkIds Ids of the chosen FRAMEWORKS.
 * @param {!Object<string, boolean>=} overrides Detector ids to switch on
 *     (true) or off (false) whatever the rules call for.
 * @return {{detectorIds: !Array<string>, planned: !Array<string>,
 *     usesModel: boolean, requiredBy: !Object<string, !Array<{framework:
 *     string, ref: string, keep: ?string}>>}} The ready detectors to run,
 *     the wanted ones that are not built yet, whether a ready one needs the
 *     on-device model, and for each detector id the requirements that call
 *     for it.
 */
export function planFor(frameworkIds, overrides = {}) {
  const requiredBy = {};
  for (const f of FRAMEWORKS) {
    if (!frameworkIds.includes(f.id)) continue;
    for (const r of f.requirements) {
      for (const id of r.detectors) {
        requiredBy[id] ||= [];
        if (
          !requiredBy[id].some(x => x.framework === f.id && x.ref === r.ref)
        ) {
          requiredBy[id].push({
            framework: f.id,
            ref: r.ref,
            keep: r.keep || null,
          });
        }
      }
    }
  }
  const wanted = new Set(Object.keys(requiredBy));
  for (const [id, on] of Object.entries(overrides)) {
    if (on) wanted.add(id);
    else wanted.delete(id);
  }
  const active = DETECTORS.filter(d => wanted.has(d.id));
  return {
    detectorIds: active.filter(d => d.status === 'ready').map(d => d.id),
    planned: active.filter(d => d.status !== 'ready').map(d => d.id),
    usesModel: active.some(d => d.kind === 'model' && d.status === 'ready'),
    requiredBy,
  };
}

/**
 * Run the pattern detectors named in detectorIds. Earlier detectors claim
 * their text first, so an email is never also reported as an account number.
 * Returns matches sorted by position: { type, label, placeholder, text, start,
 * end }.
 * @param {string} text The text to search.
 * @param {!Array<string>} detectorIds Ids of the detectors to run.
 * @param {!Array<!Array<number>>=} taken [start, end] ranges already claimed
 *     by something else; no match may overlap them.
 * @return {!Array<{type: string, label: string, placeholder: string,
 *     text: string, start: number, end: number}>} The matches, sorted by
 *     start. A match that came from identityCandidates() may also carry a
 *     reviewReason string.
 */
export function detectPatterns(text, detectorIds, taken = []) {
  // `taken` is text already claimed by something else (a name, a table cell).
  // Rules skip it, so a later, narrower rule still gets its turn at what is
  // left.
  const claimed = taken.map(([s, e]) => [s, e]);
  // The number in a statute or regulation citation is public law, not anybody's
  // data: "29 C.F.R. § 1601.12", "Wis. Stat. § 853.03", "RCW 7.105.100",
  // "Family Law Act s. 183".
  for (const m of text.matchAll(
    /(?:§§?\s?|\b(?:U\.S\.C\.|C\.F\.R\.|Stat\.|Code|MCL|RCW|NRS|ORS|R\.S\.|Ann\.|Act,? ss?\.|Act s\.|Rule|Reg\.)\s(?:§§?\s?)?)\d[\d.:]*(?:\([\dA-Za-z]+\))*[\dA-Za-z-]*/g,
  )) {
    const at = m.index + m[0].search(/\d/);
    claimed.push([at, m.index + m[0].length]);
  }
  const out = [];
  const overlaps = (s, e) => claimed.some(([a, b]) => s < b && e > a);
  // Whole identifiers before narrower rules (for example a date-like fragment
  // of an ID).
  const supplemental = identityCandidates(text, detectorIds);
  const addSupplemental = m => {
    if (overlaps(m.start, m.end)) return;
    const d = detectorById(m.type);
    claimed.push([m.start, m.end]);
    out.push({...m, label: d.label, placeholder: d.placeholder});
  };
  for (const m of supplemental.filter(m => m.type !== 'places')) {
    addSupplemental(m);
  }
  // Facts about the whole document that a rule may need.
  const years = [...text.matchAll(/\b(?:19|20)\d{2}\b/g)]
    .map(m => Number(m[0]))
    .filter(y => y <= new Date().getFullYear() + 1);
  const zips = [
    ...text.matchAll(
      /\b(?:[A-Z]{2}|[A-Z][a-z]+)\.?,?\s{1,3}(\d{5})(?:-\d{4})?\b|\b(\d{5})-\d{4}\b/g,
    ),
  ].map(m => (m[1] ?? m[2]).slice(0, 3));
  const ctx = {
    latestYear: years.length ? Math.max(...years) : new Date().getFullYear(),
    zipPrefixes: new Set(zips),
    text,
  };
  for (const d of DETECTORS) {
    if (d.kind !== 'pattern' || !detectorIds.includes(d.id)) continue;
    if (d.id === 'places') {
      for (const m of supplemental.filter(m => m.type === 'places')) {
        addSupplemental(m);
      }
    }
    for (const rule of d.rules) {
      for (const m of text.matchAll(rule.re)) {
        const s = m.index;
        const e = s + m[0].length;
        if (!m[0].length || overlaps(s, e)) continue;
        if (rule.ok && !rule.ok(m[0], ctx, s)) continue;
        claimed.push([s, e]);
        out.push({
          type: d.id,
          label: d.label,
          placeholder: d.placeholder,
          text: m[0],
          start: s,
          end: e,
        });
      }
    }
  }
  return out.sort((a, b) => a.start - b.start);
}
