/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {afterEach, beforeEach, describe, expect, it, vi} from 'vitest';

describe('fromExtensionContext', () => {
  beforeEach(() => {
    vi.resetModules();
    vi.stubGlobal('chrome', {runtime: {id: 'abc'}});
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('accepts the background worker and extension pages', async () => {
    const {fromExtensionContext} = await import('./protocol');
    const worker = {
      id: 'abc',
      origin: 'chrome-extension://abc',
      url: 'chrome-extension://abc/background.js',
    };
    const options = {
      id: 'abc',
      origin: 'chrome-extension://abc',
      url: 'chrome-extension://abc/options.html',
      tab: {id: 7},
    };
    expect(fromExtensionContext(worker)).toBe(true);
    expect(fromExtensionContext(options)).toBe(true);
    expect(fromExtensionContext({id: 'abc'})).toBe(true);
  });

  it('rejects content scripts, which share the extension id', async () => {
    const {fromExtensionContext} = await import('./protocol');
    const contentScript = {
      id: 'abc',
      origin: 'https://chatgpt.com',
      url: 'https://chatgpt.com/c/1',
      tab: {id: 3},
      frameId: 0,
    };
    expect(fromExtensionContext(contentScript)).toBe(false);
    expect(fromExtensionContext({id: 'abc', tab: {id: 3}})).toBe(false);
    expect(
      fromExtensionContext({id: 'abc', url: 'https://claude.ai/new'}),
    ).toBe(false);
    expect(
      fromExtensionContext({id: 'other', origin: 'chrome-extension://other'}),
    ).toBe(false);
    expect(fromExtensionContext(undefined)).toBe(false);
  });
});
