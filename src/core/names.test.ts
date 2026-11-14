/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';
import {definedTerms, discoverNames, nameCandidates, type Names} from './names';
import {applyRedactions, buildDetections} from './redact';
import {displayNumber} from './import/numfmt';
import {FRAMEWORKS, planFor} from '../../taxonomy/taxonomy.js';

const ALL = planFor(FRAMEWORKS.map((f: {id: string}) => f.id)).detectorIds;
const none: Names = {people: [], companies: []};
const cleaned = (text: string, names: Names = none) =>
  applyRedactions(text, buildDetections(text, ALL, names)).cleaned;
const forms = (names: {people: string[]; companies: string[]}) =>
  nameCandidates(names).map(c => c.text);

// All names here are fictional.
describe('names read straight off the page, with no model', () => {
  const people = (t: string) => discoverNames(t).people;
  const companies = (t: string) => discoverNames(t).companies;

  it('uses titles', () => {
    expect(
      people(
        'Seen by Dr. Anand Krishnamurthy, then Judge Vandermeer and Mrs Adeyemi-Clarke.',
      ),
    ).toEqual(
      expect.arrayContaining([
        'Anand Krishnamurthy',
        'Vandermeer',
        'Adeyemi-Clarke',
      ]),
    );
  });
  it('uses a middle initial, a role, a relationship, and a form field', () => {
    expect(
      people(
        'The fee was set by Thomas J. Achebe and his paralegal Wendy Pruitt-Sato.',
      ),
    ).toEqual(
      expect.arrayContaining(['Thomas J. Achebe', 'Wendy Pruitt-Sato']),
    );
    expect(
      people(
        'It was signed by Marlene Fitch, RPR.\nPrepared by: Renee Calloway\nReviewed by\tImani Okoro',
      ),
    ).toEqual(
      expect.arrayContaining([
        'Marlene Fitch',
        'Renee Calloway',
        'Imani Okoro',
      ]),
    );
  });
  it('uses email display names, in either order', () => {
    expect(
      people(
        'Cc: Leon Brathwaite <lb@firm.example>, "Abimbola, Stuart" <sa@firm.example>',
      ),
    ).toEqual(expect.arrayContaining(['Leon Brathwaite', 'Stuart Abimbola']));
  });
  it('reads forms and court captions written in capitals', () => {
    expect(
      people(
        'Patient: OYELARAN, Adebayo T.\nIn re: MARISOL ECHEVARRIA-LUND, Petitioner, and TREVOR J. LUND, Respondent.',
      ),
    ).toEqual(
      expect.arrayContaining([
        'Adebayo T. Oyelaran',
        'MARISOL ECHEVARRIA-LUND',
        'TREVOR J. LUND',
      ]),
    );
  });
  it('finds organizations by how their names end', () => {
    expect(
      companies(
        'Paid to Okafor Pediatrics, P.C. from Monongahela Valley Federal Credit Union; the Wetherington 2009 Irrevocable Trust; Pellegrino & Yoo.',
      ),
    ).toEqual(
      expect.arrayContaining([
        'Okafor Pediatrics, P.C.',
        'Monongahela Valley Federal Credit Union',
        'Wetherington 2009 Irrevocable Trust',
        'Pellegrino & Yoo',
      ]),
    );
  });
  it('leaves everyday phrases and large places in capitals alone', () => {
    for (const text of [
      'I visited America last year.',
      'This Past Weekend I went hiking with friends.',
      'Over the Past Weekend we finished the report.',
      'My trip to South America and Saudi Arabia was fun.',
      'The recap: Team America won the match in Game Seven.',
      'Thanks, see you Next Week. Happy New Year and Merry Christmas.',
      'We watched the Tour de France. The van der Waals force is weak.',
    ]) {
      expect(discoverNames(text).people, text).toEqual([]);
    }
  });

  it('does not read the second word of a state name as a first name', () => {
    for (const text of [
      'She lives in New York and works in New Jersey.',
      'They met in North Carolina, West Virginia and South Dakota last May.',
    ]) {
      expect(discoverNames(text).people, text).toEqual([]);
    }
  });

  it('still finds people whose names are also places or everyday words', () => {
    const found = discoverNames(
      'Yesterday his partner Leland Forsythe wrote to Sarah Green about India Wilson and Kenya Moore, then called Jordan Smith and Georgia Brown.',
    );
    for (const name of [
      'Leland Forsythe',
      'Sarah Green',
      'India Wilson',
      'Kenya Moore',
      'Jordan Smith',
      'Georgia Brown',
    ]) {
      expect(found.people, name).toContain(name);
    }
  });

  it('finds names with a lower-case surname particle, anywhere in a sentence', () => {
    const found = discoverNames(
      'Nik van der Giesen sent the files. I spoke with Ludwig von Hartmann, Pieter van den Berg, Anna de la Cruz and Sofia di Marco.',
    );
    for (const name of [
      'Nik van der Giesen',
      'Ludwig von Hartmann',
      'Pieter van den Berg',
      'Anna de la Cruz',
      'Sofia di Marco',
    ]) {
      expect(found.people, name).toContain(name);
    }
  });

  it('leaves ordinary capitalized phrases alone', () => {
    const found = discoverNames(
      'A. Background\nSee Fed. R. Civ. P. 26 and the Internal Revenue Code. The Bank declined. Filed in Superior Court on Monday.',
    );
    expect(found.people).toEqual([]);
    expect(found.companies).toEqual([]);
  });
});

