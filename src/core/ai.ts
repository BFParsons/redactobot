/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Raw-text inference uses Firebase's verified ONLY_ON_DEVICE
 * Chrome adapter. Missing adapters and failed local inference throw; there is
 * no cloud fallback. Cloud cleanup/answering live separately in cloud-client.ts
 * behind cloud-gate.ts.
 */

import type {Names, Topics} from './redact';
import {promptFor, schemaFor, type Answer, type Question} from './decide';
import {LocalModel} from './local-model';

export {cloudConfigured} from './firebase-config';

// ---------- on-device ----------
const NAME_SYSTEM_PROMPT = `You extract names from confidential documents so they can be redacted.
Return every person name and every company or organization name that appears in the text.
Copy each name exactly as it is written in the text, character for character.
Do not include cities, provinces, countries, places, dates, months, job titles, professional
designations, or generic words like "the company".
Respond only with JSON of the form {"people": [...], "companies": [...]}.`;

const NAME_SCHEMA = {
  type: 'object',
  properties: {
    people: {type: 'array', items: {type: 'string'}},
    companies: {type: 'array', items: {type: 'string'}},
  },
  required: ['people', 'companies'],
  additionalProperties: false,
};

const TEXT_EN = [{type: 'text' as const, languages: ['en']}];

/**
 * Availability of Chrome's on-device model as the Prompt API reports it, or
 * 'unsupported' when the browser has no such API.
 */
export type DeviceStatus =
  | 'available'
  | 'downloadable'
  | 'downloading'
  | 'unavailable'
  | 'unsupported'
  /** Chrome has the API but did not answer in time. */
  | 'unresponsive';

/** How long to wait for Chrome to say whether its model is available. */
export const STATUS_TIMEOUT_MS = 8000;

/**
 * Whether this browser can run the on-device model. This is a capability check
 * only (the Firebase SDK does not expose one); no text is sent to the model
 * here.
 */
export async function deviceStatus(): Promise<DeviceStatus> {
  const lm = (
    self as unknown as {
      LanguageModel?: {availability(o: object): Promise<string>};
    }
  ).LanguageModel;
  if (!lm) return 'unsupported';
  // Chrome sometimes never answers this call. Without a limit the page would
  // wait for ever with its main button disabled.
  let timer: ReturnType<typeof setTimeout> | undefined;
  const gaveUp = new Promise<DeviceStatus>(resolve => {
    timer = setTimeout(() => resolve('unresponsive'), STATUS_TIMEOUT_MS);
  });
  try {
    return await Promise.race([
      lm.availability({
        expectedInputs: TEXT_EN,
        expectedOutputs: TEXT_EN,
      }) as Promise<DeviceStatus>,
      gaveUp,
    ]);
  } catch {
    return 'unavailable';
  } finally {
    clearTimeout(timer);
  }
}

let deviceModel: LocalModel | undefined;
function getDeviceModel(): LocalModel {
  deviceModel ??= new LocalModel(NAME_SYSTEM_PROMPT, NAME_SCHEMA);
  return deviceModel;
}

/**
 * Load already-downloaded on-device sessions ahead of the first scan. Never
 * downloads (that needs a user gesture) and never sends text. A cold start can
 * take close to a minute, so starting it when the page opens hides most of that
 * wait.
 */
export async function warmDevice(): Promise<void> {
  if ((await deviceStatus()) !== 'available') return;
  await getDeviceModel().prepare(undefined, false);
  await getTopicModel().prepare(undefined, false);
  await getDeviceModel().wake();
}

/**
 * True when Chrome has probably unloaded the model and the next scan must wait
 * for it.
 */
export const deviceCold = () => LocalModel.cold();
/** Reload an idle-unloaded model before scanning. Sends no document text. */
export const wakeDevice = () => getDeviceModel().wake();

/**
 * Download (if needed) and load the on-device model. Must be called from a user
 * gesture.
 */
