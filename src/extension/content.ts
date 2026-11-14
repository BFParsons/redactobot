/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Content script for the supported chat sites. Holds pasted or
 * dropped text, has it scanned and inserts the cleaned text into the composer.
 */

import {
  browser,
  siteFor,
  MAX_PASTE,
  type RuntimePort,
  type Site,
  type Untyped,
} from './protocol';
import {applyTheme, themeFor} from './themes';
import {
  capture,
  composerFor,
  composersFor,
  editorValue,
  insert,
  unchanged,
  type Snapshot,
} from './editor';
import {InlineStatus} from './inline-status';
import {PasteToggle} from './paste-toggle';

interface Pending {
  id: string;
  text: string;
  snapshot: Snapshot;
  port?: RuntimePort;
  frame?: HTMLIFrameElement;
  heartbeat?: ReturnType<typeof setInterval>;
  reviewReady?: boolean;
  label?: string;
  failed?: boolean;
}
interface Transport {
  connect(): RuntimePort;
  reviewUrl(token: string): string;
  settings(): void;
}
const style = `
:host{all:initial;color:var(--rb-text);font:var(--rb-fontStyle) var(--rb-fontWeight) var(--rb-fontSize)/var(--rb-lineHeight) var(--rb-font);letter-spacing:var(--rb-letterSpacing);color-scheme:inherit}
*{box-sizing:border-box}.status{display:flex;align-items:center;gap:.5em;width:100%;min-height:var(--rb-status-height);margin:0;padding:0;border:0;border-radius:0;background:var(--rb-surface);color:var(--rb-muted);font:var(--rb-fontStyle) var(--rb-fontWeight) var(--rb-fontSize)/var(--rb-lineHeight) var(--rb-font);letter-spacing:var(--rb-letterSpacing);box-shadow:none;pointer-events:none}
.mark{width:.8em;height:.8em;flex:none;border:1.5px solid currentColor;border-right-color:transparent;border-radius:50%;animation:rb-spin .8s linear infinite}.attention .mark{animation:none;border:0;border-radius:0}
button{font:inherit;letter-spacing:inherit;border:0;background:transparent;color:var(--rb-muted);cursor:pointer;padding:0 .25em;border-radius:4px;white-space:nowrap;pointer-events:auto}button:hover{color:var(--rb-text)}button:focus-visible{outline:2px solid var(--rb-accent);outline-offset:2px}.cancel{width:1.5em;flex:none;padding:0}
.label{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.review{pointer-events:auto;width:min(520px,calc(100vw - 32px));height:min(610px,calc(100vh - 32px));border:1px solid var(--rb-border);border-radius:var(--rb-radius);background:var(--rb-surface);box-shadow:0 14px 50px #0003;overflow:hidden}.review iframe{width:100%;height:100%;border:0;display:block}
@keyframes rb-spin{to{transform:rotate(360deg)}}@media(prefers-reduced-motion:reduce){.mark{animation:none}}
`;

/**
 * Installs paste and drop interception, the status UI and the on/off switch for
 * `site`. Protection starts switched off.
 *
 * @param trustedOnly When true, ignores paste and drop events that a script
 *     generated.
 * @return Controls to switch protection on or off and to remove everything this
 *     call installed.
 */