describe('the other ways one name gets written', () => {
  it('covers initials, "Last, First", capitals, no middle name and no accents', () => {
    expect(forms({people: ['Héctor K. Reyes'], companies: []})).toEqual(
      expect.arrayContaining([
        'Héctor Reyes',
        'Hector Reyes',
        'H. Reyes',
        'H.K. Reyes',
        'Reyes, Héctor',
        'REYES, Héctor K.',
        'HÉCTOR K. REYES',
        'HKR',
        'Reyes',
        'Héctor',
        'Hector',
      ]),
    );
  });
  it('does not turn initials into a state or a common abbreviation', () => {
    const f = forms({
      people: ['Mary Edwards', 'Carl Paul Adams'],
      companies: [],
    });
    expect(f).not.toContain('ME');
    expect(f).not.toContain('CPA');
  });
  it('covers a company short name, leading words and acronym', () => {
    expect(
      forms({
        people: [],
        companies: [
          'Lone Star Teachers Credit Union',
          'Blue Heron Veterinary Clinic, Inc.',
        ],
      }),
    ).toEqual(
      expect.arrayContaining([
        'LSTCU',
        'Lone Star Teachers',
        'Blue Heron Veterinary Clinic',
        'Blue Heron',
        'BLUE HERON VETERINARY CLINIC',
      ]),
    );
  });
});

