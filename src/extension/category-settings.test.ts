/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {afterEach, beforeEach, expect, it, vi} from 'vitest';
import {readFileSync} from 'node:fs';
import {ALL_CATEGORIES, COMMON_CATEGORIES} from './categories';
let stored: any;
let get: any;
let set: any;
let listeners: Array<(changes: any, area: string) => void>;
const flush = async () => {
  for (let n = 0; n < 12; n++) await Promise.resolve();
};
const input = (id: string) =>
  document.querySelector<HTMLInputElement>(`input[value="${id}"]`)!;
const summary = () => document.querySelector('#category-status')!.textContent!;
const emit = (value: unknown) => {
  for (const listener of listeners) {
    listener({pasteCategories: {newValue: value}}, 'sync');
  }
};
beforeEach(() => {
  vi.resetModules();
  stored = {};
  listeners = [];
  document.body.innerHTML = readFileSync('extension/options.html', 'utf8');
  get = vi.fn(async () => stored);
  set = vi.fn(async (value: any) => {
    stored = {...stored, ...value};
    emit(value.pasteCategories);
  });
  vi.stubGlobal('chrome', {
    storage: {
      sync: {get, set},
      onChanged: {addListener: (fn: any) => listeners.push(fn)},
    },
  });
});
afterEach(() => vi.unstubAllGlobals());
async function open() {
  const changed = vi.fn();
  (await import('./category-settings')).installCategorySettings(changed);
  await flush();
  return changed;
}
it('preserves all checks for an existing installation until a user chooses a preset', async () => {
  await open();
  expect(
    document.querySelectorAll('#category-list input:checked'),
  ).toHaveLength(ALL_CATEGORIES.length);
  document.querySelector<HTMLButtonElement>('#categories-common')!.click();
  await flush();
  expect(stored.pasteCategories).toEqual(COMMON_CATEGORIES);
  expect(input('health').checked).toBe(false);
  document.querySelector<HTMLButtonElement>('#categories-all')!.click();
  await flush();
  expect(stored.pasteCategories).toEqual(ALL_CATEGORIES);
});
it('persists a checkbox change and loads it on the next settings visit', async () => {
  await open();
  input('health').click();
  await flush();
  expect(set).toHaveBeenCalledWith({
    pasteCategories: ALL_CATEGORIES.filter(id => id !== 'health'),
  });
  document.body.innerHTML = readFileSync('extension/options.html', 'utf8');
  await open();
  expect(input('health').checked).toBe(false);
  expect(input('names').checked).toBe(true);
});
it('rolls back a failed save instead of displaying an unsaved selection', async () => {
  await open();
  set.mockRejectedValueOnce(new Error('Storage failed'));
  input('health').click();
  await flush();
  expect(input('health').checked).toBe(true);
  expect(summary()).toContain('Could not save');
  expect(
    document.querySelector<HTMLFieldSetElement>('#paste-categories')!.disabled,
  ).toBe(false);
});
it('does not allow edits before preferences are loaded, or after a load failure', async () => {
  get.mockRejectedValueOnce(new Error('Storage failed'));
  await open();
  expect(
    document.querySelector<HTMLFieldSetElement>('#paste-categories')!.disabled,
  ).toBe(true);
  expect(summary()).toContain('Could not load');
  expect(set).not.toHaveBeenCalled();
});
it('reflects synced preferences and explains pattern-only or empty selections', async () => {
  const changed = await open();
  emit(['contact', 'payments']);
  expect(input('names').checked).toBe(false);
  expect(summary()).toContain('no AI startup needed');
  expect(changed).toHaveBeenLastCalledWith(['contact', 'payments']);
  emit([]);
  expect(summary()).toContain('without screening');
});
it('ignores an older storage read after a newer synced preference arrives', async () => {
  let resolve!: (value: any) => void;
  get.mockImplementationOnce(
    () =>
      new Promise(r => {
        resolve = r;
      }),
  );
  const {installCategorySettings} = await import('./category-settings');
  installCategorySettings(vi.fn());
  emit(['contact']);
  resolve({pasteCategories: ALL_CATEGORIES});
  await flush();
  expect(
    document.querySelectorAll('#category-list input:checked'),
  ).toHaveLength(1);
  expect(input('contact').checked).toBe(true);
});
