/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Dedicated benchmark/demo only. No production interception or
 * cloud inference.
 */

import {DETECTORS, detectPatterns} from '../taxonomy/taxonomy.js';
import {
  buildDetections,
  chunkText,
  NO_TOPICS,
  type Names,
  type Topics,
} from './core/redact';
import {
  detectNames,
  detectTopics,
  deviceStatus,
  prepareDevice,
} from './core/ai';
import {PASTE_FIXTURES} from './paste-fixtures';
import {
  createProbeSession,
  probeChunks as slices,
  PROBE_SCHEMA as schema,
  type ProbeSession as Session,
} from './paste-probe';

type Verdict = 'warn' | 'no-match' | 'error';
interface TimedVerdict {
  ms: number;
  verdict: Verdict;
  requests: number;
  firstWarningMs?: number;
  chunks: Verdict[];
  error?: string;
}
interface SampleResult {
  id: string;
  label: string;
  expected: boolean;
  words: number;
  local: Array<{
    ms: number;
    structuredMs: number;
    matches: number;
    structuredMatches: number;
    kinds: string[];
  }>;
  nano: TimedVerdict[];
  full: Array<{ms: number; matches: number; requests: number; error?: string}>;
}
const ids = DETECTORS.filter(d => d.status === 'ready').map(d => d.id);
const patternIds = DETECTORS.filter(
  d => d.status === 'ready' && d.kind === 'pattern',
).map(d => d.id);
const empty: Names = {people: [], companies: []};
const $ = <T extends HTMLElement>(id: string) =>
  document.getElementById(id) as T;
const runButton = $<HTMLButtonElement>('run');
const saveButton = $<HTMLButtonElement>('save');
const status = $('status');
const summary = $('summary');
let base: Session | undefined;
let busy = false;
let demoRevision = 0;
let started = 0;
let report: {
  version: number;
  startedAt: string;
  userAgent: string;
  hardwareConcurrency: number;
  availability: string;
  state: string;
  createMs?: number;
  firstNano?: TimedVerdict;
  fullWarmupMs?: number;
  hiddenDuringRun: boolean;
  samples: SampleResult[];
  error?: string;
};

const rounded = (n: number) => Math.round(n * 100) / 100;
const median = (a: number[]) => {
  if (!a.length) return 0;
  const s = [...a].sort((a, b) => a - b);
  return (s[Math.floor((s.length - 1) / 2)] + s[Math.floor(s.length / 2)]) / 2;
};
const duration = (n: number) =>
  n < 1000 ? `${Math.round(n)} ms` : `${(n / 1000).toFixed(2)} s`;
const yieldFrame = () => new Promise<void>(resolve => setTimeout(resolve, 0));

function localScan(text: string) {
  const t = performance.now();
  const structured = detectPatterns(text, patternIds);
  const structuredMs = performance.now() - t;
  const begin = performance.now();
  const ds = buildDetections(text, ids, empty, [], new Set(), NO_TOPICS);
  return {
    ms: rounded(performance.now() - begin),
    structuredMs: rounded(structuredMs),
    matches: ds.length,
    structuredMatches: structured.length,
    kinds: [...new Set(ds.map(d => d.kind))],
  };
}

async function nanoCheck(text: string): Promise<TimedVerdict> {
  const t = performance.now();
  let requests = 0;
  const chunks: Verdict[] = [];
  let firstWarningMs: number | undefined;
  try {
    if (!base) throw new Error('Model is not prepared.');
    for (const chunk of slices(text)) {
      let session: Session | undefined;
      try {
        session = await base.clone();
        requests++;
        const raw = await session.prompt(
          `Text to inspect:\n${JSON.stringify(chunk)}`,
          {
            responseConstraint: schema,
            signal: AbortSignal.timeout(30000),
          },
        );
        const data = JSON.parse(raw);
        if (typeof data.sensitive !== 'boolean') {
          throw new Error('Invalid model answer.');
        }
        chunks.push(data.sensitive ? 'warn' : 'no-match');
        if (data.sensitive && firstWarningMs == null) {
          firstWarningMs = rounded(performance.now() - t);
        }
      } finally {
        session?.destroy();
      }
    }
    return {
      ms: rounded(performance.now() - t),
      verdict: chunks.includes('warn') ? 'warn' : 'no-match',
      requests,
      firstWarningMs,
      chunks,
    };
  } catch (err) {
    return {
      ms: rounded(performance.now() - t),
      verdict: 'error',
      requests,
      firstWarningMs,
      chunks,
      error: String(err),
    };
  }
}

