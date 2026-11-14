/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Read-only source corpus. Results are written under ignored evaluation/results/work.
 * node tools/evaluation/desktop-corpus.mjs --corpus C:/.../Desktop/TESTFILES [--port 5180]
 */

import {createServer} from 'vite';
import {readdir, readFile, writeFile, mkdir} from 'node:fs/promises';
import {realpathSync} from 'node:fs';
import {resolve, join, extname} from 'node:path';
import {createHash, randomBytes} from 'node:crypto';
import {JSDOM} from 'jsdom';
const arg = (name, fallback) =>
  process.argv.includes(name)
    ? process.argv[process.argv.indexOf(name) + 1]
    : fallback;
const root = resolve(import.meta.dirname, '../..');
const corpus = resolve(arg('--corpus', ''));
const port = Number(arg('--port', '5180'));
const stamp = new Date().toISOString().replace(/[:.]/g, '-');
const out = resolve(root, 'evaluation/results/work', `desktop-${stamp}`);
const hash = value => createHash('sha256').update(value).digest('hex');
const answer = await readFile(join(corpus, 'answerkey.csv'));
if (answer.length < 30) throw new Error('Wait for a populated answerkey.csv.');
const entries = (await readdir(corpus, {withFileTypes: true}))
  .filter(
    d =>
      d.isFile() &&
      !d.name.startsWith('_') &&
      d.name.toLowerCase() !== 'answerkey.csv',
  )
  .map(d => d.name)
  .sort();
