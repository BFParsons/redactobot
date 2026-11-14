/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import type {Detection} from './redact';
import {
  sensitiveTerms,
  describesUniquePerson,
  describesUniqueAsset,
} from './sensitive-terms';

/**
 * Where a finding may be handled: on this device only, or also by the cloud
 * cleanup pass.
 */
export type PrivacyBucket = 'local-only' | 'cloud-cleanup';
/** The label shown to the user for each bucket. */
export const BUCKET_LABELS: Record<PrivacyBucket, string> = {
  'local-only': 'Must stay local',
  'cloud-cleanup': 'Sensitive detail — cloud cleanup eligible',
};
/**
 * Returns the bucket for a finding. Only health and sensitive findings with no
 * review reason may go to cloud cleanup. Unknown/new detectors fail closed.
 * Context or uncertainty takes precedence.
 */
export function privacyBucket(
  finding: Pick<Detection, 'kind'> & {reviewReason?: string},
): PrivacyBucket {
  return !finding.reviewReason && ['health', 'sensitive'].includes(finding.kind)
    ? 'cloud-cleanup'
    : 'local-only';
}
/** A sentence or paragraph that may identify someone, and the reason why. */
export interface IdentityContext {
  text: string;
  reason: string;
}
const sentences = new Intl.Segmenter('en', {granularity: 'sentence'});
const SELF_ASSERTION =
  /\b(?:I|we)\s+(?:have|had|am|are|was|were|suffer|suffered|take|took|underwent|received|tested|live|lived|reside|own|owned|earn|earned|owe|owed|work|worked)\b|\bI['’](?:m|ve)\b/i;
const PERSONAL_FACT =
  /\b(?:diagnos(?:is|ed)|symptoms?|medical history|treatment|prescription|disability|salary|income|net worth|debts?|account number|date of birth|home address|live at|reside at|work as|employed by)\b/i;
const POSSESSIVE_FACT =
  /\b(?:my|our)\s+(?:diagnosis|symptoms?|treatment|medication|prescription|disability|salary|income|debts?|account|address|date of birth|medical history|genome|fingerprint|voiceprint)\b/i;
const FAMILY =
  /\b(?:her|his|their|my|our|the patient['’]s|the client['’]s)\s+(?:mother|father|daughter|son|spouse|wife|husband|sibling|sister|brother|employer)\b/i;
const RARE_EVENT =
  /\b(?:rare|one[- ]of[- ]a[- ]kind|widely[- ]reported|nationally[- ]reported)\b/i;
const BIOMETRIC =
  /\b(?:genome|genomic sequence|DNA sequence|fingerprint|voiceprint|biometric|security answer|secret key|private key)\b/i;
const PRIVATE_VALUE =
  /\b(?:genome|sequence|fingerprint|voiceprint|security answer|secret key|private key)\s*[:=]\s*\S|-----BEGIN [A-Z ]*PRIVATE KEY-----|\b[ACGT]{20,}\b/i;
const GENERAL_REQUEST =
  /^\s*(?:please\s+)?(?:explain|describe|define|compare|what|how|why|can you|could you|write|summari[sz]e|give|I (?:want|need|would like)|we (?:want|need|would like))\b/i;

function contextReason(source: string): string | undefined {
  // Pronouns in requests and code are not evidence of identity. Remove only the
  // request preamble for this test; a later "I have diabetes" still gets
  // checked.
  const plain = source
    .replace(/\[[A-Z][A-Z0-9_]*\]/g, '')
    .replace(
      /\b(?:I|we)\s+(?:have|had)\s+(?:a|some|several)\s+(?:questions?|requests?|ideas?|suggestions?|examples?)\b/gi,
      '',
    )
    .replace(
      /\b(?:I am|I'm|I’m|we are)\s+(?:learning|trying|writing|studying|asking|curious|interested|looking|planning|hoping|researching)\b/gi,
      '',
    )
    .replace(
      /\b(?:my|our)\s+(?:paper|essay|article|report|prompt|summary|question|draft|example|project|research|code|document|text|notes|presentation|outline|understanding)\b/gi,
      '',
    );
  const sensitive = sensitiveTerms(plain);
  const personalSensitive = sensitive.some(
    term =>
      !/^(?:diagnosis|symptoms?|treatment|medication|prescription|medical history)$/i.test(
        plain.slice(term.start, term.end),
      ) &&
      /\b(?:my|our)(?:\s+[\p{L}-]+){0,2}\s+$/iu.test(
        plain.slice(Math.max(0, term.start - 45), term.start),
      ),
  );
  const possession = POSSESSIVE_FACT.exec(plain);
  const valueAfterPossession = possession
    ? plain
        .slice(possession.index + possession[0].length)
        .replace(/^\s*(?:is|was|are|were|number)?\s*[:=-]?\s*/i, '')
    : '';
  if (
    (possession && /[\p{L}\p{N}]/u.test(valueAfterPossession)) ||
    personalSensitive ||
    (SELF_ASSERTION.test(plain) &&
      (sensitive.length > 0 || PERSONAL_FACT.test(plain)))
  ) {
    return 'This sentence links sensitive facts to the author or account holder.';
  }
  if (
    describesUniquePerson(plain) ||
    describesUniqueAsset(plain) ||
    (RARE_EVENT.test(plain) &&
      /\b(?:patient|client|survivor|recipient|diagnosed|suffers?|experienced|underwent|has|had|I|my|our)\b/i.test(
        plain,
      ))
  ) {
    return 'A distinctive personal description or event may identify someone.';
  }
  if (FAMILY.test(plain)) {
    return 'A family or employment relationship may identify someone.';
  }
  if (
    BIOMETRIC.test(plain) &&
    (PRIVATE_VALUE.test(plain) ||
      /\b(?:my|our)\s+(?:genome|fingerprint|voiceprint|private key|secret key|security answer)\b/i.test(
        plain,
      ) ||
      !GENERAL_REQUEST.test(plain))
  ) {
    return 'This sentence may contain an identifying biometric or security secret.';
  }
}

/**
 * Conservative backstop scoped to identifying facts, not ordinary request
 * words. Keep sentence boundaries so one private fact does not erase unrelated
 * instructions. This is a detection aid, not proof of anonymity.
 */
export function identityContexts(text: string): IdentityContext[] {
  const results: IdentityContext[] = [];
  for (const paragraph of text.split(/\n\s*\n/)) {
    if (!paragraph.trim()) continue;
    // Structured secrets/biometric values can continue on several lines. Do not
    // leave the value behind after protecting only its heading.
    if (/\n/.test(paragraph) && BIOMETRIC.test(paragraph)) {
      const reason = contextReason(paragraph);
      if (reason) {
        results.push({text: paragraph.trim(), reason});
        continue;
      }
    }
    const start = results.length;
    for (const item of sentences.segment(paragraph)) {
      const sentence = item.segment.trim();
      const reason = contextReason(sentence);
      if (reason) results.push({text: sentence, reason});
    }
    // Preserve a personal fact split across an extraction line break when
    // segmentation could not keep its subject and sensitive value together.
    if (results.length === start && /\n/.test(paragraph)) {
      const reason = contextReason(paragraph);
      if (reason) results.push({text: paragraph.trim(), reason});
    }
  }
  return results;
}