async function fullScan(text: string) {
  const t = performance.now();
  let requests = 0;
  const names: Names = {people: [], companies: []};
  const topics: Topics = {places: [], health: [], sensitive: [], names: []};
  try {
    const chunks = chunkText(text);
    for (const chunk of chunks) {
      requests++;
      const found = await detectNames(text.slice(chunk.start, chunk.end));
      names.people.push(...found.people);
      names.companies.push(...found.companies);
    }
    for (const chunk of chunks) {
      requests++;
      const found = await detectTopics(text.slice(chunk.start, chunk.end));
      for (const key of ['places', 'health', 'sensitive', 'names'] as const) {
        topics[key].push(...found[key]);
      }
    }
    const ds = buildDetections(text, ids, names, [], new Set(), topics);
    return {ms: rounded(performance.now() - t), matches: ds.length, requests};
  } catch (err) {
    return {
      ms: rounded(performance.now() - t),
      matches: -1,
      requests,
      error: String(err),
    };
  }
}

function render() {
  $('rows').replaceChildren(
    ...report.samples.map(s => {
      const row = document.createElement('tr');
      const cells = [
        s.label,
        String(s.words),
        s.local.length ? duration(median(s.local.map(r => r.ms))) : '—',
        s.local.length ? (s.local.some(r => r.matches) ? 'Yes' : 'No') : '—',
        s.nano.length ? duration(median(s.nano.map(r => r.ms))) : '—',
        s.nano.length
          ? s.nano
              .map(r =>
                r.verdict === 'warn'
                  ? 'Yes'
                  : r.verdict === 'no-match'
                    ? 'No'
                    : 'Error',
              )
              .join(' / ')
          : '—',
        s.full.length ? duration(median(s.full.map(r => r.ms))) : '—',
      ];
      for (const text of cells) {
        const td = document.createElement('td');
        td.textContent = text;
        row.append(td);
      }
      return row;
    }),
  );
  const positives = report.samples.filter(s => s.expected);
  const negatives = report.samples.filter(s => !s.expected);
  const localMissed = positives.filter(
    s => s.local.length && !s.local.some(r => r.matches),
  );
  const nanoMissed = positives.filter(s =>
    s.nano.some(r => r.verdict === 'no-match'),
  );
  const localFalse = negatives.filter(s => s.local.some(r => r.matches));
  const nanoFalse = negatives.filter(s =>
    s.nano.some(r => r.verdict === 'warn'),
  );
  summary.textContent = [
    `Session creation: ${report.createMs == null ? 'not measured yet' : duration(report.createMs)}`,
    `First model check: ${report.firstNano ? duration(report.firstNano.ms) : 'not measured yet'}`,
    `Sensitive samples without a rules warning: ${localMissed.map(s => s.id).join(', ') || 'none so far'}`,
    `Sensitive samples missed by Nano in any run: ${nanoMissed.map(s => s.id).join(', ') || 'none so far'}`,
    `Clean samples warned about by rules: ${localFalse.map(s => s.id).join(', ') || 'none so far'}`,
    `Clean samples warned about by Nano: ${nanoFalse.map(s => s.id).join(', ') || 'none so far'}`,
    report.hiddenDuringRun
      ? 'The benchmark tab was hidden during this run; timings may include background scheduling.'
      : '',
  ]
    .filter(Boolean)
    .join('\n');
}

async function checkpoint(state: string) {
  report.state = state;
  status.textContent = state;
  render();
  // Opt-in local runner only. Fixed fixture metrics are saved, never custom
  // pasted text.
  if (new URLSearchParams(location.search).has('record')) {
    try {
      await fetch('/__paste_bench_result', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(report),
      });
    } catch {
      /* browser results remain available for download */
    }
  }
  await yieldFrame();
}

document.addEventListener('visibilitychange', () => {
  if (busy && document.hidden && report) report.hiddenDuringRun = true;
});
setInterval(() => {
  if (busy) {
    $('elapsed').textContent =
      `${Math.round((performance.now() - started) / 1000)} seconds elapsed`;
  }
}, 1000);

