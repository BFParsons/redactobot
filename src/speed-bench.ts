/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Live speed benchmark for the paste gate's on-device step
 * (bench/speed.html). Runs in desktop Chrome with Gemini Nano. Every variant
 * reports time and how many of the answer-key names in each sample end up
 * covered by the paste gate's findings, so a faster variant cannot silently
 * lose accuracy. Samples: the chat fixtures plus paste-sized pieces of the
 * working corpus (corpus 3; corpus 2 stays unseen). Results land in
 * window.__speed.
 */

import {PASTE_FIXTURES} from './paste-fixtures';
import {chunkText, NO_TOPICS, type Names, type Topics} from './core/redact';
import {localFindings, makeReport} from './extension/policy';
import {extract, prepareModel, EXTRACT_SYSTEM} from './extension/model';
import {mightNameSomeone} from './core/name-trigger';
import {firebaseLocalPrompt} from './core/firebase-local';
import type {Ambiguous} from './extension/protocol';

/** One benchmark input: a text and the answer-key names that occur in it. */
export interface Sample {
  id: string;
  text: string;
  names: string[];
}
interface Evidence {
  names: Names;
  topics: Topics;
  ambiguous: Ambiguous[];
  identifying: Ambiguous[];
}
/**
 * One way of getting the model's evidence for a text, so that variants can be
 * timed and scored against each other.
 */
export type Variant = (
  text: string,
  signal: AbortSignal,
) => Promise<Evidence | null>; // null = model skipped

const FIXTURE_NAMES: Record<string, string[]> = {
  person: ['Mira Calder'],
  company: ['Larkspur Fabrication LLC'],
  'first-name': ['Amity'],
  'instruction-trap': ['Mira Calder'],
  'mixed-200': ['Mira Calder', 'Larkspur Fabrication LLC'],
  'mixed-500': ['Mira Calder', 'Larkspur Fabrication LLC'],
  'late-2000': ['Mira Calder'],
};
/**
 * Loads the benchmark samples: every paste fixture, then pieces of corpus
 * documents fetched from the dev server, each with the person and
 * organization names from its answer key that occur in the piece.
 *
 * @param docs How many corpus documents to read, starting at the first.
 * @param piecesPerDoc How many leading pieces of about 150 words to take
 *     from each document.
 * @param longDocs How many of the first documents are also added whole.
 * @param corpus Which corpus to read: 2 starts at doc-201 and uses run
 *     c2-round4; any other value starts at doc-301 and uses c3-round4.
 */
export async function loadSamples(
  docs = 20,
  piecesPerDoc = 2,
  longDocs = 3,
  corpus = 3,
): Promise<Sample[]> {
  const samples: Sample[] = PASTE_FIXTURES.map(f => ({
    id: `fixture:${f.id}`,
    text: f.text,
    names: FIXTURE_NAMES[f.id] ?? [],
  }));
  const first = corpus === 2 ? 201 : 301;
  const run = corpus === 2 ? 'c2-round4' : 'c3-round4';
  for (let n = first; n < first + docs; n++) {
    const id = `doc-${n}`;
    const raw = await (
      await fetch(`/evaluation/results/${run}/raw/${id}.json`)
    ).json();
    const keys = (
      await (await fetch(`/evaluation/corpus${corpus}/keys/${id}.json`)).json()
    ).items
      .filter(
        (i: any) =>
          i.category === 'person_name' || i.category === 'organization_name',
      )
      .map((i: any) => i.value as string);
    const pieces = chunkText(raw.text, 150).slice(0, piecesPerDoc);
    pieces.forEach((p, i) => {
      const text = raw.text.slice(p.start, p.end);
      samples.push({
        id: `${id}#${i}`,
        text,
        names: keys.filter((k: string) => text.includes(k)),
      });
    });
    if (n < first + longDocs) {
      samples.push({
        id: `${id}#full`,
        text: raw.text,
        names: keys.filter((k: string) => raw.text.includes(k)),
      });
    }
  }
  return samples;
}

/**
 * Share of key-name occurrences whose every non-space character lies inside a
 * finding.
 */
function coverage(
  text: string,
  names: string[],
  spans: Array<{start: number; end: number}>,
) {
  let total = 0;
  let caught = 0;
  for (const name of [...new Set(names)].sort((a, b) => b.length - a.length)) {
    for (
      let at = text.indexOf(name);
      at >= 0;
      at = text.indexOf(name, at + name.length)
    ) {
      total++;
      let ok = true;
      for (let i = at; i < at + name.length && ok; i++) {
        if (
          !/\s/.test(text[i]) &&
          !spans.some(s => s.start <= i && i < s.end)
        ) {
          ok = false;
        }
      }
      if (ok) caught++;
    }
  }
  return {total, caught};
}

