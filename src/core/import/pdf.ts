/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview PDF text. Only PDFs with a text layer work; scanned pages are
 * pictures and are not read.
 */

import {ImportError, plural} from './text';

const MAX_PAGES = 300;

interface TextItem {
  str: string;
  hasEOL?: boolean;
  transform?: number[];
  height?: number;
}
interface PdfLib {
  getDocument(src: object): {
    promise: Promise<{
      numPages: number;
      getPage(
        n: number,
      ): Promise<{getTextContent(): Promise<{items: unknown[]}>}>;
    }>;
    destroy(): Promise<void>;
  };
}

/**
 * Pull the text out of a PDF with an already-loaded pdf.js. Separate so it can
 * be tested.
 */
export async function extractPdfText(pdfjs: PdfLib, data: Uint8Array) {
  // pdf.js takes ownership of the bytes it is given, so hand it a copy.
  const task = pdfjs.getDocument({
    data: data.slice(),
    isEvalSupported: false,
    disableFontFace: true,
    useSystemFonts: false,
    verbosity: 0,
  });
  let pdf;
  try {
    pdf = await task.promise;
  } catch (err) {
    await task.destroy().catch(() => {});
    const name = (err as {name?: string}).name;
    if (name === 'PasswordException') {
      throw new ImportError(
        'This PDF is password-protected. Remove the password and try again.',
      );
    }
    throw new ImportError('This PDF is damaged and could not be opened.');
  }
  try {
    const count = Math.min(pdf.numPages, MAX_PAGES);
    const pages: string[] = [];
    for (let n = 1; n <= count; n++) {
      const {items} = await (await pdf.getPage(n)).getTextContent();
      let text = '';
      let lastY: number | undefined;
      for (const raw of items) {
        const item = raw as TextItem;
        if (typeof item.str !== 'string') continue;
        const y = item.transform?.[5];
        // A jump down the page of more than a line and a half is a paragraph
        // break.
        if (
          lastY !== undefined &&
          y !== undefined &&
          item.height &&
          lastY - y > item.height * 1.9 &&
          text.endsWith('\n')
        ) {
          text += '\n';
        }
        text += item.str;
        if (item.hasEOL) text += '\n';
        if (y !== undefined && item.str.trim()) lastY = y;
      }
      pages.push(text.trim());
    }
    const body = pages.filter(Boolean).join('\n\n');
    if (body.replace(/\s/g, '').length < 20) {
      throw new ImportError(
        'This PDF has no text in it. It looks like a scan, and scanned documents cannot be read yet.',
      );
    }
    const notes: string[] = [];
    const empty = pages.filter(p => !p).length;
    if (empty) {
      notes.push(`${plural(empty, 'page')} had no text and may be scanned.`);
    }
    if (pdf.numPages > MAX_PAGES) {
      notes.push(`Only the first ${MAX_PAGES} pages were read.`);
    }
    return {
      text: body,
      kind: 'PDF',
      detail: plural(pdf.numPages, 'page'),
      notes,
    };
  } finally {
    await task.destroy().catch(() => {});
  }
}

/** Browser entry point. pdf.js is loaded only when a PDF is opened. */
export async function readPdf(data: Uint8Array) {
  const [pdfjs, worker] = await Promise.all([
    import('pdfjs-dist'),
    import('pdfjs-dist/build/pdf.worker.min.mjs?url'),
  ]);
  pdfjs.GlobalWorkerOptions.workerSrc = worker.default;
  return extractPdfText(pdfjs as unknown as PdfLib, data);
}
