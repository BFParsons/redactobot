/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Pattern detectors: the instant, deterministic checks. Each
 * detector has one or more rules (a regular expression plus an optional
 * validity check). Order matters: an earlier detector claims its text first, so
 * a later, more general one cannot split it.
 *
 * Design notes from the evaluation (evaluation/RESULTS.md):
 * - Real documents rarely label numbers the way a pattern author expects, so alongside the
 *   labelled rules there are general ones for "looks like an ID code" and "long number".
 * - Over-catching is cheap here (the user can untick, and values are restored afterwards);
 *   missing something is not. Rules lean toward catching.
 */

// ---------- validators ----------
const digits = s => s.replace(/\D/g, '');

/**
 * Checks the digits of a string against the Luhn checksum.
 * @param {string} s The value; everything but its digits is ignored.
 * @return {boolean} True when there is at least one digit and the checksum
 *     holds.
 */
export function luhn(s) {
  const d = digits(s);
  let sum = 0;
  for (let i = d.length - 1, alt = false; i >= 0; i--, alt = !alt) {
    let n = +d[i];
    if (alt) {
      n *= 2;
      if (n > 9) n -= 9;
    }
    sum += n;
  }
  return d.length > 0 && sum % 10 === 0;
}
/**
 * Checks that a string could be an issued US Social Security number: nine
 * digits, area not 000, 666 or 900-999, group not 00, serial not 0000.
 * @param {string} s The value; everything but its digits is ignored.
 * @return {boolean} True when the number passes every check.
 */
export function validSsn(s) {
  const d = digits(s);
  if (d.length !== 9) return false;
  return (
    d.slice(0, 3) !== '000' &&
    d.slice(0, 3) !== '666' &&
    d[0] !== '9' &&
    d.slice(3, 5) !== '00' &&
    d.slice(5) !== '0000'
  );
}
/**
 * Checks that a string could be a Canadian Social Insurance Number: nine
 * digits, not starting with 0 or 8, that pass the Luhn checksum.
 * @param {string} s The value; everything but its digits is ignored.
 * @return {boolean} True when the number passes every check.
 */
export function validSin(s) {
  const d = digits(s);
  return d.length === 9 && d[0] !== '0' && d[0] !== '8' && luhn(d);
}
/**
 * Checks that a string could be a payment card number: 13 to 19 digits that
 * pass the Luhn checksum.
 * @param {string} s The value; everything but its digits is ignored.
 * @return {boolean} True when the number passes both checks.
 */
export function validCard(s) {
  const d = digits(s);
  return d.length >= 13 && d.length <= 19 && luhn(d);
}
/**
 * Checks an IBAN: 15 to 34 characters once whitespace is removed, with a
 * mod-97 remainder of 1 after the first four characters move to the end and
 * letters become numbers.
 * @param {string} s The value, in either case, made of letters, digits and
 *     whitespace only.
 * @return {boolean} True when the length and the checksum are both valid.
 */
export function validIban(s) {
  const c = s.replace(/\s/g, '').toUpperCase();
  if (c.length < 15 || c.length > 34) return false;
  const moved = c.slice(4) + c.slice(0, 4);
  return (
    BigInt(moved.replace(/[A-Z]/g, ch => String(ch.charCodeAt(0) - 55))) %
      97n ===
    1n
  );
}
/**
 * Checks a US bank routing number: nine digits whose 3-7-1 weighted sum is a
 * multiple of ten.
 * @param {string} s The value; everything but its digits is ignored.
 * @return {boolean} True when the number passes both checks.
 */
export function validRouting(s) {
  const n = [...digits(s)].map(Number);
  return (
    n.length === 9 &&
    (3 * (n[0] + n[3] + n[6]) +
      7 * (n[1] + n[4] + n[7]) +
      (n[2] + n[5] + n[8])) %
      10 ===
      0
  );
}
const hasDigit = s => /\d/.test(s);
const digitCount = s => digits(s).length;
const looksLikeDate = s =>
  /^\d{4}-\d{1,2}-\d{1,2}$/.test(s) ||
  /^\d{1,2}[-/.]\d{1,2}[-/.](?:\d{2}|\d{4})$/.test(s);
const looksLikePhone = s => /^\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}$/.test(s);
// Tax and court form numbers that look like ID codes but are not ("Form
// 1099-NEC", "W-2").
const FORM_ONLY =
  /^(?:10(?:40|41|65|98|99|95)|1120|94[01]|990|70[69]|2848|4868|4506|8\d{3})(?:[-A-Z]{0,5})?$/;
const FORM_NUMBER =
  /^(?:10(?:40|41|65|98|99|95)|1120|94[01]|990|70[69]|2848|8\d{3}|4868|4506|W|K|SS|I|N|G|DS|UCC|CP|LT|ET|SF)\d*[-/]/i;
// Government form families that a label such as "form" or "file" may sit in
// front of.
const FORM_FAMILY = /^(?:CMS-\d+|GST\d+|T\d[A-Z]?|RL-\d+)$/;

// Capitalized words after "in" or "at" that are not places.
const NOT_A_PLACE =
  /^(?:January|February|March|April|May|June|July|August|September|October|November|December|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Q[1-4]|Exhibit|Schedule|Section|Appendix|Attachment|Part|Chapter|Article|Paragraph|Table|Form|Box|Line|Item|Step|Phase|Court|District|Superior|Federal|State|County|Probate|Family|Bankruptcy|Chambers|Excel|QuickBooks|Outlook|Zoom|Teams|English|Spanish|French|God|Medicare|Medicaid|Mr|Mrs|Ms|Dr|I|We|He|She|They|It|This|That|These|Those|My|Our|His|Her|Their|The|A|An)\b/;

// ---------- shared pieces ----------
const MONTH_TITLE =
  'Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?';
// Months as written in Title Case or in ALL CAPS (forms and captions), never in
// lower case ("may").
const MONTH = `(?:${MONTH_TITLE}|${MONTH_TITLE.toUpperCase().replace(/\(\?:/g, '(?:')})`;
const WEEKDAY =
  '(?:(?:Mon|Tue|Tues|Wed|Thu|Thur|Thurs|Fri|Sat|Sun)[a-z]*\\.?,?\\s+)?';
const YEAR = '(?:19|20)\\d{2}';
const DATE_FORMS = [
  `${WEEKDAY}(?:\\bthe\\s+)?\\b\\d{1,2}(?:st|nd|rd|th)\\s+of\\s+${MONTH}(?:,?\\s+${YEAR})?\\b`, // the 13th of October
  `(?:\\bthe\\s+)?\\b\\d{1,2}(?:st|nd|rd|th)\\s+day\\s+of\\s+${MONTH},?\\s+${YEAR}\\b`, // 19th day of February, 2026
  `${WEEKDAY}\\b${MONTH}\\.?\\s+\\d{1,2}(?:st|nd|rd|th)?(?:\\s?[-–]\\s?\\d{1,2}(?:st|nd|rd|th)?|(?:,?\\s+(?:or|and|to|through|thru|&)\\s+\\d{1,2}(?:st|nd|rd|th)?)+)(?:,?\\s+${YEAR})?\\b`, // June 1-4, 2025; November 10 or 12
  `\\b${MONTH}\\.?\\s+\\d{1,2}\\/(?:${YEAR}|\\d{2})\\b`, // Oct 5/26
  `${WEEKDAY}\\b${MONTH}\\.?\\s+\\d{1,2}(?:st|nd|rd|th)?,?\\s+${YEAR}\\b`, // March 14, 2026
  `${WEEKDAY}(?<![\\d.,$£€])\\b\\d{1,2}(?:st|nd|rd|th)?[\\s-]+${MONTH}\\.?,?[\\s-]+${YEAR}\\b`, // 14 March 2026, 14-Apr-2026
  `${WEEKDAY}\\b${MONTH}\\.?[^\\S\\n]+\\d{1,2}(?:st|nd|rd|th)?\\b(?!,?[^\\S\\n]+(?:19|20)\\d{2}\\b)(?![/-]\\d)`, // March 14
  `${WEEKDAY}(?<![\\d.,$£€])\\b\\d{1,2}(?:st|nd|rd|th)?\\s+${MONTH}\\b(?!\\.?,?[^\\S\\n]+(?:19|20)\\d{2}\\b)`, // 14 March
  `\\b${MONTH}\\.?,?\\s+${YEAR}\\b`, // March 2026
  `\\b${YEAR}[-/.](?:0?[1-9]|1[0-2])[-/.](?:0?[1-9]|[12]\\d|3[01])\\b`, // 2026-03-14
  `\\b(?:0?[1-9]|1[0-2])[/.-](?:0?[1-9]|[12]\\d|3[01])[/.-](?:${YEAR}|\\d{2})\\b`, // 03/14/2026
  `\\b(?:0?[1-9]|[12]\\d|3[01])[/.-](?:0?[1-9]|1[0-2])[/.-]${YEAR}\\b`, // 14/03/2026
  `\\b(?:0[1-9]|1[0-2])\\s(?:0[1-9]|[12]\\d|3[01])\\s${YEAR}\\b`, // 03 14 2026
  `(?<![\\d/.-])(?:0?[1-9]|1[0-2])\\/${YEAR}\\b`, // 3/2027
  `\\b(?:Mon|Tues?|Wed(?:nes)?|Thu(?:rs)?|Fri|Sat(?:ur)?|Sun)(?:day)?\\.?,?\\s+the\\s+\\d{1,2}(?:st|nd|rd|th)\\b`, // Friday the 23rd
];
// Dates as written outside the US, and in hurried notes.
const MONTH_INTL =
  '(?:janvier|janv\\.?|février|fevrier|févr\\.?|mars|avril|avr\\.?|mai|juin|juillet|juil\\.?|août|aout|septembre|octobre|novembre|décembre|decembre|déc\\.?|' +
  'enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre|' +
  'januari|februari|maart|mei|juni|juli|augustus|oktober|' +
  'Januar|Februar|März|Juni|Juli|Oktober|Dezember|' +
  'january|february|march|april|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sept?|oct|nov|dec)';
const WEEKDAY_INTL =
  '(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|lunes|martes|miércoles|miercoles|jueves|viernes|sábado|sabado|domingo|maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag)';
const WEEKDAY_ANY =
  '(?:[Mm]on|[Tt]ues?|[Ww]eds?|[Tt]hu(?:rs?)?|[Ff]ri|[Ss]at|[Ss]un|MON|TUES?|WED|THURS?|FRI|SAT|SUN)(?:day|nesday|urday|DAY)?';
