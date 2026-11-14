/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Turns rule matches and on-device model evidence into the
 * findings, review reasons and cleaned text of a scan report.
 */

import {DETECTORS, detectPatterns} from '../../taxonomy/taxonomy.js';
import {
  applyRedactions,
  buildDetections,
  findOccurrences,
  NO_TOPICS,
  type Names,
  type Topics,
} from '../core/redact';
import {collapse, key} from '../core/names';
import type {Ambiguous, Finding, ScanReport} from './protocol';
import {identityContexts, privacyBucket} from '../core/privacy-buckets';
import {generalTopicQuestion, sensitiveTerms} from '../core/sensitive-terms';
import {
  ALL_CATEGORIES,
  selectedDetectors,
  selectedModelKinds,
  watchesKind,
  type PasteCategory,
} from './categories';

const CLEAR_PATTERNS = new Set([
  'email',
  'phone',
  'card',
  'card_partial',
  'record',
  'places',
  'street',
  'zip',
  'postal_ca',
  'region',
  'ssn',
  'sin_ca',
  'iban',
  'routing',
  'account',
  'passport_dl',
]);
const FIELD_LABEL =
  /^(?:(?:payment|credit|debit)\s+)?card(?:\s+(?:number|no|id))?$|^(?:record|case|claim|file|invoice|reference|patient)(?:\s+(?:number|no|id))?$|^(?:MRN|city|town|county|location|address|email|phone|postal code|zip|SSN|SIN|IBAN|routing number|account number|passport number)$/i;
const clearPattern = (d: Finding) =>
  d.source === 'pattern' && !d.reviewReason && CLEAR_PATTERNS.has(d.kind);

