/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {afterEach, beforeEach, expect, it, vi} from 'vitest';
import {NO_TOPICS} from '../core/redact';
import {makeReport} from './policy';
import {CLOUD_TEST_TEXT} from './fixtures';
const cloud = vi.hoisted(() => ({cleanup: vi.fn(), problem: vi.fn()}));
vi.mock('../core/cloud-client', () => ({
  cleanupCloud: (...args: any[]) => cloud.cleanup(...args),
  cloudSetupProblem: () => cloud.problem(),
}));
function event() {
  const listeners: Array<(...args: any[]) => any> = [];
  return {
    addListener: (fn: (...args: any[]) => any) => listeners.push(fn),
    emit: (...args: any[]) => listeners.map(fn => fn(...args)),
  };
}
let api: any;
let owner: ReturnType<typeof port>;
function port(name: string, path = 'https://chatgpt.com/', tabId = 7) {
  return {
    name,
    sender: {id: 'test-extension', url: path, tab: {id: tabId}, frameId: 0},
    postMessage: vi.fn(),
    disconnect: vi.fn(),
    onMessage: event(),
    onDisconnect: event(),
  };
}
const empty = {people: [], companies: []};
const flush = async () => {
  for (let n = 0; n < 12; n++) await Promise.resolve();
};
beforeEach(async () => {
  vi.resetModules();
  vi.clearAllMocks();
  vi.useFakeTimers();
  api = {
    runtime: {
      id: 'test-extension',
      getURL: (p: string) => `chrome-extension://test-extension/${p}`,
      getContexts: vi.fn().mockResolvedValue([{}]),
      onConnect: event(),
      onMessage: event(),
      onInstalled: event(),
      onStartup: event(),
      sendMessage: vi.fn().mockResolvedValue({accepted: true}),
      openOptionsPage: vi.fn(),
    },
    storage: {sync: {get: vi.fn().mockResolvedValue({cloudCleanup: true})}},
    action: {onClicked: event()},
    tabs: {onRemoved: event()},
    windows: {create: vi.fn()},
  };
  vi.stubGlobal('chrome', api);
  cloud.problem.mockReturnValue(undefined);
  cloud.cleanup.mockImplementation(async (input: any) =>
    (await import('../core/cloud-gate')).applyCloudCleanup(input, {
      complete: true,
      findings: [],
    }),
  );
  await import('./background');
  owner = port('paste-guard');
  api.runtime.onConnect.emit(owner);
});
afterEach(() => {
  owner.onDisconnect.emit();
  vi.useRealTimers();
  vi.unstubAllGlobals();
});
async function start(text: string) {
  owner.onMessage.emit({type: 'start', id: 'paste', text, theme: {}});
  await flush();
  return api.runtime.sendMessage.mock.calls
    .map((c: any) => c[0])
    .filter((m: any) => m.type === 'scan')
    .at(-1);
}
async function finish(scan: any, report: any) {
  api.runtime.onMessage.emit(
    {target: 'background', type: 'result', id: scan.id, report},
    {
      id: 'test-extension',
      url: 'chrome-extension://test-extension/scanner.html',
    },
    () => {},
  );
  await flush();
}
function review() {
  const message = owner.postMessage.mock.calls
    .map(c => c[0])
    .filter(m => m.type === 'review')
    .at(-1);
  const frame = port(
    'review:' + message.token,
    'chrome-extension://test-extension/review.html',
  );
  api.runtime.onConnect.emit(frame);
  return frame;
}
const inserted = () =>
  owner.postMessage.mock.calls.map(c => c[0]).filter(m => m.type === 'insert');