export function installPasteGuard(
  site: Site,
  transport: Transport,
  trustedOnly = true,
) {
  // Clean up the retired 0.1 launcher's persistent badge, including a copy left
  // in an open page after that extension was disabled or replaced.
  const removeLegacyBadge = () =>
    document.getElementById('client-safe-ai-host')?.remove();
  removeLegacyBadge();
  const host = document.createElement('redactobot-paste-guard');
  host.style.cssText =
    'all:initial;position:fixed;z-index:2147483647;display:none;pointer-events:none;';
  const root = host.attachShadow({mode: 'closed'});
  const sheet = document.createElement('style');
  sheet.textContent = style;
  root.append(sheet);
  const box = document.createElement('div');
  root.append(box);
  let active: Pending | undefined;
  let queue: Pending[] = [];
  // Off on every page load; the switch applies to this tab only.
  let enabled = false;
  function setEnabled(value: boolean) {
    enabled = value;
    toggle.setEnabled(value);
    if (!value) {
      // Switching off stops everything at once: the held paste, the bar, and
      // the model start.
      queue = [];
      cancel();
      if (stopWarming) stopWarming(true);
      else toggle.stopWarming(false);
    } else {
      warm();
    }
  }
  const toggle = new PasteToggle(
    site,
    async value => {
      setEnabled(value);
    },
    transport.settings,
  );
  toggle.setEnabled(false);
  const inline = new InlineStatus();
  const resize =
    typeof ResizeObserver === 'undefined'
      ? undefined
      : new ResizeObserver(() => position());
  let delay: ReturnType<typeof setTimeout> | undefined;
  let notice: ReturnType<typeof setTimeout> | undefined;
  let lastPage = location.href;
  let warmed = false;
  let stopWarming: ((abandon?: boolean) => void) | undefined;
  let lastTheme = '';
  let lastComposer: HTMLElement | undefined;
  let inserting = false;
  let disposed = false;
  function mount() {
    if (!host.isConnected && document.documentElement) {
      document.documentElement.append(host);
    }
  }
  function position() {
    if (inserting || disposed) return;
    toggle.refresh();
    const composer = active?.snapshot.composer || lastComposer;
    if (!composer) return;
    if (host.style.display !== 'none') mount();
    const theme = themeFor(site, composer);
    const encoded = JSON.stringify(theme);
    if (encoded !== lastTheme) {
      lastTheme = encoded;
      applyTheme(host, theme);
      try {
        active?.port?.postMessage({type: 'theme', id: active.id, theme});
      } catch {
        /* disconnected */
      }
    }
    if (active?.frame) {
      inline.reset();
      const r = composer.getBoundingClientRect();
      const width = Math.min(520, innerWidth - 32);
      host.style.width = `${width}px`;
      host.style.left = `${Math.max(16, Math.min(r.right - width, innerWidth - width - 16))}px`;
      host.style.top = `${Math.max(16, Math.min(r.top - Math.min(610, innerHeight - 32) - 12, innerHeight - Math.min(610, innerHeight - 32) - 16))}px`;
    } else if (host.style.display !== 'none') {
      inline.place(host, composer);
    }
  }
  function button(label: string, action: () => void) {
    const node = document.createElement('button');
    node.type = 'button';
    node.textContent = label;
    node.addEventListener('click', action);
    return node;
  }
  function status(
    label: string,
    done = false,
    extra?: {label: string; action: () => void},
  ) {
    mount();
    clearTimeout(delay);
    clearTimeout(notice);
    if (active) active.frame = undefined;
    const p = document.createElement('div');
    p.className = `status${done ? ' attention' : ''}`;
    p.setAttribute('role', 'status');
    p.setAttribute('aria-live', 'polite');
    const mark = document.createElement('span');
    mark.className = 'mark';
    mark.setAttribute('aria-hidden', 'true');
    mark.textContent = done ? '!' : '';
    const words = document.createElement('span');
    words.className = 'label';
    words.textContent = label;
    words.title = label;
    p.append(mark, words);
    if (extra) p.append(button(extra.label, extra.action));
    if (active) {
      const stop = button('×', () => cancel());
      stop.className = 'cancel';
      stop.title = 'Cancel paste';
      stop.setAttribute('aria-label', 'Cancel paste');
      p.append(stop);
    }
    resize?.disconnect();
    const composer = active?.snapshot.composer || lastComposer;
    if (composer) resize?.observe(composer);
    box.replaceChildren(p);
    host.style.display = 'block';
    position();
  }
  function removeUI() {
    clearTimeout(delay);
    clearTimeout(notice);
    host.style.display = 'none';
    box.replaceChildren();
    inline.reset();
    resize?.disconnect();
  }
  function finish() {
    const previous = active;
    active = undefined;
    if (previous?.heartbeat) clearInterval(previous.heartbeat);
    if (previous && !stopWarming) toggle.stopWarming(false);
    previous?.port?.disconnect();
    if (queue.length) start(queue.shift()!);
  }
  function cancel() {
    try {
      if (active) active.port?.postMessage({type: 'cancel', id: active.id});
    } catch {
      /* disconnected */
    }
    removeUI();
    finish();
  }
  function review(token: string) {
    if (!active || active.frame) return;
    const job = active;
    mount();
    clearTimeout(delay);
    const panel = document.createElement('div');
    panel.className = 'review';
    const iframe = document.createElement('iframe');
    iframe.src = transport.reviewUrl(token);
    iframe.title = 'Review sensitive details — Redactobot';
    panel.append(iframe);
    box.replaceChildren(panel);
    job.frame = iframe;
    host.style.display = 'block';
    position();
    // If the site's policies block embedded extension pages, open the same
    // private review in an extension popup only after the user asks for it.
    setTimeout(() => {
      if (active === job && !job.reviewReady) {
        job.frame = undefined;
        status('Review needed before pasting', false, {
          label: 'Review',
          action: () =>
            job.port?.postMessage({type: 'review-window', id: job.id}),
        });
      }
    }, 2500);
  }
  function accept(job: Pending, message: Untyped) {
    if (active !== job || job.failed) return;
    // "Use this text" and "Ignore" are explicit choices made in the review. If
    // the draft changed meanwhile, add the text at the end of the current draft
    // instead of failing.
    if (message.override && !unchanged(job.snapshot)) {
      const composer = job.snapshot.composer.isConnected
        ? job.snapshot.composer
        : composersFor(site)[0];
      if (composer) {
        const value = editorValue(composer);
        job.snapshot = {
          composer,
          value,
          start: value.length,
          end: value.length,
          page: location.href,
        };
      }
    }
    if (!unchanged(job.snapshot)) {
      job.port?.postMessage({
        type: message.override ? 'insert-failed' : 'context-changed',
        id: job.id,
      });
      return;
    }
    const previous = job.snapshot;
    let inserted = false;
    inserting = true;
    try {
      inline.reset();
      inserted = insert(previous, message.cleaned);
    } finally {
      inserting = false;
    }
    if (!inserted) {
      job.port?.postMessage({
        type: message.override ? 'insert-failed' : 'context-changed',
        id: job.id,
      });
      return;
    }
    const after = capture(previous.composer);
    for (const waiting of queue) {
      if (
        after &&
        waiting.snapshot.composer === previous.composer &&
        waiting.snapshot.value === previous.value &&
        waiting.snapshot.start === previous.start &&
        waiting.snapshot.end === previous.end
      ) {
        waiting.snapshot = {...after};
      }
    }
    job.port?.postMessage({type: 'inserted', id: job.id});
    removeUI();
    finish();
  }
  function failed(job: Pending, label: string, settings = false) {
    if (active !== job || job.failed) return;
    job.failed = true;
    clearInterval(job.heartbeat);
    try {
      job.port?.postMessage({type: 'cancel', id: job.id});
    } catch {
      /* disconnected */
    }
    job.port?.disconnect();
    status(
      label,
      true,
      settings
        ? {label: 'Settings', action: transport.settings}
        : {
            label: 'Retry',
            action: () => {
              if (active !== job) return;
              active = undefined;
              removeUI();
              start({
                ...job,
                id: crypto.randomUUID(),
                port: undefined,
                frame: undefined,
                reviewReady: false,
                failed: false,
                label: undefined,
              });
            },
          },
    );
  }
  function start(job: Pending) {
    active = job;
    lastComposer = job.snapshot.composer;
    lastTheme = '';
    try {
      const port = transport.connect();
      job.port = port;
      port.onMessage.addListener((message: Untyped) => {
        if (active !== job || job.failed || message.id !== job.id) return;
        if (message.type === 'progress') {
          // A paste that has to wait for a cold model shows the same bar under
          // the chat box.
          if (/^Starting on-device/.test(message.label)) toggle.startWarming();
          else if (toggle.warming) toggle.stopWarming(true);
        }
        if (message.type === 'progress' && !job.frame) {
          job.label = message.label;
          // Do not flash a UI for a scan that finishes before the delay.
          if (host.style.display !== 'none') status(message.label);
        }
        if (message.type === 'insert') accept(job, message);
        if (message.type === 'review') review(message.token);
        if (message.type === 'review-ready') job.reviewReady = true;
        if (message.type === 'canceled') {
          removeUI();
          finish();
        }
        if (message.type === 'failed' || message.type === 'expired') {
          failed(
            job,
            message.label || 'The scan expired. Retry or paste new text.',
          );
        }
      });
      port.onDisconnect.addListener(() => {
        if (active === job) {
          failed(job, 'Protection stopped. Your paste was not inserted.', true);
        }
      });
      job.heartbeat = setInterval(() => {
        try {
          port.postMessage({type: 'heartbeat'});
        } catch {
          /* onDisconnect handles this */
        }
      }, 20000);
      delay = setTimeout(() => {
        if (active === job && !job.frame) {
          status(job.label || 'Redactobot is checking your paste…');
        }
      }, 180);
      port.postMessage({
        type: 'start',
        id: job.id,
        text: job.text,
        theme: themeFor(site, job.snapshot.composer),
      });
    } catch {
      failed(
        job,
        'Protection needs to be reloaded. Your paste is still held.',
        true,
      );
    }
  }
  // Show a short notice without disturbing a scan or an open review. With a job
  // running, the notice reverts to that job's own status; an open review is
  // left alone.
  function notify(label: string, composer: HTMLElement) {
    if (active?.frame) return;
    if (!active) lastComposer = composer;
    status(label, true);
    notice = setTimeout(() => {
      if (active && !active.frame) {
        status(active.label || 'Redactobot is checking your paste…');
      } else if (!active) {
        removeUI();
      }
    }, 5000);
  }
  // Paste and drop share one gate. Text travelling with files (Excel and Word
  // put an image of the selection beside the text) is still held and scrubbed;
  // the files are dropped with it. File-only transfers are uploads, which the
  // extension does not cover.
  const guardTransfer = (
    event: Event,
    data: DataTransfer | null | undefined,
  ) => {
    if (!enabled || (trustedOnly && !event.isTrusted)) return;
    const composer = composerFor(event, site);
    if (!composer) return;
    const text = data?.getData('text/plain');
    if (!text) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    if (event.type === 'drop') {
      composer.focus({preventScroll: true});
      const at =
        composer instanceof HTMLTextAreaElement
          ? undefined
          : document.caretRangeFromPoint?.(
              (event as DragEvent).clientX,
              (event as DragEvent).clientY,
            );
      if (at && composer.contains(at.startContainer)) {
        const selection = getSelection();
        selection?.removeAllRanges();
        selection?.addRange(at);
      }
    }
    const snapshot = capture(composer);
    if (!snapshot) {
      notify(
        'Could not read the cursor position. Select the chat box and paste again.',
        composer,
      );
      return;
    }
    if (text.length > MAX_PASTE) {
      notify('This paste is too large. Split it into smaller parts.', composer);
      return;
    }
    const job: Pending = {id: crypto.randomUUID(), text, snapshot};
    // A fresh paste replaces an unsuccessful attempt. Never leave it waiting
    // behind a failed job, or later insert stale text queued behind that
    // failure.
    if (active?.failed) {
      queue = [];
      cancel();
    }
    if (active) {
      if (queue.length < 5) queue.push(job);
      else notify('Finish the current review, then paste again.', composer);
    } else {
      start(job);
    }
  };
  const paste = (event: ClipboardEvent) =>
    guardTransfer(event, event.clipboardData);
  const drop = (event: DragEvent) => guardTransfer(event, event.dataTransfer);
  function warm() {
    if (warmed || !enabled || disposed) return;
    warmed = true;
    try {
      const port = transport.connect();
      let confirmed = false;
      // Keep the service worker alive until preparation finishes. No pasted or
      // page text enters this message. The offscreen document retains the
      // text-free base.
      const heartbeat = setInterval(() => {
        try {
          port.postMessage({type: 'heartbeat'});
        } catch {
          /* disconnect handles this */
        }
      }, 20000);
      const timer = setTimeout(() => {
        warmed = false;
        stop();
      }, 155000);
      // A warm model answers at once; only a real cold start (Chrome reloading
      // the model) shows the progress bar under the chat box.
      const slow = setTimeout(() => toggle.startWarming(), 700);
      let ended = false;
      const stop = (abandon = false) => {
        ended = true;
        clearInterval(heartbeat);
        clearTimeout(timer);
        clearTimeout(slow);
        stopWarming = undefined;
        if (abandon) {
          warmed = false;
          try {
            port.postMessage({type: 'cancel-prepare'});
          } catch {
            /* disconnected */
          }
        }
        port.disconnect();
        if (!confirmed && !active) toggle.stopWarming(false);
      };
      stopWarming = stop;
      port.onMessage.addListener(message => {
        if (!ended && message.type === 'prepared') {
          warmed = message.ok === true;
          confirmed = warmed;
          toggle.stopWarming(confirmed);
          stop();
        }
      });
      port.onDisconnect.addListener(() => {
        clearInterval(heartbeat);
        clearTimeout(timer);
        clearTimeout(slow);
        if (!confirmed) {
          warmed = false;
          if (!active) toggle.stopWarming(false);
        }
      });
      port.postMessage({type: 'prepare'});
    } catch {
      warmed = false;
    }
  }
  const focus = (event: FocusEvent) => {
    if (composerFor(event, site)) warm();
  };
  // Chrome unloads its on-device model when idle, and reloading takes minutes.
  // While this chat tab is visible with protection on, keep it loaded with
  // text-free prepare requests (the scanner touches the model only if it has
  // been idle), and wake it as soon as the user returns to the tab.
  const keepAlive = () => {
    if (
      disposed ||
      !enabled ||
      active ||
      document.visibilityState !== 'visible'
    ) {
      return;
    }
    stopWarming?.();
    warmed = false;
    warm();
  };
  const keepAliveTimer = setInterval(keepAlive, 60_000);
  document.addEventListener('visibilitychange', keepAlive);
  // Window capture at document_start runs before the site's document/element
  // paste handlers.
  window.addEventListener('paste', paste, true);
  window.addEventListener('drop', drop, true);
  window.addEventListener('focusin', focus, true);
  window.addEventListener('resize', position, {passive: true});
  window.addEventListener('scroll', position, {capture: true, passive: true});
  window.addEventListener('input', position, true);
  const media = matchMedia('(prefers-color-scheme: dark)');
  media.addEventListener('change', position);
  let scheduled = false;
  const observer = new MutationObserver(records => {
    removeLegacyBadge();
    if (
      scheduled ||
      records.every(
        r =>
          r.target === host ||
          toggle.owns(r.target) ||
          (r.type === 'childList' &&
            [...r.addedNodes, ...r.removedNodes].every(
              node =>
                node instanceof Element &&
                node.matches('redactobot-paste-toggle'),
            )),
      )
    ) {
      return;
    }
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      position();
    });
  });
  const observe = () => {
    if (disposed) return;
    removeLegacyBadge();
    mount();
    toggle.refresh();
    if (document.documentElement) {
      observer.observe(document.documentElement, {
        childList: true,
        attributes: true,
        attributeFilter: [
          'class',
          'style',
          'data-theme',
          'data-mode',
          'data-color-scheme',
        ],
        subtree: true,
      });
    }
  };
  if (document.documentElement) observe();
  else document.addEventListener('DOMContentLoaded', observe, {once: true});
  const navigation = setInterval(() => {
    if (location.href !== lastPage) {
      lastPage = location.href;
      queue = [];
      cancel();
      stopWarming?.();
      warmed = false;
      warm();
    }
  }, 500);
  return {
    setEnabled,
    dispose() {
      disposed = true;
      queue = [];
      cancel();
      stopWarming?.();
      clearInterval(navigation);
      clearInterval(keepAliveTimer);
      document.removeEventListener('visibilitychange', keepAlive);
      observer.disconnect();
      toggle.dispose();
      host.remove();
      window.removeEventListener('paste', paste, true);
      window.removeEventListener('drop', drop, true);
      window.removeEventListener('focusin', focus, true);
      window.removeEventListener('resize', position);
      window.removeEventListener('scroll', position, true);
      window.removeEventListener('input', position, true);
      media.removeEventListener('change', position);
    },
  };
}

if (browser?.runtime?.id && window.top === window) {
  const site = siteFor(location.href);
  if (site) {
    // Settings choose the sites that show the Redactobot switch. The switch
    // itself always starts off and is never saved, so each page load begins
    // unprotected and unloaded.
    let guard: ReturnType<typeof installPasteGuard> | undefined;
    const show = (on: boolean) => {
      if (on && !guard) {
        guard = installPasteGuard(site, {
          connect: () => browser.runtime.connect({name: 'paste-guard'}),
          reviewUrl: token => browser.runtime.getURL(`review.html#${token}`),
          settings: () => {
            void browser.runtime.sendMessage({type: 'open-settings'});
          },
        });
      }
      if (!on && guard) {
        guard.dispose();
        guard = undefined;
      }
    };
    void browser.storage.sync
      .get('sites')
      .then((saved: Untyped) => show(saved.sites?.[site] !== false));
    browser.storage.onChanged.addListener((changes: Untyped, area: string) => {
      if (area === 'sync' && changes.sites) {
        show(changes.sites.newValue?.[site] !== false);
      }
    });
  }
}
