/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';
import {FRAMEWORKS, planFor} from '../../taxonomy/taxonomy.js';
import {discoverNames} from './names';
import {applyRedactions, buildDetections, type Topics} from './redact';
import {tableDetections} from './tables';

const ALL: string[] = planFor(
  FRAMEWORKS.map((f: {id: string}) => f.id),
).detectorIds;
const none = {people: [], companies: []};
const kinds = (text: string, allowed = ALL) =>
  tableDetections(text, allowed).map(m => `${m.type}:${m.text}`);

// All data here is fictional.
describe('tables read by their headings', () => {
  it('uses a column heading for values that carry no label of their own', () => {
    const text =
      'Emp ID\tEmployee\tCheck #\tGross\n1017\tWisniewski, Katarzyna\t20418\t4,807.69\n1022\tBill McAllister\t20421\t41.50';
    expect(kinds(text)).toEqual([
      'record:1017',
      'names:Wisniewski, Katarzyna',
      'record:20418',
      'money:4,807.69',
      'record:1022',
      'names:Bill McAllister',
      'record:20421',
      'money:41.50',
    ]);
  });
  it('reads a two-column form: label, then value', () => {
    expect(
      kinds(
        'Known as\tSade\nPassport\t533184726\nFee earner\tRJP\nAttendance\tIn person, 55 minutes',
      ),
    ).toEqual(['names:Sade', 'passport_dl:533184726', 'names:RJP']);
  });
  it('reads a plain-text table aligned with spaces', () => {
    const text =
      'Check   Date    Payee               Amount\n20418   06/26   Skerries Rope        18,406.00\n20421   06/29   Dory Lane Supply     1,250.00';
    expect(kinds(text)).toEqual(
      expect.arrayContaining([
        'record:20418',
        'date:06/26',
        'names:Skerries Rope',
        'money:18,406.00',
        'record:20421',
      ]),
    );
  });
  it('only uses checks the selected rules call for', () => {
    const text = 'Emp ID\tGross\n1017\t4,807.69';
    expect(kinds(text, ['money'])).toEqual(['money:4,807.69']);
    expect(kinds(text, [])).toEqual([]);
  });
  it('ignores ordinary prose and headings it does not recognise', () => {
    expect(
      kinds(
        'The parties met on Tuesday.  They agreed on nothing.\nStatus\tNotes\nOpen\tAwaiting reply',
      ),
    ).toEqual([]);
  });
  it('feeds table names and numbers into the replaced text', () => {
    const text =
      'Emp ID\tEmployee\tGross\n1017\tWisniewski, Katarzyna\t4,807.69\n\nKatarzyna asked about her pay.';
    const out = applyRedactions(text, buildDetections(text, ALL, none)).cleaned;
    expect(out).not.toMatch(/1017|Wisniewski|Katarzyna|4,807/);
    expect(out).toContain('asked about her pay');
  });
});

describe('first names, nicknames and initials on their own', () => {
  const people = (t: string) => discoverNames(t).people;
  it('recognises common given names without a surname', () => {
    expect(
      people('Mateo will stay with Barbara on weekends; Gwen agreed.'),
    ).toEqual(expect.arrayContaining(['Mateo', 'Barbara', 'Gwen']));
  });
  it('treats a name that is also a word as a name only when the sentence says so', () => {
    expect(
      people(
        "The hearing is in May. We spoke with Grace, and Hunter's truck was sold.",
      ),
    ).toEqual(expect.arrayContaining(['Grace', 'Hunter']));
    expect(
      people(
        'Payment is due in May. Will the court grant the motion? Chase the invoice.',
      ),
    ).toEqual([]);
  });
  it('recognises initials written with full stops', () => {
    expect(
      people('T.J. will drive. Filed in the U.S. District Court at 9 A.M.'),
    ).toEqual(['T.J.']);
  });
});

describe('places and sensitive topics from the on-device model', () => {
  const text =
    "She lives in Wenatchee with her mother. Diagnosed with relapsing-remitting multiple sclerosis in 2023; attends Jumu'ah prayers. Sade called.";
  const topics: Topics = {
    places: ['Wenatchee'],
    health: ['relapsing-remitting multiple sclerosis'],
    sensitive: ["Jumu'ah prayers"],
    names: ['Sade', 'Plaintiff', '2023'],
  };
  const dets = buildDetections(text, ALL, none, [], new Set(), topics);
  const by = (t: string) => dets.find(d => d.text === t)!;

  it('replaces places and first names the model found', () => {
    expect(by('Wenatchee').kind).toBe('places');
    expect(by('Sade').kind).toBe('person');
    expect(dets.some(d => d.text === 'Plaintiff')).toBe(false);
  });
  it('flags sensitive topics without replacing them', () => {
    expect(by('relapsing-remitting multiple sclerosis')).toMatchObject({
      kind: 'health',
      defaultOn: false,
      enabled: false,
    });
    expect(by("Jumu'ah prayers")).toMatchObject({
      kind: 'sensitive',
      enabled: false,
    });
    const out = applyRedactions(text, dets).cleaned;
    expect(out).toContain('multiple sclerosis');
    expect(out).not.toContain('Wenatchee');
  });
  it('replaces a flagged topic once the user selects it', () => {
    const id = by('relapsing-remitting multiple sclerosis').id;
    const again = buildDetections(text, ALL, none, [], new Set([id]), topics);
    expect(applyRedactions(text, again).cleaned).toContain('[HEALTH_DETAIL_1]');
  });
  it('does nothing with topics when the selected rules do not include them', () => {
    const narrow: string[] = planFor(['frcp52']).detectorIds;
    expect(
      buildDetections(text, narrow, none, [], new Set(), topics).some(
        d => d.kind === 'health' || d.kind === 'places',
      ),
    ).toBe(false);
  });
});

describe('tables: headings with a year or "401(k)", and Markdown tables', () => {
  it('accepts a header that holds "401(k)" or a year', () => {
    const text =
      'EMP ID  NAME                 GROSS      401(k)   NET\n1017    McALLISTER, BILL     3,137.20   156.86   2,207.55';
    expect(
      tableDetections(text, ['record', 'names', 'money']).map(
        m => `${m.type}:${m.text}`,
      ),
    ).toContain('record:1017');
    const fees = 'City\tST\tZIP\t2025 fee\nTulsa\tOK\t74104\t$425.00';
    expect(
      tableDetections(fees, ['region', 'places', 'zip', 'money']).map(
        m => `${m.type}:${m.text}`,
      ),
    ).toContain('region:OK');
  });
  it('reads a Markdown table by its header', () => {
    const text =
      '| System | Username | Notes |\n|---|---|---|\n| Payroll self-service | 618THM | she sets her own password |';
    expect(
      tableDetections(text, ['credential']).map(m => `${m.type}:${m.text}`),
    ).toEqual(['credential:618THM']);
  });
});
