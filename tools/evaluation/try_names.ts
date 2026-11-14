/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Print what the name rules find in a piece of text, with no model output.
 * Usage: npx vite-node tools/evaluation/try_names.ts "some text" ...
 * Set PEOPLE="A B,C D" or COMPANIES="X,Y" to stand in for what the on-device
 * model would return.
 */

import {discoverNames} from '../../src/core/names';
import {buildDetections} from '../../src/core/redact';
import {DETECTORS} from '../../taxonomy/taxonomy.js';

for (const raw of process.argv.slice(2)) {
  const text = raw.replace(/\\t/g, '\t').replace(/\\n/g, '\n');
  const found = discoverNames(text);
  console.log(JSON.stringify(text));
  console.log('  people   ', JSON.stringify(found.people));
  console.log('  companies', JSON.stringify(found.companies));
  const ids = ['names', ...DETECTORS.map((d: {id: string}) => d.id)];
  const list = (v?: string) =>
    v
      ? v
          .split(',')
          .map(x => x.trim())
          .filter(Boolean)
      : [];
  const dets = buildDetections(text, ids, {
    people: list(process.env.PEOPLE),
    companies: list(process.env.COMPANIES),
  });
  console.log(
    '  spans    ',
    dets.map(d => `${d.kind}:${JSON.stringify(d.text)}`).join('  '),
  );
}