runButton.addEventListener('click', async () => {
  if (busy) return;
  busy = true;
  started = performance.now();
  runButton.disabled = true;
  saveButton.disabled = true;
  report = {
    version: 2,
    startedAt: new Date().toISOString(),
    userAgent: navigator.userAgent,
    hardwareConcurrency: navigator.hardwareConcurrency,
    availability: 'checking',
    state: 'starting',
    hiddenDuringRun: document.hidden,
    samples: PASTE_FIXTURES.map(s => ({
      id: s.id,
      label: s.label,
      expected: s.sensitive,
      words: s.text.match(/\S+/g)!.length,
      local: [],
      nano: [],
      full: [],
    })),
  };
  try {
    for (let i = 0; i < PASTE_FIXTURES.length; i++) {
      await checkpoint(`Timing local rules: ${PASTE_FIXTURES[i].label}`);
      for (let repeat = 0; repeat < 10; repeat++) {
        report.samples[i].local.push(localScan(PASTE_FIXTURES[i].text));
      }
    }
    report.availability = await deviceStatus();
    if (
      report.availability === 'unsupported' ||
      report.availability === 'unavailable'
    ) {
      throw new Error(`Gemini Nano: ${report.availability}`);
    }
    await checkpoint(
      'Preparing Gemini Nano. Session startup is measured separately from warm paste checks.',
    );
    base?.destroy();
    base = undefined;
    const t = performance.now();
    base = await createProbeSession();
    report.createMs = rounded(performance.now() - t);
    report.firstNano = await nanoCheck(
      'Please help make this sentence easier to understand.',
    );
    for (let repeat = 0; repeat < 3; repeat++) {
      for (let i = 0; i < PASTE_FIXTURES.length; i++) {
        await checkpoint(
          `Nano sensitivity check ${repeat + 1}/3: ${PASTE_FIXTURES[i].label}`,
        );
        report.samples[i].nano.push(await nanoCheck(PASTE_FIXTURES[i].text));
      }
    }
    await checkpoint(
      'Warming the app’s full name and topic scan for comparison.',
    );
    const warm = performance.now();
    await prepareDevice(() => {});
    const warmResult = await fullScan(
      'Mira Calder works for Larkspur Fabrication LLC and has asthma.',
    );
    if (warmResult.error) throw new Error(warmResult.error);
    report.fullWarmupMs = rounded(performance.now() - warm);
    for (let repeat = 0; repeat < 2; repeat++) {
      for (let i = 0; i < PASTE_FIXTURES.length; i++) {
        if (!PASTE_FIXTURES[i].full) continue;
        await checkpoint(
          `Full app scan ${repeat + 1}/2: ${PASTE_FIXTURES[i].label}`,
        );
        report.samples[i].full.push(await fullScan(PASTE_FIXTURES[i].text));
      }
    }
    await checkpoint('Finished. Try your own paste below.');
  } catch (err) {
    report.error = String(err);
    await checkpoint(`Stopped: ${String(err)}`);
  } finally {
    busy = false;
    runButton.disabled = false;
    saveButton.disabled = false;
  }
});

saveButton.addEventListener('click', () => {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(report, null, 2)], {type: 'application/json'}),
  );
  const a = document.createElement('a');
  a.href = url;
  a.download = 'paste-benchmark.json';
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

$<HTMLTextAreaElement>('try').addEventListener('paste', e => {
  const text = e.clipboardData?.getData('text/plain') ?? '';
  const revision = ++demoRevision;
  const result = $('try-result');
  if (busy) {
    result.textContent =
      'Wait for the benchmark to finish before testing a paste.';
    return;
  }
  if (!text.trim()) return;
  // Let the local demo editor display the paste. This is not a guard on a
  // third-party site.
  setTimeout(async () => {
    const local = localScan(text);
    const instant = `${local.matches ? 'Possible sensitive data found' : 'No match from local rules'} in ${duration(local.ms)}.`;
    result.textContent = `${instant}\n${base ? 'Checking with Gemini Nano…' : 'Run the benchmark to prepare Gemini Nano.'}`;
    if (!base) return;
    const model = await nanoCheck(text);
    if (revision !== demoRevision) return;
    result.textContent = `${instant}\nNano: ${model.verdict === 'warn' ? 'possible sensitive data' : model.verdict === 'no-match' ? 'no match (not a guarantee)' : 'check failed; review needed'} in ${duration(model.ms)}.`;
  }, 0);
});
