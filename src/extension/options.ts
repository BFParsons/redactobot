/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The settings page: prepares and tests the on-device model, and
 * saves the site, category, cloud cleanup and startup choices.
 */

import {browser, type Site, type Untyped} from './protocol';
import {prepareModel, readiness, releasePreparedModel} from './model';
import {cloudSetupProblem} from '../core/cloud-client';
import {abortable} from '../core/abortable';
import {installCategorySettings} from './category-settings';
import {allCategoriesSelected} from './categories';
const status = document.querySelector<HTMLElement>('#status')!;
const prepare = document.querySelector<HTMLButtonElement>('#prepare')!;
const test = document.querySelector<HTMLButtonElement>('#test')!;
const testGeneral = document.querySelector<HTMLButtonElement>('#test-general')!;
const test500 = document.querySelector<HTMLButtonElement>('#test-500')!;
let actionStarted = false;
function busy(value: boolean) {
  if (value) actionStarted = true;
  test500.disabled = value;
  testGeneral.disabled = value;
  test.disabled = value;
  prepare.disabled = value;
}
async function testPaste(type: 'test-scanner' | 'test-general' | 'test-500') {
  busy(true);
  status.textContent = 'Testing a sample paste on this device…';
  try {
    const result = await browser.runtime.sendMessage({type});
    const reasons = result?.ok
      ? [
          ...new Set([
            ...result.report.reasons,
            ...result.report.findings
              .map((finding: {reviewReason?: string}) => finding.reviewReason)
              .filter(Boolean),
          ]),
        ]
      : [];
    status.textContent = result?.ok
      ? `On-device scan completed in ${(result.elapsed / 1000).toFixed(2)} seconds. ${result.report.findings.length} details found. ${result.report.needsReview ? `Review would be requested. ${reasons.join(' ')}` : 'The cleaned text would paste automatically.'} ${result.timings ? `Startup: ${result.timings.prepare} ms. AI: ${result.timings.inference} ms. Local checks: ${result.timings.local} ms.` : ''} Result: ${result.report.cleaned}`
      : result?.error || 'The local scan did not finish.';
  } catch {
    status.textContent =
      'The scanner disconnected. Reload the extension and try again.';
  } finally {
    busy(false);
  }
}
test.addEventListener('click', () => void testPaste('test-scanner'));
testGeneral.addEventListener('click', () => void testPaste('test-general'));
test500.addEventListener('click', () => void testPaste('test-500'));
document
  .querySelector<HTMLButtonElement>('#check-scanner')!
  .addEventListener('click', async () => {
    const output = document.querySelector('#scanner-status')!;
    output.textContent = 'Checking scanner status…';
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);
    try {
      const result = await abortable<Untyped>(
        browser.runtime.sendMessage({type: 'scanner-status'}),
        controller.signal,
      );
      if (result?.error || !result?.model) {
        throw new Error(
          result?.error || 'The scanner did not return its status.',
        );
      }
      output.textContent = result.active
        ? `${result.active.kind === 'paste' ? 'A paste check' : 'A diagnostic test'} is ${result.active.stage} (${Math.round(result.active.elapsedMs / 1000)} seconds). ${result.waiting} checks waiting.`
        : result.model.ready
          ? 'Ready for pastes. No checks waiting.'
          : result.model.preparing
            ? 'On-device AI is starting. No check is running.'
            : 'The model needs preparation.';
      if (result.lastTimeout) {
        output.textContent += ` Last timeout: ${result.lastTimeout.stage}${result.lastTimeout.blocker ? `, waiting behind a ${result.lastTimeout.blocker.kind} check (${Math.round(result.lastTimeout.blocker.elapsedMs / 1000)} seconds)` : ''}.`;
      }
    } catch (error) {
      output.textContent =
        error instanceof Error ? error.message : 'The scanner did not respond.';
    } finally {
      clearTimeout(timeout);
    }
  });
const labels: Record<string, string> = {
  unsupported: 'On-device AI is not supported in this browser.',
  unavailable: 'On-device AI is unavailable on this device.',
  downloadable:
    'Prepare the model before your first paste. Chrome may download it.',
  downloading: 'Chrome is downloading the on-device model.',
  available:
    'The on-device model is available. Prepare it to warm up scanning.',
};
void readiness()
  .then(state => {
    if (!actionStarted) status.textContent = labels[state] || state;
  })
  .catch(error => {
    if (!actionStarted) {
      status.textContent =
        error instanceof Error
          ? error.message
          : 'Could not check the model. Try preparing it below.';
    }
  });
