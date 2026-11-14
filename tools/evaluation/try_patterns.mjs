/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Print what the pattern detectors find in a piece of text.
 * Usage: node tools/evaluation/try_patterns.mjs "some text" ...   (\t and \n are understood)
 */

import {DETECTORS, detectPatterns} from '../../taxonomy/taxonomy.js';

const ALL = DETECTORS.map(d => d.id);
for (const raw of process.argv.slice(2)) {
  const text = raw.replace(/\\t/g, '\t').replace(/\\n/g, '\n');
  console.log(JSON.stringify(text));
  console.log(
    '  ' +
      detectPatterns(text, ALL)
        .map(m => `${m.type}:${JSON.stringify(m.text)}`)
        .join('  '),
  );
}
