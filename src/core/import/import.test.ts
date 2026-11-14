/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {describe, expect, it} from 'vitest';
import {zipSync, strToU8} from 'fflate';
import {importBytes, ImportError} from './index';
import {rtfToText, emlToText, htmlToText} from './formats';
import {extractPdfText} from './pdf';

// Fixtures are made by tools/make_fixtures.py with python-docx, openpyxl,
// python-pptx and LibreOffice. All content is fictional.
const fixture = (name: string) =>
  new Uint8Array(readFileSync(resolve('src/core/import/fixtures', name)));
const load = (name: string) => importBytes(name, fixture(name));

describe('Word (.docx)', () => {
  it('reads body, table, header and footer', async () => {
    const d = await load('sample.docx');
    expect(d.kind).toBe('Word document');
    expect(d.text).toContain(
      'Met with Margaret Whitfield regarding Whitfield & Daughters Holdings Ltd.',
    );
    expect(d.text).toContain(
      'Her son Tom Whitfield joined by phone.\tFollow up: margaret@whitfieldholdings.example',
    );
    expect(d.text).toContain('Division sale\t$1,250,000');
    expect(d.text).toContain('Account 4471-889-2203 at Cascadia Credit Union.');
    expect(d.text.startsWith('Raman & Associates CPA')).toBe(true);
    expect(d.text).toContain('Confidential. File no. 2026-0147');
  });
});

describe('Excel (.xlsx)', () => {
  it('reads every sheet, with dates and money as they look in Excel', async () => {
    const d = await load('sample.xlsx');
    expect(d.detail).toMatch(/^2 sheets/);
    expect(d.text).toContain('Sheet: Ledger\nDate\tPayee\tAmount\tAccount');
    expect(d.text).toContain(
      '2026-03-14\tNorthgate Bookkeeping\t$8,400.00\t4471-889-2203',
    );
    expect(d.text).toContain(
      '2026-05-02\tHarbourline Marine Supply\t$62,000.50\t5520-114-9087',
    );
    expect(d.text).toContain(
      'Sheet: Contacts\nName\tPhone\nDaniel Okafor\t604-555-0142',
    );
  });
});

describe('Excel formulas', () => {
  it('keeps the text of a formula that has no saved result', async () => {
    const sheet =
      '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row r="1">' +
      '<c r="A1" t="inlineStr"><is><t>Note</t></is></c><c r="B1"><f> urgent care $175 not yet coded + $10 late fee</f></c>' +
      '<c r="C1"><f>SUM(A2:A3)</f><v>42</v></c></row></sheetData></worksheet>';
    const book = zipSync({
      'xl/workbook.xml': strToU8(
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="S" sheetId="1" r:id="rId1"/></sheets></workbook>',
      ),
      'xl/_rels/workbook.xml.rels': strToU8(
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>',
      ),
      'xl/worksheets/sheet1.xml': strToU8(sheet),
    });
    const d = await importBytes('f.xlsx', book);
    expect(d.text).toContain('= urgent care $175 not yet coded + $10 late fee');
    expect(d.text).toContain('42');
    expect(d.text).not.toContain('SUM(');
  });
});

describe('PowerPoint (.pptx)', () => {
  it('reads slides in order with speaker notes', async () => {
    const d = await load('sample.pptx');
    expect(d.detail).toMatch(/^2 slides/);
    expect(d.text).toMatch(
      /^Slide 1\nYear-end review\nClient: Margaret Whitfield\nSale to Harbourline Marine Supply\nSpeaker notes: Mention the \$62,000 warranty dispute\./,
    );
    expect(d.text).toContain(
      'Slide 2\nNext steps\nCall Daniel Okafor at 604-555-0142',
    );
  });
});

