/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Offscreen document. Runs paste scans and self-tests with the
 * detection worker and the on-device model, and reports progress and results to
 * the background.
 */

import {
  browser,
  fromExtensionContext,
  scanBudget,
  type Untyped,
  WAKE_BUDGET_MS,
} from './protocol';
import {
  cancelPrepare,
  extract,
  prepareModel,
  readiness,
  modelState,
  keepWarm,
} from './model';
import {NO_TOPICS} from '../core/redact';
import {
  CLOUD_TEST_TEXT,
  GENERAL_TEST_TEXT,
  PASTE_500_TEST_TEXT,
  CATEGORY_TEST_TEXT,
} from './fixtures';
import {abortable} from '../core/abortable';
import {ScanQueue} from './scan-queue';
import {normalizeCategories, selectedModelKinds} from './categories';

// The offscreen document owns a worker for deterministic detection, keeping it
// off the chat site's main thread. Raw text is only passed through
// extension-internal messages.
const worker = new Worker('detection-worker.js');
const callbacks = new Map<
  string,
  {resolve: (v: Untyped) => void; reject: (v: Error) => void}
>();
worker.onmessage = (event: MessageEvent) => {
  const callback = callbacks.get(event.data.id);
  if (!callback) return;
  callbacks.delete(event.data.id);
  if (event.data.error) callback.reject(new Error(event.data.error));
  else callback.resolve(event.data.value);
};
worker.onerror = () => {
  callbacks.forEach(c => c.reject(new Error('Local checks stopped.')));
  callbacks.clear();
};
function calculate(data: object): Promise<Untyped> {
  const id = crypto.randomUUID();
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      callbacks.delete(id);
      reject(new Error('Local checks timed out. Please retry.'));
    }, 10000);
    callbacks.set(id, {
      resolve: value => {
        clearTimeout(timer);
        resolve(value);
      },
      reject: error => {
        clearTimeout(timer);
        reject(error);
      },
    });
    worker.postMessage({...data, id});
  });
}
const jobs = new Map<string, AbortController>();
const queue = new ScanQueue();
let lastTimeout:
  | {stage: string; blocker: ReturnType<ScanQueue['snapshot']>['active']}
  | undefined;
const tell = (id: string, message: object) =>
  browser.runtime
    .sendMessage({target: 'background', id, ...message})
    .catch(() => {});
