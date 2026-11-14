/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Offline research only: these proposals are not imported by the
 * application. No answer keys, extra model calls, network access, or persisted
 * user data.
 */

import {
  findOccurrences,
  type Detection,
  type Names,
  type Topics,
} from '../../src/core/redact';
import {NOT_NAME_WORDS, ORG_TAIL} from '../../src/core/names';
import {AMBIGUOUS_NAMES} from '../../src/core/given-names';
import {isRegion} from '../../taxonomy/taxonomy.js';

export const VARIANTS = [
  'baseline',
  'trust-model',
  'guarded-exact',
  'guarded-normalized',
  'complete-spans',
  'combined',
  'identifier-memory',
  'combined-memory',
] as const;
export type Variant = (typeof VARIANTS)[number];
interface Proposal {
  value: string;
  kind: 'person' | 'company' | 'places';
}

// Deliberately generic language, not a list of missed benchmark values.
const GENERIC = new Set(
  (
    'the a an of and for in on to at by from with as is was are were it its their our your his her ' +
    'company companies corporation incorporated limited llc llp ltd co corp trust credit union bank account savings checking ' +
    'health medical dental care insurance plan policy university college school bookstore hall office public private federal ' +
    'state united states department government district county city court superior supreme circuit justice revenue treasury ' +
    'internal service services social security administration national international retirement benefit benefits payment payments ' +
    'petty cash local unknown none not available potential new client customer patient employee employer witness provider ' +
    'regular meeting family doctor phone email address street avenue road drive lane unit suite apartment building floor ' +
    'google microsoft quickbooks excel paypal zelle venmo zoom outlook gmail docusign medicare medicaid irs cra hmrc ' +
    'january february march april may june july august september october november december reading will bill mark rose hope grace ' +
    'we you he she they this that next last tomorrow yesterday today morning afternoon evening'
  ).split(' '),
);
const tokens = (s: string) =>
  s.toLowerCase().match(/[\p{L}\p{M}]+(?:['’-][\p{L}\p{M}]+)*/gu) ?? [];
const generic = (w: string) =>
  GENERIC.has(w) ||
  NOT_NAME_WORDS.has(w) ||
  ORG_TAIL.test(w[0].toUpperCase() + w.slice(1));

/**
 * Normalize graphemes while retaining original UTF-16 offsets, including
 * decomposed accents.
 */
export function normalizedView(text: string) {
  let value = '';
  const starts: number[] = [];
  const ends: number[] = [];
  for (const {segment, index} of new Intl.Segmenter('en', {
    granularity: 'grapheme',
  }).segment(text)) {
    const folded = segment
      .normalize('NFC')
      .toLowerCase()
      .replace(/[’‘ʼ]/g, "'")
      .replace(/[‐‑‒–]/g, '-');
    if (/^\s+$/u.test(folded)) {
      if (value.endsWith(' ')) {
        ends[ends.length - 1] = index + segment.length;
        continue;
      }
      value += ' ';
      starts.push(index);
      ends.push(index + segment.length);
    } else {
      value += folded;
      for (let i = 0; i < folded.length; i++) {
        starts.push(index);
        ends.push(index + segment.length);
      }
    }
  }
  return {value, starts, ends};
}

export function normalizedOccurrences(
  text: string,
  phrase: string,
  view = normalizedView(text),
): Array<[number, number]> {
  const needle = normalizedView(phrase).value.trim();
  if (!needle) return [];
  const esc = needle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const re = new RegExp(
    `(?<![\\p{L}\\p{M}\\p{N}])${esc}(?![\\p{L}\\p{M}\\p{N}])`,
    'gu',
  );
  return [...view.value.matchAll(re)].map(m => [
    view.starts[m.index],
    view.ends[m.index + m[0].length - 1],
  ]);
}

function acceptable(
  p: Proposal,
  text: string,
  start: number,
  end: number,
  ids: string[],
): boolean {
  if (
    p.value.length < 3 ||
    p.value.length > 120 ||
    /[\n\t].*[\n\t]/.test(p.value)
  ) {
    return false;
  }
  const words = tokens(p.value);
  if (
    !words.length ||
    words.length > 10 ||
    !words.some(w => w.length >= 3 && !generic(w))
  ) {
    return false;
  }
  const before = text.slice(Math.max(0, start - 60), start);
  const after = text.slice(end, end + 32);
  if (p.kind === 'person') {
    if (/\d|[;:!?]/.test(p.value)) return false;
    if (words.length > 1) return true;
    // A model's single ambiguous word is not enough evidence to replace
    // ordinary prose.
    if (AMBIGUOUS_NAMES.has(words[0]!)) return false;
    return /(?:\b(?:client|patient|witness|name|signed|regards|dear|thanks|contact|from|to)\s*[:,-]?\s*)$/i.test(
      before,
    );
  }
  if (p.kind === 'company') {
    return (
      words.length >= 2 &&
      !/\b(?:united states|department of|court of)\b/i.test(p.value)
    );
  }
  if (isRegion(p.value)) return ids.includes('region');
  // Lowercase location names need local location evidence; do not globally
  // redact e.g. "reading".
  return (
    /(?:\b(?:in|at|from|near|to|outside|within|city|town|location|address|moved to|move to)\s*[:,-]?\s*)$/i.test(
      before,
    ) || /^(?:,?\s+[A-Z]{2}\b|\s+\d{4,6}\b)/.test(after)
  );
}

/**
 * Reconcile grounded proposals. Completion may only subsume same-kind spans in
 * full.
 */
export function repairEvidence(
  text: string,
  ids: string[],
  names: Names,
  topics: Topics,
  baseline: Detection[],
  variant: Variant,
): Detection[] {
  if (variant === 'baseline') return baseline;
  if (variant === 'identifier-memory') return identifierMemory(text, baseline);
  if (variant === 'combined-memory') {
    return identifierMemory(
      text,
      repairEvidence(text, ids, names, topics, baseline, 'combined'),
    );
  }
  const normalized = variant === 'guarded-normalized' || variant === 'combined';
  const complete = variant === 'complete-spans' || variant === 'combined';
  const trust = variant === 'trust-model';
  const proposals: Proposal[] = [
    ...(ids.includes('names')
      ? [...names.people, ...(topics.names ?? [])].map(value => ({
          value,
          kind: 'person' as const,
        }))
      : []),
    ...(ids.includes('names')
      ? names.companies.map(value => ({value, kind: 'company' as const}))
      : []),
    ...(ids.includes('places')
      ? topics.places.map(value => ({value, kind: 'places' as const}))
      : []),
  ].sort((a, b) => b.value.length - a.value.length);
  let out = [...baseline];
  const view = normalized ? normalizedView(text) : undefined;
  for (const p of proposals) {
    const matches = normalized
      ? normalizedOccurrences(text, p.value, view)
      : findOccurrences(text, p.value);
    for (const [start, end] of matches) {
      if (!trust && !acceptable(p, text, start, end, ids)) continue;
      const overlap = out.filter(d => d.start < end && d.end > start);
      if (overlap.length) {
        if (
          !complete ||
          overlap.some(
            d =>
              d.source === 'manual' ||
              !d.enabled ||
              d.kind !== p.kind ||
              d.start < start ||
              d.end > end,
          )
        ) {
          continue;
        }
        // Already completely replaced, or two different established people:
        // keep the existing decision.
        if (overlap.some(d => d.start === start && d.end === end)) continue;
        if (
          p.kind === 'person' &&
          new Set(
            overlap.filter(d => /\s/.test(d.canonical)).map(d => d.entity),
          ).size > 1
        ) {
          continue;
        }
      } else if (variant === 'complete-spans') {
        // independent ablation: completion only
        continue;
      }
      const actual = text.slice(start, end);
      const owner = overlap[0];
      const entity =
        owner?.entity ?? `${p.kind}:experiment:${normalizedView(actual).value}`;
      const canonical = actual.replace(/\s+/g, ' ').trim();
      out = out.filter(d => !overlap.includes(d));
      // Keep existing aliases linked, and restore the complete value instead of
      // its former fragment.
      if (owner) {
        out = out.map(d => (d.entity === entity ? {...d, canonical} : d));
      }
      out.push({
        id: `${start}-${end}`,
        start,
        end,
        text: actual,
        kind: p.kind,
        base:
          p.kind === 'person'
            ? 'PERSON'
            : p.kind === 'company'
              ? 'COMPANY'
              : 'PLACE',
        label:
          p.kind === 'person'
            ? 'Person'
            : p.kind === 'company'
              ? 'Organization'
              : 'Place',
        entity,
        canonical,
        source: 'model',
        enabled: true,
        defaultOn: true,
      });
    }
  }
  return out.sort((a, b) => a.start - b.start);
}

/**
 * Learn document-local reference formats from at least two different explicitly
 * identified values. The literal prefix, separators, digit widths, and entity
 * kind must agree. No bare-number guessing.
 */
function identifierMemory(text: string, baseline: Detection[]): Detection[] {
  const families = new Map<
    string,
    {
      seed: Detection;
      values: Set<string>;
      expression: string;
      conflict: boolean;
    }
  >();
  for (const d of baseline) {
    if (
      !d.enabled ||
      d.source !== 'pattern' ||
      !['record', 'account', 'govid'].includes(d.kind)
    ) {
      continue;
    }
    if (!/^[A-Z]{2,8}(?:[-/]\d{2,8}){1,3}$/.test(d.text)) continue;
    const expression = d.text.replace(
      /\d+/g,
      digits => `\\d{${digits.length}}`,
    );
    const current = families.get(expression);
    if (current) {
      current.values.add(d.text);
      current.conflict ||= current.seed.kind !== d.kind;
    } else {
      families.set(expression, {
        seed: d,
        values: new Set([d.text]),
        expression,
        conflict: false,
      });
    }
  }
  const out = [...baseline];
  for (const {seed, values, expression, conflict} of families.values()) {
    if (values.size < 2 || conflict) continue;
    const re = new RegExp(
      `(?<![\\p{L}\\p{N}/-])${expression}(?![\\p{L}\\p{N}/-])`,
      'gu',
    );
    for (const m of text.matchAll(re)) {
      const start = m.index;
      const end = start + m[0].length;
      if (out.some(d => d.start < end && d.end > start)) continue;
      out.push({
        ...seed,
        id: `${start}-${end}`,
        start,
        end,
        text: m[0],
        canonical: m[0],
        entity: `${seed.kind}:${m[0].replace(/[\s-]/g, '').toLowerCase()}`,
        source: 'short-form',
      });
    }
  }
  return out.sort((a, b) => a.start - b.start);
}

/**
 * Chunk-boundary experiment, separately testable without pretending to rerun
 * the model.
 */
export function boundedChunks(text: string, maxWords = 350, overlapWords = 24) {
  if (maxWords < 1 || overlapWords < 0 || overlapWords >= maxWords) {
    throw new Error('Invalid chunk budget');
  }
  const words = [...text.matchAll(/\S+/g)];
  const out: Array<{start: number; end: number}> = [];
  for (let first = 0; first < words.length;) {
    const last = Math.min(words.length, first + maxWords);
    out.push({
      start: words[first].index,
      end: words[last - 1].index + words[last - 1][0].length,
    });
    if (last === words.length) break;
    first = last - overlapWords;
  }
  return out;
}
