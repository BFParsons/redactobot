/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The Redactobot on/off switch and model start progress bar shown
 * below each chat composer.
 */

import {composersFor, type Composer} from './editor';
import {applyTheme, themeFor} from './themes';
import type {Site} from './protocol';

const css = `
:host{color-scheme:inherit}*{box-sizing:border-box}
.row{display:flex;flex-wrap:wrap;justify-content:flex-end;align-items:center;gap:8px;padding:4px 0}
button{display:inline-flex;align-items:center;gap:7px;min-height:28px;padding:3px 8px;border:1px solid transparent;border-radius:var(--rb-radius);background:transparent;color:var(--rb-muted);font:var(--rb-fontStyle) var(--rb-fontWeight) 12px/20px var(--rb-font);letter-spacing:var(--rb-letterSpacing);cursor:pointer;white-space:nowrap}
button:hover{background:color-mix(in srgb,var(--rb-text) 6%,transparent);color:var(--rb-text)}
button:focus-visible{outline:2px solid var(--rb-accent);outline-offset:2px}button:disabled{cursor:wait;opacity:.65}
.track{display:inline-flex;align-items:center;width:26px;height:16px;padding:2px;border-radius:999px;background:var(--rb-muted);flex:none}
.thumb{width:12px;height:12px;border-radius:50%;background:var(--rb-surface);transform:translateX(0);transition:transform 120ms ease}
[aria-checked="true"] .track{background:var(--rb-accent)}[aria-checked="true"] .thumb{background:var(--rb-onAccent);transform:translateX(10px)}
.warm{display:none;flex:1 1 200px;min-width:0;max-width:420px;margin-right:auto;flex-direction:column;gap:3px;padding:2px 0;color:var(--rb-muted);font:var(--rb-fontStyle) var(--rb-fontWeight) 12px/16px var(--rb-font);letter-spacing:var(--rb-letterSpacing)}
.warm.on{display:flex}.warm-top{display:flex;justify-content:space-between;gap:8px;white-space:nowrap}.warm-text{overflow:hidden;text-overflow:ellipsis}.warm-clock{font-variant-numeric:tabular-nums}
.bar{position:relative;height:4px;border-radius:999px;overflow:hidden;background:color-mix(in srgb,var(--rb-accent) 18%,var(--rb-border))}
.fill{position:relative;height:100%;width:0;border-radius:inherit;background:var(--rb-accent);overflow:hidden;transition:width .5s cubic-bezier(.2,0,0,1)}
.fill::after{content:"";position:absolute;inset:0;width:45%;background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--rb-onAccent) 55%,transparent),transparent);animation:rb-sheen 1.4s ease-in-out infinite}
.warm.done .fill::after{display:none}.warm.done .warm-text{color:var(--rb-text)}
@keyframes rb-sheen{from{transform:translateX(-100%)}to{transform:translateX(320%)}}
.state{min-width:18px;text-align:left}.message{color:var(--rb-muted);font:12px/18px var(--rb-font)}.message:empty{display:none}
@media(prefers-reduced-motion:reduce){.thumb,.fill{transition:none}.fill::after{display:none}}
`;
interface Control {
  host: HTMLElement;
  button: HTMLButtonElement;
  state: HTMLElement;
  message: HTMLElement;
  theme: string;
  warm: HTMLElement;
  warmText: HTMLElement;
  warmClock: HTMLElement;
  bar: HTMLElement;
  fill: HTMLElement;
}

/**
 * Estimated cold-start progress: Chrome reports none while it loads the model,
 * so ease towards 95% over the typical one to three minutes, and fill when the
 * model answers.
 */
export function warmPercent(ms: number, done: boolean) {
  return done ? 100 : Math.round(95 * (1 - Math.exp(-ms / 35000)));
}

/**
 * A normal-flow sibling of the editable surface: it stays inside the composer
 * layout without becoming part of the draft, a pasted message or an overlay.
 */
