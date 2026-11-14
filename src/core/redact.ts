/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Find, replace and restore. Pure functions, no network, no
 * storage.
 *
 * The on-device model only supplies full names. Everything else is ordinary
 * code: structured patterns, short forms of names, matching across line breaks,
 * placeholder numbering, and putting the real values back into the answer.
 */

import {
  detectPatterns,
  detectorById,
  isRegion,
} from '../../taxonomy/taxonomy.js';
import {tableDetections} from './tables';
import {classifyDetections} from './classification';
import {identityCandidates} from '../../taxonomy/identity-patterns.js';
import {detectionView, viewOccurrences} from '../../taxonomy/normalize.js';

/**
 * How a detection was found: by a rule, word list or table heading ('pattern'),
 * as a name or place from the model or from name discovery ('model'), as
 * another written form of a known name ('short-form'), or marked by the user
 * ('manual').
 */
export type Source = 'pattern' | 'model' | 'short-form' | 'manual';

/**
 * A span of the text proposed for replacement, listed for the user to review.
 */
export interface Detection {
  id: string;
  start: number;
  end: number;
  text: string;
  /** Detector id from the taxonomy, or 'person' / 'company' / 'other'. */
  kind: string;
  label: string;
  /** Placeholder stem, for example PERSON or ACCOUNT. */
  base: string;
  /** Detections with the same entity share one placeholder. */
  entity: string;
  /** What is restored for this entity (the full name, or the matched text). */
  canonical: string;
  source: Source;
  /**
   * Replaced unless the user says otherwise. False for sensitive topics, which
   * are only flagged.
   */
  defaultOn: boolean;
  enabled: boolean;
  /**
   * Uncertain local evidence stays protected and requires attention before
   * sending.
   */
  reviewReason?: string;
}

/** Phrases the on-device model flagged, copied from the text. */
export interface Topics {
  places: string[];
  health: string[];
  sensitive: string[];
  /**
   * First names, nicknames and initials used on their own. Treated as extra
   * person names.
   */
  names: string[];
}
/** A Topics value with every list empty. */
export const NO_TOPICS: Topics = {
  places: [],
  health: [],
  sensitive: [],
  names: [],
};

import {GIVEN_NAMES} from './given-names';
import {sensitiveTerms, generalTopicQuestion} from './sensitive-terms';
import {COMMON_WORDS, GEOGRAPHY, isLargePlace} from './common-words';
import {
  collapse,
  definedTerms,
  discoverNames,
  key,
  nameCandidates,
  trailingSuffix,
  type Candidate,
  type Names,
  ORG_TAIL,
  ordinaryWordsOf,
  NOT_NAME_WORDS,
} from './names';

export {nameCandidates};
export type {Names};

// Words that often start a sentence right before a surname ("Call Okafor", "Per
// Whitfield").
const COMMON_OPENERS = new Set([
  'call',
  'per',
  'ask',
  'tell',
  'see',
  'email',
  'contact',
  'when',
  'then',
  'after',
  'before',
  'since',
  'if',
  'but',
  'and',
  'so',
  'both',
  'neither',
  'either',
  'only',
  'even',
  'also',
  'however',
  'meanwhile',
  'later',
  'today',
  'yesterday',
  'tomorrow',
]);
// The word that ends a street's name.
const STREET_NAME_END =
  /^(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Lane|Ln|Highway|Hwy|Parkway|Pkwy)\b\.?$|^(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Lane|Ln|Highway|Hwy|Parkway|Pkwy)\b/;
// Courts, government departments and makes of vehicle: named in many documents,
// identifying nobody.
const PUBLIC_BODY = new RegExp(
  '^(?:the )?(?:(?:united states|u\\.s\\.|us) .+|.*\\b(?:district|circuit|judicial district|eastern district|western district|northern district|southern district|middle district)$|' +
    '(?:u\\.s\\. |united states )?(?:district|circuit|supreme|bankruptcy|tax|immigration) court.*|department of (?:justice|labor|labour|revenue|state|the treasury|homeland security|health.*|motor vehicles|education|veterans affairs)|' +
    'equal employment opportunity commission|indian health service|executive office for immigration review|national insurance|national labor relations board|' +
    'ford|chevrolet|chevy|gmc|dodge|jeep|chrysler|buick|cadillac|lincoln|tesla|toyota|honda|nissan|subaru|mazda|lexus|acura|hyundai|kia|volkswagen|audi|bmw|mercedes(?:-benz)?|volvo|porsche|' +
    'freightliner|kenworth|peterbilt|mack|john deere|kubota|harley-davidson|yamaha|the subaru|the ford|the toyota|the honda)$',
  'i',
);
// Words for a party or a job. Before a surname they are a description, not a
// first name.
const ROLE_WORD =
  /^(?:defendants?|plaintiffs?|petitioners?|respondents?|appellants?|appellees?|claimants?|debtors?|creditors?|trustees?|executors?|grantors?|lessors?|lessees?|landlords?|tenants?|buyers?|sellers?|borrowers?|lenders?|employers?|employees?|taxpayers?|clients?|patients?|insureds?|decedents?|counsel|attorneys?|judges?|officers?|doctors?|nurses?|witness|witnesses|deponents?|affiants?|movants?)$/i;
// Words that come before a name without being part of it.
const GREETINGS = new Set([
  'dear',
  'hi',
  'hello',
  'hey',
  'thanks',
  'thank',
  'attn',
  'attention',
  'from',
  'to',
  'cc',
  'bcc',
  're',
  'with',
  'by',
  'for',
  'and',
  'or',
  'but',
  'that',
  'this',
  'when',
  'where',
  'while',
  'because',
  'if',
  'as',
  'of',
  'in',
  'on',
  'at',
  'told',
  'asked',
  'called',
  'emailed',
  'met',
  'saw',
  'paid',
  'copy',
  'copied',
  'sincerely',
  'regards',
  'best',
  'signed',
  'present',
  'absent',
  'not',
  'no',
  'yes',
  'per',
  'see',
  'contact',
  'call',
  'email',
  'ask',
  'tell',
]);
// Capitalized words that follow a first name without being that person's
// surname.
const NOT_SURNAME = new Set([
  'street',
  'avenue',
  'road',
  'drive',
  'lane',
  'court',
  'county',
  'city',
  'bank',
  'inc',
  'llc',
  'ltd',
  'corp',
  'co',
  'company',
  'trust',
  'estate',
  'family',
  'group',
  'law',
  'medical',
  'dental',
  'clinic',
  'hospital',
  'school',
  'church',
  'university',
  'college',
  'january',
  'february',
  'march',
  'april',
  'may',
  'june',
  'july',
  'august',
  'september',
  'october',
  'november',
  'december',
  'monday',
  'tuesday',
  'wednesday',
  'thursday',
  'friday',
  'saturday',
  'sunday',
  'said',
  'says',
  'was',
  'is',
  'has',
  'had',
  'will',
  'would',
  'and',
  'or',
  'the',
  'his',
  'her',
  'their',
  'called',
  'asked',
  'told',
  'signed',
  'agreed',
  'also',
  'then',
  'still',
  'only',
  'exhibit',
  'schedule',
  'form',
  'section',
  'page',
  'account',
  'ledger',
  'payroll',
  'services',
  'supply',
  'home',
  'house',
  'place',
  'hall',
  'center',
  'centre',
  'park',
  'lake',
  'river',
  'valley',
  'beach',
  'island',
  'springs',
  'heights',
  'falls',
  'creek',
]);
// Capitalized words that are not a given name when they come before a surname.
const NOT_GIVEN = new Set([
  'the',
  'a',
  'an',
  'mr',
  'mrs',
  'ms',
  'miss',
  'dr',
  'judge',
  'justice',
  'attorney',
  'defendant',
  'plaintiff',
  'petitioner',
  'respondent',
  'client',
  'patient',
  'witness',
  'officer',
  'detective',
  'professor',
  'senator',
  'estate',
  'trust',
  'family',
  'house',
  'team',
  'former',
  'late',
  'old',
  'young',
  'poor',
  'dear',
  'hon',
  'sir',
  'father',
  'sister',
  'brother',
  'mother',
  'aunt',
  'uncle',
  'cousin',
  'grandma',
  'grandpa',
  'nurse',
  'coach',
  'agent',
  'deponent',
  'claimant',
  'decedent',
  'debtor',
  'tenant',
  'landlord',
  'employee',
  'employer',
  'buyer',
  'seller',
  'borrower',
  'lender',
]);

