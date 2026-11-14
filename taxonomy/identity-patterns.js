/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Extra local evidence for the three highest-priority structured
 * identity gaps. Each result covers the original text, not a
 * normalized/reconstructed replacement.
 */

import {detectionView} from './normalize.js';
import {validCard, isRegion, PATTERN_DETECTORS} from './detectors.js';
import {PLACE_NAMES} from './places-data.js';

const RECORD_LABEL =
  '(?:medical[ \\t]+record|record|MRN|chart|case|cause|docket|file|matter|claim|policy|invoice|inv|reference|ref|encounter|accession|specimen|patient|member|subscriber|customer|client|employee|incident|report|permit|parcel|order|receipt|confirmation|booking|reservation|ticket|referral|authorization|authorisation|application|transaction|contract|engagement|loan|mortgage|prescription|rx)';
const ID_MARKER = '(?:number|no\\.?|id|identifier|key|code|reference)';
const recordLabel = new RegExp(
  `\\b${RECORD_LABEL}(?:[ \\t]+${ID_MARKER})?[ \\t]*[:=#][ \\t]*(?:\\r?\\n[ \\t]*)?|\\b${RECORD_LABEL}[ \\t]+${ID_MARKER}[ \\t]+|\\b(?:MRN|PNR)[ \\t]+`,
  'gi',
);
const token =
  /[\p{L}\p{M}\p{N}_]+(?:(?:[ \t]*[-/][ \t]*|[.:])[\p{L}\p{M}\p{N}_]+)*/gu;
const emptyValue =
  /^(?:none|null|unknown|pending|unassigned|n\/?a|not[ -](?:available|provided|assigned))$/i;
const shape = s => s.toLowerCase().replace(/\d+/g, '#').replace(/[ \t]/g, '');
const key = s => s.toLowerCase().replace(/[ \t]/g, '');
const cardContext = {
  test: value =>
    /\b(?:visa|mastercard|amex|american express|discover|payment|(?:credit|debit)\s+card|pan)\b/i.test(
      value,
    ) ||
    (/\bcard\b/i.test(value) &&
      !/\b(?:health|identity|id|library|insurance|student|benefit|membership|loyalty|transit|access|medicare)\s+card\b|\b(?:PHN|OHIP|NHS)\b/i.test(
        value,
      )),
};
const spokenDigit = '(?:zero|oh|one|two|three|four|five|six|seven|eight|nine)';
const spoken = new RegExp(
  `\\b${spokenDigit}(?:[ ,\\t-]+${spokenDigit}){3,18}\\b`,
  'gi',
);
const locationLabel =
  /\b(?:city|town|village|county|municipality|birthplace|location|destination|hometown|ville|ciudad|localit[eé]|municipio)[ \t]*[:=][ \t]*(?:\r?\n[ \t]*)?/gi;
const placeWord = "[\\p{L}\\p{M}]+(?:['’.-][\\p{L}\\p{M}]+)*";
const placeValue = new RegExp(`^${placeWord}(?:[ \\t]+${placeWord}){0,6}`, 'u');
const coordinatePair =
  /(?<![\p{L}\p{N}.])([+-]?\d{1,2}\.\d{3,})\s*[,;/]\s*([+-]?\d{1,3}\.\d{3,})(?![\p{L}\p{N}]|\.\d)/gu;
const ambiguousPlace =
  /^(?:reading|sale|nice|bath|mobile|orange|normal|order|may|march|hope|nice|union|enterprise|commerce|spring|summer|winter|home|work|office|court|hospital|town|village|city)$/i;