describe('putting it together', () => {
  it('links every form of a person to one placeholder', () => {
    const text =
      'Present: DKL, R. Tanaka. Dana K. Lindqvist met the client; Lindqvist will follow up. LINDQVIST, DANA signed.';
    const out = cleaned(text, {people: ['Dana K. Lindqvist'], companies: []});
    expect(out).not.toMatch(/DKL|Lindqvist|LINDQVIST|Tanaka/);
    expect(new Set(out.match(/\[PERSON_\d+\]/g))).toEqual(
      new Set(['[PERSON_1]', '[PERSON_2]']),
    );
  });
  it('treats a new first name with a known surname as a family member', () => {
    expect(
      cleaned('Ngozi Okafor called. Her brother wants Emeka Okafor removed.', {
        people: ['Ngozi Okafor'],
        companies: [],
      }),
    ).not.toContain('Emeka');
  });
  it('keeps a name suffix and a company ending with the name', () => {
    expect(
      cleaned(
        'Signed by Héctor Reyes Jr. for Blue Heron Lending, FLCA and The Okafor Family Trust.',
        {
          people: ['Héctor Reyes'],
          companies: ['Blue Heron Lending', 'Okafor Family Trust'],
        },
      ),
    ).toBe('Signed by [PERSON_1] for [COMPANY_1] and [COMPANY_2].');
  });
  it('uses short names the document defines, but only for the party they follow', () => {
    const text =
      'Brightwater Biologics, Inc. ("Brightwater") signed this Master Lease (the "Lease") with Dr. Wen. Brightwater then left; the Lease ended.';
    expect(definedTerms(text).map(t => t.term)).toEqual([
      'Brightwater',
      'Lease',
    ]);
    const out = cleaned(text);
    expect(out).not.toContain('Brightwater');
    expect(out).toContain('the Lease ended');
  });
  it('completes a full name from a first name or a surname already known', () => {
    expect(
      cleaned('Imani Okoro to send the form.\nBENEFICIARY: Trần Minh Khôi', {
        people: ['Imani', 'Minh Khôi'],
        companies: [],
      }),
    ).toBe('[PERSON_1] to send the form.\nBENEFICIARY: [PERSON_2]');
    // A street named without a number is a place, not that person's surname.
    expect(
      cleaned('Ingrid Street is closed. Ingrid said so.', {
        people: ['Ingrid'],
        companies: [],
      }),
    ).toBe('[PLACE_1] is closed. [PERSON_1] said so.');
  });
  it('treats "W. Pike" and "Wendell Pike" as one person, so "Pike" alone is linked', () => {
    const out = cleaned(
      'Check to Wendell Pike. 20425 W. Pike $850. Pike is the brother-in-law.',
      {people: ['Wendell Pike', 'W. Pike'], companies: []},
    );
    expect(out).not.toContain('Pike');
    expect(new Set(out.match(/\[PERSON_\d+\]/g))).toEqual(
      new Set(['[PERSON_1]']),
    );
  });
  it('finds a known given name typed in lower case, but not ordinary words', () => {
    expect(
      cleaned(
        'Callum Reid has the kids; callum works 6 days. Mark Reid said to mark the file.',
        {people: ['Callum Reid', 'Mark Reid'], companies: []},
      ),
    ).toBe(
      '[PERSON_1] has the kids; [PERSON_1] works 6 days. [PERSON_2] said to mark the file.',
    );
  });
  it('keeps a credential with the name, so "MD" is not read as Maryland', () => {
    expect(
      cleaned('Signed, Hannah Goldfarb, MD on the chart.', {
        people: ['Hannah Goldfarb'],
        companies: [],
      }),
    ).toBe('Signed, [PERSON_1] on the chart.');
  });
  it('still catches the state code when the city was taken by another check', () => {
    const text =
      'Offices at 500 Main Street, Dallas, TX 75201 and in Wenatchee, WA.';
    const out = cleaned(text, {people: [], companies: ['Dallas']});
    expect(out).not.toMatch(/\bTX\b|\bWA\b|Dallas|75201/);
  });
  it('reads "Jordan Lee, MD" as a person, not a place in Maryland', () => {
    const d = buildDetections(
      'Referred by Dr. Jordan Lee, MD in Dallas, TX.',
      ALL,
      none,
    );
    expect(d.find(x => x.text.includes('Jordan'))?.kind).toBe('person');
    expect(d.find(x => x.text.includes('Dallas'))?.kind).toBe('places');
  });
});

describe('spreadsheet numbers shown the way Excel shows them', () => {
  const cases: Array<[number, string, string]> = [
    [1250.5, '"C$"#,##0.00', 'C$1,250.50'],
    [-27315.88, '#,##0.00_);\\(#,##0.00\\)', '(27,315.88)'],
    [18450, '#,##0.00_);\\(#,##0.00\\)', '18,450.00'],
    [1250.5, '$#,##0.00_);($#,##0.00)', '$1,250.50'],
    [-1250.5, '$#,##0.00_);($#,##0.00)', '($1,250.50)'],
    [6000, '[$€-407]#,##0', '€6,000'],
    [0.125, '0.0%', '12.5%'],
    [1234.5, 'General', '1234.5'],
    [-500, '#,##0', '-500'],
    [22354, 'yyyy-mm-dd', '1961-03-14'],
    [22354, 'mm/dd/yyyy', '03/14/1961'],
    [22354, 'm/d/yy', '3/14/61'],
    [22354, 'd-mmm-yy', '14-Mar-61'],
    [22354, 'mmmm d, yyyy', 'March 14, 1961'],
    [22354.5, 'm/d/yyyy h:mm', '3/14/1961 12:00'],
    [46096.6875, 'h:mm AM/PM', '4:30 PM'],
  ];
  for (const [value, code, shown] of cases) {
    it(`${value} as ${code}`, () =>
      expect(displayNumber(value, code)).toBe(shown));
  }
});

