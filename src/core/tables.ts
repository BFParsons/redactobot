/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Tables read by their headings.
 *
 * Many sensitive values sit in a table with nothing beside them to say what
 * they are: a four-digit employee ID, a check number, an amount with no
 * currency sign. The column heading (or, in a two-column form, the label in the
 * first cell) says it. Imported Word, Excel, HTML and PowerPoint tables arrive
 * as tab-separated lines; plain-text tables are aligned with runs of spaces;
 * Markdown tables use pipes. All three are handled.
 *
 * Each heading is mapped to one of the app's existing checks, so a rule set
 * that does not call for, say, record numbers does not get them from tables
 * either.
 */

/** A table cell value identified by its column heading or form label. */
export interface TableMatch {
  start: number;
  end: number;
  text: string;
  /**
   * The check the heading maps to: a detector id, 'names', 'places' or
   * 'region'.
   */
  type: string;
}

interface Kind {
  type: string;
  ok: (cell: string) => boolean;
}

const hasDigit = (s: string) => /\p{Nd}/u.test(s);
const numeric = (s: string) =>
  /^[($£€-]?\s?[\d,]+(?:\.\d+)?\)?(?:\s?[A-Z]{3})?$/.test(s) &&
  hasDigit(s) &&
  !/^(?:19|20)\d{2}$/.test(s);
const nameLike = (s: string) =>
  /^\p{Lu}[\p{L}.'’-]*(?:[ ,]+(?:\p{Lu}[\p{L}.'’-]*|de|la|del|van|von|der|&|and|of)){0,6}\.?$/u.test(
    s,
  ) &&
  s.length >= 3 &&
  s.length <= 60;
const idLike = (s: string) =>
  hasDigit(s) &&
  s.length >= 3 &&
  s.length <= 40 &&
  !/\s{2,}/.test(s) &&
  s.split(' ').length <= 4;
const recordLike = (s: string) =>
  s.length <= 128 &&
  /[\p{L}\p{N}]/u.test(s) &&
  !/^(?:none|null|unknown|pending|unassigned|n\/?a|not (?:available|assigned|provided))$/i.test(
    s,
  );
