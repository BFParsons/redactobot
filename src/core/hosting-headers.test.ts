/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {readFileSync} from 'node:fs';

import {expect, it} from 'vitest';

it('serves the same Permissions-Policy on Cloudflare Pages and Firebase Hosting', () => {
  const firebase = JSON.parse(readFileSync('firebase.json', 'utf8'));
  const policy = firebase.hosting.headers
    .flatMap(
      (rule: {headers: Array<{key: string; value: string}>}) => rule.headers,
    )
    .find((header: {key: string}) => header.key === 'Permissions-Policy').value;
  const cloudflare = readFileSync('public/_headers', 'utf8');
  expect(cloudflare).toContain(`Permissions-Policy: ${policy}`);
  expect(policy).toContain('camera=()');
});
