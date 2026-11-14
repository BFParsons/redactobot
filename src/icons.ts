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

// The GitHub mark, used only to link to the project on GitHub.
const github =
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>';

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
  github,
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
