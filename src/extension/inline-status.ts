/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Positions the paste status line inside the bounds of a chat
 * composer.
 */

import {editorValue} from './editor';

interface SavedStyle {
  name: string;
  value: string;
  priority: string;
  applied: string;
}
const px = (value: string) => Number.parseFloat(value) || 0;

/**
 * Keep status out of editable text, while rendering it inside the editor's
 * bounds. For an existing draft, temporarily reserve a row so the status never
 * covers it. Restore only styles we still own; a site layout update must not be
 * overwritten.
 */
export class InlineStatus {
  private composer?: HTMLElement;
  private saved: SavedStyle[] = [];
  private shift = 0;
  private top = 0;

  /**
   * Restores each composer style this instance set, unless the page has changed
   * it since.
   */
  reset() {
    for (const item of this.saved) {
      if (this.composer?.style.getPropertyValue(item.name) !== item.applied) {
        continue;
      }
      if (item.value) {
        this.composer.style.setProperty(item.name, item.value, item.priority);
      } else {
        this.composer.style.removeProperty(item.name);
      }
    }
    this.saved = [];
    this.composer = undefined;
    this.shift = 0;
  }
  private set(name: string, value: string) {
    const style = this.composer!.style;
    this.saved.push({
      name,
      value: style.getPropertyValue(name),
      priority: style.getPropertyPriority(name),
      applied: value,
    });
    style.setProperty(name, value);
  }
  /**
   * Positions `host` over the composer's content box. When the composer holds a
   * draft, first adds top padding to reserve a row for the status.
   */
  place(host: HTMLElement, composer: HTMLElement) {
    if (this.composer !== composer) {
      this.reset();
      this.composer = composer;
    }
    let style = getComputedStyle(composer);
    const line = px(style.lineHeight) || (px(style.fontSize) || 16) * 1.5;
    const hasDraft = editorValue(composer).trim().length > 0;
    if (
      this.shift &&
      (!hasDraft ||
        this.saved.some(
          item => composer.style.getPropertyValue(item.name) !== item.applied,
        ))
    ) {
      this.reset();
      this.composer = composer;
      style = getComputedStyle(composer);
    }
    if (hasDraft && !this.shift) {
      this.top = px(style.paddingTop);
      this.shift = line + 4;
      const height = composer.getBoundingClientRect().height;
      this.set('padding-top', `${this.top + this.shift}px`);
      if (style.boxSizing === 'border-box') {
        this.set('min-height', `${height + this.shift}px`);
      }
      style = getComputedStyle(composer);
    }
    const r = composer.getBoundingClientRect();
    const left = px(style.borderLeftWidth) + px(style.paddingLeft);
    const right = px(style.borderRightWidth) + px(style.paddingRight);
    host.style.left = `${r.left + left}px`;
    host.style.top = `${r.top + px(style.borderTopWidth) + (this.shift ? this.top : px(style.paddingTop))}px`;
    host.style.width = `${Math.max(0, r.width - left - right)}px`;
    host.style.setProperty('--rb-status-height', `${line}px`);
  }
}
