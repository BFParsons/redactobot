/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {applyRedactions, findOccurrences} from './redact';
import {identityContexts, privacyBucket} from './privacy-buckets';
import {cleanedText, localFindings} from '../extension/policy';
import type {Finding, ScanReport} from '../extension/protocol';
import {allCategoriesSelected} from '../extension/categories';

/**
 * Runtime-issued capability. A cast or plain string cannot authorize a request.
 */
export interface CloudInput {
  readonly text: string;
  readonly kind: 'approved-cloud-input';
}
interface Grant {
  known: Finding[];
  prefix: string;
  used: boolean;
  expires: number;
  purpose: 'cleanup' | 'answer';
}
const grants = new WeakMap<CloudInput, Grant>();
function issue(
  text: string,
  known: Finding[],
  prefix: string,
  purpose: Grant['purpose'] = 'cleanup',
): CloudInput {
  const input: CloudInput = Object.freeze({text, kind: 'approved-cloud-input'});
  grants.set(input, {
    known,
    prefix,
    used: false,
    expires: Date.now() + 5 * 60_000,
    purpose,
  });
  return input;
}
function grantFor(input: CloudInput) {
  const grant = input && grants.get(input);
  if (!grant || Date.now() > grant.expires) {
    throw new Error(
      'A completed local privacy check is required before a cloud request.',
    );
  }
  return grant;
}
/**
 * Returns the approved text and marks the approval used, so it works once.
 * Throws if the approval is missing, expired or already used, or was issued for
 * a purpose other than `purpose`.
 */
export function takeCloudText(
  input: CloudInput,
  purpose?: Grant['purpose'],
): string {
  const grant = grantFor(input);
  if (purpose && grant.purpose !== purpose) {
    throw new Error(
      'Complete the required privacy stage before this cloud request.',
    );
  }
  if (grant.used) {
    throw new Error(
      'This cloud approval has already been used. Review again to retry.',
    );
  }
  grant.used = true;
  return input.text;
}

/**
 * Checks a finished local scan and issues a single-use approval to send the
 * locally redacted text for cloud cleanup. Throws unless the scan is complete,
 * reviewed where it asks for review, and still matches `text`, and the redacted
 * text holds no local-only identifier or identifying context.
 *
 * @param prefix Namespace added to placeholder names: capitals, digits and
 *     underscores only.
 * @param reviewed Whether the user has reviewed a scan that needs review.
 * @param removeSensitiveLocally Ids of health or sensitive findings to replace
 *     on the device. The other such findings stay in the text for the cloud
 *     pass.
 */
export function prepareCloudInput(
  text: string,
  report: ScanReport,
  prefix: string,
  reviewed = false,
  removeSensitiveLocally: string[] = [],
): CloudInput {
  if (report.categories && !allCategoriesSelected(report.categories)) {
    throw new Error(
      'Cloud cleanup requires all paste categories. This selection stays on this device.',
    );
  }
  if (!report.complete || report.reasons.length) {
    throw new Error(
      'The local identity check must finish without unresolved errors before cloud cleanup.',
    );
  }
  if (report.needsReview && !reviewed) {
    throw new Error(
      'Review identifying or uncertain details before cloud cleanup.',
    );
  }
  if (!/^[A-Z0-9_]{1,40}$/.test(prefix)) {
    throw new Error('Invalid placeholder namespace.');
  }
  const findings = [...report.findings].sort((a, b) => a.start - b.start);
  let at = 0;
  for (const d of findings) {
    if (
      !Number.isInteger(d.start) ||
      !Number.isInteger(d.end) ||
      d.start < at ||
      d.end <= d.start ||
      d.end > text.length ||
      text.slice(d.start, d.end) !== d.text
    ) {
      throw new Error('The document changed. Run the local check again.');
    }
    at = d.end;
  }
  const local = findings.filter(d => privacyBucket(d) === 'local-only');
  // The model or UI may never uncover a deterministic/local context match.
  for (const d of localFindings(text).filter(
    d => privacyBucket(d) === 'local-only',
  )) {
    if (!local.some(x => x.start <= d.start && x.end >= d.end)) {
      throw new Error(
        'A local identifier is still uncovered. Run the local check again.',
      );
    }
  }
  const remove = new Set(removeSensitiveLocally);
  const redacted = cleanedText(
    text,
    findings,
    prefix,
    findings
      .filter(d => privacyBucket(d) === 'cloud-cleanup' && !remove.has(d.id))
      .map(d => d.id),
  );
  if (
    identityContexts(redacted).length ||
    localFindings(redacted).some(d => privacyBucket(d) === 'local-only')
  ) {
    throw new Error(
      'The preview still contains a possible identifier or identifying context. Remove it locally first.',
    );
  }
  return issue(
    redacted,
    findings
      .filter(d => privacyBucket(d) === 'cloud-cleanup')
      .map(d => ({...d})),
    prefix,
  );
}

/** The result of a cloud cleanup pass over approved text. */
export interface CloudCleanup {
  /** The approved text the cloud model was given. */
  readonly text: string;
  /** The merged local and cloud findings, and the text after replacing them. */
  readonly report: ScanReport;
  /** Placeholder (without brackets) -> the text it replaced. */
  readonly replacements: ReadonlyMap<string, string>;
}
const completed = new WeakMap<
  CloudCleanup,
  {text: string; needsReview: boolean}