const organizationAfter =
  /^\s+(?:[\p{L}'’-]+\s+){0,3}(?:LLC|LLP|Ltd|Inc|Corp|Clinic|Hospital|University|Foundation|Bank|Logistics|Company)\b/iu;
const placeWords = new RegExp(placeWord, 'gu');
const placePhrase = new RegExp(`^${placeWord}(?:[ \\t]+${placeWord})*$`, 'u');
const placeBefore =
  /\b(?:in|near|outside|within|from|to|at|around|towards?)\s+$/i;
const strongPlaceBefore =
  /\b(?:lives?|living|resides?|residing|born|moved|relocated|travelled|traveled|house|home|property)\s+(?:in|near|to|from)\s+$/i;
const regionPostal =
  /^,?[ \t]+([A-Z]{2})[ \t,]+(?:\d{5}(?:-\d{4})?\b|[A-Z]\d[A-Z][ \t]?\d[A-Z]\d\b)/;

function resemblesPlace(word) {
  if (!/^[a-z]{5,22}$/.test(word)) return false;
  for (let i = 0; i <= word.length; i++) {
    if (PLACE_NAMES.has(word.slice(0, i) + word.slice(i + 1))) return true;
    if (
      i + 1 < word.length &&
      PLACE_NAMES.has(
        word.slice(0, i) + word[i + 1] + word[i] + word.slice(i + 2),
      )
    ) {
      return true;
    }
    for (const ch of 'abcdefghijklmnopqrstuvwxyz') {
      if (
        PLACE_NAMES.has(word.slice(0, i) + ch + word.slice(i)) ||
        PLACE_NAMES.has(word.slice(0, i) + ch + word.slice(i + 1))
      ) {
        return true;
      }
    }
  }
  return false;
}

/**
 * New candidate sources, also used independently to recover overlapping full
 * spans.
 * @param {string} original The text as supplied; result offsets refer to it.
 * @param {!Array<string>} allowed Detector ids to look for. Only 'record',
 *     'card', 'card_partial' and 'places' produce candidates.
 * @return {!Array<{type: string, start: number, end: number, text: string,
 *     reviewReason: (string|undefined)}>} The candidates, sorted by start
 *     and then longest first. reviewReason is set only when the user should
 *     check the value.
 */
export function identityCandidates(original, allowed) {
  if (
    !allowed.some(id =>
      ['record', 'card', 'card_partial', 'places'].includes(id),
    )
  ) {
    return [];
  }
  const view = detectionView(original);
  const text = view.text;
  const out = [];
  const add = (type, start, end, reviewReason) => {
    if (!allowed.includes(type) || start >= end) return;
    const [s, e] = view.span(start, end);
    if (!Number.isInteger(s) || !Number.isInteger(e)) return;
    out.push({
      type,
      start: s,
      end: e,
      text: original.slice(s, e),
      ...(reviewReason ? {reviewReason} : {}),
    });
  };

  if (allowed.includes('card') || allowed.includes('card_partial')) {
    // Allow bounded fragments across whitespace and punctuation. A checksum is
    // positive evidence, not permission to keep a mistyped card in an explicit
    // payment context.
    for (const m of text.matchAll(
      /(?<![\p{L}\p{N}])\d(?:[ \r\n/.-]{0,6}\d)+(?![\p{L}\p{N}]|[ \r\n/.-]{0,6}\d)/gu,
    )) {
      const before = text
        .slice(Math.max(0, m.index - 65), m.index)
        .split(/[;.!?]/)
        .at(-1);
      const after = text
        .slice(m.index + m[0].length, m.index + m[0].length + 35)
        .split(/[;.!?\n]/)[0];
      const context =
        cardContext.test(before) ||
        /^\s+(?:for|as|is the)\s+(?:a\s+)?(?:payment|card|visa|mastercard)\b/i.test(
          after,
        );
      const count = m[0].replace(/\D/g, '').length;
      if (count < 8) continue;
      const groups = m[0]
        .split(/\D+/)
        .map(g => g.length)
        .join(',');
      const conventional =
        /^\d+$/.test(m[0]) ||
        /^(?:4,4,4,[1-7]|4,6,[3-9]|4,4,4,4,[1-3]|1(?:,1){12,18})$/.test(groups);
      if ((conventional && validCard(m[0])) || context) {
        add(
          'card',
          m.index,
          m.index + m[0].length,
          context && (count < 13 || count > 19)
            ? 'This card field has an unusual number of digits. Check the full value.'
            : undefined,
        );
      }
    }
    // Preserve the established full spans, while extending them to Unicode
    // spellings.
    for (const rule of PATTERN_DETECTORS.find(d => d.id === 'card_partial')
      .rules) {
      for (const m of text.matchAll(rule.re)) {
        const context = text.slice(Math.max(0, m.index - 55), m.index) + m[0];
        if (
          cardContext.test(context) &&
          !/\bSSNs?\b/i.test(context) &&
          (!rule.ok || rule.ok(m[0]))
        ) {
          add('card_partial', m.index, m.index + m[0].length);
        }
      }
    }
    // Masked numbers and explicit last-four values, including spoken digits.
    for (const m of text.matchAll(
      /(?<![\p{L}\p{N}])(?:[xX*•][\s-]?){2,16}(?:\d[\s-]?){1,4}(?!\d)/gu,
    )) {
      if (cardContext.test(text.slice(Math.max(0, m.index - 55), m.index))) {
        add('card_partial', m.index, m.index + m[0].trimEnd().length);
      }
    }
    for (const m of text.matchAll(/\b\d{4}\b/g)) {
      const before = text.slice(Math.max(0, m.index - 70), m.index);
      if (
        cardContext.test(before) &&
        /\b(?:ending(?:[ \t]+in)?|ends[ \t]+(?:in|with)|last[ \t]+(?:four|4)(?:[ \t]+digits)?)[ \t:=-]*$/i.test(
          before,
        )
      ) {
        add('card_partial', m.index, m.index + m[0].length);
      }
    }
    for (const m of text.matchAll(spoken)) {
      const before = text.slice(Math.max(0, m.index - 70), m.index);
      if (!cardContext.test(before)) continue;
      const count = m[0].match(new RegExp(spokenDigit, 'gi')).length;
      if (count === 4 || count >= 13) {
        add(
          count === 4 ? 'card_partial' : 'card',
          m.index,
          m.index + m[0].length,
        );
      }
    }
  }

  if (allowed.includes('record')) {
    const seeds = new Set();
    const formats = new Set();
    const phrases = new Set();
    for (const m of text.matchAll(recordLabel)) {
      // "Address on file: ..." labels an address, not a file reference. Do not
      // let a small new match steal the beginning of the existing whole-address
      // rule.
      if (
        /^file\b/i.test(m[0]) &&
        /\b(?:address|residence|property|phone|email)\b[^\n:]{0,30}$/i.test(
          text.slice(Math.max(0, m.index - 50), m.index),
        )
      ) {
        continue;
      }
      const start = m.index + m[0].length;
      // A quoted ID may contain spaces; otherwise retain the entire
      // separator-joined value.
      const quote = /^["“']([^"”'\r\n]{1,100})["”']/.exec(text.slice(start));
      let value = quote
        ? quote[1]
        : new RegExp(`^(?:${token.source})`, 'u').exec(text.slice(start))?.[0];
      if (!value || emptyValue.test(value) || value.length > 128) continue;
      if (
        text[start + value.length] === '@' ||
        /^(?:https?|ftp)$/i.test(value)
      ) {
        continue;
      }
      // A case caption and a named patient/client are names, not record-number
      // fields.
      if (
        /^case\s*:/i.test(m[0]) &&
        /^\s+v(?:s)?\./i.test(text.slice(start + value.length))
      ) {
        continue;
      }
      if (
        /^(?:patient|member|subscriber|customer|client|employee)\s*[:=]/i.test(
          m[0],
        ) &&
        !/\d/.test(value)
      ) {
        continue;
      }
      let reviewReason;
      if (!quote && /^[\p{L}\p{M}]+$/u.test(value)) {
        const phrase = new RegExp(
          `^${placeWord}(?:[ \\t]+${placeWord}){1,10}`,
          'u',
        ).exec(text.slice(start))?.[0];
        if (phrase && phrase.length <= 100) {
          value = phrase;
          reviewReason =
            'This record field contains words. Check that the full reference is protected.';
        }
      }
      // An ID written in spaced groups ("81234 5678 RT0001", "123 456 789")
      // continues while the next group is digits or capitals with a digit;
      // "1234 Main Street" stops at "Main".
      if (!quote && !reviewReason && /\d/.test(value)) {
        for (let i = 0; i < 4; i++) {
          const more =
            /^[ \t]([A-Z0-9][A-Z0-9-]*\d[A-Z0-9-]*|\d+)(?![\p{L}\p{N}@])/u.exec(
              text.slice(start + value.length),
            );
          if (!more) break;
          value += more[0];
        }
      }
      const at = start + (quote ? 1 : 0);
      add('record', at, at + value.length, reviewReason);
      if (value.length >= 4 && /\p{L}/u.test(value)) seeds.add(key(value));
      if ((quote || reviewReason) && /\s/.test(value)) phrases.add(value);
      // Learn only an anchored alphabetic prefix with digits and a separator. A
      // bare number or arbitrary word must not teach the scanner to redact
      // every similar word.
      if (/^[a-z]{2,}[-/:]/i.test(value) && /\d/.test(value)) {
        formats.add(shape(value));
      }
    }
    if (seeds.size || formats.size) {
      for (const m of text.matchAll(token)) {
        if (seeds.has(key(m[0]))) {
          add('record', m.index, m.index + m[0].length);
        } else if (formats.has(shape(m[0]))) {
          add(
            'record',
            m.index,
            m.index + m[0].length,
            'This value matches a record format used elsewhere in this document.',
          );
        }
      }
    }
    for (const phrase of phrases) {
      const escaped = phrase
        .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
        .replace(/\s+/g, '[ \\t]+');
      for (const m of text.matchAll(
        new RegExp(`(?<![\\p{L}\\p{N}])${escaped}(?![\\p{L}\\p{N}])`, 'giu'),
      )) {
        add('record', m.index, m.index + m[0].length);
      }
    }
  }

  if (allowed.includes('places')) {
    for (const m of text.matchAll(locationLabel)) {
      const start = m.index + m[0].length;
      const value = placeValue.exec(text.slice(start))?.[0];
      if (value && !emptyValue.test(value) && !isRegion(value)) {
        add('places', start, start + value.length);
      }
    }
    for (const m of text.matchAll(coordinatePair)) {
      if (Math.abs(Number(m[1])) > 90 || Math.abs(Number(m[2])) > 180) continue;
      // Precision plus a valid pair is useful evidence even without a location
      // label.
      add('places', m.index, m.index + m[0].length);
    }
    // Offline dictionary lookup, using this occurrence's surrounding words. A
    // city name alone is not enough to relabel a person or the beginning of a
    // company.
    const words = [...text.matchAll(placeWords)];
    let fuzzyBudget = 24;
    for (let i = 0; i < words.length; i++) {
      const start = words[i].index;
      const before = text.slice(Math.max(0, start - 70), start);
      const strong = strongPlaceBefore.test(before);
      const prep = placeBefore.test(before);
      if (
        !prep &&
        !/\b(?:address|office|residence|neighbou?rhood|property|city|county)\b|\b[A-Z]{2}[ \t,]+(?:\d{5}|[A-Z]\d[A-Z])/i.test(
          text.slice(start, start + 100),
        )
      ) {
        continue;
      }
      let found = false;
      for (let n = Math.min(6, words.length - i); n >= 1; n--) {
        const last = words[i + n - 1];
        const end = last.index + last[0].length;
        const value = text.slice(start, end);
        if (!placePhrase.test(value)) continue;
        const after = text.slice(end, end + 80);
        const postal = regionPostal.exec(after);
        const context =
          prep ||
          /^\s+(?:address|office|residence|neighbou?rhood|property|city|county)\b/i.test(
            after,
          ) ||
          Boolean(postal && isRegion(postal[1]));
        if (
          !context ||
          !PLACE_NAMES.has(value.toLowerCase()) ||
          isRegion(value) ||
          (!strong && ambiguousPlace.test(value)) ||
          organizationAfter.test(after)
        ) {
          continue;
        }
        add('places', start, end);
        found = true;
        break;
      }
      // A close spelling with strong residential/travel context is protected
      // but held for review. It never invents a replacement spelling or changes
      // the source text.
      if (
        !found &&
        strong &&
        fuzzyBudget-- > 0 &&
        resemblesPlace(words[i][0].toLowerCase())
      ) {
        add(
          'places',
          start,
          start + words[i][0].length,
          'This may be a misspelled place name.',
        );
      }
    }
  }
  return out.sort((a, b) => a.start - b.start || b.end - a.end);
}