const DATE_FORMS_INTL = [
  // 12 novembre 2025, le 14 nov., 1er janvier, mardi 9 décembre, woensdag 3
  // december, 12 nov
  `(?:\\b${WEEKDAY_INTL}\\s+)?(?:\\ble\\s+)?(?<![\\d.,$£€/-])\\b(?:1er|\\d{1,2})\\s+${MONTH_INTL}(?![\\p{L}])\\.?(?:\\s+${YEAR}\\b)?`,
  // 5 de noviembre de 2025, martes 18 de noviembre
  `(?:\\b${WEEKDAY_INTL}\\s+)?(?<![\\d.,$£€/-])\\b\\d{1,2}\\s+de\\s+${MONTH_INTL}(?:\\s+de\\s+${YEAR}\\b)?`,
  // aug 15, nov 3rd (lower case, as typed in notes)
  `\\b(?:jan|feb|mar|apr|jun|jul|aug|sept?|oct|nov|dec)\\.?\\s\\d{1,2}(?:st|nd|rd|th)?\\b(?!\\s?(?:%|:|\\/|\\d))`,
  // sat 2/28, Tues. 11/4, Friday 11/14, Tues 4/11/25
  `\\b${WEEKDAY_ANY}\\.?,?\\s+\\d{1,2}\\/\\d{1,2}(?:\\/(?:\\d{4}|\\d{2}))?\\b`,
  // Weds 12th, Fri 14th, Friday 14th
  `\\b${WEEKDAY_ANY}\\.?,?\\s+\\d{1,2}(?:st|nd|rd|th)\\b`,
  // 29/10/25, 24.11.1980 (day first, two- or four-digit year)
  `(?<![\\d/.-])(?:1[3-9]|2\\d|3[01])[/.](?:0?[1-9]|1[0-2])[/.](?:\\d{4}|\\d{2})\\b`,
  // 30/10 (day first, no year)
  `(?<![\\d/.-])(?:1[3-9]|2\\d|3[01])\\/(?:0?[1-9]|1[0-2])(?![\\d/%])`,
  // the day of the month alone, after a word that makes it a date: "on the
  // 22nd", "docs due by the 20th", "moved to the nineteenth"
  `(?<=\\b(?:on|by|until|till|before|after|from|since|for|to|want|wants|wanted|due|tmrw|tomorrow)\\s)the\\s(?:\\d{1,2}(?:st|nd|rd|th)|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|twenty-(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth)|thirtieth|thirty-first)\\b(?!\\s+(?:floor|quarter|party|amendment|circuit|district|time|day|week|month|year|grade|century|edition|page|paragraph|anniversary|street|avenue|ave|st|of|and|or)\\b)`,
  // Christmas 2022
  `\\b(?:Christmas|Easter|Thanksgiving|Halloween|New Year(?:['’]s)?|Hanukkah|Diwali|Passover|Memorial Day|Labou?r Day)(?:\\s(?:Eve|Day))?\\s${YEAR}\\b`,
];
// A time of day right after a date belongs with it: "10/27/2026 4:52 PM".
const DATE = `(?:(?:${DATE_FORMS.join('|')})(?:,?\\s+(?:at\\s+)?\\d{1,2}:\\d{2}(?::\\d{2})?(?:\\s?[AaPp]\\.?[Mm]\\.?)?)?)`;
// A month on its own after a preposition: "took a loan in May". Only used by
// the any-date check.
const MONTH_ALONE = `(?<=\\b(?:in|during|since|until|till|by|before|after|last|next|this|early|late|mid|of|from|through|for)\\s)(?:${MONTH_TITLE.replace(/Jan\(\?:uary\)\?/, 'January').replace(/\(\?:/g, '(?:')})\\b(?!\\.?,?\\s*\\d)`;
const MONTH_DAY_ONLY =
  '(?<![\\d/.-])(?:0?[1-9]|1[0-2])\\/(?:0?[1-9]|[12]\\d|3[01])(?![\\d/%])';

const STATE_ABBR =
  'AL|AK|AZ|AR|CA|CO|CT|DE|DC|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|PR';
const PROVINCE_ABBR = 'AB|BC|MB|NB|NL|NS|NT|NU|ON|PE|QC|SK|YT';
const STATE_NAME =
  'Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming|District of Columbia|Puerto Rico';
const PROVINCE_NAME =
  'Alberta|British Columbia|Manitoba|New Brunswick|Newfoundland and Labrador|Newfoundland|Nova Scotia|Northwest Territories|Nunavut|Ontario|Prince Edward Island|Quebec|Québec|Saskatchewan|Yukon';
const REGION = `(?:${STATE_ABBR}|${PROVINCE_ABBR}|${STATE_NAME}|${PROVINCE_NAME})`;
// Countries, for "Đà Nẵng, Vietnam": the country can stay, the city before it
// cannot.
const COUNTRY =
  'Mexico|Canada|Vietnam|China|India|Japan|Korea|South Korea|Philippines|Thailand|Indonesia|Malaysia|Singapore|Pakistan|Bangladesh|Nepal|Sri Lanka|Iran|Iraq|Israel|Lebanon|Syria|Turkey|Egypt|Morocco|Nigeria|Ghana|Kenya|Ethiopia|Somalia|South Africa|Brazil|Argentina|Chile|Colombia|Peru|Venezuela|Ecuador|Guatemala|Honduras|El Salvador|Nicaragua|Costa Rica|Panama|Cuba|Haiti|Jamaica|Dominican Republic|England|Scotland|Wales|Ireland|United Kingdom|UK|France|Germany|Italy|Spain|Portugal|Netherlands|Belgium|Switzerland|Austria|Poland|Hungary|Romania|Ukraine|Russia|Greece|Sweden|Norway|Denmark|Finland|Australia|New Zealand|Taiwan|Hong Kong';
// A state or province on its own is the state check's business, not a "place
// smaller than a state".
const JUST_A_REGION = new RegExp(`^(?:${STATE_NAME}|${PROVINCE_NAME})$`);
// Words before "District Court" and the like that are not a town.
const NOT_A_COURT_TOWN =
  /^(?:United|U\.S\.|Supreme|Appellate|Northern|Southern|Eastern|Western|Central|Middle|First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|In|At|By|To|From|Of|For|Before|Any|Each|Said|Such|Same|Local|General|Small|Tribal|Honorable|Hon|Judge|Clerk)\b/;

const STREET_TYPE =
  '(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Place|Pl|Terrace|Ter|Crescent|Cres|Highway|Hwy|Parkway|Pkwy|Trail|Trl|Ridge|Circle|Cir|Square|Sq|Row|Run|Pass|Path|Pike|Loop|Spur|Bend|Crossing|Alley|Plaza|Point|Cove|Close|Gardens|Grove|Mews|Walk|Quay|Turnpike|Freeway|Expressway|Route|Rte)';
const DIRECTION =
  '(?:N|S|E|W|NE|NW|SE|SW|North|South|East|West|Northeast|Northwest|Southeast|Southwest)';
const UNIT_WORD =
  '(?:Suite|Ste|Unit|Apt|Apartment|Room|Rm|Bldg|Building|Studio|Floor|Fl|Flat|Lot|#)';
const UNIT = `(?:,?\\s+${UNIT_WORD}\\.?\\s*#?\\s*[A-Za-z0-9-]+|,?\\s+(?:apt|unit|suite|ste)\\.?\\s*#?\\s*\\d[A-Za-z0-9-]*|,?\\s+\\d{1,3}(?:st|nd|rd|th)\\s+(?:Floor|Fl\\.?|floor)|,\\s+(?:Upper|Lower|Rear|Front|Basement|Office|Lobby|Clubhouse)\\b(?![^\\S\\n]+[A-Z][a-z])){0,2}`;
// Spaces inside one address: never a line break or a table cell boundary.
const SPC = '[^\\S\\n\\t]+';
// A house number: 918, 212-B, 418 1/2, 1210-363. Not an amount, and not the day
// in "June 14".
const HOUSE_NO = `(?:(?<![$£€\\d.,/])(?<!${MONTH}\\.?\\s)\\b[NSEW]?\\d{1,6}(?:-\\d{1,4}|-[A-Z]|\\/\\d{1,5})?[A-Z]?(?:\\s1\\/2)?|\\bOne(?=[^\\S\\n\\t]+[A-Z]))`;
// A unit written first: "Unit 12 - 815 Kristjanson Road", "#1204 - 13618 100
// Avenue", "Unit 6, ..."
const UNIT_FIRST = `(?:The${SPC}[A-Z][a-z]+(?:${SPC}[A-Z][a-z]+)?,\\s)?(?:(?:#|\\b(?:Unit|Apt|Suite|Ste|Apartment|Rm|Room|Flat)\\.?\\s)\\s?[A-Za-z0-9]+(?:,\\s+|\\s[-–]\\s))?`;

const AMOUNT = '\\d{1,3}(?:,\\d{3})+(?:\\.\\d+)?|\\d+(?:\\.\\d+)?';
const SCALE =
  '(?:\\s?(?:k|K|M|MM|B|bn|mm)\\b|\\s(?:thousand|million|billion|trillion)\\b)?';
const CURRENCY_SYMBOL = '(?:US|CA|C|A|AU|NZ|HK|S|CDN)?[$£€¥]';
const CURRENCY_CODE = '(?:USD|CAD|EUR|GBP|AUD|NZD|CHF|JPY|MXN|CDN)';
const NUMBER_WORD =
  '(?:a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|half)';

const SPOKEN_DIGIT = '(?:zero|oh|one|two|three|four|five|six|seven|eight|nine)';
const DIGIT_WORD =
  '(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)';
/** True when the line around `at` is a row of figures: three or more amounts on it. */
function ledgerLine(text, at) {
  const from = text.lastIndexOf('\n', at - 1) + 1;
  const to = text.indexOf('\n', at);
  const line = text.slice(from, to < 0 ? text.length : to);
  const figures = (
    line.match(
      /[$£€]\s?\d[\d,]*(?:\.\d{2})?|\b\d{1,3}(?:,\d{3})+(?:\.\d{2})?|\b\d+\.\d{2}\b/g,
    ) || []
  ).length;
  return (
    figures >= 3 ||
    (figures >= 2 && /^\s*\d{1,2}[/.-]\d{1,2}(?:[/.-]\d{2,4})?\s/.test(line))
  );
}

// Words that follow "login" or "user name" in ordinary writing.
const NOT_A_USER =
  /^(?:required|locked|pages?|accounts?|credentials?|interface|names?|access|attempts?|failed|screen|details|information|passwords?|portal|history|records?|sessions?|button|through|using|should|cannot|could|would|needs|there|their|these|those|which|where|while|errors?|issues?|problems?|below|above|again|after|before|being|still|since|until|every|other|shared|works|worked|working|reset|expired|disabled|enabled|created|changed|blocked|failure|success|prompt|email|emails|times?|today|yesterday|first|never|always|only|manual|guide|agreement|rights|profile|settings?|data|group|roles?|level|types?|status|token|codes?|links?|forms?|field|fields)$/;

/**
 * Make the letters of a pattern match either case, leaving escapes such as \s
 * alone.
 */
function ci(source) {
  let out = '';
  let inClass = false;
  for (let i = 0; i < source.length; i++) {
    const ch = source[i];
    if (ch === '\\') {
      out += ch + (source[++i] ?? '');
      continue;
    }
    if (ch === '[') inClass = true;
    if (ch === ']') inClass = false;
    if (/[A-Za-z]/.test(ch)) {
      out += inClass
        ? ch.toLowerCase() + ch.toUpperCase()
        : `[${ch.toLowerCase()}${ch.toUpperCase()}]`;
    } else {
      out += ch;
    }
  }
  return out;
}
/**
 * Placed before a value: a label in either case, optional "no./number/#",
 * optional "is/of", then a separator. Only the label ignores case; the value
 * that follows does not.
 */
const after = (labels, gap = 40) =>
  `(?<=\\b(?:${ci(labels)})\\b\\.?(?:\\s*(?:${ci('no\\.?|nos\\.?|number|num\\.?|id|code')}|#))?(?:\\s+(?:is|was|of|for))?[^\\S\\n]*[:#=]?[^\\S\\n]{0,3}(?:[^\\n\\d:#=$£€¥]{0,${gap}}?[:#=\\s])?[^\\S\\n]{0,2}(?:\\*{1,2}|__)?)`;
/**
 * An ID-like value: letters and digits, with spaces or dashes between groups.
 */
const ID_VALUE = '[A-Z0-9][A-Z0-9]*(?:[-/. ][A-Z0-9]+){0,5}(?![A-Za-z])';

const d = (id, group, label, placeholder, rules, extra = {}) => ({
  id,
  group,
  label,
  placeholder,
  kind: 'pattern',
  rules: rules.map(r => (r instanceof RegExp ? {re: r} : r)),
  ...extra,
});
const re = (source, flags = 'g') => new RegExp(source, flags);

/**
 * The pattern detectors, in the order they claim text. Each has id, group,
 * label, placeholder, kind 'pattern' and rules. A rule is {re, ok}: a global
 * regular expression and an optional ok(match, ctx, start) that rejects a
 * match by returning false.
 */
