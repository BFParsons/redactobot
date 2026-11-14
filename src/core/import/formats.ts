/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Rich Text (.rtf), email (.eml) and web pages (.html).
 */

import {decodeText, fromLatin1} from './text';

// ---------------- RTF ----------------
// Groups that hold settings or binary data, not document text.
const RTF_SKIP = new Set([
  'fonttbl',
  'colortbl',
  'stylesheet',
  'info',
  'pict',
  'object',
  'themedata',
  'colorschememapping',
  'datastore',
  'latentstyles',
  'generator',
  'listtable',
  'listoverridetable',
  'rsidtbl',
  'xmlnstbl',
  'fldinst',
  'bkmkstart',
  'bkmkend',
  'filetbl',
  'revtbl',
  'pgdsctbl',
  'nonshppict',
  'shpinst',
  'operator',
  'author',
  'company',
  'title',
  'template',
]);
const RTF_CHARS: Record<string, string> = {
  par: '\n',
  line: '\n',
  sect: '\n',
  page: '\n',
  row: '\n',
  tab: '\t',
  cell: '\t',
  emdash: '—',
  endash: '–',
  lquote: '‘',
  rquote: '’',
  ldblquote: '“',
  rdblquote: '”',
  bullet: '•',
  emspace: ' ',
  enspace: ' ',
};
const cp1252 = new TextDecoder('windows-1252');

/** Plain text from RTF source (read as one byte per character). */
export function rtfToText(src: string): string {
  const out: string[] = [];
  const stack: Array<{skip: boolean; uc: number}> = [];
  let cur = {skip: false, uc: 1};
  let pendingSkip = 0; // fallback characters to drop after a \uN
  let i = 0;
  const emit = (s: string) => {
    if (pendingSkip > 0) {
      pendingSkip--;
      return;
    }
    if (!cur.skip) out.push(s);
  };
  while (i < src.length) {
    const ch = src[i];
    if (ch === '{') {
      stack.push(cur);
      cur = {...cur};
      i++;
      continue;
    }
    if (ch === '}') {
      cur = stack.pop() ?? {skip: false, uc: 1};
      pendingSkip = 0;
      i++;
      continue;
    }
    if (ch === '\r' || ch === '\n') {
      i++;
      continue;
    }
    if (ch !== '\\') {
      emit(ch);
      i++;
      continue;
    }

    const next = src[i + 1];
    if (next === "'") {
      // \'hh: one byte in the document code page
      emit(
        cp1252.decode(
          Uint8Array.of(parseInt(src.slice(i + 2, i + 4), 16) || 0x3f),
        ),
      );
      i += 4;
      continue;
    }
    if (next === '*') {
      cur.skip = true;
      i += 2;
      continue;
    }
    if (next === '\\' || next === '{' || next === '}') {
      emit(next);
      i += 2;
      continue;
    }
    if (next === '~') {
      emit(' ');
      i += 2;
      continue;
    }
    if (next === '_' || next === '-') {
      if (next === '_') emit('-');
      i += 2;
      continue;
    }
    if (next === '\n' || next === '\r') {
      emit('\n');
      i += 2;
      continue;
    }

    const m = /^\\([a-zA-Z]+)(-?\d+)? ?/.exec(src.slice(i, i + 48));
    if (!m) {
      i += 2;
      continue;
    }
    i += m[0].length;
    const word = m[1];
    const num = m[2] === undefined ? undefined : Number(m[2]);
    if (RTF_SKIP.has(word)) {
      cur.skip = true;
      continue;
    }
    if (word === 'uc') {
      cur.uc = num ?? 1;
      continue;
    }
    if (word === 'u' && num !== undefined) {
      emit(String.fromCharCode(num < 0 ? num + 65536 : num));
      pendingSkip = cur.uc;
      continue;
    }
    if (word === 'bin' && num) {
      i += num;
      continue;
    }
    if (RTF_CHARS[word]) emit(RTF_CHARS[word]);
  }
  return out.join('');
}

// ---------------- HTML ----------------
const BLOCK = new Set([
  'p',
  'div',
  'section',
  'article',
  'header',
  'footer',
  'h1',
  'h2',
  'h3',
  'h4',
  'h5',
  'h6',
  'ul',
  'ol',
  'li',
  'table',
  'tr',
  'blockquote',
  'pre',
  'address',
  'dl',
  'dt',
  'dd',
  'hr',
  'figure',
  'figcaption',
  'main',
  'nav',
  'aside',
]);
const DROP = new Set([
  'script',
  'style',
  'noscript',
  'template',
  'head',
  'svg',
  'iframe',
  'object',
  'canvas',
]);

/**
 * Visible text of a web page or HTML email. Scripts and styles are dropped,
 * nothing is run.
 */