// Rules added while taking each sub-category of the evaluation to 100%. All
// names are fictional.
describe('names completed from what is on the page', () => {
  it('grows an organization over the words that finish its name', () => {
    expect(
      cleaned('Insurance: Prairie State Blue Shield PPO, member', {
        people: [],
        companies: ['Prairie State Blue Shield'],
      }),
    ).toBe('Insurance: [COMPANY_1], member');
    expect(
      cleaned('paid Meridian Coastal Title & Escrow Co. today', {
        people: [],
        companies: ['Meridian Coastal Title'],
      }),
    ).toBe('paid [COMPANY_1] today');
    expect(
      cleaned('Aide at Flint Hills Unified School District 383 since then', {
        people: [],
        companies: ['Flint Hills Unified School District'],
      }),
    ).toBe('Aide at [COMPANY_1] since then');
  });
  it('turns a "person" followed by an organization word into an organization', () => {
    expect(
      cleaned('She stays at Cedar Glen Memory Care now.', {
        people: ['Cedar Glen'],
        companies: [],
      }),
    ).toBe('She stays at [COMPANY_1] now.');
  });
  it('keeps "Estate of" with the name, as a party of its own', () => {
    expect(
      cleaned(
        'Retitle to the Estate of Wade R. Abernathy. Wade R. Abernathy died.',
        {people: ['Wade R. Abernathy'], companies: []},
      ),
    ).toBe('Retitle to the [COMPANY_1]. [PERSON_1] died.');
  });
  it('drops a role word in front of an organization, and finds campaign committees and universities', () => {
    expect(
      cleaned('1. Defendant Brightwater Freight Systems, Inc. is a carrier.'),
    ).toBe('1. Defendant [COMPANY_1] is a carrier.');
    expect(
      cleaned('a check to Friends of Varga for County Commissioner, coded'),
    ).toBe('a check to [COMPANY_1], coded');
    expect(
      cleaned('M.Sc. Computer Science, University of Regina, conferred'),
    ).toContain('[COMPANY_1], conferred');
  });
  it('reads a surname from a case name and from a home called by the family name', () => {
    expect(cleaned('Case: Kowalczyk v. Brightpath Home Care, LLC')).toContain(
      '[PERSON_1] v.',
    );
    expect(
      cleaned('lumber for Hartung residence; crew lunch, Hartung topping-out'),
    ).not.toContain('Hartung');
    expect(cleaned('United States v. Brightpath Home Care, LLC')).toContain(
      'United States v.',
    );
  });
  it('ignores a name the model misspelled when the right spelling is on the page', () => {
    const out = cleaned(
      'Marisela Lopez starts Monday.\n- Lopez: new Form W-4.',
      {people: ['Marisela Lopez', 'Marisola Lopez'], companies: []},
    );
    expect(out).toBe('[PERSON_1] starts Monday.\n- [PERSON_1]: new Form W-4.');
  });
  it('does not take part of a city for a person', () => {
    const out = cleaned(
      'Office at 2150 South 1300 East, Suite 500, Salt Lake City, Utah 84106. Louis lives in St. Louis, Missouri.',
      {people: ['Salt Lake', 'Louis'], companies: []},
    );
    expect(out).not.toContain('Salt Lake');
    expect(out).not.toContain('St.');
    expect(out).toContain('[PERSON_1] lives in');
  });
  it('finds salutations, sign-offs and nicknames', () => {
    expect(cleaned('Steph,\nplease call me.\nthanks\nlola\n')).toBe(
      '[PERSON_1],\nplease call me.\nthanks\n[PERSON_2]\n',
    );
    expect(cleaned('Everyone calls him Buddy at work.')).toBe(
      'Everyone calls him [PERSON_1] at work.',
    );
  });
});

