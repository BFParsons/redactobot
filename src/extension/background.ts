/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Service worker. Owns each held paste: starts the offscreen
 * scanner, relays progress and results between the chat tab and the review
 * page, and runs the optional cloud cleanup.
 */

import {
  browser,
  namespace,
  siteFor,
  MAX_PASTE,
  scanBudget,
  WAKE_BUDGET_MS,
  type RuntimePort,
  type ScanReport,
  type Theme,
  type Untyped,
} from './protocol';
import {cleanedText} from './policy';
import {prepareCloudInput} from '../core/cloud-gate';
import {cleanupCloud, cloudSetupProblem} from '../core/cloud-client';
import {privacyBucket} from '../core/privacy-buckets';
import {CLOUD_TEST_TEXT} from './fixtures';
import {
  ALL_CATEGORIES,
  normalizeCategories,
  allCategoriesSelected,
  selectedModelKinds,
  type PasteCategory,
} from './categories';

interface Job {
  id: string;
  scanId?: string;
  token: string;
  tabId: number;
  owner: RuntimePort;
  text: string;
  original: string;
  prefix: string;
  theme: Theme;
  report?: ScanReport;
  review?: RuntimePort;
  reviewTab?: number;
  timer: ReturnType<typeof setTimeout>;
  scanTimer?: ReturnType<typeof setTimeout>;
  contextChanged?: boolean;
  categories: readonly PasteCategory[];
  cloudCleanup: boolean;
  cloudDone?: boolean;
  cloudFailed?: boolean;
  reviewWindow?: number;
  cloudAbort?: AbortController;
  problem?: string;
  phase: 'scanning' | 'review' | 'cloud' | 'ready' | 'failed';
}
const jobs = new Map<string, Job>();
let startingScanner: Promise<void> | undefined;
const scannerExists = async () =>
  (
    await browser.runtime.getContexts({
      contextTypes: ['OFFSCREEN_DOCUMENT'],
      documentUrls: [browser.runtime.getURL('scanner.html')],
    })
  ).length > 0;
/**
 * Make sure the offscreen scanner document exists. Callers share one attempt:
 * switching Redactobot on and pasting straight away both ask for the scanner,
 * and Chrome allows only one such document. Checking and creating separately
 * let the second caller see "none yet", then fail to create a duplicate, which
 * left the first paste after startup held with "could not start".
 */
function scanner(): Promise<void> {
  startingScanner ??= (async () => {
    if (await scannerExists()) return;
    try {
      await browser.offscreen.createDocument({
        url: 'scanner.html',
        reasons: ['WORKERS'],
        justification:
          'Run local document detection in a dedicated worker, with on-device AI in its owning document.',
      });
    } catch (error) {
      // Another caller, or an earlier worker, created it first.
      if (!(await scannerExists())) throw error;
    }
  })().finally(() => {
    startingScanner = undefined;
  });
  return startingScanner;
}
/**
 * Send a message to the scanner. A document that has only just been created may
 * not be listening yet, in which case Chrome rejects the send; try again
 * briefly instead of failing the paste.
 */
async function toScanner(message: object): Promise<Untyped> {
  for (let attempt = 0; ; attempt++) {
    try {
      return await browser.runtime.sendMessage({target: 'scanner', ...message});
    } catch (error) {
      if (attempt >= 4) throw error;
      await new Promise(resolve => setTimeout(resolve, 120));
    }
  }
}
// A startup load the user opted into is not canceled by a tab switching off.
let preloading = false;
/**
 * Optional startup load (settings: "Load on-device AI when Chrome starts"). Off
 * by default.
 */
