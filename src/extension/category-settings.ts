/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The category checkboxes on the settings page.
 */

import {browser, type Untyped} from './protocol';
import {
  ALL_CATEGORIES,
  COMMON_CATEGORIES,
  PASTE_CATEGORIES,
  normalizeCategories,
  selectedModelKinds,
  type PasteCategory,
} from './categories';

/**
 * Builds the category checkboxes and preset buttons, loads and saves the
 * selection in synced storage, and calls `changed` with the selection each time
 * it is shown.
 */
export function installCategorySettings(
  changed: (categories: readonly PasteCategory[]) => void,
) {
  const fields =
    document.querySelector<HTMLFieldSetElement>('#paste-categories')!;
  const list = document.querySelector('#category-list')!;
  const summary = document.querySelector('#category-status')!;
  const inputs = new Map<PasteCategory, HTMLInputElement>();
  let categories = ALL_CATEGORIES;
  let revision = 0;
  const render = () => {
    for (const [id, input] of inputs) input.checked = categories.includes(id);
    summary.textContent = !categories.length
      ? 'No categories selected. Pastes will be inserted without screening.'
      : `${categories.length} of ${ALL_CATEGORIES.length} categories selected. ${selectedModelKinds(categories).length ? 'Uses local pattern checks and on-device AI.' : 'Uses local pattern checks only; no AI startup needed.'}`;
    changed(categories);
  };
  const save = async (next: readonly PasteCategory[]) => {
    fields.disabled = true;
    try {
      await browser.storage.sync.set({pasteCategories: [...next]});
      categories = normalizeCategories(next);
      revision++;
      render();
    } catch {
      render();
      summary.textContent =
        'Could not save these choices. Your previous selection is still active. Try again.';
    } finally {
      fields.disabled = false;
    }
  };
  for (const category of PASTE_CATEGORIES) {
    const label = document.createElement('label');
    label.className = 'category';
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.value = category.id;
    const text = document.createElement('span');
    const title = document.createElement('strong');
    const detail = document.createElement('small');
    title.textContent = category.label;
    detail.textContent = category.detail;
    text.append(title, detail);
    label.append(input, text);
    list.append(label);
    inputs.set(category.id, input);
    input.addEventListener(
      'change',
      () => void save(ALL_CATEGORIES.filter(id => inputs.get(id)!.checked)),
    );
  }
  document
    .querySelector('#categories-common')!
    .addEventListener('click', () => void save(COMMON_CATEGORIES));
  document
    .querySelector('#categories-all')!
    .addEventListener('click', () => void save(ALL_CATEGORIES));
  browser.storage.onChanged.addListener((changes: Untyped, area: string) => {
    if (area !== 'sync' || !changes.pasteCategories) return;
    categories = normalizeCategories(changes.pasteCategories.newValue);
    revision++;
    render();
  });
  const requested = revision;
  void browser.storage.sync
    .get('pasteCategories')
    .then((saved: Untyped) => {
      if (revision === requested) {
        categories = normalizeCategories(saved.pasteCategories);
      }
      render();
      fields.disabled = false;
    })
    .catch(() => {
      summary.textContent =
        'Could not load your choices. Reopen settings to try again.';
    });
}
