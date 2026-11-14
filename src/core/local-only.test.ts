/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {afterEach, beforeEach, describe, expect, it, vi} from 'vitest';
import {readFileSync} from 'node:fs';

const raw = 'Fictional confidential note: Avery Bennett, avery@example.com.';
let network: ReturnType<typeof vi.fn>;
beforeEach(() => {
  vi.resetModules();
  // Configure a fictional cloud project so these checks cannot pass merely
  // because the optional cloud feature has no configuration. Do not mock the
  // Firebase SDK.
  vi.stubEnv('VITE_FIREBASE_API_KEY', 'fictional-test-key');
  vi.stubEnv('VITE_FIREBASE_PROJECT_ID', 'local-only-test');
  vi.stubEnv('VITE_FIREBASE_APP_ID', '1:123:web:local-only-test');
  vi.stubEnv('VITE_RECAPTCHA_ENTERPRISE_SITE_KEY', '');
  vi.stubEnv('VITE_APPCHECK_DEBUG_TOKEN', '');
  vi.stubGlobal('LanguageModel', undefined);
  network = vi.fn(() => {
    throw new Error('Network calls forbidden in this test');
  });
  vi.stubGlobal('fetch', network);
  vi.stubGlobal('XMLHttpRequest', network);
  vi.stubGlobal('WebSocket', network);
  Object.defineProperty(navigator, 'sendBeacon', {
    configurable: true,
    value: network,
  });
});
afterEach(() => {
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
  Reflect.deleteProperty(navigator, 'sendBeacon');
});