export class PasteToggle {
  private controls = new Map<Composer, Control>();
  private enabled = true;
  private saving = false;
  private error = '';
  private warmStart = 0;
  private warmDone = false;
  private warmTick?: ReturnType<typeof setInterval>;
  private warmHide?: ReturnType<typeof setTimeout>;
  constructor(
    private site: Site,
    private change: (enabled: boolean) => Promise<void>,
    private settings?: () => void,
  ) {}

  /** Returns whether `node` is inside a paste toggle element. */
  owns(node: Node) {
    return node instanceof Element && !!node.closest('redactobot-paste-toggle');
  }
  /** Sets the switch position shown by every control. */
  setEnabled(enabled: boolean) {
    this.enabled = enabled;
    for (const control of this.controls.values()) this.update(control);
  }
  /** Show the on-device model's cold start right below the chat box. */
  startWarming() {
    clearTimeout(this.warmHide);
    if (this.warmStart && !this.warmDone) return;
    this.warmStart = Date.now();
    this.warmDone = false;
    clearInterval(this.warmTick);
    this.warmTick = setInterval(() => this.paintWarm(), 500);
    this.paintWarm(true);
  }
  /**
   * Ready: fill the bar, say so briefly, then remove it. Failed or canceled:
   * remove it now.
   */
  stopWarming(ready: boolean) {
    if (!this.warmStart || this.warmDone) return;
    clearInterval(this.warmTick);
    if (!ready) {
      this.warmStart = 0;
      this.paintWarm(true);
      return;
    }
    this.warmDone = true;
    this.paintWarm(true);
    this.warmHide = setTimeout(() => {
      this.warmStart = 0;
      this.warmDone = false;
      this.paintWarm(true);
    }, 1600);
  }
  /** True while the model start progress bar is running. */
  get warming() {
    return this.warmStart > 0 && !this.warmDone;
  }
  private paintWarm(announce = false) {
    for (const control of this.controls.values()) {
      this.drawWarm(control, announce);
    }
  }
  private drawWarm(control: Control, announce: boolean) {
    const on = this.warmStart > 0;
    control.warm.classList.toggle('on', on);
    control.warm.classList.toggle('done', this.warmDone);
    if (!on) return;
    const ms = Date.now() - this.warmStart;
    const pct = warmPercent(ms, this.warmDone);
    const secs = Math.floor(ms / 1000);
    if (announce) {
      control.warmText.textContent = this.warmDone
        ? 'On-device AI is ready'
        : 'Starting on-device AI…';
    }
    control.warmClock.textContent = this.warmDone
      ? ''
      : `${Math.floor(secs / 60)}:${String(secs % 60).padStart(2, '0')}`;
    control.fill.style.width = `${pct}%`;
    control.bar.setAttribute('aria-valuenow', String(pct));
    control.bar.setAttribute(
      'aria-valuetext',
      this.warmDone ? 'Ready' : `About ${pct}%, ${secs} seconds so far`,
    );
  }
  private update(control: Control) {
    const checked = String(this.enabled);
    if (control.button.getAttribute('aria-checked') !== checked) {
      control.button.setAttribute('aria-checked', checked);
    }
    const state = this.enabled ? 'On' : 'Off';
    if (control.state.textContent !== state) control.state.textContent = state;
    control.button.disabled = this.saving;
    control.button.title = this.enabled
      ? 'Pasted text is checked for private details. Click to turn off on this site.'
      : 'Pasted text is not checked. Click to turn on for this site.';
    control.message.textContent = this.error;
  }
  private create(): Control {
    const host = document.createElement('redactobot-paste-toggle');
    // Normal flow reserves its own space, including on narrow/mobile composers.
    host.style.cssText =
      'all:initial;display:flex;justify-content:flex-end;align-self:stretch;flex:0 0 auto;grid-column:1 / -1;box-sizing:border-box;';
    host.contentEditable = 'false';
    const root = host.attachShadow({mode: 'closed'});
    const style = document.createElement('style');
    style.textContent = css;
    const row = document.createElement('div');
    row.className = 'row';
    const button = document.createElement('button');
    button.type = 'button';
    button.setAttribute('role', 'switch');
    button.setAttribute(
      'aria-label',
      'Redactobot: check pasted text for private details',
    );
    const label = document.createElement('span');
    label.textContent = 'Redactobot';
    const track = document.createElement('span');
    track.className = 'track';
    track.setAttribute('aria-hidden', 'true');
    const thumb = document.createElement('span');
    thumb.className = 'thumb';
    track.append(thumb);
    const state = document.createElement('span');
    state.className = 'state';
    state.setAttribute('aria-hidden', 'true');
    const message = document.createElement('span');
    message.className = 'message';
    message.setAttribute('role', 'status');
    // Cold-start bar: hidden until the on-device model takes more than a moment
    // to load.
    const warm = document.createElement('div');
    warm.className = 'warm';
    const top = document.createElement('div');
    top.className = 'warm-top';
    const warmText = document.createElement('span');
    warmText.className = 'warm-text';
    warmText.setAttribute('role', 'status');
    warmText.setAttribute('aria-live', 'polite');
    const warmClock = document.createElement('span');
    warmClock.className = 'warm-clock';
    warmClock.setAttribute('aria-hidden', 'true');
    top.append(warmText, warmClock);
    const bar = document.createElement('div');
    bar.className = 'bar';
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute(
      'aria-label',
      'Redactobot: starting the on-device AI model',
    );
    bar.setAttribute('aria-valuemin', '0');
    bar.setAttribute('aria-valuemax', '100');
    const fill = document.createElement('div');
    fill.className = 'fill';
    bar.append(fill);
    warm.append(top, bar);
    button.append(label, track, state);
    row.append(warm, message, button);
    root.append(style, row);
    if (this.settings) {
      const settings = document.createElement('button');
      settings.type = 'button';
      settings.textContent = 'Data types';
      settings.title = 'Choose which types of data to check';
      settings.setAttribute('aria-label', settings.title);
      settings.addEventListener('click', () => this.settings?.());
      row.append(settings);
    }
    const control = {
      host,
      button,
      state,
      message,
      theme: '',
      warm,
      warmText,
      warmClock,
      bar,
      fill,
    };
    button.addEventListener('click', () => {
      if (this.saving) return;
      this.saving = true;
      this.error = '';
      const next = !this.enabled;
      // Update synchronously so the next paste follows the visible switch.
      const changed = this.change(next);
      this.setEnabled(next);
      void changed
        .catch(() => {
          this.setEnabled(!next);
          this.error = 'Could not save. Try again.';
        })
        .finally(() => {
          this.saving = false;
          this.setEnabled(this.enabled);
        });
    });
    this.update(control);
    this.drawWarm(control, true);
    return control;
  }
  /**
   * Mounts a control after each current composer, removes the controls of
   * composers that are gone and reapplies any theme that changed.
   */
  refresh() {
    const composers = composersFor(this.site);
    for (const [composer, control] of this.controls) {
      if (composers.includes(composer)) continue;
      control.host.remove();
      this.controls.delete(composer);
    }
    for (const composer of composers) {
      // Gemini owns rich-textarea's internals; mount after that component.
      const anchor = composer.closest<HTMLElement>('rich-textarea') || composer;
      if (!anchor.parentElement || anchor.parentElement.isContentEditable) {
        continue;
      }
      let control = this.controls.get(composer);
      if (!control) {
        control = this.create();
        this.controls.set(composer, control);
      }
      if (anchor.nextElementSibling !== control.host) {
        anchor.after(control.host);
      }
      const theme = themeFor(this.site, composer);
      const encoded = JSON.stringify(theme);
      if (encoded !== control.theme) {
        applyTheme(control.host, theme);
        control.theme = encoded;
      }
    }
  }
  /** Stops the timers and removes every control. */
  dispose() {
    clearInterval(this.warmTick);
    clearTimeout(this.warmHide);
    for (const control of this.controls.values()) control.host.remove();
    this.controls.clear();
  }
}
