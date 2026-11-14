/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Typed questions answered by the on-device model: a small
 * "decisions" layer.
 *
 * The idea (the same shape as Jev and the Gemini Decisions API): instead of
 * asking a model to write out what it finds, ordinary code finds candidates and
 * the model answers closed questions about them: yes/no, one of a fixed set, or
 * a score. Here the questions go to Gemini Nano through Chrome's native Prompt
 * API, with a JSON schema that only allows the permitted answers. Raw text
 * never leaves the device.
 *
 * What this does NOT give: calibrated probabilities. Chrome's on-device model
 * returns text, not scores, so an answer is a single choice. Treat it as a
 * vote, not a measurement.
 *
 * EXPERIMENTAL: used by the evaluation harness (tools/evaluation) to compare
 * against the "write out the names" request. Not yet used by the app.
 */

/**
 * A closed question for the model: yes or no ('noul'), one of `options`
 * ('choice'), or a whole number from 0 to `max` ('score').
 */
export type Question =
  | {id: string; type: 'noul'; instructions: string}
  | {
      id: string;
      type: 'choice';
      instructions: string;
      options: readonly string[];
    }
  | {id: string; type: 'score'; instructions: string; max: number};

/** The answer to one Question: a boolean, the chosen option, or a score. */
export type Answer = boolean | string | number;

/** Something that can answer a batch of questions about a piece of text. */
export type Decider = (
  state: string,
  preamble: string,
  questions: Question[],
) => Promise<Record<string, Answer>>;

/**
 * The JSON schema that restricts the model to one permitted answer per
 * question.
 */
export function schemaFor(questions: Question[]) {
  const properties: Record<string, object> = {};
  for (const q of questions) {
    properties[q.id] =
      q.type === 'noul'
        ? {type: 'boolean'}
        : q.type === 'choice'
          ? {type: 'string', enum: [...q.options]}
          : {type: 'integer', minimum: 0, maximum: q.max};
  }
  return {
    type: 'object',
    properties,
    required: questions.map(q => q.id),
    additionalProperties: false,
  };
}

/** The request text: the document, then one line per question. */
export function promptFor(state: string, questions: Question[]): string {
  const lines = questions.map(
    q =>
      `${q.id}: ${q.instructions}` +
      (q.type === 'choice'
        ? ` (${q.options.join(' | ')})`
        : q.type === 'score'
          ? ` (0 to ${q.max})`
          : ' (true | false)'),
  );
  return `Document:\n"""\n${state}\n"""\n\nQuestions:\n${lines.join('\n')}`;
}

/** The labels the model may give a candidate phrase. */
export const NAME_LABELS = [
  'person',
  'organization',
  'place',
  'other',
] as const;
/** What a candidate phrase is, as labelled by the model. */
export type NameLabel = (typeof NAME_LABELS)[number];

const NAME_PREAMBLE = `You label phrases taken from a confidential document.
For each numbered phrase, say what it is IN THIS DOCUMENT:
person: a person's name, including a first name, surname, nickname or initials on their own.
organization: a company, firm, bank, school, hospital, agency, trust or other named body.
place: a city, town, county, neighbourhood or named building.
other: anything else, such as an ordinary word, a title, a month, a product or a legal term.
Answer every question. Respond only with JSON.`;

/**
 * Ask the model what each candidate phrase is. Candidates are sent in batches
 * so one request stays short. Returns a label per candidate; a batch that fails
 * twice is left unlabelled.
 */
export async function judgeNames(
  chunk: string,
  candidates: string[],
  decide: Decider,
  batchSize = 15,
) {
  const labels = new Map<string, NameLabel>();
  let requests = 0;
  let failures = 0;
  for (let i = 0; i < candidates.length; i += batchSize) {
    const batch = candidates.slice(i, i + batchSize);
    const questions: Question[] = batch.map((c, n) => ({
      id: `p${n + 1}`,
      type: 'choice',
      instructions: JSON.stringify(c),
      options: NAME_LABELS,
    }));
    requests++;
    try {
      const answers = await decide(chunk, NAME_PREAMBLE, questions);
      batch.forEach((c, n) => {
        const a = answers[`p${n + 1}`];
        if (
          typeof a === 'string' &&
          (NAME_LABELS as readonly string[]).includes(a)
        ) {
          labels.set(c, a as NameLabel);
        }
      });
    } catch {
      failures++;
    }
  }
  return {labels, requests, failures};
}