// A table cell under a "Name" heading that is an organization, not a person.
const COMPANY_HINT =
  /&|\b(?:Inc|LLC|LLP|Ltd|Corp|Co|Company|Bank|Trust|Group|Partners|Associates|Services|Supply|Clinic|Hospital|University|School|Church|Foundation|Fund|Union|Agency|Department|Authority|Homes|Builders|Insurance|District|Society|Association|Holdings|Enterprises|Industries|Systems|Solutions|Logistics|Rentals|Pharmacy|Dental|Medical|Law)\b/;
// Software, payment services and public bodies: named in many documents,
// identifying nobody.
const WELL_KNOWN = new Set([
  'irs',
  'internal revenue service',
  'ssa',
  'social security administration',
  'medicare',
  'medicaid',
  'quickbooks',
  'zelle',
  'venmo',
  'paypal',
  'excel',
  'microsoft',
  'google',
  'zoom',
  'outlook',
  'gmail',
  'docusign',
  'dropbox',
  'visa',
  'mastercard',
  'amex',
  'american express',
  'discover',
  'fedex',
  'ups',
  'usps',
  'cra',
  'canada revenue agency',
  'hmrc',
  'dmv',
  'uscis',
  'eeoc',
  'osha',
  'sec',
  'fdic',
  'finra',
  'cms',
  'hhs',
  'dol',
  'doj',
  'fbi',
  'acas',
  'equifax',
  'experian',
  'transunion',
  'turbotax',
  'adp',
  'paychex',
  'gusto',
  'stripe',
  'square',
  'xero',
  'sage',
  'iban',
  'swift',
]);
// Defined terms that name a role, not a party. They are left as written.
const ROLE_TERMS = new Set([
  'plaintiff',
  'plaintiffs',
  'defendant',
  'defendants',
  'petitioner',
  'petitioners',
  'respondent',
  'respondents',
  'appellant',
  'appellee',
  'claimant',
  'employee',
  'employer',
  'landlord',
  'tenant',
  'lessor',
  'lessee',
  'buyer',
  'seller',
  'purchaser',
  'vendor',
  'supplier',
  'customer',
  'client',
  'lender',
  'borrower',
  'guarantor',
  'licensor',
  'licensee',
  'contractor',
  'consultant',
  'company',
  'firm',
  'parties',
  'party',
  'agreement',
  'lease',
  'contract',
  'premises',
  'property',
  'effective date',
  'separation date',
  'trustee',
  'executor',
  'grantor',
  'settlor',
  'beneficiary',
  'debtor',
  'creditor',
  'insured',
  'insurer',
  'patient',
  'provider',
]);

// Words the on-device model sometimes returns as a "sensitive topic" that are
// only labels.
const NOT_A_TOPIC = new Set([
  'ssn',
  'sin',
  'itin',
  'ein',
  'tin',
  'dob',
  'date of birth',
  'social security number',
  'social security',
  'ni number',
  'national insurance number',
  'mobile',
  'phone',
  'email',
  'address',
  'occupation',
  'age',
  'gender',
  'sex',
  'religion',
  'race',
  'ethnicity',
  'nationality',
  'citizenship',
  'immigration',
  'immigration status',
  'marital status',
  'background',
  'legal',
  'anonymous',
  'personnel',
  'payroll',
  'hospital',
  'clinic',
  'medicare',
  'medicaid',
  'insurance',
  'mastercard',
  'visa',
  'criminal history',
  'health',
  'medical',
  'medication',
  'medications',
  'diagnosis',
  'treatment',
  'leave',
  'trustee',
  'executor',
  'plaintiff',
  'defendant',
  'union',
  'politics',
  'political',
  'disability',
  'name',
  'names',
  'password',
  'pin',
  'account',
  'date',
  'signature',
  'confidential',
  'privileged',
  'personal',
  'private',
  'sensitive',
  'family',
  'employment',
  'employer',
  'employee',
  'income',
  'tax',
  'taxes',
]);

const escapeRe = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/**
 * Where an organization's name ends when capitalized words after a known name
 * complete it.
 */
