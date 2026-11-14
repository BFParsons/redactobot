/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';
import {
  judgeNames,
  promptFor,
  schemaFor,
  type Decider,
  type Question,
} from './decide';

const questions: Question[] = [
  {id: 'a', type: 'noul', instructions: 'Is a person named?'},
  {
    id: 'b',
    type: 'choice',
    instructions: '"Grace"',
    options: ['person', 'place', 'other'],
  },
  {id: 'c', type: 'score', instructions: 'How sensitive is this?', max: 4},
];

describe('typed questions for the on-device model', () => {
  it('builds a schema that allows only the permitted answers', () => {
    expect(schemaFor(questions)).toEqual({
      type: 'object',
      properties: {
        a: {type: 'boolean'},
        b: {type: 'string', enum: ['person', 'place', 'other']},
        c: {type: 'integer', minimum: 0, maximum: 4},
      },
      required: ['a', 'b', 'c'],
      additionalProperties: false,
    });
  });
  it('writes the document and one line per question', () => {
    const p = promptFor('Grace called.', questions);
    expect(p).toContain('Document:\n"""\nGrace called.\n"""');
    expect(p).toContain('a: Is a person named? (true | false)');
    expect(p).toContain('b: "Grace" (person | place | other)');
    expect(p).toContain('c: How sensitive is this? (0 to 4)');
  });
});

describe('labelling candidate names', () => {
  // A stand-in for the model: it knows three words.
  const known: Record<string, string> = {
    Grace: 'person',
    Wenatchee: 'place',
    Zelle: 'other',
  };
  const decide: Decider = async (_state, _preamble, qs) =>
    Object.fromEntries(
      qs.map(q => [
        q.id,
        known[JSON.parse(q.instructions) as string] ?? 'other',
      ]),
    );

  it('returns a label per candidate and batches long lists', async () => {
    const candidates = [
      'Grace',
      'Wenatchee',
      'Zelle',
      ...Array.from({length: 30}, (_, i) => `Word${i}`),
    ];
    const out = await judgeNames('text', candidates, decide, 15);
    expect(out.requests).toBe(3);
    expect(out.labels.get('Grace')).toBe('person');
    expect(out.labels.get('Wenatchee')).toBe('place');
    expect(out.labels.get('Zelle')).toBe('other');
    expect(out.labels.size).toBe(33);
  });
  it('leaves a batch unlabelled when the model fails, and ignores answers outside the options', async () => {
    const failing: Decider = async () => {
      throw new Error('model failed');
    };
    expect((await judgeNames('text', ['Grace'], failing)).failures).toBe(1);
    const odd: Decider = async (_s, _p, qs) =>
      Object.fromEntries(qs.map(q => [q.id, 'maybe']));
    expect((await judgeNames('text', ['Grace'], odd)).labels.size).toBe(0);
  });
});