prepare.addEventListener('click', async () => {
  busy(true);
  const started = performance.now();
  let phase = 'Checking on-device AI…';
  const progress = (message: string) => {
    phase = message;
    status.textContent = message;
  };
  progress(phase);
  const elapsed = setInterval(() => {
    status.textContent = `${phase} ${Math.floor((performance.now() - started) / 1000)} seconds elapsed.`;
  }, 1000);
  try {
    // Download may need a gesture in this visible page. Once installed, only
    // the actual offscreen scanner should own a session; do not initialize a
    // second one.
    if ((await readiness()) !== 'available') await prepareModel(true, progress);
    progress('Starting the paste scanner…');
    const controller = new AbortController();
    const deadline = setTimeout(
      () =>
        controller.abort(
          new Error(
            'The paste scanner did not respond. Try preparing it again.',
          ),
        ),
      155000,
    );
    try {
      const result = await abortable<
        {ok?: boolean; error?: string} | undefined
      >(browser.runtime.sendMessage({type: 'warm-scanner'}), controller.signal);
      status.textContent = result?.ok
        ? 'Ready. Reload an AI chat tab, then paste to try it.'
        : result?.error ||
          'The paste scanner could not start. Try preparing it again.';
    } finally {
      clearTimeout(deadline);
    }
  } catch (error) {
    status.textContent =
      error instanceof Error
        ? error.message
        : 'Could not prepare on-device AI.';
  } finally {
    clearInterval(elapsed);
    releasePreparedModel();
    busy(false);
  }
});
const sites: Site[] = ['chatgpt', 'claude', 'gemini'];
const cloudToggle = document.querySelector<HTMLInputElement>('#cloud-cleanup')!;
const cloudStatus = document.querySelector<HTMLElement>('#cloud-status')!;
const cloudProblem = cloudSetupProblem();
cloudToggle.disabled = !!cloudProblem;
cloudStatus.textContent =
  cloudProblem ||
  'Available. Cloud cleanup is optional; it never receives the identity mapping or chat history.';
installCategorySettings(categories => {
  cloudStatus.textContent =
    cloudProblem ||
    (allCategoriesSelected(categories)
      ? 'Available. Cloud cleanup is optional; it never receives the identity mapping or chat history.'
      : 'Cloud cleanup is paused for this selection. Pastes stay on this device. Choose All categories to use cloud cleanup; your cloud preference is remembered.');
});
const cloudTest = document.querySelector<HTMLButtonElement>('#test-cloud')!;
cloudTest.disabled = !!cloudProblem;
cloudTest.addEventListener('click', async () => {
  cloudTest.disabled = true;
  cloudStatus.textContent =
    'Testing a fixed fictional sample: local identity check, then cloud cleanup…';
  try {
    const result = await browser.runtime.sendMessage({type: 'test-cloud'});
    cloudStatus.textContent = result?.ok
      ? `Firebase connection succeeded. Local scan: ${(result.localMs / 1000).toFixed(2)} s. Cloud cleanup: ${(result.cloudMs / 1000).toFixed(2)} s. ${result.healthRemoved ? 'Fictional medical details removed.' : 'Some fictional medical details remain; review needed.'} ${result.needsReview ? 'Human review would be requested.' : ''} Cloud received: ${result.preview} Result: ${result.cleaned}`
      : result?.error || 'The cloud connection test did not finish.';
  } catch {
    cloudStatus.textContent =
      'The test disconnected. Reload the extension and try again.';
  } finally {
    cloudTest.disabled = !!cloudProblem;
  }
});
void browser.storage.sync.get('cloudCleanup').then((saved: Untyped) => {
  cloudToggle.checked = saved.cloudCleanup === true;
});
// Optional: load the model at Chrome startup. Off by default, so nothing loads
// until a switch is on.
const startupToggle =
  document.querySelector<HTMLInputElement>('#preload-startup')!;
void browser.storage.sync.get('preloadAtStartup').then((saved: Untyped) => {
  startupToggle.checked = saved.preloadAtStartup === true;
});
startupToggle.addEventListener('change', () => {
  void browser.storage.sync
    .set({preloadAtStartup: startupToggle.checked})
    .catch(() => {
      startupToggle.checked = !startupToggle.checked;
    });
});
cloudToggle.addEventListener('change', () => {
  void browser.storage.sync
    .set({cloudCleanup: cloudToggle.checked})
    .catch(() => {
      cloudToggle.checked = !cloudToggle.checked;
      cloudStatus.textContent = 'Could not save this setting. Try again.';
    });
});
browser.storage.onChanged.addListener((changes: Untyped, area: string) => {
  if (area === 'sync' && changes.cloudCleanup) {
    cloudToggle.checked = changes.cloudCleanup.newValue === true;
  }
  if (area !== 'sync' || !changes.sites) return;
  for (const site of sites) {
    document.querySelector<HTMLInputElement>(`#${site}`)!.checked =
      changes.sites.newValue?.[site] !== false;
  }
});
void browser.storage.sync.get('sites').then((saved: Untyped) => {
  for (const site of sites) {
    const input = document.querySelector<HTMLInputElement>(`#${site}`)!;
    input.checked = saved.sites?.[site] !== false;
    input.addEventListener('change', async () => {
      const current = await browser.storage.sync.get('sites');
      await browser.storage.sync.set({
        sites: {...current.sites, [site]: input.checked},
      });
    });
  }
});
