/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {afterEach, expect, it, vi} from 'vitest';
const prompt = vi.hoisted(() => vi.fn(async () => '{}'));
vi.mock('./firebase-local', () => ({firebaseLocalPrompt: prompt}));
import {LocalModel} from './local-model';
afterEach(() => {
  Reflect.deleteProperty(globalThis, 'LanguageModel');
});
it('gives every prompt a clone of the one warm, text-free session', async () => {
  const base = {clone: vi.fn(), prompt: vi.fn(), destroy: vi.fn()};
  const create = vi.fn(async () => base);
  (globalThis as any).LanguageModel = {
    availability: async () => 'available',
    create,
  };
  const model = new LocalModel('system', {});
  await model.prompt('one');
  await model.prompt('two');
  expect(create).toHaveBeenCalledOnce();
  expect(prompt.mock.calls.map(c => (c as unknown[])[4])).toEqual([base, base]);
  expect(base.prompt).not.toHaveBeenCalled();
});
it('wakes an idle model once with a text-free prompt, then only after another idle period', async () => {
  let now = 5_000_000;
  vi.spyOn(performance, 'now').mockImplementation(() => now);
  const touch = vi.fn(async (_text: string, _options: object) => 'OK');
  const base = {
    clone: vi.fn(async () => ({
      clone: vi.fn(),
      prompt: touch,
      destroy: vi.fn(),
    })),
    prompt: vi.fn(),
    destroy: vi.fn(),
  };
  (globalThis as any).LanguageModel = {
    availability: async () => 'available',
    create: async () => base,
  };
  const model = new LocalModel('system', {});
  await Promise.all([model.wake(), model.wake()]);
  expect(touch).toHaveBeenCalledOnce();
  expect(touch.mock.calls[0][0]).toBe('Reply with OK.');
  now += 30_000;
  await model.wake();
  expect(touch).toHaveBeenCalledOnce();
  now += 91_000;
  await model.wake();
  expect(touch).toHaveBeenCalledTimes(2);
});
