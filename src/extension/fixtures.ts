/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Fixed fictional text only; never populated from a paste, file
 * or chat history.
 */

/**
 * Fictional text with a name, a place, a health detail, an amount, an email
 * address and a record number.
 */
export const CATEGORY_TEST_TEXT =
  'Avery Bennett lives in Seattle. The patient has diabetes. Budget: $1,250. Email: avery@example.com. Record number: 42.';
/**
 * Fictional contact details followed by health details, used to test cloud
 * cleanup.
 */
export const CLOUD_TEST_TEXT =
  'Contact Avery Bennett at avery@example.com or (202) 555-0147.\n\nDiagnosis: type 2 diabetes. Treatment: metformin.';
/**
 * Public economic paragraph supplied for a regression test; no private
 * identifiers.
 */
export const GENERAL_TEST_TEXT =
  'As investors have pumped trillions of dollars into artificial intelligence companies, chipmakers and data center developers, the economy has come to rely on the industry as its primary — some would argue only — reliable driver of growth.';

/**
 * Fictional appliance instructions: quoted control labels are not client names.
 */
export const CONTROL_LABEL_TEST_TEXT =
  'Begin by disconnecting the appliance from the local ley line. Do not simply unplug the power cord from the wall; doing so without first soothing the machine’s internal gyroscope will cause the rinse-aid reservoir to flash-freeze. Instead, turn the dial three clicks past "Pots & Pans" until you reach the hidden "Sub-Zero Gentle" setting, then tap the latch twice with your tuning fork. Wait for a faint sighing sound from beneath the kickplate. Once the appliance has emotionally stabilized, pull the lower rack completely out and place it on the kitchen floor facing true north to prevent residual magnetism from warping the tine coatings.';

/**
 * Public appliance instructions supplied to reproduce a false identification
 * warning.
 */
export const APPLIANCE_TEST_TEXT = `Temperature
Hottest setting (Extra Hot or Hot): Ideal for heavily soiled, colorfast items. This setting is available only on specific cycles.
Second hottest setting (Hot): Suitable for whites and heavily soiled, colorfast items.
Middle setting (Warm): For colorfast items. Only the final rinse will be warm; other rinses will be cold to conserve energy.
Eco setting (Warm/Cold or Eco Warm): For moderately soiled, colorfast items, and most wrinkle-free items. This setting uses less energy than the Middle setting.
Second coldest setting (Cool or Cold): For brightly colored, very lightly soiled items. This setting may include hot water to achieve a temperature around 60 degrees Celsius if necessary.
Coldest setting (Cold or Tap Cold): Uses only cold water. On some models, you may need to select this by cycling the Temperature button until no indicators are lit. This setting does not use any hot water, regardless of the tap water temperature.
Spin
Extra High: Maximizes water removal. Avoid using with wrinkle-free or no-iron fabrics and do not overload the washer.
High: Best for sturdy garments like underwear, t-shirts, jeans, and sturdy cottons.
Medium: For jeans, wrinkle-free items, and synthetics.
Low: For delicate items requiring a gentle spin.
No Spin: Drains water without spinning. Suitable for extremely delicate items.
Rinse Hold: Pauses draining and spinning, keeping laundry in water. Deactivate to resume and complete the cycle. On most models, you need to select Rinse Hold by cycling the Spin setting until no indicators are lit.
Soil level
Extra Heavy: For extremely soiled loads.
Heavy: For heavily soiled loads.
Normal: Best for most loads, suitable for moderate soil.
Light: For lightly soiled loads.
Extra Light: For minimally soiled items.`;

const testContact =
  'Contact Avery Bennett at avery@example.com. Record number: 42.';
/**
 * Exactly 500 words, including fictional identifiers at the end to check
 * coverage.
 */
export const PASTE_500_TEST_TEXT =
  [
    GENERAL_TEST_TEXT,
    CONTROL_LABEL_TEST_TEXT,
    APPLIANCE_TEST_TEXT,
    CONTROL_LABEL_TEST_TEXT,
  ]
    .join(' ')
    .split(/\s+/)
    .slice(0, 500 - testContact.split(/\s+/).length)
    .join(' ') +
  ' ' +
  testContact;
