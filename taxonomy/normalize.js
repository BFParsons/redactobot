/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview A detection-only view. Never replace or transmit this copy:
 * every match maps back to the original UTF-16 offsets, including hidden
 * characters inside an identifier.
 */

const invisible = /\p{Default_Ignorable_Code_Point}/gu;
const decimal = /\p{Nd}/u;
const folded = new Map();

function fold(cluster) {
  let result = folded.get(cluster);
  if (result !== undefined) return result;
  result = [...cluster.normalize('NFKC').replace(invisible, '')]
    .map(ch => {
      if (/[\u2010-\u2015\u2212]/u.test(ch)) return '-';
      if (!decimal.test(ch) || /[0-9]/.test(ch)) return ch;
      // Unicode decimal digits occur in ordered runs of ten (some runs are
      // adjacent).
      const code = ch.codePointAt(0);
      let zero = code;
      while (decimal.test(String.fromCodePoint(zero - 1))) zero--;
      return String((code - zero) % 10);
    })
    .join('');
  // Cache characters, never document phrases or values. Bound even adversarial
  // input.
  if (cluster.length <= 4 && folded.size < 2048) folded.set(cluster, result);
  return result;
}

/**
 * Builds a copy of the text for detection only: NFKC-normalized, with
 * invisible characters removed, Unicode dashes folded to "-" and decimal
 * digits of any script folded to 0-9. ASCII-only text is used as it is.
 * @param {string} original The text as supplied.
 * @return {{text: string, span: function(number, number): !Array<number>}}
 *     The folded text, and span(start, end), which maps a range of the
 *     folded text to the [start, end] offsets it covers in the original.
 */
export function detectionView(original) {
  // oxlint-disable-next-line no-control-regex -- an ASCII-only test is the point.
  if (!/[^\x00-\x7f]/.test(original)) {
    return {text: original, span: (s, e) => [s, e]};
  }
  const starts = [];
  const ends = [];
  const parts = [];
  for (const m of original.matchAll(/\P{M}\p{M}*|\p{M}+/gu)) {
    const value = fold(m[0]);
    parts.push(value);
    for (let i = 0; i < value.length; i++) {
      starts.push(m.index);
      ends.push(m.index + m[0].length);
    }
  }
  return {text: parts.join(''), span: (s, e) => [starts[s], ends[e - 1]]};
}

/**
 * Finds every occurrence of a term in a detection view, ignoring case and
 * the amount of whitespace, where the term is not part of a longer word or
 * number.
 * @param {{text: string, span: function(number, number): !Array<number>}}
 *     view A view built by detectionView().
 * @param {string} term The term to find; it is folded the same way first.
 * @return {!Array<!Array<number>>} One [start, end] pair of offsets in the
 *     original text for each occurrence.
 */
export function viewOccurrences(view, term) {
  const folded = detectionView(term).text.trim();
  if (!folded) return [];
  const escaped = folded
    .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    .replace(/\s+/g, '\\s+');
  return [
    ...view.text.matchAll(
      new RegExp(`(?<![\\p{L}\\p{N}])${escaped}(?![\\p{L}\\p{N}])`, 'giu'),
    ),
  ].map(m => view.span(m.index, m.index + m[0].length));
}
