/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Print what the paste gate (rules only) removes from pieces of text.
 * Usage: npx vite-node tools/evaluation/try_gate.ts FILE   (pieces separated by a line "===")
 */

import {readFileSync} from 'node:fs';
import {makeReport} from '../../src/extension/policy';
import {NO_TOPICS} from '../../src/core/redact';
for (const text of readFileSync(process.argv[2], 'utf8')
  .replace(/\r/g, '')
  .split(/\n===\n/)) {
  const r = makeReport(text, {people: [], companies: []}, NO_TOPICS, [], 'T');
  console.log(JSON.stringify(text.slice(0, 80)));
  console.log(
    '  ' +
      r.findings
        .filter(
          d => !['date', 'money', 'record', 'passport_dl'].includes(d.kind),
        )
        .map(
          d =>
            `${d.kind}:${JSON.stringify(d.text)}${d.reviewReason ? '?' : ''}`,
        )
        .join('  '),
  );
}
