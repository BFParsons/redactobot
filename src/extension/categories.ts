/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The categories of private detail a user can choose to screen in
 * pastes, and the rule detectors and model kinds that each category switches
 * on.
 */

/**
 * Saved preferences contain category IDs only, never excerpts or model output.
 */
export const PASTE_CATEGORIES = [
  {
    id: 'names',
    label: 'People and organizations',
    detail: 'Names, initials and aliases',
    detectors: ['names'],
    model: ['person', 'company'],
  },
  {
    id: 'contact',
    label: 'Email addresses and phone numbers',
    detail: 'Including fax numbers',
    detectors: ['email', 'phone'],
    model: [],
  },
  {
    id: 'places',
    label: 'Addresses and places',
    detail: 'Street addresses, cities, states and postal codes',
    detectors: ['street', 'places', 'region', 'zip', 'postal_ca'],
    model: ['place'],
  },
  {
    id: 'records',
    label: 'Government IDs and record numbers',
    detail: 'Tax IDs, passports, licenses, medical records and case numbers',
    detectors: ['ssn', 'sin_ca', 'ein', 'bn_ca', 'passport_dl', 'record'],
    model: [],
  },
  {
    id: 'payments',
    label: 'Payment cards and bank accounts',
    detail:
      'Card numbers, security codes, expiration dates and routing numbers',
    detectors: [
      'card',
      'card_partial',
      'card_exp',
      'cvv',
      'iban',
      'account',
      'routing',
    ],
    model: [],
  },
  {
    id: 'credentials',
    label: 'Passwords and login details',
    detail: 'Labelled passwords, PINs and usernames',
    detectors: ['credential'],
    model: [],
  },
  {
    id: 'online',
    label: 'Web, device and vehicle identifiers',
    detail: 'URLs, IP addresses, serial numbers, VINs and license plates',
    detectors: ['url', 'ip', 'device', 'vin'],
    model: [],
  },
  {
    id: 'dates',
    label: 'Dates and ages over 89',
    detail: 'Birth dates and other calendar dates',
    detectors: ['dob', 'date', 'age90'],
    model: [],
  },
  {
    id: 'money',
    label: 'Money amounts',
    detail: 'Prices, balances and other financial amounts',
    detectors: ['money'],
    model: [],
  },
  {
    id: 'health',
    label: 'Health details',
    detail: 'Personal conditions, symptoms, medicines and treatments',
    detectors: ['sensitive_topics'],
    model: ['health'],
  },
  {
    id: 'sensitive',
    label: 'Other sensitive personal facts',
    detail:
      'Religion, ethnicity, politics, sexuality, immigration, legal and financial circumstances',
    detectors: ['sensitive_topics'],
    model: ['sensitive'],
  },
  {
    id: 'context',
    label: 'Indirect identity clues',
    detail:
      'Relationships, distinctive jobs or assets, biometrics and self-linked facts; may ask for review',
    detectors: ['sensitive_topics'],
    model: ['identifying', 'uncertain'],
  },
] as const;
/** The id of a paste category. */
export type PasteCategory = (typeof PASTE_CATEGORIES)[number]['id'];
/** Every category id, in display order. */
export const ALL_CATEGORIES: readonly PasteCategory[] = Object.freeze(
  PASTE_CATEGORIES.map(c => c.id),
);
/** The categories chosen by the settings page's common preset. */
export const COMMON_CATEGORIES: readonly PasteCategory[] = Object.freeze([
  'names',
  'contact',
  'places',
  'records',
  'payments',
  'credentials',
]);

/**
 * Old installations retain full coverage. Invalid storage never silently
 * disables it.
 */
export function normalizeCategories(value: unknown): readonly PasteCategory[] {
  if (!Array.isArray(value) || value.some(id => !ALL_CATEGORIES.includes(id))) {
    return ALL_CATEGORIES;
  }
  return Object.freeze(ALL_CATEGORIES.filter(id => value.includes(id)));
}
/** Returns whether every category is in `categories`. */
export function allCategoriesSelected(
  categories: readonly PasteCategory[],
): boolean {
  return ALL_CATEGORIES.every(id => categories.includes(id));
}
/**
 * Returns the ids of the rule detectors used by `categories`, without
 * duplicates.
 */
export function selectedDetectors(
  categories: readonly PasteCategory[],
): string[] {
  return [
    ...new Set(
      PASTE_CATEGORIES.filter(c => categories.includes(c.id)).flatMap(c => [
        ...c.detectors,
      ]),
    ),
  ];
}
/** Returns the on-device model kinds requested by `categories`. */
export function selectedModelKinds(
  categories: readonly PasteCategory[],
): string[] {
  return PASTE_CATEGORIES.filter(c => categories.includes(c.id)).flatMap(c => [
    ...c.model,
  ]);
}
/**
 * Returns whether a finding of `kind` falls within `categories`. `kind` may be
 * a model kind, a detector id or `other`, which is always watched.
 */
export function watchesKind(
  categories: readonly PasteCategory[],
  kind: string,
): boolean {
  if (kind === 'person' || kind === 'company') {
    return categories.includes('names');
  }
  if (kind === 'health' || kind === 'sensitive') {
    return categories.includes(kind);
  }
  // An overlap or disagreement among enabled checks still needs review.
  if (kind === 'other') return true;
  return selectedDetectors(categories).includes(kind);
}
