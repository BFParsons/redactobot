/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Local-only runner. Saves metrics for the fixed fictional suite; never clipboard text.
 * node tools/paste_benchmark.mjs --out C:/path/to/results.json
 */

import {createServer} from 'vite';
import {realpathSync} from 'node:fs';
import {mkdir, writeFile} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
const root = resolve(import.meta.dirname, '..');
const arg = (key, fallback) =>
  process.argv.includes(key)
    ? process.argv[process.argv.indexOf(key) + 1]
    : fallback;
const out = resolve(
  arg('--out', 'evaluation/results/work/paste-benchmark.json'),
);
const strategiesOut = resolve(
  arg('--strategies-out', 'evaluation/results/work/paste-strategies.json'),
);
const port = Number(arg('--port', '5175'));
await mkdir(dirname(out), {recursive: true});
await mkdir(dirname(strategiesOut), {recursive: true});
const server = await createServer({
  root,
  configFile: false,
  server: {
    host: '127.0.0.1',
    port,
    strictPort: true,
    hmr: false,
    watch: null,
    fs: {allow: [root, realpathSync(resolve(root, 'node_modules'))]},
  },
  plugins: [
    {
      name: 'local-paste-results',
      configureServer(vite) {
        const collect = (target, validate) => async (req, res) => {
          if (
            req.method !== 'POST' ||
            req.headers.origin !== `http://127.0.0.1:${port}`
          ) {
            res.statusCode = 403;
            res.end();
            return;
          }
          let body = '';
          for await (const chunk of req) {
            body += chunk;
            if (body.length > 250000) {
              res.statusCode = 413;
              res.end();
              return;
            }
          }
          try {
            const value = JSON.parse(body);
            if (!validate(value)) throw new Error('Invalid report');
            await writeFile(target, JSON.stringify(value, null, 2));
            console.log(value.state);
            res.statusCode = 204;
            res.end();
          } catch {
            res.statusCode = 400;
            res.end('Invalid report');
          }
        };
        vite.middlewares.use(
          '/__paste_bench_result',
          collect(
            out,
            value =>
              [1, 2].includes(value.version) &&
              Array.isArray(value.samples) &&
              value.samples.length === 17,
          ),
        );
        vite.middlewares.use(
          '/__paste_strategy_result',
          collect(
            strategiesOut,
            value =>
              value.version === 4 &&
              value.experiment === 'first-warning-latency' &&
              Array.isArray(value.samples) &&
              value.samples.length === 8,
          ),
        );
      },
    },
  ],
});
await server.listen();
console.log(
  `Open http://127.0.0.1:${port}/bench/paste/?record=1 and press Run paste benchmark.`,
);
console.log(`Metrics: ${out}`);
console.log(
  `Long paste comparison: http://127.0.0.1:${port}/bench/paste/strategies.html?record=1; metrics ${strategiesOut}`,
);
