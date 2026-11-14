/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Could this text name a person or organization? A cheap,
 * deliberately over-eager check that decides whether the paste gate needs
 * Gemini Nano at all. Rules already handle every structured identifier as well
 * as the model does (evaluation/PASTE-GATE-DETERMINISTIC.md); the model's job
 * is names. When this returns false, no word in the text could be a name, so
 * the model is skipped and the paste is decided by rules in milliseconds.
 *
 * It fires on: a capitalized or all-caps word that does not start a sentence;
 * initials; any word that is a known given name, in any case. It ignores
 * existing placeholders ([PERSON_1]) and a short list of common acronyms.
 * Measured recall on paste-sized pieces of two labelled corpora: every piece
 * that contained a name fired (472 of 472). Known gap: a first name typed
 * entirely in lowercase that is not in GIVEN_NAMES ("tell amity").
 */

import {GIVEN_NAMES} from './given-names';

const PLACEHOLDER = /\[[A-Z][A-Z0-9_]*\]/g;
// Email addresses and URLs are removed whole by the rules, so a name inside one
// needs no model.
const ADDRESS = /[\w.+-]+@[\w-]+(?:\.[\w-]+)+|https?:\/\/\S+|www\.\S+/gi;
// All-caps words that are common in ordinary requests and never a name on their
// own.
const ACRONYMS = new Set([
  'SSN',
  'SIN',
  'DOB',
  'ID',
  'IDS',
  'PIN',
  'URL',
  'URLS',
  'API',
  'APIS',
  'JSON',
  'HTML',
  'CSS',
  'PDF',
  'CSV',
  'SQL',
  'AI',
  'LLM',
  'FAQ',
  'TL',
  'DR',
  'OK',
  'USA',
  'US',
  'UK',
  'EU',
  'CEO',
  'CFO',
  'CTO',
  'HR',
  'IT',
  'Q1',
  'Q2',
  'Q3',
  'Q4',
  'AM',
  'PM',
  'ASAP',
  'FYI',
  'ETA',
  'N/A',
  'NA',
  'TBD',
  'IBAN',
  'SWIFT',
  'VAT',
  'GST',
  'HST',
  'IRS',
  'CRA',
  'MRN',
  'RN',
  'MD',
  'PHD',
  'CPA',
  'LLC',
  'INC',
  'LTD',
]);
const given = GIVEN_NAMES;
const TITLES = new Set([
  'mr',
  'mrs',
  'ms',
  'miss',
  'mx',
  'dr',
  'prof',
  'professor',
  'rev',
  'hon',
  'sir',
  'dame',
  'judge',
  'justice',
  'det',
  'sgt',
  'capt',
  'lt',
  'mme',
  'mlle',
  'herr',
  'frau',
  'sr',
  'sra',
  'dra',
  'lic',
]);
// Common words that start sentences. Any other capitalized first word ("Quillon
// will call") might be a name and sends the paste to the model.
const STARTERS = new Set(
  `a about above actually add after again all also although always am an and another any anyone anything are
around as ask at attached be because been before being below best both but by can cannot check could create dear define
describe did do does don't done draft during each edit either even every everyone everything example explain feel few
fill find first fix following for from generate get give go good great had has have having he hello help her here hers
hey hi his how however i if imagine in include instead is it its it's just keep last let let's list look make many may
maybe me might more most much must my never new next no none nor not note now of off ok okay on once one only or other
our out over overall perhaps please point provide put quick rather read really reply respond return review rewrite
same say second see send several she should show simplify since so some something sometimes sorry still subject
suggest summarize summarise sure take tell than thank thanks that the their them then there these they thing think
this those though three through thus to today tomorrow too translate two under unless until up update us use using
very was we well were what when where whether which while who why will with within without would write yes yesterday
yet you your yours email call contact compare analyze analyse calculate convert format organize organise outline plan
proofread rephrase shorten expand improve correct answer turn change remove replace extract identify discuss consider
assume given based regarding re attn attachment notes meeting agenda action items background context question
questions request goal summary overview introduction conclusion step steps task tasks finish start begin continue
avoid ensure focus try remember act pretend design build implement refactor debug test run install open close save
load print choose select pick rank sort group split merge combine clarify highlight mark label count estimate predict
recommend prepare schedule cancel confirm apply approve reject accept share post publish sign submit complete
evaluate assess critique grade score rate ignore disregard forget finally additionally furthermore moreover meanwhile otherwise therefore`.split(
    /\s+/,
  ),
);

/** Words that could be (part of) a name, with their positions in the input. */
export function nameCandidates(
  input: string,
): Array<{start: number; end: number; word: string}> {
  // Blank placeholders and addresses with spaces of the same length, so
  // positions stay valid.
  const blank = (s: string) => ' '.repeat(s.length);
  const text = input.replace(PLACEHOLDER, blank).replace(ADDRESS, blank);
  const found: Array<{start: number; end: number; word: string}> = [];
  for (const m of text.matchAll(/[\p{L}][\p{L}\p{N}'’.-]*/gu)) {
    const raw = m[0];
    const word = raw.replace(/[.'’-]+$/, '');
    const hit = () =>
      found.push({
        start: m.index!,
        end: m.index! + word.length || m.index! + raw.length,
        word: word || raw,
      });
    if (/^(?:\p{Lu}\.){1,3}$/u.test(raw)) {
      found.push({start: m.index!, end: m.index! + raw.length, word: raw});
      continue;
    } // initials: "D." "D.K."
    if (given.has(word.toLowerCase())) {
      hit();
      continue;
    } // "amity", "Mira"
    if (!/^\p{Lu}/u.test(word) || word === 'I') continue;
    // "Dr" in "Dr. Mira Calder": the name follows
    if (TITLES.has(word.toLowerCase())) continue;
    if (ACRONYMS.has(word.toUpperCase()) && word === word.toUpperCase()) {
      continue;
    }
    const before = text.slice(Math.max(0, m.index! - 4), m.index!);
    const sentenceStart =
      m.index === 0 || /(?:[.!?:;]\s+|\n\s*|^\s*|["“(]\s*)$/.test(before);
    if (!sentenceStart || !STARTERS.has(word.toLowerCase())) hit();
  }
  return found;
}

/**
 * Returns whether any word in `input` could be a name. When false, the
 * on-device model can be skipped.
 */
export function mightNameSomeone(input: string): boolean {
  return nameCandidates(input).length > 0;
}

/**
 * Possible names the rules have not already covered. When this is empty the
 * rules have accounted for every word that could be a name, so the on-device
 * model is unlikely to add one: the compliant counterpart of a
 * confidence-routed cascade (evaluation/ROUTING.md).
 */
export function unexplainedNameCandidates(
  input: string,
  covered: ReadonlyArray<{start: number; end: number}>,
) {
  return nameCandidates(input).filter(
    c => !covered.some(s => s.start <= c.start && s.end >= c.end),
  );
}
