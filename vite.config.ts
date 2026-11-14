/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {defineConfig} from 'vitest/config';
import {loadEnv} from 'vite';
import {readFileSync, realpathSync} from 'node:fs';
import {fileURLToPath} from 'node:url';

/**
 * The Permissions-Policy header from firebase.json, so the local server blocks
 * the same browser features (camera, microphone, location and the rest) as the
 * hosted site. Redactobot needs only clipboard-write, for its Copy buttons.
 */
const permissionsPolicy: string = JSON.parse(
  readFileSync(new URL('./firebase.json', import.meta.url), 'utf8'),
)
  .hosting.headers.flatMap(
    (rule: {headers: Array<{key: string; value: string}>}) => rule.headers,
  )
  .find((header: {key: string}) => header.key === 'Permissions-Policy').value;

export default defineConfig(({command, mode}) => {
  // Vite compiles VITE_* values into public JavaScript. A debug token in the
  // hosted bundle lets anyone mint App Check tokens for the project, so refuse
  // that build. The unpacked extension (tools/build_extension.mjs) is a
  // separate, local build.
  if (
    command === 'build' &&
    loadEnv(mode, process.cwd(), 'VITE_').VITE_APPCHECK_DEBUG_TOKEN
  ) {
    throw new Error(
      'VITE_APPCHECK_DEBUG_TOKEN is set. Remove it from the web build environment and use reCAPTCHA Enterprise for the hosted app.',
    );
  }
  return {
    build: {target: 'es2022', outDir: 'dist'},
    preview: {headers: {'Permissions-Policy': permissionsPolicy}},
    server: {
      host: '127.0.0.1',
      port: 5173,
      headers: {'Permissions-Policy': permissionsPolicy},
      fs: {
        allow: [
          fileURLToPath(new URL('.', import.meta.url)),
          realpathSync(
            fileURLToPath(new URL('./node_modules', import.meta.url)),
          ),
        ],
      },
    },
    test: {
      include: ['src/**/*.test.ts'],
      alias: {
        'firebase/ai': fileURLToPath(
          new URL(
            './node_modules/@firebase/ai/dist/esm/index.esm.js',
            import.meta.url,
          ),
        ),
      },
    },
  };
});
