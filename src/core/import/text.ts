/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Shared helpers for the importers. Everything here runs on the
 * device; no file is uploaded.
 */

/** A problem the user can act on. The message is shown as written. */
export class ImportError extends Error {}

/**
 * Decode text bytes: honour a byte-order mark, try UTF-8, fall back to
 * Windows-1252.
 */
export function decodeText(bytes: Uint8Array, charset?: string): string {
  if (bytes[0] === 0xff && bytes[1] === 0xfe) {
    return new TextDecoder('utf-16le').decode(bytes.subarray(2));
  }
  if (bytes[0] === 0xfe && bytes[1] === 0xff) {
    return new TextDecoder('utf-16be').decode(bytes.subarray(2));
  }
  if (bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
    return new TextDecoder('utf-8').decode(bytes.subarray(3));
  }
  if (charset) {
    try {
      return new TextDecoder(charset.trim().toLowerCase()).decode(bytes);
    } catch {
      /* unknown label: fall through */
    }
  }
  try {
    return new TextDecoder('utf-8', {fatal: true}).decode(bytes);
  } catch {
    return new TextDecoder('windows-1252').decode(bytes);
  }
}

/**
 * Tidy extracted text: Unix line ends, no trailing spaces, at most one blank
 * line in a row.
 */
export function tidy(text: string): string {
  return text
    .replace(/\r\n?/g, '\n')
    .replace(/ /g, ' ')
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/** Returns a string with one character per byte (code points 0 to 255). */
export const latin1 = (bytes: Uint8Array) => {
  let s = '';
  for (let i = 0; i < bytes.length; i += 0x8000) {
    s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  }
  return s;
};
/**
 * Returns the bytes of a string made by latin1(). Keeps only the low eight bits
 * of each character.
 */
export const fromLatin1 = (s: string) =>
  Uint8Array.from(s, c => c.charCodeAt(0) & 0xff);

/** Returns a count with its noun, adding "s" unless the count is 1. */
export const plural = (n: number, word: string) =>
  `${n} ${word}${n === 1 ? '' : 's'}`;