describe('names: later rules from the sub-category work', () => {
  it('finds initials where only initials would stand, and lower-case typist initials', () => {
    const out = cleaned(
      'Marguerite Oyelaran took the call. shred. (MO)\nSummarized by: jdl, 3/2/26\nReviewed: HJK 02/24/2026',
      {people: ['Marguerite Oyelaran'], companies: []},
    );
    expect(out).toContain('shred. ([PERSON_1])');
    expect(out).not.toMatch(/jdl|HJK/);
  });
  it('reads "Last, First" when only the first name is known', () => {
    expect(
      cleaned('TAXPAYER   Petrosyan, Nikolai ("Niko")', {
        people: ['Nikolai'],
        companies: [],
      }),
    ).not.toContain('Petrosyan');
  });
  it('does not take a role word or a street for a person', () => {
    const out = cleaned(
      'an order compelling Defendants Stavros Precision Hydraulics, Inc. and Hunter J. Stavros. Defendants deny it. The acres on Tieton Drive; we drive there.',
      {people: ['Hunter J. Stavros', 'Stavros'], companies: []},
    );
    expect(out).toContain('compelling Defendants [COMPANY_1]');
    expect(out).toContain('Defendants deny it');
    expect(out).toContain('we drive there');
    expect(out).not.toContain('Tieton');
  });
  it('finds organizations written in capitals, but not headings', () => {
    const companies = (t: string) => discoverNames(t).companies;
    expect(
      companies('SAGEBRUSH FAMILY MEDICINE              OFFICE VISIT NOTE'),
    ).toEqual(['SAGEBRUSH FAMILY MEDICINE']);
    expect(
      companies(
        'UNITED STATES DISTRICT COURT\nDECLARATION OF TRUST\nPATIENT FINANCIAL SERVICES',
      ),
    ).toEqual([]);
  });
  it("finds user names made from a known person's name", () => {
    const out = cleaned(
      'using the administrator account hstavros_adm; Gwendolyn Marsh (`gmarsh`) got it.',
      {people: ['Hunter J. Stavros', 'Gwendolyn Marsh'], companies: []},
    );
    expect(out).not.toMatch(/hstavros_adm|gmarsh/);
  });
});

describe('names: precision and the third test set', () => {
  const companies = (t: string) => discoverNames(t).companies;
  const people = (t: string) => discoverNames(t).people;
  it('does not take ordinary words at the front of a name, headings or public bodies for an organization', () => {
    expect(
      companies(
        'He signed it. Signed Fairweather Orchards & Cider Mill, Inc. today.',
      ),
    ).not.toContain('Signed Fairweather Orchards');
    expect(
      companies('We need the letters. Letters of Authority issued 3/12/2026.'),
    ).toEqual([]);
    expect(
      companies('Court:     U.S. District Court, Eastern District of Virginia'),
    ).toEqual([]);
    expect(
      cleaned('Conflicts check.\nPNC: Yusuf Haddad. Paid by trust company.', {
        people: ['Yusuf Haddad'],
        companies: ['PNC', 'trust company', 'LLC'],
      }),
    ).toBe('Conflicts check.\nPNC: [PERSON_1]. Paid by trust company.');
  });
  it('does not take job titles, headings or vehicles for a person', () => {
    expect(
      people(
        'She became a Managing Member and read the Privacy Practices notice about her Toyota Corolla.',
      ),
    ).toEqual([]);
    expect(
      people('We obtained the June reconciliation; there is a Miranda issue.'),
    ).toEqual([]);
  });
  it('finds organizations with endings in lower case, in capitals with a comma, and of three words', () => {
    expect(
      companies('Conseiller, Textiles Beauharnois ltée | 450 555-0136'),
    ).toContain('Textiles Beauharnois ltée');
    expect(
      companies('vs.\nGREENMANTLE GROCERS, INC., an Arizona corporation'),
    ).toContain('GREENMANTLE GROCERS, INC');
    expect(
      companies('Dr. Vasbinder of Vasbinder Facial Plastics saw him.'),
    ).toContain('Vasbinder Facial Plastics');
    expect(
      cleaned('for the defendant, Stonecutter Assurance Company of Canada.', {
        people: [],
        companies: ['Stonecutter Assurance Company'],
      }),
    ).toBe('for the defendant, [COMPANY_1].');
  });
  it('finds people in notes typed in lower case, and by title, maiden name and card name', () => {
    expect(
      people(
        'client: tyrese m. goodwine, goes by reese. lives w/ ms. hyacinth',
      ),
    ).toEqual(
      expect.arrayContaining(['tyrese m. goodwine', 'reese', 'hyacinth']),
    );
    expect(
      people(
        'My maiden name was Stachura. Police: Ofc. Pruneau. M. et Mme ENTWISTLE',
      ),
    ).toEqual(expect.arrayContaining(['Stachura', 'Pruneau', 'ENTWISTLE']));
    expect(people('Name on card: LUCINDA M APONTE-RHEE')).toContain(
      'LUCINDA M APONTE-RHEE',
    );
  });
  it('takes the town and state written after a street address', () => {
    const out = cleaned(
      'Seen at 1127 Vigo Street, Terre Haute IN. Tow yard: 1450 West 2100 South, Salt Lake City.',
    );
    expect(out).toBe(
      'Seen at [ADDRESS_1], [PLACE_1] [STATE_1]. Tow yard: [ADDRESS_2], [PLACE_2].',
    );
  });
});