/**
 * Runs one variant over every sample. Times the model step and the local
 * report step, and counts how many answer-key names the report's findings
 * cover. A variant that throws is recorded as an error and scored without
 * model evidence.
 *
 * @param name Label copied into the summary.
 * @return A summary (name recall as a percentage, median, 90th-percentile
 *     and mean time, skips, errors) and one row per sample.
 */
export async function run(name: string, variant: Variant, samples: Sample[]) {
  const rows: Array<{
    id: string;
    words: number;
    modelMs: number;
    localMs: number;
    skipped: boolean;
    error: string;
    total: number;
    caught: number;
    review: boolean;
    findings: number;
  }> = [];
  for (const s of samples) {
    const started = performance.now();
    let evidence: Evidence | null = null;
    let error = '';
    try {
      evidence = await variant(s.text, new AbortController().signal);
    } catch (e) {
      error = String(e).slice(0, 120);
    }
    const modelMs = performance.now() - started;
    const t = performance.now();
    const e = evidence ?? {
      names: {people: [], companies: []},
      topics: NO_TOPICS,
      ambiguous: [],
      identifying: [],
    };
    const report = makeReport(
      s.text,
      e.names,
      e.topics,
      e.ambiguous,
      'B',
      !error,
      undefined,
      e.identifying,
    );
    const localMs = performance.now() - t;
    const cov = coverage(s.text, s.names, report.findings);
    rows.push({
      id: s.id,
      words: s.text.split(/\s+/).length,
      modelMs: Math.round(modelMs),
      localMs: Math.round(localMs),
      skipped: evidence === null && !error,
      error,
      ...cov,
      review: report.needsReview,
      findings: report.findings.length,
    });
  }
  const sum = (k: 'modelMs' | 'total' | 'caught') =>
    rows.reduce((n, r) => n + r[k], 0);
  const ms = rows.map(r => r.modelMs + r.localMs).sort((a, b) => a - b);
  const summary = {
    variant: name,
    samples: rows.length,
    nameRecall: +((100 * sum('caught')) / Math.max(1, sum('total'))).toFixed(1),
    namesCaught: sum('caught'),
    namesTotal: sum('total'),
    medianMs: ms[Math.floor(ms.length / 2)],
    p90Ms: ms[Math.floor(ms.length * 0.9)],
    meanMs: Math.round(ms.reduce((a, b) => a + b, 0) / ms.length),
    skipped: rows.filter(r => r.skipped).length,
    errors: rows.filter(r => r.error).length,
  };
  return {summary, rows};
}

// ---------- variants ----------
/** The production request, unchanged. */
export const production: Variant = async (text, signal) =>
  extract(text, signal, () => {});

/** Same production request, but skip the model when no word could be a name. */
export function gated(
  inner: Variant,
  mightName: (text: string) => boolean,
): Variant {
  return async (text, signal) => (mightName(text) ? inner(text, signal) : null);
}

/**
 * Grouped JSON output: one array per kind, so each item costs only its own
 * text.
 */
const GROUP_KINDS = [
  'person',
  'company',
  'place',
  'health',
  'sensitive',
  'identifying',
  'uncertain',
] as const;
const groupedSchema = {
  type: 'object',
  properties: Object.fromEntries(
    GROUP_KINDS.map(k => [k, {type: 'array', items: {type: 'string'}}]),
  ),
  required: [...GROUP_KINDS],
  additionalProperties: false,
};
/**
 * Builds a variant that asks for one array of excerpts per kind and converts
 * the answer into evidence.
 *
 * @param system The system instructions sent with every request.
 * @param base Returns the prepared session; called on every request, so the
 *     session may be created after the variant is built.
 */
export function grouped(system: string, base: () => any): Variant {
  return async (text, signal) => {
    const prompt = `Document:\n${JSON.stringify(text)}`;
    const raw = await firebaseLocalPrompt(
      prompt,
      system,
      groupedSchema,
      signal,
      base(),
    );
    const data = JSON.parse(raw);
    const list = (k: string) =>
      (Array.isArray(data[k]) ? data[k] : []).filter(
        (v: unknown) => typeof v === 'string' && v.trim(),
      );
    return {
      names: {people: list('person'), companies: list('company')},
      topics: {
        ...NO_TOPICS,
        places: list('place'),
        health: list('health'),
        sensitive: list('sensitive'),
        names: [],
      },
      ambiguous: list('uncertain').map((t: string) => ({
        text: t,
        reason: 'This possible private detail needs a closer look.',
      })),
      identifying: list('identifying').map((t: string) => ({
        text: t,
        reason: 'This detail may identify someone indirectly.',
      })),
    };
  };
}

