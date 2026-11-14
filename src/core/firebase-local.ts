/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {getApps, initializeApp} from 'firebase/app';
import {
  getAI,
  getGenerativeModel,
  GoogleAIBackend,
  InferenceMode,
  InferenceSource,
} from 'firebase/ai';
import {cloudConfigured, firebaseConfig} from './firebase-config';
import {abortable} from './abortable';

interface LocalSession {
  destroy(): void;
}
interface PreparedLocalSession {
  clone(options?: {signal: AbortSignal}): Promise<LocalSession>;
}
interface LocalAdapter {
  mode: string;
  isAvailable: unknown;
  generateContent: unknown;
  oldSession?: LocalSession;
  createSession?: () => Promise<LocalSession>;
}
/**
 * Pinned Firebase 13.3.0 has a Node entry point with no Chrome adapter, even
 * when ONLY_ON_DEVICE is requested. Refuse that build BEFORE giving the SDK any
 * document. Lock the verified adapter/mode so this call has no cloud branch.
 */
export async function firebaseLocalPrompt(
  text: string,
  system: string,
  schema: object,
  signal: AbortSignal,
  prepared?: PreparedLocalSession,
): Promise<string> {
  signal.throwIfAborted();
  if (
    typeof window === 'undefined' ||
    !(globalThis as {LanguageModel?: unknown}).LanguageModel
  ) {
    throw new Error(
      'On-device AI is unavailable. No document was sent to cloud.',
    );
  }
  const config = cloudConfigured
    ? firebaseConfig
    : {
        apiKey: 'local-inference-no-network',
        projectId: 'client-safe-local-only',
        appId: 'client-safe-local-only',
      };
  const app =
    getApps().find(a => a.name === 'client-safe-local') ||
    initializeApp(config, 'client-safe-local');
  // Chrome supports prompt cancellation; the pinned Firebase type definition
  // omits this native option, so pass it through as part of the options value.
  const promptOptions = {responseConstraint: schema, signal};
  const model = getGenerativeModel(
    getAI(app, {backend: new GoogleAIBackend()}),
    {
      mode: InferenceMode.ONLY_ON_DEVICE,
      onDeviceParams: {
        createOptions: {
          expectedInputs: [{type: 'text', languages: ['en']}],
          expectedOutputs: [{type: 'text', languages: ['en']}],
          initialPrompts: [
            {role: 'system', content: [{type: 'text', value: system}]},
          ],
          signal,
        },
        promptOptions,
      },
    },
  );
  const adapter = (model as unknown as {chromeAdapter?: LocalAdapter})
    .chromeAdapter;
  if (
    !adapter ||
    adapter.mode !== InferenceMode.ONLY_ON_DEVICE ||
    typeof adapter.isAvailable !== 'function' ||
    typeof adapter.generateContent !== 'function'
  ) {
    throw new Error(
      'This Firebase build cannot guarantee on-device inference. The document was not submitted.',
    );
  }
  Object.defineProperty(adapter, 'mode', {
    value: InferenceMode.ONLY_ON_DEVICE,
    writable: false,
    configurable: false,
  });
  Object.defineProperty(model, 'chromeAdapter', {
    value: adapter,
    writable: false,
    configurable: false,
  });
  if (prepared) {
    // Firebase 13.3.0 creates a new native session for every request. Give that
    // pinned adapter an isolated clone of our text-free prepared session
    // instead. Firebase still formats the request, invokes prompt and verifies
    // the source; no global API is replaced and the base never receives
    // document text.
    if (
      typeof adapter.createSession !== 'function' ||
      typeof prepared.clone !== 'function'
    ) {
      throw new Error(
        'This Firebase build cannot use the prepared local session.',
      );
    }
    Object.defineProperty(adapter, 'createSession', {
      value: async () => {
        signal.throwIfAborted();
        const pending = prepared.clone({signal}).then(session => {
          if (signal.aborted) {
            session.destroy();
            signal.throwIfAborted();
          }
          adapter.oldSession = session;
          return session;
        });
        const session = await abortable(pending, signal);
        signal.throwIfAborted();
        return session;
      },
      writable: false,
      configurable: false,
    });
  }
  try {
    const result = await abortable(
      model.generateContent(text, {signal}),
      signal,
    );
    signal.throwIfAborted();
    if (result.response.inferenceSource !== InferenceSource.ON_DEVICE) {
      throw new Error('Unexpected inference source. The scan is invalid.');
    }
    return result.response.text();
  } finally {
    adapter.oldSession?.destroy();
    adapter.oldSession = undefined;
  }
}