async function preload() {
  try {
    const saved = await browser.storage.sync.get([
      'preloadAtStartup',
      'pasteCategories',
    ]);
    if (saved.preloadAtStartup !== true) return;
    if (
      !selectedModelKinds(normalizeCategories(saved.pasteCategories)).length
    ) {
      return;
    }
    await scanner();
    // Preparation carries no page/document text and never starts a cloud
    // request.
    preloading = true;
    await browser.runtime.sendMessage({target: 'scanner', type: 'prepare'});
  } catch {
    /* Unavailable/download-needed states are shown in settings or on paste. */
  } finally {
    preloading = false;
  }
}
// Tabs waiting for the on-device model to start. Redactobot starts switched off
// on every page, so the model loads only after the user switches it on, and
// stops loading when every tab that asked has switched off again (or closed)
// with no paste in progress.
const waiting = new Set<RuntimePort>();
function abandon(port?: RuntimePort) {
  if (port && !waiting.delete(port)) return;
  if (waiting.size || jobs.size || preloading) return;
  void browser.runtime
    .sendMessage({target: 'scanner', type: 'cancel-prepare'})
    .catch(() => {});
}
function send(port: RuntimePort | undefined, message: Untyped) {
  try {
    port?.postMessage(message);
  } catch {
    /* disconnected */
  }
}
function release(id: string) {
  const job = jobs.get(id);
  if (!job) return;
  clearTimeout(job.timer);
  clearTimeout(job.scanTimer);
  jobs.delete(id);
  job.cloudAbort?.abort();
  if (job.scanId) {
    void browser.runtime
      .sendMessage({target: 'scanner', type: 'cancel', id: job.scanId})
      .catch(() => {});
  }
  send(job.review, {type: 'closed'});
  if (job.reviewWindow != null) {
    void browser.windows.remove(job.reviewWindow).catch(() => {});
  }
  job.text = '';
  job.original = '';
  job.report = undefined;
}
function reviewState(job: Job) {
  return {
    type: 'review-state',
    id: job.id,
    theme: job.theme,
    text: job.text,
    report: job.report,
    contextChanged: !!job.contextChanged,
    cloudCleanup: job.cloudCleanup && !job.cloudDone && !job.cloudFailed,
    error: job.problem,
  };
}
function requireReview(job: Job) {
  job.phase = 'review';
  send(job.owner, {type: 'review', id: job.id, token: job.token});
  if (job.review) send(job.review, reviewState(job));
}
function scanFailed(job: Job, label: string) {
  clearTimeout(job.scanTimer);
  if (job.scanId) {
    void browser.runtime
      .sendMessage({target: 'scanner', type: 'cancel', id: job.scanId})
      .catch(() => {});
  }
  job.scanId = undefined;
  job.phase = 'failed';
  send(job.owner, {type: 'failed', id: job.id, label});
}
async function scanJob(job: Job) {
  if (job.scanId) {
    void browser.runtime
      .sendMessage({target: 'scanner', type: 'cancel', id: job.scanId})
      .catch(() => {});
  }
  const scanId = crypto.randomUUID();
  job.scanId = scanId;
  clearTimeout(job.scanTimer);
  job.scanTimer = setTimeout(
    () => {
      if (
        jobs.get(job.id) === job &&
        job.scanId === scanId &&
        job.phase === 'scanning'
      ) {
        scanFailed(
          job,
          'The local scanner did not finish. Retry or paste new text.',
        );
      }
      // Backstop only: the scanner owns the precise wake and scan deadlines and
      // reports them.
    },
    WAKE_BUDGET_MS + scanBudget(job.text) + 1000,
  );
  job.phase = 'scanning';
  job.report = undefined;
  job.problem = undefined;
  send(job.owner, {
    type: 'progress',
    id: job.id,
    label: 'Checking identifying details…',
  });
  send(job.review, {type: 'busy', label: 'Checking the edited text locally…'});
  try {
    await scanner();
    if (jobs.get(job.id) !== job || job.scanId !== scanId) return;
    const response = await toScanner({
      type: 'scan',
      id: scanId,
      text: job.text,
      prefix: job.prefix,
      categories: job.categories,
    });
    if (response?.accepted !== true) {
      throw new Error('Scanner did not accept the paste.');
    }
  } catch {
    if (jobs.get(job.id) === job && job.scanId === scanId) {
      scanFailed(
        job,
        'The local scanner could not start. Your paste is still held.',
      );
    }
  }
}
function insertLocal(job: Job, kept: string[] = []) {
  if (!job.report?.complete) {
    send(job.review, {
      type: 'error',
      message: 'The full local check must finish before text can be pasted.',
    });
    return;
  }
  // The identity bucket is mandatory, including after a human review.
  const allowed = kept.filter(id =>
    job.report!.findings.some(
      d => d.id === id && privacyBucket(d) === 'cloud-cleanup',
    ),
  );
  const cleaned = cleanedText(
    job.text,
    job.report.findings,
    job.prefix,
    allowed,
  );
  job.phase = 'ready';
  send(job.owner, {
    type: 'insert',
    id: job.id,
    cleaned,
    reviewed: true,
    count: job.report.findings.length - allowed.length,
  });
}
async function runCloud(
  job: Job,
  reviewed = false,
  removeSensitiveLocally: string[] = [],
) {
  if (!job.report || job.phase === 'cloud') return;
  try {
    const problem = cloudSetupProblem();
    if (problem) throw new Error(problem);
    const input = prepareCloudInput(
      job.text,
      job.report,
      job.prefix,
      reviewed,
      removeSensitiveLocally,
    );
    job.phase = 'cloud';
    job.problem = undefined;
    job.cloudAbort = new AbortController();
    send(job.owner, {
      type: 'progress',
      id: job.id,
      label: 'Removing sensitive details in cloud…',
    });
    send(job.review, {
      type: 'busy',
      label: 'Only the identity-scrubbed preview is being checked in cloud…',
    });
    const result = await cleanupCloud(input, job.cloudAbort.signal);
    if (jobs.get(job.id) !== job || job.cloudAbort.signal.aborted) return;
    job.text = result.text;
    job.report = result.report;
    job.prefix += '_CLOUD';
    job.cloudDone = true;
    if (job.report.needsReview || job.contextChanged) requireReview(job);
    else insertLocal(job);
  } catch (error) {
    if (jobs.get(job.id) !== job || job.cloudAbort?.signal.aborted) return;
    // Never retry cloud silently. The review now offers local removal only,
    // with sensitive details removed locally by default; the user decides.
    job.cloudFailed = true;
    job.problem = `${error instanceof Error ? error.message : 'Cloud cleanup did not finish.'} You can paste with local removal only.`;
    requireReview(job);
  }
}
function ownPage(sender: Untyped, path: string) {
  try {
    return (
      sender?.id === browser.runtime.id &&
      new URL(sender.url).pathname === path &&
      new URL(sender.url).protocol === 'chrome-extension:'
    );
  } catch {
    return false;
  }
}

