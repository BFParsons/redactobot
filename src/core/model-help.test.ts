/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';

import {modelHelp} from './model-help';

const CHROME =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36';
const OLD_CHROME = CHROME.replace('Chrome/150', 'Chrome/131');
const EDGE = `${CHROME} Edg/150.0.0.0`;
const FIREFOX =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0';
const SAFARI =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/19.0 Safari/605.1.15';
const IPHONE =
  'Mozilla/5.0 (iPhone; CPU iPhone OS 19_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/19.0 Mobile/15E148 Safari/604.1';
const ANDROID_CHROME =
  'Mozilla/5.0 (Linux; Android 16; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36';

describe('why the on-device model is unavailable', () => {
  it('says nothing when the model is available', () => {
    expect(modelHelp('available', CHROME)).toBeUndefined();
  });

  it('names the browser when it is not Chrome', () => {
    expect(modelHelp('unsupported', FIREFOX)).toEqual({
      gap: 'other-browser',
      browser: 'Firefox',
    });
    expect(modelHelp('unsupported', SAFARI)).toEqual({
      gap: 'other-browser',
      browser: 'Safari',
    });
    expect(modelHelp('unsupported', EDGE)).toEqual({
      gap: 'other-browser',
      browser: 'Microsoft Edge',
    });
  });

  it('recognises phones and tablets, whatever the browser', () => {
    expect(modelHelp('unsupported', IPHONE)?.gap).toBe('mobile');
    expect(modelHelp('unsupported', ANDROID_CHROME)?.gap).toBe('mobile');
    expect(modelHelp('unavailable', ANDROID_CHROME)?.gap).toBe('mobile');
  });

  it('tells an old Chrome from one with the feature switched off', () => {
    expect(modelHelp('unsupported', OLD_CHROME)?.gap).toBe('old-chrome');
    expect(modelHelp('unsupported', CHROME)?.gap).toBe('switched-off');
  });

  it('reports hardware limits and a pending download', () => {
    expect(modelHelp('unavailable', CHROME)?.gap).toBe('hardware');
    expect(modelHelp('downloadable', CHROME)?.gap).toBe('download');
    expect(modelHelp('downloading', CHROME)?.gap).toBe('download');
  });
});
