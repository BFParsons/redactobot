/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Document import. A file is read and turned into text entirely
 * on this device. The file itself is never uploaded, stored or sent anywhere;
 * only the text continues into the app.
 */

import {emlToText, htmlToText, rtfToText} from './formats';
import {listEntries, readDocx, readOdf, readPptx, readXlsx} from './office';
import {ImportError, decodeText, latin1, plural, tidy} from './text';

export {ImportError};

/** The text read from a file, with a description of the file for the user. */
export interface Imported {
  name: string;
  text: string;
  /** Plain description of what the file was, for example "Word document". */
  kind: string;
  /** Size of the result, for example "3 pages · 1,204 words". */
  detail: string;
  /** Things the user should know were left out. */
  notes: string[];
}

/** The largest file accepted, in bytes (25 MB). */
export const MAX_FILE_BYTES = 25 * 1024 * 1024;

/**
 * What the file picker offers. Dropped files are checked by content, not by
 * this list.
 */
export const ACCEPT = [
  '.pdf',
  '.docx',
  '.xlsx',
  '.pptx',
  '.odt',
  '.ods',
  '.odp',
  '.rtf',
  '.eml',
  '.html',
  '.htm',
  '.csv',
  '.tsv',
  '.txt',
  '.md',
].join(',');
/** The accepted file types, worded for the user. */
export const ACCEPT_LABEL =
  'PDF, Word, Excel, PowerPoint, OpenDocument, RTF, email (.eml), web page, CSV or text';

const starts = (b: Uint8Array, ...sig: number[]) =>
  sig.every((v, i) => b[i] === v);
const ext = (name: string) =>
  name.toLowerCase().match(/\.([a-z0-9]+)$/)?.[1] ?? '';

interface Result {
  text: string;
  kind: string;
  detail: string;
  notes: string[];
}

async function read(name: string, bytes: Uint8Array): Promise<Result> {
  const e = ext(name);

  if (starts(bytes, 0x25, 0x50, 0x44, 0x46)) {
    // %PDF
    return (await import('./pdf')).readPdf(bytes);
  }
  if (starts(bytes, 0xd0, 0xcf, 0x11, 0xe0)) {
    // Old binary Office formats (.doc .xls .ppt) and Outlook .msg
    throw new ImportError(
      e === 'msg'
        ? 'Outlook .msg files cannot be read. In Outlook, save the email as .eml or copy the text.'
        : 'This is an older Office format. Open it and save it as .docx, .xlsx or .pptx, then try again.',
    );
  }
  if (starts(bytes, 0x50, 0x4b)) {
    // zip container
    const entries = listEntries(bytes);
    if (entries.some(n => n === 'word/document.xml')) return readDocx(bytes);
    if (entries.some(n => n === 'xl/workbook.xml')) return readXlsx(bytes);
    if (entries.some(n => n.startsWith('ppt/slides/'))) return readPptx(bytes);
    if (entries.includes('content.xml') && entries.includes('mimetype')) {
      return readOdf(bytes);
    }
    if (entries.some(n => n === 'EncryptedPackage')) {
      throw new ImportError(
        'This file is password-protected. Remove the password and try again.',
      );
    }
    throw new ImportError(
      e === 'zip'
        ? 'Zip files cannot be read. Add the documents inside one at a time.'
        : 'This file type is not supported.',
    );
  }
  if (latin1(bytes.subarray(0, 6)).startsWith('{\\rtf')) {
    return {
      text: rtfToText(latin1(bytes)),
      kind: 'Rich Text document',
      detail: '',
      notes: [],
    };
  }
  if (
    e === 'eml' ||
    (/^(Received|Return-Path|From|MIME-Version|Delivered-To|Date|Subject):/im.test(
      latin1(bytes.subarray(0, 400)),
    ) &&
      e !== 'txt' &&
      e !== 'md' &&
      e !== 'csv')
  ) {
    const mail = emlToText(latin1(bytes));
    return {
      text: mail.text,
      kind: 'Email',
      detail: '',
      notes: mail.attachments.length
        ? [
            `${plural(mail.attachments.length, 'attachment')} not read: ${mail.attachments.join(', ')}. Add them separately.`,
          ]
        : [],
    };
  }

  // Everything else must be text. Binary files have NUL bytes; UTF-16 text is
  // allowed.
  const utf16 = starts(bytes, 0xff, 0xfe) || starts(bytes, 0xfe, 0xff);
  if (!utf16 && bytes.subarray(0, 4096).includes(0)) {
    throw new ImportError(
      /^(png|jpe?g|gif|tiff?|bmp|webp|heic)$/.test(e)
        ? 'Pictures and scans cannot be read yet. Add a file that contains text.'
        : 'This file type is not supported.',
    );
  }
  const text = decodeText(bytes);
  if (
    e === 'html' ||
    e === 'htm' ||
    /^\s*(<!doctype html|<html[\s>])/i.test(text.slice(0, 200))
  ) {
    return {text: htmlToText(text), kind: 'Web page', detail: '', notes: []};
  }
  const kind =
    e === 'csv' || e === 'tsv'
      ? 'Spreadsheet (CSV)'
      : e === 'md'
        ? 'Markdown document'
        : 'Text file';
  return {text, kind, detail: '', notes: []};
}

/**
 * Turn a file's bytes into text. Throws ImportError with a message the user can
 * act on.
 */
export async function importBytes(
  name: string,
  bytes: Uint8Array,
): Promise<Imported> {
  if (bytes.length === 0) throw new ImportError('This file is empty.');
  if (bytes.length > MAX_FILE_BYTES) {
    throw new ImportError(
      'This file is larger than 25 MB. Split it into smaller documents.',
    );
  }
  let result: Result;
  try {
    result = await read(name, bytes);
  } catch (err) {
    if (err instanceof ImportError) throw err;
    throw new ImportError('This file could not be read. It may be damaged.');
  }
  const text = tidy(result.text);
  if (!text) throw new ImportError('No text was found in this file.');
  const words = (text.match(/\S+/g) ?? []).length;
  return {
    name,
    text,
    kind: result.kind,
    notes: result.notes,
    detail: [result.detail, `${words.toLocaleString('en-US')} words`]
      .filter(Boolean)
      .join(' · '),
  };
}

/**
 * Turns a file the user chose or dropped into text. Rejects a file over
 * MAX_FILE_BYTES before reading it. Throws ImportError with a message the user
 * can act on.
 */
export async function importFile(file: File): Promise<Imported> {
  if (file.size > MAX_FILE_BYTES) {
    throw new ImportError(
      'This file is larger than 25 MB. Split it into smaller documents.',
    );
  }
  return importBytes(file.name, new Uint8Array(await file.arrayBuffer()));
}