if (!entries.length) throw new Error('No supported documents.');
await mkdir(join(out, 'nano'), {recursive: true});
await mkdir(join(out, 'local'), {recursive: true});
const dom = new JSDOM();
globalThis.DOMParser = dom.window.DOMParser;
const token = randomBytes(32).toString('hex');
const documents = [];
const completed = new Set();
let state = {state: 'preparing', total: entries.length, completed: 0};
const origin = `http://127.0.0.1:${port}`;
const server = await createServer({
  root,
  configFile: false,
  appType: 'mpa',
  server: {
    host: '127.0.0.1',
    port,
    strictPort: true,
    hmr: false,
    watch: null,
    ws: false,
    fs: {allow: [root, realpathSync(join(root, 'node_modules'))]},
    headers: {
      'Content-Security-Policy':
        "default-src 'self'; connect-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'",
    },
  },
  plugins: [
    {
      name: 'desktop-corpus',
      configureServer(vite) {
        vite.middlewares.use('/__corpus', async (req, res) => {
          if (
            req.headers.authorization !== `Bearer ${token}` ||
            (req.method === 'POST' && req.headers.origin !== origin)
          ) {
            res.statusCode = 403;
            res.end();
            return;
          }
          res.setHeader('Content-Type', 'application/json');
          res.setHeader('Cache-Control', 'no-store');
          try {
            if (req.method === 'GET' && req.url === '/manifest') {
              res.end(
                JSON.stringify({
                  total: documents.length,
                  completed: completed.size,
                  pending: documents
                    .map((_, i) => i)
                    .filter(i => !completed.has(i)),
                }),
              );
              return;
            }
            const match = /^\/document\/(\d+)$/.exec(req.url);
            if (req.method === 'GET' && match) {
              const d = documents[Number(match[1])];
              if (!d) throw new Error('Unknown document');
              res.end(
                JSON.stringify({
                  name: d.name,
                  text: d.text,
                  textHash: d.textHash,
                }),
              );
              return;
            }
            if (
              req.method !== 'POST' ||
              !['/result', '/status'].includes(req.url)
            ) {
              throw new Error('Unknown route');
            }
            let body = '';
            for await (const chunk of req) {
              body += chunk;
              if (body.length > 2500000) throw new Error('Result too large');
            }
            const value = JSON.parse(body);
            if (req.url === '/result') {
              const d = documents[value.index];
              if (
                !Number.isInteger(value.index) ||
                !d ||
                d.textHash !== value.textHash ||
                !Array.isArray(value.report?.findings)
              ) {
                throw new Error('Invalid result');
              }
              for (const f of value.report.findings) {
                if (d.text.slice(f.start, f.end) !== f.text) {
                  throw new Error('Invalid span');
                }
              }
              await writeFile(
                join(out, 'nano', `${value.index}.json`),
                JSON.stringify(value, null, 2),
                {flag: 'wx'},
              );
              completed.add(value.index);
              state = {
                state: 'running',
                total: documents.length,
                completed: completed.size,
                lastMs: Math.round(value.elapsedMs),
              };
              console.log(
                `${completed.size}/${documents.length} · ${Math.round(value.elapsedMs)} ms · ${value.gate}`,
              );
            } else {
              state = {...state, ...value};
            }
            await writeFile(
              join(out, 'status.json'),
              JSON.stringify(state, null, 2),
            );
            res.end('{"ok":true}');
          } catch (error) {
            res.statusCode = 400;
            res.end(JSON.stringify({error: error.message}));
          }
        });
      },
    },
  ],
});
const {importBytes} = await server.ssrLoadModule('/src/core/import/index.ts');
const {localFindings} = await server.ssrLoadModule('/src/extension/policy.ts');
const {applyRedactions} = await server.ssrLoadModule('/src/core/redact.ts');
const files = [];
for (const name of entries) {
  const bytes = await readFile(join(corpus, name));
  const file = {
    name,
    sha256: hash(bytes),
    bytes: bytes.length,
    extension: extname(name),
  };
  try {
    const imported = await importBytes(name, bytes);
    const text = imported.text;
    const textHash = hash(text);
    const index = documents.length;
    const at = performance.now();
    const findings = localFindings(text);
    const elapsedMs = performance.now() - at;
    documents.push({name, text, textHash});
    await writeFile(
      join(out, 'local', `${index}.json`),
      JSON.stringify(
        {
          index,
          name,
          text,
          textHash,
          elapsedMs,
          findings,
          cleaned: applyRedactions(text, findings).cleaned,
          importNotes: imported.notes,
        },
        null,
        2,
      ),
    );
    files.push({...file, index, textHash, importNotes: imported.notes});
  } catch (error) {
    files.push({...file, importError: error.message});
  }
}
// Detect generation changing under us before we accept this as an independent
// run.
for (const file of files) {
  if (hash(await readFile(join(corpus, file.name))) !== file.sha256) {
    throw new Error('Corpus changed during import. Retry after generation.');
  }
}
if (hash(await readFile(join(corpus, 'answerkey.csv'))) !== hash(answer)) {
  throw new Error('Answer key changed during import. Retry after generation.');
}
await writeFile(join(out, 'answerkey.csv'), answer);
const sourceFiles = [
  'taxonomy/taxonomy.js',
  'taxonomy/detectors.js',
  'taxonomy/identity-patterns.js',
  'taxonomy/normalize.js',
  'taxonomy/places-data.js',
  'src/core/redact.ts',
  'src/core/tables.ts',
  'src/core/classification.ts',
  'src/core/names.ts',
  'src/core/privacy-buckets.ts',
  'src/core/firebase-local.ts',
  'src/core/cloud-gate.ts',
  'src/extension/policy.ts',
  'src/extension/model.ts',
];
const sourceHashes = Object.fromEntries(
  await Promise.all(
    sourceFiles.map(async name => [
      name,
      hash(await readFile(join(root, name))),
    ]),
  ),
);
await writeFile(
  join(out, 'manifest.json'),
  JSON.stringify(
    {
      created: new Date().toISOString(),
      corpus,
      answerkeySha256: hash(answer),
      files,
      sourceHashes,
      note: 'The answer key is used only by the offline scorer, never by detection or Nano.',
    },
    null,
    2,
  ),
);
state = {state: 'ready', total: documents.length, completed: 0};
await writeFile(join(out, 'status.json'), JSON.stringify(state, null, 2));
await server.listen();
const url = `${origin}/tools/evaluation/desktop-corpus.html#${token}`;
await writeFile(
  join(root, 'evaluation/results/work/desktop-run.json'),
  JSON.stringify({out, url, pid: process.pid}, null, 2),
);
console.log(
  JSON.stringify({
    out,
    documents: documents.length,
    importFailures: files.filter(f => f.importError).length,
  }),
);
console.log(
  'Local results saved. Open the evaluation URL in desktop-run.json to run Nano.',
);