browser.runtime.onConnect.addListener((port: RuntimePort) => {
  const sender = port.sender;
  if (port.name === 'paste-guard') {
    const tabId = sender?.tab?.id;
    if (
      !sender ||
      sender.id !== browser.runtime.id ||
      sender.frameId !== 0 ||
      tabId == null ||
      !siteFor(sender.url || '')
    ) {
      port.disconnect();
      return;
    }
    port.onMessage.addListener((message: Untyped) => {
      if (message?.type === 'cancel-prepare') {
        abandon(port);
        return;
      }
      if (message?.type === 'prepare') {
        waiting.add(port);
        void browser.storage.sync
          .get('pasteCategories')
          .then(async (saved: Untyped) => {
            if (
              !selectedModelKinds(normalizeCategories(saved.pasteCategories))
                .length
            ) {
              return {ok: true};
            }
            await scanner();
            return browser.runtime.sendMessage({
              target: 'scanner',
              type: 'prepare',
            });
          })
          .then((result: Untyped) =>
            send(port, {type: 'prepared', ok: result?.ok === true}),
          )
          .catch(() => send(port, {type: 'prepared', ok: false}))
          .finally(() => waiting.delete(port));
        return;
      }
      if (message?.type === 'heartbeat') return;
      if (message?.type === 'start') {
        if (
          typeof message.id !== 'string' ||
          typeof message.text !== 'string' ||
          message.text.length > MAX_PASTE ||
          jobs.has(message.id)
        ) {
          return;
        }
        const job: Job = {
          id: message.id,
          token: crypto.randomUUID(),
          text: message.text,
          original: message.text,
          prefix: namespace(),
          tabId,
          owner: port,
          theme: message.theme,
          categories: ALL_CATEGORIES,
          cloudCleanup: false,
          phase: 'scanning',
          timer: setTimeout(
            () => {
              send(port, {type: 'expired', id: message.id});
              release(message.id);
            },
            10 * 60 * 1000,
          ),
        };
        jobs.set(job.id, job);
        void browser.storage.sync
          .get(['cloudCleanup', 'pasteCategories'])
          .then((saved: Untyped) => {
            if (jobs.get(job.id) !== job) return;
            job.categories = normalizeCategories(saved.pasteCategories);
            job.cloudCleanup =
              saved.cloudCleanup === true &&
              allCategoriesSelected(job.categories);
            return scanJob(job);
          })
          .catch(() =>
            send(port, {
              type: 'failed',
              id: job.id,
              label:
                'Could not read privacy settings. Your paste is still held.',
            }),
          );
        return;
      }
      const job = jobs.get(message?.id);
      if (!job || job.owner !== port) return;
      if (message.type === 'cancel') {
        release(job.id);
        abandon();
        return;
      }
      if (message.type === 'inserted') {
        release(job.id);
        return;
      }
      if (message.type === 'theme') {
        job.theme = message.theme;
        send(job.review, {type: 'theme', theme: job.theme});
      }
      if (message.type === 'insert-failed') {
        job.phase = 'review';
        send(job.review, {type: 'insert-failed'});
        return;
      }
      if (message.type === 'context-changed') {
        job.contextChanged = true;
        if (job.report && job.phase !== 'cloud') requireReview(job);
      }
      if (message.type === 'review-window') {
        void browser.windows
          .create({
            url: browser.runtime.getURL(`review.html#${job.token}`),
            type: 'popup',
            width: 560,
            height: 680,
          })
          .then((window: Untyped) => {
            job.reviewTab = window.tabs?.[0]?.id;
            job.reviewWindow = window.id;
          });
      }
    });
    port.onDisconnect.addListener(() => {
      for (const job of jobs.values()) if (job.owner === port) release(job.id);
      abandon(port);
    });
  } else if (
    port.name.startsWith('review:') &&
    ownPage(sender, '/review.html')
  ) {
    const token = port.name.slice('review:'.length);
    const job = [...jobs.values()].find(j => j.token === token);
    // The unguessable token and extension origin authorize the private popup,
    // including when it connects before windows.create resolves with its tab
    // ID.
    if (!job) {
      port.disconnect();
      return;
    }
    if (job.review && job.review !== port) {
      send(job.review, {type: 'closed'});
      job.review.disconnect();
    }
    job.review = port;
    send(port, reviewState(job));
    send(job.owner, {type: 'review-ready', id: job.id});
    port.onMessage.addListener((message: Untyped) => {
      if (!jobs.has(job.id) || job.review !== port) return;
      if (message?.type === 'cancel') {
        send(job.owner, {type: 'canceled', id: job.id});
        release(job.id);
      }
      if (message?.type === 'settings') void browser.runtime.openOptionsPage();
      // User overrides from the review: paste the reviewed box as written, or
      // the original paste. Either ends checking for this paste; the inserted
      // text is not rescanned.
      if (
        (message?.type === 'use' || message?.type === 'ignore') &&
        job.phase !== 'ready'
      ) {
        const text = message.type === 'ignore' ? job.original : message.text;
        if (typeof text !== 'string' || text.length > MAX_PASTE) return;
        if (job.scanId) {
          void browser.runtime
            .sendMessage({target: 'scanner', type: 'cancel', id: job.scanId})
            .catch(() => {});
        }
        clearTimeout(job.scanTimer);
        job.scanId = undefined;
        job.cloudAbort?.abort();
        job.phase = 'ready';
        send(job.owner, {
          type: 'insert',
          id: job.id,
          cleaned: text,
          reviewed: true,
          override: message.type,
        });
        return;
      }
      if (message?.type === 'approve' && job.report && job.phase === 'review') {
        if (typeof message.edited === 'string' || message.rescan === true) {
          if (typeof message.edited === 'string') {
            if (message.edited.length > MAX_PASTE) return;
            // Edits invalidate the old scan. Never route edited preview text
            // directly.
            job.text = message.edited;
          }
          job.prefix = namespace();
          job.cloudDone = false;
          void scanJob(job);
          return;
        }
        if (!job.report.complete) {
          send(port, {
            type: 'error',
            message:
              'The full local identity check must finish. Scan again before pasting.',
          });
          return;
        }
        const kept = Array.isArray(message.kept)
          ? message.kept.filter((id: unknown) => typeof id === 'string')
          : [];
        if (job.cloudCleanup && !job.cloudDone && !job.cloudFailed) {
          const remove = job.report.findings
            .filter(
              d => privacyBucket(d) === 'cloud-cleanup' && !kept.includes(d.id),
            )
            .map(d => d.id);
          void runCloud(job, true, remove);
        } else {
          insertLocal(job, kept);
        }
      }
    });
    port.onDisconnect.addListener(() => {
      if (job.review === port) job.review = undefined;
    });
  }
});

