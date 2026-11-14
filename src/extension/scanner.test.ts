/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {afterEach, beforeEach, expect, it, vi} from 'vitest';
import {PASTE_500_TEST_TEXT} from './fixtures';
const fake = vi.hoisted(() => ({extract: vi.fn()}));
vi.mock('./model', () => ({
  extract: (...args: any[]) => fake.extract(...args),
  prepareModel: async () => {},
  keepWarm: async () => {},
  readiness: async () => 'available',
  modelState: () => ({ready: true, preparing: false}),
}));
let receive: (message: any, sender: any, reply: (value: any) => void) => void;
let worker: any;
let sent: any[];
const flush = async () => {
  for (let i = 0; i < 20; i++) await Promise.resolve();
};
const message = (value: any) =>
  receive({target: 'scanner', ...value}, {id: 'test'}, () => {});
const evidence = {
  names: {people: [], companies: []},
  topics: {},
  ambiguous: [],
  identifying: [],
};
beforeEach(async () => {
  vi.resetModules();
  vi.clearAllMocks();
  vi.useFakeTimers();
  sent = [];
  vi.stubGlobal('chrome', {
    runtime: {
      id: 'test',
      onMessage: {
        addListener: (fn: typeof receive) => {
          receive = fn;
        },
      },
      sendMessage: async (value: any) => {
        sent.push(value);
      },
    },
  });
  vi.stubGlobal(
    'Worker',
    class {
      onmessage?: (event: any) => void;
      onerror?: () => void;
      constructor() {
        // oxlint-disable-next-line typescript/no-this-alias -- the test drives this instance later.
        worker = this;
      }
      postMessage = vi.fn((m: any) => {
        Promise.resolve().then(() =>
          this.onmessage?.({
            data: {id: m.id, value: m.type === 'local' ? [] : {complete: true}},
          }),
        );
      });
    },
  );
  fake.extract.mockResolvedValue(evidence);
  await import('./scanner');
});
afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

it('runs a pattern-only paste while another paste is waiting on Nano', async () => {
  fake.extract.mockImplementationOnce(() => new Promise(() => {}));
  message({
    type: 'scan',
    id: 'slow',
    text: 'A long model scan.',
    prefix: 'TEST',
  });
  await flush();
  message({
    type: 'scan',
    id: 'fast',
    text: 'avery@example.com',
    prefix: 'TEST',
    categories: ['contact'],
  });
  await flush();
  expect(sent.filter(m => m.type === 'result').map(m => m.id)).toEqual([
    'fast',
  ]);
  const requests = worker.postMessage.mock.calls
    .map((c: any[]) => c[0])
    .filter((m: any) => m.text === 'avery@example.com');
  expect(requests).toHaveLength(2);
  expect(requests.every((m: any) => m.categories.join() === 'contact')).toBe(
    true,
  );
  message({type: 'cancel', id: 'slow'});
});

it('includes queue time in the deadline for a 500-word paste over 4,000 characters', async () => {
  fake.extract.mockImplementation(() => new Promise(() => {}));
  message({
    type: 'scan',
    id: 'first',
    text: 'longword '.repeat(500),
    prefix: 'TEST',
  });
  await flush();
  await vi.advanceTimersByTimeAsync(5000);
  message({
    type: 'scan',
    id: 'second',
    text: 'anotherword '.repeat(500),
    prefix: 'TEST',
  });
  await flush();
  await vi.advanceTimersByTimeAsync(25000);
  expect(sent.filter(m => m.type === 'failed').map(m => m.id)).toEqual([
    'first',
  ]);
  await vi.advanceTimersByTimeAsync(5000);
  expect(sent.filter(m => m.type === 'failed').map(m => m.id)).toEqual([
    'first',
    'second',
  ]);
  expect(sent.filter(m => m.type === 'result')).toEqual([]);
  expect(fake.extract).toHaveBeenCalledTimes(2);
});

it('distinguishes slow model startup from a slow document scan', async () => {
  fake.extract.mockImplementation((_text, _signal, progress) => {
    progress('Starting on-device AI…');
    return new Promise(() => {});
  });
  message({type: 'scan', id: 'cold', text: 'A sample.', prefix: 'TEST'});
  await flush();
  // Waking a model Chrome unloaded gets the 5-minute startup budget, not the
  // scan budget.
  await vi.advanceTimersByTimeAsync(30000);
  expect(sent.filter(m => m.type === 'failed')).toEqual([]);
  await vi.advanceTimersByTimeAsync(270000);
  expect(sent.find(m => m.type === 'failed').label).toContain('still starting');
});

