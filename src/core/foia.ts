/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview US Freedom of Information Act release markings.
 *
 * 5 U.S.C. § 552(b) (as amended by the OPEN Government Act of 2007) requires
 * that "the amount of information deleted, and the exemption under which the
 * deletion is made, shall be indicated at the place in the record where such
 * deletion is made". FOIA officers do this with a box over the withheld text,
 * sized to it, labelled with the exemption, for example "(b)(6)". Law
 * enforcement records usually cite privacy twice: "(b)(6), (b)(7)(C)".
 *
 * The defaults below are a starting point for a FOIA professional, not legal
 * advice: every exemption can be changed per data type, or the type released.
 */

import type {Detection} from './redact';

/** A FOIA exemption: its citation, such as "(b)(6)", and what it covers. */
export interface Exemption {
  code: string;
  label: string;
}

/**
 * The exemptions of 5 U.S.C. § 552(b) a user can choose, in statutory order.
 */
export const EXEMPTIONS: Exemption[] = [
  {code: '(b)(1)', label: 'Classified national security information'},
  {code: '(b)(2)', label: 'Internal personnel rules and practices'},
  {code: '(b)(3)', label: 'Exempted by another statute'},
  {
    code: '(b)(4)',
    label: 'Trade secrets, confidential commercial or financial information',
  },
  {code: '(b)(5)', label: 'Privileged inter- or intra-agency records'},
  {code: '(b)(6)', label: 'Personal privacy'},
  {code: '(b)(7)(A)', label: 'Would interfere with enforcement proceedings'},
  {code: '(b)(7)(C)', label: 'Personal privacy in law enforcement records'},
  {code: '(b)(7)(D)', label: 'Confidential source'},
  {
    code: '(b)(7)(E)',
    label: 'Law enforcement techniques, procedures or guidelines',
  },
  {code: '(b)(7)(F)', label: 'Could endanger life or physical safety'},
  {code: '(b)(8)', label: 'Financial institution supervision'},
  {code: '(b)(9)', label: 'Geological and geophysical data on wells'},
];
/** The code used when a data type is released rather than withheld. */
export const RELEASE = 'release';

const COMMERCIAL = new Set(['company', 'ein', 'bn_ca', 'money']);
const SYSTEMS = new Set(['credential', 'ip', 'device']);

/**
 * Default exemption for a detection kind. Personal details are (b)(6); in law
 * enforcement records they also carry (b)(7)(C). Business identifiers and
 * amounts are (b)(4). System access details are (b)(7)(E) in law enforcement
 * records, otherwise (b)(6).
 */
export function defaultExemption(
  kind: string,
  lawEnforcement: boolean,
): string {
  if (COMMERCIAL.has(kind)) return '(b)(4)';
  if (SYSTEMS.has(kind) && lawEnforcement) return '(b)(7)(E)';
  return lawEnforcement ? '(b)(6), (b)(7)(C)' : '(b)(6)';
}

/** The user's choices for a FOIA release. */
export interface FoiaSettings {
  /** Whether these are law enforcement records, which changes the defaults. */
  lawEnforcement: boolean;
  /** Detection kind -> the exemption code chosen for it, or RELEASE. */
  overrides: Record<string, string>;
}

/**
 * The exemption marked on a withheld detection. A type set to release that the
 * user withholds one by one falls back to the default code, so a box is never
 * unlabelled.
 */
export function exemptionFor(kind: string, s: FoiaSettings): string {
  const o = s.overrides[kind];
  return o && o !== RELEASE ? o : defaultExemption(kind, s.lawEnforcement);
}

/**
 * Every distinct exemption code used, in statutory order: "(b)(6), (b)(7)(C)"
 * counts as two.
 */
export function exemptionsUsed(dets: Detection[], s: FoiaSettings): string[] {
  const used = new Set<string>();
  for (const d of dets) {
    if (d.enabled) {
      for (const c of exemptionFor(d.kind, s).split(/,\s*/)) used.add(c);
    }
  }
  const order = EXEMPTIONS.map(e => e.code);
  return [...used].sort((a, b) => order.indexOf(a) - order.indexOf(b));
}

/**
 * The cells of a redaction box that follow its exemption label: one block
 * character for each withheld character, so the box is exactly as long as the
 * text it hides, however long that is. Spaces stay, so a long box wraps where
 * the text did. The label takes the first cells; a withholding shorter than
 * its label is as wide as the label.
 */
export function boxFill(withheld: string, code: string): string {
  return withheld.replace(/\S/g, '█').slice(code.length);
}

/**
 * The release as plain text: each withheld passage becomes a run of █ as long
 * as the text it replaces, followed by its exemption, under a release stamp.
 */
export function foiaText(
  text: string,
  dets: Detection[],
  s: FoiaSettings,
): string {
  const active = dets.filter(d => d.enabled).sort((a, b) => a.start - b.start);
  let out = '';
  let at = 0;
  for (const d of active) {
    if (d.start < at) continue;
    const code = exemptionFor(d.kind, s);
    out +=
      text.slice(at, d.start) +
      `${'█'.repeat(Math.max(1, d.end - d.start))} ${code}`;
    at = d.end;
  }
  out += text.slice(at);
  const used = exemptionsUsed(dets, s);
  const stamp = used.length
    ? `RELEASED IN PART — ${used.join(', ')}`
    : 'RELEASED IN FULL';
  return `${stamp}\n\n${out}`;
}