/**
 * The production instructions with the output format switched to one array per
 * kind.
 */
export const GROUPED_SYSTEM = EXTRACT_SYSTEM.replace(
  /Return only a JSON array of[^\n]*\n/,
  'Return only a JSON object with one array of exact excerpts per kind: {"person":[],"company":[],"place":[],"health":[],"sensitive":[],"identifying":[],"uncertain":[]}. Use empty arrays when nothing applies. No explanations.\n',
).replace(
  /For a genuinely ambiguous match, use uncertain_person[^\n]*\n/,
  'Put a genuinely ambiguous possible private detail in "uncertain". Clear full names go in "person".\n',
);
let groupedBase: any;
/** Creates the session for the grouped variant, unless it already exists. */
export async function prepareGrouped() {
  const language = {
    expectedInputs: [{type: 'text', languages: ['en']}],
    expectedOutputs: [{type: 'text', languages: ['en']}],
  };
  groupedBase ??= await (globalThis as any).LanguageModel.create({
    ...language,
    initialPrompts: [{role: 'system', content: GROUPED_SYSTEM}],
  });
}
/**
 * The grouped request, using GROUPED_SYSTEM and the session from
 * prepareGrouped().
 */
export const groupedVariant: Variant = (text, signal) =>
  grouped(GROUPED_SYSTEM, () => groupedBase)(text, signal);

/**
 * Send the model only the sentences that could name someone (plus their
 * neighbours).
 */
export function sentenceFiltered(inner: Variant): Variant {
  return async (text, signal) => {
    const sentences = [...text.matchAll(/[^.!?\n]+(?:[.!?]+|\n|$)/g)].map(
      m => m[0],
    );
    const keep = new Set<number>();
    sentences.forEach((s, i) => {
      if (mightNameSomeone(s)) {
        keep.add(i);
        if (i > 0) keep.add(i - 1);
        if (i + 1 < sentences.length) keep.add(i + 1);
      }
    });
    if (!keep.size) return null;
    const subset = [...keep]
      .sort((a, b) => a - b)
      .map(i => sentences[i])
      .join(' ');
    return inner(subset, signal);
  };
}
/** The production request, skipped when no word could be a name. */
export const gatedProduction = gated(production, mightNameSomeone);
/**
 * The production request, sent only the sentences that could name someone.
 */
export const filteredProduction = sentenceFiltered(production);

export {prepareModel};
declare global {
  interface Window {
    __speed: any;
    speed: any;
  }
}
window.speed = {
  loadSamples,
  run,
  production,
  gated,
  grouped,
  prepareModel,
  prepareGrouped,
  groupedVariant,
  gatedProduction,
  filteredProduction,
  sentenceFiltered,
  GROUPED_SYSTEM,
};
window.__speed = {ready: true};

// ---------- round 2 ----------
/**
 * Grouped output where every key is optional, so "nothing found" can be just
 * {}.
 */
const optionalSchema = {
  type: 'object',
  properties: groupedSchema.properties,
  additionalProperties: false,
};
/**
 * The grouped instructions, changed to leave out kinds with no excerpts and
 * to answer {} when nothing applies.
 */
export const GROUPED_OPTIONAL_SYSTEM = GROUPED_SYSTEM.replace(
  'Use empty arrays when nothing applies.',
  'Include only kinds that have excerpts; return {} when nothing applies.',
);
let optionalBase: any;
/**
 * Creates the session for the optional-keys variant, unless it already
 * exists.
 */
export async function prepareOptional() {
  const language = {
    expectedInputs: [{type: 'text', languages: ['en']}],
    expectedOutputs: [{type: 'text', languages: ['en']}],
  };
  optionalBase ??= await (globalThis as any).LanguageModel.create({
    ...language,
    initialPrompts: [{role: 'system', content: GROUPED_OPTIONAL_SYSTEM}],
  });
}
/**
 * The grouped request with every key optional. A kind that is missing or not
 * an array counts as empty.
 */