function genericIndustryWarning(
  text: string,
  start: number,
  end: number,
): boolean {
  const phrase = text.slice(start, end);
  if (
    !/^(?:artificial intelligence(?: companies| industry| sector)?|chipmakers|data cent(?:er|re) developers|(?:technology|software|semiconductor|construction) (?:companies|firms|industry|sector))$/.test(
      phrase,
    )
  ) {
    return false;
  }
  const before = text.slice(Math.max(0, start - 70), start);
  const after = text.slice(end, end + 30);
  // This resolves only a generic prose description, never a named field, alias,
  // personal affiliation, quoted name or organization with a legal suffix.
  return (
    !/(?:["'“‘]|\b(?:my|our|his|her|their)\s+|\b(?:client|company|employer|business|name)\s*[:=]\s*|\b(?:called|named|aka)\s+)$/i.test(
      before,
    ) && !/^\s*(?:["'”’]|(?:LLC|Ltd|Inc|Corp)\b)/i.test(after)
  );
}

function ordinaryTaskWarning(phrase: string): boolean {
  // Exact, bounded instruction grammar: never discard unknown words or values
  // just because a phrase starts with a request. Existing detector matches take
  // priority.
  const value = phrase
    .trim()
    .replace(/[.!?]$/, '')
    .trim();
  return (
    /^(?:please\s+)?(?:I|we)\s+(?:want|need|would like)\s+(?:a\s+)?(?:(?:short|brief|concise)\s+)?(?:summary|rewrite|revision)\s+of\s+(?:this|the|my|our)\s+(?:article|text|document|draft|paragraph|note)$/i.test(
      value,
    ) ||
    /^(?:please\s+)?(?:only\s+)?(?:return|output|use)\s+(?:only\s+)?JSON(?:\s+with\s+(?:unique\s+)?keys)?$/i.test(
      value,
    ) ||
    /^(?:please\s+)?keep\s+(?:the|your)\s+(?:reply|response|answer|tone)\s+(?:short|concise|brief|friendly|professional)$/i.test(
      value,
    )
  );
}

function redundantFieldWarning(
  text: string,
  start: number,
  end: number,
  overlaps: Finding[],
): boolean {
  if (!overlaps.length || overlaps.some(d => !clearPattern(d))) return false;
  let at = start;
  for (const d of [...overlaps].sort((a, b) => a.start - b.start)) {
    const gap = text
      .slice(at, Math.max(at, d.start))
      .replace(/[\p{P}\s]/gu, ' ')
      .trim()
      .replace(/\s+/g, ' ');
    if (gap && !FIELD_LABEL.test(gap)) return false;
    at = Math.max(at, d.end);
  }
  return !/[\p{L}\p{N}]/u.test(text.slice(at, end));
}

function generalTopicWarning(
  text: string,
  start: number,
  end: number,
): boolean {
  if (!generalTopicQuestion(text, start, end)) return false;
  const phrase = text.slice(start, end);
  const terms = sensitiveTerms(phrase, true).filter(
    t => t.topic !== 'identifying',
  );
  if (!terms.length) return false;
  let residual = '';
  let at = 0;
  for (const term of terms) {
    residual += phrase.slice(at, term.start) + ' ';
    at = term.end;
  }
  residual += phrase.slice(at);
  // Only known topic vocabulary and a small ordinary question frame. Unknown
  // names, numbers, codes and other facts are never excused by a vague
  // educational prefix.
  residual = residual.replace(
    /\b(?:please|explain|define|describe|compare|what|is|are|how|does|do|give|me|an|a|the|overview|of|teach|about|in|simple|plain|terms|language|and|or|work|works|briefly)\b/gi,
    '',
  );
  return !/[\p{L}\p{N}]/u.test(residual);
}

/** Ids of every detector whose status is `ready`. */
export const GUARD_DETECTORS = DETECTORS.filter(d => d.status === 'ready').map(
  d => d.id,
);
function unselectedContactRanges(
  text: string,
  categories: readonly PasteCategory[],
) {
  // Recognize token boundaries for classification even when their removal is
  // off. A name alias inside an email/URL must not become a separate person
  // finding.
  const ids = [
    ...(categories.includes('contact') ? [] : ['email']),
    ...(categories.includes('online') ? [] : ['url']),
  ];
  return ids.length ? detectPatterns(text, ids, []) : [];
}
function scopedCandidates(
  text: string,
  names: Names,
  topics: Topics,
  categories: readonly PasteCategory[],
): Finding[] {
  if (!categories.length) return [];
  return buildDetections(
    text,
    selectedDetectors(categories),
    categories.includes('names') ? names : {people: [], companies: []},
    [],
    new Set(),
    {
      names: categories.includes('names') ? topics.names : [],
      places: categories.includes('places') ? topics.places : [],
      health: categories.includes('health') ? topics.health : [],
      sensitive: categories.includes('sensitive') ? topics.sensitive : [],
    },
    {
      health: categories.includes('health'),
      sensitive: categories.includes('sensitive'),
      identifying: categories.includes('context'),
    },
  );
}
const selectedFinding = (categories: readonly PasteCategory[], d: Finding) =>
  watchesKind(categories, d.kind) ||
  (categories.includes('context') && !!d.reviewReason);
/**
 * Returns the findings that the rules alone make in `text` for the selected
 * categories. A name inside an email address or URL whose own category is off
 * is left out.
 */
export function localFindings(
  text: string,
  categories: readonly PasteCategory[] = ALL_CATEGORIES,
): Finding[] {
  const boundaries = unselectedContactRanges(text, categories);
  return scopedCandidates(
    text,
    {people: [], companies: []},
    NO_TOPICS,
    categories,
  ).filter(
    d =>
      selectedFinding(categories, d) &&
      (!['person', 'company'].includes(d.kind) ||
        !boundaries.some(b => b.start <= d.start && b.end >= d.end)),
  );
}

/**
 * Returns `text` with each finding replaced by its placeholder in square
 * brackets. Findings whose ids are in `kept`, and findings that overlap an
 * earlier replacement, stay as written.
 *
 * @param prefix Suffix added to the base name of every placeholder.
 */
export function cleanedText(
  text: string,
  findings: Finding[],
  prefix: string,
  kept: string[] = [],
): string {
  const keep = new Set(kept);
  const result = applyRedactions(
    text,
    findings.map(d => ({...d, enabled: true, base: `${d.base}_${prefix}`})),
  );
  let cleaned = '';
  let at = 0;
  for (const d of [...findings].sort((a, b) => a.start - b.start)) {
    if (keep.has(d.id) || d.start < at) continue;
    cleaned += text.slice(at, d.start) + `[${result.placeholders.get(d.id)}]`;
    at = d.end;
  }
  return cleaned + text.slice(at);
}

/**
 * Builds the scan report for `text`. Merges the model evidence with the rule
 * findings without uncovering any rule match, turns uncertainties into review
 * reasons or new findings, assigns each finding a privacy bucket and produces
 * the cleaned text.
 *
 * @param ambiguous Excerpts the model was unsure of.
 * @param prefix Suffix added to the base name of every placeholder.
 * @param complete False when the model scan did not finish; the report then
 *     needs review.
 * @param failure Reason for review to show the user.
 * @param identifying Excerpts the model says may identify someone indirectly.
 */
export function makeReport(
  text: string,
  names: Names,
  topics: Topics,
  ambiguous: Ambiguous[],
  prefix: string,
  complete = true,
  failure?: string,
  identifying: Ambiguous[] = [],
  categories: readonly PasteCategory[] = ALL_CATEGORIES,
): ScanReport {
  const baseline = localFindings(text, categories);
  const candidates = scopedCandidates(text, names, topics, categories);
  const boundaries = unselectedContactRanges(text, categories);
  const excluded = candidates.filter(d => !selectedFinding(categories, d));
  let findings: Finding[] = candidates
    .filter(
      d =>
        selectedFinding(categories, d) &&
        (!['person', 'company'].includes(d.kind) ||
          !boundaries.some(b => b.start <= d.start && b.end >= d.end)),
    )
    .map(d => ({...d, enabled: true}));
  // Retain the union of local and model spans. Model evidence must never
  // uncover an earlier match.
  for (const original of baseline) {
    if (
      findings.some(d => d.start <= original.start && d.end >= original.end)
    ) {
      continue;
    }
    const overlaps = findings.filter(
      d => d.start < original.end && d.end > original.start,
    );
    if (!overlaps.length) {
      findings.push({...original, enabled: true});
      continue;
    }
    const start = Math.min(original.start, ...overlaps.map(d => d.start));
    const end = Math.max(original.end, ...overlaps.map(d => d.end));
    findings = findings.filter(d => !overlaps.includes(d));
    const value = text.slice(start, end);
    findings.push({
      ...original,
      id: `${start}-${end}`,
      start,
      end,
      text: value,
      canonical: value,
      kind: 'other',
      label: 'Detail to review',
      base: 'REDACTED',
      entity: `other:${key(value)}`,
      enabled: true,
      reviewReason: 'The checks disagree about the extent of this detail.',
    });
  }
  const reasons = failure ? [failure] : [];
  const modelKinds = selectedModelKinds(categories);
  const uncertainties = ambiguous.filter(item =>
    item.kind ? modelKinds.includes(item.kind) : categories.includes('context'),
  );
  for (const item of [
    ...uncertainties,
    ...(categories.includes('context')
      ? [...identifying, ...identityContexts(text)]
      : []),
  ]) {
    // A pronoun is not an identifier on its own. Actual self-linked sensitive
    // facts are still supplied by identityContexts and the model's full
    // identifying phrase.
    if (
      /^(?:I|me|my|mine|we|us|our|ours|you|your|he|him|his|she|her|they|them|their|it)$/i.test(
        item.text.trim(),
      )
    ) {
      continue;
    }
    const positions = findOccurrences(text, item.text);
    if (!positions.length) {
      reasons.push(
        'The model reported an uncertainty that needs a closer look.',
      );
      continue;
    }
    for (const [start, end] of positions) {
      // A corrected out-of-scope match (for example Seattle mislabelled as a
      // person) cannot return through the generic uncertainty path.
      if (
        [...excluded, ...boundaries].some(d => d.start <= start && d.end >= end)
      ) {
        continue;
      }
      const overlaps = findings.filter(d => d.start < end && d.end > start);
      if (!overlaps.length && ordinaryTaskWarning(text.slice(start, end))) {
        continue;
      }
      if (!overlaps.length && genericIndustryWarning(text, start, end)) {
        continue;
      }
      if (
        generalTopicWarning(text, start, end) ||
        redundantFieldWarning(text, start, end, overlaps)
      ) {
        continue;
      }
      const covering = overlaps.find(d => d.start <= start && d.end >= end);
      // Nano may call an email or phone "potentially sensitive". The exact
      // local detector already removes that entire detail, so this adds no
      // decision for the user. Keep review for broader phrases, uncertain
      // categories and any disagreement that was already found; never reduce
      // redaction coverage.
      if (covering) {
        // A generic doubt about a full name is resolved when local evidence and
        // Nano independently agree on the same person and exact span. Preserve
        // real category conflicts, short names and wider contextual warnings.
        const confirmedPerson =
          'kind' in item &&
          item.kind === 'person' &&
          covering.kind === 'person' &&
          !covering.reviewReason &&
          collapse(covering.text).split(' ').length >= 2 &&
          baseline.some(
            d =>
              d.kind === 'person' &&
              !d.reviewReason &&
              d.start === start &&
              d.end === end,
          ) &&
          names.people.some(name => key(name) === key(covering.text)) &&
          !names.companies.some(name => key(name) === key(covering.text));
        if (!clearPattern(covering) && !confirmedPerson) {
          covering.reviewReason =
            item.reason || 'This detail could have more than one meaning.';
        }
      } else {
        const from = Math.min(start, ...overlaps.map(d => d.start));
        const to = Math.max(end, ...overlaps.map(d => d.end));
        const value = text.slice(from, to);
        findings = findings.filter(d => !overlaps.includes(d));
        findings.push({
          id: `${from}-${to}`,
          start: from,
          end: to,
          text: value,
          kind: 'other',
          label: 'Detail to review',
          base: 'REDACTED',
          entity: `other:${key(value)}`,
          canonical: collapse(value),
          source: 'model',
          defaultOn: true,
          enabled: true,
          reviewReason:
            item.reason || 'This detail could have more than one meaning.',
        });
      }
    }
  }
  const people = new Set(names.people.map(key));
  const companies = new Set(names.companies.map(key));
  findings = findings
    .sort((a, b) => a.start - b.start)
    .map(d => {
      let reviewReason = d.reviewReason;
      if (d.kind === 'other') {
        reviewReason ??=
          'Removing this could change the meaning. Please check it.';
      }
      if (d.kind === 'person' && !collapse(d.text).includes(' ')) {
        reviewReason ??= 'This short name may also be an ordinary word.';
      }
      if (
        ['person', 'company'].includes(d.kind) &&
        people.has(key(d.text)) &&
        companies.has(key(d.text))
      ) {
        reviewReason ??=
          'The model disagrees about whether this is a person or organization.';
      }
      return {
        ...d,
        enabled: true,
        reviewReason,
        bucket: privacyBucket({...d, reviewReason}),
      };
    });
  if (!complete && !reasons.length) {
    reasons.push(
      'The full scan could not finish. Please review before pasting.',
    );
  }
  const result = applyRedactions(
    text,
    findings.map(d => ({...d, base: `${d.base}_${prefix}`})),
  );
  const cloudText = cleanedText(
    text,
    findings,
    prefix,
    findings.filter(d => d.bucket === 'cloud-cleanup').map(d => d.id),
  );
  return {
    findings,
    cleaned: result.cleaned,
    replacements: Object.fromEntries(result.placeholders),
    complete,
    cloudText,
    categories: [...categories],
    needsReview:
      !complete || reasons.length > 0 || findings.some(d => d.reviewReason),
    reasons: [...new Set(reasons)],
  };
}
