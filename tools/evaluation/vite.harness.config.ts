/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Builds the evaluation harness as a static page, so a long
 * evaluation run is not disturbed by edits to the source (the dev server
 * reloads the page on every change).
 *
 *   npx vite build -c tools/evaluation/vite.harness.config.ts --outDir /some/dir
 *   python3 -m http.server 5181 --bind 127.0.0.1 -d /some/dir
 *   REDACTOBOT_HARNESS_URL=http://127.0.0.1:5181/tools/evaluation/harness.html python3 -P tools/evaluation/run_eval.py NAME
 */

import {resolve} from 'node:path';
import {defineConfig} from 'vite';

export default defineConfig({
  root: resolve(__dirname, '../..'),
  base: '/',
  publicDir: false,
  build: {
    target: 'es2022',
    emptyOutDir: true,
    rollupOptions: {input: resolve(__dirname, 'harness.html')},
  },
});
