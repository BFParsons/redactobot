/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {afterEach, beforeEach, expect, it, vi} from 'vitest';
import {readFileSync} from 'node:fs';
const fake = vi.hoisted(() => ({
  readiness: vi.fn(),
  prepare: vi.fn(),
  release: vi.fn(),
  send: vi.fn(),
}));
vi.mock('./model', () => ({
  readiness: fake.readiness,
  prepareModel: fake.prepare,
  releasePreparedModel: fake.release,
}));
vi.mock('../core/cloud-client', () => ({cloudSetupProblem: () => undefined}));
const flush = async () => {
  for (let i = 0; i < 20; i++) await Promise.resolve();
};
const status = () => document.querySelector('#status')!.textContent!;
const prepare = () => document.querySelector<HTMLButtonElement>('#prepare')!;
beforeEach(async () => {
  vi.resetModules();
  vi.clearAllMocks();
  vi.useFakeTimers();
  document.body.innerHTML = readFileSync('extension/options.html', 'utf8');
  fake.readiness.mockResolvedValue('available');
  fake.prepare.mockResolvedValue(undefined);
  fake.send.mockResolvedValue({ok: true});
  vi.stubGlobal('chrome', {
    runtime: {sendMessage: fake.send},
    storage: {
      sync: {get: async () => ({}), set: vi.fn()},
      onChanged: {addListener() {}},
    },
  });
});
afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});
it('prepares only the real scanner when the model is already installed', async () => {
  await import('./options');
  await flush();
  prepare().click();
  await flush();
  expect(fake.prepare).not.toHaveBeenCalled();
  expect(fake.send).toHaveBeenCalledWith({type: 'warm-scanner'});
  expect(status()).toMatch(/^Ready\./);
  expect(prepare().disabled).toBe(false);
});
it('retains initial-download setup but releases its temporary settings session', async () => {
  fake.readiness.mockResolvedValue('downloadable');
  await import('./options');
  await flush();
  prepare().click();
  await flush();
  expect(fake.prepare).toHaveBeenCalledWith(true, expect.any(Function));
  expect(fake.send).toHaveBeenCalledWith({type: 'warm-scanner'});
  expect(fake.release).toHaveBeenCalledOnce();
  expect(status()).toMatch(/^Ready\./);
});
it('shows elapsed time and a retryable error if the scanner never replies', async () => {
  fake.send.mockImplementationOnce(() => new Promise(() => {}));
  await import('./options');
  await flush();
  prepare().click();
  await flush();
  expect(document.querySelector<HTMLButtonElement>('#test-500')!.disabled).toBe(
    true,
  );
  await vi.advanceTimersByTimeAsync(10000);
  expect(status()).toContain('10 seconds elapsed');
  await vi.advanceTimersByTimeAsync(145000);
  expect(status()).toContain('did not respond');
  expect(prepare().disabled).toBe(false);
  prepare().click();
  await flush();
  expect(status()).toMatch(/^Ready\./);
});
it('preserves the actual scanner startup error', async () => {
  fake.send.mockResolvedValueOnce({
    ok: false,
    error: 'Chrome did not answer the on-device availability check.',
  });
  await import('./options');
  await flush();
  prepare().click();
  await flush();
  expect(status()).toContain('availability check');
  expect(prepare().disabled).toBe(false);
});
it('does not let the initial availability display overwrite a completed action', async () => {
  let resolve!: (value: string) => void;
  fake.readiness.mockImplementationOnce(
    () =>
      new Promise(r => {
        resolve = r;
      }),
  );
  await import('./options');
  prepare().click();
  await flush();
  expect(status()).toMatch(/^Ready\./);
  resolve('available');
  await flush();
  expect(status()).toMatch(/^Ready\./);
});
