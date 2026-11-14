/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Word, Excel, PowerPoint (.docx .xlsx .pptx) and OpenDocument
 * (.odt .ods .odp). These are zip archives of XML. They are unpacked and read
 * in the browser.
 */

import {strFromU8, unzipSync} from 'fflate';
import {displayNumber, formatCode} from './numfmt';
import {ImportError, plural} from './text';

const MAX_ENTRY = 40 * 1024 * 1024; // one unpacked part
// all unpacked parts we read (guards against zip bombs)
const MAX_TOTAL = 120 * 1024 * 1024;

/** Unpacked archive entries, keyed by their path in the archive. */
export type Parts = Record<string, Uint8Array>;

/**
 * Unpack only the parts whose name passes `want`, with size limits.
 *
 * The limits use the size each entry declares. That is a real bound, not a
 * trusted hint: fflate inflates each entry into a buffer of its declared size
 * and stops there, so an archive that understates its sizes yields truncated
 * parts (which then fail to parse) and can never use more memory than the
 * limits allow. import.test.ts holds this with a crafted archive.
 */
export function unpack(
  bytes: Uint8Array,
  want: (name: string) => boolean,
): Parts {
  let total = 0;
  try {
    return unzipSync(bytes, {
      filter: f => {
        if (!want(f.name)) return false;
        if (f.originalSize > MAX_ENTRY) {
          throw new ImportError('This file is too large to open safely.');
        }
        total += f.originalSize;
        if (total > MAX_TOTAL) {
          throw new ImportError('This file is too large to open safely.');
        }
        return true;
      },
    });
  } catch (err) {
    if (err instanceof ImportError) throw err;
    throw new ImportError(
      'This file is damaged or password-protected and could not be opened.',
    );
  }
}

/** Names of every entry, without unpacking anything. */
export function listEntries(bytes: Uint8Array): string[] {
  const names: string[] = [];
  try {
    unzipSync(bytes, {
      filter: f => {
        names.push(f.name);
        return false;
      },
    });
  } catch {
    /* not a zip */
  }
  return names;
}

function xml(part: Uint8Array | undefined): Document | null {
  if (!part) return null;
  const doc = new DOMParser().parseFromString(
    strFromU8(part),
    'application/xml',
  );
  return doc.getElementsByTagName('parsererror').length ? null : doc;
}
const kids = (el: Element) => Array.from(el.children);
const byNumber = (re: RegExp) => (a: string, b: string) =>
  Number(a.match(re)![1]) - Number(b.match(re)![1]);
const oneLine = (s: string) => s.replace(/\s*\n\s*/g, ' ').trim();

// ---------------- Word ----------------
const WORD_SKIP = new Set([
  'del',
  'delText',
  'instrText',
  'Fallback',
  'pPr',
  'rPr',
  'sectPr',
  'tblPr',
  'tblGrid',
  'tcPr',
  'trPr',
  'footnoteReference',
  'endnoteReference',
  'annotationRef',
]);

function wordWalk(n: Element, out: string[]) {
  const name = n.localName;
  if (WORD_SKIP.has(name)) return;
  if (name === 't') {
    out.push(n.textContent ?? '');
    return;
  }
  if (name === 'tab' || name === 'ptab') {
    out.push('\t');
    return;
  }
  if (name === 'br' || name === 'cr') {
    out.push('\n');
    return;
  }
  if (name === 'noBreakHyphen') {
    out.push('-');
    return;
  }
  if (name === 'tr') {
    const cells = kids(n)
      .filter(c => c.localName === 'tc')
      .map(c => {
        const o: string[] = [];
        wordWalk(c, o);
        return oneLine(o.join(''));
      });
    out.push(cells.join('\t') + '\n');
    return;
  }
  for (const c of kids(n)) wordWalk(c, out);
  if (name === 'p') out.push('\n');
}
const wordText = (doc: Document | null) => {
  const o: string[] = [];
  if (doc) wordWalk(doc.documentElement, o);
  return o.join('').trim();
};

