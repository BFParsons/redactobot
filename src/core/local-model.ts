/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Native API is used for model preparation only. Inference uses
 * Firebase's verified browser adapter, with no cloud branch and no retained raw
 * history.
 */

import {firebaseLocalPrompt} from './firebase-local';
interface NativeSession {
  clone(options?: {signal: AbortSignal}): Promise<NativeSession>;
  prompt(text: string, options: object): Promise<string>;
  destroy(): void;
}
interface NativeAPI {
  availability(options: object): Promise<string>;
  create(options: object): Promise<NativeSession>;
}
const language = {
  expectedInputs: [{type: 'text', languages: ['en']}],
  expectedOutputs: [{type: 'text', languages: ['en']}],
};
const nativeAPI = () =>
  (globalThis as unknown as {LanguageModel?: NativeAPI}).LanguageModel;

/**
 * Chrome unloads the on-device model when idle; touch it if it has been idle
 * this long.
 */
export const TOUCH_AFTER_MS = 90_000;
/** Reloading an unloaded model measured 1-3+ minutes. */
export const WAKE_TIMEOUT_MS = 300_000;
// Shared by every LocalModel: Chrome loads one on-device model for all
// sessions.
let lastActive = 0;
let waking: Promise<void> | undefined;

/**
 * A session with Chrome's on-device model, set up with a fixed system prompt
 * and a JSON schema for its answers.
 */
export class LocalModel {
  private base?: NativeSession;
  private preparing?: Promise<void>;
  /**
   * Returns whether no LocalModel has answered for TOUCH_AFTER_MS, so Chrome
   * may have unloaded the model.
   */
  static cold() {
    return performance.now() - lastActive > TOUCH_AFTER_MS;
  }
  constructor(
    private system: string,
    private schema: object,
  ) {}

  /**
   * Creates the text-free base session, downloading the model first if needed.
   * Calls made while one is in progress share it.
   *
   * @param onProgress Called with the fraction downloaded, from 0 to 1.
   * @param allowDownload When false, throws unless the model is already
   *     downloaded.
   */
  async prepare(
    onProgress: (fraction: number) => void = () => {},
    allowDownload = true,
  ): Promise<void> {
    if (this.base) return;
    if (this.preparing) return this.preparing;
    this.preparing = (async () => {
      const api = nativeAPI();
      if (!api) {
        throw new Error(
          'On-device AI is unavailable. No document was sent to a cloud model.',
        );
      }
      const state = await api.availability(language);
      if (
        state === 'unavailable' ||
        (!allowDownload && state !== 'available')
      ) {
        throw new Error(
          'On-device AI is not ready. No document was sent to a cloud model.',
        );
      }
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 180000);
      try {
        this.base = await api.create({
          ...language,
          signal: controller.signal,
          initialPrompts: [{role: 'system', content: this.system}],
          monitor: (monitor: EventTarget) =>
            monitor.addEventListener('downloadprogress', (event: Event) =>
              onProgress((event as Event & {loaded: number}).loaded),
            ),
        });
        onProgress(1);
      } finally {
        clearTimeout(timer);
      }
    })();
    try {
      await this.preparing;
    } finally {
      this.preparing = undefined;
    }
  }

  /**
   * Text-free one-word prompt that makes Chrome reload a model it unloaded
   * while idle.
   */
  async wake(): Promise<void> {
    await this.prepare(undefined, false);
    if (!LocalModel.cold()) return;
    const base = this.base!;
    waking ??= (async () => {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), WAKE_TIMEOUT_MS);
      const clone = await base.clone({signal: controller.signal});
      try {
        await clone.prompt('Reply with OK.', {signal: controller.signal});
        lastActive = performance.now();
      } finally {
        clearTimeout(timer);
        clone.destroy();
      }
    })().finally(() => {
      waking = undefined;
    });
    await waking;
  }

  /**
   * Sends `text` to the model through Firebase's on-device adapter and returns
   * the reply. Gives up after 60 seconds.
   */
  async prompt(text: string): Promise<string> {
    await this.prepare(undefined, false);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 60000);
    try {
      // Clone the warm, text-free base session instead of letting Firebase
      // build a new one (and re-read the system prompt) for every chunk. The
      // base never sees text.
      const result = await firebaseLocalPrompt(
        text,
        this.system,
        this.schema,
        controller.signal,
        this.base,
      );
      lastActive = performance.now();
      return result;
    } finally {
      clearTimeout(timer);
    }
  }
  /**
   * Releases the base session. The next call that needs one creates it again.
   */
  destroy() {
    this.base?.destroy();
    this.base = undefined;
  }
}
