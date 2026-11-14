/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Evaluation harness. Not part of the shipped app: it is only
 * reachable through tools/evaluation/harness.html on the dev server. It runs
 * one document through exactly the code the app uses (import -> rules ->
 * on-device names via Firebase AI Logic -> detections) and returns what was
 * found, so tools/evaluation/run_eval.py can score it against an answer key.
 */

import {FRAMEWORKS, planFor} from '../taxonomy/taxonomy.js';
import {ImportError, importBytes} from './core/import';
import {
  NO_TOPICS,
  buildDetections,
  chunkText,
  type Names,
  type Topics,
  unexplainedCapitals,
} from './core/redact';
import {
  decideOnDevice,
  deviceStatus,
  detectNames,
  detectTopics,
  prepareDevice,
} from './core/ai';
import {judgeNames} from './core/decide';

const ALL_RULES: string[] = FRAMEWORKS.map((f: {id: string}) => f.id);

interface Options {
  frameworks?: string[];
  model: boolean;
  /** Reuse names from an earlier run in place of calling the model. */
  names?: Names;
  /**
   * 'live' asks the model, 'off' skips it, an object reuses an earlier run's
   * answer. Default: live when the model is on.
   */
  topics?: 'live' | 'off' | Topics;
  /**
   * Experiment: skip the "write out the names" request. Code finds names first,
   * then the on-device model labels each capitalized phrase that is still
   * unexplained.
   */
  judge?: boolean;
}

async function run(name: string, base64: string, options: Options) {
  const bytes = Uint8Array.from(atob(base64), c => c.charCodeAt(0));
  const t0 = performance.now();
  let imported;
  try {
    imported = await importBytes(name, bytes);
  } catch (err) {
    return {
      importError: err instanceof ImportError ? err.message : String(err),
    };
  }
  const importMs = performance.now() - t0;
  const {text} = imported;
  const plan = planFor(options.frameworks ?? ALL_RULES);

  const names: Names = options.names
    ? {
        people: [...options.names.people],
        companies: [...options.names.companies],
      }
    : {people: [], companies: []};
  const chunks = chunkText(text);
  let chunkErrors = 0;
  const t1 = performance.now();
  if (options.model && !options.names && !options.judge && plan.usesModel) {
    for (const c of chunks) {
      try {
        const found = await detectNames(text.slice(c.start, c.end));
        names.people = [...new Set([...names.people, ...found.people])];
        names.companies = [
          ...new Set([...names.companies, ...found.companies]),
        ];
      } catch {
        chunkErrors++;
      }
    }
  }
  let modelMs = performance.now() - t1;

  // Judge experiment: code first, then closed questions about what is left.
  const judged = {
    candidates: 0,
    requests: 0,
    failures: 0,
    places: [] as string[],
    labels: {} as Record<string, string>,
  };
  if (options.judge) {
    const tj = performance.now();
    const codeOnly = buildDetections(text, plan.detectorIds, {
      people: [],
      companies: [],
    });
    for (const c of chunks) {
      const piece = text.slice(c.start, c.end);
      const inChunk = codeOnly
        .filter(d => d.start >= c.start && d.end <= c.end)
        .map(d => ({...d, start: d.start - c.start, end: d.end - c.start}));
      const candidates = unexplainedCapitals(piece, inChunk).filter(
        w => !(w in judged.labels),
      );
      if (!candidates.length) continue;
      judged.candidates += candidates.length;
      const out = await judgeNames(piece, candidates, decideOnDevice);
      judged.requests += out.requests;
      judged.failures += out.failures;
      for (const [phrase, label] of out.labels) {
        judged.labels[phrase] = label;
        if (label === 'person') names.people.push(phrase);
        else if (label === 'organization') names.companies.push(phrase);
        else if (label === 'place') judged.places.push(phrase);
      }
    }
    modelMs = performance.now() - tj;
  }

  // Places and sensitive topics: a second on-device request per chunk.
  let topics: Topics = {places: [], health: [], sensitive: [], names: []};
  let topicErrors = 0;
  const wantTopics =
    plan.detectorIds.includes('sensitive_topics') ||
    plan.detectorIds.includes('places');
  const mode =
    options.topics ?? (options.model && !options.names ? 'live' : 'off');
  const t2 = performance.now();
  if (typeof mode === 'object') topics = {...topics, ...mode};
  if (options.judge) {
    topics = {...topics, places: [...topics.places, ...judged.places]};
  } else if (mode === 'live' && wantTopics) {
    for (const c of chunks) {
      try {
        const found = await detectTopics(text.slice(c.start, c.end));
        for (const k of ['places', 'health', 'sensitive', 'names'] as const) {
          topics[k] = [...new Set([...topics[k], ...found[k]])];
        }
      } catch {
        topicErrors++;
      }
    }
  }
  const topicMs = performance.now() - t2;
  const slim = (list: ReturnType<typeof buildDetections>) =>
    list.map(d => ({
      start: d.start,
      end: d.end,
      text: d.text,
      kind: d.kind,
      source: d.source,
      canonical: d.canonical,
    }));

  return {
    text,
    kind: imported.kind,
    detail: imported.detail,
    notes: imported.notes,
    names,
    topics,
    judged,
    chunks: chunks.length,
    chunkErrors,
    topicErrors,
    importMs,
    modelMs,
    topicMs,
    detectors: plan.detectorIds,
    detections: slim(
      buildDetections(text, plan.detectorIds, names, [], new Set(), topics),
    ),
    patternOnly: slim(
      buildDetections(
        text,
        plan.detectorIds,
        {people: [], companies: []},
        [],
        new Set(),
        NO_TOPICS,
      ),
    ),
  };
}

const api = {
  status: deviceStatus,
  ready: false,
  async prepare() {
    await prepareDevice(() => {});
    api.ready = true;
  },
  run,
};
(window as unknown as {redactobotEval: typeof api}).redactobotEval = api;

document.getElementById('prepare')?.addEventListener('click', () => {
  const out = document.getElementById('state')!;
  out.textContent = 'loading model…';
  api.prepare().then(
    () => {
      out.textContent = 'ready';
    },
    e => {
      out.textContent = `failed: ${e}`;
    },
  );
});