it('cancels an unresponsive scan and starts the next without accepting a late result', async () => {
  let resolve!: (value: any) => void;
  fake.extract.mockImplementationOnce(
    () =>
      new Promise(r => {
        resolve = r;
      }),
  );
  message({type: 'scan', id: 'first', text: 'Old text.', prefix: 'TEST'});
  await flush();
  message({type: 'cancel', id: 'first'});
  message({type: 'scan', id: 'second', text: 'New text.', prefix: 'TEST'});
  await flush();
  resolve(evidence);
  await flush();
  expect(sent.filter(m => m.type === 'result').map(m => m.id)).toEqual([
    'second',
  ]);
  expect(sent.filter(m => m.type === 'failed')).toEqual([]);
});

it('never reports a completed scan if cancellation happens during final local checks', async () => {
  let pending: any;
  worker.postMessage.mockImplementation((m: any) => {
    if (m.type === 'local') {
      Promise.resolve().then(() =>
        worker.onmessage({data: {id: m.id, value: []}}),
      );
    } else {
      pending = m;
    }
  });
  message({type: 'scan', id: 'late', text: 'A sample.', prefix: 'TEST'});
  await flush();
  expect(pending.type).toBe('report');
  message({type: 'cancel', id: 'late'});
  await flush();
  worker.onmessage({data: {id: pending.id, value: {complete: true}}});
  await flush();
  expect(sent.some(m => m.type === 'result')).toBe(false);
});
it('uses a fixed 500-word diagnostic including identifiers at the end, never caller text', async () => {
  const reply = vi.fn();
  receive(
    {target: 'scanner', type: 'self-test-500', text: 'Untrusted caller text'},
    {id: 'test'},
    reply,
  );
  await flush();
  expect(PASTE_500_TEST_TEXT.split(/\s+/)).toHaveLength(500);
  expect(fake.extract.mock.calls[0][0]).toBe(PASTE_500_TEST_TEXT);
  expect(PASTE_500_TEST_TEXT).toMatch(
    /Avery Bennett.*avery@example.com.*42\.$/,
  );
  expect(reply.mock.calls[0][0].ok).toBe(true);
});
it('preempts a hung diagnostic when a real paste arrives, including late diagnostic results', async () => {
  let resolve!: (value: any) => void;
  fake.extract.mockImplementationOnce(
    () =>
      new Promise(r => {
        resolve = r;
      }),
  );
  const reply = vi.fn();
  receive({target: 'scanner', type: 'self-test-500'}, {id: 'test'}, reply);
  await flush();
  message({type: 'scan', id: 'live', text: 'Actual paste.', prefix: 'TEST'});
  await flush();
  expect(sent.filter(m => m.type === 'result').map(m => m.id)).toEqual([
    'live',
  ]);
  expect(reply).toHaveBeenCalledOnce();
  expect(reply.mock.calls[0][0]).toMatchObject({ok: false});
  resolve(evidence);
  await flush();
  expect(reply).toHaveBeenCalledOnce();
});
it('refuses a diagnostic while a paste is running instead of adding another blocker', async () => {
  fake.extract.mockImplementationOnce(() => new Promise(() => {}));
  message({type: 'scan', id: 'live', text: 'Actual paste.', prefix: 'TEST'});
  await flush();
  const reply = vi.fn();
  receive({target: 'scanner', type: 'self-test'}, {id: 'test'}, reply);
  await flush();
  expect(reply.mock.calls[0][0]).toMatchObject({ok: false});
  expect(fake.extract).toHaveBeenCalledOnce();
  message({type: 'cancel', id: 'live'});
  await flush();
});
it('exposes queue stages without any pasted text or model findings', async () => {
  fake.extract.mockImplementationOnce(() => new Promise(() => {}));
  message({
    type: 'scan',
    id: 'live',
    text: 'Fictional private note.',
    prefix: 'TEST',
  });
  await flush();
  const reply = vi.fn();
  receive({target: 'scanner', type: 'diagnostics'}, {id: 'test'}, reply);
  expect(reply.mock.calls[0][0].active.kind).toBe('paste');
  expect(JSON.stringify(reply.mock.calls[0][0])).not.toContain('Fictional');
  message({type: 'cancel', id: 'live'});
  await flush();
});

it('ignores commands from a content script, which shares the extension id', async () => {
  const reply = vi.fn();
  const contentScript = {
    id: 'test',
    origin: 'https://chatgpt.com',
    url: 'https://chatgpt.com/c/1',
    tab: {id: 3},
  };
  receive({target: 'scanner', type: 'diagnostics'}, contentScript, reply);
  receive(
    {
      target: 'scanner',
      type: 'scan',
      id: 'x',
      text: 'Avery Bennett',
      prefix: 'T',
    },
    contentScript,
    reply,
  );
  await flush();
  expect(reply).not.toHaveBeenCalled();
  expect(fake.extract).not.toHaveBeenCalled();
});