it('reads categories from trusted storage, pauses cloud cleanup and inserts the selected local result', async () => {
  api.storage.sync.get.mockResolvedValue({
    cloudCleanup: true,
    pasteCategories: ['contact'],
  });
  owner.onMessage.emit({
    type: 'start',
    id: 'paste',
    text: 'Avery Bennett: avery@example.com',
    theme: {},
    categories: [],
  });
  await flush();
  const scan = api.runtime.sendMessage.mock.calls
    .map((c: any) => c[0])
    .find((m: any) => m.type === 'scan');
  expect(scan.categories).toEqual(['contact']);
  await finish(
    scan,
    makeReport(
      scan.text,
      empty,
      NO_TOPICS,
      [],
      scan.prefix,
      true,
      undefined,
      [],
      scan.categories,
    ),
  );
  expect(cloud.cleanup).not.toHaveBeenCalled();
  expect(inserted()[0].cleaned).toContain('Avery Bennett:');
  expect(inserted()[0].cleaned).not.toContain('avery@example.com');
});
it('keeps the same category snapshot when a held paste is edited and scanned again', async () => {
  api.storage.sync.get.mockResolvedValue({
    cloudCleanup: true,
    pasteCategories: ['names', 'contact'],
  });
  const scan = await start('Avery Bennett: avery@example.com');
  const report = makeReport(
    scan.text,
    empty,
    NO_TOPICS,
    [],
    scan.prefix,
    true,
    undefined,
    [],
    scan.categories,
  );
  await finish(scan, {...report, needsReview: true});
  api.storage.sync.get.mockResolvedValue({pasteCategories: ['contact']});
  review().onMessage.emit({
    type: 'approve',
    edited: 'Revised: Avery Bennett, avery@example.com',
  });
  await flush();
  const next = api.runtime.sendMessage.mock.calls
    .map((c: any) => c[0])
    .filter((m: any) => m.type === 'scan')
    .at(-1);
  expect(next.categories).toEqual(['names', 'contact']);
  expect(next.id).not.toBe(scan.id);
});
it('does not preload Nano for a pattern-only selection', async () => {
  api.storage.sync.get.mockResolvedValue({
    pasteCategories: ['contact', 'payments'],
  });
  api.runtime.onStartup.emit();
  await flush();
  owner.onMessage.emit({type: 'prepare'});
  await flush();
  expect(api.runtime.sendMessage).not.toHaveBeenCalled();
});
it('uses saved categories for local settings diagnostics', async () => {
  api.storage.sync.get.mockResolvedValue({pasteCategories: ['contact']});
  api.runtime.onMessage.emit(
    {type: 'test-general'},
    {
      id: 'test-extension',
      url: 'chrome-extension://test-extension/options.html',
    },
    vi.fn(),
  );
  await flush();
  expect(api.runtime.sendMessage).toHaveBeenCalledWith({
    target: 'scanner',
    type: 'self-test-general',
    categories: ['contact'],
  });
});
it('does not load the model at Chrome startup: Redactobot starts switched off', async () => {
  api.runtime.onStartup.emit();
  await flush();
  expect(api.runtime.sendMessage).not.toHaveBeenCalled();
});
it('loads the model at Chrome startup when that option is on', async () => {
  api.storage.sync.get.mockResolvedValue({preloadAtStartup: true});
  api.runtime.onStartup.emit();
  await flush();
  expect(api.runtime.sendMessage).toHaveBeenCalledWith({
    target: 'scanner',
    type: 'prepare',
  });
  expect(cloud.cleanup).not.toHaveBeenCalled();
  expect(inserted()).toEqual([]);
});
it('cancels a model start when the only tab waiting for it switches off', async () => {
  api.storage.sync.get.mockResolvedValue({});
  api.runtime.sendMessage.mockImplementation(() => new Promise(() => {}));
  owner.onMessage.emit({type: 'prepare'});
  await flush();
  expect(api.runtime.sendMessage).toHaveBeenCalledWith({
    target: 'scanner',
    type: 'prepare',
  });
  owner.onMessage.emit({type: 'cancel-prepare'});
  await flush();
  expect(api.runtime.sendMessage).toHaveBeenCalledWith({
    target: 'scanner',
    type: 'cancel-prepare',
  });
});
it('does not preload when paste checking is disabled on every supported site', async () => {
  api.storage.sync.get.mockResolvedValue({
    sites: {chatgpt: false, claude: false, gemini: false},
  });
  api.runtime.onStartup.emit();
  await flush();
  expect(api.runtime.sendMessage).not.toHaveBeenCalled();
});
it('does not load the model or open settings on extension update', async () => {
  api.runtime.onInstalled.emit({reason: 'update'});
  await flush();
  expect(api.runtime.sendMessage).not.toHaveBeenCalled();
  expect(api.runtime.openOptionsPage).not.toHaveBeenCalled();
});
it('shows retry instead of waiting indefinitely if the offscreen scanner did not accept the job', async () => {
  api.runtime.sendMessage.mockResolvedValue(undefined);
  await start('A short paragraph.');
  expect(
    owner.postMessage.mock.calls.map(c => c[0]).some(m => m.type === 'failed'),
  ).toBe(true);
  expect(inserted()).toEqual([]);
});
it('ignores a late scan result after the scanner reports a timeout', async () => {
  const text = 'A short paragraph.';
  const scan = await start(text);
  api.runtime.onMessage.emit(
    {target: 'background', type: 'failed', id: scan.id},
    {
      id: 'test-extension',
      url: 'chrome-extension://test-extension/scanner.html',
    },
    () => {},
  );
  await finish(scan, makeReport(text, empty, NO_TOPICS, [], scan.prefix));
  expect(cloud.cleanup).not.toHaveBeenCalled();
  expect(inserted()).toEqual([]);
});
it('times out a silent scanner independently and rejects any late result', async () => {
  api.runtime.sendMessage.mockImplementation((message: any) =>
    message.type === 'scan'
      ? new Promise(() => {})
      : Promise.resolve({ok: true}),
  );
  const text = 'longword '.repeat(500);
  const scan = await start(text);
  // The background is only a backstop behind the scanner's own wake and scan
  // deadlines.
  await vi.advanceTimersByTimeAsync(31000);
  expect(
    owner.postMessage.mock.calls.map(c => c[0]).some(m => m.type === 'failed'),
  ).toBe(false);
  await vi.advanceTimersByTimeAsync(300000);
  expect(
    owner.postMessage.mock.calls.map(c => c[0]).some(m => m.type === 'failed'),
  ).toBe(true);
  await finish(scan, makeReport(text, empty, NO_TOPICS, [], scan.prefix));
  expect(inserted()).toEqual([]);
  expect(cloud.cleanup).not.toHaveBeenCalled();
});
it('stops the local deadline when a complete result enters the cloud stage', async () => {
  cloud.cleanup.mockImplementationOnce(() => new Promise(() => {}));
  const text = 'A fictional sample.';
  const scan = await start(text);
  await finish(scan, makeReport(text, empty, NO_TOPICS, [], scan.prefix));
  await vi.advanceTimersByTimeAsync(31000);
  expect(
    owner.postMessage.mock.calls.map(c => c[0]).some(m => m.type === 'failed'),
  ).toBe(false);
});
it('sends a scrubbed input to cloud and inserts the final scrubbed result', async () => {
  const text = 'Contact avery@example.com. Diagnosis: diabetes.';
  const scan = await start(text);
  await finish(
    scan,
    makeReport(
      text,
      empty,
      {...NO_TOPICS, health: ['diabetes']},
      [],
      scan.prefix,
    ),
  );
  await flush();
  expect(cloud.cleanup).toHaveBeenCalledOnce();
  const input = cloud.cleanup.mock.calls[0][0];
  expect(input.text).not.toContain('avery@example.com');
  expect(input.text).toContain('diabetes');
  expect(inserted()).toHaveLength(1);
  expect(inserted()[0].cleaned).not.toMatch(/avery@example.com|diabetes/);
});
it('holds incomplete scans even after review approval', async () => {
  const text = 'Contact avery@example.com.';
  const scan = await start(text);
  await finish(
    scan,
    makeReport(text, empty, NO_TOPICS, [], scan.prefix, false),
  );
  review().onMessage.emit({type: 'approve', kept: []});
  await flush();
  expect(cloud.cleanup).not.toHaveBeenCalled();
  expect(inserted()).toEqual([]);
});
it('rescans edits and rejects stale results instead of sending or inserting edited text', async () => {
  const text = 'I have diabetes.';
  const scan = await start(text);
  await finish(scan, makeReport(text, empty, NO_TOPICS, [], scan.prefix));
  const frame = review();
  frame.onMessage.emit({
    type: 'approve',
    edited: 'Reach new@example.com.',
    kept: [],
  });
  await flush();
  const scans = api.runtime.sendMessage.mock.calls
    .map((c: any) => c[0])
    .filter((m: any) => m.type === 'scan');
  expect(scans).toHaveLength(2);
  expect(scans[1].id).not.toBe(scan.id);
  await finish(
    scan,
    makeReport('Nothing sensitive.', empty, NO_TOPICS, [], scan.prefix),
  );
  expect(cloud.cleanup).not.toHaveBeenCalled();
  expect(inserted()).toEqual([]);
  await finish(
    scans[1],
    makeReport(scans[1].text, empty, NO_TOPICS, [], scans[1].prefix),
  );
  await flush();
  expect(cloud.cleanup.mock.calls[0][0].text).not.toContain('new@example.com');
});
it('keeps identity removal mandatory even when approval requests keeping it', async () => {
  api.storage.sync.get.mockResolvedValue({cloudCleanup: false});
  const text = 'Alex called.';
  const scan = await start(text);
  const r = makeReport(
    text,
    empty,
    {...NO_TOPICS, names: ['Alex']},
    [],
    scan.prefix,
  );
  await finish(scan, r);
  review().onMessage.emit({type: 'approve', kept: r.findings.map(d => d.id)});
  await flush();
  expect(inserted()[0].cleaned).not.toContain('Alex');
  expect(cloud.cleanup).not.toHaveBeenCalled();
});
it.each(['Cloud unavailable', 'Connect a Firebase project'])(
  'holds the paste on cloud failure: %s',
  async error => {
    cloud.cleanup.mockRejectedValueOnce(new Error(error));
    const text = 'Contact avery@example.com.';
    const scan = await start(text);
    await finish(scan, makeReport(text, empty, NO_TOPICS, [], scan.prefix));
    await flush();
    expect(inserted()).toEqual([]);
    const state = review().postMessage.mock.calls[0][0];
    expect(state.error).toContain(error);
    expect(state.cloudCleanup).toBe(false);
    // Approving after a failure pastes locally scrubbed text and never retries
    // cloud.
    review().onMessage.emit({type: 'approve', kept: []});
    await flush();
    expect(cloud.cleanup).toHaveBeenCalledTimes(1);
    expect(inserted()[0].cleaned).not.toContain('avery@example.com');
  },
);
it('does not insert a cloud result after the user cancels', async () => {
  let resolve!: (value: any) => void;
  cloud.cleanup.mockImplementationOnce(
    () =>
      new Promise(r => {
        resolve = r;
      }),
  );
  const text = 'Contact avery@example.com.';
  const scan = await start(text);
  await finish(scan, makeReport(text, empty, NO_TOPICS, [], scan.prefix));
  const [input, signal] = cloud.cleanup.mock.calls[0];
  const gate = await import('../core/cloud-gate');
  const result = gate.applyCloudCleanup(input, {complete: true, findings: []});
  owner.onMessage.emit({type: 'cancel', id: 'paste'});
  expect(signal.aborted).toBe(true);
  resolve(result);
  await flush();
  expect(inserted()).toEqual([]);
});
it('allows the cloud diagnostic only from extension settings and uses its fixed sample', async () => {
  const reply = vi.fn();
  api.runtime.onMessage.emit(
    {type: 'test-cloud', text: 'Untrusted input'},
    {id: 'test-extension', url: 'https://chatgpt.com/'},
    reply,
  );
  await flush();
  expect(cloud.cleanup).not.toHaveBeenCalled();
  expect(api.runtime.sendMessage).not.toHaveBeenCalled();
  const report = makeReport(
    CLOUD_TEST_TEXT,
    {people: ['Avery Bennett'], companies: []},
    {...NO_TOPICS, health: ['diabetes', 'metformin']},
    [],
    'DEMO',
  );
  api.runtime.sendMessage.mockResolvedValue({ok: true, elapsed: 100, report});
  api.runtime.onMessage.emit(
    {type: 'test-cloud', text: 'Untrusted input'},
    {
      id: 'test-extension',
      url: 'chrome-extension://test-extension/options.html',
    },
    reply,
  );
  await flush();
  await flush();
  expect(api.runtime.sendMessage).toHaveBeenCalledWith({
    target: 'scanner',
    type: 'self-test-hybrid',
  });
  expect(cloud.cleanup.mock.calls[0][0].text).not.toMatch(
    /Avery Bennett|avery@example.com|Untrusted input/,
  );
  expect(reply.mock.calls[0][0]).toMatchObject({ok: true, healthRemoved: true});
});
it('does not send a cloud diagnostic after an incomplete local scan', async () => {
  const reply = vi.fn();
  const report = makeReport(
    CLOUD_TEST_TEXT,
    empty,
    NO_TOPICS,
    [],
    'DEMO',
    false,
  );
  api.runtime.sendMessage.mockResolvedValue({ok: true, elapsed: 100, report});
  api.runtime.onMessage.emit(
    {type: 'test-cloud'},
    {
      id: 'test-extension',
      url: 'chrome-extension://test-extension/options.html',
    },
    reply,
  );
  await flush();
  expect(cloud.cleanup).not.toHaveBeenCalled();
  expect(reply.mock.calls[0][0].ok).toBe(false);
});
it('exposes scanner status only to settings without sending any document text', async () => {
  const reply = vi.fn();
  api.runtime.onMessage.emit(
    {type: 'scanner-status'},
    {id: 'test-extension', url: 'https://claude.ai/'},
    reply,
  );
  await flush();
  expect(api.runtime.sendMessage).not.toHaveBeenCalled();
  api.runtime.onMessage.emit(
    {type: 'scanner-status'},
    {
      id: 'test-extension',
      url: 'chrome-extension://test-extension/options.html',
    },
    reply,
  );
  await flush();
  expect(api.runtime.sendMessage).toHaveBeenCalledWith({
    target: 'scanner',
    type: 'diagnostics',
  });
  expect(cloud.cleanup).not.toHaveBeenCalled();
});
