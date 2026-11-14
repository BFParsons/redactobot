/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Benchmark page only (bench/paste/strategies.html). Times four
 * ways of deciding whether pasted text needs a warning: 500-word chunks,
 * 1,000-word chunks, one full-text request, and local rules before the
 * full-text request. Uses fixed fictional samples and the on-device model.
 */

import {DETECTORS} from '../taxonomy/taxonomy.js';
import {buildDetections, NO_TOPICS} from './core/redact';
import {PASTE_FIXTURES, type PasteFixture} from './paste-fixtures';
import {
  createProbeSession,
  probeChunks,
  PROBE_SYSTEM,
  PROBE_SCHEMA,
  type ProbeSession,
} from './paste-probe';

type Method = 'chunks-500' | 'chunks-1000' | 'whole' | 'rules-first';
type Verdict = 'warn' | 'no-match' | 'error';
interface Result {
  ms: number;
  elapsedMs?: number;
  verdict: Verdict;
  requests: number;
  completed: number;
  firstWarningMs?: number;
  tokens?: number;
  tokenCheckMs?: number;
  fallback: boolean;
  localMatches?: number;
  localMs?: number;
  error?: string;
  chunks: Verdict[];
}
interface Row {
  id: string;
  label: string;
  expected: boolean;
  words: number;
  results: Record<Method, Result[]>;
}
const methods: Method[] = ['chunks-500', 'chunks-1000', 'whole', 'rules-first'];
const methodNames: Record<Method, string> = {
  'chunks-500': '500-word chunks, stop on match',
  'chunks-1000': '1,000-word chunks, stop on match',
  whole: 'One full-text request',
  'rules-first': 'Local rules, then full-text if needed',
};
const ids = DETECTORS.filter(d => d.status === 'ready').map(d => d.id);
const $ = <T extends HTMLElement>(id: string) =>
  document.getElementById(id) as T;
const run = $<HTMLButtonElement>('run');
const save = $<HTMLButtonElement>('save');
const status = $('status');
let base: ProbeSession | undefined;
let busy = false;
let revision = 0;
let report: {
  version: number;
  experiment: string;
  startedAt: string;
  userAgent: string;
  state: string;
  hiddenDuringRun: boolean;
  createMs?: number;
  contextWindow?: number;
  contextUsage?: number;
  error?: string;
  samples: Row[];
};
const round = (n: number) => Math.round(n * 100) / 100;
const median = (a: number[]) => {
  const s = [...a].sort((a, b) => a - b);
  return (s[Math.floor((s.length - 1) / 2)] + s[Math.floor(s.length / 2)]) / 2;
};
const display = (ms: number) =>
  ms < 100 ? `${ms.toFixed(1)} ms` : `${(ms / 1000).toFixed(2)} s`;

const clean = PASTE_FIXTURES.find(f => f.id === 'clean-2000')!.text.split(
  /\s+/,
);
function inserted(id: string, at: number): PasteFixture {
  const words = [...clean];
  const sentence =
    'Could you tell Amity that her appointment has been moved?'.split(/\s+/);
  words.splice(at, sentence.length, ...sentence);
  return {
    id,
    label: `2,000 words, first name ${at === 0 ? 'at start' : at === 1000 ? 'in middle' : 'at end'}`,
    text: words.join(' '),
    sensitive: true,
  };
}
const fixtures: PasteFixture[] = [
  ...PASTE_FIXTURES.filter(f =>
    [
      'late-2000',
      'clean-2000',
      'clean-short',
      'clean-placeholder',
      'clean-health',
    ].includes(f.id),
  ),
  inserted('name-start-2000', 0),
  inserted('name-middle-2000', 1000),
  inserted('name-end-2000', 1990),
];

async function check(text: string, method: Method): Promise<Result> {
  const t = performance.now();
  const result: Result = {
    ms: 0,
    verdict: 'no-match',
    requests: 0,
    completed: 0,
    fallback: false,
    chunks: [],
  };
  try {
    if (method === 'rules-first') {
      const local = performance.now();
      result.localMatches = buildDetections(
        text,
        ids,
        {people: [], companies: []},
        [],
        new Set(),
        NO_TOPICS,
      ).length;
      result.localMs = round(performance.now() - local);
      if (result.localMatches) {
        result.verdict = 'warn';
        result.firstWarningMs = round(performance.now() - t);
        return result;
      }
    }
    if (!base) throw new Error('Model not prepared');
    let chunks: string[];
    if (method === 'whole' || method === 'rules-first') {
      const start = performance.now();
      const prompt = `Text to inspect:\n${JSON.stringify(text)}`;
      // Include schema overhead and reserve room for the short answer. Never
      // truncate a paste.
      if (
        base.measureContextUsage &&
        base.contextWindow &&
        base.contextUsage != null
      ) {
        result.tokens = await base.measureContextUsage(prompt, {
          responseConstraint: PROBE_SCHEMA,
        });
        result.fallback =
          result.tokens + base.contextUsage + 128 > base.contextWindow;
      } else {
        result.fallback = true;
      }
      result.tokenCheckMs = round(performance.now() - start);
      chunks = result.fallback ? probeChunks(text) : [text];
    } else {
      chunks = probeChunks(text, method === 'chunks-1000' ? 1000 : 500);
    }
    const checkOne = async (index: number) => {
      let session: ProbeSession | undefined;
      try {
        session = await base!.clone();
        result.requests++;
        const data = JSON.parse(
          await session.prompt(
            `Text to inspect:\n${JSON.stringify(chunks[index])}`,
            {
              responseConstraint: PROBE_SCHEMA,
              signal: AbortSignal.timeout(30000),
            },
          ),
        );
        if (typeof data.sensitive !== 'boolean') {
          throw new Error('Invalid model answer');
        }
        result.chunks[index] = data.sensitive ? 'warn' : 'no-match';
        result.completed++;
        if (data.sensitive && result.firstWarningMs == null) {
          result.firstWarningMs = round(performance.now() - t);
        }
      } finally {
        session?.destroy();
      }
    };
    for (let i = 0; i < chunks.length; i++) {
      await checkOne(i);
      if (result.chunks[i] === 'warn') break;
    }
    result.verdict = result.chunks.includes('warn') ? 'warn' : 'no-match';
  } catch (err) {
    result.verdict = 'error';
    result.error = String(err);
  } finally {
    result.elapsedMs = round(performance.now() - t);
    result.ms = result.firstWarningMs ?? result.elapsedMs;
  }
  return result;
}

