/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Local evaluation harness only; not part of either production
 * build.
 */

import {extract, prepareModel} from './extension/model';
import {makeReport} from './extension/policy';
import {NO_TOPICS} from './core/redact';
import {prepareCloudInput} from './core/cloud-gate';

const status = document.querySelector('#status')!;
const run = document.querySelector<HTMLButtonElement>('#run')!;
const stop = document.querySelector<HTMLButtonElement>('#stop')!;
const token = location.hash.slice(1);
const savedFetch = window.fetch.bind(window);
let stopped = false;
const api = async (path: string, body?: object) => {
  const response = await savedFetch(`/__corpus/${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      ...(body ? {'Content-Type': 'application/json'} : {}),
    },
    ...(body ? {method: 'POST', body: JSON.stringify(body)} : {}),
  });
  if (!response.ok) {
    throw new Error(`Local runner returned ${response.status}.`);
  }
  return response.json();
};
const output = (s: string) => {
  status.textContent = s;
};
stop.onclick = () => {
  stopped = true;
  stop.disabled = true;
  output('Stopping after this file…');
};
run.onclick = async () => {
  run.disabled = true;
  stop.disabled = false;
  stopped = false;
  const original = {
    fetch: window.fetch,
    xhr: window.XMLHttpRequest,
    socket: window.WebSocket,
    beacon: navigator.sendBeacon,
  };
  let blocked = 0;
  const block = () => {
    blocked++;
    throw new Error('Network access is blocked during local inference.');
  };
  // The only permitted transport is the saved same-origin helper above. The
  // page also has a connect-src 'self' policy. Raw input never enters a cloud
  // helper.
  window.fetch = block;
  window.XMLHttpRequest = block as unknown as typeof XMLHttpRequest;
  window.WebSocket = block as unknown as typeof WebSocket;
  navigator.sendBeacon = block;
  try {
    const manifest = await api('manifest');
    output(`Preparing Nano for ${manifest.total} documents…`);
    await prepareModel(false, output);
    const start = performance.now();
    let done = manifest.completed;
    for (const index of manifest.pending) {
      if (stopped) break;
      const document = await api(`document/${index}`);
      const at = performance.now();
      const firstBlocked = blocked;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 180000);
      let report;
      let evidence;
      let failure: string | undefined;
      try {
        evidence = await extract(document.text, controller.signal, message =>
          output(
            `${done}/${manifest.total} complete · ${document.name}\n${message}`,
          ),
        );
        report = makeReport(
          document.text,
          evidence.names,
          evidence.topics,
          evidence.ambiguous,
          'CORPUS',
          true,
          undefined,
          evidence.identifying,
        );
      } catch (error) {
        failure = error instanceof Error ? error.message : 'Local scan failed.';
        report = makeReport(
          document.text,
          {people: [], companies: []},
          NO_TOPICS,
          [],
          'CORPUS',
          false,
          failure,
        );
      } finally {
        clearTimeout(timer);
      }
      let gate = report.needsReview ? 'held-for-review' : 'eligible';
      let gateReason: string | undefined;
      if (!report.needsReview) {
        try {
          prepareCloudInput(document.text, report, 'CORPUS');
        } catch (error) {
          gate = 'held-by-final-check';
          gateReason =
            error instanceof Error ? error.message : 'Final check failed.';
        }
      }
      await api('result', {
        index,
        textHash: document.textHash,
        elapsedMs: performance.now() - at,
        report,
        evidence,
        failure,
        gate,
        gateReason,
        blockedNetworkAttempts: blocked - firstBlocked,
      });
      done++;
      output(
        `${done}/${manifest.total} complete\nElapsed: ${Math.round((performance.now() - start) / 1000)} seconds\nBlocked network attempts: ${blocked}`,
      );
      // Yield so browser input and stop remain responsive.
      await new Promise(resolve => setTimeout(resolve, 0));
    }
    await api('status', {
      state: stopped ? 'stopped' : 'complete',
      blockedNetworkAttempts: blocked,
    });
    output(
      `${stopped ? 'Stopped' : 'Complete'}: ${done}/${manifest.total}\nBlocked network attempts: ${blocked}`,
    );
  } catch (error) {
    output(error instanceof Error ? error.message : 'Evaluation failed.');
    await api('status', {
      state: 'failed',
      error: status.textContent,
      blockedNetworkAttempts: blocked,
    }).catch(() => {});
  } finally {
    window.fetch = original.fetch;
    window.XMLHttpRequest = original.xhr;
    window.WebSocket = original.socket;
    navigator.sendBeacon = original.beacon;
    run.disabled = false;
    stop.disabled = true;
  }
};
