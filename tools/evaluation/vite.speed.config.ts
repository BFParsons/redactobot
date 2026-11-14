/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Dev server for bench/speed.html with no file watching or
 * reloads, so code can be edited while a long live measurement runs. Restart it
 * to pick up changes.
 */

import {defineConfig} from 'vite';
import {realpathSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const root = fileURLToPath(new URL('../..', import.meta.url));
export default defineConfig({
  root,
  server: {
    host: '127.0.0.1',
    port: 5183,
    strictPort: true,
    hmr: false,
    watch: null,
    fs: {
      allow: [
        root,
        realpathSync(
          fileURLToPath(new URL('../../node_modules', import.meta.url)),
        ),
      ],
    },
  },
});