function render() {
  $('rows').replaceChildren(
    ...report.samples.flatMap(s =>
      methods.map(m => {
        const values = s.results[m];
        const row = document.createElement('tr');
        for (const value of [
          s.label,
          methodNames[m],
          values.length ? display(median(values.map(v => v.ms))) : '—',
          values.map(v => v.requests).join(' / '),
          values.map(v => v.verdict).join(' / '),
        ]) {
          const td = document.createElement('td');
          td.textContent = value;
          row.append(td);
        }
        return row;
      }),
    ),
  );
  $('summary').textContent = methods
    .map(m => {
      const missed = report.samples.filter(
        s => s.expected && s.results[m].some(r => r.verdict === 'no-match'),
      );
      const falseWarnings = report.samples.filter(
        s => !s.expected && s.results[m].some(r => r.verdict === 'warn'),
      );
      const errors = report.samples
        .flatMap(s => s.results[m])
        .filter(r => r.verdict === 'error').length;
      return `${methodNames[m]}: misses ${missed.map(s => s.id).join(', ') || 'none so far'}; false warnings ${falseWarnings.map(s => s.id).join(', ') || 'none so far'}; errors ${errors}`;
    })
    .join('\n');
}

async function checkpoint(message: string) {
  report.state = message;
  status.textContent = message;
  render();
  if (new URLSearchParams(location.search).has('record')) {
    const response = await fetch('/__paste_strategy_result', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(report),
    });
    if (!response.ok) {
      throw new Error(`Saving local metrics failed: ${response.status}`);
    }
  }
  await new Promise(resolve => setTimeout(resolve, 0));
}

document.addEventListener('visibilitychange', () => {
  if (busy && document.hidden && report) report.hiddenDuringRun = true;
});
run.addEventListener('click', async () => {
  if (busy) return;
  busy = true;
  run.disabled = true;
  save.disabled = true;
  report = {
    version: 4,
    experiment: 'first-warning-latency',
    startedAt: new Date().toISOString(),
    userAgent: navigator.userAgent,
    state: 'starting',
    hiddenDuringRun: document.hidden,
    samples: fixtures.map(f => ({
      id: f.id,
      label: f.label,
      expected: f.sensitive,
      words: f.text.split(/\s+/).length,
      results: Object.fromEntries(
        methods.map(m => [m, []]),
      ) as unknown as Record<Method, Result[]>,
    })),
  };
  try {
    await checkpoint('Preparing the model session.');
    base?.destroy();
    const start = performance.now();
    base = await createProbeSession(PROBE_SYSTEM);
    report.createMs = round(performance.now() - start);
    report.contextWindow = base.contextWindow;
    report.contextUsage = base.contextUsage;
    const warm = await check(
      'Please explain how to make a paragraph clearer.',
      'whole',
    );
    if (warm.verdict === 'error') throw new Error(warm.error);
    for (let repeat = 0; repeat < 3; repeat++) {
      for (let i = 0; i < fixtures.length; i++) {
        const order = [
          ...methods.slice((i + repeat) % methods.length),
          ...methods.slice(0, (i + repeat) % methods.length),
        ];
        for (const method of order) {
          await checkpoint(
            `Run ${repeat + 1}/3: ${fixtures[i].label} — ${methodNames[method]}`,
          );
          report.samples[i].results[method].push(
            await check(fixtures[i].text, method),
          );
        }
      }
    }
    await checkpoint(
      'Finished. Timings and incorrect decisions are shown below.',
    );
  } catch (err) {
    report.error = String(err);
    report.state = `Stopped: ${String(err)}`;
    status.textContent = report.state;
    render();
  } finally {
    busy = false;
    run.disabled = false;
    save.disabled = false;
  }
});

save.addEventListener('click', () => {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(report, null, 2)], {type: 'application/json'}),
  );
  const a = document.createElement('a');
  a.href = url;
  a.download = 'first-warning-comparison.json';
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
$<HTMLTextAreaElement>('try').addEventListener('paste', e => {
  const text = e.clipboardData?.getData('text/plain') ?? '';
  const current = ++revision;
  if (busy) {
    $('try-result').textContent = 'Wait for the comparison to finish.';
    return;
  }
  if (!text.trim()) return;
  $('try-result').textContent = 'Checking locally…';
  setTimeout(async () => {
    const result = await check(text, 'rules-first');
    if (current !== revision) return;
    $('try-result').textContent =
      `${result.verdict === 'warn' ? 'Possible sensitive data found' : result.verdict === 'no-match' ? 'No match found; this is not an all-clear guarantee' : 'Check incomplete; review needed'} in ${display(result.ms)}. ${result.requests} model requests.`;
  }, 0);
});