export const optionalVariant: Variant = async (text, signal) => {
  const raw = await firebaseLocalPrompt(
    `Document:\n${JSON.stringify(text)}`,
    GROUPED_OPTIONAL_SYSTEM,
    optionalSchema,
    signal,
    optionalBase,
  );
  const data = JSON.parse(raw);
  const list = (k: string) =>
    (Array.isArray(data[k]) ? data[k] : []).filter(
      (v: unknown) => typeof v === 'string' && v.trim(),
    );
  return {
    names: {people: list('person'), companies: list('company')},
    topics: {
      ...NO_TOPICS,
      places: list('place'),
      health: list('health'),
      sensitive: list('sensitive'),
      names: [],
    },
    ambiguous: list('uncertain').map((t: string) => ({
      text: t,
      reason: 'This possible private detail needs a closer look.',
    })),
    identifying: list('identifying').map((t: string) => ({
      text: t,
      reason: 'This detail may identify someone indirectly.',
    })),
  };
};
/** The optional-keys request, skipped when no word could be a name. */
export const gatedOptional = gated(optionalVariant, mightNameSomeone);
/** The grouped request, skipped when no word could be a name. */
export const gatedGrouped = gated(groupedVariant, mightNameSomeone);
Object.assign(window.speed, {
  prepareOptional,
  optionalVariant,
  gatedOptional,
  gatedGrouped,
});

// ---------- round 3 ----------
/**
 * Flat list of tagged strings: "person: Margaret Whitfield". Empty is still [].
 */
const TAGS = [
  'person',
  'company',
  'place',
  'health',
  'sensitive',
  'identifying',
  'uncertain',
];
const taggedSchema = {type: 'array', items: {type: 'string'}};
/**
 * The production instructions with the output format switched to a flat list
 * of "kind: exact excerpt" strings.
 */
export const TAGGED_SYSTEM = EXTRACT_SYSTEM.replace(
  /Return only a JSON array of[^\n]*\n/,
  'Return only a JSON array of strings, each "kind: exact excerpt", for example ["person: Nerys", "place: Norvale"]. Kinds: person, company, place, health, sensitive, identifying, uncertain. Return [] if none. No explanations.\n',
).replace(
  /For a genuinely ambiguous match, use uncertain_person[^\n]*\n/,
  'Use the kind "uncertain" for a genuinely ambiguous possible private detail. Clear full names are person.\n',
);
let taggedBase: any;
/** Creates the session for the tagged variant, unless it already exists. */
export async function prepareTagged() {
  const language = {
    expectedInputs: [{type: 'text', languages: ['en']}],
    expectedOutputs: [{type: 'text', languages: ['en']}],
  };
  taggedBase ??= await (globalThis as any).LanguageModel.create({
    ...language,
    initialPrompts: [{role: 'system', content: TAGGED_SYSTEM}],
  });
}
/** Raw model output of the latest taggedVariant request, for debugging. */
export let lastRaw = '';
/**
 * The tagged-list request. Rejects when an item is not a "kind: excerpt"
 * string; an item of an unknown kind is dropped.
 */
export const taggedVariant: Variant = async (text, signal) => {
  const prompt = `Active categories: person, company, place, health, sensitive, identifying, uncertain. Check only these categories.\nDocument:\n${JSON.stringify(text)}`;
  const raw = await firebaseLocalPrompt(
    prompt,
    TAGGED_SYSTEM,
    taggedSchema,
    signal,
    taggedBase,
  );
  lastRaw = raw;
  const by: Record<string, string[]> = Object.fromEntries(
    TAGS.map(t => [t, []]),
  );
  for (const item of JSON.parse(raw)) {
    const m =
      typeof item === 'string'
        ? /^\s*([a-z_]+)\s*:\s*(.+?)\s*$/i.exec(item)
        : null;
    if (!m) throw new Error('The model returned an incomplete answer.');
    const kind = m[1].toLowerCase().replace(/^uncertain_.*/, 'uncertain');
    if (by[kind]) by[kind].push(m[2]);
  }
  return {
    names: {people: by.person, companies: by.company},
    topics: {
      ...NO_TOPICS,
      places: by.place,
      health: by.health,
      sensitive: by.sensitive,
      names: [],
    },
    ambiguous: by.uncertain.map(t => ({
      text: t,
      reason: 'This possible private detail needs a closer look.',
    })),
    identifying: by.identifying.map(t => ({
      text: t,
      reason: 'This detail may identify someone indirectly.',
    })),
  };
};
/** Debug: raw output of the optional-keys variant for one text. */
export async function optionalRaw(text: string) {
  return firebaseLocalPrompt(
    `Document:\n${JSON.stringify(text)}`,
    GROUPED_OPTIONAL_SYSTEM,
    optionalSchema,
    new AbortController().signal,
    optionalBase,
  );
}
Object.assign(window.speed, {
  prepareTagged,
  taggedVariant,
  gatedTagged: gated(taggedVariant, mightNameSomeone),
  optionalRaw,
  raw: () => lastRaw,
});