/**
 * Reads a Word document: headers, body, footnotes and endnotes, then footers.
 * Leaves out margin comments and text deleted with tracked changes, and says so
 * in `notes`.
 */
export function readDocx(bytes: Uint8Array) {
  const parts = unpack(bytes, n =>
    /^word\/(document|footnotes|endnotes|header\d*|footer\d*|comments)\.xml$/.test(
      n,
    ),
  );
  if (!parts['word/document.xml']) {
    throw new ImportError('This Word file has no readable document inside.');
  }
  const names = Object.keys(parts);
  const unique = (re: RegExp) => [
    ...new Set(
      names
        .filter(n => re.test(n))
        .sort()
        .map(n => wordText(xml(parts[n])))
        .filter(Boolean),
    ),
  ];
  const sections = [
    ...unique(/header\d*\.xml$/),
    wordText(xml(parts['word/document.xml'])),
    ...unique(/(footnotes|endnotes)\.xml$/),
    ...unique(/footer\d*\.xml$/),
  ].filter(Boolean);
  const notes: string[] = [];
  if (parts['word/comments.xml'] && wordText(xml(parts['word/comments.xml']))) {
    notes.push('Comments in the margin were left out.');
  }
  if (/<w:del\b/.test(strFromU8(parts['word/document.xml']))) {
    notes.push('Text deleted with tracked changes was left out.');
  }
  return {
    text: sections.join('\n\n'),
    kind: 'Word document',
    detail: '',
    notes,
  };
}

// ---------------- PowerPoint ----------------
function slideWalk(n: Element, out: string[]) {
  const name = n.localName;
  if (name === 'fld' || name === 'Fallback') return; // slide numbers, dates
  if (name === 't') {
    out.push(n.textContent ?? '');
    return;
  }
  if (name === 'br') {
    out.push('\n');
    return;
  }
  if (name === 'tab') {
    out.push('\t');
    return;
  }
  if (name === 'tr') {
    const cells = kids(n)
      .filter(c => c.localName === 'tc')
      .map(c => {
        const o: string[] = [];
        slideWalk(c, o);
        return oneLine(o.join(''));
      });
    out.push(cells.join('\t') + '\n');
    return;
  }
  for (const c of kids(n)) slideWalk(c, out);
  if (name === 'p') out.push('\n');
}
const slideText = (doc: Document | null) => {
  const o: string[] = [];
  if (doc) slideWalk(doc.documentElement, o);
  return o
    .join('')
    .replace(/\n{2,}/g, '\n')
    .trim();
};

/**
 * Reads a PowerPoint file: the text of each slide in order, each followed by
 * its speaker notes.
 */
export function readPptx(bytes: Uint8Array) {
  const parts = unpack(bytes, n =>
    /^ppt\/(slides\/slide\d+\.xml|slides\/_rels\/slide\d+\.xml\.rels|notesSlides\/notesSlide\d+\.xml)$/.test(
      n,
    ),
  );
  const slides = Object.keys(parts)
    .filter(n => /^ppt\/slides\/slide\d+\.xml$/.test(n))
    .sort(byNumber(/slide(\d+)\.xml$/));
  if (!slides.length) {
    throw new ImportError('This PowerPoint file has no slides inside.');
  }
  const out = slides.map((name, i) => {
    const rels = parts[name.replace('slides/', 'slides/_rels/') + '.rels'];
    const noteTarget =
      rels &&
      strFromU8(rels).match(/Target="\.\.\/(notesSlides\/notesSlide\d+\.xml)"/);
    const notes = noteTarget
      ? slideText(xml(parts['ppt/' + noteTarget[1]]))
      : '';
    return [
      `Slide ${i + 1}`,
      slideText(xml(parts[name])),
      notes ? `Speaker notes: ${notes}` : '',
    ]
      .filter(Boolean)
      .join('\n');
  });
  return {
    text: out.join('\n\n'),
    kind: 'PowerPoint presentation',
    detail: plural(slides.length, 'slide'),
    notes: [] as string[],
  };
}

