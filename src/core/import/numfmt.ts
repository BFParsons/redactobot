/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Show a spreadsheet number the way Excel displays it, from the
 * cell's number format code. Covers the formats business files actually use:
 * thousands separators, decimals, currency (including custom symbols such as
 * "C$" and [$€-407]), negatives in parentheses, percent, and date/time formats.
 * Anything unrecognised falls back to the plain number.
 */

const BUILTIN: Record<number, string> = {
  1: '0',
  2: '0.00',
  3: '#,##0',
  4: '#,##0.00',
  5: '$#,##0_);($#,##0)',
  6: '$#,##0_);($#,##0)',
  7: '$#,##0.00_);($#,##0.00)',
  8: '$#,##0.00_);($#,##0.00)',
  9: '0%',
  10: '0.00%',
  14: 'm/d/yyyy',
  15: 'd-mmm-yy',
  16: 'd-mmm',
  17: 'mmm-yy',
  18: 'h:mm AM/PM',
  19: 'h:mm:ss AM/PM',
  20: 'h:mm',
  21: 'h:mm:ss',
  22: 'm/d/yyyy h:mm',
  37: '#,##0_);(#,##0)',
  38: '#,##0_);(#,##0)',
  39: '#,##0.00_);(#,##0.00)',
  40: '#,##0.00_);(#,##0.00)',
  41: '#,##0_);(#,##0)',
  42: '$#,##0_);($#,##0)',
  43: '#,##0.00_);(#,##0.00)',
  44: '$#,##0.00_);($#,##0.00)',
  45: 'mm:ss',
  46: '[h]:mm:ss',
  47: 'mm:ss.0',
};

/**
 * Returns the format code for a number format id: the workbook's own code if it
 * defines one, else Excel's built-in code, else ''.
 *
 * @param custom The format codes the workbook defines, by id.
 */
export function formatCode(
  numFmtId: number,
  custom: Map<number, string>,
): string {
  return custom.get(numFmtId) ?? BUILTIN[numFmtId] ?? '';
}

type Token = {lit: string} | {code: string};

/** Split a format section into literal text and format codes. */
function tokenize(section: string): Token[] {
  const out: Token[] = [];
  for (let i = 0; i < section.length; i++) {
    const ch = section[i];
    if (ch === '"') {
      const end = section.indexOf('"', i + 1);
      out.push({lit: section.slice(i + 1, end < 0 ? undefined : end)});
      i = end < 0 ? section.length : end;
    } else if (ch === '\\') {
      out.push({lit: section[++i] ?? ''});
    } else if (ch === '_') {
      i++;
    } // space the width of the next character
    else if (ch === '*') {
      i++;
    } // repeat-fill character
    else if (ch === '[') {
      const end = section.indexOf(']', i);
      const inner = section.slice(i + 1, end);
      const currency = /^\$([^-\]]*)/.exec(inner); // [$€-407] -> €
      if (currency) out.push({lit: currency[1]});
      else if (/^h+$|^m+$|^s+$/i.test(inner)) out.push({code: inner});
      i = end < 0 ? section.length : end;
    } else {
      out.push({code: ch});
    }
  }
  return out;
}

const splitSections = (code: string) => {
  const parts: string[] = [];
  let cur = '';
  let quoted = false;
  let bracket = false;
  for (let i = 0; i < code.length; i++) {
    const ch = code[i];
    if (ch === '\\') {
      cur += ch + (code[++i] ?? '');
      continue;
    }
    if (ch === '"') quoted = !quoted;
    if (!quoted && ch === '[') bracket = true;
    if (!quoted && ch === ']') bracket = false;
    if (ch === ';' && !quoted && !bracket) {
      parts.push(cur);
      cur = '';
    } else {
      cur += ch;
    }
  }
  parts.push(cur);
  return parts;
};

const codesOf = (tokens: Token[]) =>
  tokens.map(t => ('code' in t ? t.code : '')).join('');

/**
 * Returns whether a format code shows a date or time rather than a number: its
 * first section has date or time letters and no digit placeholders, other than
 * fractions of a second.
 */
export function isDateFormat(code: string): boolean {
  if (!code || /^general$/i.test(code)) return false;
  const codes = codesOf(tokenize(splitSections(code)[0]));
  return /[dmyhs]/i.test(codes) && !/[0#?]/.test(codes.replace(/\.0+/g, ''));
}

const MONTHS = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];
const DAYS = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
];
const pad = (n: number, w = 2) => String(n).padStart(w, '0');