export function prepareDevice(
  onProgress: (fraction: number) => void,
): Promise<void> {
  return getDeviceModel().prepare(onProgress);
}

function parseNames(raw: string): Names {
  const data = JSON.parse(raw) as Partial<Names>;
  const list = (v: unknown) =>
    Array.isArray(v) ? v.filter((x): x is string => typeof x === 'string') : [];
  return {people: list(data.people), companies: list(data.companies)};
}

/**
 * Ask the on-device model for the names in one chunk of raw text. Retries once,
 * because the model fails intermittently (see bench/RESULTS.md). Throws if both
 * attempts fail.
 */
export async function detectNames(rawChunk: string): Promise<Names> {
  const model = getDeviceModel();
  let lastError: unknown;
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const result = await model.prompt(`Document:\n"""\n${rawChunk}\n"""`);
      return parseNames(result);
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError;
}

// ---------- on-device: places and sensitive topics ---------- A second
// on-device request per chunk. It is kept separate from the name request so
// that asking for more does not make the name list worse.
const TOPIC_SYSTEM_PROMPT = `You flag sensitive details in confidential documents so a person can review them.
Read the text and return four lists, each item copied exactly as written in the text.
places: cities, towns, counties, neighbourhoods and named buildings or facilities. Not countries, not street addresses.
health: diagnoses, conditions, symptoms, medications and doses, procedures, test results, mental health, substance use, disability.
sensitive: race or ethnicity, religion, political views or donations, union membership, sexual orientation, immigration or citizenship status, criminal history, genetic information.
first_names: every first name, nickname or initials used on their own to refer to a person.
Keep each health or sensitive item to the few words that carry the fact. Use an empty list when there is nothing.
Respond only with JSON of the form {"places": [...], "health": [...], "sensitive": [...], "first_names": [...]}.`;

const list = {type: 'array', items: {type: 'string'}};
const TOPIC_SCHEMA = {
  type: 'object',
  properties: {places: list, health: list, sensitive: list, first_names: list},
  required: ['places', 'health', 'sensitive', 'first_names'],
  additionalProperties: false,
};

let topicModel: LocalModel | undefined;
function getTopicModel(): LocalModel {
  topicModel ??= new LocalModel(TOPIC_SYSTEM_PROMPT, TOPIC_SCHEMA);
  return topicModel;
}

/**
 * Ask the on-device model for places and sensitive topics in one chunk of raw
 * text. Retries once.
 */
export async function detectTopics(rawChunk: string): Promise<Topics> {
  const model = getTopicModel();
  let lastError: unknown;
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const result = await model.prompt(`Document:\n"""\n${rawChunk}\n"""`);
      const data = JSON.parse(result) as Partial<Topics> & {
        first_names?: unknown;
      };
      const strings = (v: unknown) =>
        Array.isArray(v)
          ? v.filter((x): x is string => typeof x === 'string')
          : [];
      return {
        places: strings(data.places),
        health: strings(data.health),
        sensitive: strings(data.sensitive),
        names: strings(data.first_names),
      };
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError;
}

// ---------- on-device: typed questions (experimental) ----------
/**
 * Answer closed questions about raw text on the device. Each request gets a
 * schema that allows only the permitted answers. See decide.ts.
 */
export async function decideOnDevice(
  state: string,
  preamble: string,
  questions: Question[],
): Promise<Record<string, Answer>> {
  const model = new LocalModel(preamble, schemaFor(questions));
  try {
    let lastError: unknown;
    for (let attempt = 0; attempt < 2; attempt++) {
      try {
        const result = await model.prompt(promptFor(state, questions));
        return JSON.parse(result) as Record<string, Answer>;
      } catch (err) {
        lastError = err;
      }
    }
    throw lastError;
  } finally {
    model.destroy();
  }
}

// Cloud actions live in cloud-client.ts and accept runtime-issued approvals
// only.
