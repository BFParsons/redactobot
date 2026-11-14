/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Web worker that runs the rule-based checks and builds scan
 * reports off the main thread.
 */

import {localFindings, makeReport} from './policy';
import {normalizeCategories} from './categories';
self.onmessage = (event: MessageEvent) => {
  const {
    id,
    type,
    text,
    names,
    topics,
    ambiguous,
    prefix,
    complete,
    failure,
    identifying,
  } = event.data;
  const categories = normalizeCategories(event.data.categories);
  try {
    const value =
      type === 'local'
        ? localFindings(text, categories)
        : makeReport(
            text,
            names,
            topics,
            ambiguous,
            prefix,
            complete,
            failure,
            identifying,
            categories,
          );
    self.postMessage({id, value});
  } catch {
    self.postMessage({id, error: 'Could not finish the local checks.'});
  }
};