const placeLike = (s: string) =>
  s.length <= 100 &&
  /^[\p{L}\p{M}][\p{L}\p{M} .'’,-]*$/u.test(s) &&
  !/^(?:none|null|unknown|n\/?a)$/i.test(s);

// Heading words -> the check that owns that kind of value. First match wins.
const HEADINGS: Array<[RegExp, Kind]> = [
  // Labels for a person that contain a word used for something else ("fee",
  // "date")
  [
    /\b(?:fee earner|known as|prepared by|reviewed by|approved by|signed by|reported by|seen by|referred by|taken by|entered by|billed to|bill to|ship to|sold to|attn|attention)\b/i,
    {type: 'names', ok: nameLike},
  ],
  [
    /\b(?:ssn|ss#|social(?: sec(?:urity)?)?|sin|itin|tin|ein|tax(?:payer)? id|bn|vat)\b/i,
    {type: 'ssn', ok: hasDigit},
  ],
  [
    /\b(?:dob|d\.o\.b\.?|birth ?date|date of birth|born|birthday)\b/i,
    {type: 'dob', ok: hasDigit},
  ],
  [/^age$/i, {type: 'age90', ok: s => /^(?:9\d|1[01]\d)$/.test(s)}],
  [
    /\b(?:e-?mail|courriel|correo)\b/i,
    {type: 'email', ok: s => s.includes('@')},
  ],
  [
    /\b(?:téléphone|telephone|tél|teléfono|telefono|cellulaire|móvil)\b/i,
    {type: 'phone', ok: hasDigit},
  ],
  [
    /\b(?:code postal|código postal|codigo postal)\b/i,
    {type: 'zip', ok: hasDigit},
  ],
  [
    /\b(?:adresse|dirección|direccion|domicile|domicilio)\b/i,
    {type: 'street', ok: s => s.length >= 5},
  ],
  [
    /\b(?:ville|ciudad|localité|municipalité|municipio)\b/i,
    {type: 'places', ok: placeLike},
  ],
  [
    /\b(?:date de naissance|fecha de nacimiento|née? le)\b/i,
    {type: 'dob', ok: hasDigit},
  ],
  [
    /\b(?:personne-ressource|personne ressource|responsable|contacto)\b/i,
    {type: 'names', ok: nameLike},
  ],
  [
    /\b(?:phone|tel(?:ephone)?|cell|mobile|fax|direct line|ext(?:ension)?)\b/i,
    {type: 'phone', ok: hasDigit},
  ],
  [
    /\b(?:plate|plates|tag no|vin|hull|veh(?:icle)? (?:id|no|reg))\b/i,
    {type: 'vin', ok: idLike},
  ],
  [
    /\b(?:passport|licen[sc]e|dl|state id|bar (?:no|number|id)|npi|dea|medicare|mbi|phn|ohip|nhs|ni number|nino|national insurance|visa no|a-number)\b/i,
    {type: 'passport_dl', ok: idLike},
  ],
  [
    /\b(?:routing|aba|rtn|sort code|transit)\b/i,
    {type: 'routing', ok: hasDigit},
  ],
  [
    /\b(?:user ?name|user ?id|login|log-in|password|passcode|pin)\b/i,
    {
      type: 'credential',
      ok: s =>
        s.length >= 3 && !/\s/.test(s) && /[\d._\\@#!$-]|^[a-z]+$/.test(s),
    },
  ],
  [
    /\b(?:cvv2?|cvc2?|csc|cid|sec(?:urity)? code)\b/i,
    {type: 'cvv', ok: s => /^\d{3,4}$/.test(s)},
  ],
  [
    /^(?:exp\.?|expiry|expires|expiration)(?: date)?$/i,
    {type: 'card_exp', ok: hasDigit},
  ],
  [
    /\b(?:card(?: no| number| #)?|pan|cc ?#?)\b/i,
    {type: 'card_partial', ok: hasDigit},
  ],
  // A reference range in a lab report is a published norm, not the patient's
  // value.
  [
    /\b(?:reference range|ref\.? range|normal range|range|units?|flag)\b/i,
    {type: 'none', ok: () => false},
  ],
  // A ledger's "Account" column holds chart-of-accounts names ("1010
  // Checking"), not bank account numbers.
  [
    /\b(?:account|acct|a\/c|iban|swift|bic)\b/i,
    {type: 'account', ok: s => idLike(s) && !/^\d{3,5} [A-Za-z]/.test(s)},
  ],
  [
    /\b(?:check|cheque|chk|ck|invoice|inv|ref(?:erence)?|claim|policy|case|docket|matter|file|mrn|chart|member|subscriber|group|loan|order|po|receipt|confirmation|ticket|folio|employee id|emp(?:loyee)? ?(?:no|#|id)|badge|id|no\.?|number|#|rx|prescription|record|serial|tag|unit|encounter|accession|specimen|referral)\b/i,
    {type: 'record', ok: recordLike},
  ],
  [/\b(?:zip|postal ?code|postcode)\b/i, {type: 'zip', ok: hasDigit}],
  [/\b(?:address|street|addr)\b/i, {type: 'street', ok: s => s.length >= 5}],
  [
    /\b(?:state|province|prov|st)\b/i,
    {type: 'region', ok: s => /^[A-Z]{2}$/.test(s) || nameLike(s)},
  ],
  [
    /\b(?:city|town|county|location|site|branch|area)\b/i,
    {type: 'places', ok: placeLike},
  ],
  [
    /\b(?:amount|amt|balance|bal|total|subtotal|paid|payment|payments|charge|charges|fee|fees|price|cost|rate|salary|wage|wages|gross|net|debit|credit|deposit|withdrawal|draw|tax|ytd|earnings|deductions?|refund|due|owed|value|income|expense|expenses|proceeds|principal|interest|limit|budget|bonus|commission|rent|premium|copay|deductible|hours? pay|pay)\b/i,
    {type: 'money', ok: numeric},
  ],
  [
    /\b(?:date|dated|period|as of|hired|hire|start|end|issued|expires?|expiry|due date|service|admit(?:ted)?|discharged?|visit|filed|posted|cleared)\b/i,
    {type: 'date', ok: hasDigit},
  ],
  [
    /^(?:last|first|surname|given|middle|forename|nom|prénom|prenom|apellidos?|nombre)(?: names?)?$/i,
    {type: 'names', ok: nameLike},
  ],
  [
    /\b(?:name|employee|payee|payer|customer|client|patient|vendor|supplier|contact|tenant|landlord|owner|borrower|lender|beneficiary|insured|claimant|witness|attorney|counsel|provider|physician|doctor|preparer|manager|supervisor|officer|party|plaintiff|defendant|debtor|creditor|signer|signatory|cardholder|spouse|dependent|child|parent|guardian|known as|fee earner|opponent|carrier|employer|company|firm|bank|institution|organization|organisation|issuer|from|to|cc|by)\b/i,
    {type: 'names', ok: nameLike},
  ],
];

function kindOf(heading: string): Kind | undefined {
  // "Emp #" reads as "Emp no"
  const h = heading.trim().replace(/#/g, ' no ').replace(/\s+/g, ' ').trim();
  if (!h || h.length > 40) return undefined;
  return HEADINGS.find(([re]) => re.test(h))?.[1];
}

interface Cell {
  text: string;
  start: number;
  end: number;
}

type Mode = 'tab' | 'space' | 'pipe';

/**
 * Split a line into cells on tabs, on pipes, or on runs of two or more spaces.
 */
function cellsOf(line: string, offset: number, mode: Mode): Cell[] {
  const out: Cell[] = [];
  const sep = mode === 'tab' ? /\t/g : mode === 'pipe' ? /\|/g : / {2,}/g;
  let at = 0;
  const push = (from: number, to: number) => {
    const raw = line.slice(from, to);
    const lead = raw.length - raw.trimStart().length;
    const text = raw.trim();
    out.push({
      text,
      start: offset + from + lead,
      end: offset + from + lead + text.length,
    });
  };
  for (const m of line.matchAll(sep)) {
    push(at, m.index);
    at = m.index + m[0].length;
  }
  push(at, line.length);
  // A Markdown row starts and ends with a pipe, which leaves an empty cell at
  // each end.
  if (mode === 'pipe') {
    if (out.length && !out[0].text) out.shift();
    if (out.length && !out[out.length - 1].text) out.pop();
  }
  return out;
}

const looksLikeHeader = (cells: Cell[]) =>
  cells.filter(c => c.text).length >= 2 &&
  // "401(k)" and form numbers are headings, not data.
  cells.every(
    c =>
      c.text.length <= 40 &&
      !/\d{3,}/.test(
        c.text.replace(
          /\b(?:401|403|457)\s?\(?[kb]\)?|\b(?:1099|1040|1098|941|940)\b|\b(?:19|20)\d{2}\b/gi,
          '',
        ),
      ),
  ) &&
  cells.filter(c => kindOf(c.text)).length >= 1;

/**
 * Values identified by a column heading or a form label.
 * `allowed` is the list of checks the selected rule sets call for.
 */
export function tableDetections(
  text: string,
  allowed: readonly string[],
): TableMatch[] {
  const out: TableMatch[] = [];
  const add = (cell: Cell, kind: Kind | undefined) => {
    if (
      !kind ||
      !cell.text ||
      !allowed.includes(kind.type) ||
      !kind.ok(cell.text)
    ) {
      return;
    }
    // Two fields on one line are not necessarily a two-column form. For
    // example, "Date 14 March 2026  Location: 123 Elm St" must not make the
    // address a date.
    const nested =
      /^([\p{L} .#/-]{1,35}):\s*/u.exec(cell.text) ??
      /^([\p{L}][\p{L} .#/-]{0,35}?)[ \t]+(?=\d)/u.exec(cell.text);
    const nestedKind = nested ? kindOf(nested[1]) : undefined;
    if (nestedKind && nestedKind.type !== kind.type) return;
    out.push({
      start: cell.start,
      end: cell.end,
      text: cell.text,
      type: kind.type,
    });
  };

  const lines: Array<{text: string; offset: number}> = [];
  let offset = 0;
  for (const line of text.split('\n')) {
    lines.push({text: line, offset});
    offset += line.length + 1;
  }

  for (const mode of ['tab', 'space', 'pipe'] as Mode[]) {
    const byTab = mode !== 'space';
    let header: Cell[] | null = null;
    let kinds: Array<Kind | undefined> = [];
    for (const {text: line, offset: at} of lines) {
      const isRow =
        mode === 'tab'
          ? line.includes('\t')
          : mode === 'pipe'
            ? /^\s*\|.*\|\s*$/.test(line) && !line.includes('\t')
            : / {2,}\S/.test(line.trimStart()) &&
              !line.includes('\t') &&
              !/^\s*\|.*\|\s*$/.test(line);
      if (!isRow) {
        if (line.trim() === '' && byTab) continue;
        header = null;
        continue;
      }
      const cells = cellsOf(byTab ? line : line.trimEnd(), at, mode);
      if (mode === 'pipe' && cells.every(c => /^:?-{2,}:?$/.test(c.text))) {
        // the rule under a Markdown header
        continue;
      }

      // A two-cell row is a form line: label, then value.
      if (
        cells.length === 2 &&
        !header &&
        !(looksLikeHeader(cells) && kindOf(cells[1].text))
      ) {
        add(cells[1], kindOf(cells[0].text.replace(/[:#]+$/, '')));
        continue;
      }
      if (
        !header ||
        (looksLikeHeader(cells) && cells.length !== header.length)
      ) {
        if (looksLikeHeader(cells)) {
          header = cells;
          kinds = cells.map(c => kindOf(c.text));
        }
        continue;
      }
      // A data row under a header. Aligned-space tables can lose a cell when a
      // value is blank, so only rows with the same number of cells are trusted.
      // Imported tables drop empty cells at the end of a row, so a
      // tab-separated row may be shorter.
      if (
        mode === 'tab'
          ? cells.length > header.length
          : cells.length !== header.length
      ) {
        continue;
      }
      cells.forEach((c, i) => add(c, kinds[i]));
    }
  }
  return out;
}
