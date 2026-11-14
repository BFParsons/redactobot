/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Names, handled in ordinary code.
 *
 * The on-device model returns full names. Everything here is deterministic:
 *   discoverNames()  finds names the model may have missed, from reliable cues in the text
 *                    (a title such as "Dr." or "Judge", a company ending such as "LLC" or
 *                    "Credit Union", "SURNAME, First" in forms, "known as …").
 *   nameCandidates() expands each name into the other ways it gets written (initials,
 *                    "Last, First", ALL CAPS, without the middle name, without accents,
 *                    a company's short name or acronym), all linked to one entity so they
 *                    share a placeholder.
 * Both lean toward catching: a wrongly marked word is replaced and later
 * restored, and the user can untick it.
 */

import {COMMON_WORDS, GEOGRAPHY, isLargePlace} from './common-words';
import {AMBIGUOUS_NAMES, GIVEN_NAMES} from './given-names';
import {SSA_GIVEN_NAMES} from './given-names-ssa';
import {PLACE_NAMES} from '../../taxonomy/places-data.js';
import {isRegion} from '../../taxonomy/detectors.js';

/** People and organizations named in a text. */
export interface Names {
  people: string[];
  companies: string[];
  /**
   * A written form that belongs to a person but cannot be derived from the
   * name.
   */
  links?: Array<{text: string; person: string}>;
}
/**
 * How a candidate arose: a name as given ('model'), or another written form
 * derived from one ('short-form').
 */
export type NameSource = 'model' | 'short-form';
/** One written form of a name, to be searched for in the text. */
export interface Candidate {
  text: string;
  kind: 'person' | 'company';
  /** Candidates with the same entity share one placeholder. */
  entity: string;
  /** The full name that is restored for this entity. */
  canonical: string;
  source: NameSource;
}

/** Returns `s` trimmed, with each run of whitespace made a single space. */
export const collapse = (s: string) => s.replace(/\s+/g, ' ').trim();
/** Returns the collapsed, lower-case form of `s`, for comparing names. */
export const key = (s: string) => collapse(s).toLowerCase();
const unaccent = (s: string) => s.normalize('NFD').replace(/\p{M}/gu, '');
const upper = (s: string) => s.toLocaleUpperCase('en-US');

const TITLE =
  'Mr|Mrs|Ms|Miss|Mx|Dr|Prof|Professor|Hon|Judge|Justice|Magistrate|Reverend|Father|Sister|Senator|Atty|Attorney|Officer|Ofc|Det|Detective|Sgt|Cpl|Tpr|Trooper|Deputy|Insp|Constable|Capt|Lt|Sir|Dame|Doña|Don|Señor|Señora|Sra|Dra|Dre|Lic|Mme|Mlle|Maître|Herr|Frau|Mevr|Dhr|RN|MR|MRS|MS|DR';
const HONORIFIC = new RegExp(`^(?:${TITLE})\\.?$`, 'i');
const SUFFIX_WORD =
  /^(?:Jr|Sr|II|III|IV|Esq|MD|M\.D|PhD|Ph\.D|CPA|JD|J\.D|RN|DDS|DO)\.?,?$/i;
const PARTICLE =
  /^(?:de|del|della|di|da|dos|das|la|las|le|los|van|von|der|den|ter|ten|bin|ibn|al|el|ní|ó|mac|st\.?)$/i;
// Any capital, so names like "Íñigo", "Élodie" and "Óscar" count.
const NAME_WORD = "(?:Mc|Mac|O['’]|D['’])?\\p{Lu}[\\p{Ll}][\\p{L}'’-]*";
const ROLE_AFTER =
  'Partner|Associate|Paralegal|EA|RPR|CPA|CPAs|Esq|MD|M\\.D|RN|NP|PA-C|DO|PhD|Ph\\.D|JD|Director|Manager|President|CEO|CFO|COO|Controller|Treasurer|Secretary|Owner|Principal|Counsel|Attorney|Notary|Trustee|Executor|Administrator|Bookkeeper|Supervisor|Foreman|Agent|Adjuster|Mediator|Arbitrator|Clerk';
const ROLE_BEFORE =
  'consultant|applicant|resident|student|employee|counsellor|counselor|advisor|adviser|broker|realtor|teacher|coach|pastor|dentist|pharmacist|interpreter|translator|caseworker|paralegal|associate|attorney|counsel|accountant|bookkeeper|nurse|physician|surgeon|therapist|adjuster|supervisor|foreman|dispatcher|clerk|assistant|coordinator|technician|driver|tenant|landlord|patient|claimant|witness|deponent|plaintiff|defendant|petitioner|respondent|wife|husband|son|daughter|brother|sister|mother|father|spouse|niece|nephew|aunt|uncle|cousin|grandson|granddaughter|grandmother|grandfather|neighbor|neighbour|friend|colleague|coworker|co-worker|roommate|fiancé|fiancée|girlfriend|boyfriend|stepson|stepdaughter|caregiver|guardian|beneficiary|executor|trustee|controller|preparer|mediator|officer|deputy|detective|inspector';
const FIELD_LABEL =
  'Approver|Cardholder|Card holder|Account holder|Requester|Requestor|Employee name|Applicant|Consultant|Prepared by|Reviewed by|Approved by|Reported by|Summarized by|Drafted by|Signed by|Submitted by|Taken by|Entered by|Reporter|Attn|Attention|Contact|Preparer|Supervisor|Manager|Spouse|Patient|Client|Employee|Witness|Claimant|Insured|Policyholder|Subscriber|Guarantor|Borrower|Co-borrower|Taxpayer|Decedent|Beneficiary|Physician|Provider|Referring provider|Attending|Emergency contact|Next of kin|Name|Fee earner|Author|From|To|Cc|Bcc';
const CAPTION_ROLE =
  'Petitioners?|Respondents?|Plaintiffs?|Defendants?|Appellants?|Appellees?|Debtors?|Claimants?|Deceased|Decedent|Trustee|Executor|Intervenors?';
const NAME_TOKEN = `(?:[A-Z]\\.|${NAME_WORD}|de|del|della|di|da|la|las|los|van|von|der|den|bin|al|ní)`;

const COMPANY_SUFFIX =
  /[,\s]+(?:ltd|limited|inc|incorporated|llc|l\.l\.c|llp|l\.l\.p|lp|l\.p|corp|corporation|co|company|plc|gmbh|pc|p\.c|pllc|p\.l\.l\.c|p\.a|n\.a|s\.a|ag|bv|b\.v|teoranta)\.?$/i;
// Words that mark the end of an organization's name.
const ORG_END =
  'Inc|Incorporated|LLC|L\\.L\\.C|LLP|L\\.L\\.P|LP|L\\.P|PLLC|P\\.L\\.L\\.C|P\\.C|PC|P\\.A|Ltd|Limited|Corp|Corporation|Co|Company|PLC|GmbH|N\\.A|Bank|Credit Union|Trust|Foundation|University|College|Hospital|Clinic|Associates|Partners|Partnership|Group|Holdings|Elementary|Academy|School|Church|Institute|Center|Centre|Society|Association|Agency|Authority|Fund|Estate|Pharmacy|Insurance|Solicitors|Chartered|Industries|Enterprises|Services|Solutions|Systems|Logistics|Builders|Construction|Realty|Properties|Capital|Ventures|Advisors|Consulting|Laboratories|Labs|Medical|Dental|Pediatrics|Orthopedics|Cardiology|Dermatology|Veterinary|Law Firm|Law Office|Law Offices|Brokerage|Mortgage|Financial|Securities|Union|Local \\d+|District|Department|Commission|Council|Board|Ministry|Bureau|Cooperative|Co-op|Homes|Cabins|Joinery|Bookkeeping|Supply|Supplies|Motors|Farms|Orchards|Brewing|Bakery|Studio|Studios|Press|Media|Airlines|Hotel|Hotels|Inn|Café|Cafe|Restaurant|Market|Markets|Parish|Diocese|Ministries|Temple|Synagogue|Mosque|Urgent Care|Health|Healthcare|Health Plan|Health System|Hospice|Lending|CPAs|Attorneys|Architects|Engineers|Contractors|Plumbing|Electric|Roofing|Landscaping|Trucking|Transport|Freight|Shipping|Outfitters|Marine|Aviation|Rentals|Linen Service|Auto Glass|Auto Body|Tribe|Nation|Band|Court Reporting|Title|Escrow|Brewery|Winery|Distillery|Nursery|Daycare|Preschool|Library|Museum|Theatre|Theater|Club|League|Lodge|Post|Chapter|Committee|Coalition|Alliance|Network|Collective|Works|Outlet|Depot|Warehouse|Mill|Mills|Ranch|Dairy|Fisheries|Cannery|Mining|Energy|Power|Utilities|Water|Telecom|Wireless|Software|Technologies|Analytics|Biologics|Pharmaceuticals|Therapeutics|Diagnostics|Imaging|Radiology|Oncology|Urology|Neurology|Psychiatry|Counseling|Counselling|Physiotherapy|Chiropractic|Optometry|Eye Care|Family Practice|Internal Medicine|Home Care|Senior Living|Assisted Living|Nursing Home|Funeral Home|Cemetery';
const ORG_END_WRAP = ORG_END.replace(/ /g, '\\s+');
const CONNECT = '(?:of(?:[^\\S\\n]+the)?|de|du|&)';
// One word of an organization's name. A full stop is allowed only in an
// abbreviation.
const ORG_WORD =
  "(?:St\\.|Mt\\.|Ft\\.|[A-Z]\\.(?:[A-Z]\\.)*|[A-Z][\\p{L}0-9'’-]*)";
/**
 * Words that end an organization's name when they follow a name already known:
 * "Blue Shield PPO", "Band Boosters".
 */
const ORG_TAIL_WORDS = `${ORG_END}|Boosters|Plan|PPO|HMO|Care|Montessori|Meals|Club|Hotel|Inn|Daycare|Preschool|Ministries|League|Lodge|Escrow|Title|Rescue|Shelter|Benefits|Office|Living|Hall|Staffing|Catering|Market|Shop|Store|Studio|Salon|Garage|Diner|Grill|Bakery|Café|Cafe|Restaurant|Outfitters|Nursery|Kennel|Stables|Gym|Fitness|Theater|Theatre|Museum|Library|Temple|Mosque|Synagogue|Chapel|Cathedral|Mission|Pantry|Network|Alliance|Coalition|Committee|Residence|Manor|Village|Villa|Pavilion|Commons|Estates|Apartments|Towers|Mutual|Assurance|Underwriters|Exchange|Hire|Bakehouse|Roasters|Chambers|Lawyers|Accountants|Law|Plastics|Nursing|Pharmasave|Super|Banco|Sparkasse|Pawn|Loan|IT|Comptable|Photonics`;
/** Matches a string that is exactly one of ORG_TAIL_WORDS. */
export const ORG_TAIL = new RegExp(`^(?:${ORG_TAIL_WORDS})$`);
// Endings of an organization's name written in capitals.
const CAPS_END =
  ORG_END.split('|')
    .filter(w => !w.includes('\\d'))
    .join('|')
    .toUpperCase() +
  '|MEDICINE|CARE|HEALTH|RECOVERY|ESTATE|EXCHANGE|MUTUAL|ASSURANCE|UNDERWRITERS|HOTEL|PHARMACY|BBQ|GRILL|AIR|AIRLINES';
// Words in capitals that head a section or a form and say nothing about whose
// it is.
const GENERIC_CAPS = new Set(
  (
    'THE A AN OF AND FOR IN ON TO REVOCABLE IRREVOCABLE LIVING DECLARATION FAMILY GENERAL NATIONAL STATE FEDERAL COUNTY CITY PUBLIC PRIVATE ' +
    'CONFIDENTIAL PROTECTED PATIENT CLIENT ANNUAL MONTHLY WEEKLY QUARTERLY TOTAL SUMMARY STATEMENT NOTICE REPORT SCHEDULE EXHIBIT ATTACHMENT APPENDIX SECTION ARTICLE PART ' +
    'UNITED STATES SUPERIOR DISTRICT CIRCUIT SUPREME MUNICIPAL PROBATE BANKRUPTCY INTERNAL REVENUE SOCIAL SECURITY PRIMARY URGENT EMERGENCY INTENSIVE HOME LONG-TERM ' +
    'MENTAL BEHAVIORAL PUBLIC OCCUPATIONAL MANAGED PREVENTIVE DENTAL MEDICAL LEGAL FINANCIAL PERSONAL REAL OPERATING SAVINGS CHECKING RETIREMENT PENSION PROFIT SHARING ' +
    'BOARD MEETING NOTES MEMO MEMORANDUM DRAFT FINAL PRIVILEGED ATTORNEY WORK PRODUCT TAX RETURN INCOME EXPENSE BALANCE SHEET ACCOUNT ACCOUNTS PAYABLE RECEIVABLE ' +
    'NEW OLD CURRENT PRIOR NEXT LAST FIRST SECOND THIRD OUR YOUR MY HIS HER THEIR THIS THAT ALL ANY NO NOT SEE PER RE'
  ).split(' '),
);
const ORG_END_ONLY = new RegExp(`^(?:${ORG_END})$`);
// Company endings that are abbreviations, so a full stop after them belongs to
// the name.
const ABBREVIATED_END =
  /(?:Inc|Co|Corp|Ltd|L\.L\.C|L\.L\.P|L\.P|P\.L\.L\.C|P\.C|P\.A|N\.A|S\.A)\.$/;
// First words too common to stand in for a company on their own.
const GENERIC_FIRST = new Set([
  'the',
  'national',
  'first',
  'american',
  'united',
  'general',
  'new',
  'north',
  'south',
  'east',
  'west',
  'royal',
  'pacific',
  'atlantic',
  'global',
  'international',
  'central',
  'city',
  'state',
  'federal',
  'bank',
  'law',
  'office',
  'department',
  'university',
  'st',
  'saint',
  'county',
  'great',
  'grand',
  'upper',
  'lower',
  'old',
  'big',
  'little',
  'mount',
  'lake',
  'fort',
  'port',
  'san',
  'santa',
  'blue',
  'red',
  'green',
  'black',
  'white',
]);
// Last words that mean the "person" was really a thing; never used alone as a
// surname.
const GENERIC_LAST = new Set([
  'defendants',
  'defendant',
  'plaintiff',
  'plaintiffs',
  'vendor',
  'customer',
  'representative',
  'terms',
  'doctor',
  'cash',
  'rate',
  'court',
  'trust',
  'estate',
  'summary',
  'bank',
  'company',
  'firm',
  'group',
  'office',
  'department',
  'county',
  'city',
  'state',
  'agreement',
  'lease',
  'account',
  'fund',
  'plan',
  'board',
  'committee',
  'services',
  'center',
  'centre',
  'hospital',
  'clinic',
  'school',
  'church',
  'family',
  'date',
  'number',
  'street',
  'avenue',
  'road',
]);
// Short words that can follow "typed" or "taken by" without being initials.
const SMALL_WORDS = new Set([
  'the',
  'me',
  'him',
  'her',
  'us',
  'you',
  'our',
  'my',
  'his',
  'and',
  'for',
  'in',
  'on',
  'at',
  'up',
  'out',
  'to',
  'of',
  'an',
  'it',
  'mom',
  'dad',
  'all',
  'one',
  'two',
  'by',
  'as',
  'or',
  'so',
  'if',
  'is',
  'was',
  'via',
  'per',
  'off',
  'not',
  'now',
  'she',
  'he',
  'we',
  'cpa',
  'hr',
  'it',
]);
// A party's role in front of its name: "Defendants Stavros Precision
// Hydraulics, Inc."
const LEAD_ROLE =
  /^(?:Defendants?|Plaintiffs?|Petitioners?|Respondents?|Appellants?|Appellees?|Claimants?|Debtors?|Creditors?|Movants?|Intervenors?|DEFENDANTS?|PLAINTIFFS?|PETITIONERS?|RESPONDENTS?)$/;
// Words before "residence" that are not a family's name.
const NOT_A_HOME = new Set([
  'primary',
  'principal',
  'private',
  'personal',
  'permanent',
  'main',
  'second',
  'secondary',
  'family',
  'legal',
  'former',
  'current',
  'new',
  'old',
  'official',
  'marital',
  'joint',
  'their',
  'his',
  'her',
  'my',
  'our',
  'your',
  'the',
  'a',
  'of',
  'in',
  'same',
  'usual',
  'habitual',
  'last',
  'first',
  'only',
  'single',
  'vacation',
  'summer',
  'winter',
  'rental',
  'shared',
  'client',
  'debtor',
  'decedent',
  'tax',
  'state',
  'us',
  'canadian',
]);
// Parties in a case name that are not a person's surname.
const CASE_PARTY = new Set([
  'people',
  'state',
  'commonwealth',
  'united',
  'states',
  'city',
  'county',
  'town',
  'village',
  'usa',
  'plaintiff',
  'plaintiffs',
  'petitioner',
  'respondent',
  'defendant',
  'crown',
  'regina',
  'rex',
  'government',
  'estate',
  'board',
  'department',
  'commissioner',
  'secretary',
  'trustee',
  'trustees',
  'bank',
  'doe',
  'roe',
]);
// Kinds of body that people refer to as "the Authority", "the Bank", "the
// Trust".
const INSTITUTION = new Set([
  'authority',
  'bank',
  'trust',
  'foundation',
  'clinic',
  'hospital',
  'university',
  'college',
  'board',
  'district',
  'department',
  'commission',
  'agency',
  'fund',
  'union',
  'association',
  'society',
  'institute',
  'center',
  'centre',
  'council',
  'ministry',
  'bureau',
  'cooperative',
  'academy',
  'school',
  'church',
  'parish',
  'pharmacy',
  'tribe',
  'nation',
  'estate',
  'partnership',
  'league',
]);
// Capitalized words that are not the start of a name after a title, or of an
// organization.
const NOT_A_NAME = new Set([
  'let',
  'who',
  'what',
  'where',
  'when',
  'why',
  'how',
  'that',
  'there',
  'here',
  'this',
  'everyone',
  'nobody',
  'somebody',
  'someone',
  'anyone',
  'bonjour',
  'bonsoir',
  'salut',
  'hola',
  'hallo',
  'liebe',
  'lieber',
  'beste',
  'ciao',
  'olá',
  'chère',
  'cher',
  'querido',
  'querida',
  'estimado',
  'estimada',
  'caro',
  'cara',
  'dear',
  'hi',
  'hello',
  'hey',
  'today',
  'tomorrow',
  'yesterday',
  'tonight',
  'she',
  'he',
  'they',
  'we',
  'you',
  'it',
  'i',
  'said',
  'mom',
  'dad',
  'mum',
  'fuel',
  'lake',
  'one',
  'two',
  'three',
  'four',
  'five',
  'six',
  'seven',
  'eight',
  'nine',
  'ten',
  'commercial',
  'collision',
  'medical',
  'personal',
  'total',
  'court',
  'local',
  'workers',
  'summary',
  'file',
  'approve',
  'item',
  'detail',
  'civ',
  'crim',
  'app',
  'evid',
  'bankr',
  'stat',
  'supp',
  'cir',
  'ct',
  'proc',
  'code',
  'number',
  'box',
  'respondent',
  'petitioner',
  'plaintiff',
  'defendant',
  'appellant',
  'appellee',
  'trustee',
  'executor',
  'debtor',
  'inc',
  'llc',
  'llp',
  'ltd',
  'general',
  'advocate',
  'client',
  'fees',
  'work',
  'the',
  'and',
  'or',
  'at',
  'in',
  'on',
  'to',
  'for',
  'of',
  'this',
  'that',
  'our',
  'your',
  'their',
  'his',
  'her',
  'its',
  'a',
  'an',
  'no',
  'not',
  'see',
  'per',
  'please',
  'dear',
  're',
  'from',
  'date',
  'subject',
  'note',
  'notes',
  'total',
  'amount',
  'balance',
  'page',
  'pro',
]);
const STREET_WORDS =
  'Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Place|Pl|Terrace|Highway|Hwy|Parkway|Trail|Ridge|Circle|Square|County|Parish|Township|Borough|River|Lake|Valley|Mountain|Island|Beach|Park|Bridge|Building|Tower|Plaza|Mall|Airport|Station|Division|Branch|Region|Province|Territory';
// Capitalized words that are ordinary vocabulary in business, legal and medical
// writing.
const ORDINARY = new Set(
  (
    'january february march april may june july august september october november december ' +
    'monday tuesday wednesday thursday friday saturday sunday spring summer fall autumn winter ' +
    'new old north south east west northern southern eastern western central upper lower greater ' +
    'united states state federal national international american canadian british european english french spanish german chinese mexican ' +
    'social security internal revenue service medicare medicaid district superior supreme circuit appellate appeals bankruptcy family probate juvenile municipal ' +
    'court judge county city town village commonwealth republic kingdom government department ministry agency bureau office division board commission committee council ' +
    'law act code rule rules order motion notice section article chapter exhibit schedule form table appendix attachment part title ' +
    'tax taxes income sales payroll property estate gift excise return returns audit credit debit account accounts balance ledger ' +
    'bank banking loan mortgage insurance policy claim claims benefits pension retirement savings checking investment ' +
    'agreement contract lease deed will trust amendment addendum settlement release waiver consent ' +
    'health medical dental clinical patient hospital clinic care emergency urgent primary mental behavioral physical occupational ' +
    'human resources customer client vendor supplier employee employer manager director officer president vice chief executive financial operating ' +
    'general special limited senior junior assistant associate deputy acting interim ' +
    'first second third fourth fifth last next prior current former annual quarterly monthly weekly daily fiscal calendar ' +
    'plaintiff defendant petitioner respondent appellant appellee claimant debtor creditor trustee executor landlord tenant buyer seller lender borrower ' +
    'please thank thanks dear regards sincerely best re subject attention confidential privileged draft final ' +
    'google microsoft apple amazon zoom excel word outlook quickbooks zelle venmo paypal visa mastercard amex ' +
    'christmas thanksgiving easter passover ramadan hanukkah labor memorial independence veterans ' +
    'main home work cell mobile fax phone email mail street avenue road suite floor room building ' +
    'yes no not none all any both each either neither other another same such this that these those ' +
    'total subtotal net gross amount paid due owed received remaining opening closing beginning ending ' +
    'common stock preferred shares class series fund capital equity assets liabilities revenue expenses profit loss'
  ).split(' '),
);
// Words that end a message or open one, and are not names.
const SIGN_OFFS = new Set([
  'merci',
  'cordialement',
  'salutations',
  'gracias',
  'saludos',
  'atentamente',
  'danke',
  'thanks',
  'thank',
  'regards',
  'cheers',
  'best',
  'sincerely',
  'yours',
  'respectfully',
  'cordially',
  'warmly',
  'all',
  'team',
  'everyone',
  'folks',
  'again',
  'you',
  'much',
  'kindly',
  'soon',
  'wishes',
  'hi',
  'hello',
  'dear',
  'note',
  'notes',
  'summary',
  'update',
  'reminder',
  'agenda',
  'attendees',
  'present',
  'action',
  'items',
  'next',
  'steps',
  'background',
  'facts',
  'issue',
  'issues',
  'analysis',
  'conclusion',
  'recommendation',
  'question',
  'answer',
  'yes',
  'no',
  'ok',
  'okay',
  'sure',
  'well',
  'also',
  'however',
  'first',
  'second',
  'third',
  'finally',
  'meanwhile',
  'separately',
  'so',
  'and',
  'but',
  'then',
  'today',
  'tomorrow',
  'yesterday',
  'sent',
  'from',
  'for',
  'the',
  'this',
  'that',
]);
// Two- and three-letter strings that are far more often something other than a
// person's initials.
const NOT_INITIALS = new Set(
  (
    'AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND ' +
    'OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY PR AB BC MB NB NL NS NT NU ON PE QC SK YT ' +
    'US UK EU UN IT HR PR QA AI TV PC CC RE FY PO AM PM VP ID NO TO AT ON OR IF OF BY AS IS BE DO GO SO UP WE MY HE ' +
    'CEO CFO COO CTO CIO LLC LLP INC LTD IRS SSA SSN DOB EIN TIN CPA USA FBI CIA ATM PDF FAQ HIV DUI DWI ADA EOB PTO ' +
    'YTD EOM EOY NET TAX THE AND FOR NOT ALL ANY ETA TBD FYI ASAP RSVP DBA AKA FKA NSF ACH EFT PIN VIN MRI ICU ' +
    'DNA RSA CAD USD EUR GBP VAT GST HST PST QST RRSP TFSA IRA ROI KPI SLA NDA MSA SOW RFP PO BOX MD DO RN PA NP'
  ).split(' '),
);

/**
 * Dotted abbreviations and Roman numerals that are not anyone's initials:
 * "S.C.", "U.S.", "VII".
 */
// Common English words that are also in the SSA name list. Capitalized in
// mid-sentence they are usually headings, titles or defined terms ("the Case",
// "Your Honor", "the Manual"), so the large list never makes them names on its
// own (the curated GIVEN_NAMES and cue rules still can).
const SSA_WORDS = new Set(
  `case honor honour lord lady manual trip court major judge justice king prince princess duke earl baron
knight bishop pope saint angel story price cash bank page lane field brook wood woods stone rock river forest ocean sky star
sun moon rain storm snow winter summer spring autumn fall season mark bill will grant chase hope faith joy grace love glory
mercy charity patience prudence chance destiny fortune lucky happy merry sunny rusty dusty sandy candy honey ginger pepper
olive rose lily daisy iris ivy holly hazel violet ruby pearl jade amber crystal diamond gem jewel silver gold golden royal
regal noble general colonel captain sergeant marshal admiral senator governor president deacon pastor dean chancellor master
miss mister sir madam baby boy girl son guy man carter cooper tanner taylor parker hunter fisher baker miller smith walker
turner archer porter mason gardner early young little long short strong wise good best free true sterling bond case
cliff dale glen heath marsh moor ridge vale bay coral reef shore harbor harbour haven meadow prairie canyon valley summit
peak hill rocky stormy windy misty rainy cloud clay flint steel iron copper bronze penny nickel dime crown regent rex reign
legend hero champion victory triumph liberty freedom unity harmony melody lyric poem poet sonnet song music jazz blues
rhythm dancer artist author page reader writer scholar sage oracle prophet miracle blessing heaven paradise eden trinity
genesis exodus psalm journey quest venture wealth rich worth noble gentle brave bold swift lane drive way court terrace
plaza square park garden orchard grove forest jungle desert island delta`.split(
    /\s+/,
  ),
);
/**
 * Returns whether `s` is a known two-letter dotted abbreviation such as "U.S."
 * or "P.O.", or a Roman numeral, and so not a name.
 */
export function isAbbreviation(s: string): boolean {
  const t = s.trim();
  return (
    /^(?:U\.S|U\.K|D\.C|P\.O|P\.C|N\.A|L\.P|P\.A|E\.U|S\.A|A\.M|P\.M|M\.D|J\.D|R\.N|D\.O|N\.Y|L\.A|N\.J|N\.H|N\.M|N\.C|N\.D|S\.C|S\.D|W\.V|R\.I|B\.C|I\.D|V\.P|H\.R|I\.T|Q\.C|K\.C|N\.W|N\.E|S\.W|S\.E|P\.S|R\.E|C\.C|A\.D|B\.A|B\.S|M\.A|M\.S)\.?$/.test(
      t,
    ) || /^(?:II|III|IV|VI|VII|VIII|IX|XI|XII|XIII|XIV|XV)$/.test(t)
  );
}

/**
 * Split a person's name into given names, particles and surname; drop titles
 * and suffixes.
 */
function personParts(full: string) {
  const tokens = collapse(full)
    .split(' ')
    .filter(t => !HONORIFIC.test(t));
  let suffix = '';
  while (tokens.length > 1 && SUFFIX_WORD.test(tokens[tokens.length - 1])) {
    suffix = tokens.pop()!.replace(/,$/, '');
  }
  if (tokens.length && tokens[tokens.length - 1].endsWith(',')) {
    tokens[tokens.length - 1] = tokens[tokens.length - 1].slice(0, -1);
  }
  const last = tokens[tokens.length - 1] ?? '';
  let i = tokens.length - 2;
  const particles: string[] = [];
  while (i > 0 && PARTICLE.test(tokens[i])) particles.unshift(tokens[i--]);
  const given = tokens.slice(0, i + 1);
  return {
    tokens,
    given,
    particles,
    last,
    suffix,
    surname: [...particles, last].join(' '),
  };
}

/**
 * Names that can be read straight off the page, without the model.
 * Returns full names (people) and organization names as written.
 */
// First names of six letters or more that are also ordinary words when typed in
// lower case.
const LOWER_NAME_STOP = new Set([
  'hunter',
  'harper',
  'carter',
  'cooper',
  'tanner',
  'taylor',
  'parker',
  'sawyer',
  'porter',
  'summer',
  'autumn',
  'winter',
  'august',
  'violet',
  'ginger',
  'crystal',
  'heather',
  'melody',
  'harmony',
  'charity',
  'patience',
  'justice',
  'liberty',
  'victor',
  'junior',
  'sterling',
  'marshal',
  'marshall',
  'bishop',
  'destiny',
  'christian',
  'forest',
  'forrest',
  'stormy',
  'rosemary',
  'constance',
  'prudence',
  'chance',
  'chandler',
  'fisher',
  'archer',
  'spencer',
  'walker',
  'turner',
  'tucker',
  'trinity',
  'serenity',
  'precious',
  'unique',
  'majesty',
  'genesis',
  'journey',
  'legend',
  'maverick',
  'canyon',
  'denver',
  'dallas',
  'austin',
  'houston',
  'phoenix',
  'london',
  'sydney',
  'paris',
  'ireland',
  'israel',
  'jordan',
  'chelsea',
  'savannah',
  'charlotte',
  'virginia',
  'georgia',
  'carolina',
  'florence',
  'victoria',
  'regina',
  'madison',
  'jackson',
  'lincoln',
  'carson',
  'montana',
  'dakota',
  'cheyenne',
  'sierra',
  'aurora',
  'scarlet',
  'scarlett',
  'willow',
  'clover',
  'jasmine',
  'juniper',
  'magnolia',
  'marigold',
  'dahlia',
  'diamond',
  'emerald',
  'silver',
  'golden',
  'ocean',
  'river',
  'meadow',
  'prairie',
  'storm',
  'winter',
  'season',
  'reason',
  'treasure',
  'miracle',
  'promise',
  'blessing',
  'heaven',
  'angelic',
  'divine',
  'bonnie',
  'sonny',
  'buster',
  'buddy',
  'cricket',
  'bunny',
  'kitty',
  'missy',
  'sissy',
  'honey',
  'candy',
  'cookie',
  'peaches',
  'cherry',
  'pepper',
  'olive',
  'clementine',
  'early',
  'german',
  'french',
  'english',
  'norman',
  'roman',
  'gordon',
  'grover',
  'butler',
  'cannon',
  'dexter',
  'gentry',
  'mercer',
  'palmer',
  'sailor',
  'sawyer',
  'skyler',
  'stetson',
  'thatcher',
  'weaver',
  'wheeler',
  'wilder',
  'windsor',
  'yankee',
  'general',
  'colonel',
  'captain',
  'doctor',
  'master',
  'mister',
  'senior',
  'pastor',
  'deacon',
  'father',
  'sister',
  'brother',
  'mother',
  'cousin',
  'friend',
  'lovely',
  'pretty',
  'beauty',
  'gentle',
  'bright',
  'clever',
  'lucky',
  'merry',
  'happy',
  'sunny',
  'stormy',
  'windy',
  'rainy',
  'misty',
  'dusty',
  'rusty',
  'sandy',
  'rocky',
  'woody',
  'ruby',
  'pearl',
  'amber',
  'ebony',
  'ivory',
  'sable',
  'raven',
  'robin',
  'wren',
  'lark',
  'dove',
  'finch',
  'falcon',
  'hawk',
]);
// First names that are also months, weekdays or ordinary nouns: a name only
// when the sentence treats them as a person.
const ALSO_A_WORD = new Set([
  'les',
  'january',
  'jan',
  'april',
  'may',
  'june',
  'july',
  'august',
  'tues',
  'summer',
  'autumn',
  'winter',
  'van',
  'lake',
  'bail',
  'miranda',
  'ann',
  'dawn',
  'faith',
  'hope',
  'joy',
  'grace',
  'bill',
  'mark',
  'art',
  'pat',
  'rob',
  'sue',
  'will',
  'chase',
  'grant',
  'rose',
  'drew',
  'frank',
  'jack',
  'penny',
  'iris',
  'ivy',
  'daisy',
  'holly',
  'robin',
  'dean',
  'earl',
  'duke',
  'king',
  'prince',
  'major',
  'page',
  'reed',
  'wade',
  'lane',
  'ford',
  'lincoln',
  'mercedes',
  'paris',
  'jordan',
  'chad',
  'georgia',
  'virginia',
  'carolina',
  'dakota',
  'montana',
  'austin',
  'dallas',
  'houston',
  'phoenix',
  'savannah',
  'charlotte',
  'madison',
  'jackson',
  'lincoln',
  'carson',
  'regina',
  'victoria',
  'florence',
  'sydney',
  'kelly',
  'angel',
  'christian',
  'destiny',
  'justice',
  'sage',
  'sky',
  'star',
  'storm',
  'sunny',
  'trinity',
  'unique',
  'precious',
  'summer',
]);
/**
 * Capitalized words that are common in business and legal writing and are not
 * names: job titles, headings, statute words, makes of vehicle.
 */
export const NOT_NAME_WORDS = new Set(
  (
    'member members manager managing director officer president vice superintendent analyst procurement supervisor coordinator ' +
    'administrator assistant associate partner counsel clerk agent trustee executor settlor grantor beneficiary technical senior junior chief general regular special annual ' +
    'meeting minutes agenda payment payments transfer subscription master intake business new economy plus faster land labour labor day act acts code rules rule rights civil ' +
    'criminal procedure practices privacy notice discrimination retaliation negligent negligence hiring retention supervision entrustment jurisdiction venue exhibit exhibits ' +
    'schedule appendix section article title count claim claims relief damages complaint answer motion order orders judgment health history visit office field landscape ' +
    'construction transportation carrier age equal employment opportunity immigration review between that they this these those there then when where which while with from ' +
    'hours gross net phone email note notes by contact address city state zip total subtotal balance amount date dated period signed prior form forms letters storage ' +
    'toyota honda ford chevrolet chevy nissan subaru mazda lexus hyundai kia volkswagen audi bmw mercedes volvo tesla jeep dodge buick cadillac gmc chrysler freightliner ' +
    'corolla camry civic accord outback hybrid sedan truck pickup van suv tractor trailer'
  ).split(' '),
);

/**
 * Words the document also writes in lower case, standing on their own
 * ("signed", "letters"). A capitalized word that is on this list is an ordinary
 * word at the start of a sentence or in a heading, not part of a name.
 */
export function ordinaryWordsOf(text: string): Set<string> {
  const prose = text.replace(
    /\b\S+ (?:dot|at|underscore) \S+(?: (?:dot|at|underscore) \S+)*/g,
    ' ',
  ); // "bob underscore k at mail dot example"
  return new Set(
    prose.match(
      /(?<![\p{L}\p{N}@._'’/\\=:-])\p{Ll}{3,}(?![\p{L}\p{N}@_'’/\\-]|\.[a-z])/gu,
    ) ?? [],
  );
}

/**
 * Explicit quoted control labels, used only to qualify the weak X & Y firm
 * rule. Quotes alone say nothing about privacy. A label is not an exemption for
 * model evidence, a legal company ending, a person's name or a structured
 * identifier.
 */
function quotedControlLabels(text: string): Array<[number, number]> {
  const labels: Array<[number, number]> = [];
  for (const m of text.matchAll(
    /"([^"\r\n]{1,120})"|“([^”\r\n]{1,120})”|(?<![\p{L}\p{N}])'([^'\r\n]{1,120})'|‘([^’\r\n]{1,120})’/gu,
  )) {
    const before = text.slice(Math.max(0, m.index - 100), m.index);
    const after = text.slice(m.index + m[0].length, m.index + m[0].length + 35);
    if (
      /\b(?:client|company|customer|employer|vendor|supplier|recipient|payee|patient|contact)(?:\s+name)?\s*[:=]\s*$/i.test(
        before,
      )
    ) {
      continue;
    }
    const controlAfter =
      /^\s+(?:setting|cycle|mode|button|menu option)\b/i.test(after);
    const controlBefore =
      /\b(?:setting|cycle|mode|button|menu option)\s*(?:(?:called|named|labelled|labeled|to)\s+|:\s*)?$/i.test(
        before,
      );
    const dialBefore =
      /\b(?:turn|rotate|move|set)\s+(?:the\s+)?(?:dial|knob|selector)\b[^.!?;:\r\n]{0,65}\b(?:to|past)\s*$/i.test(
        before,
      );
    if (controlAfter || controlBefore || dialBefore) {
      labels.push([m.index + 1, m.index + m[0].length - 1]);
    }
  }
  return labels;
}

