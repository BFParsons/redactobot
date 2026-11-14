/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {afterEach, beforeEach, expect, it, vi} from 'vitest';
const fake = vi.hoisted(() => ({prompt: vi.fn(), create: vi.fn()}));
vi.mock('../core/firebase-local', () => ({
  firebaseLocalPrompt: (...args: any[]) => fake.prompt(...args),
}));
beforeEach(() => {
  vi.resetModules();
  vi.clearAllMocks();
  fake.create.mockResolvedValue({destroy() {}});
  fake.prompt.mockResolvedValue('[]');
  vi.stubGlobal('LanguageModel', {
    availability: async () => 'available',
    create: fake.create,
  });
});
afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
});
it('shares one text-free preload across callers and makes one Firebase request per short paste', async () => {
  const {prepareModel, extract} = await import('./model');
  await Promise.all([prepareModel(), prepareModel()]);
  const result = await extract(
    'A short sample from Avery.',
    new AbortController().signal,
    () => {},
  );
  expect(fake.create).toHaveBeenCalledOnce();
  expect(fake.prompt).toHaveBeenCalledOnce();
  expect(JSON.stringify(fake.create.mock.calls)).not.toContain(
    'A short sample',
  );
  expect(result.names.people).toEqual([]);
  expect(result.ambiguous).toEqual([]);
});
it('retains all extraction categories and indirect identifying links in the compact answer', async () => {
  const details = [
    'person',
    'company',
    'place',
    'health',
    'sensitive',
    'identifying',
    'uncertain',
  ].map(kind => `${kind}: sample ${kind}`);
  fake.prompt.mockResolvedValue(JSON.stringify(details));
  const {extract} = await import('./model');
  const result = await extract(
    'Sample from Avery',
    new AbortController().signal,
    () => {},
  );
  expect(result.names).toEqual({
    people: ['sample person'],
    companies: ['sample company'],
  });
  expect(result.topics).toMatchObject({
    places: ['sample place'],
    health: ['sample health'],
    sensitive: ['sample sensitive'],
  });
  expect(result.identifying[0].text).toBe('sample identifying');
  expect(result.ambiguous[0].text).toBe('sample uncertain');
});
it('does not load or call Nano for checks that only use local patterns', async () => {
  const {extract} = await import('./model');
  const timing = vi.fn();
  await extract(
    'avery@example.com, card 4111 1111 1111 1111',
    new AbortController().signal,
    () => {},
    timing,
    ['contact', 'payments'],
  );
  expect(fake.create).not.toHaveBeenCalled();
  expect(fake.prompt).not.toHaveBeenCalled();
  expect(timing).toHaveBeenCalledWith('inference', 0);
});
it('limits the model request and accepts only selected categories without recreating the warm base', async () => {
  fake.prompt.mockResolvedValue(
    JSON.stringify([
      'uncertain_person: Avery Bennett',
      'place: Seattle',
      'health: diabetes',
    ]),
  );
  const {extract} = await import('./model');
  const result = await extract(
    'Avery Bennett has diabetes in Seattle.',
    new AbortController().signal,
    () => {},
    undefined,
    ['names'],
  );
  expect(fake.prompt.mock.calls[0][0]).toContain(
    'Active categories: person, company.',
  );
  expect(fake.prompt.mock.calls[0][2]).toEqual({
    type: 'array',
    items: {
      type: 'string',
      pattern: '^(person|company|uncertain_person|uncertain_company): .+$',
    },
  });
  expect(result.names.people).toEqual(['Avery Bennett']);
  expect(result.topics.places).toEqual([]);
  expect(result.topics.health).toEqual([]);
  expect(result.ambiguous[0]).toMatchObject({
    text: 'Avery Bennett',
    kind: 'person',
  });
  await extract(
    'We met in Seattle.',
    new AbortController().signal,
    () => {},
    undefined,
    ['places'],
  );
  expect(fake.create).toHaveBeenCalledOnce();
});
it.each([
  '{}',
  '["unknown: name"]',
  '["person:"]',
  '["no tag here"]',
  '[{"text":"name","kind":"person"}]',
])('never treats an invalid answer as a clean paste: %s', async value => {
  fake.prompt.mockResolvedValue(value);
  const {extract} = await import('./model');
  await expect(
    extract('Sample from Avery', new AbortController().signal, () => {}),
  ).rejects.toThrow('incomplete');
  expect(fake.prompt).toHaveBeenCalledTimes(2);
});
it('cancels a paste while shared model preparation is still pending', async () => {
  let ready!: (session: object) => void;
  fake.create.mockImplementation(
    () =>
      new Promise(resolve => {
        ready = resolve;
      }),
  );
  const {extract, prepareModel} = await import('./model');
  const signal = new AbortController();
  const waiting = extract('Sample from Avery', signal.signal, () => {});
  const rejected = expect(waiting).rejects.toThrow();
  for (let n = 0; n < 12; n++) await Promise.resolve();
  signal.abort();
  await rejected;
  expect(fake.prompt).not.toHaveBeenCalled();
  ready({destroy() {}});
  await prepareModel();
});
it('does not leave the queue blocked when native inference ignores cancellation', async () => {
  fake.prompt.mockImplementationOnce(() => new Promise(() => {}));
  const {extract} = await import('./model');
  const controller = new AbortController();
  const waiting = extract('First, ask Avery', controller.signal, () => {});
  const rejected = expect(waiting).rejects.toThrow();
  for (let n = 0; n < 10; n++) await Promise.resolve();
  controller.abort();
  await rejected;
  await expect(
    extract('Second, ask Avery', new AbortController().signal, () => {}),
  ).resolves.toMatchObject({ambiguous: []});
});
it('checks the last chunk of a long paste instead of exiting after the first clean answer', async () => {
  const {extract} = await import('./model');
  const text = `${'word '.repeat(950)}Zelda`;
  await extract(text, new AbortController().signal, () => {});
  expect(fake.prompt).toHaveBeenCalledTimes(2);
  expect(fake.prompt.mock.calls[1][0]).toContain('Zelda');
});
it('bounds an unresponsive availability check and allows another startup attempt', async () => {
  vi.useFakeTimers();
  const availability = vi
    .fn()
    .mockImplementationOnce(() => new Promise(() => {}))
    .mockResolvedValue('available');
  vi.stubGlobal('LanguageModel', {availability, create: fake.create});
  const {prepareModel} = await import('./model');
  const failed = expect(prepareModel()).rejects.toThrow('availability check');
  await vi.advanceTimersByTimeAsync(10000);
  await failed;
  expect(fake.create).not.toHaveBeenCalled();
  await prepareModel();
  expect(fake.create).toHaveBeenCalledOnce();
});
it('reports startup timeout and disposes a session that arrives too late', async () => {
  vi.useFakeTimers();
  let resolve!: (value: any) => void;
  fake.create.mockImplementationOnce(
    () =>
      new Promise(r => {
        resolve = r;
      }),
  );
  const {prepareModel} = await import('./model');
  const failed = expect(prepareModel()).rejects.toThrow('5 minutes');
  await vi.advanceTimersByTimeAsync(300000);
  await failed;
  const destroy = vi.fn();
  resolve({destroy});
  await vi.advanceTimersByTimeAsync(0);
  expect(destroy).toHaveBeenCalledOnce();
  await prepareModel();
  expect(fake.create).toHaveBeenCalledTimes(2);
});
it('measures context only when the prompt might not fit', async () => {
  const measure = vi.fn(async (text: string) => text.length);
  fake.create.mockResolvedValue({
    destroy() {},
    contextWindow: 9216,
    contextUsage: 1500,
    measureContextUsage: measure,
  });
  const {extract} = await import('./model');
  await extract(
    'A short sample from Avery.',
    new AbortController().signal,
    () => {},
  );
  expect(measure).not.toHaveBeenCalled();
  expect(fake.prompt).toHaveBeenCalledOnce();
  await extract(
    'Avery ' + 'abcdefghij '.repeat(880),
    new AbortController().signal,
    () => {},
  );
  expect(measure).toHaveBeenCalled();
});
it('wakes an idle model with a text-free prompt, and skips it while the model is active', async () => {
  let now = 1_000_000;
  vi.spyOn(performance, 'now').mockImplementation(() => now);
  const touch = vi.fn(async (_text: string) => 'OK');
  const destroy = vi.fn();
  fake.create.mockResolvedValue({
    destroy() {},
    clone: async () => ({prompt: touch, destroy}),
  });
  const {extract, keepWarm, modelCold} = await import('./model');
  const labels: string[] = [];
  await extract(
    'A short sample from Avery.',
    new AbortController().signal,
    label => labels.push(label),
  );
  // The first use after loading touches the model and labels it as startup.
  expect(touch).toHaveBeenCalledOnce();
  expect(touch.mock.calls[0][0]).toBe('Reply with OK.');
  expect(
    labels.some(l => l.startsWith('Starting on-device AI. After a break')),
  ).toBe(true);
  expect(destroy).toHaveBeenCalledOnce();
  expect(modelCold()).toBe(false);
  now += 60_000;
  await keepWarm();
  await extract(
    'Another sample from Avery.',
    new AbortController().signal,
    () => {},
  );
  expect(touch).toHaveBeenCalledOnce();
  now += 91_000;
  expect(modelCold()).toBe(true);
  await keepWarm();
  expect(touch).toHaveBeenCalledTimes(2);
  // Document text never reaches the keepalive.
  expect(JSON.stringify(touch.mock.calls)).not.toContain('Avery');
});
it('skips the model, and any cold start, when it has nothing to add to the rules', async () => {
  const {extract, modelNeeded} = await import('./model');
  const timing = vi.fn();
  await extract(
    'Please rewrite this paragraph in plain language. Email avery@example.com.',
    new AbortController().signal,
    () => {},
    timing,
  );
  expect(fake.create).not.toHaveBeenCalled();
  expect(fake.prompt).not.toHaveBeenCalled();
  expect(timing).toHaveBeenCalledWith('inference', 0);
  const all = [
    'person',
    'company',
    'place',
    'health',
    'sensitive',
    'identifying',
    'uncertain',
  ];
  expect(
    modelNeeded('Could you tell Amity that her appointment moved?', all),
  ).toBe(true);
  expect(
    modelNeeded('My daughter has asthma and needs help at school.', all),
  ).toBe(true);
  expect(
    modelNeeded('My daughter has asthma and needs help at school.', [
      'person',
      'company',
    ]),
  ).toBe(false);
  expect(
    modelNeeded('Summarize [PERSON_1] and [COMPANY_1] in two lines.', all),
  ).toBe(false);
});
it('skips the model when the rules already removed every possible name', async () => {
  const {modelNeeded} = await import('./model');
  const all = [
    'person',
    'company',
    'place',
    'health',
    'sensitive',
    'identifying',
    'uncertain',
  ];
  const text = 'I met with Mira Calder to discuss the draft.';
  const at = text.indexOf('Mira Calder');
  expect(modelNeeded(text, all)).toBe(true); // a possible name
  expect(
    modelNeeded(text, all, [{start: at, end: at + 'Mira Calder'.length}]),
  ).toBe(false); // ...already covered
  expect(modelNeeded(text, all, [])).toBe(true); // nothing covered yet
  const titled = 'Dr. Mira Calder reviewed the draft.';
  const t = titled.indexOf('Mira');
  expect(
    modelNeeded(titled, all, [{start: t, end: t + 'Mira Calder'.length}]),
  ).toBe(false); // the title is not a name
  // health still goes to the model
  expect(modelNeeded('My daughter has asthma.', all, [])).toBe(true);
});
it('cancels a model start at once, destroys a late session, and starts fresh afterwards', async () => {
  let ready!: (session: any) => void;
  const late = {destroy: vi.fn()};
  fake.create.mockImplementationOnce(
    () =>
      new Promise(resolve => {
        ready = resolve;
      }),
  );
  const {prepareModel, cancelPrepare, modelState} = await import('./model');
  const first = prepareModel();
  await vi.waitFor(() => expect(fake.create).toHaveBeenCalledOnce());
  cancelPrepare();
  await expect(first).rejects.toThrow('canceled');
  expect(fake.create.mock.calls[0][0].signal.aborted).toBe(true);
  ready(late);
  await Promise.resolve();
  await Promise.resolve();
  expect(late.destroy).toHaveBeenCalled();
  expect(modelState().ready).toBe(false);
  await prepareModel();
  expect(fake.create).toHaveBeenCalledTimes(2);
  expect(modelState().ready).toBe(true);
});