describe('raw-text inference stays local on failure', () => {
  it.each(['detectNames', 'detectTopics', 'decideOnDevice'] as const)(
    'app %s rejects without network when Nano is missing',
    async method => {
      const ai = await import('./ai');
      expect(ai.cloudConfigured).toBe(true);
      const result =
        method === 'decideOnDevice'
          ? ai.decideOnDevice(raw, 'Check the text.', [
              {
                id: 'private',
                type: 'noul',
                instructions: 'Contains a personal name?',
              },
            ])
          : ai[method](raw);
      await expect(result).rejects.toThrow();
      expect(network).not.toHaveBeenCalled();
    },
  );
  it('extension rejects without a remote request when Nano is unavailable', async () => {
    const create = vi.fn();
    vi.stubGlobal('LanguageModel', {
      availability: async () => 'unavailable',
      create,
    });
    const {extract} = await import('../extension/model');
    await expect(
      extract(raw, new AbortController().signal, () => {}),
    ).rejects.toThrow('unavailable');
    expect(create).not.toHaveBeenCalled();
    expect(network).not.toHaveBeenCalled();
  });
  it.each(['detectNames', 'detectTopics', 'decideOnDevice'] as const)(
    'app %s never switches to cloud after local generation fails',
    async method => {
      const prompt = vi.fn().mockRejectedValue(new Error('Local model failed'));
      const session = {
        prompt,
        destroy() {},
        clone: async () => ({prompt, destroy() {}}),
      };
      vi.stubGlobal('LanguageModel', {
        availability: async () => 'available',
        create: async () => session,
      });
      const ai = await import('./ai');
      const result =
        method === 'decideOnDevice'
          ? ai.decideOnDevice(raw, 'Check the text.', [
              {
                id: 'private',
                type: 'noul',
                instructions: 'Contains a personal name?',
              },
            ])
          : ai[method](raw);
      await expect(result).rejects.toThrow('Local model failed');
      expect(prompt).toHaveBeenCalledTimes(2);
      expect(network).not.toHaveBeenCalled();
    },
  );
  it('app still parses successful native name, topic and decision results without network calls', async () => {
    const prompt = vi
      .fn()
      .mockResolvedValueOnce('{"people":["Avery Bennett"],"companies":[]}')
      .mockResolvedValueOnce(
        '{"places":["Seattle"],"health":[],"sensitive":[],"first_names":[]}',
      )
      .mockResolvedValueOnce('{"private":true}');
    const destroy = vi.fn();
    vi.stubGlobal('LanguageModel', {
      availability: async () => 'available',
      create: async () => ({
        prompt,
        destroy,
        clone: async () => ({prompt, destroy}),
      }),
    });
    const ai = await import('./ai');
    await ai.prepareDevice(() => {});
    expect(await ai.detectNames(raw)).toEqual({
      people: ['Avery Bennett'],
      companies: [],
    });
    expect(await ai.detectTopics(raw)).toEqual({
      places: ['Seattle'],
      health: [],
      sensitive: [],
      names: [],
    });
    expect(
      await ai.decideOnDevice(raw, 'Check the text.', [
        {
          id: 'private',
          type: 'noul',
          instructions: 'Contains a personal name?',
        },
      ]),
    ).toEqual({private: true});
    // Three per-request sessions and the temporary decision base.
    expect(destroy).toHaveBeenCalledTimes(4);
    expect(network).not.toHaveBeenCalled();
  });
  it('extension retries a failed prompt locally and never switches to a remote service', async () => {
    const prompt = vi.fn().mockRejectedValue(new Error('Local model failed'));
    const session = {
      prompt,
      destroy() {},
      clone: async () => ({prompt, destroy() {}}),
    };
    vi.stubGlobal('LanguageModel', {
      availability: async () => 'available',
      create: async () => session,
    });
    const {extract} = await import('../extension/model');
    await expect(
      extract(raw, new AbortController().signal, () => {}),
    ).rejects.toThrow('Local model failed');
    expect(prompt).toHaveBeenCalledTimes(2);
    expect(network).not.toHaveBeenCalled();
  });
  it('blocks scanner connections and limits cloud connections to Firebase', () => {
    const manifest = JSON.parse(
      readFileSync('extension/manifest.json', 'utf8'),
    );
    const directives = manifest.content_security_policy.extension_pages
      .split(';')
      .map((x: string) => x.trim());
    expect(directives.find((s: string) => s.startsWith('connect-src'))).toBe(
      'connect-src https://firebasevertexai.googleapis.com https://firebaseappcheck.googleapis.com https://content-firebaseappcheck.googleapis.com',
    );
    expect(manifest.host_permissions).toEqual([
      'https://firebasevertexai.googleapis.com/*',
      'https://firebaseappcheck.googleapis.com/*',
      'https://content-firebaseappcheck.googleapis.com/*',
    ]);
    expect(readFileSync('extension/scanner.html', 'utf8')).toContain(
      "connect-src 'none'",
    );
    expect(
      readFileSync('src/extension/detection-worker.ts', 'utf8'),
    ).not.toMatch(/fetch|XMLHttpRequest|firebase|cloud-client/);
  });
  it('uses isolated warm clones through the real Firebase SDK without re-creating the base', async () => {
    const children: any[] = [];
    const base = {
      prompt: vi.fn(),
      destroy: vi.fn(),
      clone: vi.fn(async () => {
        const child = {
          prompt: vi.fn().mockResolvedValue('[]'),
          destroy: vi.fn(),
        };
        children.push(child);
        return child;
      }),
    };
    const create = vi.fn().mockResolvedValue(base);
    vi.stubGlobal('LanguageModel', {
      availability: async () => 'available',
      create,
    });
    const {extract, prepareModel} = await import('../extension/model');
    await prepareModel();
    await extract(raw, new AbortController().signal, () => {});
    await extract(
      'A separate fictional document from Quinn Harlow.',
      new AbortController().signal,
      () => {},
    );
    expect(create).toHaveBeenCalledOnce();
    expect(base.clone).toHaveBeenCalledTimes(2);
    expect(base.prompt).not.toHaveBeenCalled();
    expect(base.destroy).not.toHaveBeenCalled();
    expect(JSON.stringify(children[0].prompt.mock.calls)).toContain(
      'Avery Bennett',
    );
    expect(JSON.stringify(children[1].prompt.mock.calls)).not.toContain(
      'Avery Bennett',
    );
    for (const child of children) {
      expect(child.prompt).toHaveBeenCalledOnce();
      expect(child.destroy).toHaveBeenCalledOnce();
    }
    expect(network).not.toHaveBeenCalled();
  });
  it('destroys a clone that arrives after cancellation without ever prompting it', async () => {
    let ready!: (value: any) => void;
    const child = {prompt: vi.fn(), destroy: vi.fn()};
    const clone = vi.fn(
      () =>
        new Promise(resolve => {
          ready = resolve;
        }),
    );
    vi.stubGlobal('LanguageModel', {
      availability: async () => 'available',
      create: async () => ({clone, destroy() {}}),
    });
    const {extract, prepareModel} = await import('../extension/model');
    await prepareModel();
    const controller = new AbortController();
    const waiting = extract(raw, controller.signal, () => {});
    const rejected = expect(waiting).rejects.toThrow();
    await vi.waitFor(() => expect(clone).toHaveBeenCalledOnce());
    controller.abort();
    await rejected;
    ready(child);
    await vi.waitFor(() => expect(child.destroy).toHaveBeenCalledOnce());
    expect(child.prompt).not.toHaveBeenCalled();
    expect(network).not.toHaveBeenCalled();
  });
  it('releases an unresponsive inference clone on abort and can scan another document', async () => {
    const first = {
      prompt: vi.fn(() => new Promise(() => {})),
      destroy: vi.fn(),
    };
    const second = {prompt: vi.fn().mockResolvedValue('[]'), destroy: vi.fn()};
    const clone = vi
      .fn()
      .mockResolvedValueOnce(first)
      .mockResolvedValueOnce(second);
    const base = {clone, destroy: vi.fn()};
    vi.stubGlobal('LanguageModel', {
      availability: async () => 'available',
      create: async () => base,
    });
    const {extract, prepareModel} = await import('../extension/model');
    await prepareModel();
    const controller = new AbortController();
    const waiting = extract(raw, controller.signal, () => {});
    const rejected = expect(waiting).rejects.toThrow();
    await vi.waitFor(() => expect(first.prompt).toHaveBeenCalledOnce());
    controller.abort();
    await rejected;
    expect(first.destroy).toHaveBeenCalledOnce();
    await extract(
      'New document from Quinn Harlow.',
      new AbortController().signal,
      () => {},
    );
    expect(second.prompt).toHaveBeenCalledOnce();
    expect(second.destroy).toHaveBeenCalledOnce();
    expect(base.destroy).not.toHaveBeenCalled();
    expect(network).not.toHaveBeenCalled();
  });
});