browser.runtime.onMessage.addListener(
  (message: Untyped, sender: Untyped, respond: (value: Untyped) => void) => {
    if (
      message?.type === 'open-settings' &&
      sender?.id === browser.runtime.id &&
      siteFor(sender.url || '')
    ) {
      void browser.runtime.openOptionsPage();
      return;
    }
    if (message?.target === 'background' && ownPage(sender, '/scanner.html')) {
      const job = [...jobs.values()].find(j => j.scanId === message.id);
      if (!job || job.phase !== 'scanning') return;
      if (message.type === 'progress') {
        send(job.owner, {type: 'progress', id: job.id, label: message.label});
      }
      if (message.type === 'failed') {
        scanFailed(
          job,
          message.label || 'The scan stopped. Your paste is still held.',
        );
      }
      if (message.type === 'result') {
        if (job.phase !== 'scanning') return;
        clearTimeout(job.scanTimer);
        // The background owns the selection; a report cannot expand its cloud
        // authority.
        job.report = {...message.report, categories: [...job.categories]};
        if (job.report?.needsReview || job.contextChanged) {
          requireReview(job);
        } else if (job.report?.complete) {
          if (job.cloudCleanup && !job.cloudFailed) void runCloud(job);
          else insertLocal(job);
        }
      }
      return;
    }
    if (ownPage(sender, '/options.html') && message?.type === 'warm-scanner') {
      void scanner()
        .then(() =>
          browser.runtime.sendMessage({target: 'scanner', type: 'prepare'}),
        )
        .then(respond)
        .catch(() => respond({ok: false}));
      return true;
    }
    if (
      ownPage(sender, '/options.html') &&
      message?.type === 'scanner-status'
    ) {
      void scanner()
        .then(() =>
          browser.runtime.sendMessage({target: 'scanner', type: 'diagnostics'}),
        )
        .then(respond)
        .catch(() => respond({error: 'The local scanner did not respond.'}));
      return true;
    }
    if (
      ownPage(sender, '/options.html') &&
      (message?.type === 'test-scanner' ||
        message?.type === 'test-general' ||
        message?.type === 'test-500')
    ) {
      void browser.storage.sync
        .get('pasteCategories')
        .then(async (saved: Untyped) => {
          await scanner();
          return browser.runtime.sendMessage({
            target: 'scanner',
            type:
              message.type === 'test-general'
                ? 'self-test-general'
                : message.type === 'test-500'
                  ? 'self-test-500'
                  : 'self-test',
            categories: normalizeCategories(saved.pasteCategories),
          });
        })
        .then(respond)
        .catch(() =>
          respond({ok: false, error: 'The local scanner could not start.'}),
        );
      return true;
    }
    if (ownPage(sender, '/options.html') && message?.type === 'test-cloud') {
      void (async () => {
        try {
          const problem = cloudSetupProblem();
          if (problem) throw new Error(problem);
          await scanner();
          const local = await browser.runtime.sendMessage({
            target: 'scanner',
            type: 'self-test-hybrid',
          });
          if (!local?.ok) {
            throw new Error(local?.error || 'The local test did not finish.');
          }
          // The fixed sample is authored and reviewed here. User text cannot
          // enter this path.
          const input = prepareCloudInput(
            CLOUD_TEST_TEXT,
            local.report,
            'DEMO',
            true,
          );
          if (
            /Avery Bennett|avery@example.com|202\) 555-0147/.test(input.text)
          ) {
            throw new Error(
              'The fictional identifiers were not fully removed. Cloud test held.',
            );
          }
          const started = performance.now();
          const result = await cleanupCloud(input);
          respond({
            ok: true,
            localMs: local.elapsed,
            cloudMs: Math.round(performance.now() - started),
            preview: input.text,
            cleaned: result.report.cleaned,
            needsReview: result.report.needsReview,
            healthRemoved: !/diabetes|metformin/i.test(result.report.cleaned),
          });
        } catch (error) {
          respond({
            ok: false,
            error:
              error instanceof Error
                ? error.message
                : 'The connection test did not finish.',
          });
        }
      })();
      return true;
    }
  },
);
browser.action.onClicked.addListener(() => {
  void browser.runtime.openOptionsPage();
});
browser.runtime.onStartup.addListener(() => {
  void preload();
});
browser.storage.onChanged?.addListener((changes: Untyped, area: string) => {
  if (area === 'sync' && changes.preloadAtStartup?.newValue === true) {
    void preload();
  }
});
browser.runtime.onInstalled.addListener((details: Untyped) => {
  void preload();
  if (details.reason === 'install') void browser.runtime.openOptionsPage();
});
browser.tabs.onRemoved.addListener((tabId: number) => {
  for (const job of jobs.values()) if (job.tabId === tabId) release(job.id);
});
