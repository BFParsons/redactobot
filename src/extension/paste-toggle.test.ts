/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {afterEach, describe, expect, it, vi} from 'vitest';
import {PasteToggle, warmPercent} from './paste-toggle';
import type {Site} from './protocol';

let toggle: PasteToggle | undefined;
afterEach(() => {
  toggle?.dispose();
  toggle = undefined;
  document.body.replaceChildren();
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});
function setup(site: Site = 'chatgpt', change = vi.fn(async () => {})) {
  vi.stubGlobal('matchMedia', () => ({matches: false}));
  const html = {
    chatgpt:
      '<div class="ProseMirror" role="textbox" aria-label="Ask ChatGPT" contenteditable="true">Draft text</div>',
    claude: '<div class="ProseMirror" contenteditable="true">Draft text</div>',
    gemini:
      '<rich-textarea><div class="ql-editor" contenteditable="true">Draft text</div></rich-textarea>',
  };
  document.body.innerHTML = `<form style="background:white;color:black">${html[site]}<button>Send</button></form>`;
  const editor = document.querySelector<HTMLElement>('[contenteditable]')!;
  editor.style.cssText =
    'font-family:Georgia;font-size:16px;color:rgb(20,20,20)';
  const attach = vi.spyOn(Element.prototype, 'attachShadow');
  toggle = new PasteToggle(site, change);
  toggle.refresh();
  const root = attach.mock.results[0].value as ShadowRoot;
  return {
    editor,
    host: document.querySelector<HTMLElement>('redactobot-paste-toggle')!,
    root,
    button: root.querySelector<HTMLButtonElement>('button')!,
    change,
  };
}
describe('composer paste toggle', () => {
  it('opens data settings without changing the draft, switch or submitting the chat', () => {
    const {editor} = setup();
    toggle!.dispose();
    const settings = vi.fn();
    const change = vi.fn(async () => {});
    const attach = vi.spyOn(Element.prototype, 'attachShadow');
    toggle = new PasteToggle('chatgpt', change, settings);
    toggle.refresh();
    const root = attach.mock.results.at(-1)!.value as ShadowRoot;
    const button = root.querySelector<HTMLButtonElement>(
      'button[aria-label="Choose which types of data to check"]',
    )!;
    expect(button.type).toBe('button');
    button.click();
    expect(settings).toHaveBeenCalledOnce();
    expect(change).not.toHaveBeenCalled();
    expect(editor.textContent).toBe('Draft text');
  });
  it.each(['chatgpt', 'claude', 'gemini'] as Site[])(
    'renders inside the %s composer layout, outside its editable text',
    site => {
      const {editor, host, button} = setup(site);
      expect(host.closest('form')).toBe(document.querySelector('form'));
      expect(editor.contains(host)).toBe(false);
      expect(editor.textContent).toBe('Draft text');
      expect(button.type).toBe('button');
      expect(button.getAttribute('role')).toBe('switch');
      expect(button.getAttribute('aria-checked')).toBe('true');
      expect(button.textContent).toBe('RedactobotOn');
      expect(host.style.getPropertyValue('--rb-font')).toBe('Georgia');
    },
  );
  it('changes the setting without submitting, and displays its saved off state', async () => {
    const {button, change} = setup();
    const submit = vi.fn();
    document.querySelector('form')!.addEventListener('submit', submit);
    button.click();
    expect(change).toHaveBeenCalledWith(false);
    expect(button.getAttribute('aria-checked')).toBe('false');
    expect(button.title).toContain('not checked');
    expect(submit).not.toHaveBeenCalled();
    await vi.waitFor(() => expect(button.disabled).toBe(false));
    toggle!.setEnabled(true);
    expect(button.getAttribute('aria-checked')).toBe('true');
  });
  it('restores the prior state and explains a failed preference save', async () => {
    const {button, root} = setup(
      'chatgpt',
      vi.fn(async () => {
        throw new Error('Storage failed');
      }),
    );
    button.click();
    await vi.waitFor(() => expect(button.disabled).toBe(false));
    expect(button.getAttribute('aria-checked')).toBe('true');
    expect(root.querySelector('.message')!.textContent).toContain(
      'Could not save',
    );
  });
  it('follows site color tokens and a theme change', () => {
    const {editor, host} = setup('claude');
    editor.style.setProperty('--text-400', 'rgb(80, 90, 100)');
    editor.style.setProperty('--accent-main-100', 'rgb(170, 80, 50)');
    toggle!.refresh();
    expect(host.style.getPropertyValue('--rb-muted')).toBe('rgb(80, 90, 100)');
    expect(host.style.getPropertyValue('--rb-accent')).toBe('rgb(170, 80, 50)');
    document.querySelector<HTMLElement>('form')!.style.background =
      'rgb(30, 30, 30)';
    toggle!.refresh();
    expect(host.style.colorScheme).toBe('dark');
  });
  it('survives a site re-render without duplicating the control or losing the setting', () => {
    const {editor, host} = setup();
    toggle!.setEnabled(false);
    const next = editor.cloneNode(true);
    editor.replaceWith(next);
    toggle!.refresh();
    toggle!.refresh();
    expect(host.isConnected).toBe(false);
    expect(document.querySelectorAll('redactobot-paste-toggle')).toHaveLength(
      1,
    );
    expect(document.querySelector('form')!.textContent).toBe('Draft textSend');
    toggle!.dispose();
    expect(document.querySelector('redactobot-paste-toggle')).toBeNull();
  });
  it('mounts only once for Gemini nested editable wrappers', () => {
    const {editor} = setup('gemini');
    const inner = document.createElement('div');
    inner.contentEditable = 'true';
    inner.setAttribute('contenteditable', 'true');
    inner.setAttribute('aria-label', 'Enter a prompt for Gemini');
    inner.textContent = editor.textContent;
    editor.replaceChildren(inner);
    toggle!.refresh();
    toggle!.refresh();
    expect(document.querySelectorAll('redactobot-paste-toggle')).toHaveLength(
      1,
    );
    expect(
      document
        .querySelector('rich-textarea')!
        .contains(document.querySelector('redactobot-paste-toggle')),
    ).toBe(false);
    expect(inner.textContent).toBe('Draft text');
  });
  it('ignores Gemini’s hidden Quill clipboard buffer alongside the real editor', () => {
    setup('gemini');
    const buffer = document.createElement('div');
    buffer.className = 'ql-clipboard';
    buffer.setAttribute('contenteditable', 'true');
    buffer.style.cssText =
      'position:absolute;left:-100000px;width:0;height:1px';
    document.querySelector('rich-textarea')!.append(buffer);
    toggle!.refresh();
    toggle!.refresh();
    expect(document.querySelectorAll('redactobot-paste-toggle')).toHaveLength(
      1,
    );
    expect(buffer.textContent).toBe('');
  });
  it('shows the cold-start bar under the chat box, fills it when ready, then removes it', () => {
    vi.useFakeTimers();
    const {root, editor} = setup('claude');
    const warm = root.querySelector<HTMLElement>('.warm')!;
    const bar = root.querySelector<HTMLElement>('[role="progressbar"]')!;
    expect(warm.classList.contains('on')).toBe(false);
    toggle!.startWarming();
    expect(warm.classList.contains('on')).toBe(true);
    expect(root.querySelector('.warm-text')!.textContent).toBe(
      'Starting on-device AI…',
    );
    expect(root.querySelector('[role="status"].sr')!.textContent).toContain(
      'starting on-device AI',
    );
    vi.advanceTimersByTime(70_000);
    expect(Number(bar.getAttribute('aria-valuenow'))).toBeGreaterThan(50);
    // By now the visible line is one of the light-hearted ones; screen
    // readers still have the plain status, unchanged.
    expect(root.querySelector('.warm-text')!.textContent).not.toBe(
      'Starting on-device AI…',
    );
    expect(root.querySelector('.warm-text')!.getAttribute('aria-hidden')).toBe(
      'true',
    );
    toggle!.stopWarming(true);
    expect(bar.getAttribute('aria-valuenow')).toBe('100');
    expect(root.querySelector('.warm-text')!.textContent).toBe(
      'On-device AI is ready',
    );
    vi.advanceTimersByTime(2000);
    expect(warm.classList.contains('on')).toBe(false);
    expect(editor.textContent).toBe('Draft text');
    vi.useRealTimers();
  });
  it('removes the bar at once when the start fails', () => {
    const {root} = setup();
    toggle!.startWarming();
    toggle!.stopWarming(false);
    expect(root.querySelector('.warm')!.classList.contains('on')).toBe(false);
  });
  it('estimates progress without ever claiming done before the model answers', () => {
    expect(warmPercent(0, false)).toBe(0);
    expect(warmPercent(10 * 60_000, false)).toBe(95);
    expect(warmPercent(1000, true)).toBe(100);
  });
});