describe('cue rules for short pastes', () => {
  const people = (text: string) => discoverNames(text).people;
  it.each([
    ['Ksenia Abramovich (CEO)\tCommon\t3,600,000', 'Ksenia Abramovich'],
    ['Present:  Shabnam Akhtar, Operations Manager (chair)', 'Shabnam Akhtar'],
    ['Merci,\nMarie-Ève Dandurand\nOpératrice', 'Marie-Ève Dandurand'],
    ["For our records: Anjali's passport no. Z4418830.", 'Anjali'],
    ['Approved by Priyanka. We will reimburse.', 'Priyanka'],
    ['Please ask Shirin which hospital.', 'Shirin'],
    ['Hamza also owes 2 500,00 on a personal loan.', 'Hamza'],
    ['Grandchildren: Wren, born 2014.', 'Wren'],
    ['CHILD:   Dariel Zelaya, 9 años', 'Dariel Zelaya'],
    ['Contact\nJürgen: 0171 5550 188', 'Jürgen'],
    ["Harper's share can go to her outright.", 'Harper'],
    ['Bonjour Marie-Ève,\n\nMerci.', 'Marie-Ève'],
    ['Dear Dafydd and Anjali,\n\nThank you.', 'Dafydd'],
    ['Íñigo uses the old account.', 'Íñigo'],
  ])('finds the person in %j', (text, name) =>
    expect(people(text)).toContain(name),
  );
  it.each([
    "Today's agenda is short.",
    "Let's review the draft.",
    'Fee: $250 due on receipt.',
    'Debts: none listed.',
    'Out-of-Pocket Co-Payments\t$100.00',
    'Revenue takes time to recognise.',
    'The agenda is attached.',
  ])('finds no person in %j', text => expect(people(text)).toEqual([]));
});

describe('initials, capitals and "Surname, First"', () => {
  const people = (text: string) => discoverNames(text).people;
  it.each([
    ['Payment plan agreed. Ring him Fri 14th.   BK', 'BK'],
    ['Please keep that between us.\n\nR.', 'R.'],
    ['GM said the ban was 12 months.', 'GM'],
    ['Fee earner: Honor Wilmot (HW)', 'HW'],
    [
      'Claimant: TSEHAY WOLDEMICHAEL          Employer: QUAYSIDE VALET LLC',
      'TSEHAY WOLDEMICHAEL',
    ],
    ['Patient:\tReyes, Marisol\nDOB: 07/22/1984', 'Marisol Reyes'],
    ['Okafor, Daniel J.\nnext line', 'Daniel Okafor'],
  ])('finds the person in %j', (text, name) =>
    expect(people(text)).toContain(name),
  );
  it.each([
    'The IRS said no. HR confirmed.',
    'Seattle, Washington\nRevenue, Expenses',
    'NOTICE: ANNUAL REVIEW',
    'Total: USD 4,000 in CA.',
  ])('finds no person in %j', text => expect(people(text)).toEqual([]));
});

describe('larger given-name list (SSA)', () => {
  const people = (text: string) => discoverNames(text).people;
  it.each([
    ['Online banking is still under the login of Ksenia only.', 'Ksenia'],
    ['Please confirm the dates with Anjali before Friday.', 'Anjali'],
    ['The deposit was paid by Corwin last week.', 'Corwin'],
  ])('finds a less common first name in mid-sentence: %j', (text, name) =>
    expect(people(text)).toContain(name),
  );
  it.each([
    'Please read the Manual before the Trip.',
    'The Case was heard by the Court.',
    'Thank you, Your Honor, the matter is closed.',
    'Shipments go through Washington and Tacoma.',
  ])('does not treat capitalized ordinary words or places as names: %j', text =>
    expect(people(text)).toEqual([]),
  );
});