describe('OpenDocument (.odt) and Rich Text (.rtf)', () => {
  for (const name of ['sample.odt', 'sample.rtf']) {
    it(`reads ${name}`, async () => {
      const d = await load(name);
      expect(d.text).toContain(
        'Met with Margaret Whitfield regarding Whitfield & Daughters Holdings Ltd.',
      );
      expect(d.text).toContain('Tom Whitfield');
      expect(d.text).toContain('$1,250,000');
      expect(d.text).toContain(
        'Account 4471-889-2203 at Cascadia Credit Union.',
      );
      expect(d.text).toContain('Raman & Associates CPA');
      // no RTF codes or font tables
      expect(d.text).not.toMatch(/\\[a-z]+\d*|Times New Roman|Liberation/);
    });
  }
  it('handles RTF escapes', () => {
    expect(
      rtfToText(
        "{\\rtf1\\ansi{\\fonttbl{\\f0 Arial;}}Caf\\'e9 \\u8212? ok\\par {\\*\\generator x;}line \\{2\\}}",
      ),
    ).toBe('Café — ok\nline {2}');
  });
});

describe('PDF', () => {
  const pdfjs = () => import('pdfjs-dist/legacy/build/pdf.mjs');
  it('reads a text PDF', async () => {
    const d = await extractPdfText(
      (await pdfjs()) as never,
      fixture('sample.pdf'),
    );
    expect(d.detail).toBe('1 page');
    expect(d.text).toContain(
      'Met with Margaret Whitfield regarding Whitfield & Daughters Holdings Ltd.',
    );
    expect(d.text).toContain('$1,250,000');
    expect(d.text).toContain('Account 4471-889-2203 at Cascadia Credit Union.');
  });
  it('says so when a PDF has no text (a scan)', async () => {
    await expect(
      extractPdfText((await pdfjs()) as never, fixture('scanned.pdf')),
    ).rejects.toThrow(/looks like a scan/);
  });
  it('rejects a damaged PDF', async () => {
    await expect(
      extractPdfText((await pdfjs()) as never, strToU8('%PDF-1.7 not really')),
    ).rejects.toBeInstanceOf(ImportError);
  });
});

describe('Email (.eml)', () => {
  it('reads headers and the plain-text part, decoding encoded words and quoted-printable', async () => {
    const d = await load('sample.eml');
    expect(d.kind).toBe('Email');
    expect(d.text).toContain('From: Priya Raman <priya@raman-cpa.example>');
    expect(d.text).toContain(
      'To: Margaret Whitfield <margaret@whitfieldholdings.example>',
    );
    expect(d.text).toContain('Subject: Year-end filing – next steps');
    expect(d.text).toContain(
      'transfer of $310,500.75 from account 5520-114-9087 before Friday. Café meeting',
    );
    expect(d.text).not.toContain('HTML version');
  });
  it('lists attachments without opening them, and falls back to the HTML part', () => {
    const raw = [
      'Subject: Hi',
      'Content-Type: multipart/mixed; boundary="x"',
      '',
      '--x',
      'Content-Type: text/html',
      '',
      '<p>Hello <b>Tom</b></p>',
      '--x',
      'Content-Type: application/pdf; name="ledger.pdf"',
      'Content-Disposition: attachment; filename="ledger.pdf"',
      'Content-Transfer-Encoding: base64',
      '',
      'JVBERi0=',
      '--x--',
      '',
    ].join('\r\n');
    const mail = emlToText(raw);
    expect(mail.text).toContain('Hello Tom');
    expect(mail.attachments).toEqual(['ledger.pdf']);
  });
});

describe('Web pages and plain text', () => {
  it('keeps visible text and drops scripts and styles', async () => {
    const d = await load('sample.html');
    expect(d.kind).toBe('Web page');
    expect(d.text).toContain('Met with Margaret Whitfield.');
    expect(d.text).toContain('- Account 4471-889-2203');
    expect(d.text).toContain('Sale\t$1,250,000');
    expect(d.text).not.toMatch(/should not appear|color:red/);
  });
  it('does not run anything in a page', () => {
    expect(
      htmlToText('<img src=x onerror="window.pwned=1"><p>ok</p>'),
    ).toContain('ok');
    expect((globalThis as Record<string, unknown>).pwned).toBeUndefined();
  });
  it('reads CSV, UTF-16 and Windows-1252 text', async () => {
    expect((await load('sample.csv')).text).toBe(
      'Payee,Amount\nNorthgate Bookkeeping,"$8,400"',
    );
    expect((await load('utf16.txt')).text).toBe(
      'Client: Zoë Müller, account 4471-889-2203',
    );
    expect((await load('latin1.txt')).text).toBe('Client: Zoë Müller');
  });
});