function growOrg(text: string, end: number): number {
  let best = end;
  let pos = end;
  for (let i = 0; i < 5; i++) {
    const m =
      /^(?: (?:and|of|for)(?= \p{Lu}))? (\p{Lu}[\p{L}'’-]*|&(?= \p{Lu}))/u.exec(
        text.slice(pos, pos + 40),
      );
    if (!m) break;
    pos += m[0].length;
    // An abbreviated ending keeps its full stop: "& Escrow Co."
    if (ORG_TAIL.test(m[1])) {
      best =
        /^(?:Inc|Co|Corp|Ltd|Bros|Assn|Assoc|Dept|Mfg)$/.test(m[1]) &&
        text[pos] === '.'
          ? pos + 1
          : pos;
    }
  }
  // "Okafor-Bell Bookkeeping" + " & Tax" when a legal ending follows: "& Tax,
  // LLC"
  const amp =
    /^ & \p{Lu}[\p{L}'’-]*(?=,? (?:Inc|LLC|L\.L\.C|LLP|Ltd|Co|Corp|PLLC|P\.C|PC)\b)/u.exec(
      text.slice(best, best + 40),
    );
  if (amp) best += amp[0].length;
  // "... Assurance Company" + " of Canada", "... Law Clinic" + " of Puget
  // Sound"
  const tail = /(\p{Lu}[\p{L}'’-]*)$/u.exec(
    text.slice(Math.max(0, best - 30), best),
  );
  const ofPlace =
    tail && ORG_TAIL.test(tail[1])
      ? /^ of (?:the )?\p{Lu}[\p{L}'’-]+(?: \p{Lu}[\p{L}'’-]+)?/u.exec(
          text.slice(best, best + 40),
        )
      : null;
  if (ofPlace) best += ofPlace[0].length;
  return best;
}

/**
 * Finds every place `name` appears as whole words, treating any run of spaces
 * or line breaks as one space. Returns [start, end) pairs.
 */
export function findOccurrences(
  text: string,
  name: string,
): Array<[number, number]> {
  const tokens = collapse(name).split(' ').filter(Boolean);
  if (!tokens.length) return [];
  const re = new RegExp(
    `(?<![\\p{L}\\p{N}])${tokens.map(escapeRe).join('\\s+')}(?![\\p{L}\\p{N}])`,
    'gu',
  );
  return [...text.matchAll(re)].map(m => [m.index, m.index + m[0].length]);
}

const KIND_LABEL: Record<string, string> = {
  person: 'Person',
  company: 'Organization',
  other: 'Other detail',
};
const KIND_BASE: Record<string, string> = {
  person: 'PERSON',
  company: 'COMPANY',
  other: 'REDACTED',
};

/**
 * Build the list the user reviews. Patterns claim their text first (they are
 * exact), then names, longest first, so "Whitfield & Daughters Holdings Ltd."
 * wins over "Whitfield". Names the model returned that are not in the text are
 * dropped.
 */
export function buildDetections(
  text: string,
  detectorIds: string[],
  names: Names,
  manual: Array<{text: string; kind: string}> = [],
  flipped: ReadonlySet<string> = new Set(),
  topics: Topics = NO_TOPICS,
  topicScope: Readonly<{
    health: boolean;
    sensitive: boolean;
    identifying: boolean;
  }> = {health: true, sensitive: true, identifying: true},
): Detection[] {
  const out: Detection[] = [];
  const claimed: Array<[number, number]> = [];
  const free = (s: number, e: number) =>
    !claimed.some(([a, b]) => s < b && e > a);
  // `flipped` holds the detections the user has switched away from their
  // default.
  const push = (
    d: Omit<Detection, 'id' | 'enabled' | 'defaultOn'>,
    defaultOn = true,
  ) => {
    const id = `${d.start}-${d.end}`;
    claimed.push([d.start, d.end]);
    out.push({...d, id, defaultOn, enabled: defaultOn !== flipped.has(id)});
  };

  // Things the user marked by hand come first: their choice wins over
  // everything.
  for (const m of [...manual].sort((a, b) => b.text.length - a.text.length)) {
    for (const [s, e] of findOccurrences(text, m.text)) {
      if (!free(s, e)) continue;
      push({
        start: s,
        end: e,
        text: text.slice(s, e),
        kind: m.kind,
        label: KIND_LABEL[m.kind] || 'Other detail',
        base: KIND_BASE[m.kind] || 'REDACTED',
        entity: `${m.kind}:${key(m.text)}`,
        canonical: collapse(m.text),
        source: 'manual',
      });
    }
  }
  const pushPattern = (found: ReturnType<typeof detectPatterns>[number]) => {
    let m = found;
    if (!free(m.start, m.end)) return;
    // A country or continent is not a place smaller than a state.
    if (m.type === 'places' && isLargePlace(m.text)) return;
    // "York" inside "New York", "Jersey" inside "New Jersey": take the whole
    // name, so the cleaned text does not read "New [PLACE]".
    if (m.type === 'places') {
      const lead = /(\p{Lu}\p{Ll}+)[^\S\n]$/u.exec(
        text.slice(Math.max(0, m.start - 20), m.start),
      );
      if (lead && isRegion(`${lead[1]} ${m.text}`)) {
        const start = m.start - lead[0].length;
        if (free(start, m.end)) {
          m = {...m, start, text: text.slice(start, m.end)};
        }
      }
    }
    push({
      start: m.start,
      end: m.end,
      text: m.text,
      kind: m.type,
      label: detectorById(m.type)!.label,
      base: m.placeholder ?? 'REDACTED',
      entity: `${m.type}:${m.text.replace(/[\s-]/g, '').toLowerCase()}`,
      canonical: m.text,
      source: 'pattern',
      ...('reviewReason' in m && m.reviewReason
        ? {reviewReason: String(m.reviewReason)}
        : {}),
    });
  };
  // Values named by a table heading or a form label ("Check #", "Emp ID",
  // "Amount").
  const inTables = tableDetections(text, detectorIds);
  const tableNames: Names = {people: [], companies: []};
  for (const t of inTables) {
    if (t.type === 'names') {
      const flip = /^([^,]+),\s*(.+)$/.exec(t.text);
      if (COMPANY_HINT.test(t.text)) {
        tableNames.companies.push(t.text);
      } else {
        tableNames.people.push(
          flip && !/\s(?:Jr|Sr|II|III|IV)\.?$/.test(t.text)
            ? `${flip[2]} ${flip[1]}`
            : t.text,
        );
      }
      continue;
    }
    // placed after names, below
    if (t.type === 'places' || t.type === 'region') continue;
    const det = detectorById(t.type)!;
    pushPattern({
      ...t,
      label: det.label,
      placeholder: (det.placeholder ?? 'REDACTED').split(' ')[0],
    });
  }

  // The town written right after a street address, and the state code after
  // that: "1127 Vigo Street, Terre Haute IN.", "61 Larchmere Ln, Upper Darby PA
  // 19082", "1450 West 2100 South, Salt Lake City."
  if (detectorIds.includes('street') && detectorIds.includes('places')) {
    const placeDet = detectorById('places')!;
    const regionDet = detectorById('region')!;
    const streets = detectPatterns(text, ['street'], []);
    for (const st of streets) {
      // The whole town name is taken ("Salt Lake City", "Thunder Bay"); a state
      // code is never part of it.
      const m =
        /^,\s((?![A-Z]{2,3}\b)\p{Lu}[\p{L}'’.-]+(?: (?![A-Z]{2,3}\b)\p{Lu}[\p{L}'’.-]+){0,2})(?:,? ([A-Z]{2,3}))?(?=[.,;)]|\s+\d{4,5}\b|\s*\n|\s*$)/u.exec(
          text.slice(st.end, st.end + 60),
        );
      if (
        !m ||
        /^(?:Suite|Ste|Unit|Apt|Floor|Room|Bldg|Building|PO|P\.O\.|Attn|Phone|Tel|Fax|Email|The|And|But|He|She|They|We|It)$/.test(
          m[1].split(' ')[0],
        )
      ) {
        continue;
      }
      // a full stop that ends the sentence is not part of the town
      m[1] = m[1].replace(/\.$/, '');
      const cityStart = st.end + 2;
      const cityEnd = cityStart + m[1].length;
      if (isRegion(m[1])) continue;
      if (free(cityStart, cityEnd)) {
        push({
          start: cityStart,
          end: cityEnd,
          text: m[1],
          kind: 'places',
          label: placeDet.label,
          base: 'PLACE',
          entity: `places:${key(m[1]).replace(/\s/g, '')}`,
          canonical: m[1],
          source: 'pattern',
        });
      }
      if (m[2] && isRegion(m[2]) && detectorIds.includes('region')) {
        const rs = st.end + m[0].length - m[2].length;
        if (free(rs, rs + m[2].length)) {
          push({
            start: rs,
            end: rs + m[2].length,
            text: m[2],
            kind: 'region',
            label: regionDet.label,
            base: 'STATE',
            entity: `region:${m[2].toLowerCase()}`,
            canonical: m[2],
            source: 'pattern',
          });
        }
      }
    }
  }
  // Places are matched after names, so "Jordan Lee, MD" is a person, not a town
  // in Maryland.
  const LATE = ['places', 'region'];
  for (const m of detectPatterns(
    text,
    detectorIds.filter(id => !LATE.includes(id)),
    claimed,
  )) {
    pushPattern(m);
  }

  if (detectorIds.includes('names')) {
    // Names the model returned, plus names that can be read straight off the
    // page.
    const found = discoverNames(text);
    const all: Names = {
      // The second on-device request also returns first names and nicknames
      // used on their own.
      people: [
        ...new Set([
          ...names.people,
          ...found.people,
          ...tableNames.people,
          ...(topics.names ?? [])
            .map(collapse)
            .filter(
              n =>
                /^\p{Lu}/u.test(n) &&
                n.length >= 2 &&
                n.split(' ').length <= 3 &&
                !/\d/.test(n) &&
                !ROLE_TERMS.has(n.toLowerCase()),
            ),
        ]),
      ].filter(n => !ROLE_TERMS.has(key(n).replace(/^the /, ''))),
      // Software and public bodies the model sometimes returns are not client
      // identifiers.
      companies: [
        ...new Set([
          ...names.companies.filter(c => !WELL_KNOWN.has(key(c))),
          ...found.companies,
          ...tableNames.companies,
        ]),
      ].filter(n => !ROLE_TERMS.has(key(n).replace(/^the /, ''))),
    };
    const modelSaid = new Set([...names.people, ...names.companies].map(key));
    // Single surnames that came with a title ("Mr. Ferreira") are safe to treat
    // as surnames.
    const discoveredByTitle = new Set(
      found.people.filter(n => !n.includes(' ')),
    );
    // A city written before its state: "Salt Lake City, Utah 84106", "St.
    // Louis,\nMissouri". A person's name found inside one is part of the city's
    // name.
    const cities = detectPatterns(text, ['places'], []).filter(m => {
      const next = /^,\s+([A-Z][A-Za-z]+(?:\s[A-Z][a-z]+)?)(\s+\d{5}\b)?/.exec(
        text.slice(m.end, m.end + 40),
      );
      if (/\sCity$/.test(m.text) || /^\p{Lu}\p{Ll}+ \d{1,2}$/u.test(m.text)) {
        // "Ho Chi Minh City", "Dublin 8"
        return true;
      }
      if (!next || /^(?:Dr|Mr|Mrs|Ms|Prof|Hon|Judge|Attorney)\b/.test(m.text)) {
        return false;
      }
      const full = [next[1], next[1].split(' ')[0]].find(
        r => r.length > 2 && isRegion(r),
      );
      return (
        Boolean(full) || (isRegion(next[1].split(' ')[0]) && Boolean(next[2]))
      );
    });
    // A city of two or more words, once identified, is the same city wherever
    // it appears.
    for (const m of [...cities]) {
      if (!/\s/.test(m.text)) continue;
      for (const [a, b] of findOccurrences(text, m.text)) {
        if (cities.some(c => c.start === a && c.end === b)) continue;
        const again = {...m, start: a, end: b, text: text.slice(a, b)};
        cities.push(again);
        if (detectorIds.includes('places')) pushPattern(again);
      }
    }
    const insideCity = (s: number, e: number) =>
      cities.some(m => m.start <= s && e <= m.end && m.end - m.start > e - s);
    // "Carlton Street", "N. Zarzamora St", "Fanning Drive": a street, unless it
    // opens with a first name ("Tom Lane").
    const STREET_END =
      /^(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Highway|Hwy|Parkway|Pkwy)\b\.?/;
    const isStreet = (s: number, e: number) => {
      const name = text.slice(s, e);
      if (
        STREET_END.test(text.slice(e + 1, e + 12)) &&
        text[e] === ' ' &&
        !/^(?:Dr|St)\.?\s\p{Lu}/u.test(text.slice(e + 1, e + 8))
      ) {
        return true;
      }
      const words = name.split(' ');
      return (
        words.length === 2 &&
        STREET_END.test(words[1]) &&
        !/^(?:Dr|St)\.?$/.test(words[1]) &&
        !GIVEN_NAMES.has(words[0].toLowerCase())
      );
    };
    const place = (cands: Candidate[]) => {
      for (const c of [...cands].sort(
        (a, b) => b.text.length - a.text.length,
      )) {
        for (const [s0, e0] of findOccurrences(text, c.text)) {
          if (c.kind === 'person' && (insideCity(s0, e0) || isStreet(s0, e0))) {
            continue;
          }
          if (
            c.kind === 'person' &&
            !c.text.includes(' ') &&
            /\b(?:North|South|West|New) $/.test(
              text.slice(Math.max(0, s0 - 6), s0),
            ) &&
            isRegion(
              `${/(\w+) $/.exec(text.slice(Math.max(0, s0 - 6), s0))![1]} ${c.text}`,
            )
          ) {
            continue;
          }
          if (
            c.kind === 'company' &&
            !c.text.includes(' ') &&
            text[e0] === ' ' &&
            STREET_NAME_END.test(text.slice(e0 + 1, e0 + 12))
          ) {
            // "Zarzamora St"
            continue;
          }
          if (
            !c.text.includes(' ') &&
            /^ (?:County|Parish|Township|Borough|Lake|River|Creek|Island|Bay|Valley|Falls|Springs|Heights|Harbou?r|Beach)\b/.test(
              text.slice(e0, e0 + 10),
            )
          ) {
            // "Riley County"
            continue;
          }
          const plainEnd = trailingSuffix(text, e0, c.kind);
          let e = plainEnd;
          let s = s0;
          let kind = c.kind;
          // Words after a known name that complete an organization's name:
          // "Prairie State Blue Shield" + " PPO", "Cedar Glen" + " Memory
          // Care", "... Title" + " & Escrow Co."
          const grown = plainEnd === e0 ? growOrg(text, e0) : e0;
          if (grown > e0) {
            e = trailingSuffix(text, grown, 'company');
            kind = 'company';
          }
          // A numbered body: "Flint Hills Unified School District 383",
          // "Machinists Lodge 2211"
          const numbered =
            kind === 'company' &&
            /(?:District|Local|Lodge|Post|Chapter|Unit|Troop|Council|Station|Precinct|School)$/.test(
              text.slice(s0, e),
            )
              ? /^ (?:No\. ?|#)?\d{1,4}\b(?![.,/-]\d)/.exec(
                  text.slice(e, e + 12),
                )
              : null;
          if (numbered) e += numbered[0].length;
          // A family name that starts with a particle: "van der Berg Marine
          // Joinery"
          const particle =
            c.kind === 'company'
              ? /(?<!\p{L})(?:(?:van|von|der|den|de|del|della|du|ter|ten)\s)+$/u.exec(
                  text.slice(Math.max(0, s0 - 16), s0),
                )
              : null;
          if (particle) s = s0 - particle[0].length;
          // "St. Landry Parish Kingdom Hall": the saint's title belongs to the
          // name
          const saint =
            kind === 'company' && s === s0
              ? /(?<![\p{L}])(?:St|Ste|Mt|Ft)\. $/u.exec(
                  text.slice(Math.max(0, s0 - 5), s0),
                )
              : null;
          if (saint) s = s0 - saint[0].length;
          // A capitalized word right before an organization, in mid-sentence,
          // starts its name: "to Menomonee Valley Animal Rescue" when only
          // "Valley Animal Rescue" was found.
          const before =
            kind === 'company' && s === s0
              ? /(?<![.!?:;]\s|["“(])(?<=[\p{Ll},]\s+)(\p{Lu}\p{Ll}{3,}) $/u.exec(
                  text.slice(Math.max(0, s0 - 30), s0),
                )
              : null;
          if (
            before &&
            !COMMON_OPENERS.has(before[1].toLowerCase()) &&
            !GREETINGS.has(before[1].toLowerCase()) &&
            !NOT_GIVEN.has(before[1].toLowerCase()) &&
            !ROLE_WORD.test(before[1])
          ) {
            s = s0 - before[0].length;
          }
          // "Estate of Bernadette L. Kowalczyk" is a party in its own right.
          const estate =
            c.kind === 'person'
              ? /\b(?:Estate|ESTATE|Succession|SUCCESSION|Conservatorship|Guardianship) (?:of|OF) $/.exec(
                  text.slice(Math.max(0, s0 - 20), s0),
                )
              : null;
          if (estate) {
            s = s0 - estate[0].length;
            kind = 'company';
          }
          // "The Okafor Family Trust": the article is part of the name as
          // written. The same goes for a two-word name the model took for a
          // person: "The Wexley Riverside, 3 nights".
          const article =
            text.slice(s - 4, s) === 'The ' &&
            (kind === 'company' ||
              (c.text.includes(' ') &&
                /^(?:[,.;]|\s*$|\s*\n)/.test(text.slice(e, e + 3))));
          if (article) {
            s -= 4;
            kind = 'company';
          }
          if (!free(s, e)) {
            s = s0;
            e = plainEnd;
            kind = c.kind;
          }
          // the suffix belongs to something else: "Paulette Dzialo, RPR,
          // Certified Reporter"
          if (!free(s, e)) e = e0;
          if (!free(s, e)) continue;
          const changed = s !== s0 || e !== plainEnd;
          push({
            start: s,
            end: e,
            text: text.slice(s, e),
            kind,
            label: KIND_LABEL[kind],
            base: KIND_BASE[kind],
            entity:
              changed && c.kind === 'person'
                ? `company:${key(text.slice(s, e))}`
                : c.entity,
            canonical: changed ? collapse(text.slice(s, e)) : c.canonical,
            source:
              c.source === 'model' && !modelSaid.has(key(c.canonical))
                ? 'short-form'
                : c.source,
          });
        }
      }
    };
    // Family members: a capitalized word right before a surname we already know
    // ("Emeka Okafor" when "Ngozi Okafor" is known) is treated as another
    // person.
    const surnames = new Set(
      all.people
        .map(n =>
          collapse(n)
            .split(' ')
            .filter(t => !/^(?:Jr|Sr|II|III|IV|Esq)\.?,?$/.test(t)),
        )
        .filter(t => t.length > 1 || discoveredByTitle.has(t[0]))
        .map(t => t[t.length - 1])
        .filter(w => w && w.length >= 3 && /^\p{Lu}\p{Ll}/u.test(w)),
    );
    for (const sur of surnames) {
      // One or two capitalized words before the surname ("Trần Minh Khôi" when
      // "Khôi" is known).
      const re = new RegExp(
        `(?<![\\p{L}\\p{N}])((?:\\p{Lu}\\p{Ll}[\\p{L}'’-]+ )?\\p{Lu}\\p{Ll}[\\p{L}'’-]+) ${sur.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\p{L}\\p{N}])(?! (?!Jr|Sr|II|III|IV|Esq)\\p{Lu}\\p{Ll})`,
        'gu',
      );
      for (const m of text.matchAll(re)) {
        // "Defendants Stavros Precision Hydraulics": a role word in front of a
        // surname is not a first name.
        if (m[1].split(' ').some(w => ROLE_WORD.test(w))) continue;
        const lead = text.slice(Math.max(0, m.index - 2), m.index);
        const sentenceStart = m.index === 0 || /[.!?:]\s$|\n$/.test(lead);
        const lead1 = m[1].split(' ')[0].toLowerCase();
        if (
          !(sentenceStart && COMMON_OPENERS.has(lead1)) &&
          !NOT_GIVEN.has(lead1) &&
          !NOT_GIVEN.has(m[1].split(' ').pop()!.toLowerCase())
        ) {
          all.people.push(collapse(m[0]));
        }
      }
    }
    // A known first name followed by a capitalized word is that person's full
    // name ("Imani Okoro" when only "Imani" was known), unless the next word is
    // an ordinary one.
    const singles = new Set(
      all.people
        .map(collapse)
        .filter(
          n =>
            !n.includes(' ') &&
            n.length >= 3 &&
            /^\p{Lu}\p{Ll}/u.test(n) &&
            !/^(?:Mr|Mrs|Ms|Miss|Mx|Dr|Prof|Hon|Sir|Judge)\.?$/.test(n),
        ),
    );
    for (const given of singles) {
      const re = new RegExp(
        `(?<![\\p{L}\\p{N}'’-])${given.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')} ((?:[A-Z]\\. )?(?:Mc|Mac|O['’]|Al-|De |Van |Von )?\\p{Lu}\\p{Ll}[\\p{L}'’-]+)(?![\\p{L}\\p{N}])`,
        'gu',
      );
      for (const m of text.matchAll(re)) {
        const next = m[1].split(' ').pop()!.toLowerCase();
        if (!NOT_GIVEN.has(next) && !NOT_SURNAME.has(next)) {
          all.people.push(collapse(m[0]));
        }
      }
    }
    // Surname first, in a form or a table, when only the first name is known:
    // "Petrosyan, Nikolai".
    const extraLinks: Array<{text: string; person: string}> = [];
    for (const given of singles) {
      const re = new RegExp(
        `(?<=^|\\n|\\t|\\s{2}|:\\s)(\\p{Lu}[\\p{L}'’-]+(?: (?:(?:de|da|del|van|von|der|la|di) )?\\p{Lu}[\\p{L}'’-]+){0,2}), ${given.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\p{L}\\p{N}'’-])`,
        'gu',
      );
      for (const m of text.matchAll(re)) {
        if (GREETINGS.has(m[1].split(' ')[0].toLowerCase())) continue;
        all.people.push(`${given} ${m[1]}`);
        extraLinks.push({text: m[0], person: `${given} ${m[1]}`});
      }
    }
    // A single known name is often a surname. A capitalized word or an initial
    // right before it makes a full name: "Cormac Brennan" and "É. Beaulieu"
    // when "Brennan" and "Beaulieu" are known.
    for (const sur of new Set([...singles, ...surnames])) {
      const esc = sur.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      for (const m of text.matchAll(
        new RegExp(
          `(?<![\\p{L}\\p{N}.])(?<!\\d\\s)(?<!\\p{Lu}[\\p{L}\\p{M}'’-]+\\s)\\p{Lu}\\p{M}*\\.(?:\\s?\\p{Lu}\\p{M}*\\.)?\\s${esc}(?![\\p{L}\\p{N}])`,
          'gu',
        ),
      )) {
        all.people.push(collapse(m[0]));
      }
      if (!singles.has(sur)) continue;
      for (const m of text.matchAll(
        new RegExp(
          `(?<![\\p{L}\\p{N}'’-])(\\p{Lu}\\p{Ll}[\\p{L}'’-]+) ${esc}(?![\\p{L}\\p{N}])`,
          'gu',
        ),
      )) {
        const w = m[1].toLowerCase();
        if (
          !COMMON_OPENERS.has(w) &&
          !NOT_GIVEN.has(w) &&
          !GREETINGS.has(w) &&
          !ROLE_WORD.test(w)
        ) {
          all.people.push(collapse(m[0]));
        }
      }
    }
    // A line that holds nothing but an initial and a word from a known name is
    // that person or a relative: a signature or a "cc" line such as "É.
    // Beaulieu".
    for (const word of new Set(
      all.people
        .flatMap(n => collapse(n).split(' '))
        .filter(w => w.length >= 4 && /^\p{Lu}\p{Ll}+$/u.test(w)),
    )) {
      for (const m of text.matchAll(
        new RegExp(
          `(?:^|\\n)[^\\S\\n]*(\\p{Lu}\\p{M}*\\.\\s${word})[^\\S\\n]*(?=\\n|$)`,
          'gu',
        ),
      )) {
        all.people.push(collapse(m[1]));
      }
    }
    // "Fanning Drive", "Tieton Drive": a street, unless it opens with a first
    // name ("Tom Lane"). Left in as a person, "Drive" alone would be replaced
    // wherever it appears.
    all.people = all.people.filter(n => {
      const w = collapse(n).split(' ');
      return !(
        w.length === 2 &&
        STREET_NAME_END.test(w[1]) &&
        !GIVEN_NAMES.has(w[0].toLowerCase())
      );
    });
    // A "name" made only of words this document also uses in lower case, or of
    // job titles and heading words, is a heading or a description: "Regular
    // Meeting", "family doctor", "Exhibit".
    {
      const here = ordinaryWordsOf(text);
      const plain = (w: string) => {
        const k = w.replace(/[^\p{L}]/gu, '').toLocaleLowerCase('en-US');
        // Everyday words and large places the model sometimes calls a person:
        // "America", "Past Weekend".
        return (
          here.has(k) ||
          NOT_NAME_WORDS.has(k) ||
          COMMON_WORDS.has(k) ||
          GEOGRAPHY.has(k)
        );
      };
      const said = new Set(names.people.map(n => collapse(n)));
      all.people = all.people.filter(n => {
        const name = collapse(n);
        // lower case: one word only (typist initials, a sign-off)
        if (!/\p{Lu}/u.test(name)) return !name.includes(' ');
        if (
          /^(?:[IVX]{2,5}|PP|IRC|USC|CFR|R\.S\.|DNR|POLST|SUV|VIN|ADA|ADEA|FMLA|HIPAA|ERISA|OSHA|LLC|EIN)$/.test(
            name,
          )
        ) {
          return false;
        }
        const words = name
          .replace(/,/g, ' ')
          .split(/\s+/)
          .filter(w => w.replace(/[^\p{L}]/gu, '').length >= 3);
        if (!words.length) return true; // initials
        if (words.length === 1) {
          return (
            !plain(words[0]) ||
            said.has(name) ||
            (GIVEN_NAMES.has(words[0].toLowerCase()) &&
              !NOT_NAME_WORDS.has(words[0].toLowerCase()))
          );
        }
        return !words.every(plain);
      });
    }
    all.people = [...new Set(all.people)];
    // A name the model misspelled ("Marisola Lopez" for Marisela Lopez) is
    // nowhere on the page. Left in, it would look like a second person with the
    // same surname, and "Lopez" alone would then belong to nobody. Drop it when
    // a correctly spelled name shares one of its words.
    const lowered = text.toLocaleLowerCase('en-US');
    const onPage = (w: string) =>
      lowered.includes(w.toLocaleLowerCase('en-US'));
    const wordsOf = (n: string) =>
      collapse(n)
        .split(/[\s,]+/)
        .filter(w => w.replace(/\./g, '').length >= 3);
    all.people = all.people.filter(n => {
      const words = wordsOf(n);
      if (words.length < 2 || words.every(onPage)) return true;
      const here = new Set(words.filter(onPage).map(key));
      return !all.people.some(
        o =>
          o !== n &&
          wordsOf(o).length >= 2 &&
          wordsOf(o).every(onPage) &&
          wordsOf(o).some(w => here.has(key(w))),
      );
    });
    // Organization names from the model that are not names: a legal ending on
    // its own ("LLC"), a bare run of capitals that is no known organization's
    // initials ("PNC" for potential new client), a phrase in lower case ("trust
    // company"), a public body, a make of car.
    const ordinary = ordinaryWordsOf(text);
    const capsOf = (n: string) =>
      n
        .split(/[\s-]+/)
        .filter(
          w =>
            /^\p{Lu}/u.test(w) &&
            !/^(?:Inc|LLC|LLP|Ltd|Co|Corp|PLLC)\.?,?$/.test(w),
        )
        .map(w => w[0])
        .join('');
    const defined = new Set(definedTerms(text).map(d => d.term));
    all.companies = all.companies.filter(c => {
      const name = collapse(c);
      if (
        PUBLIC_BODY.test(name) ||
        WELL_KNOWN.has(key(name)) ||
        /^(?:Inc|LLC|LLP|Ltd|Co|Corp|PLLC|EIN|SSN|ABA|CPT|ICD|DOB|POA|TBD|N\/A)\.?$/i.test(
          name,
        )
      ) {
        return false;
      }
      if (/^[A-Z&]{2,5}$/.test(name)) {
        const letters = name.replace(/&/g, '');
        return (
          defined.has(name) ||
          all.companies.some(
            o =>
              o !== c &&
              capsOf(collapse(o)).startsWith(letters) &&
              letters.length >= 2 &&
              collapse(o).includes(' '),
          )
        );
      }
      // A phrase with no capital after its first letter ("trust company",
      // "Petty cash") is a name only if one of its words is used as a name
      // elsewhere: capitalized in mid-sentence, or inside a login or address.
      const words = name.split(' ');
      if (words.length >= 2 && !words.slice(1).some(w => /^\p{Lu}/u.test(w))) {
        if (/['’]s\b/.test(name)) return false;
        return words.some(w => {
          const k = w.toLowerCase().replace(/[^a-z]/g, '');
          if (
            k.length < 5 ||
            ORG_TAIL.test(k[0].toUpperCase() + k.slice(1)) ||
            /^(?:account|health|credit|checking|savings|petty|state|supplier|payments?|company|design)$/.test(
              k,
            )
          ) {
            return false;
          }
          const cap = k[0].toUpperCase() + k.slice(1);
          return new RegExp(
            `(?<=[\\p{Ll},;:] )${cap}(?![\\p{L}])|[a-z0-9.]*${k}[a-z0-9]*[@._][a-z0-9]`,
            'u',
          ).test(text);
        });
      }
      if (!/\p{Lu}/u.test(name)) return false;
      return true;
    });
    const candidates = nameCandidates(all, ordinary);
    // Forms that cannot be derived, such as "RUNNING BEAR, WENDELL K.", linked
    // to their person.
    for (const link of [...(found.links ?? []), ...extraLinks]) {
      const owner = candidates.find(
        c => c.kind === 'person' && c.text === collapse(link.person),
      );
      if (owner) {
        candidates.push({...owner, text: link.text, source: 'short-form'});
      }
    }
    place(candidates);

    // Initials of a person already found, in the spots where only initials
    // would stand: alone in brackets "(MO)", before a colon at the start of a
    // line "LA:", or alone in a table cell. There a two-letter state code is
    // somebody's initials too, so the usual stoplist is not used.
    const known = out.filter(
      d => d.kind === 'person' && d.canonical.includes(' '),
    );
    const initialsOf = new Map<string, Detection | null>();
    for (const d of known) {
      const w = d.canonical
        .replace(/,/g, '')
        .split(' ')
        .filter(
          t =>
            /^\p{Lu}/u.test(t) &&
            !/^(?:Mr|Mrs|Ms|Mx|Dr|Prof|Jr|Sr|II|III|IV|Esq)\.?$/.test(t),
        );
      if (w.length < 2) continue;
      const first = w[0];
      const last = w[w.length - 1];
      const forms = new Set([first[0] + last[0], w.map(t => t[0]).join('')]);
      const double = /^(\p{Lu})\p{L}*-(\p{Lu})/u.exec(first);
      if (double) {
        forms.add(`${double[1]}-${double[2]}`);
        forms.add(double[1] + double[2] + last[0]);
      }
      const apostrophe = /^(\p{Lu})['’](\p{Lu})/u.exec(last);
      if (apostrophe) forms.add(first[0] + apostrophe[1] + apostrophe[2]);
      for (const f of forms) {
        initialsOf.set(
          f,
          initialsOf.has(f) && initialsOf.get(f)?.entity !== d.entity
            ? null
            : d,
        );
      }
    }
    for (const [ini, d] of initialsOf) {
      if (!d) continue; // two people share these initials
      const esc = ini.replace(/-/g, '\\-');
      // ... and at the end of a note ("... visa ends.   FY", "- MT"), after a
      // sign-off word, or after "Prepared"
      for (const m of text.matchAll(
        new RegExp(
          `(?<=\\()${esc}(?=\\))|(?<=^|\\n)${esc}(?=:\\s)|(?<=\\t)${esc}(?=\\t|\\n|$)|(?<=[.!?]\\s+(?:[-–—]\\s)?)${esc}(?=\\s*(?:\\n|$))|(?<=\\b(?:[Cc]heers|[Tt]hanks|[Rr]egards|[Bb]est|[Pp]repared|[Rr]eviewed|[Dd]rafted),?\\s(?:by\\s)?)${esc}(?=[,.\\s]|$)`,
          'g',
        ),
      )) {
        if (free(m.index, m.index + ini.length)) {
          push({
            start: m.index,
            end: m.index + ini.length,
            text: ini,
            kind: 'person',
            label: KIND_LABEL.person,
            base: KIND_BASE.person,
            entity: d.entity,
            canonical: d.canonical,
            source: 'short-form',
          });
        }
      }
    }
    // User names made from the name of a person already found: "tboone" for T.
    // Boone, "khoitran_sj" for Khoi Tran. A plain one needs a word nearby that
    // says it is an account; one with a digit or a symbol does not.
    if (detectorIds.includes('credential')) {
      const plain = (w: string) =>
        w
          .normalize('NFD')
          .toLowerCase()
          .replace(/[^a-z]/g, '');
      const stems = new Set<string>();
      for (const d of known) {
        const w = d.canonical
          .replace(/[,.]/g, ' ')
          .split(/\s+/)
          .filter(
            t =>
              /^\p{Lu}/u.test(t) &&
              !/^(?:Mr|Mrs|Ms|Mx|Dr|Prof|Jr|Sr|II|III|IV|Esq)$/.test(t),
          );
        if (w.length < 2) continue;
        const first = plain(w[0]);
        const last = plain(w[w.length - 1]);
        if (last.length < 3 || !first) continue;
        for (const stem of [
          first[0] + last,
          first + last,
          last + first[0],
          last + first,
        ]) {
          if (stem.length >= 5) stems.add(stem);
        }
      }
      const cred = detectorById('credential')!;
      for (const m of text.matchAll(
        /(?<![\w@./\\-])[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*(?![\w@-]|\.[a-z])/g,
      )) {
        const token = m[0];
        if (
          token.length < 5 ||
          token.length > 32 ||
          !free(m.index, m.index + token.length)
        ) {
          continue;
        }
        const letters = token.replace(/[^a-z]/g, '');
        if (![...stems].some(stem => letters.startsWith(stem))) continue;
        const cue =
          /\b(?:user|login|log-in|account|signed in|logged in|portal|vpn|platform|admin|sso|credentials?)\b[^\n]{0,40}$|[(`]$/i.test(
            text.slice(Math.max(0, m.index - 48), m.index),
          );
        if (!cue && !/[\d._-]/.test(token)) continue;
        push({
          start: m.index,
          end: m.index + token.length,
          text: token,
          kind: 'credential',
          label: cred.label,
          base: 'CREDENTIAL',
          entity: `credential:${token}`,
          canonical: token,
          source: 'short-form',
        });
      }
    }
    // A message signed with one letter: a line that holds only "M." when someone's name starts with M.
    for (const m of text.matchAll(
      /(?<=\n(?:>[^\S\n]?)*[^\S\n]*)\p{Lu}\.(?=[^\S\n]*(?:\n|$))/gu,
    )) {
      const owners = [
        ...new Map(
          out
            .filter(d => d.kind === 'person' && d.canonical.startsWith(m[0][0]))
            .map(d => [d.entity, d]),
        ).values(),
      ];
      if (!owners.length || !free(m.index, m.index + 2)) continue;
      const one = owners.length === 1 ? owners[0] : null;
      push({
        start: m.index,
        end: m.index + 2,
        text: m[0],
        kind: 'person',
        label: KIND_LABEL.person,
        base: KIND_BASE.person,
        entity: one ? one.entity : `person:initial:${m[0][0]}`,
        canonical: one ? one.canonical : m[0],
        source: 'short-form',
      });
    }

    // Short names the document itself defines: Brightwater Biologics, Inc. ("Brightwater").
    // Each is linked to the closest name before it.
    const named = out.filter(d => d.kind === 'person' || d.kind === 'company');
    const aliases: Candidate[] = [];
    for (const {term, at} of definedTerms(text)) {
      // The name must come right before the bracket, in the same sentence, and the words in
      // between must not already contain the term (as in: this Lease (the "Lease")).
      const owner = named
        .filter(d => d.end <= at && at - d.end <= 70)
        .sort((a, b) => b.end - a.end)[0];
      if (!owner) continue;
      const between = text.slice(owner.end, at);
      const bare = term.replace(/^the\s+/i, '');
      if (
        /[.;!?]\s/.test(between) ||
        between.toLowerCase().includes(bare.toLowerCase())
      ) {
        continue;
      }
      // A role word such as "Plaintiff" or "the Company" says nothing about who the party is.
      if (ROLE_TERMS.has(bare.toLowerCase())) continue;
      // A run of capitals in brackets is a short name only if it is the owner's initials:
      // "(BFS)" after Brightwater Freight Systems, not "(SUMF)" after a party named in a heading.
      if (/^[A-Z&]{2,7}$/.test(bare)) {
        const initials = owner.canonical
          .split(/[\s-]+/)
          .filter(w => /^\p{Lu}/u.test(w))
          .map(w => w[0])
          .join('');
        let at2 = 0;
        const fits = [...bare.replace(/&/g, '')].every(ch => {
          at2 = initials.indexOf(ch, at2) + 1;
          return at2 > 0;
        });
        if (!fits) continue;
      }
      const forms = [
        term,
        ...(/^the\s/i.test(term) ? [] : [`the ${term}`, `The ${term}`]),
      ];
      for (const t of forms) {
        aliases.push({
          text: t,
          kind: owner.kind as 'person' | 'company',
          entity: owner.entity,
          canonical: owner.canonical,
          source: 'short-form',
        });
      }
    }
    place(aliases);
  }
  if (detectorIds.includes('places')) {
    for (const t of inTables.filter(x => x.type === 'places')) {
      pushPattern({
        ...t,
        label: detectorById('places')!.label,
        placeholder: 'PLACE',
      });
    }
    // Written forms first, so "Boulder County" is taken whole before the model's "Boulder".
    for (const m of detectPatterns(text, ['places'], claimed)) pushPattern(m);
    // Places the on-device model named, wherever they appear. A state is left to the state check,
    // which only runs when a selected rule covers states.
    const view = detectionView(text);
    for (const name of [...new Set(topics.places.map(collapse))].sort(
      (a, b) => b.length - a.length,
    )) {
      if (!/\p{L}/u.test(name) || isRegion(name) || isLargePlace(name)) {
        continue;
      }
      for (const [s, e] of viewOccurrences(view, name)) {
        // "Chesapeake" + " Senior Meals": the place is the start of an organization's name.
        const grown = growOrg(text, e);
        if (grown > e && free(s, grown)) {
          push({
            start: s,
            end: grown,
            text: text.slice(s, grown),
            kind: 'company',
            label: KIND_LABEL.company,
            base: KIND_BASE.company,
            entity: `company:${key(text.slice(s, grown))}`,
            canonical: collapse(text.slice(s, grown)),
            source: 'short-form',
          });
          continue;
        }
        if (free(s, e)) {
          push({
            start: s,
            end: e,
            text: text.slice(s, e),
            kind: 'places',
            label: detectorById('places')!.label,
            base: 'PLACE',
            entity: `place:${key(name)}`,
            canonical: name,
            source: 'model',
          });
        }
      }
    }
  }
  if (detectorIds.includes('region')) {
    for (const t of inTables.filter(x => x.type === 'region')) {
      pushPattern({
        ...t,
        label: detectorById('region')!.label,
        placeholder: 'STATE',
      });
    }
  }
  for (const m of detectPatterns(
    text,
    detectorIds.filter(id => LATE.includes(id)),
    claimed,
  )) {
    pushPattern(m);
  }

  // Sensitive topics: flagged, not replaced, because the question may depend on the fact itself.
  if (detectorIds.includes('sensitive_topics')) {
    const groups: Array<[string[], string, string, string]> = [
      [topics.health, 'health', 'Health detail', 'HEALTH_DETAIL'],
      [
        topics.sensitive,
        'sensitive',
        'Sensitive personal detail',
        'SENSITIVE_DETAIL',
      ],
    ];
    for (const [phrases, kind, label, base] of groups) {
      if (!topicScope[kind as 'health' | 'sensitive']) continue;
      for (const phrase of [...new Set(phrases.map(collapse))].sort(
        (a, b) => b.length - a.length,
      )) {
        // Field labels and role words are not sensitive facts, whatever the model says.
        if (
          phrase.length < 3 ||
          phrase.length > 160 ||
          NOT_A_TOPIC.has(phrase.toLowerCase()) ||
          ROLE_TERMS.has(phrase.toLowerCase())
        ) {
          continue;
        }
        for (const [s, e] of findOccurrences(text, phrase)) {
          if (generalTopicQuestion(text, s, e)) continue;
          if (free(s, e)) {
            push(
              {
                start: s,
                end: e,
                text: text.slice(s, e),
                kind,
                label,
                base,
                entity: `${kind}:${key(phrase)}`,
                canonical: collapse(phrase),
                source: 'model',
              },
              false,
            );
          }
        }
      }
    }
    // Words from a fixed list that point to a sensitive fact (see sensitive-terms.ts). Flagged, never replaced by default.
    for (const t of sensitiveTerms(text)) {
      if (!topicScope[t.topic === 'identifying' ? 'identifying' : t.kind]) {
        continue;
      }
      if (!free(t.start, t.end)) continue;
      const word = text.slice(t.start, t.end);
      push(
        {
          start: t.start,
          end: t.end,
          text: word,
          kind: t.kind,
          label: t.label,
          base: t.kind === 'health' ? 'HEALTH_DETAIL' : 'SENSITIVE_DETAIL',
          entity: `${t.kind}:${key(word)}`,
          canonical: collapse(word),
          source: 'pattern',
          ...(t.topic === 'identifying'
            ? {
                reviewReason:
                  'This description may identify someone indirectly.',
              }
            : {}),
        },
        false,
      );
    }
  }
  // A table cell, name, or smaller pattern must never cut a complete identifier in half.
  // Preserve the union in original coordinates; a category disagreement cannot uncover text.
  let complete = out;
  for (const m of identityCandidates(text, detectorIds)) {
    const overlaps = complete.filter(d => d.start < m.end && d.end > m.start);
    const covering = overlaps.find(d => d.start <= m.start && d.end >= m.end);
    if (
      covering &&
      (covering.start !== m.start ||
        covering.end !== m.end ||
        covering.source === 'manual' ||
        (m.type === 'places' && ['person', 'company'].includes(covering.kind)))
    ) {
      continue;
    }
    const start = Math.min(m.start, ...overlaps.map(d => d.start));
    const end = Math.max(m.end, ...overlaps.map(d => d.end));
    const value = text.slice(start, end);
    const id = `${start}-${end}`;
    const conflict =
      overlaps.some(d => d.source === 'manual') ||
      start !== m.start ||
      end !== m.end;
    const kind = conflict ? 'other' : m.type;
    const det = detectorById(m.type)!;
    complete = complete.filter(d => !overlaps.includes(d));
    complete.push({
      id,
      start,
      end,
      text: value,
      kind,
      label: conflict ? 'Detail to review' : det.label,
      base: conflict ? 'REDACTED' : det.placeholder!,
      entity: `${kind}:${key(value)}`,
      canonical: value,
      source: 'pattern',
      defaultOn: true,
      enabled: !flipped.has(id),
      reviewReason:
        overlaps.find(d => d.reviewReason)?.reviewReason ??
        (conflict
          ? 'The checks disagree about the extent of this detail.'
          : m.reviewReason),
    });
  }
  return classifyDetections(text, complete, topics).sort(
    (a, b) => a.start - b.start,
  );
}

/** The result of replacing detections with placeholders. */
export interface Redaction {
  /** The text with a placeholder in place of each enabled detection. */
  cleaned: string;
  /** placeholder (without brackets) -> real value. Kept in memory only. */
  map: Map<string, string>;
  /** detection id -> placeholder, for display. */
  placeholders: Map<string, string>;
}

/**
 * Swap every enabled detection for a numbered placeholder such as
 * [PERSON_1].
 */
export function applyRedactions(
  text: string,
  detections: Detection[],
): Redaction {
  const active = detections
    .filter(d => d.enabled)
    .sort((a, b) => a.start - b.start);
  const byEntity = new Map<string, string>();
  const counters = new Map<string, number>();
  const map = new Map<string, string>();
  const placeholders = new Map<string, string>();
  let cleaned = '';
  let at = 0;
  for (const d of active) {
    if (d.start < at) continue;
    let ph = byEntity.get(d.entity);
    if (!ph) {
      const n = (counters.get(d.base) || 0) + 1;
      counters.set(d.base, n);
      ph = `${d.base}_${n}`;
      byEntity.set(d.entity, ph);
      map.set(ph, d.canonical);
    }
    placeholders.set(d.id, ph);
    cleaned += text.slice(at, d.start) + `[${ph}]`;
    at = d.end;
  }
  return {cleaned: cleaned + text.slice(at), map, placeholders};
}

/**
 * Put the real values back into the cloud model's answer. Unknown
 * placeholders are left as they are.
 */
export function restore(
  answer: string,
  map: ReadonlyMap<string, string>,
): string {
  return answer.replace(
    /\[\s*([A-Z][A-Z_]*_\d+)\s*\]/g,
    (whole, ph: string) => map.get(ph) ?? whole,
  );
}

/**
 * Split text into pieces of roughly `maxWords`, breaking at paragraph
 * boundaries where possible.
 */
export function chunkText(
  text: string,
  maxWords = 350,
): Array<{start: number; end: number}> {
  // Units are paragraphs. A paragraph over the limit (a spreadsheet sheet or a PDF page
  // with no blank lines) is split at line breaks, and a single over-long line at words,
  // so no piece exceeds the on-device model's input budget.
  const units: Array<{start: number; end: number; words: number}> = [];
  const count = (s: string) => (s.match(/\S+/g) || []).length;
  const words = (from: number, to: number) => {
    let piece = -1;
    let n = 0;
    let last = from;
    for (const w of text.slice(from, to).matchAll(/\S+/g)) {
      const at = from + w.index!;
      if (piece < 0) piece = at;
      if (n === maxWords) {
        units.push({start: piece, end: last, words: n});
        piece = at;
        n = 0;
      }
      n++;
      last = at + w[0].length;
    }
    if (piece >= 0) units.push({start: piece, end: last, words: n});
  };
  for (const p of text.matchAll(/[^\n]+(?:\n(?!\s*\n)[^\n]+)*/g)) {
    const w = count(p[0]);
    if (w <= maxWords) {
      units.push({start: p.index!, end: p.index! + p[0].length, words: w});
      continue;
    }
    for (const line of p[0].matchAll(/[^\n]+/g)) {
      const from = p.index! + line.index!;
      const to = from + line[0].length;
      const lw = count(line[0]);
      if (lw <= maxWords) {
        if (lw) units.push({start: from, end: to, words: lw});
      } else {
        words(from, to);
      }
    }
  }
  const chunks: Array<{start: number; end: number}> = [];
  let start = -1;
  let end = 0;
  let total = 0;
  const flush = () => {
    if (start >= 0) chunks.push({start, end});
    start = -1;
    total = 0;
  };
  for (const u of units) {
    if (start >= 0 && total + u.words > maxWords) flush();
    if (start < 0) start = u.start;
    end = u.end;
    total += u.words;
  }
  flush();
  return chunks;
}

/**
 * Capitalized words that nothing has explained. Shown as "worth a look",
 * never auto-redacted.
 */
export function unexplainedCapitals(
  text: string,
  detections: Detection[],
): string[] {
  const covered = (i: number) =>
    detections.some(d => i >= d.start && i < d.end);
  const seen = new Set<string>();
  const out: string[] = [];
  for (const m of text.matchAll(
    /(?<![.!?:]\s|^|\n\s*)\b\p{Lu}\p{Ll}{2,}(?:\s+\p{Lu}\p{Ll}{2,})*\b/gu,
  )) {
    if (covered(m.index)) continue;
    const k = key(m[0]);
    if (seen.has(k) || STOP_CAPS.has(k)) continue;
    // A phrase made only of everyday words or large place names ("Next Week",
    // "New Year", "South America") is not worth a second look.
    if (
      k
        .split(' ')
        .every(
          w => COMMON_WORDS.has(w) || GEOGRAPHY.has(w) || NOT_NAME_WORDS.has(w),
        )
    ) {
      continue;
    }
    seen.add(k);
    out.push(m[0]);
  }
  return out;
}
const STOP_CAPS = new Set([
  'january',
  'february',
  'march',
  'april',
  'may',
  'june',
  'july',
  'august',
  'september',
  'october',
  'november',
  'december',
  'monday',
  'tuesday',
  'wednesday',
  'thursday',
  'friday',
  'saturday',
  'sunday',
]);
