/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {afterEach, beforeEach, describe, expect, it, vi} from 'vitest';
import {installPasteGuard} from './content';
import {capture, insert} from './editor';
import type {RuntimePort} from './protocol';

class Port implements RuntimePort {
  name = 'test';
  sent: any[] = [];
  listeners: Array<(message: any) => void> = [];
  disconnectors: Array<() => void> = [];
  onMessage = {
    addListener: (fn: (message: any) => void) => this.listeners.push(fn),
  };
  onDisconnect = {addListener: (fn: () => void) => this.disconnectors.push(fn)};
  postMessage(message: any) {
    this.sent.push(message);
  }
  disconnected = false;
  disconnect() {
    this.disconnected = true;
    this.disconnectors.forEach(fn => fn());
  }
  emit(message: any) {
    this.listeners.forEach(fn => fn(message));
  }
}
let guard: ReturnType<typeof installPasteGuard>;
let ports: Port[];
let editor: HTMLTextAreaElement;
let shadow: ShadowRoot;
let toggleRoot: ShadowRoot;
function paste(text: string, element: HTMLElement = editor) {
  const event = new Event('paste', {
    bubbles: true,
    cancelable: true,
    composed: true,
  });
  Object.defineProperty(event, 'clipboardData', {
    value: {files: [], getData: () => text},
  });
  element.dispatchEvent(event);
  return event;
}
function job() {
  const port = ports.findLast(p => p.sent.some(m => m.type === 'start'))!;
  return {port, id: port.sent.find(m => m.type === 'start').id};
}
beforeEach(() => {
  vi.useFakeTimers();
  vi.stubGlobal('matchMedia', () => ({
    matches: false,
    addEventListener() {},
    removeEventListener() {},
  }));
  document.body.innerHTML =
    '<form><textarea id="prompt-textarea"></textarea><button type="submit">Send</button></form><input type="search">';
  editor = document.querySelector('textarea')!;
  editor.style.backgroundColor = 'white';
  ports = [];
  const attach = vi.spyOn(Element.prototype, 'attachShadow');
  guard = installPasteGuard(
    'chatgpt',
    {
      connect: () => {
        const p = new Port();
        ports.push(p);
        return p;
      },
      reviewUrl: token => `about:blank#${token}`,
      settings() {},
    },
    false,
  );
  shadow =
    attach.mock.results[
      attach.mock.instances.findIndex(
        node => (node as Element).tagName === 'REDACTOBOT-PASTE-GUARD',
      )
    ]!.value;
  toggleRoot =
    attach.mock.results[
      attach.mock.instances.findIndex(
        node => (node as Element).tagName === 'REDACTOBOT-PASTE-TOGGLE',
      )
    ]!.value;
  // Redactobot starts off on every page; most tests exercise it switched on.
  guard.setEnabled(true);
  ports = [];
});
afterEach(() => {
  guard.dispose();
  vi.useRealTimers();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});