// ---------------- Excel ----------------
/**
 * Reads an Excel workbook as tab-separated rows under a heading per sheet,
 * hidden sheets included. Numbers and dates read the way Excel displays them. A
 * formula with no saved result is kept as its text.
 */
export function readXlsx(bytes: Uint8Array) {
  const parts = unpack(bytes, n =>
    /^xl\/(workbook\.xml|_rels\/workbook\.xml\.rels|sharedStrings\.xml|styles\.xml|worksheets\/[^/]+\.xml)$/.test(
      n,
    ),
  );
  const book = xml(parts['xl/workbook.xml']);
  if (!book) {
    throw new ImportError('This Excel file has no readable workbook inside.');
  }

  const strings = Array.from(
    xml(parts['xl/sharedStrings.xml'])?.getElementsByTagName('si') ?? [],
  ).map(si =>
    Array.from(si.getElementsByTagName('t'))
      .filter(t => t.parentElement?.localName !== 'rPh')
      .map(t => t.textContent ?? '')
      .join(''),
  );

  // Number formats, so dates and money read the way they look in Excel.
  const styles = xml(parts['xl/styles.xml']);
  const custom = new Map<number, string>();
  for (const f of Array.from(styles?.getElementsByTagName('numFmt') ?? [])) {
    custom.set(
      Number(f.getAttribute('numFmtId')),
      f.getAttribute('formatCode') ?? '',
    );
  }
  const xfs = Array.from(
    styles?.getElementsByTagName('cellXfs')[0]?.children ?? [],
  ).map(xf => Number(xf.getAttribute('numFmtId') ?? 0));
  const codeOf = (s: string | null) =>
    formatCode(xfs[Number(s ?? 0)] ?? 0, custom);
  const date1904 =
    book.getElementsByTagName('workbookPr')[0]?.getAttribute('date1904') ===
    '1';

  const rels = new Map<string, string>();
  for (const m of strFromU8(
    parts['xl/_rels/workbook.xml.rels'] ?? new Uint8Array(),
  ).matchAll(/<Relationship\b[^>]*>/g)) {
    const id = m[0].match(/\bId="([^"]+)"/)?.[1];
    const target = m[0].match(/\bTarget="([^"]+)"/)?.[1];
    if (id && target) rels.set(id, target.replace(/^\/?(xl\/)?/, 'xl/'));
  }

  const sheets = Array.from(book.getElementsByTagName('sheet'));
  const out: string[] = [];
  for (const sheet of sheets) {
    const rid =
      sheet.getAttribute('r:id') ??
      sheet.getAttributeNS(
        'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'id',
      ) ??
      '';
    const doc = xml(parts[rels.get(rid) ?? '']);
    if (!doc) continue;
    const lines: string[] = [];
    for (const row of Array.from(doc.getElementsByTagName('row'))) {
      const cells: string[] = [];
      for (const c of kids(row).filter(x => x.localName === 'c')) {
        const col = (c.getAttribute('r') ?? '').replace(/\d+/g, '');
        const index = col
          ? [...col].reduce((n, ch) => n * 26 + ch.charCodeAt(0) - 64, 0) - 1
          : cells.length;
        const t = c.getAttribute('t');
        const v = kids(c).find(x => x.localName === 'v')?.textContent ?? '';
        const formula =
          kids(c).find(x => x.localName === 'f')?.textContent ?? '';
        // A formula with no saved result shows nothing in the grid, but its
        // text is in the file and can hold names and amounts. Keep it.
        let value = v === '' && formula ? `=${formula}` : v;
        if (t === 's') {
          value = strings[Number(v)] ?? '';
        } else if (t === 'inlineStr') {
          value = Array.from(c.getElementsByTagName('t'))
            .map(x => x.textContent ?? '')
            .join('');
        } else if (t === 'b') {
          value = v === '1' ? 'TRUE' : 'FALSE';
        } else if (
          v !== '' &&
          t !== 'str' &&
          t !== 'e' &&
          !Number.isNaN(Number(v))
        ) {
          value = displayNumber(
            Number(v),
            codeOf(c.getAttribute('s')),
            date1904,
          );
        }
        while (cells.length < index && cells.length < 200) cells.push('');
        cells.push(oneLine(value));
      }
      const line = cells.join('\t').replace(/\t+$/, '');
      if (line.trim()) lines.push(line);
    }
    const hidden = /hidden/i.test(sheet.getAttribute('state') ?? '')
      ? ' (hidden sheet)'
      : '';
    if (lines.length) {
      out.push(
        `Sheet: ${sheet.getAttribute('name') ?? ''}${hidden}\n${lines.join('\n')}`,
      );
    }
  }
  if (!out.length) {
    throw new ImportError('No text was found in this Excel file.');
  }
  return {
    text: out.join('\n\n'),
    kind: 'Excel workbook',
    detail: plural(out.length, 'sheet'),
    notes: [] as string[],
  };
}