export function htmlToText(source: string): string {
  const doc = new DOMParser().parseFromString(source, 'text/html');
  const out: string[] = [];
  const walk = (n: Node) => {
    if (n.nodeType === 3) {
      out.push((n.nodeValue ?? '').replace(/\s+/g, ' '));
      return;
    }
    if (n.nodeType !== 1) return;
    const tag = (n as Element).localName;
    if (DROP.has(tag)) return;
    if (tag === 'br') {
      out.push('\n');
      return;
    }
    if (BLOCK.has(tag)) out.push('\n');
    if (tag === 'li') out.push('- ');
    n.childNodes.forEach(walk);
    if (tag === 'td' || tag === 'th') out.push('\t');
    if (BLOCK.has(tag)) out.push('\n');
  };
  walk(doc.body ?? doc.documentElement);
  return out
    .join('')
    .replace(/[ \t]*\n[ \t]*/g, '\n')
    .replace(/\t+\n/g, '\n')
    .replace(/ {2,}/g, ' ');
}

// ---------------- Email (.eml) ----------------
function decodeQuotedPrintable(s: string): Uint8Array {
  return fromLatin1(
    s
      .replace(/=\r?\n/g, '')
      .replace(/=([0-9A-Fa-f]{2})/g, (_, h: string) =>
        String.fromCharCode(parseInt(h, 16)),
      ),
  );
}
function decodeBase64(s: string): Uint8Array {
  try {
    return fromLatin1(atob(s.replace(/[^A-Za-z0-9+/=]/g, '')));
  } catch {
    return new Uint8Array();
  }
}
/** RFC 2047 encoded words in headers, for example =?UTF-8?B?...?= */
function decodeHeader(value: string): string {
  return value.replace(
    /=\?([^?]+)\?([bBqQ])\?([^?]*)\?=(\s+(?==\?))?/g,
    (_, charset: string, enc: string, data: string) =>
      decodeText(
        enc.toLowerCase() === 'b'
          ? decodeBase64(data)
          : decodeQuotedPrintable(data.replace(/_/g, ' ')),
        charset,
      ),
  );
}
function splitHeaders(raw: string): {
  headers: Map<string, string>;
  body: string;
} {
  const cut = raw.search(/\r?\n\r?\n/);
  const head = cut < 0 ? raw : raw.slice(0, cut);
  const body = cut < 0 ? '' : raw.slice(cut).replace(/^\r?\n\r?\n/, '');
  const headers = new Map<string, string>();
  for (const line of head.replace(/\r?\n[ \t]+/g, ' ').split(/\r?\n/)) {
    const at = line.indexOf(':');
    if (at > 0) {
      headers.set(
        line.slice(0, at).trim().toLowerCase(),
        line.slice(at + 1).trim(),
      );
    }
  }
  return {headers, body};
}
const param = (value: string, name: string) =>
  value.match(new RegExp(`${name}\\s*=\\s*"?([^";]+)"?`, 'i'))?.[1];

interface MailText {
  plain: string[];
  html: string[];
  attachments: string[];
}

function readPart(raw: string, into: MailText, depth = 0) {
  const {headers, body} = splitHeaders(raw);
  const type = headers.get('content-type') ?? 'text/plain';
  const disposition = headers.get('content-disposition') ?? '';
  const filename = param(disposition, 'filename') ?? param(type, 'name');
  if (/^multipart\//i.test(type) && depth < 8) {
    const boundary = param(type, 'boundary');
    if (!boundary) return;
    const pieces = body.split(
      new RegExp(
        `(?:^|\\r?\\n)--${boundary.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?:--)?[ \\t]*(?:\\r?\\n|$)`,
      ),
    );
    for (const piece of pieces.slice(1)) {
      if (piece.trim()) readPart(piece, into, depth + 1);
    }
    return;
  }
  if (/attachment/i.test(disposition) || (filename && !/^text\//i.test(type))) {
    into.attachments.push(decodeHeader(filename ?? 'unnamed'));
    return;
  }
  if (!/^text\/(plain|html)/i.test(type)) return;
  const encoding = (
    headers.get('content-transfer-encoding') ?? ''
  ).toLowerCase();
  const bytes =
    encoding === 'quoted-printable'
      ? decodeQuotedPrintable(body)
      : encoding === 'base64'
        ? decodeBase64(body)
        : fromLatin1(body);
  const text = decodeText(bytes, param(type, 'charset'));
  if (/^text\/html/i.test(type)) into.html.push(htmlToText(text));
  else into.plain.push(text);
}

/**
 * Headers that matter plus the message text. Attachments are listed, not
 * opened.
 */
export function emlToText(raw: string): {text: string; attachments: string[]} {
  const {headers} = splitHeaders(raw);
  const found: MailText = {plain: [], html: [], attachments: []};
  readPart(raw, found);
  const lines = (['from', 'to', 'cc', 'date', 'subject'] as const)
    .filter(h => headers.get(h))
    .map(
      h =>
        `${h[0].toUpperCase()}${h.slice(1)}: ${decodeHeader(headers.get(h)!)}`,
    );
  const body = (found.plain.length ? found.plain : found.html).join('\n\n');
  return {
    text: `${lines.join('\n')}\n\n${body}`,
    attachments: found.attachments,
  };
}