describe('paste gate', () => {
  it('holds text that arrives with a file, as Excel and Word copies do', () => {
    const event = new Event('paste', {
      bubbles: true,
      cancelable: true,
      composed: true,
    });
    Object.defineProperty(event, 'clipboardData', {
      value: {
        files: [{name: 'image.png'}],
        getData: () => 'Margaret Whitfield',
      },
    });
    editor.dispatchEvent(event);
    expect(event.defaultPrevented).toBe(true);
    expect(job().port.sent.find(m => m.type === 'start').text).toBe(
      'Margaret Whitfield',
    );
  });
  it('lets file-only pastes through to the site', () => {
    const event = new Event('paste', {
      bubbles: true,
      cancelable: true,
      composed: true,
    });
    Object.defineProperty(event, 'clipboardData', {
      value: {files: [{name: 'image.png'}], getData: () => ''},
    });
    editor.dispatchEvent(event);
    expect(event.defaultPrevented).toBe(false);
  });
  it('holds dropped text', () => {
    const event = new Event('drop', {
      bubbles: true,
      cancelable: true,
      composed: true,
    });
    Object.defineProperty(event, 'dataTransfer', {
      value: {files: [], getData: () => 'Tom Whitfield'},
    });
    editor.dispatchEvent(event);
    expect(event.defaultPrevented).toBe(true);
    expect(job().port.sent.find(m => m.type === 'start').text).toBe(
      'Tom Whitfield',
    );
  });
  it('rejects an oversized paste without blocking later pastes or closing an open review', () => {
    expect(paste('x'.repeat(100_001)).defaultPrevented).toBe(true);
    expect(ports.some(p => p.sent.some(m => m.type === 'start'))).toBe(false);
    vi.advanceTimersByTime(5000);
    paste('next');
    const {port, id} = job();
    port.emit({type: 'review', id, token: 'token'});
    const frame = shadow.querySelector('iframe');
    expect(frame).not.toBeNull();
    paste('x'.repeat(100_001));
    expect(shadow.querySelector('iframe')).toBe(frame);
  });
  it('preloads when enabled before any focus or paste and sends no document text', () => {
    guard.setEnabled(false);
    ports = [];
    guard.setEnabled(true);
    const warm = ports.find(p => p.sent.some(m => m.type === 'prepare'))!;
    expect(warm.sent).toEqual([{type: 'prepare'}]);
    vi.advanceTimersByTime(21000);
    expect(warm.sent).toContainEqual({type: 'heartbeat'});
    warm.emit({type: 'prepared', ok: true});
    expect(paste('next').defaultPrevented).toBe(true);
  });
  it('starts switched off on every page: pastes pass through and the model is not loaded', () => {
    guard.dispose();
    ports = [];
    const attach = vi.spyOn(Element.prototype, 'attachShadow');
    guard = installPasteGuard(
      'chatgpt',
      {
        connect: () => {
          const p = new Port();
          ports.push(p);
          return p;
        },
        reviewUrl: token => `about:blank#${token}`,
        settings() {},
      },
      false,
    );
    const root = attach.mock.results[
      attach.mock.instances.findLastIndex(
        node => (node as Element).tagName === 'REDACTOBOT-PASTE-TOGGLE',
      )
    ]!.value as ShadowRoot;
    expect(root.querySelector('button')!.getAttribute('aria-checked')).toBe(
      'false',
    );
    editor.dispatchEvent(new FocusEvent('focusin', {bubbles: true}));
    vi.advanceTimersByTime(61_000);
    expect(paste('unchecked').defaultPrevented).toBe(false);
    expect(ports).toHaveLength(0);
  });
  it('keeps one progress bar running through a long cold start, never restarting it', async () => {
    guard.setEnabled(false);
    ports = [];
    guard.setEnabled(true);
    const first = ports.find(p => p.sent.some(m => m.type === 'prepare'))!;
    await vi.advanceTimersByTimeAsync(800);
    const bar = toggleRoot.querySelector<HTMLElement>('[role="progressbar"]')!;
    const warm = toggleRoot.querySelector<HTMLElement>('.warm')!;
    expect(warm.classList.contains('on')).toBe(true);
    // Past the once-a-minute keep-alive: the same request is still the only one.
    await vi.advanceTimersByTimeAsync(65_000);
    expect(first.disconnected).toBe(false);
    expect(
      ports.filter(p => p.sent.some(m => m.type === 'prepare')),
    ).toHaveLength(1);
    const atOneMinute = Number(bar.getAttribute('aria-valuenow'));
    expect(atOneMinute).toBeGreaterThan(40);
    // Past the request's own timeout: it asks again, and the bar carries on.
    await vi.advanceTimersByTimeAsync(100_000);
    expect(
      ports.filter(p => p.sent.some(m => m.type === 'prepare')),
    ).toHaveLength(2);
    expect(warm.classList.contains('on')).toBe(true);
    expect(Number(bar.getAttribute('aria-valuenow'))).toBeGreaterThan(
      atOneMinute,
    );
    const second = ports.filter(p => p.sent.some(m => m.type === 'prepare'))[1];
    second.emit({type: 'prepared', ok: true});
    expect(bar.getAttribute('aria-valuenow')).toBe('100');
  });
  it('stops a cold start at once when switched off, and starts fresh when switched back on', async () => {
    guard.setEnabled(false);
    ports = [];
    const button = toggleRoot.querySelector<HTMLButtonElement>('button')!;
    button.click();
    await vi.advanceTimersByTimeAsync(0);
    const warm = ports.find(p => p.sent.some(m => m.type === 'prepare'))!;
    await vi.advanceTimersByTimeAsync(800);
    expect(toggleRoot.querySelector('.warm')!.classList.contains('on')).toBe(
      true,
    );
    button.click();
    await vi.advanceTimersByTimeAsync(0);
    expect(warm.sent).toContainEqual({type: 'cancel-prepare'});
    expect(warm.disconnected).toBe(true);
    expect(toggleRoot.querySelector('.warm')!.classList.contains('on')).toBe(
      false,
    );
    warm.emit({type: 'prepared', ok: true});
    expect(toggleRoot.querySelector('.warm')!.classList.contains('on')).toBe(
      false,
    );
    button.click();
    await vi.advanceTimersByTimeAsync(0);
    expect(
      ports.filter(p => p.sent.some(m => m.type === 'prepare')),
    ).toHaveLength(2);
  });
  it('keeps the real startup state when progress arrives before the display delay', () => {
    paste('sample');
    const {port, id} = job();
    port.emit({type: 'progress', id, label: 'Starting on-device AI…'});
    vi.advanceTimersByTime(180);
    expect(shadow.querySelector('[role="status"]')!.textContent).toContain(
      'Starting on-device AI',
    );
  });
  it('cancels pending and queued pastes when switched off, ignores late results, and resumes when on', async () => {
    const button = toggleRoot.querySelector<HTMLButtonElement>('button')!;
    paste('first secret');
    const first = job();
    paste('second secret');
    button.click();
    expect(button.getAttribute('aria-checked')).toBe('false');
    expect(first.port.sent.some(message => message.type === 'cancel')).toBe(
      true,
    );
    first.port.emit({type: 'insert', id: first.id, cleaned: 'late result'});
    expect(editor.value).toBe('');
    expect(paste('off').defaultPrevented).toBe(false);
    expect(
      ports.filter(port => port.sent.some(message => message.type === 'start')),
    ).toHaveLength(1);
    await vi.advanceTimersByTimeAsync(0);
    button.click();
    await vi.advanceTimersByTimeAsync(0);
    expect(button.getAttribute('aria-checked')).toBe('true');
    expect(paste('on').defaultPrevented).toBe(true);
  });
  it('updates the visible switch when switched off programmatically', () => {
    guard.setEnabled(false);
    expect(
      toggleRoot.querySelector('button')!.getAttribute('aria-checked'),
    ).toBe('false');
    expect(paste('off').defaultPrevented).toBe(false);
  });
  it('does not recreate controls after disposal with a pending DOM update', async () => {
    document.body.append(document.createElement('div'));
    await Promise.resolve();
    guard.dispose();
    await vi.advanceTimersByTimeAsync(40);
    expect(document.querySelector('redactobot-paste-toggle')).toBeNull();
  });
  it('removes a retired launcher badge added after page startup', async () => {
    const old = document.createElement('div');
    old.id = 'client-safe-ai-host';
    document.body.append(old);
    await Promise.resolve();
    expect(document.getElementById('client-safe-ai-host')).toBeNull();
  });
  it('shows unbranded status inside the input, without adding status text to the draft', () => {
    editor.style.cssText =
      'padding:12px;border:1px solid;font:400 18px/27px Georgia;background:white';
    vi.spyOn(editor, 'getBoundingClientRect').mockReturnValue({
      left: 100,
      top: 200,
      right: 700,
      bottom: 280,
      width: 600,
      height: 80,
    } as DOMRect);
    paste('avery@example.com');
    vi.advanceTimersByTime(180);
    const {port, id} = job();
    port.emit({type: 'progress', id, label: 'Removing private details…'});
    const host = document.querySelector<HTMLElement>('redactobot-paste-guard')!;
    expect(host.style.left).toBe('113px');
    expect(host.style.top).toBe('213px');
    expect(host.style.width).toBe('574px');
    expect(host.style.getPropertyValue('--rb-font')).toBe('Georgia');
    expect(host.style.getPropertyValue('--rb-fontSize')).toBe('18px');
    expect(shadow.querySelector('[role="status"]')!.textContent).toContain(
      'Removing private details',
    );
    expect(shadow.querySelector('.brand')).toBeNull();
    expect(editor.value).toBe('');
    port.emit({type: 'insert', id, cleaned: '[EMAIL_TEST_1]', count: 1});
    expect(editor.value).toBe('[EMAIL_TEST_1]');
    expect(host.style.display).toBe('none');
  });
  it('makes room above an existing draft and restores the input after cancellation', () => {
    editor.value = 'Existing draft';
    editor.style.cssText =
      'box-sizing:border-box;padding-top:10px;min-height:40px;line-height:24px';
    vi.spyOn(editor, 'getBoundingClientRect').mockReturnValue({
      left: 100,
      top: 200,
      right: 700,
      bottom: 280,
      width: 600,
      height: 80,
    } as DOMRect);
    editor.setSelectionRange(14, 14);
    paste('avery@example.com');
    vi.advanceTimersByTime(180);
    expect(editor.style.paddingTop).toBe('38px');
    expect(editor.style.minHeight).toBe('108px');
    expect(editor.value).toBe('Existing draft');
    shadow
      .querySelector<HTMLButtonElement>('[aria-label="Cancel paste"]')!
      .click();
    expect(editor.style.paddingTop).toBe('10px');
    expect(editor.style.minHeight).toBe('40px');
    expect(editor.value).toBe('Existing draft');
    expect(job().port.sent.some(message => message.type === 'cancel')).toBe(
      true,
    );
  });
  it('does not change editor layout during the native insertion input event', () => {
    editor.value = 'Draft ';
    editor.setSelectionRange(6, 6);
    editor.style.paddingTop = '10px';
    editor.style.lineHeight = '24px';
    paste('avery@example.com');
    vi.advanceTimersByTime(180);
    Object.defineProperty(document, 'execCommand', {
      configurable: true,
      value: vi.fn(() => {
        editor.value = 'Draft [EMAIL_TEST_1]';
        editor.dispatchEvent(
          new InputEvent('input', {bubbles: true, inputType: 'insertText'}),
        );
        expect(editor.style.paddingTop).toBe('10px');
        return true;
      }),
    });
    const {port, id} = job();
    port.emit({type: 'insert', id, cleaned: '[EMAIL_TEST_1]', count: 1});
    expect(editor.style.paddingTop).toBe('10px');
    expect(editor.value).toBe('Draft [EMAIL_TEST_1]');
    Reflect.deleteProperty(document, 'execCommand');
  });
  it('restores inline spacing before opening a private review, preserving later site style changes', () => {
    editor.value = 'Draft';
    editor.style.cssText =
      'box-sizing:border-box;padding-top:10px;min-height:40px;line-height:24px';
    paste('uncertain detail');
    vi.advanceTimersByTime(180);
    // A site layout update that we must not undo.
    editor.style.minHeight = '120px';
    const {port, id} = job();
    port.emit({type: 'review', id, token: 'token'});
    expect(editor.style.paddingTop).toBe('10px');
    expect(editor.style.minHeight).toBe('120px');
    expect(shadow.querySelector('iframe')).not.toBeNull();
    expect(editor.value).toBe('Draft');
  });
  it('protects the live ChatGPT composer without an ID, including pastes in a nested paragraph', () => {
    const composer = document.createElement('div');
    composer.className = 'ProseMirror';
    composer.setAttribute('contenteditable', 'true');
    composer.setAttribute('role', 'textbox');
    composer.setAttribute('aria-label', 'Ask ChatGPT');
    const paragraph = document.createElement('p');
    composer.append(paragraph);
    document.body.append(composer);
    const range = document.createRange();
    range.selectNodeContents(paragraph);
    range.collapse(false);
    window.getSelection()!.removeAllRanges();
    window.getSelection()!.addRange(range);
    const sitePaste = vi.fn();
    composer.addEventListener('paste', sitePaste);
    expect(paste('Email: avery@example.com.', paragraph).defaultPrevented).toBe(
      true,
    );
    expect(composer.textContent).toBe('');
    expect(sitePaste).not.toHaveBeenCalled();
    const {port, id} = job();
    port.emit({
      type: 'insert',
      id,
      cleaned: 'Email: [EMAIL_TEST_1].',
      count: 1,
    });
    expect(composer.textContent).toBe('Email: [EMAIL_TEST_1].');
  });
  it('recognizes the labeled ChatGPT textarea variant', () => {
    editor.removeAttribute('id');
    editor.setAttribute('aria-label', 'Ask ChatGPT');
    expect(paste('avery@example.com').defaultPrevented).toBe(true);
    const {port, id} = job();
    port.emit({type: 'insert', id, cleaned: '[EMAIL_TEST_1]', count: 1});
    expect(editor.value).toBe('[EMAIL_TEST_1]');
  });
  it('does not intercept an unrelated rich text box on ChatGPT', () => {
    const other = document.createElement('div');
    other.className = 'ProseMirror';
    other.setAttribute('contenteditable', 'true');
    other.setAttribute('role', 'textbox');
    other.setAttribute('aria-label', 'Search chats');
    document.body.append(other);
    expect(paste('search text', other).defaultPrevented).toBe(false);
    expect(ports).toHaveLength(0);
  });
  it('holds raw text before site handlers, then inserts only cleaned text without submitting', () => {
    const sitePaste = vi.fn();
    const submit = vi.fn();
    const input = vi.fn();
    editor.addEventListener('paste', sitePaste);
    editor.addEventListener('input', input);
    document.querySelector('form')!.addEventListener('submit', submit);
    expect(paste('avery@example.com').defaultPrevented).toBe(true);
    expect(editor.value).toBe('');
    expect(sitePaste).not.toHaveBeenCalled();
    const {port, id} = job();
    port.emit({type: 'insert', id, cleaned: '[EMAIL_TEST_1]', count: 1});
    expect(editor.value).toBe('[EMAIL_TEST_1]');
    expect(input).toHaveBeenCalledOnce();
    expect(submit).not.toHaveBeenCalled();
    expect(port.sent.some(m => m.type === 'inserted')).toBe(true);
  });
  it('does not overwrite a draft edited while scanning', () => {
    paste('secret');
    const {port, id} = job();
    editor.value = 'new draft';
    port.emit({type: 'insert', id, cleaned: '[REDACTED_1]'});
    expect(editor.value).toBe('new draft');
    expect(port.sent.some(m => m.type === 'context-changed')).toBe(true);
  });
  it('holds ambiguous and failed scans, with raw text absent from page DOM', () => {
    paste('private original');
    const {port, id} = job();
    port.emit({type: 'review', id, token: 'token'});
    port.emit({type: 'failed', id, label: 'Scan stopped'});
    expect(editor.value).toBe('');
    expect(document.documentElement.textContent).not.toContain(
      'private original',
    );
    expect(
      document.querySelector('redactobot-paste-guard')!.shadowRoot,
    ).toBeNull();
  });
  it('ignores late results after cancellation', () => {
    paste('secret');
    const {port, id} = job();
    port.emit({type: 'canceled', id});
    port.emit({type: 'insert', id, cleaned: 'too late'});
    expect(editor.value).toBe('');
  });
  it.each(['failed', 'expired'])(
    'accepts a new paste after %s without inserting stale queued text',
    type => {
      paste('failed original');
      const first = job();
      paste('old queued paste');
      first.port.emit({type, id: first.id, label: 'Local check timed out.'});
      first.port.emit({type: 'insert', id: first.id, cleaned: 'late result'});
      expect(editor.value).toBe('');
      expect(paste('fresh paste').defaultPrevented).toBe(true);
      const next = job();
      expect(next.id).not.toBe(first.id);
      expect(next.port.sent.find(m => m.type === 'start').text).toBe(
        'fresh paste',
      );
      next.port.emit({
        type: 'insert',
        id: next.id,
        cleaned: 'checked fresh paste',
        count: 0,
      });
      expect(editor.value).toBe('checked fresh paste');
      expect(
        ports.flatMap(p => p.sent).filter(m => m.type === 'start'),
      ).toHaveLength(2);
    },
  );
  it('retries a held failed paste with a fresh job and no stale progress', () => {
    paste('held original');
    const first = job();
    first.port.emit({
      type: 'failed',
      id: first.id,
      label: 'Local check timed out.',
    });
    Array.from(shadow.querySelectorAll('button'))
      .find(b => b.textContent === 'Retry')!
      .click();
    const retry = job();
    expect(retry.id).not.toBe(first.id);
    expect(retry.port.sent.find(m => m.type === 'start').text).toBe(
      'held original',
    );
    retry.port.emit({
      type: 'insert',
      id: retry.id,
      cleaned: 'checked retry',
      count: 0,
    });
    expect(editor.value).toBe('checked retry');
  });
  it('does not block the next paste after a scanner disconnect', () => {
    paste('first');
    const first = job();
    first.port.disconnect();
    paste('second');
    expect(job().id).not.toBe(first.id);
    expect(job().port.sent.find(m => m.type === 'start').text).toBe('second');
    expect(editor.value).toBe('');
  });
  it('keeps multiple pending pastes in order', () => {
    paste('first');
    const first = job();
    paste('second');
    first.port.emit({
      type: 'insert',
      id: first.id,
      cleaned: '[FIRST]',
      count: 1,
    });
    const second = job();
    expect(second.id).not.toBe(first.id);
    second.port.emit({
      type: 'insert',
      id: second.id,
      cleaned: '[SECOND]',
      count: 1,
    });
    expect(editor.value).toBe('[FIRST][SECOND]');
  });
  it('leaves search fields, ordinary typing and disabled sites alone', () => {
    expect(
      paste('search', document.querySelector('input')!).defaultPrevented,
    ).toBe(false);
    editor.value = 'typed normally';
    editor.dispatchEvent(
      new InputEvent('input', {bubbles: true, data: 'typed normally'}),
    );
    expect(ports).toHaveLength(0);
    guard.setEnabled(false);
    expect(paste('unprotected').defaultPrevented).toBe(false);
  });
  it('sends a live theme change to the review without a mutation loop', async () => {
    paste('secret');
    const {port, id} = job();
    vi.advanceTimersByTime(180);
    port.emit({type: 'review', id, token: 'token'});
    port.emit({type: 'review-ready', id});
    editor.style.backgroundColor = '#202020';
    await Promise.resolve();
    await vi.advanceTimersByTimeAsync(50);
    const themes = port.sent.filter(m => m.type === 'theme');
    expect(themes.at(-1).theme.dark).toBe(true);
    await vi.advanceTimersByTimeAsync(200);
    expect(port.sent.filter(m => m.type === 'theme')).toHaveLength(
      themes.length,
    );
    expect(
      document.querySelector<HTMLElement>('redactobot-paste-guard')!.style
        .colorScheme,
    ).toBe('dark');
  });
});
describe('editor insertion', () => {
  it('replaces only the captured selection and preserves multiline text', () => {
    editor.value = 'before old after';
    editor.setSelectionRange(7, 10);
    expect(insert(capture(editor)!, 'new\nlines')).toBe(true);
    expect(editor.value).toBe('before new\nlines after');
  });
  it('preserves contenteditable block position at a blank paragraph', () => {
    const editable = document.createElement('div');
    editable.contentEditable = 'true';
    editable.innerHTML = '<p>Before</p><p><br></p><p>After</p>';
    document.body.append(editable);
    const middle = editable.children[1];
    const range = document.createRange();
    range.setStart(middle, 0);
    range.collapse(true);
    window.getSelection()!.removeAllRanges();
    window.getSelection()!.addRange(range);
    const snapshot = capture(editable)!;
    Object.defineProperty(document, 'execCommand', {
      configurable: true,
      value: vi.fn(() => {
        const selected = window.getSelection()!.getRangeAt(0);
        expect(selected.startContainer).toBe(middle);
        selected.insertNode(document.createTextNode('[SAFE]'));
        return true;
      }),
    });
    expect(insert(snapshot, '[SAFE]')).toBe(true);
    expect(middle.textContent).toBe('[SAFE]');
    Reflect.deleteProperty(document, 'execCommand');
  });
});