export const PATTERN_DETECTORS = [
  d('email', 'Contact details', 'Email address', 'EMAIL', [
    /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g,
    // "name dot surname at firm dot example"
    /\b[A-Za-z0-9]+(?:\s+(?:dot|underscore|dash|hyphen)\s+[A-Za-z0-9]+)*\s+at\s+[A-Za-z0-9-]+(?:\s+dot\s+[A-Za-z0-9-]+)+\b/g,
  ]),
  d('url', 'Online identifiers', 'Web address', 'URL', [
    /\bhttps?:\/\/[^\s<>"')]+|\bwww\.[^\s<>"')]+/gi,
    // A bare host name: vpn.firm.example
    /(?<![@\w.-])(?:[a-z0-9-]+\.)+(?:example|com|org|net|gov|edu|io|co|ca|uk|us|law|cpa|health|info|biz|app|dev|cloud|tech)\b(?![@\w-])(?:\/[^\s<>"')]*)?/g,
  ]),
  d('ip', 'Online identifiers', 'IP address', 'IP', [
    /\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b/g,
    {
      re: /(?<![A-Za-z0-9:])(?:[0-9A-Fa-f]{1,4}:){2,7}(?::?[0-9A-Fa-f]{1,4}){1,6}(?![A-Za-z0-9:])/g,
      ok: s =>
        /::|(?:.*:){5}/.test(s) &&
        !/^\d{1,2}:\d{2}(?::\d{2})?$/.test(s) &&
        !/^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$/.test(s),
    },
  ]),
  d('iban', 'Bank accounts and cards', 'IBAN', 'ACCOUNT', [
    {
      re: /\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){2,7}(?:\s?[A-Z0-9]{1,3})?\b/g,
      ok: validIban,
    },
  ]),
  d('card', 'Bank accounts and cards', 'Payment card number', 'CARD', [
    {re: /\b\d(?:[ -]?\d){12,18}\b/g, ok: validCard},
  ]),
  d(
    'card_exp',
    'Bank accounts and cards',
    'Card expiration date',
    'CARD_EXPIRY',
    [
      re(
        `${after('exp(?:ires|iry|iration)?(?:\\s+date)?|valid\\s+thru|good\\s+thru', 0)}(?:0[1-9]|1[0-2])\\s?[/-]\\s?(?:\\d{4}|\\d{2})\\b(?![/-]\\d)`,
        'g',
      ),
    ],
  ),
  d('cvv', 'Bank accounts and cards', 'Card security code', 'CARD_CODE', [
    re(
      `${after('CVV2?|CVC2?|CID|CSC|security\\s+code|card\\s+code', 10)}\\d{3,4}\\b`,
      'g',
    ),
    // In brackets after the label, or described: "the CVV (406)", "four digit
    // code on the front is 4026"
    /(?<=\b(?:CVV2?|CVC2?|CSC|CID)\s?\()\d{3,4}(?=\))/g,
    /(?<=\b(?:three|four|3|4)[- ]digit\s(?:security\s)?code\b[^.\n]{0,30}\s)\d{3,4}\b/gi,
    // "code on the back 771", "Exp / CVC<tab>09/27 / 418"
    /(?<=\bcode\son\s(?:the\s)?back\s(?:is\s)?)\d{3,4}\b/gi,
    /(?<=\b(?:CVC2?|CVV2?|CSC)\b[^\n]{0,12}\d{2}\s?\/\s?\d{2,4}\s?\/\s?)\d{3,4}\b/g,
    // "exp 08/29  code 611"
    /(?<=\b[Ee]xp[^\n]{0,20}\b[Cc]ode[:\s]+)\d{3,4}\b/g,
    /(?<=\b(?:[Cc]ard|[Vv]isa|[Mm]aster[Cc]ard|[Aa]mex|[Dd]iscover)\b[^\n]{0,80}\b(?:[Cc]ode|[Ss]ec\.?|[Ss]ecurity)[:#\s]+)\d{3,4}\b(?![-/]\d)/g,
  ]),
  d('ssn', 'Government and tax IDs', 'Social Security number', 'SSN', [
    {re: /\b\d{3}-\d{2}-\d{4}\b/g, ok: validSsn},
    // "SSN ends 6134", "His SSN ends -7758"
    /(?<=\b(?:SSNs?|SS#|[Ss]ocial(?:\s[Ss]ecurity)?(?:\s(?:[Nn]umbers?|#))?)\b(?:(?!\b(?:acct|account|card|check|cheque|visa|amex|mastercard|loan|policy)\b)[^.\n]){0,40}\b(?:ends|ending)\s(?:in\s|with\s)?)-?\d{4}\b/gi,
    // The second of two: "SSNs ending 4983 (Everett) and 8373 (Noor)"
    /(?<=\bSSNs?\b[^.\n]{0,40}\b(?:ends|ending)\s(?:in\s)?\d{4}\s(?:\([^)\n]{0,24}\)\s)?(?:and|&)\s)\d{4}\b/g,
    // "Last four of SSN: 5625"
    /(?<=\b[Ll]ast\s(?:four|4)(?:\sdigits)?\sof\s(?:the\s|his\s|her\s|my\s|your\s)?(?:SSN|[Ss]ocial(?:\s[Ss]ecurity)?(?:\s[Nn]umber)?)\b:?\s{1,3})\d{4}\b/g,
    // Asked for on one line and answered on the next: "Last four only.\n A.
    // 4570."
    /(?<=\blast\s(?:four|4)\b[^\n]{0,60}\n[^\n\d]{0,24})\d{4}(?=[.,]?(?:\s|$))(?![.,]?\s?(?:%|am|pm|\d))/gi,
    {re: /\b\d{3} \d{2} \d{4}\b/g, ok: validSsn},
    {
      re: re(
        `${after('SSN|SS#|social\\s+security', 15)}\\d{3}[- \\n]\\d{2}[- \\n]\\d{4}\\b`,
        'g',
      ),
      ok: s => validSsn(s.replace(/\s/g, '-')),
    },
    // Masked: xxx-xx-1234, ***-**-1234, 9XX-7X-4410
    {
      re: /(?<![A-Za-z0-9])[\dxX*•#]{3}-[\dxX*•#]{2}-\d{4}\b/g,
      ok: s => /[xX*•#]/.test(s),
    },
    {
      re: re(
        `${after('SSN|SS#|social\\s+security|social|ITIN|TIN|taxpayer\\s+id(?:entification)?', 20)}\\d{9}\\b`,
        'g',
      ),
      ok: validSsn,
    },
  ]),
  d('bn_ca', 'Government and tax IDs', 'Canadian business number', 'TAX_ID', [
    /\b\d{5}\s?\d{4}\s?[A-Z]{2}\s?\d{4}\b/g,
  ]),
  d(
    'sin_ca',
    'Government and tax IDs',
    'Canadian Social Insurance Number',
    'SIN',
    [
      {re: /\b\d{3}[- ]\d{3}[- ]\d{3}\b/g, ok: validSin},
      {
        re: /(?<![A-Za-z0-9*])[\dxX*]{3}[- ][xX*]{3}[- ][\dxX*]{3}(?![A-Za-z0-9*])/g,
        ok: s => /\d/.test(s),
      },
      {
        re: re(`${after('SIN|social\\s+insurance', 20)}\\d{9}\\b`, 'g'),
        ok: validSin,
      },
    ],
  ),
  d('ein', 'Government and tax IDs', 'Employer or VAT ID number', 'TAX_ID', [
    // Australian ABN/TFN/ACN, French SIRET and numéro fiscal, Quebec NEQ,
    // Spanish NIF, German Steuer-IdNr. and Steuernummer
    {
      re: /(?<=\b(?:ABN|TFN|ACN|SIRET|SIREN|NEQ|NIF|NIE|CIF|NAS|Steuer-IdNr\.?|Steuernummer|USt-IdNr\.?|numéro fiscal|no d['’]identification|TVQ|TPS|TVA)\s?:?\s{1,2})[A-Z]{0,2}\d[\d\s/.]{5,22}\d(?:\s[A-Z]{2}\d{4})?/g,
      ok: s => digitCount(s) >= 8 && !/\n\s*\n/.test(s),
    },
    /(?<![A-Za-z0-9-])\d{2}-\d{7}(?![A-Za-z0-9-])/g,
    {
      re: re(
        `${after('EIN|FEIN|VAT|GST|HST|tax\\s+id|business\\s+number|UTR|UBI', 25)}${ID_VALUE}`,
        'g',
      ),
      ok: s => digitCount(s) >= 6,
    },
  ]),
  d(
    'card_partial',
    'Bank accounts and cards',
    'Card or account number shown in part',
    'ACCOUNT',
    [
      // The middle hidden: 4769 15•• •••• 2996
      /\b\d{4}[ -]?\d{2}[•*xX]{2}[ -]?[•*xX]{4}[ -]?\d{4}\b/g,
      // Masked: x4410, ****1234, ...2204, XXXX-XXXX-XXXX-1234
      /(?<![A-Za-z0-9*#])(?<!\d[- ])(?:(?:[xX•]+|#{2,}|\*{3,})[- ]?)+\d{4}\b/g,
      /(?<![A-Za-z0-9.])(?:\.{3}|…)\s?\d{4,5}\b/g,
      /\b(?:Visa|Master[Cc]ard|Amex|American Express|Discover|Diners|JCB)(?:\s+(?:card|debit|credit))?\s+(?:ending(?:\s+in)?|x+|\*+|#)\s?\d{4,5}\b/g,
      // "savings ending -8840"
      /(?<=\bending\s(?:in\s)?)-\d{4}\b/g,
      // "her own acct ... ends 9920"
      /(?<=\b(?:acct|account|card|checking|chequing|savings)\b[^.\n]{0,70}\bends\s)\d{4}\b(?!\s?(?:\d|%))/gi,
      // "ending in 2239", "last four 5148", "Amex ending 34224"
      re(
        `${after('ending(?:\\s+in)?|ends\\s+in|last\\s+(?:four|4|five|5)(?:\\s+digits)?(?:\\s+of\\s+(?:the\\s+)?(?:card|account|acct))?|last4', 12)}\\d{4,5}\\b`,
        'g',
      ),
    ],
  ),
  d('phone', 'Contact details', 'Phone or fax number', 'PHONE', [
    /(?:(?<![\d-])\+?1[-. ]?)?\(?\b\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b(?:,?\s*(?:x|ext\.?|extension)\s*\.?\s*\d{1,6}\b)?/gi,
    {
      re: /\+\d{1,3}(?:[\s.-]?\(?\d{1,4}\)?){2,6}\b/g,
      ok: s => digitCount(s) >= 8 && digitCount(s) <= 15,
    },
    {
      re: /\b0\d{2,4} \d{3,4}(?: ?\d{3,4})?\b/g,
      ok: s => digitCount(s) >= 10 && digitCount(s) <= 12,
    },
    // Read aloud: "nine two eight, 555-0164", "five oh nine, 555, oh one three
    // four"
    re(
      `\\b(?:${SPOKEN_DIGIT}[\\s-]){2}${SPOKEN_DIGIT},?\\s\\d{3}-\\d{4}\\b`,
      'gi',
    ),
    {
      re: re(
        `\\b(?:(?:${SPOKEN_DIGIT}|\\d{3,4})(?:,\\s|[\\s-])){5,}(?:${SPOKEN_DIGIT}|\\d{3,4})\\b`,
        'gi',
      ),
      ok: s => {
        const n = s
          .split(/[\s,-]+/)
          .reduce((sum, w) => sum + (/^\d+$/.test(w) ? w.length : 1), 0);
        return n >= 7 && n <= 11;
      },
    },
    // Australian landline "(02) 5550 0142", French "05 55 55 01 42", Spanish
    // "655 55 01 82"
    /\(0\d\)\s?\d{4}\s?\d{4}\b/g,
    /(?<![\d.,])\b0\d(?:[ .]\d{2}){4}\b/g,
    /(?<![\d.,$£€])\b[6-9]\d{2}\s\d{2}\s\d{2}\s\d{2}\b(?!\s?[€$£%])/g,
    // An internal extension on its own: "Adjuster: Anders Folkestad, ext 4418"
    /(?<=\b(?:ext|extension)\.?\s)\d{3,5}\b/gi,
    // Dutch national format: 010-555 01 62
    /\b0\d{1,3}-\d{3} \d{2} \d{2}\b/g,
    // Any number after a word that says it is a phone number
    {
      re: re(
        `${after('tel|telephone|phone|mob|mobile|cell|fax|DDI|direct|direct\\s+line|direct\\s+dial', 8)}\\+?\\(?\\d[\\d ().-]{6,18}\\d\\b`,
        'g',
      ),
      ok: s => digitCount(s) >= 8 && digitCount(s) <= 15 && !looksLikeDate(s),
    },
  ]),
  // A street address is read before dates and reference numbers: "418 1/2 Cass
  // St" holds no date, and the 918 in "residing at 918 Juniper Court" is not an
  // employee number.
  d('street', 'Contact details', 'Street address or PO box', 'ADDRESS', [
    // Numbered roads: 4402 Highway 53, 118 County Road 12
    re(
      `${HOUSE_NO}${SPC}(?:(?:US|U\\.S\\.|State|County|Old)${SPC})?(?:Highway|Hwy|Route|Rte|Road|Rd|CR|SR|FM)\\.?${SPC}\\d{1,4}[A-Z]?\\b${UNIT}`,
    ),
    // Lettered county roads: N3172 County Road K
    re(
      `${HOUSE_NO}${SPC}(?:County|State)${SPC}(?:Road|Rd|Highway|Hwy|Trunk)\\.?${SPC}[A-Z]{1,3}\\b${UNIT}`,
    ),
    re(
      `${UNIT_FIRST}${HOUSE_NO}${SPC}(?:${DIRECTION}\\.?${SPC})?(?:[A-Z0-9][A-Za-z0-9.'’-]*${SPC}){0,4}?[A-Z0-9][A-Za-z0-9.'’-]*(?:${SPC}|\\n)${STREET_TYPE}\\b\\.?(?:${SPC}${STREET_TYPE}\\b\\.?)?(?:${SPC}${DIRECTION}\\b\\.?)?${UNIT}`,
    ),
    // No street word: 211 North Broadway, Suite 2950
    re(
      `${UNIT_FIRST}${HOUSE_NO}${SPC}(?:${DIRECTION}\\.?${SPC})?Broadway\\b${UNIT}`,
    ),
    // Grid addresses: 2150 South 1300 East, Suite 500
    re(
      `${HOUSE_NO}${SPC}${DIRECTION}\\.?${SPC}\\d{2,5}${SPC}${DIRECTION}\\b\\.?${UNIT}`,
    ),
    // A box number on its own line before the town: "Box 418, Fort Qu'Appelle,
    // SK"
    /(?<=^|\n)[^\S\n]*(?:General Delivery|Box\s\d{1,5})(?=,\s[A-Z])/g,
    // A house number alone, after a word that says who lives there: neighbor
    // "Hank" at 618
    re(
      `(?<=\\b(?:${ci('neighbor|neighbour|next\\s+door|tenant|landlord')})\\b[^.\\n]{0,25}\\bat\\s)\\d{2,5}\\b(?!\\s?(?:am|pm|a\\.m|p\\.m|%|:\\d|\\d))`,
    ),
    re(
      `\\b\\d{1,6}\\s+(?:${DIRECTION}\\.?\\s+)?(?:Calle|Avenida|Camino|Paseo|Via|Rue|Chemin|Boulevard)\\s+(?:(?:de|del|la|las|los|du|des)\\s+)?[A-Z][\\p{L}'’-]+(?:\\s+[A-Z][\\p{L}'’-]+)?${UNIT}`,
      'gu',
    ),
    // French and French-Canadian, with the comma after the number: "4418,
    // avenue du Mont-Royal Est", "14 bis, rue de la République", "1288, rue de
    // la Canardière, app. 4"
    re(
      `${HOUSE_NO}(?:\\s(?:bis|ter))?,?${SPC}(?:chemin|rue|avenue|av\\.|boul\\.?|boulevard|rang|route|montée|côte|place|allée|impasse|quai|cours)${SPC}(?:(?:de la|de l['’]|du|des|de|la|le|d['’])\\s?)?\\p{Lu}[\\p{L}'’-]+(?:[ -](?:de |du |des |la |le )?\\p{Lu}[\\p{L}'’-]+){0,3}(?:,?${SPC}(?:app\\.|appartement|bureau|suite|porte)\\s?\\d+[A-Z]?)?`,
      'gu',
    ),
    // Numbered avenues in Quebec: "88, 12e Avenue", "1150, 3e Avenue, bureau
    // 210"
    re(
      `${HOUSE_NO},?${SPC}\\d{1,3}e${SPC}(?:Avenue|Rue)(?:${SPC}(?:Est|Ouest|Nord|Sud))?(?:,?${SPC}(?:app\\.|appartement|bureau|suite|porte)\\s?\\d+[A-Z]?)?`,
    ),
    // Spanish, with the number after the street: "Calle Licenciado Poza 44, 3º
    // Izda."
    re(
      `\\b(?:Calle|C\\/|Avenida|Avda\\.?|Paseo|Plaza|Carrer|Camino|Ronda)${SPC}(?:(?:de|del|la|las|los)${SPC})?(?:\\p{Lu}[\\p{L}'’-]+${SPC}){1,4}\\d{1,4}(?:,${SPC}?\\d{1,2}[ºª]${SPC}?(?:Izda|Dcha|[A-Z])\\.?)?`,
      'gu',
    ),
    // British: "Flat 3, 27 Stricklandgate" (a street name with no street word)
    /\b(?:Flat|Apt|Apartment|Unit)\s\d+[A-Za-z]?,\s\d{1,4}[A-Za-z]?\s[A-Z][\p{L}'’-]+(?:[^\S\n\t][A-Z][\p{L}'’-]+)?/gu,
    // The street word first: "1420 Avenue H, Lot 6"
    re(
      `${HOUSE_NO}${SPC}(?:Avenue|Ave|Road|Rd|Street|St|Route)\\.?${SPC}[A-Z]\\b${UNIT}`,
    ),
    // Typed in lower case: "2218 w tioga st", "2204 ranger dr apt b"
    /(?<![$£€\d.,/])\b\d{3,6}\s(?:[nsew]\s)?[a-z]+(?:\s[a-z]+)?\s(?:st|ave|rd|dr|ln|blvd|hwy|pkwy)\b(?:\s(?:apt|unit|#)\s?[a-z0-9]+\b)?/g,
    // French-Canadian: 1184 chemin Kamiskotia Road, 22 rue Saint-Jean
    re(
      `${HOUSE_NO}${SPC}(?:chemin|rue|avenue|boul\\.?|boulevard|rang|route|montée|côte|place)${SPC}(?:(?:de la|de|du|des|la|le)${SPC})?[A-Z][\\p{L}'’-]+(?:[ -][A-Z][\\p{L}'’-]+){0,3}${UNIT}`,
      'gu',
    ),
    // ALL CAPS, as printed on forms: 745 MEDICAL CENTER PKWY STE 204
    re(
      `(?:\\b(?:UNIT|APT|SUITE|STE)\\.?\\s*[A-Z0-9-]+,?\\s+)?${HOUSE_NO}${SPC}(?:[A-Z0-9]+${SPC}){1,5}?${STREET_TYPE.toUpperCase()}\\b\\.?(?:${SPC}(?:STE|SUITE|UNIT|APT|BLDG|FL|#)\\.?\\s*[A-Z0-9-]+)?`,
    ),
    /\bP\.?\s?O\.?\s?Box\s+\d+\b/gi,
    /(?<![A-Za-z.])(?:RR|R\.R\.|Rural\s+Route|HC)\s?#?\d+(?:,?\s+Box\s+\d+)?\b/g,
    // British and Irish: 3 Toft Green; 55 Fleet Wharf, 6th Floor; Unit 6,
    // Ballybrit Business Park
    re(
      `(?:\\b${UNIT_WORD}\\.?\\s*[A-Za-z0-9-]+,\\s+)?\\b\\d{1,5}[A-Za-z]?\\s+(?:[A-Z][A-Za-z'’-]*\\s+){1,3}(?:Green|Wharf|Gate|Hill|Rise|Vale|Bank|Parade|Yard|End|Fields|Common|Embankment|Quay|Mews|Wynd|Brae|Gardens|Crescent|Terrace|Chase|Croft|Drove|Lea|Meadow|Meadows|Orchard|Paddock|View)\\b${UNIT}`,
    ),
    re(
      `\\b${UNIT_WORD}\\.?\\s*[A-Za-z0-9-]+,\\s+(?:[A-Z][A-Za-z'’-]*\\s+){1,3}(?:Business Park|Enterprise Park|Industrial Estate|Trading Estate|Retail Park|Enterprise Centre|Technology Park|Science Park|Office Park)\\b`,
    ),
    // Dutch and German: Keizersgracht 418-II, Havenkade 41-43, Hauptstraße 12a
    /\b[A-Z][\p{L}]+(?:straat|gracht|kade|weg|laan|plein|dijk|singel|strasse|straße|gasse|platz|allee|damm|ufer)\s\d+[A-Za-z]?(?:[-/]\s?[0-9A-Za-z]+)?\b/gu,
  ]),
  // Dates come before the general number rules so "12-05-2026" is a date, not
  // an account.
  d('dob', 'Dates and ages', 'Birth date', 'BIRTH_DATE', [
    // Typed in a hurry: "born aug 2019", "dobs: me 24.11.1980, anj 9 Jan 87"
    /(?<=\bborn\s)(?:jan|feb|mar|apr|may|jun|jul|aug|sept?|oct|nov|dec)[a-z]*\.?\s(?:19|20)\d{2}\b/g,
    re(
      `(?<=\\b(?:dobs?|DOBs?|born)\\b[^\\n]{0,40})\\b\\d{1,2}[\\s-]${MONTH}\\.?[\\s-]'?\\d{2}\\b(?!\\s?(?:%|:|\\d))`,
    ),
    re(
      `${after('born(?:\\s+on)?|DOB|D\\.O\\.B\\.?|date\\s+of\\s+birth|birth\\s*date|birthday|b\\.', 12)}${DATE}`,
      'g',
    ),
    re(
      `(?<=\\b(?:born|birth)\\s+(?:(?:in|during|around|about|circa)\\s+)?)(?:the\\s+)?(?:(?:early|late|mid)[\\s-]+)?(?:(?:spring|summer|fall|autumn|winter|${MONTH})\\s+(?:of\\s+)?)?${YEAR}\\b`,
      'g',
    ),
    {
      re: re(DATE),
      ok: (s, ctx) => {
        const y = /(?:19|20)\d{2}/.exec(s);
        return Boolean(y) && Number(y[0]) <= ctx.latestYear - 16;
      },
    },
  ]),
  d('age90', 'Dates and ages', 'Age over 89', 'AGE', [
    /(?:\bbeing\s)?\b(?:ninety|one\s+hundred(?:\s+and)?)(?:[- ](?:one|two|three|four|five|six|seven|eight|nine))?(?:\s\(\d{2,3}\))?[- ]years?[- ](?:old|of\s+age)\b/gi,
    /\b(?:aged?|age:)\*{0,2}\s(?:9\d|1[01]\d)\b/gi,
    // "she is 91 now", "She's 91 and doesn't do email", "her mother, who is
    // 92,"
    /(?<=\b(?:[Hh]e|[Ss]he|who|[Mm]other|[Ff]ather|[Gg]randmother|[Gg]randfather|[Mm]om|[Dd]ad|[Aa]unt|[Uu]ncle|[Cc]lient|[Pp]atient)\s(?:is|was|turned|turns)\s(?:now\s)?|\b(?:[Ss]he|[Hh]e)['’]s\s)(?:9\d|1[01]\d)(?:[- ]years?[- ](?:old|of\s+age))?(?=[\s,.;)]|$)(?!\s?(?:%|percent|days?|miles?|lbs?|pounds?|kg|weeks?|months?|minutes?|hours?|points?|years?\s+(?:into|away|ago|from)))/g,
    // "turned one hundred and one", "ninety-something", "her 95th birthday",
    // "Mrs Arkwright is 92 (born ...)"
    /\b(?:turned|turns|turning|aged?)\s(?:ninety|one\s+hundred)(?:[- ](?:and\s)?(?:one|two|three|four|five|six|seven|eight|nine))?\b/gi,
    /\bninety-something\b/gi,
    /\b(?:9\d|1[01]\d)(?:st|nd|rd|th)\sbirthday\b/g,
    /(?<=\b\p{Lu}\p{Ll}+\sis\s)(?:9\d|1[01]\d)(?=\s\(born|[,;]|\snow\b|\sand\b)/gu,
    // Chart shorthand: "93 y/o", "96 Y / F"
    /\b(?:9\d|1[01]\d)\s?(?:y\/o|y\.o\.?|yo\b|yrs?\b\.?(?!\s+(?:ago|of|into|from|later|after|before))|Y(?=\s?\/\s?[MF]\b))/g,
    // "died August 30, 2026 at 97"
    /(?<=\b(?:died|passed|deceased)\b[^.\n]{0,40}\b)at\s(?:9\d|1[01]\d)\b(?!\s?(?:%|:|am|pm|a\.m|p\.m|\d))/g,
    /\b(?:9\d|1[01]\d)[- ]years?[- ](?:old|of\s+age)\b/gi,
    /\b(?:9\d|1[01]\d)[- ]year[- ]old\b/gi,
    /\b(?:turned|turning|turns|at\s+age|age\s+of|reached)\s(?:9\d|1[01]\d)\b/gi,
    // After a name, as in "Walter Kowalczyk, 91, …"
    /(?<=\p{Lu}[\p{L}'’-]+,\s)(?:9\d|1[01]\d)(?=[,;)])/gu,
    /(?<=\((?:age\s)?)(?:9\d|1[01]\d)(?=\))/g,
    /\b(?:ninety|one\s+hundred(?:\s+and)?)(?:[- ](?:one|two|three|four|five|six|seven|eight|nine))?(?:\s\(\d{2,3}\))?[- ]years?[- ](?:old|of\s+age)\b/gi,
  ]),
  d('date', 'Dates and ages', 'Any date', 'DATE', [
    re(DATE),
    ...DATE_FORMS_INTL.map(f => re(f, 'gu')),
    re(MONTH_DAY_ONLY),
    // The end of a range: "7/20-8/7"
    /(?<=\d{1,2}\/\d{1,2}\s?[-–]\s?)(?:0?[1-9]|1[0-2])\/(?:0?[1-9]|[12]\d|3[01])(?![\d/])/g,
    re(MONTH_ALONE),
  ]),
  d(
    'passport_dl',
    'Government and tax IDs',
    'Passport, license or other government ID number',
    'ID_NUMBER',
    [
      {
        re: re(
          `${after("passport|driver'?s?\\s+licen[sc]es?|driving\\s+licen[sc]es?|DL|state\\s+id|licen[sc]es?|certificate|bar|NPI|DEA|national\\s+insurance|NI|NINO|medicare|MBI|alien(?:\\s+registration)?|A-number|USCIS|CAF|PTIN|EFIN|visa|green\\s+card|voter|attorney\\s+id|bar\\s+id|SBN|VSB|registration|health\\s+card|health\\s+number|PHN|OHIP|RAMQ|HCN|RCIC|CRPO|SRA|ICCRC|LSO|CPSO|CNO|MARN|lic|pasaporte|passeport|permis|assurance\\s+maladie|carte\\s+soleil|ID", 25)}${ID_VALUE}`,
          'g',
        ),
        ok: s =>
          digitCount(s) >= 4 ||
          (digitCount(s) >= 3 && s.replace(/[^A-Z0-9]/g, '').length >= 9),
      },
      // A bar number after a lawyer's name: "Calloway Jefferson-Ruiz,
      // #68214MO", "Marguerite Oyelaran (P71443)"
      /(?<=\p{Ll},\s#)\d{4,8}[A-Z]{0,3}\b/gu,
      /(?<=\p{Ll}\s\()[A-Z]{0,2}\d{5,8}(?=\))/gu,
      // A regulator known only by its initials: "CRPO # 009417", "SRA no.
      // 648213"
      /(?<=\b(?!(?:PO|INV|REF|ACCT|CK|CHK|RX|MRN|EIN|SSN|VIN|ID|NO|TEL|FAX|ZIP|APT|STE|RM|BOX|DOB|PIN|CVV|TXN|JOB|LOT|ROOM|ITEM|FORM|LINE|PAGE|RFP|RFA|ROG)\b)[A-Z]{3,6}\s?(?:#|[Nn]o\.)\s?)[A-Z]?\d{5,10}\b/g,
      // UK National Insurance number
      /\b[A-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b/g,
      // US alien registration number
      /\bA[- ]?\d{3}[- ]?\d{3}[- ]?\d{3}\b/g,
    ],
  ),
  d(
    'routing',
    'Bank accounts and cards',
    'Bank routing number or sort code',
    'ROUTING',
    [
      {
        re: re(`${after('routing|ABA|RTN|transit', 20)}\\d{9}\\b`, 'g'),
        ok: validRouting,
      },
      re(`${after('sort(?:\\s+code)?', 10)}\\d{2}-\\d{2}-\\d{2}\\b`, 'g'),
      re(`${after('BSB', 6)}\\d{3}-?\\d{3}\\b`, 'g'),
      re(
        `${after('transit|institution|inst', 20)}\\d{3,5}(?:-\\d{3})?\\b`,
        'g',
      ),
    ],
  ),
  d(
    'credential',
    'Online identifiers',
    'Password, PIN or user name',
    'CREDENTIAL',
    [
      // Shaped like a password: capital, small letter, digit and symbol in one
      // word of 8+ ("Maple!4471", "Winter2026$")
      /(?<![\w@/.#$-])(?=[A-Za-z0-9!#$%&*^+=?_-]*[a-z])(?=[A-Za-z0-9!#$%&*^+=?_-]*[A-Z])(?=[A-Za-z0-9!#$%&*^+=?_-]*\d)(?=[A-Za-z0-9_-]*[!#$%&*^+=?])[A-Za-z][A-Za-z0-9!#$%&*^+=?_-]{7,31}(?![\w/@])/g,
      // Note shorthand: "user mnguyenfraser / temp pw Maple!4471"
      /(?<=\buser\s)[a-z][a-z0-9._-]{4,30}(?=\s?\/\s?(?:temp\s)?(?:pw|pass|password|pwd)\b)/gi,
      // After the word for it, a few words on: "the password he was using,
      // Ruffin1958,", "admin pw Rainbow2Brown"
      {
        re: re(
          `(?<=\\b(?:${ci('password|passcode|pw|pwd')})\\b[^\\n.;:]{0,30}?[\\s,\\/])[A-Za-z][^\\s"”',;()]{5,40}(?<![.:)])`,
        ),
        ok: s =>
          /[\d!#$%&*^+=?]/.test(s) && /[a-z]/.test(s) && /[A-Z\d]/.test(s),
      },
      // After a login and a slash: "login tvandermolen@mossback.example /
      // Elk$Hair#Caddis"
      {
        re: re(
          `(?<=\\b(?:${ci('login|user\\s?name|user\\s?id|user')})\\b[^\\n]{0,60}\\s\\/\\s)[A-Za-z][^\\s"”',;()]{5,40}(?<![.:)])`,
        ),
        ok: s => /[\d!#$%&*^+=?]/.test(s) && /[a-z]/.test(s),
      },
      // Social media and payment-app handles: @shirin.g.runs, $tavi_L
      /(?<![\w.@])@[A-Za-z][\w.]{3,30}\b/g,
      /(?<![\w$.,])\$[A-Za-z][A-Za-z0-9_]{2,20}\b/g,
      // The answer to a security question: 'Recovery question answer ("first
      // pet"): Bolinha'
      /(?<=\b(?:security|recovery|secret)\s(?:question|answer)\b[^\n:]{0,40}:\s)[A-Z][\w-]+(?:\s(?:[A-Z]{1,3}|[A-Z][a-z]+))?\b/g,
      // A Windows account with its domain: bbg\tmokoenahart
      /\b[a-z][a-z0-9]{1,11}\\[a-z][a-z0-9._-]{2,30}\b/g,
      // A Wi-Fi network: network "BellHouse"
      /(?<=\b(?:network|SSID)\s(?:name\s)?(?:is\s)?["“])[^"”\n]{3,32}(?=["”])/g,
      // A user name after the word for it, when it has a digit or a symbol in
      // it: "user ID kravchukelec1", "account (jreyes.redmond)"
      {
        re: re(
          `(?<=\\b(?:${ci('user\\s?id|user\\s?name|user|login|log-in|sign(?:ed)?\\s+in\\s+as|log(?:ged)?\\s+in\\s+as|account')})\\b(?:\\s+(?:is|was|as))?[:=]?[^\\S\\n]{0,3}[(\\x60"“']?)[a-z][a-z0-9]*(?:[._\\\\-][a-z0-9]+)*(?![\\w@]|\\.[a-z])`,
        ),
        ok: s => s.length >= 5 && /[\d._\\-]/.test(s),
      },
      // ... or a plain one, after a cue that leaves no doubt: "Windows login is
      // coadmin", "signed in as tboone"
      {
        re: re(
          `(?<=\\b(?:${ci('user\\s?id|user\\s?name|login|log-in|sign(?:ed)?\\s+in\\s+as|log(?:ged)?\\s+in\\s+as|user\\s+is|user:')})(?:\\s+(?:is|was))?(?:[:=\\t]|\\s)\\s{0,2}[(\\x60"“']?)[a-z][a-z0-9]{4,30}(?![\\w@-]|\\.[a-z])`,
        ),
        ok: s => !NOT_A_USER.test(s),
      },
      // A label, then ":" or "=", then the value
      re(
        `(?<=\\b(?:${ci('password|passcode|passphrase|pwd|pw|PIN|user\\s?name|user\\s?id|login|log-in|portal\\s+id')})\\b[^\\n:=.;!?]{0,20}[:=][^\\S\\n]*)["“']?[^\\s"”',;]{3,40}(?<![.:)])`,
      ),
      // A PIN at the end of a longer phrase: "Identity Protection PIN issued to
      // Tevita by the IRS for this season: 604417"
      re(
        `(?<=\\b(?:${ci('PIN|passcode')})\\b[^\\n:=.;!?]{0,60}[:=][^\\S\\n]*)\\d{4,8}\\b`,
      ),
      // In brackets, or after a few words: "the passcode to my phone (0513,
      // ...)", "PIN for cash advance 7714", "the callback PIN, which is 4471"
      re(
        `(?<=\\b(?:${ci('PIN|passcode|password')})\\b[^\\n:=.;!?()\\d]{0,30}\\()\\d{4,8}(?=[,)])`,
      ),
      re(
        `(?<=\\b(?:${ci('PIN|passcode')})\\b(?:,?\\s(?:which\\s)?(?:is|was)|\\sfor\\s[^\\n\\d.;:]{2,25})\\s)\\d{4,8}\\b(?!\\s?(?:%|\\/|-\\d))`,
      ),
      // Door, alarm and lockbox codes: "Lockbox on side door, code **1930**",
      // "Alarm panel code 40418#"
      re(
        `(?<=\\b(?:${ci('lockbox|alarm|door|gate|garage|safe|keypad|entry|access|security|panel|voicemail|wi-?fi')})\\b[^.\\n]{0,30}\\b(?:${ci('code|combo|combination')})\\s(?:is\\s)?\\*{0,2})\\d{3,8}#?`,
      ),
      // "password Sweetgrass#2019", "user name as buddyk34", "the PIN, 0834":
      // no colon, so the value must look like a credential (a digit or a symbol
      // in it), not like the next word of a sentence
      {
        re: re(
          `(?<=\\b(?:${ci('password|passcode|passphrase|PIN|user\\s?name|user|login')})(?:\\s+(?:is|was|to|as|of))?,?\\s+)["“']?[^\\s"”',;()]{4,40}(?<![.:)])`,
        ),
        ok: s => /\d/.test(s) || /[!@#$%^&*_+=.-]/.test(s.slice(1, -1)),
      },
    ],
  ),
  d(
    'device',
    'Online identifiers',
    'Device serial or hardware address',
    'DEVICE',
    [
      /\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b/g,
      // A computer's name on the network: host name STANS-MACBOOK
      /(?<=\bhost\s?name\s(?:is\s)?)[A-Z0-9][A-Z0-9-]{3,24}\b/g,
      {
        re: re(
          `${after('serial|S\\/N|SN|IMEI|asset\\s+tag|device\\s+id|transmitter|sensor|pacemaker|implant', 20)}${ID_VALUE}`,
          'g',
        ),
        ok: s => digitCount(s) >= 3 && s.length >= 5,
      },
    ],
  ),
  d(
    'vin',
    'Record numbers',
    'Vehicle identification or plate number',
    'VEHICLE',
    [
      // British registration plates: YK21 HXT
      /\b[A-Z]{2}\d{2}\s[A-Z]{3}\b/g,
      {
        re: /\b[A-HJ-NPR-Z0-9]{17}\b/g,
        ok: s => /\d/.test(s) && /[A-Z]/.test(s) && digitCount(s) < 17,
      },
      {
        re: re(
          `${after('plate|plates|tag|registration|reg|rego|hull|HIN|IMO|MMSI|official\\s+number', 15)}(?:(?:${STATE_ABBR})[ -])?[A-Z0-9]{1,4}[- ]?[A-Z0-9]{2,8}(?![A-Za-z])`,
          'g',
        ),
        ok: s => hasDigit(s) && s.replace(/[^A-Z0-9]/g, '').length >= 5,
      },
    ],
  ),
  d(
    'record',
    'Record numbers',
    'Case, file, claim, policy or other reference number',
    'RECORD',
    [
      // A court number after a case name or at the start of a caption line:
      // "Lindqvist v. Larkfield, No. CI 26-4471"
      {
        re: re(
          `(?<=(?:\\bv\\.[^\\n]{1,80},|^|\\n)[^\\S\\n]*(?:${ci('case|cause|docket')}\\s+)?N[oO]\\.[^\\S\\n]{1,2})${ID_VALUE}(?:-[a-z]{2,4}\\b)?`,
          'g',
        ),
        ok: s => digitCount(s) >= 4 && !looksLikeDate(s),
      },
      // A short number after the word that says what it is: unit T5512, lot
      // 203-B, folio 88104-2, box #214
      {
        re: re(
          `(?<=\\b(?:${ci('unit|lot|safe\\s+deposit\\s+box|box|folio|agreement|job|room|bed|title|tracking|company')})\\s(?:(?:${ci('no\\.?|number')})\\s?)?#?)(?:[A-Z]{1,3}\\s)?[A-Z0-9]*\\d[A-Z0-9]*(?:[-/][A-Z0-9]+)*(?:\\s\\d{4,5}(?:\\s[A-Z0-9]{2,4})?)?(?![A-Za-z])`,
          'g',
        ),
        ok: s =>
          digitCount(s) >= 3 &&
          !looksLikeDate(s) &&
          !/^(?:19|20)\d{2}$/.test(s),
      },
      // An ID that starts with one small letter: "Resident ID t0044187"
      re(
        `${after('resident|member|customer|client|user|account|tenant', 12)}[a-z]\\d{5,10}\\b`,
        'g',
      ),
      // Check numbers named in the plural: "Checks 5391 ($1,200, June 6) and
      // 5447"
      /(?<=\b[Cc]he(?:ck|que)s\s(?:nos?\.?\s)?(?:#?\d{3,6}\s(?:\([^)\n]{0,40}\)\s)?(?:and|&)\s)?)#?\d{3,6}\b(?!\s?(?:%|\.\d))/g,
      // Booking and confirmation codes: six letters and digits, "conf. QK7M2X"
      {
        re: re(
          `${after('conf|confirmation|booking|locator|PNR|reservation', 12)}[A-Z0-9]{6}\\b`,
          'g',
        ),
        ok: s => /\d/.test(s) && /[A-Z]/.test(s),
      },
      {
        re: re(
          `${after('case|cause|docket|file|matter|claim|policy|invoice|inv|reference|ref|MRN|medical\\s+record|chart|member|beneficiary|subscriber|group|loan|mortgage|check|cheque|chq|ck|chk|I\\.D|payroll|matricule|resident|authori[sz]ation|warrant|booking|tax\\s+map|frequent\\s+flyer|membership|PO(?!\\s*Box)|purchase\\s+order|order|receipt|confirmation|client|customer|contract|engagement|incident|report|permit|parcel|APN|employee|emp|EID|badge|ticket|rx|prescription|citation|booking|inmate|control|notice|account\\s+id', 20)}${ID_VALUE}`,
          'g',
        ),
        ok: s =>
          (digitCount(s) >= 3 || /^[A-Z]{3,6}\d{2,}$/.test(s)) &&
          !looksLikeDate(s) &&
          !FORM_ONLY.test(s) &&
          !FORM_FAMILY.test(s) &&
          !/^(?:19|20)\d{2}$/.test(s) &&
          !/^\d{1,2}\.\d{1,2}$/.test(s),
      },
      // Federal docket style: 2:24-cv-01234-JLR
      /\b\d{1,2}:\d{2}-[a-z]{2,4}-\d{3,6}(?:-[A-Z]{2,5}){0,2}\b/g,
      // Letters then digits with separators: INV-26-3391, BW-00672, KR-10418
      {
        re: /(?<![A-Za-z0-9-])(?<!\b(?:Form|Schedule|Section|Rule|Title|Chapter|Article|Exhibit|Publication|Pub\.?)\s)[A-Z][A-Z0-9]{0,15}(?:[-/.:][A-Z0-9]+){1,5}(?![A-Za-z0-9-])/g,
        ok: s => digitCount(s) >= 4 && !FORM_NUMBER.test(s),
      },
      // Digits first, with a letter somewhere: 2025-CV-03381, 0312-44871-R,
      // 4471-B
      {
        re: /(?<![A-Za-z0-9-])(?<!\b(?:Form|Schedule|Section|Rule|Title|Chapter|Article|Exhibit|Publication|Pub\.?)\s)(?<![$£€¥.,])\d[A-Z0-9]*(?:[-/:][A-Z0-9]+|-[a-z]{2,4}(?=-)){1,5}(?![A-Za-z0-9-])/g,
        ok: s =>
          digitCount(s) >= 4 &&
          /[A-Za-z]/.test(s) &&
          !FORM_NUMBER.test(s) &&
          !looksLikeDate(s) &&
          !/^\d{1,2}:\d{2}/.test(s),
      },
      // Letters and digits run together: NL004471882B01, 23CV41877, A09417726
      {
        re: /\b[A-Z0-9]{8,20}\b/g,
        ok: s => digitCount(s) >= 4 && /[A-Z]/.test(s),
      },
      // Two or three capitals and a long number: "IR 2204187"
      /\b[A-Z]{2,3}\s\d{6,10}\b(?!\s?(?:%|\.\d))/g,
    ],
  ),
  d(
    'account',
    'Bank accounts and cards',
    'Account number or other long number',
    'ACCOUNT',
    [
      re(
        `${after('SWIFT|BIC', 30)}[A-Z]{6}[A-Z0-9]{2}(?:[A-Z0-9]{3})?\\b`,
        'g',
      ),
      {
        re: re(
          `${after('account|acct|a\\/c|checking|chequing|savings|deposit', 20)}\\d{3,}(?:[ -]\\d{2,}|\\n\\d{2,}){1,4}(?![\\dA-Za-z-])`,
          'g',
        ),
        ok: s => digitCount(s) >= 7 && !looksLikeDate(s.replace(/\s/g, '-')),
      },
      {
        re: re(
          `${after('account|acct|a\\/c|IBAN|brokerage|plan|portfolio|checking|chequing|savings', 20)}${ID_VALUE}`,
          'g',
        ),
        ok: s => digitCount(s) >= 4 && !looksLikeDate(s),
      },
      // Groups of digits joined by dashes: 4471-889-2203, 0048-771203-9,
      // 77-104-5529
      {
        re: /(?<![A-Za-z0-9-])\d{2,}(?:-\d+){1,5}(?![A-Za-z0-9-])/g,
        ok: s =>
          digitCount(s) >= 7 &&
          !looksLikeDate(s) &&
          !looksLikePhone(s) &&
          !/^(?:19|20)\d{2}-(?:19|20)\d{2}$/.test(s),
      },
      // Groups of four or more digits joined by single spaces: 4471 8892 2031
      {
        re: /\b\d{4,}(?: \d{4,}){1,4}\b/g,
        ok: s => !/^(?:19|20)\d{2} (?:19|20)\d{2}$/.test(s),
      },
      // Any long run of digits
      /\b\d{8,17}\b/g,
    ],
  ),
  d('money', 'Financial details', 'Money amount', 'AMOUNT', [
    // A claim-form charge with a space for the decimal point, on a line that
    // starts with a date: "09 10 2026 72148 B 1,460 00"
    /(?<=(?:^|\n)\d{2}[ /-]\d{2}[ /-]\d{2,4}\s[^\n]*\s)\d{1,3}(?:,\d{3})*\s\d{2}(?=[^\S\n]*(?:\n|$))/g,
    re(`\\(${CURRENCY_SYMBOL}\\s?(?:${AMOUNT})\\)`),
    // The currency sign after the number, continental style: "1 200 $", "46 000
    // €", "112.480,17 €", "412 €"
    re(
      `(?<![\\d.,\\p{L}])\\d{1,3}(?:[ \\u00A0\\u202F.]\\d{3})*(?:,\\d{2})?\\s?(?:\\$|€|£)(?!\\s?\\d)`,
      'gu',
    ),
    // Brazilian reais and Swiss francs: "R$ 61.000", "CHF 61'000"
    /\bR\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?/g,
    re(`\\b${CURRENCY_CODE}\\s?\\d{1,3}(?:['’]\\d{3})+(?:\\.\\d{2})?\\b`),
    // Slang: "2 grand"
    /\b\d+(?:\.\d+)?\s(?:grand|bucks)\b/g,
    // A fee quoted with no sign: "fee quoted 425"
    /(?<=\bquoted\s(?:me\s|us\s|her\s|him\s|them\s)?)\d{2,6}\b(?!\s?(?:%|\/|-|:|\d))/g,
    // French-Canadian: 41 280,16 $
    re(
      `(?<![\\d.,])\\d{1,3}(?:[ \\u00A0\\u202F]\\d{3})*,\\d{2}\\s?${CURRENCY_SYMBOL}`,
    ),
    // European style: € 18.020,00
    re(
      `${CURRENCY_SYMBOL}\\s?(?:\\d{1,3}(?:\\.\\d{3})+(?:,\\d{2})?|\\d{1,3},\\d{2})\\b`,
    ),
    re(
      `(?<![A-Za-z0-9])-?${CURRENCY_SYMBOL}\\s?(?:${AMOUNT})${SCALE}(?:\\s?\\/\\s?(?:mo|month|wk|week|hr|hour|yr|year|day|ea|each|unit|sf|sq\\s?ft|mile|mi|visit|session|person)\\b)?`,
    ),
    re(`\\b${CURRENCY_CODE}\\s?\\d{1,3}(?:\\.\\d{3})+(?:,\\d{2})?\\b`),
    re(`\\b${CURRENCY_CODE}\\s?(?:${AMOUNT})${SCALE}`),
    re(
      `\\b(?:${AMOUNT})${SCALE}[^\\S\\n]?(?:${CURRENCY_CODE}|dollars?|euros?|pounds?|bucks|cents)\\b`,
      'gi',
    ),
    // Shorthand: 75k, 48.2k (but not 401k)
    {re: /\b\d{1,3}(?:\.\d+)?[kK]\b/g, ok: s => !/^401k$/i.test(s)},
    // Spelled out: twelve thousand dollars, sixty thousand
    re(
      `\\b${NUMBER_WORD}(?:[\\s-]+(?:and\\s+)?${NUMBER_WORD})*\\s+(?:dollars|pounds|euros|bucks|grand)\\b(?:\\s(?:a|an|per|each)\\s(?:hour|month|year|week|day|quarter))?`,
      'gi',
    ),
    re(
      `\\b${NUMBER_WORD}(?:[\\s-]+(?:and\\s+)?${NUMBER_WORD})*[\\s-]+(?:hundred|thousand|million|billion)\\b(?:\\s(?:a|per|each)\\s(?:month|year|week|day|hour|quarter))?`,
      'gi',
    ),
    // Figures as spoken: "Forty-three eight seventy-five"
    re(`\\b${DIGIT_WORD}(?:[\\s-]${DIGIT_WORD}){3,}\\b`, 'gi'),
    // "worth around six fifty"
    re(
      `(?<=\\b(?:worth|paid|pay|offered|asking|owes?|owed|costs?|sold\\s+for|bought\\s+for|settled?\\s+for)\\s+["“]?(?:(?:around|about|roughly|maybe|like|approximately)\\s+)?)(?:one|two|three|four|five|six|seven|eight|nine)\\s(?:ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)(?:[- ](?:one|two|three|four|five|six|seven|eight|nine))?\\b`,
      'gi',
    ),
    // A scale word with no currency sign: "about 2.8 million in revenue"
    re(
      `(?<![A-Za-z0-9.,$£€¥-])\\d{1,3}(?:\\.\\d+)?\\s?(?:million|billion|MM)\\b(?!\\s(?:people|users|shares|units|miles|tons|barrels|acres|records|customers|views|members|square|sq|gallons|pounds|lbs|kilometers|km|years))`,
    ),
    // Pay described as a share: "sixty percent of her former salary"
    re(
      `\\b(?:\\d{1,3}(?:\\.\\d+)?\\s?(?:%|percent|per\\s+cent)|${NUMBER_WORD}(?:[\\s-]+${NUMBER_WORD})*\\s+(?:percent|per\\s+cent))\\s+of\\s+(?:(?:his|her|their|my|our|the|its)\\s+)?(?:(?:former|current|prior|previous|base|gross|net|annual|monthly|weekly|regular|usual|pre-injury|pre-tax)\\s+)*(?:salary|pay|wages?|earnings|income|compensation|commissions?|bonus|rate|revenue|profits?|proceeds|draw)\\b`,
      'gi',
    ),
    // Ledger figures with no currency sign: (27,315.88), 134,031.48, 52,800,
    // 1250.50
    /\(\d{1,3}(?:,\d{3})+(?:\.\d{2})?\)|\(\d+\.\d{2}\)/g,
    /(?<![A-Za-z0-9.,$£€¥-])\d{1,3}(?:,\d{3})+(?:\.\d{2})?(?![A-Za-z0-9]|[.,]\d)(?!\s"?(?:online\s)?(?:miles|shares|units|hours|sq\b|square|acres|lbs|pounds|gallons|employees|users|pages|words|members|people|customers|feet|ft\b|km\b|tons|barrels|bushels|head\b|kWh|views|visits|downloads))/g,
    /(?<![A-Za-z0-9.,$£€¥-])\d{3,}\.\d{2}(?![A-Za-z0-9]|[.,]\d)/g,
    // A small figure after the word that says it is money: "union dues 28.50
    // plus garnishment 383.50"
    re(
      `(?<=\\b(?:${ci('dues|fee|fees|rent|payment|premium|copay|deductible|balance|amount|charge|price|cost|total|refund|deposit|garnishment|wages?|tip|tax|interest|penalty|fine|allowance|stipend|bonus')})\\s(?:of\\s|is\\s|was\\s)?)\\d{1,3}\\.\\d{2}\\b(?!\\s?%)`,
    ),
    // Small figures with no sign, in a row of other amounts: 41.50   156.86
    // --   2,207.55
    {
      re: /(?<![A-Za-z0-9.,$£€¥%-])\d{1,2}\.\d{2}(?![A-Za-z0-9%]|[.,]\d)/g,
      ok: (s, ctx, at) => ledgerLine(ctx.text, at),
    },
  ]),
  d('zip', 'Contact details', 'ZIP code', 'ZIP', [
    /\b\d{5}-\d{4}\b/g,
    re(`(?<=\\b(?:${STATE_ABBR})\\.?,?\\s{1,3})\\d{5}(?:-\\d{4})?\\b`),
    re(`(?<=\\b(?:${STATE_NAME}),?\\s{1,3})\\d{5}(?:-\\d{4})?\\b`),
    re(
      `${after('ZIP(?:\\s+code)?|postal\\s+code|postcode', 6)}(?:\\d{5}(?:-\\d{4})?|[A-Za-z]\\d[A-Za-z][ -]?\\d[A-Za-z]\\d)\\b`,
      'g',
    ),
    // German and Dutch: the postal code follows the street and house number
    /(?<=(?:straat|gracht|kade|weg|laan|plein|dijk|singel|strasse|straße|gasse|platz|allee|damm|ufer)\s\d+[a-z]?(?:[-/]\d+)?\s*[,|]?\s*)\d{4,5}(?:\s?[A-Z]{2})?\b/gu,
    /(?<=\b(?:NSW|VIC|QLD|TAS|ACT|WA|SA|NT) )\d{4}\b/g,
    // Dutch: "Kruisstraat 118-B, 5612 CL Eindhoven"
    /(?<=,\s)\d{4}\s[A-Z]{2}(?=\s[A-Z][a-z]+)/g,
    /(?<=^|\n|,\s|[-–—]\s)\d{5}(?=\s\p{Lu}[\p{L}'’-]+(?:[\s,.;-]|$))(?!\s(?:[A-Z]{2}\b|North|South|East|West|N\b|S\b|E\b|W\b))/gmu,
    // A five-digit number that starts like a ZIP code found elsewhere in the
    // same document
    {
      re: /(?<![\d$£€.,#-])\b\d{5}\b(?![-.,]?\d)/g,
      ok: (s, ctx) => ctx.zipPrefixes.has(s.slice(0, 3)),
    },
  ]),
  d(
    'postal_ca',
    'Contact details',
    'Canadian, UK or Irish postal code',
    'POSTAL',
    [
      /\b[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d\b/g,
      /\b[A-Z]{1,2}\d[A-Z\d]?\s\d[A-Z]{2}\b/g,
      {
        re: /\b[A-Z]\d{2}\s?[A-Z0-9]{4}\b/g,
        ok: s => /[A-Z]/.test(s.slice(-4)) && /\d/.test(s.slice(-4)),
      },
    ],
  ),
  d(
    'places',
    'Names',
    'Cities, counties and other places smaller than a state',
    'PLACE',
    [
      // The city in "Dallas, TX" or "Thunder Bay, Ontario". The state is a
      // separate check (below), because HIPAA lets a state stay and the other
      // rules do not.
      re(
        `(?<![\\p{L}\\p{N}])\\p{Lu}[\\p{L}\\p{M}.'’-]+(?: \\p{Lu}[\\p{L}\\p{M}.'’-]+){0,2}(?=,\\s(?:${REGION}|${COUNTRY})\\b)`,
        'gu',
      ),
      // No comma before the state: "Farmington NM 87401", "Etobicoke ON M8V
      // 1J2"
      re(
        `\\b(?!(?:St|Ave|Rd|Dr|Blvd|Ln|Ct|Way|Pl|Hwy|N|S|E|W|NE|NW|SE|SW|Street|Avenue|Road|Drive|Lane|Court|Unit|Apt|Suite|Box)\\b)[A-Z][\\p{L}'’-]+(?: [A-Z][\\p{L}'’-]+)?(?= (?:${STATE_ABBR}|${PROVINCE_ABBR})\\s{1,2}(?:\\d{5}\\b|[A-Z]\\d[A-Z]\\s?\\d[A-Z]\\d))`,
        'gu',
      ),
      // "IN AND FOR THE COUNTY OF PIMA", "County of Lane"
      /(?<=\b(?:COUNTY|County) (?:OF|of) )[A-Z][\p{L}'’-]+(?: [A-Z][\p{L}'’-]+)?/gu,
      // The town before a British or Irish postcode: "Skipton BD23 2QR",
      // "Kendal, Cumbria LA9 4HT", "Galway H91 X4K7"
      /\b[A-Z][\p{L}'’-]+(?: [A-Z][\p{L}'’-]+)?(?=,? (?:[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}|[A-Z]\d{2} [A-Z0-9]{4})\b)/gu,
      // The suburb before an Australian state and postcode: "Marrickville NSW
      // 2204", "West End QLD 4101"
      /\b[A-Z][\p{L}'’-]+(?: [A-Z][\p{L}'’-]+)?(?= (?:NSW|VIC|QLD|TAS|ACT|WA|SA|NT) \d{4}\b)/gu,
      // The town after a continental postcode: "24200 Sarlat-la-Canéda", "48011
      // Bilbao"
      /(?<=(?:^|\n|,\s|[-–—]\s)\d{5}\s)\p{Lu}[\p{L}'’]+(?:[- ](?:la-|le-|de-|sur-|en-)?\p{Lu}?[\p{L}'’]+){0,3}(?=[\s,.;-]|$)/gu,
      // A witness or guardian "of" a town: "Marcus Tindall, of Hardeeville;"
      /(?<=\p{Ll},\sof\s)[A-Z][\p{L}'’-]+(?: [A-Z][\p{L}'’-]+)?(?=[;,.)])/gu,
      // A street named in lower case, or a Utah-style grid street, after "on"
      // or "at": "traffic stop on rivers ave", "the light at 3300 South"
      /(?<=\b(?:on|at|off)\s)(?:[a-z]+\s(?:rd|ave|st|blvd|hwy|ln|dr)\b|\d{3,5}\s(?:North|South|East|West)\b)/g,
      // A Dutch or German street with no number: "the letter goes to
      // Kruisstraat"
      /\b[A-Z][\p{L}]{2,}(?:straat|gracht|kade|laan|plein|singel|strasse|straße|gasse|platz|allee)\b(?!\s\d)/gu,
      // "FIFO out of Mackay", "based out of Tulsa"
      {
        re: /(?<=\bout\sof\s)[A-Z][\p{L}'’-]+(?:\s[A-Z][\p{L}'’-]+)?(?=[.,;)\s]|$)/gu,
        ok: s => !NOT_A_PLACE.test(s),
      },
      // The town a letter is written from, French style: "Sarlat, le 12
      // novembre 2025"
      /(?<=^|\n)\p{Lu}[\p{L}'’-]+(?=,\sle\s(?:1er|\d{1,2})\s)/gu,
      // A lake, river or valley by name: "40 acres on Stewart Lake"
      {
        re: /\b[A-Z][\p{L}'’-]+(?: [A-Z][\p{L}'’-]+)? (?:Lake|River|Creek|Island|Bay|Valley|Falls|Springs|Heights|Harbou?r|Beach)\b(?! [A-Z][a-z]+ (?:&|and) [A-Z])(?! (?:Road|Rd|Street|St|Avenue|Ave|Drive|Dr|Lane|Blvd|Boulevard|Way|Court|Ct|Place|Trail|Bank|Credit|Community|Senior|Medical|Hospital|Clinic|Inc|LLC|Ltd|Co|Corp)\b)/gu,
        ok: s =>
          !NOT_A_PLACE.test(s) &&
          !/^(?:The|On|At|In|Near|From|To|Of|And|Great Salt)\s/.test(s),
      },
      // A postal district after an address: "14 Usher's Quay,\nDublin 8"
      /(?<=,\s)[A-Z][a-z]{3,} \d{1,2}(?=[.,;]?\s|$)(?!\s?(?:am|pm|a\.m|p\.m|%))/g,
      // Where a flight went: "Airfare ATL-BDL r/t"
      re(
        `(?<=\\b(?:${ci('airfare|flight|flights|flew|fly|flying|air\\s+ticket|itinerary')})\\s(?:from\\s)?)[A-Z]{3}[-–/][A-Z]{3}(?:[-–/][A-Z]{3})?\\b`,
      ),
      // A street named without a house number: "the light at Culebra Rd and N.
      // Zarzamora St", "off Carlton Street"
      {
        re: re(
          `(?<![\\p{L}\\p{N}])(?:(?:N|S|E|W|North|South|East|West)\\.?${SPC})?[A-Z][\\p{L}'’-]+(?:${SPC}[A-Z][\\p{L}'’-]+)?${SPC}(?:(?:Street|Avenue|Road|Boulevard|Drive|Lane|Highway|Parkway)\\b|(?:St|Ave|Rd|Blvd|Dr|Ln|Hwy|Pkwy)\\b\\.?)(?![\\p{L}])`,
          'gu',
        ),
        ok: s =>
          !NOT_A_PLACE.test(s) &&
          !/^(?:On|At|Off|Near|From|To|Take|Via|Along|Down|Up|Cross|Corner|And|Or|The|This|That|Main\sSt\.)\s/.test(
            s,
          ) &&
          !/\bDr\.?$/.test(s),
      },
      {
        re: /\b(?:Route|Highway|Hwy|Interstate|State Road|County Road)\s\d{1,4}[A-Z]?\b|\bI-\d{1,3}\b|\bUS-\d{1,3}\b/g,
      },
      // "Kansas City", "Ho Chi Minh City"
      /\b(?!(?:In|At|To|From|Near|Of|For|And|Or|But|With|By|On|The|A|An|This|That|Our|Their|His|Her|Inner|Capital|Sister|Twin|Host|Home|Big|Any|Each|Every|Which|What)\b)(?:[A-Z][\p{L}'’-]+[^\S\n]){1,3}City\b/gu,
      // Where a federal court sits, in a caption: "WESTERN DISTRICT OF
      // WASHINGTON AT SEATTLE"
      /(?<=\bDISTRICT OF [A-Z]+(?: [A-Z]+)? AT )[A-Z]{3,}(?: [A-Z]{3,})?\b/g,
      re(
        `\\b[A-Z][\\p{L}'’-]+(?:\\s[A-Z][\\p{L}'’-]+)?\\s(?:County|Parish|Township|Borough)\\b`,
        'gu',
      ),
      // In capitals, as in a caption: "SUPERIOR COURT OF WASHINGTON FOR KING
      // COUNTY"
      /(?<=\b(?:FOR|OF|IN)\s)(?!THE\b|SAID\b|ANY\b|EACH\b|THIS\b|THAT\b)[A-Z]{3,}\s[A-Z]{3,}\sCOUNTY\b/g,
      /\b(?!THE\b|FOR\b|SAID\b|AND\b|ANY\b|EACH\b|THIS\b|THAT\b|SAME\b)[A-Z]{3,}\sCOUNTY\b/g,
      // The town a local court sits in: "Flagstaff Justice Court"
      {
        re: /\b[A-Z][\p{L}'’-]+(?:\s[A-Z][\p{L}'’-]+)?(?=\s(?:Justice|Municipal|Superior|Circuit|District|Family|Probate|Juvenile|City|Provincial)\sCourt\b)/gu,
        ok: s =>
          !NOT_A_PLACE.test(s) &&
          !NOT_A_COURT_TOWN.test(s) &&
          !JUST_A_REGION.test(s),
      },
      // The seat of a company written the continental way: "Nordsee Fischhandel
      // GmbH, Bremerhaven, IBAN ..."
      {
        re: /(?<=(?:\bGmbH|\bB\.V\.|\bN\.V\.|\bS\.A\.|\bS\.A\.S\.|\bSARL|\bS\.r\.l\.|\bS\.p\.A\.|\bKft\.?|\bOy|\bApS|\bA\/S|\bS\.L\.|\bPty Ltd),\s)[A-Z][\p{L}'’-]+(?:\s[A-Z][\p{L}'’-]+)?(?=[,.;)\n]|$)/gu,
        ok: s => !NOT_A_PLACE.test(s),
      },
      // Meeting-location context also covers small towns outside the city
      // gazetteer.
      {
        re: re(
          `(?<=\\b(?:met|meeting)\\s+in\\s+)[A-Z][\\p{L}'’-]+(?:\\s[A-Z][\\p{L}'’-]+){0,2}`,
          'gu',
        ),
        ok: s => !NOT_A_PLACE.test(s) && !JUST_A_REGION.test(s),
      },
      // "lives in Wenatchee", "moved to Tofino", "the Stourton depot", "our
      // Norfolk office"
      {
        re: re(
          `(?<=\\b(?:lives?|lived|living|resides?|resided|residing|located|based|moved|moving|relocated|relocating|born|raised|grew\\s+up|stationed|incarcerated|hospitalized|treated|seen|working|worked|works|travell?ed|flew|drove|returned|home|office|offices|branch|store|facility|plant|depot|warehouse|clinic|hospital|campus|property|properties|cabin|cottage|house|farm|ranch|land|acres|venue|court|courthouse|jail|prison|banks?|banked|banking|headquartered|domiciled|travel|trip|flight|holiday|vacation|staying|stays?|stayed|visiting|visited|visits?)\\s+(?:is\\s+|are\\s+|was\\s+|were\\s+)?(?:back\\s+|out\\s+|up\\s+|down\\s+|over\\s+)?(?:in|at|to|from|near|outside|outside\\s+of|around|of)\\s+(?:the\\s+)?)[A-Z][\\p{L}'’-]+(?:\\s[A-Z][\\p{L}'’-]+){0,2}`,
          'gu',
        ),
        ok: s => !NOT_A_PLACE.test(s) && !JUST_A_REGION.test(s),
      },
      {
        re: re(
          `(?<=\\b(?:its|our|the|their|his|her|a)\\s)[A-Z][\\p{L}'’-]+(?:\\s[A-Z][\\p{L}'’-]+)?(?=\\s(?:office|offices|branch|store|depot|warehouse|plant|facility|clinic|campus|location|yard|property|rental|cabin|home|house)\\b)`,
          'gu',
        ),
        ok: s => !NOT_A_PLACE.test(s),
      },
    ],
  ),
  d('region', 'Names', 'State or province', 'STATE', [
    // The code after a city: "Dallas, TX 75201", "Kelowna, BC"
    re(
      `(?<=[\\p{L}.],\\s{1,2})(?:${STATE_ABBR}|${PROVINCE_ABBR})(?=\\.?(?:,|\\t|\\s+\\d{5}\\b|\\s+[A-Z]\\d[A-Z]\\s?\\d|\\s*$|[.;)]))`,
      'gmu',
    ),
    re(`\\b(?:${STATE_NAME}|${PROVINCE_NAME})\\b`),
    // Australian states, with the postcode that follows: "Marrickville NSW
    // 2204"
    /\b(?:NSW|VIC|QLD|TAS|ACT|WA|SA|NT)(?= \d{4}\b)/g,
    // A city and state code at the end of a table cell: "Atlanta GA<tab>"
    re(`(?<=\\p{L} )(?:${STATE_ABBR}|${PROVINCE_ABBR})(?=\\t)`, 'gu'),
    // No comma after the city: "Winnipeg MB  R3C 3N9"
    re(
      `(?<=\\p{L} )(?:${STATE_ABBR}|${PROVINCE_ABBR})(?=\\s{1,2}(?:\\d{5}\\b|[A-Z]\\d[A-Z]\\s?\\d[A-Z]\\d))`,
      'gu',
    ),
    // The old abbreviations, as courts write them: "Westmoreland County, Pa.,
    // No. 2025-CV-03381"
    /(?<=,\s)(?:Pa|Cal|Calif|Fla|Tex|Ill|Mass|Mich|Minn|Wis|Wash|Ariz|Colo|Conn|Del|Ga|Ind|Kan|Ky|La|Md|Miss|Mo|Mont|Neb|Nev|Okla|Ore|Tenn|Va|Vt|Wyo|Ala|Ark|N\.Y|N\.J|N\.C|N\.M|N\.H|N\.D|S\.C|S\.D|W\.Va|D\.C|R\.I)\.(?=,|\s|$)/g,
    // In a rule citation: "Pa.R.C.P. 4007.1", "Fla. R. Civ. P."
    /\b(?:Pa|Cal|Fla|Tex|Ill|Mass|Mich|Minn|Wis|Wash|Ariz|Colo|Conn|Del|Ga|Ind|Kan|Ky|La|Md|Miss|Mo|Mont|Neb|Nev|Okla|Ore|Tenn|Va|Vt|Wyo|Ala|Ark)\.(?=\s?(?:R\.\s?(?:C|Civ|Crim|App|Evid|A)\.|C\.S\.|Stat\.|Code\b|Rev\.|Gen\.|Comp\.|Admin\.|Const\.))/g,
    // After a form label: "STATE: TN"
    re(
      `(?<=\\b(?:STATE|State|ST|PROVINCE|Province|PROV|Prov)\\.?\\)?\\s?:\\s?)(?:${STATE_ABBR}|${PROVINCE_ABBR})\\b`,
    ),
    // After the word "plate": "car plate CT AV-90217"
    re(`(?<=\\bplates?\\s+)(?:${STATE_ABBR}|${PROVINCE_ABBR})(?=\\s[A-Z0-9])`),
    // The state that issued a plate or a licence: "AZ plate CKH7R42", "TX DL#
    // 31874425"
    re(
      `\\b(?:${STATE_ABBR}|${PROVINCE_ABBR})(?=\\s(?:DL|plates?|licen[sc]e|tags?|driver|registration|reg\\.|registry|title|Attorney|Bar|withholding|unemployment|sales\\s+tax|notary|nurse|resident|income\\s+tax|state\\s+tax)\\b)`,
    ),
    /\b(?:NSW|VIC|QLD|TAS|ACT)(?=\s(?:driver|licen[sc]e|rego|registration|plates?)\b)/g,
    re(
      `(?<=\\b(?:tag|plate|plates|reg|rego|registration)\\b[^()\\n]{0,24}\\()(?:${STATE_ABBR}|${PROVINCE_ABBR})(?=\\))`,
    ),
    // In a caption: "SUPERIOR COURT OF WASHINGTON", "WESTERN DISTRICT OF
    // WASHINGTON"
    re(`(?<=\\b(?:OF|STATE OF)\\s)(?:${STATE_NAME.toUpperCase()})\\b`),
  ]),
];

/**
 * True when the text is a US state or Canadian province, by name or postal
 * code.
 * @param {string} s The text; surrounding whitespace is ignored.
 * @return {boolean} Whether the whole text is one region.
 */
export const isRegion = s => new RegExp(`^(?:${REGION})$`).test(s.trim());