// ---------- round 4: previous production format, for a fair comparison
// ----------
const OBJECT_SYSTEM = EXTRACT_SYSTEM.replace(
  /Return only a JSON array of strings[^\n]*\n/,
  'Return only a JSON array of {"text":"exact excerpt","kind":"person"}; return [] if none. No explanations.\n',
);
const OBJECT_KINDS = [
  'person',
  'company',
  'place',
  'health',
  'sensitive',
  'identifying',
  'uncertain',
  'uncertain_person',
  'uncertain_company',
  'uncertain_place',
  'uncertain_health',
  'uncertain_sensitive',
];
const objectSchema = {
  type: 'array',
  items: {
    type: 'object',
    properties: {
      text: {type: 'string'},
      kind: {type: 'string', enum: OBJECT_KINDS},
    },
    required: ['text', 'kind'],
    additionalProperties: false,
  },
};
let objectBase: any;
/**
 * Creates the session for the object-list variant, unless it already exists.
 */
export async function prepareObjects() {
  const language = {
    expectedInputs: [{type: 'text', languages: ['en']}],
    expectedOutputs: [{type: 'text', languages: ['en']}],
  };
  objectBase ??= await (globalThis as any).LanguageModel.create({
    ...language,
    initialPrompts: [{role: 'system', content: OBJECT_SYSTEM}],
  });
}
/**
 * The previous production format: a list of {text, kind} objects. An
 * uncertain_<kind> item counts both as that kind and as ambiguous.
 */
export const objectsVariant: Variant = async (text, signal) => {
  const prompt = `Active categories: ${OBJECT_KINDS.slice(0, 7).join(', ')}. Check only these categories.\nDocument:\n${JSON.stringify(text)}`;
  const data = JSON.parse(
    await firebaseLocalPrompt(
      prompt,
      OBJECT_SYSTEM,
      objectSchema,
      signal,
      objectBase,
    ),
  );
  const by = (k: string) =>
    data
      .filter((d: any) => d.kind === k || d.kind === `uncertain_${k}`)
      .map((d: any) => d.text);
  return {
    names: {people: by('person'), companies: by('company')},
    topics: {
      ...NO_TOPICS,
      places: by('place'),
      health: by('health'),
      sensitive: by('sensitive'),
      names: [],
    },
    ambiguous: data
      .filter((d: any) => d.kind.startsWith('uncertain'))
      .map((d: any) => ({text: d.text, reason: 'Uncertain'})),
    identifying: by('identifying').map((t: string) => ({
      text: t,
      reason: 'Identifying',
    })),
  };
};
Object.assign(window.speed, {
  prepareObjects,
  objectsVariant,
  gatedObjects: gated(objectsVariant, mightNameSomeone),
});

// ---------- round 6: hide what the rules already found ----------
/**
 * Replace structured rule findings (emails, phones, numbers, dates, money...)
 * with placeholders before the model sees the text, so it cannot spend output
 * repeating them.
 */
export function premasked(inner: Variant): Variant {
  return async (text, signal) => {
    const spans = localFindings(text)
      .filter(
        d =>
          ![
            'person',
            'company',
            'place',
            'health',
            'sensitive',
            'other',
          ].includes(d.kind) && !d.reviewReason,
      )
      .sort((a, b) => a.start - b.start);
    let masked = '';
    let at = 0;
    for (const d of spans) {
      if (d.start < at) continue;
      masked += text.slice(at, d.start) + `[${d.base || 'REDACTED'}]`;
      at = d.end;
    }
    return inner(masked + text.slice(at), signal);
  };
}
Object.assign(window.speed, {
  premasked,
  premaskedProduction: premasked(production),
});

// ---------- round 8: Firebase per-call overhead ----------
/**
 * Same tagged request through Firebase AI Logic vs the native session, n times
 * each.
 */
export async function fbVsNative(text: string, n = 6) {
  await prepareTagged();
  const prompt = `Active categories: person, company. Check only these categories.\nDocument:\n${JSON.stringify(text)}`;
  const schema = {
    type: 'array',
    items: {type: 'string', pattern: '^(person|company): .+$'},
  };
  const out: Record<string, number[]> = {firebase: [], native: []};
  for (let i = 0; i < n; i++) {
    let t = performance.now();
    await firebaseLocalPrompt(
      prompt,
      TAGGED_SYSTEM,
      schema,
      new AbortController().signal,
      taggedBase,
    );
    out.firebase.push(Math.round(performance.now() - t));
    t = performance.now();
    const c = await taggedBase.clone();
    await c.prompt(prompt, {responseConstraint: schema});
    c.destroy();
    out.native.push(Math.round(performance.now() - t));
  }
  return out;
}
Object.assign(window.speed, {fbVsNative});