>();
/**
 * Cloud output is a list of exact excerpts. It never becomes replacement prose.
 * Include every locally known sensitive span even when the cloud misses it.
 */
export function applyCloudCleanup(
  input: CloudInput,
  value: unknown,
): CloudCleanup {
  const grant = grantFor(input);
  const data = value as {complete?: unknown; findings?: unknown};
  if (
    !data ||
    data.complete !== true ||
    !Array.isArray(data.findings) ||
    data.findings.length > 5000
  ) {
    throw new Error(
      'Cloud cleanup returned an incomplete answer. The paste is still held.',
    );
  }
  const spans: Finding[] = [];
  const add = (
    phrase: string,
    kind: string,
    reason?: string,
    requireMatch = false,
  ) => {
    const matches = findOccurrences(input.text, phrase);
    if (requireMatch && !matches.length) {
      throw new Error(
        'Cloud cleanup returned a detail that is not in the approved text. Review locally.',
      );
    }
    for (const [start, end] of matches) {
      spans.push({
        id: `${start}-${end}`,
        start,
        end,
        text: input.text.slice(start, end),
        kind,
        label:
          kind === 'health'
            ? 'Health detail'
            : kind === 'sensitive'
              ? 'Sensitive detail'
              : 'Detail to review',
        base:
          kind === 'health'
            ? 'HEALTH'
            : kind === 'sensitive'
              ? 'SENSITIVE'
              : 'REDACTED',
        source: 'model',
        canonical: phrase,
        entity: `${kind}:${phrase.toLowerCase()}`,
        defaultOn: true,
        enabled: true,
        reviewReason: reason,
        bucket: kind === 'other' ? 'local-only' : 'cloud-cleanup',
      });
    }
  };
  for (const d of grant.known) add(d.text, d.kind);
  for (const row of data.findings) {
    if (
      !row ||
      typeof row.text !== 'string' ||
      !row.text.trim() ||
      /^\[[A-Z][A-Z0-9_]*\]$/.test(row.text.trim()) ||
      row.text.length > input.text.length ||
      !['health', 'sensitive', 'identifying', 'uncertain'].includes(
        row.category,
      )
    ) {
      throw new Error(
        'Cloud cleanup returned an invalid detail. The paste is still held.',
      );
    }
    const review = ['identifying', 'uncertain'].includes(row.category);
    // An excerpt can span a placeholder ("[PERSON_X_1]'s diabetes"). Redact
    // only the text around it, so restore() can still put the name back in the
    // answer.
    for (const part of row.text.split(/\[[A-Z][A-Z0-9_]*\]/)) {
      const phrase = part
        .replace(/^['’]s\b/, '')
        .replace(/^[\s\p{P}]+|[\s\p{P}]+$/gu, '');
      if (/[\p{L}\p{N}]/u.test(phrase)) {
        add(
          phrase,
          review ? 'other' : row.category,
          review
            ? 'Cloud review found a possible identifying or ambiguous detail. Check the cleaned result.'
            : undefined,
          true,
        );
      }
    }
  }
  const merged: Finding[] = [];
  for (const d of spans.sort((a, b) => a.start - b.start || b.end - a.end)) {
    const prior = merged.at(-1);
    if (!prior || d.start >= prior.end) {
      merged.push({...d});
      continue;
    }
    prior.end = Math.max(prior.end, d.end);
    prior.id = `${prior.start}-${prior.end}`;
    prior.text = input.text.slice(prior.start, prior.end);
    prior.reviewReason ||= d.reviewReason;
    if (prior.kind !== d.kind || prior.reviewReason) {
      prior.kind = 'other';
      prior.base = 'REDACTED';
      prior.bucket = 'local-only';
    }
    prior.canonical = prior.text;
    prior.entity = `${prior.kind}:${prior.text.toLowerCase()}`;
  }
  const red = applyRedactions(
    input.text,
    merged.map(d => ({...d, base: `${d.base}_${grant.prefix}_CLOUD`})),
  );
  const report: ScanReport = {
    findings: merged,
    cleaned: red.cleaned,
    replacements: Object.fromEntries(red.placeholders),
    complete: true,
    needsReview: merged.some(d => d.reviewReason),
    reasons: [],
  };
  const result: CloudCleanup = Object.freeze({
    text: input.text,
    report,
    replacements: red.map,
  });
  completed.set(result, {text: red.cleaned, needsReview: report.needsReview});
  return result;
}
/**
 * Issues a single-use approval to send a cloud-cleaned text for answering.
 * Throws if `result` did not come from applyCloudCleanup, or it needs review
 * and `reviewed` is false.
 */
export function approveCleanedResult(
  result: CloudCleanup,
  reviewed = false,
): CloudInput {
  const saved = completed.get(result);
  if (!saved || (saved.needsReview && !reviewed)) {
    throw new Error('Review the cleaned cloud result first.');
  }
  return issue(saved.text, [], 'FINAL', 'answer');
}
