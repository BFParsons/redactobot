/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Everyday words and large place names that people capitalize
 * without meaning a person: "this Past Weekend", "Game Seven", "Happy New
 * Year", "South America". The name rules use these to veto guesses that rest
 * only on capital letters.
 *
 * Words that are also common first names (Hope, Grace, Rose, Summer, Mark,
 * Will) are deliberately left out, so those names are still found. Countries
 * that are common first names (Jordan, Georgia, Chad, Israel) are left out of
 * the geography list for the same reason.
 */

/** Everyday English words, in lower case. */
export const COMMON_WORDS = new Set(
  // Time
  (
    'past present future weekend weekends week weeks weekday month months year years decade century ' +
    'today tomorrow yesterday tonight morning afternoon evening night nights noon midnight midday ' +
    'day days hour hours minute minutes second seconds moment season seasons holiday holidays vacation ' +
    'birthday anniversary break recess semester term quarter deadline schedule ' +
    // Numbers and order
    'one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty hundred ' +
    'thousand million billion half double triple single couple several many few more most less least ' +
    'sixth seventh eighth ninth tenth zero ' +
    // Describing words
    'good great big small little large huge tiny happy merry sad glad sorry best better worst top bottom ' +
    'free open closed full empty high low long short early late quick fast slow real true false final ' +
    'major minor public private local global digital modern classic basic advanced simple easy hard ' +
    'hot cold warm cool dark light bright black white red blue green yellow orange purple pink gold ' +
    'silver grey gray brown clean dirty wet dry heavy strong weak poor safe secure ready busy ' +
    'important urgent official personal professional original popular famous favorite favourite ' +
    'whole entire complete partial extra super ultra mega mini maximum minimum average normal standard ' +
    'right wrong left correct proper possible impossible likely actual recent ancient young fresh ' +
    'awesome amazing wonderful beautiful lovely nice fine perfect terrible awful strange weird funny ' +
    'serious crazy wild quiet loud ' +
    // People, in general
    'people person man men woman women kid kids child children boy boys girl girls guys friend ' +
    'friends mom dad mother father parent parents brother sister son daughter husband wife ' +
    'uncle aunt cousin grandma grandpa baby babies neighbor neighbour boss coworker colleague team ' +
    'teams crew staff squad group groups club community crowd audience guest guests host hosts ' +
    'everyone everybody someone somebody anyone anybody nobody ' +
    // Things and places, in general
    'world earth country countries nation land sea lake beach island mountain mountains ' +
    'forest desert sun moon stars space planet weather rain snow wind storm fire water ' +
    'house home apartment room kitchen garden yard garage door window table chair bed desk ' +
    'school college university campus library museum church temple theater theatre stadium arena ' +
    'airport station restaurant cafe bar hotel store shop mall market gym pool ' +
    'car bus train plane flight boat bike ticket trip tour travel journey drive ride walk run ' +
    'food dinner lunch breakfast brunch coffee tea beer wine pizza burger cake ' +
    'game games match season playoffs finals championship league score win loss draw goal ' +
    'movie movies film show shows series episode podcast song album music video book books story ' +
    'news article post blog page site website app phone computer laptop internet ' +
    // Work and school
    'project projects plan plans report reports meeting update updates summary list item items ' +
    'question questions answer answers problem problems issue issues idea ideas thing things stuff ' +
    'job jobs career work task tasks goal goals result results data design product products ' +
    'system systems model process program programme course lesson test exam grade level stage ' +
    'phase step steps version edition volume chapter session event events party parties ' +
    'conference workshop seminar webinar presentation interview deal price cost budget money cash ' +
    'business company industry service services support help info information details overview ' +
    'introduction conclusion background experience research study studies analysis review reviews ' +
    'feedback request response reply message messages comment comments announcement reminder ' +
    // Doing words, often capitalized in headings
    'welcome hello hi hey goodbye bye congratulations congrats cheers thank thanks ' +
    'get got go going went come came see saw look watch read write make made take took give gave ' +
    'start started begin end ended finish finished stop wait keep let try need want like love hate ' +
    'know think feel say said tell told ask asked call called meet met find found send sent ' +
    'buy sell pay play learn teach build fix check join leave move change save share follow ' +
    'coming soon now later always never again also just only still even very really ' +
    // Small words
    'the and but for nor yet with without about above below over under after before during until ' +
    'into onto from than then when where what who why how here there our your their his her its ' +
    'you they them she him was were are been being have has had does did can could should would ' +
    'might must shall ' +
    // Nationalities and languages not already listed elsewhere
    'african asian australian indian japanese korean russian italian irish scottish welsh dutch ' +
    'swiss swedish polish greek turkish arab arabic latin hispanic brazilian egyptian israeli ' +
    'pakistani vietnamese thai filipino nigerian portuguese'
  ).split(' '),
);

/** Continents, large regions and countries that are rarely a person's name. */
export const GEOGRAPHY = new Set(
  (
    'america americas africa antarctica asia australia europe eurasia oceania ' +
    'caribbean scandinavia balkans mediterranean pacific atlantic arctic midwest ' +
    'canada mexico brazil argentina chile peru colombia venezuela ecuador bolivia uruguay paraguay ' +
    'cuba jamaica haiti bahamas panama guatemala honduras nicaragua ' +
    'england scotland wales ireland britain france germany spain portugal italy netherlands ' +
    'belgium switzerland austria denmark norway sweden finland iceland poland ukraine russia ' +
    'greece turkey hungary romania bulgaria serbia croatia czechia slovakia ' +
    'egypt morocco algeria tunisia libya nigeria ghana kenya ethiopia tanzania uganda zimbabwe ' +
    'china japan korea india pakistan bangladesh nepal thailand vietnam cambodia malaysia ' +
    'indonesia philippines singapore taiwan mongolia afghanistan iran iraq syria lebanon ' +
    'kuwait qatar oman yemen arabia zealand lanka'
  ).split(' '),
);

const PLACE_MODIFIERS = new Set(
  'north south east west northern southern eastern western central latin new saudi the of'.split(
    ' ',
  ),
);
const WHOLE_COUNTRIES = new Set([
  'united states',
  'united states of america',
  'united kingdom',
  'usa',
  'u.s.',
  'u.s.a.',
  'uk',
  'u.k.',
]);

/**
 * Whether a place name is a country, a continent or a region of one ("South
 * America", "Western Europe", "the United States"). These are far larger than
 * a state, so the check for places smaller than a state leaves them alone.
 */
export function isLargePlace(name: string): boolean {
  const words = name.toLowerCase().replace(/\s+/g, ' ').trim();
  if (WHOLE_COUNTRIES.has(words.replace(/^the /, ''))) return true;
  const parts = words.split(' ');
  return (
    parts.some(w => GEOGRAPHY.has(w)) &&
    parts.every(w => GEOGRAPHY.has(w) || PLACE_MODIFIERS.has(w))
  );
}