describe('files that cannot be read', () => {
  const fails = async (name: string, bytes: Uint8Array, message: RegExp) => {
    await expect(importBytes(name, bytes)).rejects.toBeInstanceOf(ImportError);
    await expect(importBytes(name, bytes)).rejects.toThrow(message);
  };
  it('explains old Office formats', () =>
    fails('sample.doc', fixture('sample.doc'), /older Office format/));
  it('explains Outlook .msg', () =>
    fails(
      'mail.msg',
      Uint8Array.of(0xd0, 0xcf, 0x11, 0xe0, 0, 0),
      /save the email as \.eml/,
    ));
  it('explains pictures', () =>
    fails(
      'scan.png',
      Uint8Array.of(0x89, 0x50, 0x4e, 0x47, 0, 0, 0, 0),
      /Pictures and scans/,
    ));
  it('rejects unknown binary files', () =>
    fails('data.bin', Uint8Array.of(1, 2, 0, 3), /not supported/));
  it('rejects empty files', () =>
    fails('empty.txt', new Uint8Array(), /empty/));
  it('rejects a plain zip', () =>
    fails('files.zip', zipSync({'a.txt': strToU8('hi')}), /one at a time/));
  it('rejects a Word file with nothing in it', () =>
    fails(
      'blank.docx',
      zipSync({
        'word/document.xml': strToU8(
          '<w:document xmlns:w="x"><w:body/></w:document>',
        ),
      }),
      /No text/,
    ));
  it('rejects a file over the size limit', () =>
    fails(
      'big.txt',
      new Uint8Array(26 * 1024 * 1024).fill(65),
      /larger than 25 MB/,
    ));
  it('refuses an archive that unpacks to an unsafe size', async () => {
    const bomb = zipSync(
      {'word/document.xml': new Uint8Array(45 * 1024 * 1024)},
      {level: 9},
    );
    expect(bomb.length).toBeLessThan(1024 * 1024);
    await fails('bomb.docx', bomb, /too large to open safely/);
  });
});

describe('OpenDocument space runs', () => {
  it('caps file-controlled repeat counts', async () => {
    const {zipSync, strToU8} = await import('fflate');
    const content =
      '<?xml version="1.0"?><office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><office:body><office:text><text:p>A<text:s text:c="100000000"/>B</text:p></office:text></office:body></office:document-content>';
    const bytes = zipSync({
      mimetype: strToU8('application/vnd.oasis.opendocument.text'),
      'content.xml': strToU8(content),
    });
    const {importFile} = await import('./index');
    const doc = await importFile(new File([bytes], 'bomb.odt'));
    expect(doc.text.length).toBeLessThan(200);
  });
});

describe('archive size limits', () => {
  it('never unpacks more than an entry declares, even if the archive lies', async () => {
    const {unpack} = await import('./office');
    // 5 MB that compresses to almost nothing, declared as 1,000 bytes.
    const zip = zipSync({
      'word/document.xml': new Uint8Array(5_000_000).fill(65),
    });
    const view = new DataView(zip.buffer);
    for (let i = 0; i < zip.length - 4; i++) {
      const signature = view.getUint32(i, true);
      if (signature === 0x04034b50) view.setUint32(i + 22, 1000, true);
      if (signature === 0x02014b50) view.setUint32(i + 24, 1000, true);
    }
    const parts = unpack(zip, () => true);
    expect(parts['word/document.xml'].length).toBe(1000);
  });

  it('refuses an entry that declares more than the limit', async () => {
    const {unpack} = await import('./office');
    const zip = zipSync({'word/document.xml': new Uint8Array(1000)});
    const view = new DataView(zip.buffer);
    for (let i = 0; i < zip.length - 4; i++) {
      if (view.getUint32(i, true) === 0x02014b50) {
        view.setUint32(i + 24, 500 * 1024 * 1024, true);
      }
    }
    expect(() => unpack(zip, () => true)).toThrow(/too large/);
  });
});
