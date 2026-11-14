/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {afterEach, beforeEach, expect, it, vi} from 'vitest';
const fake = vi.hoisted(() => ({
  model: undefined as any,
  generate: vi.fn(),
  getModel: vi.fn(),
}));
vi.mock('firebase/ai', () => ({
  GoogleAIBackend: class {},
  getAI: vi.fn(),
  InferenceMode: {ONLY_ON_DEVICE: 'only_on_device'},
  InferenceSource: {ON_DEVICE: 'on_device'},
  getGenerativeModel: (...args: any[]) => {
    fake.getModel(...args);
    return fake.model;
  },
}));
beforeEach(() => {
  vi.resetModules();
  vi.clearAllMocks();
  vi.stubGlobal('LanguageModel', {});
  fake.model = {generateContent: fake.generate};
});
afterEach(() => vi.unstubAllGlobals());
it('refuses an SDK build without a Chrome adapter before handing it any raw text', async () => {
  const {firebaseLocalPrompt} = await import('./firebase-local');
  await expect(
    firebaseLocalPrompt(
      'Raw fictional note',
      'System',
      {},
      new AbortController().signal,
    ),
  ).rejects.toThrow('cannot guarantee');
  expect(fake.generate).not.toHaveBeenCalled();
});
it('locks local routing and destroys the native session after an error', async () => {
  const adapter = {
    mode: 'only_on_device',
    isAvailable() {},
    generateContent() {},
    oldSession: {destroy: vi.fn()},
  };
  const destroy = adapter.oldSession.destroy;
  fake.model.chromeAdapter = adapter;
  fake.generate.mockRejectedValueOnce(new Error('Local failure'));
  const {firebaseLocalPrompt} = await import('./firebase-local');
  await expect(
    firebaseLocalPrompt(
      'Raw fictional note',
      'System',
      {},
      new AbortController().signal,
    ),
  ).rejects.toThrow('Local failure');
  expect(destroy).toHaveBeenCalledOnce();
  expect(Object.getOwnPropertyDescriptor(adapter, 'mode')?.writable).toBe(
    false,
  );
  expect(
    Object.getOwnPropertyDescriptor(fake.model, 'chromeAdapter')?.writable,
  ).toBe(false);
});
it('refuses an unexpected inference source and an already canceled request', async () => {
  fake.model.chromeAdapter = {
    mode: 'only_on_device',
    isAvailable() {},
    generateContent() {},
  };
  fake.generate.mockResolvedValueOnce({
    response: {inferenceSource: 'in_cloud', text: () => '{}'},
  });
  const {firebaseLocalPrompt} = await import('./firebase-local');
  await expect(
    firebaseLocalPrompt(
      'Raw fictional note',
      'System',
      {},
      new AbortController().signal,
    ),
  ).rejects.toThrow('Unexpected');
  const canceled = new AbortController();
  canceled.abort();
  await expect(
    firebaseLocalPrompt('Raw fictional note', 'System', {}, canceled.signal),
  ).rejects.toThrow();
  expect(fake.generate).toHaveBeenCalledOnce();
});
it('refuses an incompatible warm-session adapter before submitting any document', async () => {
  fake.model.chromeAdapter = {
    mode: 'only_on_device',
    isAvailable() {},
    generateContent() {},
  };
  const prepared = {clone: vi.fn()};
  const {firebaseLocalPrompt} = await import('./firebase-local');
  await expect(
    firebaseLocalPrompt(
      'Raw fictional note',
      'System',
      {},
      new AbortController().signal,
      prepared,
    ),
  ).rejects.toThrow('prepared local session');
  expect(fake.generate).not.toHaveBeenCalled();
  expect(prepared.clone).not.toHaveBeenCalled();
});
