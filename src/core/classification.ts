/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Resolve conflicting labels after detection. This pass never
 * removes a match, shrinks a span, or changes whether it is replaced. Uncertain
 * text stays protected for review.
 */

import {
  detectPatterns,
  detectorById,
  isRegion,
} from '../../taxonomy/taxonomy.js';
import {collapse, definedTerms, key, nameCandidates, ORG_TAIL} from './names';
import {GIVEN_NAMES} from './given-names';
import {sensitiveTerms} from './sensitive-terms';
import {tableDetections} from './tables';
import type {Detection, Topics} from './redact';

const ORGANIZATION_END =
  /\b(?:Inc|Incorporated|LLC|LLP|Ltd|Limited|Corp|Corporation|Company|Co|PLC|GmbH|Foundation|Hospital|Clinic|University|College|School|Bank|Credit Union|Associates|Partners|Insurance|Pharmacy|Laboratories|Center|Centre|Institute)\.?$/i;
// Complete labels only. A heading followed by a real name must keep the name's
// label.
const ROLE_OR_LABEL =
  /^(?:(?:(?:primary|secondary|joint|co)[ -]+)?(?:applicant|patient|policyholder|subscriber|beneficiary)|case\s+worker|(?:state\s+)?driver['’]?s?\s+licen[cs]e|attestation\s*(?:&|and)\s*digital\s+signatures?)$/i;
const isLabel = (s: string) => ROLE_OR_LABEL.test(collapse(s));
const CLINICAL_END =
  /\b(?:asthma|diabetes(?:\s+mellitus)?|hypertension|disease|disorder|syndrome|infection|fracture|[a-z]{4,}(?:itis|osis|[ae]mia|plegia|opathy))$/i;
const MEDICAL_SERVICE =
  /^(?:(?:inpatient|outpatient)\s+)?(?:room\s*(?:&|and)\s*board|diagnostic\s+imaging|(?:ct\s+)?angiogram(?:\s*(?:&|and)\s*lumbar\s+mri)?|laboratory\s*(?:&|and)\s*hematology\s+services|pharmacy\s*(?:&|and)\s*iv\s+infusions)$/i;
const BILLING_LABEL =
  /^(?:contractual\s+insurance(?:\s+adjustments?)?|out-of-pocket\s+(?:co(?:-?pay(?:ments?)?)?|costs?|expenses?|charges?))$/i;
const ICD_CODE = /^[A-TV-Z]\d{2}(?:\.[0-9A-Z]{1,4})$/i;
const ICD_LABEL =
  /\b(?:ICD(?:[- ]?10(?:[- ]CM)?)?|diagnosis\s+code)\s*[:#(-]?\s*$/i;
const PERSONAL_BEFORE =
  /\b(?:Mr|Mrs|Ms|Miss|Mx|Dr|Prof|Judge|Sir|Dame|patient|client|son|daughter|spouse|husband|wife|brother|sister|employee|respondent|claimant|investigator|witness|author|reporter|(?:reported|prepared|reviewed|approved|signed|entered)\s+by)\.?\s*:?\s+$/i;
const PERSONAL_AFTER =
  /^\s+(?:said|says|told|asked|called|emailed|texted|wrote|signed|lives|works|married|retired|was\s+born)\b/i;
const BUSINESS_AFTER =
  /^\s+(?:invoiced|billed|approved|denied|insured|employed|hired|supplied|shipped|delivered|manufactured|underwrote)\b/i;
const BUSINESS_BEFORE =
  /\b(?:department|clinic|hospital|account|invoice|bill|policy|coverage|contract|employer|payroll)\s+(?:at|with|from|of|through)\s+$/i;

function locationContext(text: string, d: Detection): boolean {
  const before = text.slice(Math.max(0, d.start - 60), d.start);
  const after = text.slice(d.end, d.end + 65);
  // A town next to a state/province and postal code is stronger evidence than a
  // name match.
  const address =
    /^,?\s+([A-Z]{2}|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*,?\s+(?:\d{4,6}\b|[A-Z]\d[A-Z]\s?\d[A-Z]\d\b)/.exec(
      after,
    );
  if (address && isRegion(address[1])) return true;
  if (
    /^\s+(?:address|residence|property|neighbou?rhood|city|county|area)\b/i.test(
      after,
    )
  ) {
    return true;
  }
  return (
    /\b(?:in|near|outside|within|through|around|towards?)\s+$/i.test(before) ||
    /\b(?:moved|relocated|travelled|traveled|returned|drove|flew)\s+(?:back\s+)?(?:to|from)\s+$/i.test(
      before,
    ) ||
    /\b(?:city|town|county|location|residence)\s*:\s*$/i.test(before)
  );
}

function organizationName(value: string): boolean {
  const name = collapse(value);
  const last = name
    .split(' ')
    .at(-1)!
    .replace(/[.,]+$/, '');
  return (
    !MEDICAL_SERVICE.test(name) &&
    (ORGANIZATION_END.test(name) || ORG_TAIL.test(last))
  );
}

function groundedLocation(
  text: string,
  start: number,
  end: number,
  detections: Detection[],
): boolean {
  const before = text.slice(Math.max(0, start - 60), start);
  const after = text.slice(end, end + 65);
  const address =
    /^,?\s+([A-Z]{2}|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*,?\s+(?:\d{4,6}\b|[A-Z]\d[A-Z]\s?\d[A-Z]\d\b)/.exec(
      after,
    );
  if (address && isRegion(address[1])) return true;
  if (/^\s+(?:address|city|county|neighbou?rhood)\b/i.test(after)) return true;
  if (/\b(?:city|town|county|birthplace)\s*:\s*$/i.test(before)) return true;
  if (
    /\b(?:lives?|living|resides?|residing|born|house|condo|apartment|property)\s+in\s+$/i.test(
      before,
    )
  ) {
    return true;
  }
  return detections.some(
    d =>
      d.kind === 'street' &&
      d.end <= start &&
      /^[,\s]{1,5}$/.test(text.slice(d.end, start)),
  );
}

function relabel(
  d: Detection,
  kind: string,
  label: string,
  base: string,
  canonical = collapse(d.text),
  entity = `${kind}:${key(canonical)}`,
): Detection {
  return {...d, kind, label, base, canonical, entity};
}

/**
 * Correct a category using the context of this occurrence, retaining its
 * redaction choice.
 */
export function classifyDetections(
  text: string,
  detections: Detection[],
  topics: Topics,
): Detection[] {
  // The model's place list includes facilities, and can include unrelated
  // people. Require address, residence or table-column evidence before it can
  // override an existing name.
  const placeMatches = detectPatterns(text, ['places'], []);
  const places = new Set(
    [
      ...placeMatches
        .filter(
          m =>
            groundedLocation(text, m.start, m.end, detections) ||
            locationContext(text, {start: m.start, end: m.end} as Detection),
        )
        .map(m => m.text),
      ...tableDetections(text, ['places'])
        .filter(m => m.type === 'places')
        .map(m => m.text),
    ]
      .filter(s => !organizationName(s))
      .map(key),
  );
  for (const name of topics.places) {
    if (organizationName(name)) continue;
    const escaped = collapse(name)
      .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      .replace(/ /g, '\\s+');
    if (!escaped) continue;
    for (const m of text.matchAll(
      new RegExp(`(?<![\\p{L}\\p{N}])${escaped}(?![\\p{L}\\p{N}])`, 'gu'),
    )) {
      if (groundedLocation(text, m.index, m.index + m[0].length, detections)) {
        places.add(key(name));
      }
    }
  }
  const health = new Set(topics.health.map(key));
  const terms = sensitiveTerms(text);
  const defined = new Set(definedTerms(text).map(t => key(t.term)));
  const placeLabel = detectorById('places')!.label;

  const corrected = detections.map(d => {
    if (d.source === 'manual') return d;
    // Pattern and model place matches use the same entity, so they restore to
    // the city, never to a clinic whose name starts with it.
    if (d.kind === 'places') return relabel(d, 'places', placeLabel, 'PLACE');

    const word = collapse(d.text);
    const before = text.slice(Math.max(0, d.start - 60), d.start);
    const after = text.slice(d.end, d.end + 65);
    if (
      ICD_CODE.test(word) &&
      ICD_LABEL.test(before) &&
      ['record', 'government_id', 'person', 'company'].includes(d.kind)
    ) {
      return relabel(d, 'health', 'Health detail', 'HEALTH_DETAIL');
    }
    if (d.kind !== 'person' && d.kind !== 'company') return d;

    // "Elm Dr\nCalgary" ends a street address; Dr is not a title for Calgary.
    const followsStreet = detections.some(
      st =>
        st.kind === 'street' &&
        st.end <= d.start &&
        /^[,\s]{1,5}$/.test(text.slice(st.end, d.start)),
    );
    const titled = PERSONAL_BEFORE.test(before) && !followsStreet;
    const personal = titled || PERSONAL_AFTER.test(after);
    if (places.has(key(word)) && !isRegion(word)) {
      const location =
        locationContext(text, d) ||
        groundedLocation(text, d.start, d.end, detections);
      const personAlias =
        d.kind === 'person' &&
        collapse(d.canonical).includes(' ') &&
        key(d.canonical) !== key(word);
      const companyAlias =
        d.kind === 'company' && key(d.canonical) !== key(word);
      const business =
        BUSINESS_BEFORE.test(before) ||
        BUSINESS_AFTER.test(after) ||
        defined.has(key(word));
      if (
        !titled &&
        !organizationName(word) &&
        (location || (!personal && !personAlias && !companyAlias && !business))
      ) {
        return relabel(d, 'places', placeLabel, 'PLACE');
      }
    }
    if (personal) return d;

    // Recognize complete headings and their spurious short forms. Keep the
    // actual text as the restoration value: "Primary" must not restore to
    // "Primary Applicant".
    if (isLabel(word) || isLabel(d.canonical)) {
      return relabel(d, 'other', 'Document label or role', 'REDACTED');
    }
    const billing = /^[^\n]{0,60}(?:[$€£]|\t\s*\d)/.test(after);
    if (BILLING_LABEL.test(word) && billing) {
      return relabel(d, 'other', 'Billing description', 'REDACTED');
    }

    // "Asthma Research Foundation" is an organization, not an illness. The same
    // applies to a known provider's shortened name, such as "Diagnostic
    // Imaging" for "... LLC".
    if (organizationName(word) || organizationName(d.canonical)) return d;
    const clinicalTerm = terms.some(
      t => t.kind === 'health' && t.start >= d.start && t.end <= d.end,
    );
    const condition = CLINICAL_END.test(word) && clinicalTerm;
    if (
      (health.has(key(word)) && clinicalTerm) ||
      condition ||
      (MEDICAL_SERVICE.test(word) && billing)
    ) {
      return relabel(d, 'health', 'Health detail', 'HEALTH_DETAIL');
    }
    return d;
  });

  // An explicit organization on the page can also be returned as a "person"
  // without its ending. Prefer its known organization identity when the short
  // form is unambiguous.
  const companies = [
    ...new Set(
      corrected
        .filter(d => d.kind === 'company' && d.source !== 'manual')
        .map(d => d.canonical),
    ),
  ];
  const aliases = new Map<string, Map<string, string>>();
  for (const c of nameCandidates({people: [], companies})) {
    if (!c.text.includes(' ')) continue;
    const owners = aliases.get(key(c.text)) ?? new Map<string, string>();
    owners.set(c.entity, c.canonical);
    aliases.set(key(c.text), owners);
  }
  return corrected.map(d => {
    if (d.source === 'manual' || d.kind !== 'person') return d;
    if (PERSONAL_BEFORE.test(text.slice(Math.max(0, d.start - 60), d.start))) {
      return d;
    }
    if (GIVEN_NAMES.has(key(collapse(d.text).split(' ')[0]))) return d;
    const owners = aliases.get(key(d.text));
    if (owners?.size !== 1) return d;
    const [entity, canonical] = [...owners][0];
    return relabel(d, 'company', 'Organization', 'COMPANY', canonical, entity);
  });
}