// ---------------- OpenDocument ----------------
const ODF_SKIP = new Set([
  'tracked-changes',
  'annotation',
  'forms',
  'sequence-decls',
  'note-citation',
  'table-of-content-source',
]);

function odfWalk(n: Element, out: string[]) {
  const name = n.localName;
  if (ODF_SKIP.has(name)) return;
  if (name === 'tab') {
    out.push('\t');
    return;
  }
  if (name === 'line-break') {
    out.push('\n');
    return;
  }
  // text:c is file-controlled. Cap it so a crafted document cannot exhaust
  // memory.
  if (name === 's') {
    const count = Number(n.getAttribute('text:c') ?? 1);
    out.push(
      ' '.repeat(
        Number.isFinite(count)
          ? Math.min(Math.max(Math.trunc(count), 0), 64)
          : 1,
      ),
    );
    return;
  }
  if (name === 'table-row') {
    const cells = kids(n)
      .filter(c => c.localName === 'table-cell')
      .map(c => {
        const o: string[] = [];
        odfWalk(c, o);
        return oneLine(o.join(''));
      });
    const line = cells.join('\t').replace(/\t+$/, '');
    if (line) out.push(line + '\n');
    return;
  }
  for (const c of Array.from(n.childNodes)) {
    if (c.nodeType === 3) out.push(c.nodeValue ?? '');
    else if (c.nodeType === 1) odfWalk(c as Element, out);
  }
  if (name === 'p' || name === 'h') out.push('\n');
}

/**
 * Reads an OpenDocument text, spreadsheet or presentation: page header, body,
 * then page footer. Tracked changes and comments are left out.
 */
export function readOdf(bytes: Uint8Array) {
  const parts = unpack(
    bytes,
    n => n === 'content.xml' || n === 'styles.xml' || n === 'mimetype',
  );
  const content = xml(parts['content.xml']);
  if (!content) {
    throw new ImportError(
      'This OpenDocument file has no readable content inside.',
    );
  }
  const body =
    content.getElementsByTagNameNS('*', 'body')[0] ?? content.documentElement;
  const out: string[] = [];
  const master = xml(parts['styles.xml'])?.getElementsByTagNameNS(
    '*',
    'master-styles',
  )[0];
  const edge = (tag: string) => {
    const o: string[] = [];
    for (const el of Array.from(
      master?.getElementsByTagNameNS('*', tag) ?? [],
    )) {
      odfWalk(el, o);
    }
    return o.join('').trim();
  };
  const header = edge('header');
  const footer = edge('footer');
  odfWalk(body, out);
  const mime = strFromU8(parts.mimetype ?? new Uint8Array());
  const kind = mime.includes('spreadsheet')
    ? 'OpenDocument spreadsheet'
    : mime.includes('presentation')
      ? 'OpenDocument presentation'
      : 'OpenDocument text';
  return {
    text: [header, out.join('').trim(), footer].filter(Boolean).join('\n\n'),
    kind,
    detail: '',
    notes: [] as string[],
  };
}