/**
 * Finds names from reliable cues in the text: a title such as "Dr." or "Judge",
 * a company ending such as "LLC", "SURNAME, First" in forms, "known as …". Also
 * returns `links` for written forms that cannot be derived from the name they
 * belong to.
 */
export function discoverNames(text: string): Names {
  const lowerHere = ordinaryWordsOf(text);
  const controlLabels = quotedControlLabels(text);
  const plainWord = (w: string) => {
    const k = w.replace(/[^\p{L}]/gu, '').toLocaleLowerCase('en-US');
    return (
      k.length >= 3 &&
      (lowerHere.has(k) ||
        ORDINARY.has(k) ||
        NOT_A_NAME.has(k) ||
        NOT_NAME_WORDS.has(k))
    );
  };
  const people = new Set<string>();
  const companies = new Set<string>();
  const links: Array<{text: string; person: string}> = [];
  const addPerson = (s: string) => {
    if (/\n/.test(s.trim())) return;
    const name = collapse(s).replace(/[,.;:]+$/, '');
    const first = name.split(' ')[0];
    if (
      name.length >= 3 &&
      /^\p{Lu}/u.test(name) &&
      !NOT_A_NAME.has(key(first))
    ) {
      people.add(name);
    }
  };

  // A title followed by a name: "Dr. Anand Krishnamurthy", "Judge Vandermeer",
  // "Mrs Adeyemi-Clarke"
  for (const m of text.matchAll(
    new RegExp(
      `\\b(?:${TITLE})\\.?\\s+((?:${NAME_TOKEN}\\s+){0,4}${NAME_WORD})`,
      'gu',
    ),
  )) {
    // Stop at a company ending so "Dr. Park Pediatrics" keeps only "Park".
    const words = m[1].split(/\s+/);
    const cut = words.findIndex(
      (w, i) => i > 0 && new RegExp(`^(?:${ORG_END})$`).test(w),
    );
    addPerson((cut > 0 ? words.slice(0, cut) : words).join(' '));
  }
  // A title and a single letter used as a name: "Dr. Q stays the only signer"
  for (const m of text.matchAll(
    new RegExp(`\\b(?:${TITLE})\\.?\\s[A-Z]\\b(?![.'’\\p{L}])`, 'gu'),
  )) {
    people.add(collapse(m[0]));
  }
  // A title and a surname in capitals: "M. et Mme ENTWISTLE", "MR C J
  // RUTHERGLEN"
  for (const m of text.matchAll(
    new RegExp(
      `\\b(?:${TITLE})\\.?\\s+((?:[A-Z]\\.?\\s){0,2}[A-Z][A-Z'’-]{3,})\\b(?![\\p{Ll}])`,
      'gu',
    ),
  )) {
    if (
      !NOT_INITIALS.has(m[1]) &&
      !plainWord(m[1]) &&
      !new RegExp(`^(?:${CAPS_END})$`).test(m[1])
    ) {
      people.add(collapse(m[1]));
    }
  }
  // The name embossed on a card: "Name on card: LUCINDA M APONTE-RHEE"
  for (const m of text.matchAll(
    /\b[Nn]ame\son\s(?:the\s)?(?:card|it|account)(?:\sis)?:?\s+((?:(?:MR|MRS|MS|DR)\s)?[A-Z][A-Z'’-]*(?:\s[A-Z][A-Z'’-]*){1,3})\b(?![\p{Ll}])/gu,
  )) {
    people.add(collapse(m[1]));
  }
  // A surname in capitals in a case name: "GOLZARI v. STONECUTTER ASSURANCE"
  for (const m of text.matchAll(
    /(?<![A-Z&] )\b([A-Z][A-Z'’-]{3,})(?=\sv\.?\s[A-Z])/g,
  )) {
    if (
      !plainWord(m[1]) &&
      !CASE_PARTY.has(key(m[1])) &&
      !NOT_INITIALS.has(m[1])
    ) {
      people.add(m[1]);
    }
  }
  // "My maiden name was Stachura", "(maiden name Solheim-Berge)"
  for (const m of text.matchAll(
    new RegExp(
      `\\b(?i:maiden\\s+name|birth\\s+name|former\\s+name|married\\s+name)(?:\\s+(?:was|is|of))?:?\\s+(${NAME_WORD}(?:\\s${NAME_WORD})?)`,
      'gu',
    ),
  )) {
    if (!plainWord(m[1].split(' ')[0])) addPerson(m[1]);
  }
  // A family called by its name: "Relocation file: Zubeldia family"
  for (const m of text.matchAll(
    new RegExp(`(?<![\\p{L}'’-])(${NAME_WORD})(?=\\sfamily\\b)`, 'gu'),
  )) {
    if (!plainWord(m[1]) && !NOT_A_HOME.has(key(m[1]))) people.add(m[1]);
  }
  // Notes typed in lower case. A label, a title or "this is ... calling" says
  // the next words are a name: "client: tyrese m. goodwine", "tp: dwayne e
  // broadnax", "ms. hyacinth", "ofc mulvaney-luz", "this is uh ronnie latiolais
  // calling"
  for (const m of text.matchAll(
    /(?<=(?:^|\n|[.;]\s)(?:client|tp|sp|taxpayer|spouse|patient|employee|witness|victim|defendant|caller)\s?:\s)[a-z]{3,}(?:\s[a-z]\.?)?\s[a-z][a-z'-]{2,}(?=\s{2}|[,.;]|\s*$|\s+(?:ss|dob|ssn|goes|aka)\b)/gm,
  )) {
    people.add(m[0]);
  }
  for (const m of text.matchAll(
    /\b(?:(?:mr|mrs|ms|dr)\.|ofc\.?|officer|det\.?|sgt\.?)\s([a-z][a-z'-]{2,})\b/g,
  )) {
    if (
      !/^(?:the|and|was|is|said|says|at|on|in|for|who|his|her|apt|unit|suite|office|told|will|has|had)$/.test(
        m[1],
      )
    ) {
      people.add(m[1]);
    }
  }
  for (const m of text.matchAll(
    /(?<=\bthis\sis\s(?:uh\s|um\s)?)[a-z]{3,}\s[a-z][a-z'-]{2,}(?=\s(?:calling|speaking|from|here)\b)/g,
  )) {
    people.add(m[0]);
  }
  // "goes by reese", aka "dre"
  for (const m of text.matchAll(
    /(?<=\b(?:goes\sby|known\sas|aka|a\/k\/a|a\.k\.a\.?)\s["“]?)[a-z]{3,12}(?=["”]?(?:[\s.,;)-]|$))/g,
  )) {
    if (
      !/^(?:the|his|her|their|a|an|that|this|another|different)$/.test(m[0])
    ) {
      people.add(m[0]);
    }
  }
  // A first name typed in lower case, when it is a name and not also a word:
  // "shanice has the only key"
  for (const m of text.matchAll(
    /(?<![\p{L}\p{N}@._'’/-])[a-z]{6,12}(?![\p{L}\p{N}@_/-]|\.[a-z])/gu,
  )) {
    if (
      GIVEN_NAMES.has(m[0]) &&
      !ALSO_A_WORD.has(m[0]) &&
      !AMBIGUOUS_NAMES.has(m[0]) &&
      !LOWER_NAME_STOP.has(m[0])
    ) {
      people.add(m[0]);
    }
  }
  // A party in a case name: "Kowalczyk v. Brightpath Home Care, LLC"
  for (const m of text.matchAll(
    new RegExp(
      `(?<!\\p{Lu}[\\p{L}'’&.,-]*\\s)(${NAME_WORD})(?=\\s(?:v|vs)\\.?\\s+\\p{Lu})`,
      'gu',
    ),
  )) {
    if (
      !ORDINARY.has(key(m[1])) &&
      !NOT_A_NAME.has(key(m[1])) &&
      !CASE_PARTY.has(key(m[1]))
    ) {
      people.add(m[1]);
    }
  }
  // A matter or deal called by a party's name: "the Hartwell brief"
  for (const m of text.matchAll(
    new RegExp(
      `(?<=\\bthe\\s)(${NAME_WORD})(?=\\s(?:spec\\s+house|house|residence|household|family|return|tax\\s+return|folder|job|remodel|renovation|kitchen|wedding|brief|matter|case|file|deal|account|appeal|litigation|settlement|transaction|engagement|audit|lawsuit|trial|closing|project|estate|claim)\\b)`,
      'gu',
    ),
  )) {
    if (!ORDINARY.has(key(m[1])) && !NOT_A_NAME.has(key(m[1]))) {
      people.add(m[1]);
    }
  }
  // Initial and surname, not at the start of a line (which is usually an
  // outline heading)
  for (const m of text.matchAll(
    new RegExp(
      `(?<=[^\\n\\s][^\\n]*?[\\s(:;,])(?<!\\p{Lu}[\\p{Ll}'’-]+\\s)(?<!\\d )([A-Z]\\.(?:\\s?[A-Z]\\.)?\\s(?:(?:de|del|la|van|von|der|di|da)\\s)*${NAME_WORD})(?!\\.,?\\s?(?:Stat|Code|§|No\\b|Rev|Ann|Admin|Const|Civ|Crim|App|\\d))`,
      'gu',
    ),
  )) {
    if (plainWord(m[1].split(' ').pop()!)) continue;
    if (
      !/^(?:B\.\s?V\.|N\.\s?V\.|S\.\s?L\.|U\.\s?S\.|U\.\s?K\.|D\.\s?C\.|P\.\s?O\.|N\.\s?A\.|P\.\s?C\.|L\.\s?P\.|E\.\s?U\.|S\.\s?A\.|P\.\s?A\.|I\.\s?D\.|N\.\s?[YWEJ]\.|S\.\s?[WE]\.|L\.\s?A\.|[A-Z]\.\s?[A-Z]\.\s(?:Box|Code))/.test(
        m[1],
      ) &&
      !NOT_A_NAME.has(key(m[1].split(' ').pop()!))
    ) {
      addPerson(m[1]);
    }
  }
  // Forms and captions: "OYELARAN, Adebayo T."  "WISNIEWSKI, KATARZYNA"
  // "McALLISTER, BILL"
  for (const m of text.matchAll(
    /\b((?:Mc|Mac|O['’]|De |Van )?[A-Z][A-Z'’-]{2,}(?:\s[A-Z][A-Z'’-]{2,})?),\s([A-Z][\p{L}'’-]+(?:\s[A-Z][\p{L}'’-]+)?(?:\s[A-Z]\b\.?)?)(?:\s(?:JR|SR|II|III|IV)\b\.?)?/gu,
  )) {
    const firstGiven = m[2].split(' ')[0];
    if (
      new RegExp(`^(?:${ORG_END}|${CAPTION_ROLE})\\.?$`, 'i').test(
        firstGiven,
      ) ||
      NOT_A_NAME.has(key(firstGiven)) ||
      NOT_INITIALS.has(m[1])
    ) {
      continue;
    }
    if (
      plainWord(firstGiven) ||
      m[1].split(/\s/).some(plainWord) ||
      NOT_INITIALS.has(firstGiven) ||
      /^[A-Z]{2,5}$/.test(firstGiven)
    ) {
      continue;
    }
    if (
      /^(?:RPR|CPA|CPAS|ESQ|LLC|INC|PHD|DDS|DMD|LCSW|APRN|CRNA|CFP|CFA|MBA|LLP|PLLC)$/.test(
        m[1],
      ) ||
      m[1].length <= 3 ||
      /^(?:Certified|Licensed|Registered|Chartered|Board)$/.test(firstGiven)
    ) {
      // "NEGLIGENT HIRING, RETENTION", "DNR, POLST"
      continue;
    }
    const title = (w: string) =>
      w.length > 2 && w === upper(w)
        ? w[0] + w.slice(1).toLocaleLowerCase('en-US')
        : w;
    const surname = m[1]
      .split(/([\s'’-])/)
      .map(title)
      .join('');
    const rebuilt = `${m[2].split(' ').map(title).join(' ')} ${surname}`;
    addPerson(rebuilt);
    links.push({text: collapse(m[0]), person: rebuilt});
  }
  // Court captions: "In re: MARISOL ECHEVARRÍA-LUND, Petitioner, and TREVOR J.
  // LUND, Respondent."
  for (const m of text.matchAll(
    new RegExp(
      `\\b(\\p{Lu}[\\p{Lu}'’.-]+(?:\\s\\p{Lu}[\\p{Lu}'’.-]*){1,3}),\\s(?:${CAPTION_ROLE})\\b`,
      'gu',
    ),
  )) {
    addPerson(m[1]);
  }
  for (const m of text.matchAll(
    /\b(?:In re:?|In the Matter of|Estate of|ESTATE OF|IN RE:?)\s+(\p{Lu}[\p{Lu}'’.-]+(?:\s\p{Lu}[\p{Lu}'’.-]*){1,3})\b/gu,
  )) {
    addPerson(m[1]);
  }
  // Given name, middle initial, surname: "Thomas J. Achebe"
  for (const m of text.matchAll(
    new RegExp(
      `\\b(${NAME_WORD}\\s[A-Z]\\.\\s(?:(?:de|del|la|van|von|der|di|da)\\s)*${NAME_WORD})`,
      'gu',
    ),
  )) {
    addPerson(m[1]);
  }
  // Email display names: Leon Brathwaite <leon@firm.example>, "Abimbola,
  // Stuart" <s@firm.example>
  for (const m of text.matchAll(
    /["“]?([\p{Lu}][\p{L}.'’,-]+(?:\s[\p{L}.'’-]+){1,3})["”]?\s*<[^<>\s@]+@[^<>\s]+>/gu,
  )) {
    const raw = m[1].trim();
    const flip = /^([^,]+),\s*(.+)$/.exec(raw);
    addPerson(flip ? `${flip[2]} ${flip[1]}` : raw);
  }
  // A name followed by a role or credential: "Marlene Fitch, RPR", "Rupert
  // Pemberton, Partner"
  for (const m of text.matchAll(
    new RegExp(
      `\\b(${NAME_WORD}(?:\\s[A-Z]\\.)?(?:\\s(?:de|del|la|van|von|der|di|da))*\\s${NAME_WORD}),\\s(?:${ROLE_AFTER})\\b`,
      'gu',
    ),
  )) {
    addPerson(m[1]);
  }
  // A role or relationship word followed by a name: "paralegal Wendy
  // Pruitt-Sato", "her son Tom Whitfield"
  for (const m of text.matchAll(
    new RegExp(
      `\\b(?:${ROLE_BEFORE}),?\\s(${NAME_WORD}(?:\\s[A-Z]\\.)?(?:\\s(?:de|del|la|van|von|der|di|da))*\\s${NAME_WORD})`,
      'gu',
    ),
  )) {
    addPerson(m[1]);
  }
  // A form field: "Prepared by: Renee Calloway", "Patient\tWendell Running
  // Bear"
  for (const m of text.matchAll(
    new RegExp(
      `(?:^|\\n|\\t)[^\\S\\n]*(?:${FIELD_LABEL})[^\\S\\n]*[:\\t][^\\S\\n]*(${NAME_WORD}(?:\\s[A-Z]\\.)?(?: (?:de|del|la|van|von|der|di|da))*(?: ${NAME_WORD}){1,2})(?=[^\\S\\n]*(?:[,;(<\\n\\t]|$))`,
      'gu',
    ),
  )) {
    addPerson(m[1]);
  }
  // Initials where a person is expected: "Fee earner  RJP", "Present: DKL",
  // "NOTE FOR CO'B"
  for (const m of text.matchAll(
    /\b(?:Fee earner|Present|Attendees|Attending|cc|bcc|Initials|Prepared by|Reviewed by|Summarized by|Drafted by|Approved by|Author|Preparer|Timekeeper|TK|NOTE FOR|Note for|Note to|per)[^\S\n]*[:\t ][^\S\n]*([A-Z][A-Z'’]{1,3})\b(?![A-Za-z'’-])/g,
  )) {
    if (!NOT_INITIALS.has(m[1])) people.add(m[1]);
  }
  // Name fields on a form: "Last name: DIMACULANGAN       First: Maria Corazon"
  for (const m of text.matchAll(
    /\b(?i:last name|surname|family name|first name|first|given names?|middle name|maiden name)[^\S\n]*:[^\S\n]*(\p{Lu}[\p{L}'’-]+(?: \p{Lu}[\p{L}'’-]+)?)(?=[^\S\n]{2,}|[^\S\n]*(?:\n|$|[,;(]))/gu,
  )) {
    if (
      !NOT_A_NAME.has(key(m[1].split(' ')[0])) &&
      !ORDINARY.has(key(m[1].split(' ')[0]))
    ) {
      people.add(m[1]);
    }
  }
  // The same after a label that needs its colon: "Reviewer: IF", "Reviewed:
  // HJK", "taken by: KS"
  for (const m of text.matchAll(
    /\b(?i:Reviewer|Reviewed|Prepared|Preparer|Drafted|Taken by|Typed by|Dictated by|Intake by|Entered by|Notes by|Interviewer|Staff)[^\S\n]*:[^\S\n]*([A-Z][A-Z'’-]{1,3})\b(?![A-Za-z'’-])/g,
  )) {
    if (!/^(?:NO|YES|NA|TBD|OK|ALL|SEE|PER|FOR|NOT|YTD|N-A)$/.test(m[1])) {
      people.add(m[1]);
    }
  }
  // Initials after a credential, in brackets: "Triage note (RN SB)"
  for (const m of text.matchAll(
    /(?<=\((?:RN|LPN|NP|PA|PA-C|MD|DO|CNA|MA|RT|PT|OT|SW|LCSW|CPA|EA)\s)[A-Z]{2,3}(?=\))/g,
  )) {
    people.add(m[0]);
  }
  // A typist's initials in lower case: "Summarized by: jdl", "typed dhp"
  for (const m of text.matchAll(
    /\b(?i:summarized by|typed(?: by)?|taken by|prepared by|reviewed by|drafted by|dictated by|entered by|notes by|transcribed by)[^\S\n]*:?[^\S\n]*([a-z]{2,3})\b(?=[,;)\s]|$)/g,
  )) {
    if (!SMALL_WORDS.has(m[1])) people.add(m[1]);
  }
  // "known as Sade", "a/k/a Bobby Kowalczyk", and a nickname in quotes inside a
  // name
  for (const m of text.matchAll(
    new RegExp(
      `\\b(?i:known\\s+as|goes\\s+by|went\\s+by|calls?\\s+(?:him|her|them|me)|called\\s+(?:him|her|them|me)|calling\\s+(?:him|her|them)|a\\/k\\/a|aka|a\\.k\\.a\\.?|nicknamed|née|nee|f\\/k\\/a|formerly\\s+known\\s+as)\\s+["“'‘]?(${NAME_WORD}(?:\\s${NAME_WORD}){0,2})`,
      'gu',
    ),
  )) {
    addPerson(m[1]);
  }
  for (const m of text.matchAll(
    new RegExp(
      `${NAME_WORD}\\s+["“(]\\s?(${NAME_WORD})\\s?["”)]\\s+${NAME_WORD}`,
      'gu',
    ),
  )) {
    addPerson(m[1]);
  }

  // Organizations: capitalized words ending in a company or institution word
  // names found by cue stay on one line, and inside one table cell
  const SP = '[^\\S\\n\\t]+';
  const WRAP = `(?:${SP}|\\n(?![^\\n]*\\t))`; // a name may wrap onto the next line, unless that line is a table row
  const org = new RegExp(
    `\\b(?:The${SP})?(${ORG_WORD}(?:${SP}(?:${ORG_WORD}|${CONNECT}|(?:19|20)\\d{2}|\\([A-Z]{2,}\\))){0,6}?,?${WRAP}(?:${ORG_END_WRAP})\\b\\.?(?:,?${WRAP}(?:${ORG_END_WRAP})\\b\\.?)*)`,
    'gu',
  );
  for (const m of text.matchAll(org)) {
    // A role or heading word in front is not part of the name: "Defendant
    // Brightwater Freight Systems, Inc."
    const words = collapse(m[1]).split(' ');
    const ourLady = () =>
      words[0] === 'Our' &&
      /^(?:Lady|Savior|Saviour|Redeemer|Mother|Father|Lord)$/.test(words[1]);
    while (
      words.length > 2 &&
      ((NOT_A_NAME.has(key(words[0])) && !ourLady()) ||
        LEAD_ROLE.test(words[0]) ||
        /['’]s$/.test(words[0]) ||
        (plainWord(words[0]) &&
          !ourLady() &&
          !ORG_END_ONLY.test(words[1].replace(/[.,]+$/, ''))))
    ) {
      words.shift();
    }
    // "U.S. District" in "U.S. District Court", "Prior Chapter" in "Prior
    // Chapter 13": not an organization's name.
    const after = text.slice(m.index + m[0].length, m.index + m[0].length + 8);
    if (
      /^\sCourt\b/.test(after) ||
      (/\bChapter$/.test(words[words.length - 1]) && /^\s\d/.test(after)) ||
      /^(?:United States|U\.S\.|UNITED STATES)\b/.test(words.join(' '))
    ) {
      continue;
    }
    // At least one word must be a name rather than an ordinary word: not
    // "Letters of Authority".
    if (
      !words.some(
        w =>
          /^\p{Lu}/u.test(w) &&
          w.replace(/[^\p{L}]/gu, '').length >= 3 &&
          !plainWord(w) &&
          !ORG_END_ONLY.test(w.replace(/[.,]+$/, '')) &&
          !/^(?:of|and|the|for)$/i.test(w),
      )
    ) {
      continue;
    }
    if (
      words.length < 2 ||
      (NOT_A_NAME.has(key(words[0])) && !ourLady()) ||
      ORG_END_ONLY.test(words[0].replace(/[.,]+$/, ''))
    ) {
      continue;
    }
    const name = words.join(' ');
    // A comma belongs in a name only before a legal ending: not "Computer
    // Science, University"
    if (
      /,\s(?!(?:Inc|Incorporated|LLC|L\.L\.C|LLP|L\.L\.P|LP|L\.P|PLLC|P\.L\.L\.C|P\.L\.C|P\.C|PC|P\.A|S\.C|Ltd|Limited|Corp|Corporation|Co|Company|PLC|GmbH|N\.A|Chartered)\b)/.test(
        name,
      )
    ) {
      continue;
    }
    const clean = name.replace(/[,;:]+$/, '');
    companies.add(
      ABBREVIATED_END.test(clean) ? clean : clean.replace(/\.$/, ''),
    );
  }
  // In capitals, as in a letterhead or a caption: "SAGEBRUSH FAMILY MEDICINE",
  // "FAIRWEATHER ESTATE". The whole run of capitals must be the name: it starts
  // the run and ends it.
  const capsOrg = new RegExp(
    `(?<![A-Z&][^\\S\\n\\t]?)\\b((?:[A-Z][A-Z'’.-]*,?[^\\S\\n\\t]){1,5}?(?:(?:&|OF|AND)[^\\S\\n\\t](?:[A-Z][A-Z'’.-]*[^\\S\\n\\t]){1,3}?)?(?:${CAPS_END}))\\b(?![^\\S\\n\\t]?[A-Z&]|[.'’-]?[A-Za-z])`,
    'g',
  );
  for (const m of text.matchAll(capsOrg)) {
    const words = m[1].replace(/,/g, '').split(/\s+/);
    const telling = words
      .slice(0, -1)
      .filter(
        w =>
          /^[A-Z]{3,}/.test(w) &&
          !plainWord(w) &&
          !GENERIC_CAPS.has(w) &&
          !new RegExp(`^(?:${CAPS_END})$`).test(w),
      );
    if (telling.length) companies.add(collapse(m[1]));
  }
  // A run of two to five capitalized words that ends the way organizations'
  // names end and starts with a word that is a name rather than an ordinary
  // word: "Menomonee Valley Animal Rescue", "Halsted Street Bakehouse".
  for (const m of text.matchAll(
    new RegExp(
      `(?<![\\p{L}'’-]|\\p{Lu}[\\p{L}'’-]* )(${NAME_WORD}(?: ${NAME_WORD}){0,3}) (${ORG_TAIL_WORDS})(?![\\p{L}'’-]| \\p{Lu}\\p{Ll})`,
      'gu',
    ),
  )) {
    const first = m[1].split(' ')[0];
    if (
      plainWord(first) ||
      NOT_A_NAME.has(key(first)) ||
      LEAD_ROLE.test(first) ||
      new RegExp(`^(?:${ORG_TAIL_WORDS})$`).test(first)
    ) {
      continue;
    }
    companies.add(collapse(m[0]));
  }
  // Three capitalized words in mid-sentence, the first of them not an ordinary
  // word: a name of some kind. "of Vasbinder Facial Plastics saw", "Maeve
  // Teskey, Teskey Injury Law, 410-55 ...". An organization unless it opens
  // with a first name.
  for (const m of text.matchAll(
    new RegExp(
      `(?<=[\\p{Ll},;:(] )(?<!\\p{Lu}[\\p{L}'’-]* )(${NAME_WORD}) (${NAME_WORD}) (${NAME_WORD})(?: (${NAME_WORD}))?(?![\\p{L}'’-]|\\s\\p{Lu})`,
      'gu',
    ),
  )) {
    const ws = [m[1], m[2], m[3], ...(m[4] ? [m[4]] : [])];
    if (
      LEAD_ROLE.test(m[1]) ||
      plainWord(m[1]) ||
      ws.filter(plainWord).length > 1 ||
      ws.some(w => NOT_A_NAME.has(key(w)))
    ) {
      continue;
    }
    const lastWord = ws[ws.length - 1];
    if (
      new RegExp(`^(?:${STREET_WORDS})$`).test(lastWord) ||
      /\sCity$/.test(m[0])
    ) {
      continue;
    }
    if (/^(?:Jr|Sr|II|III|IV|Esq|MD|RN|CPA|EA|PhD|DDS|JD)$/.test(lastWord)) {
      // "Héctor Reyes Jr." is a person with a suffix
      continue;
    }
    if (GIVEN_NAMES.has(key(m[1])) && !ORG_TAIL.test(lastWord)) addPerson(m[0]);
    else companies.add(m[0]);
  }
  // Legal endings written in lower case, as in Quebec: "Textiles Beauharnois
  // ltée", "Bistro Le Cormoran inc."
  for (const m of text.matchAll(
    /(?<![\p{L}\p{N}])\p{Lu}[\p{L}'’&-]*(?:[^\S\n\t](?:\p{Lu}[\p{L}'’&-]*|de|du|des|la|le|et|&)){0,5}[^\S\n\t](?:inc\.|ltée|ltee|lt[ée]e\.|enr\.|s\.e\.n\.c\.|mbB|e\.V\.|S\.L\.|S\.A\.S\.|SARL|B\.V\.|N\.V\.|GmbH|Pty Ltd)(?![\p{L}])/gu,
  )) {
    companies.add(collapse(m[0]));
  }
  // A name with a lower-case surname particle: "Nik van der Giesen", "Ludwig
  // von Hartmann", "Anna de la Cruz". The particle between two capitalized
  // words is the cue, so this works at the start of a sentence too. Dutch and
  // German particles are rarely anything but a surname. Romance ones also
  // join place and product names ("Tour de France", "Pico de Gallo"), so
  // those need a known first name in front.
  for (const m of text.matchAll(
    new RegExp(
      `(?<![p{L}p{N}'’-])(${NAME_WORD}) (van der|van den|van de|van het|van|von der|von dem|von|ter|ten|te|zu|op de|op den|af|bin|ibn|de la|de los|de las|del|della|dello|degli|de|di|da|dos|das|du|le|la) (${NAME_WORD})(?![p{L}'’-])`,
      'gu',
    ),
  )) {
    const [whole, first, particle, last] = m;
    const firstKey = key(first);
    const lastKey = key(last);
    if (
      COMMON_WORDS.has(firstKey) ||
      ORDINARY.has(firstKey) ||
      NOT_A_NAME.has(firstKey) ||
      plainWord(first)
    ) {
      continue; // "The van der Waals force", "Call von Braun"
    }
    const surnameOnly = /^(?:van|von|ter|ten|te|zu|op|af|bin|ibn)\b/.test(
      particle,
    );
    if (
      !surnameOnly &&
      !(
        (GIVEN_NAMES.has(firstKey) || SSA_GIVEN_NAMES.has(firstKey)) &&
        !GEOGRAPHY.has(lastKey) &&
        !COMMON_WORDS.has(lastKey) &&
        !ORDINARY.has(lastKey) &&
        !PLACE_NAMES.has(key(whole))
      )
    ) {
      continue;
    }
    addPerson(whole);
  }
  // Two capitalized words in mid-sentence, neither of them an ordinary word:
  // very likely a person the other cues missed ("his partner Leland Forsythe
  // wrote").
  for (const m of text.matchAll(
    new RegExp(
      `(?<=[\\p{Ll},;:(] )(${NAME_WORD}) (${NAME_WORD})(?![\\p{L}'’-]|,?\\s(?:${ORG_END}|${STREET_WORDS})\\b|\\s[A-Z]{2,5},?\\s(?:${ORG_END})\\b|\\s\\p{Lu}[\\p{L}'’-]+(?![\\p{L}'’-]|\\s\\p{Lu}))`,
      'gu',
    ),
  )) {
    if (LEAD_ROLE.test(m[1])) continue; // "compelling Defendants Stavros ..."
    // "Privacy Practices", "Managing Member", "Toyota Corolla"
    if (plainWord(m[1]) || plainWord(m[2])) continue;
    if (ORG_TAIL.test(m[2])) continue; // "Animal Rescue"
    // "this Past Weekend", "Game Seven", "Happy Birthday": two everyday words
    // in capitals are a phrase, not a person.
    if (COMMON_WORDS.has(key(m[1])) && COMMON_WORDS.has(key(m[2]))) continue;
    // "South America", "Saudi Arabia", "Team Canada": a large place, or an
    // everyday word in front of one. An unfamiliar word in front ("Payworks
    // Midwest") is still a name of some kind.
    if (
      isLargePlace(m[0]) ||
      (GEOGRAPHY.has(key(m[2])) && COMMON_WORDS.has(key(m[1])))
    ) {
      continue;
    }
    if (
      !ORDINARY.has(key(m[1])) &&
      !ORDINARY.has(key(m[2])) &&
      !NOT_A_NAME.has(key(m[1])) &&
      !GENERIC_LAST.has(key(m[2])) &&
      !ORG_END_ONLY.test(m[2]) &&
      !ORG_END_ONLY.test(m[1])
    ) {
      addPerson(m[0]);
    }
  }
  // A first name or nickname standing on its own: "Mateo will stay with
  // Barbara".
  for (const m of text.matchAll(
    /(?<![\p{L}\p{N}'’-])(\p{Lu}[\p{Ll}]+(?:-\p{Lu}[\p{Ll}]+)?)(?![\p{L}\p{N}-])/gu,
  )) {
    const word = m[1];
    const k = key(word);
    // "New Jersey", "West Virginia", "South Dakota": the second word of a
    // state's name is not someone's first name.
    const stateStart = /(\p{Lu}\p{Ll}+)[^\S\n]$/u.exec(
      text.slice(Math.max(0, m.index - 20), m.index),
    );
    if (stateStart && isRegion(`${stateStart[1]} ${word}`)) continue;
    if (
      GIVEN_NAMES.has(k) &&
      !ALSO_A_WORD.has(k) &&
      !/^['’]s\sRules\b/.test(
        text.slice(m.index + word.length, m.index + word.length + 9),
      )
    ) {
      people.add(word);
      continue;
    }
    // The larger public-domain list (given-names-ssa.ts) counts only in
    // mid-sentence, where an ordinary word is rarely capitalized ("Mine is
    // broken. Kalkidan said", "tell Ksenia", "and Shirin").
    if (
      SSA_GIVEN_NAMES.has(k) &&
      // "America", "India" and "Kenya" are on the name list, but in running
      // text they are nearly always the place.
      !GEOGRAPHY.has(k) &&
      !COMMON_WORDS.has(k) &&
      !PLACE_NAMES.has(k) &&
      !SSA_WORDS.has(k) &&
      !ALSO_A_WORD.has(k) &&
      !AMBIGUOUS_NAMES.has(k) &&
      !LOWER_NAME_STOP.has(k) &&
      !plainWord(word) &&
      !ORDINARY.has(k) &&
      !NOT_A_NAME.has(k) &&
      !SIGN_OFFS.has(k) &&
      !GENERIC_LAST.has(k) &&
      !ORG_END_ONLY.test(word) &&
      /(?:[\p{Ll}\p{N},;:)]|\b(?:and|or|with|to|by|for|from))[^\S\n]+$|\($/u.test(
        text.slice(Math.max(0, m.index - 6), m.index),
      )
    ) {
      people.add(word);
      continue;
    }
    if (!AMBIGUOUS_NAMES.has(k) && !ALSO_A_WORD.has(k)) continue;
    // "Grace", "Hunter", "Jordan": a name only when the sentence treats it as a
    // person.
    const before = text.slice(Math.max(0, m.index - 24), m.index);
    const after = text.slice(m.index + word.length, m.index + word.length + 14);
    const midSentence = /[\p{Ll},;]\s$/u.test(before);
    const personal =
      /^(?:['’]s\b|\s(?:said|says|told|asked|called|emailed|texted|wrote|signed|agreed|is|was|has|had|will|would|can|could|did|does|wants|wanted|needs|lives|works)\b|\sand\s\p{Lu})/u.test(
        after,
      ) ||
      /\b(?:with|told|asked|called|and|son|daughter|wife|husband|brother|sister|friend|client|named)\s$/i.test(
        before,
      );
    const lineStart =
      /(?:^|\n)[^\S\n]*$/.test(before) &&
      /^\s(?:said|says|told|asked|called|emailed|texted|wrote|signed|agreed|wants|wanted|needs|keeps|kept|has|had|lives|works)\b/.test(
        after,
      ) &&
      !/^(?:may|will|mark|bill|chase|grant|drew|rose|hope|faith|joy|art|rob|pat|sue|dawn|eve)$/.test(
        k,
      );
    if ((personal && (midSentence || /^['’]s\b/.test(after))) || lineStart) {
      people.add(word);
    }
  }
  // Cue-based rules for short pastes, where no full name elsewhere gives a name
  // away. Each needs a word that is not ordinary vocabulary here, plus a cue
  // that only fits a person.
  const nameLike = (word: string) => {
    const w = word.replace(/['’]s$/, '');
    return nameLikeWord(w);
  };
  const nameLikeWord = (w: string) =>
    !plainWord(w) &&
    !ORDINARY.has(key(w)) &&
    !NOT_A_NAME.has(key(w)) &&
    !SIGN_OFFS.has(key(w)) &&
    !GENERIC_LAST.has(key(w)) &&
    !ORG_END_ONLY.test(w) &&
    !ALSO_A_WORD.has(key(w)) &&
    w.replace(/[^\p{L}]/gu, '').length >= 3 &&
    // Hyphenated names have capitalized parts that are not ordinary words:
    // "Marie-Ève", not "Out-of-Pocket" or "Co-Payments".
    !/-\p{Ll}/u.test(w) &&
    !w
      .split('-')
      .slice(1)
      .some(
        part =>
          plainWord(part) || ORDINARY.has(key(part)) || ORG_END_ONLY.test(part),
      );
  // Cue words match in either case at their first letter; NAME_WORD must keep
  // its capital, so no "i" flag.
  const ci = (words: string) =>
    words
      .split('|')
      .map(
        w =>
          `[${w[0].toUpperCase()}${w[0]}]${w.slice(1).replace(/ /g, '\\s+')}`,
      )
      .join('|');
  const FULL = `(${NAME_WORD}(?:-${NAME_WORD})?)[^\\S\\n\\t]+((?:${NAME_WORD}(?:-${NAME_WORD})?[^\\S\\n\\t]+)?${NAME_WORD}(?:-${NAME_WORD})?)`;
  // A full name at the start of a line or table cell, followed by a role, a
  // bracket or the next cell: "Ksenia Abramovich (CEO)\tCommon", "Gareth Moxon,
  // PCV driver", "| Suda Wongsakul |". Also after a sentence ends:
  // "15:30-16:50. Ansel Corrigan (HR manager) sat in."; and before a dash, a
  // phone number or a quoted nickname: "Geneviève Courtemanche - Gen",
  // "Babatunde Olawale, 343-555-0108".
  for (const m of text.matchAll(
    new RegExp(
      `(?<=^|\\n|\\t|\\||:|[.!?;][^\\S\\n])[^\\S\\n]*${FULL}(?=[^\\S\\n]*\\((?:${ROLE_AFTER}|[A-Z]{2,5}|\\p{Ll}[^)\\n]{0,30}|["“'‘][^)\\n]{1,20})\\)|,[^\\S\\n]*(?:\\p{Ll}|[+(]?\\d{3}|(?:[\\p{L}-]+[^\\S\\n]){0,3}(?:${ROLE_AFTER}|${ROLE_BEFORE}))|[^\\S\\n]*\\t|[^\\S\\n]*\\||[^\\S\\n]+[-–—][^\\S\\n])`,
      'gmu',
    ),
  )) {
    const words = m[0].trim().split(/\s+/);
    if (words.every(nameLike)) addPerson(m[0]);
  }
  // A full name filling a labelled line: "Also present:   Zbigniew Wawrzyniak",
  // "De : Marie-Ève Dandurand", "**Client:** Bronislava Havlicek (". Every word
  // must be a name, so "Subject: Annual Review" is skipped.
  for (const m of text.matchAll(
    new RegExp(
      `(?:^|\\n)[^\\S\\n]*[*_]{0,2}\\p{L}[\\p{L} ./-]{0,30}?[^\\S\\n]?:[*_]{0,2}[^\\S\\n]*${FULL}(?=[^\\S\\n]*(?:\\n|$|[,(;]|[-–—][^\\S\\n]))`,
      'gu',
    ),
  )) {
    if ([m[1], ...m[2].split(/\s+/)].every(nameLike)) {
      addPerson(`${m[1]} ${m[2]}`);
    }
  }
  // A full name in brackets: "Ahluwalia Valuation Advisors (Sandeep
  // Ahluwalia)", "(Suda Wongsakul)"
  for (const m of text.matchAll(new RegExp(`\\(${FULL}\\)`, 'gu'))) {
    if ([m[1], ...m[2].split(/\s+/)].every(nameLike)) {
      addPerson(`${m[1]} ${m[2]}`);
    }
  }
  // A full name alone on the line after a sign-off: "Merci,\nMarie-Ève
  // Dandurand"
  for (const m of text.matchAll(
    new RegExp(
      `(?:${ci('thanks|thank you|regards|cheers|best|sincerely|yours|respectfully|cordially|merci|cordialement|salutations|gracias|saludos|atentamente|danke|grüße|groeten|met vriendelijke groet')})[^\\n]{0,24}\\n[^\\S\\n]*${FULL}[^\\S\\n]*(?=,|\\n|$)`,
      'gu',
    ),
  )) {
    if ([m[1], ...m[2].split(/\s+/)].every(nameLike)) {
      addPerson(`${m[1]} ${m[2]}`);
    }
  }
  // Whose passport, login or date of birth: "Anjali's passport no.", "Ksenia's
  // login"
  for (const m of text.matchAll(
    new RegExp(
      `(?<![\\p{L}'’-])(${NAME_WORD}(?:-${NAME_WORD})?)['’]s\\s+(?:passport|date\\s+of\\s+birth|DOB|SSN|SIN|NI\\s+number|licen[cs]e|login|password|phone|cell|mobile|email|address|visa|permit|birthday|wife|husband|son|daughter|mother|father|mom|mum|dad|sister|brother|partner|fianc[ée]e?|boss|doctor|lawyer|attorney|salary|wages|income|diagnosis|meds|medication|appointment|signature|ID|insurance|bank|account|tax|return|kids|children|parents|ex)\\b`,
      'gu',
    ),
  )) {
    if (nameLike(m[1])) people.add(m[1]);
  }
  // Addressed or acted on as a person: "Ask Shirin", "Approved by Priyanka",
  // "report to Ansel by"
  for (const m of text.matchAll(
    new RegExp(
      `\\b(?:${ci('ask|asked|tell|told|remind|reminded|thank|thanked|ping|cc|email|emailed|call|called|text|texted|inform|informed|notify|copy|message|approved by|signed by|reviewed by|prepared by|sent by|report to|reports to|send it to|send this to|send them to|forward it to|forward this to|on behalf of|guarantee from')})\\s+(${NAME_WORD}(?:-${NAME_WORD})?)(?![\\p{L}'’-]|\\s+${NAME_WORD})`,
      'gu',
    ),
  )) {
    if (nameLike(m[1])) people.add(m[1]);
  }
  // Acts only a person does: "Hamza also owes", "Hollis dials in", "Bree is
  // nervous. She"
  for (const m of text.matchAll(
    new RegExp(
      `(?<![\\p{L}'’-])(${NAME_WORD}(?:-${NAME_WORD})?)\\s+(?:(?:also|still|never|only|just)\\s+)?(?:says|said|told|asked|wants|wanted|refused|agreed|knows|knew|thinks|thought|prefers|preferred|interprets|owes|owed|dials|dialed|dialled|emailed|texted|wrote|signed|denies|denied|admits|admitted|confirmed|mentioned|claims|claimed|lives|lived|moved|feels|felt|hopes|hoped|remembers|recalls|recalled|disputes|disputed|insists|insisted|apologi[sz]ed|resigned|retired|takes|took|uses|used|pays|paid|has\\s+paid|challenges|challenged|pre-approved|sat\\s+in|will\\s+(?:call|drive|step|sign|send|come|stay|bring|pay|attend|testify|move)|would\\s+rather|to\\s+stay\\s+home|was\\s+born|is\\s+(?:nervous|upset|worried|pregnant|expecting|married|divorced|separated|unemployed|retired|recovering|grieving|anxious|afraid|scared|on\\s+(?:leave|an?\\s+\\S+\\s+visa)))\\b`,
      'gu',
    ),
  )) {
    if (nameLike(m[1])) people.add(m[1]);
  }
  // A name with an age or a birth: "Wren, born 2014", "Josué, age 6", "Dariel
  // Zelaya, 9 años"
  for (const m of text.matchAll(
    new RegExp(
      `(?<![\\p{L}'’-])(${NAME_WORD}(?:-${NAME_WORD})?)(?:[^\\S\\n]+(${NAME_WORD}(?:-${NAME_WORD})?))?(?=,?[^\\S\\n]*\\(?(?:(?:born|aged?|DOB|née?)\\b|b\\.\\s|\\d{1,2}\\s*(?:years?\\s+old|yrs?|y\\/o|años|ans|Jahre)\\b))`,
      'gu',
    ),
  )) {
    const words = [m[1], ...(m[2] ? [m[2]] : [])];
    if (words.every(nameLike)) addPerson(words.join(' '));
  }
  // A name as the label of its own line, followed by a phone number or an email
  // address: "Jürgen: 0171 5550 188", "Rosemarie: 912.555.0189". Headings
  // ("Fee: $250") need the contact cue.
  for (const m of text.matchAll(
    new RegExp(
      `(?:^|\\n)[^\\S\\n]*(${NAME_WORD}(?:-${NAME_WORD})?)[^\\S\\n]*:[^\\S\\n]*(?=[+(]?\\d[\\d\\s().-]{6,}\\d|[\\w.+-]+@[\\w-]+\\.)`,
      'gu',
    ),
  )) {
    if (
      nameLike(m[1]) &&
      !new RegExp(`^(?:${FIELD_LABEL})$`, 'i').test(m[1]) &&
      !/^(?:tel|tél|fax|phone|telephone|téléphone|teléfono|telefon|mobile|cell|handy|portable|móvil|celular|office|home|work|main|direct|whatsapp|signal|pager|ext|toll|support|sales|billing|reception|desk|line|landline|hotline|contact|email|e-mail|mail|courriel|correo|account|acct|routing|iban|swift|bic|card|ref|reference|case|file|claim|policy|invoice|order|ticket|amount|total|balance|fee|fees|date|dob|ssn|sin|ein|tin|vat|abn|license|licence|passport|permit|id|no|number)$/i.test(
        m[1],
      )
    ) {
      people.add(m[1]);
    }
  }
  // Something that belongs to someone: "Harper's share", "Efraín's cousin",
  // "Ottilie's long-term care"
  for (const m of text.matchAll(
    new RegExp(
      `(?<![\\p{L}'’-])(${NAME_WORD}(?:-${NAME_WORD})?)['’]s[^\\S\\n]+(?=\\p{Ll})`,
      'gu',
    ),
  )) {
    if (nameLike(m[1])) people.add(m[1]);
  }
  // Greeting someone in another language: "Bonjour Marie-Ève,", "Hola
  // Yorleny,", "Liebe Aylin,"
  for (const m of text.matchAll(
    new RegExp(
      `(?:^|\\n)[^\\S\\n>]*(?:Bonjour|Bonsoir|Salut|Chère|Cher|Hola|Querid[ao]|Estimad[ao]|Hallo|Liebe|Lieber|Beste|Ciao|Olá|Caro|Cara)[^\\S\\n]+(${NAME_WORD}(?:-${NAME_WORD})?)\\s*[,:!]`,
      'gu',
    ),
  )) {
    if (nameLike(m[1])) people.add(m[1]);
  }
  // Initials used as a person. Agencies and common acronyms are excluded on top
  // of NOT_INITIALS.
  const AGENCY =
    /^(?:HMRC|CRA|DOJ|DOL|EEOC|OSHA|HUD|FTC|SEC|FDA|CDC|NHS|GP|DMV|DVLA|ICE|USCIS|IRCC|CBSA|ATO|ESA|EI|CPP|OAS|WCB|WSIB|TSA|FEMA|NLRB|EPA|ER|ED|OT|PT|ME|AG|DOT|CHP|LAPD|NYPD|RCMP|OPP|FBI|DEA|ATF|DHS|SSA|VA|IRS|EDD|UI|AP|AR|GL|CPA|CFO|CEO|HR|IT|QA|PM|PMO|BA)$/;
  const initials = (s: string) => !NOT_INITIALS.has(s.replace(/\./g, ''));
  // A message signed with initials: "ring him Fri 14th.   BK", "good luck -
  // T.", "\n\nR."
  for (const m of text.matchAll(
    /(?:\n|[^\S\n]{2,}|[^\S\n][-–—][^\S\n]?)((?:[A-Z]\.){1,3}|[A-Z]\.[A-Z]-[A-Z]\.|[A-Z]{2,3})[^\S\n]*(?=\n\s*\n|\s*$)/g,
  )) {
    if (initials(m[1])) people.add(m[1]);
  }
  // Initials that speak or act: "GM said the ban was 12 months", "SA
  // confirmed", "HW attending", "RS: agree?"
  for (const m of text.matchAll(
    /(?<![\p{L}\p{N}.])([A-Z]{2,3})(?:['’]s)?(?=\s+(?:said|says|confirmed|accepted|agreed|denied|admitted|stated|explained|asked|referred|attending|attended|called|emailed|reported|noted|declined|refused)\b|:\s+(?:agree|ok|please|can|could|thoughts|fyi)\b)/gu,
  )) {
    if (initials(m[1]) && !AGENCY.test(m[1])) people.add(m[1]);
  }
  // Initials in brackets after a name or as a note's author: "Honor Wilmot
  // (HW)", "Staff note (AO, 11/8)"
  for (const m of text.matchAll(
    /(?:\p{Ll}|note|notes|by)[^\S\n]*\(([A-Z]{2,3})(?:,[^)\n]{0,20})?\)/gu,
  )) {
    if (initials(m[1]) && !AGENCY.test(m[1])) people.add(m[1]);
  }
  // A name in capitals after a label or between parties: "Claimant: TSEHAY
  // WOLDEMICHAEL", "Para: REYNA ISABEL CIFUENTES DE LEÓN", "and PRESTON ELLERY
  // CALDECOTT III ("
  const CAPS_WORD = "\\p{Lu}[\\p{Lu}'’-]+";
  const CAPS_NAME = `(${CAPS_WORD}(?:[^\\S\\n]+(?:\\p{Lu}\\.?|DE|DEL|DA|DOS|LA|VAN|VON|DER|${CAPS_WORD})){1,4})`;
  for (const m of text.matchAll(
    new RegExp(
      `(?:(?:^|\\n)[^\\S\\n]*[*_]{0,2}\\p{L}[\\p{L} ./-]{0,30}?[^\\S\\n]?:[*_]{0,2}[^\\S\\n]*|\\band[^\\S\\n]+)${CAPS_NAME}(?=[^\\S\\n]*(?:\\n|$|[,(;]|[^\\S\\n]{2,}|and\\b))`,
      'gu',
    ),
  )) {
    const words = m[1]
      .split(/\s+/)
      .filter(
        w =>
          w.length > 2 &&
          !/^(?:DE|DEL|DOS|VAN|VON|DER|II|III|IV|JR|SR)$/.test(w),
      );
    if (
      words.length &&
      words.every(
        w =>
          !GENERIC_CAPS.has(w) &&
          !new RegExp(`^(?:${CAPS_END})$`).test(w) &&
          nameLike(w[0] + w.slice(1).toLowerCase()),
      )
    ) {
      addPerson(m[1].replace(/[^\S\n]+(?:II|III|IV|JR|SR)$/, ''));
    }
  }
  // "Surname, First" at the start of a line, cell or label: "Reyes, Marisol",
  // "Okafor, Daniel J.", "Patient:\tVan Der Berg, Anneke". Both parts must be
  // names, so "Seattle, Washington" style pairs of ordinary or place words are
  // rare here; a wrong pair is still removed, not exposed.
  for (const m of text.matchAll(
    new RegExp(
      `(?<=^|\\n|\\t|\\||:)[^\\S\\n]*((?:(?:Van|Von|De|Del|Da|Di|Le|La|Mac|Mc|O['’])[^\\S\\n]*)?${NAME_WORD}(?:-${NAME_WORD})?),[^\\S\\n]*(${NAME_WORD}(?:-${NAME_WORD})?)(?:[^\\S\\n]+\\p{Lu}\\.?)?(?=[^\\S\\n]*(?:\\n|$|[\\t|(;]|,[^\\S\\n]*(?:\\d|\\p{Ll}|DOB|SSN|MRN|#)|[^\\S\\n]{2,}))`,
      'gu',
    ),
  )) {
    const surname = m[1].split(/\s+/).at(-1)!;
    const initialFollows =
      /^[^\S\n]+\p{Lu}\.?(?![\p{L}])/u.test(
        text.slice(m.index! + m[0].length - 3, m.index! + m[0].length + 3),
      ) || /\s\p{Lu}\.?$/u.test(m[0]);
    if (
      nameLike(surname) &&
      nameLike(m[2]) &&
      (GIVEN_NAMES.has(key(m[2])) || initialFollows)
    ) {
      addPerson(`${m[2]} ${m[1]}`);
    }
  }
  // Greeting two people: "Dear Dafydd and Anjali,"
  for (const m of text.matchAll(
    new RegExp(
      `(?:^|\\n)[^\\S\\n>]*(?:Hi|Hello|Hey|Dear|Bonjour|Hola|Hallo)\\s+(${NAME_WORD}(?:-${NAME_WORD})?)\\s+(?:and|&|et|y|und)\\s+(${NAME_WORD}(?:-${NAME_WORD})?)\\s*[,:!]`,
      'gu',
    ),
  )) {
    for (const w of [m[1], m[2]]) if (nameLike(w)) people.add(w);
  }
  // A salutation line: "Steph," or "Hi Ravi,"
  for (const m of text.matchAll(
    /(?:^|\n)[^\S\n>]*(?:(?:Hi|Hello|Hey|Dear|Good\s+(?:morning|afternoon|evening))\s+)?(\p{Lu}\p{Ll}+(?:-\p{Lu}\p{Ll}+)?)\s*[,:—-]\s*(?=\n)/gu,
  )) {
    if (
      !ORDINARY.has(key(m[1])) &&
      !NOT_A_NAME.has(key(m[1])) &&
      !SIGN_OFFS.has(key(m[1]))
    ) {
      people.add(m[1]);
    }
  }
  // A sign-off: "thanks\nlola", "Regards, Priya"
  for (const m of text.matchAll(
    /\b(?:thanks|thank\s+you|thx|regards|cheers|best|sincerely|yours|respectfully|cordially|warmly|talk\s+soon)[,!.]?[^\S\n]*\n?[^\S\n]*(\p{L}{3,14})[^\S\n]*(?=\n|$)/giu,
  )) {
    if (
      !ORDINARY.has(key(m[1])) &&
      !NOT_A_NAME.has(key(m[1])) &&
      !SIGN_OFFS.has(key(m[1]))
    ) {
      people.add(m[1]);
    }
  }
  // Initials with full stops used as a name: "T.J. will drive"
  for (const m of text.matchAll(/(?<![\p{L}.])([A-Z]\.[A-Z]\.)(?![\p{L}])/gu)) {
    if (
      !/^(?:U\.S|U\.K|D\.C|P\.O|P\.C|N\.A|L\.P|P\.A|E\.U|S\.A|A\.M|P\.M|M\.D|J\.D|R\.N|D\.O|N\.Y|L\.A|N\.J|N\.H|N\.M|N\.C|N\.D|S\.C|S\.D|W\.V|R\.I|B\.C|I\.D|V\.P|H\.R|I\.T|Q\.C|K\.C|N\.W|N\.E|S\.W|S\.E|P\.S|R\.E|C\.C|A\.D|B\.A|B\.S|M\.A|M\.S)\.$/.test(
        m[1],
      )
    ) {
      people.add(m[1]);
    }
  }
  // "University of Regina", "Diocese of Lafayette"
  for (const m of text.matchAll(
    /\b(?:University|Diocese|Archdiocese|Church|Hospital|Sisters|Society|Bank)\sof\s(?:the\s)?\p{Lu}[\p{L}'’-]+(?:\s\p{Lu}[\p{L}'’-]+)?/gu,
  )) {
    companies.add(collapse(m[0]));
  }
  // A home called by the family's name: "Hartung residence", "the Cho
  // household"
  for (const m of text.matchAll(
    new RegExp(
      `(?<![\\p{L}'’-])(${NAME_WORD})(?=\\s(?:residence|household)\\b)`,
      'gu',
    ),
  )) {
    if (
      !ORDINARY.has(key(m[1])) &&
      !NOT_A_NAME.has(key(m[1])) &&
      !NOT_A_HOME.has(key(m[1]))
    ) {
      people.add(m[1]);
    }
  }
  // Campaign committees: "Friends of Varga for County Commissioner"
  for (const m of text.matchAll(
    /\b(?:Friends of|Citizens for|People for|Neighbors for|Committee to (?:Re-?[Ee]lect|Elect))\s(?:\p{Lu}[\p{L}'’.-]*\s){1,3}for\s\p{Lu}\p{L}+(?:\s\p{Lu}\p{L}+){0,2}/gu,
  )) {
    companies.add(collapse(m[0]));
  }
  // Union locals: "Local 1408"
  for (const m of text.matchAll(/\bLocal\s+(?:No\.\s*)?\d{1,5}\b/g)) {
    companies.add(collapse(m[0]));
  }
  // Firms named for their partners: "Pellegrino & Yoo", "Whitlock-Tan &
  // Associates, CPAs"
  for (const m of text.matchAll(
    /(?<![\p{L}'’-])((?:\p{Lu}[\p{L}'’-]+ [A-Z][\p{L}'’-]+|[A-Z][\p{L}'’-]+(?:,\s[A-Z][\p{L}'’-]+){0,2})\s&\s[A-Z][\p{L}'’-]+(?:\s[A-Z][\p{L}'’-]+)?)/gu,
  )) {
    // Capitalization and an ampersand alone are insufficient inside an explicit
    // control label. Skip this occurrence before creating company aliases. A
    // real company occurrence elsewhere, another name cue or model evidence
    // still wins.
    const labelEnd = m.index + m[0].replace(/['’]$/, '').length;
    if (
      !COMPANY_SUFFIX.test(m[1]) &&
      controlLabels.some(
        ([start, end]) => start === m.index && end === labelEnd,
      )
    ) {
      continue;
    }
    const parts = collapse(m[1])
      .split(/[\s,&]+/)
      .filter(Boolean);
    // An abbreviated ending keeps its full stop: "Coastal Title & Escrow Co."
    const stop =
      /(?:Co|Inc|Corp|Ltd|Bros)$/.test(m[1]) &&
      text[m.index + m[0].length] === '.'
        ? '.'
        : '';
    if (!parts.every(w => GENERIC_CAPS.has(w.toUpperCase()) || plainWord(w))) {
      companies.add(collapse(m[1]) + stop);
    }
  }
  return {people: [...people], companies: [...companies], links};
}

/**
 * Turn names into search candidates, adding the other ways each one gets
 * written. Variants of one name share an entity, so they share a placeholder.
 */
export function nameCandidates(
  names: Names,
  ordinary: ReadonlySet<string> = new Set(),
): Candidate[] {
  const out: Candidate[] = [];
  const seen = new Set<string>();
  const add = (c: Candidate) => {
    const text = collapse(c.text);
    const k = `${c.kind}:${text}`; // case-sensitive: "Mari" and "MARI" are both kept
    if (text.length < 2 || seen.has(k)) return;
    seen.add(k);
    out.push({...c, text});
  };

  const everyone = [
    ...new Set(
      names.people
        .map(n => collapse(n).replace(/^the\s+/i, ''))
        .filter(Boolean),
    ),
  ].filter(
    n =>
      !NOT_A_NAME.has(key(n.split(' ')[0])) &&
      !isAbbreviation(n) &&
      !HONORIFIC.test(n),
  );
  // An organization's name starts with a capital letter or a digit.
  names = {
    ...names,
    companies: names.companies.filter(
      c =>
        (/^[\p{Lu}\d]/u.test(c.trim()) || c.trim().split(/\s+/).length >= 2) &&
        !/['’]s$/.test(c.trim()),
    ),
  };
  const companies = [...new Set(names.companies.map(collapse).filter(Boolean))];
  // "Dana K. Lindqvist" and "Dana Lindqvist" are one person: group by given
  // name and surname, and call the group by its longest form.
  const plainIdentity = (n: string) => {
    const p = personParts(n);
    return p.given.length ? key(`${p.given[0]} ${p.surname}`) : key(n);
  };
  // "W. Pike" is the same person as "Wendell Pike" when only one known person
  // fits.
  const fullForms = everyone
    .map(personParts)
    .filter(p => p.given.length && !/^\p{L}\.?$/u.test(p.given[0]));
  const identity = (n: string) => {
    const p = personParts(n);
    if (p.given.length && /^\p{L}\.?$/u.test(p.given[0])) {
      const fits = [
        ...new Set(
          fullForms
            .filter(
              f =>
                key(f.surname) === key(p.surname) &&
                key(f.given[0][0]) === key(p.given[0][0]),
            )
            .map(f => key(`${f.given[0]} ${f.surname}`)),
        ),
      ];
      if (fits.length === 1) return fits[0];
    }
    return plainIdentity(n);
  };
  const groups = new Map<string, string[]>();
  for (const n of everyone) {
    groups.set(identity(n), [...(groups.get(identity(n)) ?? []), n]);
  }
  const canonicalOf = new Map<string, string>();
  for (const forms of groups.values()) {
    const longest = [...forms].sort((a, b) => b.length - a.length)[0];
    for (const f of forms) canonicalOf.set(f, longest);
  }
  const people = everyone;
  const parsed = people.map(personParts);
  const count = (
    pick: (p: ReturnType<typeof personParts>) => string | undefined,
  ) => {
    const m = new Map<string, Set<string>>();
    people.forEach((n, i) => {
      const v = pick(parsed[i]);
      if (v) m.set(key(v), (m.get(key(v)) ?? new Set()).add(identity(n)));
    });
    return new Map([...m].map(([k, v]) => [k, v.size]));
  };
  const surnames = count(p => (p.tokens.length > 1 ? p.last : undefined));
  const firsts = count(p => (p.tokens.length > 1 ? p.given[0] : undefined));
  const personWords = new Set(parsed.flatMap(p => p.tokens).map(key));
  const entityOf = (full: string) => `person:${identity(full)}`;

  people.forEach((full, i) => {
    const p = parsed[i];
    if (p.tokens.length < 2 || !p.given.length) return;
    const entity = entityOf(full);
    const short = (text: string) =>
      add({
        text,
        kind: 'person',
        entity,
        canonical: canonicalOf.get(full) ?? full,
        source: 'short-form',
      });
    const first = p.given[0];
    const middles = p.given.slice(1);
    const isInitial = (t: string) => /^\p{L}\.?$/u.test(t);
    const plain = p.tokens.join(' ');
    const noMiddle = `${first} ${p.surname}`;
    const both = (s: string) => {
      short(s);
      if (unaccent(s) !== s) short(unaccent(s));
    };

    if (plain !== full) both(plain);
    if (noMiddle !== full) both(noMiddle);
    if (/^\p{L}/u.test(first)) {
      const fi = first[0];
      const mi = middles.map(m => m[0]);
      for (const sur of new Set([p.surname, p.last])) {
        both(`${fi}. ${sur}`);
        both(`${fi} ${sur}`);
        if (mi.length) {
          both(`${fi}.${mi.join('.')}. ${sur}`);
          both(`${fi}. ${mi.join('. ')}. ${sur}`);
          both(`${fi}${mi.join('')} ${sur}`);
        }
      }
      // "Last, First" and "LAST, First M." as written in forms, tables and
      // captions
      const rest = [first, ...middles].join(' ');
      for (const sur of new Set([p.surname, upper(p.surname)])) {
        both(`${sur}, ${rest}`);
        both(`${sur}, ${first}`);
        if (middles.length) {
          both(`${sur}, ${first} ${middles.map(m => m[0] + '.').join(' ')}`);
        }
      }
      both(upper(`${p.surname}, ${rest}`));
      both(upper(`${p.surname}, ${first}`));
      both(upper(plain));
      both(upper(noMiddle));
      if (p.suffix) {
        both(upper(`${plain} ${p.suffix}`));
        both(upper(`${p.surname}, ${rest} ${p.suffix}`));
      }
      // Initials, as used in file notes ("DKL", "D.K.L.", "DL")
      const letters = [fi, ...mi, ...p.last.split(/[-\s]/).map(w => w[0])].map(
        upper,
      );
      const forms = new Set([letters.join(''), upper(fi + p.last[0])]);
      for (const f of forms) {
        if (f.length >= 2 && !NOT_INITIALS.has(f)) {
          short(f);
          short(f.split('').join('.') + '.');
        }
      }
    }
    // A shared surname or first name is ambiguous, so it is left for the user
    // to mark.
    if (
      p.last.length >= 3 &&
      surnames.get(key(p.last)) === 1 &&
      !GENERIC_LAST.has(key(p.last))
    ) {
      both(p.last);
      if (p.particles.length) both(p.surname);
      both(upper(p.last));
    }
    if (
      first.length >= 3 &&
      firsts.get(key(first)) === 1 &&
      !isInitial(first) &&
      /^\p{Lu}/u.test(first) &&
      !NOT_A_NAME.has(key(first))
    ) {
      both(first);
      // In capitals in a note: "(PAZ -- SHRED THIS PAGE)". Not for names that
      // are also words or codes.
      if (
        !ORDINARY.has(key(first)) &&
        !AMBIGUOUS_NAMES.has(key(first)) &&
        !NOT_INITIALS.has(upper(first))
      ) {
        short(upper(first));
      }
      // Notes typed in a hurry: "callum works 6 days". Only for names that are
      // not also ordinary words.
      if (first.length >= 4 && GIVEN_NAMES.has(key(first))) {
        short(first.toLocaleLowerCase('en-US'));
        if (first.length >= 5) short(`${first.toLocaleLowerCase('en-US')}s`);
      }
    }
  });

  for (const full of companies) {
    const entity = `company:${key(full)}`;
    const short = (text: string) =>
      add({
        text,
        kind: 'company',
        entity,
        canonical: full,
        source: 'short-form',
      });
    let base = full.replace(/^the\s+/i, '');
    while (COMPANY_SUFFIX.test(base)) base = base.replace(COMPANY_SUFFIX, '');
    base = base.replace(/[,\s]+$/, '');
    // The name without its legal ending, unless what is left is one ordinary
    // word ("trust" from "trust company").
    const bareWord =
      !base.includes(' ') &&
      (!/^\p{Lu}/u.test(base) ||
        ordinary.has(key(base)) ||
        ORG_END_ONLY.test(base) ||
        INSTITUTION.has(key(base)));
    if (base !== full && !bareWord) short(base);
    short(upper(full));
    if (!bareWord) short(upper(base));
    const baseWords = base.split(' ');
    // Typed in a hurry, all in lower case: "sokolov auto glass"
    if (baseWords.length >= 2) short(base.toLocaleLowerCase('en-US'));
    // A word cut short: "Marsh Vet" for Marsh Veterinary Clinic, "Sellwood
    // Animal Hosp." for ... Hospital
    for (let n = 1; n < baseWords.length; n++) {
      const word = baseWords[n];
      if (!/^\p{Lu}\p{Ll}{5,}$/u.test(word)) continue;
      const lead = baseWords.slice(0, n).join(' ');
      for (const cut of [3, 4, 5]) {
        short(`${lead} ${word.slice(0, cut)}`);
        short(`${lead} ${word.slice(0, cut)}.`);
      }
    }
    // An institution referred to by what it is: "the Authority" for the ...
    // Transit Authority
    const lastWord = baseWords[baseWords.length - 1];
    if (baseWords.length >= 2 && INSTITUTION.has(key(lastWord))) {
      short(`the ${lastWord}`);
      short(`The ${lastWord}`);
    }
    // "F&D" for Ferreira & Daughters Seafood
    const amp = baseWords.indexOf('&');
    if (amp > 0 && baseWords[amp + 1]) {
      short(`${baseWords[amp - 1][0]}&${baseWords[amp + 1][0]}`);
      short(`${baseWords[amp - 1][0]} & ${baseWords[amp + 1][0]}`);
    }
    const words = base.split(' ');
    // Leading parts of the name, two words or more: "Blue Heron" for "Blue
    // Heron Veterinary Clinic"
    for (let n = words.length - 1; n >= 2; n--) {
      if (/^(?:of|and|the|for|de|du|&)$/i.test(words[n - 1])) continue;
      short(words.slice(0, n).join(' '));
    }
    const first = words[0];
    if (
      words.length > 1 &&
      first.length >= 5 &&
      /^\p{Lu}/u.test(first) &&
      !GENERIC_FIRST.has(key(first)) &&
      !personWords.has(key(first)) &&
      !ordinary.has(key(first)) &&
      !ORDINARY.has(key(first))
    ) {
      short(first);
    }
    // Acronym: "LSTCU" for "Lone Star Teachers Credit Union"
    const caps = words.filter(
      w => /^\p{Lu}/u.test(w) && !/^(?:of|and|the|for)$/i.test(w),
    );
    const acronym = caps.map(w => w[0]).join('');
    if (caps.length >= 3 && !NOT_INITIALS.has(acronym)) short(acronym);
    const fullCaps = full
      .replace(/^the\s+/i, '')
      .split(' ')
      .filter(w => /^\p{Lu}/u.test(w));
    const fullAcronym = fullCaps.map(w => w[0]).join('');
    if (
      fullCaps.length >= 3 &&
      fullAcronym !== acronym &&
      !NOT_INITIALS.has(fullAcronym)
    ) {
      short(fullAcronym);
    }
  }
  // Full names go in last. A short form that was also returned on its own
  // ("Harbourline" next to "Harbourline Marine Supply") is already linked above
  // and is skipped here, so both forms share one placeholder.
  for (const full of people) {
    add({
      text: full,
      kind: 'person',
      entity: entityOf(full),
      canonical: canonicalOf.get(full) ?? full,
      source: 'model',
    });
  }
  for (const full of companies) {
    add({
      text: full,
      kind: 'company',
      entity: `company:${key(full)}`,
      canonical: full,
      source: 'model',
    });
  }
  return out;
}

/**
 * Text right after a matched name that belongs to it: "Jr.", ", Esq.", ",
 * P.C.", ", LLC".
 */
export function trailingSuffix(
  text: string,
  end: number,
  kind: 'person' | 'company',
): number {
  const rest = text.slice(end, end + 24);
  const m =
    kind === 'person'
      ? (/^,?\s(?:Jr|Sr|JR|SR|II|III|IV|Esq|ESQ|M\.D|MD|D\.O|DO|RN|NP|PA-C|Ph\.D|PhD|CPA|J\.D|JD|DDS|DMD|EA|LCSW|RPR|P\.E)\b\.?(?:,\s(?:M\.D|MD|RN|Ph\.D|PhD|CPA|J\.D|JD|EA|Esq)\b\.?)?/.exec(
          rest,
        ) ?? /^,\s\p{Lu}\.(?!\s?\p{Lu}[\p{Ll}.])/u.exec(rest))
      : (/^,?\s(?:Inc|Incorporated|LLC|L\.L\.C|LLP|L\.L\.P|LP|PLLC|P\.L\.L\.C|P\.L\.C|P\.C|PC|P\.A|S\.C|Ltd|Limited|Corp|Corporation|Co|PLC|GmbH|N\.A|B\.V|N\.V|inc|ltée|mbB|Pty Ltd|plc|DAC)\b\.?/.exec(
          rest,
        ) ??
        /^(?:,?\s(?:Attorneys|Counselors|Counsellors))?\sat\sLaw\b/.exec(
          rest,
        ) ??
        // ", PA" and ", SC" are professional corporations here, unless a ZIP
        // code follows
        /^,\s(?:PA|SC|PC)\b(?!\.?,?\s+\d{5})/.exec(rest) ??
        /^,\s(?!(?:AL|AK|AZ|AR|CA|CO|CT|DE|DC|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|AB|BC|MB|NB|NL|NS|ON|PE|QC|SK)\b)[A-Z]{2,5}s?\b\.?/.exec(
          rest,
        ));
  return m ? end + m[0].length : end;
}

/**
 * Short names a document defines for a party: Brightwater Biologics, Inc.
 * ("Brightwater"). Returns each defined term with the position of its opening
 * bracket.
 */
export function definedTerms(text: string): Array<{term: string; at: number}> {
  const out: Array<{term: string; at: number}> = [];
  const re =
    /\(\s*(?:hereinafter,?\s+|each,?\s+an?\s+|collectively,?\s+|together,?\s+|individually,?\s+)?(?:the\s+)?["“]([^"”\n]{2,40})["”](?:\s+or\s+(?:the\s+)?["“]([^"”\n]{2,40})["”])?\s*\)/g;
  for (const m of text.matchAll(re)) {
    for (const term of [m[1], m[2]]) {
      if (term && /\p{Lu}/u.test(term)) {
        out.push({term: collapse(term), at: m.index});
      }
    }
  }
  // Without quotation marks: (the Authority), (hereinafter Brightwater), (F&D),
  // (LSTCU)
  for (const m of text.matchAll(
    /\(\s*(?:(?:the|hereinafter|hereafter)\s+(\p{Lu}[\p{L}&'’-]*(?:\s\p{Lu}[\p{L}&'’-]*){0,2})|(\p{Lu}[\p{Lu}&]{1,6}))\s*\)/gu,
  )) {
    out.push({term: collapse(m[1] ?? m[2]), at: m.index});
  }
  return out;
}