browser.runtime.onMessage.addListener(
  (message: Untyped, sender: Untyped, respond: (v: Untyped) => void) => {
    // Only the background worker and extension pages may command the scanner.
    // A content script must go through the background worker's checks.
    if (message?.target !== 'scanner' || !fromExtensionContext(sender)) {
      return;
    }
    const categories = normalizeCategories(message.categories);
    if (message.type === 'diagnostics') {
      respond({model: modelState(), ...queue.snapshot(), lastTimeout});
      return;
    }
    if (message.type === 'cancel') {
      const job = jobs.get(message.id);
      jobs.delete(message.id);
      job?.abort();
      respond({ok: true});
      return;
    }
    if (message.type === 'status') {
      void readiness()
        .then(value => respond({value}))
        .catch(() => respond({value: 'unavailable'}));
      return true;
    }
    if (message.type === 'cancel-prepare') {
      if (!jobs.size) cancelPrepare();
      respond({ok: true});
      return;
    }
    if (message.type === 'prepare') {
      // Also wake a model Chrome unloaded while idle, so focusing the chat box
      // or an open chat tab's keepalive starts the reload before the user
      // pastes. No text is sent.
      void prepareModel(false)
        .then(() => keepWarm())
        .then(() => respond({ok: true}))
        .catch(error =>
          respond({
            ok: false,
            error:
              error instanceof Error
                ? error.message
                : 'The local model could not start.',
          }),
        );
      return true;
    }
    if (
      message.type === 'self-test' ||
      message.type === 'self-test-hybrid' ||
      message.type === 'self-test-general' ||
      message.type === 'self-test-500'
    ) {
      // Fixed fictional fixture only. Diagnostic evidence never includes user
      // pastes.
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 180000);
      void queue
        .run('diagnostic', controller, async () => {
          const started = performance.now();
          const text =
            message.type === 'self-test-hybrid'
              ? CLOUD_TEST_TEXT
              : message.type === 'self-test-general'
                ? GENERAL_TEST_TEXT
                : message.type === 'self-test-500'
                  ? PASTE_500_TEST_TEXT
                  : CATEGORY_TEST_TEXT;
          const timings: Record<string, number> = {};
          const evidence = await abortable(
            extract(
              text,
              controller.signal,
              label =>
                queue.stage(
                  controller,
                  label.startsWith('Starting') ? 'preparing' : 'scanning',
                ),
              (stage, ms) => {
                timings[stage] = Math.round(ms);
              },
              categories,
            ),
            controller.signal,
          );
          controller.signal.throwIfAborted();
          queue.stage(controller, 'finishing');
          const reportStart = performance.now();
          const report = await abortable(
            calculate({
              type: 'report',
              text,
              ...evidence,
              prefix: 'DEMO',
              complete: true,
              categories,
            }),
            controller.signal,
          );
          timings.local = Math.round(performance.now() - reportStart);
          return {
            ok: true,
            elapsed: Math.round(performance.now() - started),
            report,
            evidence,
            timings,
          };
        })
        .then(respond, error =>
          respond({
            ok: false,
            error:
              error instanceof Error ? error.message : 'Test did not finish.',
          }),
        )
        .finally(() => {
          clearTimeout(timer);
        });
      return true;
    }
    if (
      message.type !== 'scan' ||
      typeof message.text !== 'string' ||
      message.text.length > 100000
    ) {
      return;
    }
    const controller = new AbortController();
    jobs.set(message.id, controller);
    let stage = 'queue';
    // Start at receipt, not after earlier work finishes. Notify immediately
    // even if a worker or native promise ignores cancellation; all late results
    // lose authority. Two deadlines: waking a model Chrome unloaded gets
    // WAKE_BUDGET_MS; the scan itself gets scanBudget, restarted once the model
    // is answering again.
    let timer = setTimeout(() => controller.abort(), scanBudget(message.text));
    const deadline = (ms: number) => {
      clearTimeout(timer);
      timer = setTimeout(() => controller.abort(), ms);
    };
    controller.signal.addEventListener(
      'abort',
      () => {
        clearTimeout(timer);
        if (jobs.get(message.id) !== controller) return;
        lastTimeout = {
          stage,
          blocker: stage === 'queue' ? queue.snapshot().active : null,
        };
        jobs.delete(message.id);
        const label =
          stage === 'prepare'
            ? 'On-device AI is still starting. Retry shortly or paste new text.'
            : stage === 'queue'
              ? 'Another local check did not finish. Retry or paste new text.'
              : 'The local check timed out. Your paste was not inserted. Retry or paste new text.';
        void tell(message.id, {type: 'failed', label});
      },
      {once: true},
    );
    respond({accepted: true});
    void tell(message.id, {
      type: 'progress',
      label: 'Waiting for the local scanner…',
    });
    const scan = async () => {
      if (controller.signal.aborted) return;
      const progress = (label: string) => {
        const next = label.startsWith('Starting on-device')
          ? 'prepare'
          : 'inference';
        if (next === 'prepare' && stage !== 'prepare') deadline(WAKE_BUDGET_MS);
        if (next === 'inference' && stage === 'prepare') {
          deadline(scanBudget(message.text));
        }
        stage = next;
        queue.stage(controller, stage);
        if (!controller.signal.aborted) {
          void tell(message.id, {type: 'progress', label});
        }
      };
      try {
        stage = 'local';
        queue.stage(controller, stage);
        const local = await abortable(
          calculate({type: 'local', text: message.text, categories}),
          controller.signal,
        );
        progress(
          local.length
            ? 'Removing private details…'
            : 'Redactobot is checking your paste…',
        );
        let evidence: Untyped = {
          names: {people: [], companies: []},
          topics: NO_TOPICS,
          ambiguous: [],
        };
        let complete = true;
        let failure: string | undefined;
        try {
          evidence = await abortable(
            extract(
              message.text,
              controller.signal,
              progress,
              undefined,
              categories,
              local,
            ),
            controller.signal,
          );
        } catch (error) {
          complete = false;
          failure = controller.signal.aborted
            ? 'The scan did not finish. Review this paste before inserting it.'
            : error instanceof Error
              ? error.message
              : 'The full scan could not finish.';
        }
        // A canceled job has no authority to insert anything, even if a late
        // result arrives.
        if (controller.signal.aborted) return;
        stage = 'report';
        queue.stage(controller, stage);
        const report = await abortable(
          calculate({
            type: 'report',
            text: message.text,
            ...evidence,
            prefix: message.prefix,
            complete,
            failure,
            categories,
          }),
          controller.signal,
        );
        if (!controller.signal.aborted) {
          void tell(message.id, {type: 'result', report});
        }
      } catch {
        if (!controller.signal.aborted) {
          void tell(message.id, {
            type: 'failed',
            label: 'The local check stopped. Retry or paste new text.',
          });
        }
      } finally {
        clearTimeout(timer);
        if (jobs.get(message.id) === controller) jobs.delete(message.id);
      }
    };
    // Pattern-only checks do not wait behind Nano startup or another model
    // request.
    void (
      selectedModelKinds(categories).length
        ? queue.run('paste', controller, scan)
        : scan()
    ).catch(() => {
      /* Cancellation was already reported by the deadline or owner. */
    });
  },
);