function formatDate(serial: number, code: string, date1904: boolean): string {
  const ms = Math.round((serial + (date1904 ? 1462 : 0) - 25569) * 86400000);
  const d = new Date(ms);
  const tokens = tokenize(splitSections(code)[0]);
  const codes = codesOf(tokens);
  const ampm = /am\/pm|a\/p/i.test(codes);
  let out = '';
  let prev = '';
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    if ('lit' in t) {
      out += t.lit;
      continue;
    }
    // group runs of the same letter
    let run = t.code;
    while (
      i + 1 < tokens.length &&
      'code' in tokens[i + 1] &&
      (tokens[i + 1] as {code: string}).code.toLowerCase() ===
        t.code[0].toLowerCase() &&
      /[a-z]/i.test(t.code)
    ) {
      run += (tokens[++i] as {code: string}).code;
    }
    const c = run[0].toLowerCase();
    const n = run.length;
    if (c === 'y') {
      out +=
        n <= 2 ? pad(d.getUTCFullYear() % 100) : String(d.getUTCFullYear());
    } else if (c === 'm') {
      // "m" means minutes right after hours or right before seconds
      const rest = tokens
        .slice(i + 1)
        .map(x => ('code' in x ? x.code : ''))
        .join('')
        .toLowerCase()
        .replace(/[^a-z]/g, '');
      const minutes = prev === 'h' || rest.startsWith('s');
      if (minutes) {
        out += n === 1 ? String(d.getUTCMinutes()) : pad(d.getUTCMinutes());
      } else if (n === 1) {
        out += String(d.getUTCMonth() + 1);
      } else if (n === 2) {
        out += pad(d.getUTCMonth() + 1);
      } else if (n === 3) {
        out += MONTHS[d.getUTCMonth()].slice(0, 3);
      } else if (n === 5) {
        out += MONTHS[d.getUTCMonth()][0];
      } else {
        out += MONTHS[d.getUTCMonth()];
      }
    } else if (c === 'd') {
      if (n === 1) out += String(d.getUTCDate());
      else if (n === 2) out += pad(d.getUTCDate());
      else if (n === 3) out += DAYS[d.getUTCDay()].slice(0, 3);
      else out += DAYS[d.getUTCDay()];
    } else if (c === 'h') {
      const h = ampm ? d.getUTCHours() % 12 || 12 : d.getUTCHours();
      out += n === 1 ? String(h) : pad(h);
    } else if (c === 's') {
      out += n === 1 ? String(d.getUTCSeconds()) : pad(d.getUTCSeconds());
    } else if (c === 'a' && /^(am\/pm|a\/p)/i.test(codesOf(tokens.slice(i)))) {
      const full = /^am\/pm/i.test(codesOf(tokens.slice(i)));
      out += d.getUTCHours() < 12 ? (full ? 'AM' : 'A') : full ? 'PM' : 'P';
      i += full ? 4 : 2;
    } else if (!/[a-z]/i.test(c)) {
      out += run;
    }
    if (/[a-z]/i.test(c)) prev = c;
  }
  return out;
}

function formatPlain(
  value: number,
  section: string,
  negativeSection: boolean,
  onlySection: boolean,
): string {
  const tokens = tokenize(section);
  const codes = codesOf(tokens);
  if (!/[0#?]/.test(codes)) {
    return (
      tokens
        .map(t => ('lit' in t ? t.lit : /[0#?.,%]/.test(t.code) ? '' : t.code))
        .join('') || String(value)
    );
  }
  const percent = codes.includes('%');
  let n = Math.abs(value) * (percent ? 100 : 1);
  const [intCodes, decCodes = ''] = codes.replace(/[^0#?.,]/g, '').split('.');
  const decimals = (decCodes.match(/[0#?]/g) ?? []).length;
  const thousands = /[0#?],[0#?]/.test(intCodes);
  // trailing commas scale by thousands
  const scale = (intCodes.match(/,+$/) ?? [''])[0].length;
  n /= 1000 ** scale;
  const digits = n.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
    useGrouping: thousands,
  });
  let out = '';
  let placed = false;
  for (const t of tokens) {
    if ('lit' in t) {
      out += t.lit;
    } else if (/[0#?.,]/.test(t.code)) {
      if (!placed) {
        out += digits;
        placed = true;
      }
    } else {
      // $ ( ) - % and similar
      out += t.code;
    }
  }
  if (value < 0 && (!negativeSection || onlySection)) out = '-' + out;
  return out;
}

/**
 * The text Excel would show for a numeric cell. `code` is the cell's number
 * format.
 */
export function displayNumber(
  value: number,
  code: string,
  date1904 = false,
): string {
  if (!code || /^general$/i.test(code) || code === '@') {
    return String(Number(value.toPrecision(15)));
  }
  try {
    if (isDateFormat(code)) return formatDate(value, code, date1904);
    const sections = splitSections(code);
    const index =
      value > 0
        ? 0
        : value < 0
          ? sections.length > 1
            ? 1
            : 0
          : sections.length > 2
            ? 2
            : 0;
    return formatPlain(
      value,
      sections[index],
      index === 1,
      sections.length === 1,
    );
  } catch {
    return String(Number(value.toPrecision(15)));
  }
}
