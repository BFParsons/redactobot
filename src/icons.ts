/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Material Symbols (outlined, weight 400), embedded as SVG. Only
 * the icons listed here are shipped, so there is no icon font to download. To
 * use a new icon, import it below.
 */

import {html, type TemplateResult} from 'lit';
import {ifDefined} from 'lit/directives/if-defined.js';
import {unsafeHTML} from 'lit/directives/unsafe-html.js';

import add from '@material-symbols/svg-400/outlined/add.svg?raw';
import arrow_back from '@material-symbols/svg-400/outlined/arrow_back.svg?raw';
import block from '@material-symbols/svg-400/outlined/block.svg?raw';
import check_circle from '@material-symbols/svg-400/outlined/check_circle.svg?raw';
import cloud_off from '@material-symbols/svg-400/outlined/cloud_off.svg?raw';
import contrast from '@material-symbols/svg-400/outlined/contrast.svg?raw';
import content_copy from '@material-symbols/svg-400/outlined/content_copy.svg?raw';
import description from '@material-symbols/svg-400/outlined/description.svg?raw';
import devices from '@material-symbols/svg-400/outlined/devices.svg?raw';
import downloading from '@material-symbols/svg-400/outlined/downloading.svg?raw';
import error from '@material-symbols/svg-400/outlined/error.svg?raw';
import fact_check from '@material-symbols/svg-400/outlined/fact_check.svg?raw';
import info from '@material-symbols/svg-400/outlined/info.svg?raw';
import chevron_right from '@material-symbols/svg-400/outlined/chevron_right.svg?raw';
import list_alt from '@material-symbols/svg-400/outlined/list_alt.svg?raw';
import manage_search from '@material-symbols/svg-400/outlined/manage_search.svg?raw';
import pause from '@material-symbols/svg-400/outlined/pause.svg?raw';
import play_arrow from '@material-symbols/svg-400/outlined/play_arrow.svg?raw';
import rule from '@material-symbols/svg-400/outlined/rule.svg?raw';
import schedule from '@material-symbols/svg-400/outlined/schedule.svg?raw';
import search from '@material-symbols/svg-400/outlined/search.svg?raw';
import send from '@material-symbols/svg-400/outlined/send.svg?raw';
import upload_file from '@material-symbols/svg-400/outlined/upload_file.svg?raw';
import visibility from '@material-symbols/svg-400/outlined/visibility.svg?raw';
import warning from '@material-symbols/svg-400/outlined/warning.svg?raw';

const ICONS = {
  add,
  arrow_back,
  block,
  check_circle,
  cloud_off,
  content_copy,
  contrast,
  description,
  devices,
  downloading,
  error,
  fact_check,
  info,
  chevron_right,
  list_alt,
  manage_search,
  pause,
  play_arrow,
  rule,
  schedule,
  search,
  send,
  upload_file,
  visibility,
  warning,
} as const;

/** The name of an embedded icon. */
export type IconName = keyof typeof ICONS;

/**
 * A Material icon. Icons are decorative here (every use sits next to text or
 * inside a labelled button), so they are hidden from screen readers. `slot`
 * places the icon in a Material Web component slot, for example a button's
 * "icon".
 */
export function icon(name: IconName, slot?: string): TemplateResult {
  // The SVG source comes from the @material-symbols package at build time,
  // never from user input.
  return html`<md-icon slot=${ifDefined(slot)} aria-hidden="true">${unsafeHTML(ICONS[name])}</md-icon>`;
}
