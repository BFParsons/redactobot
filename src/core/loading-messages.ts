/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Light-hearted lines shown while the on-device model starts,
 * which can take a minute or two. They are decoration: the real state is
 * announced separately, once, for screen readers.
 */

/** The lines, without the trailing ellipsis. */
export const LOADING_MESSAGES: readonly string[] = [
  'Calculating the square root of infinity',
  'Triangulating the parabolas',
  'Untangling the neural spaghetti',
  'Teaching electrons to keep secrets',
  'Sharpening the black markers',
  'Warming up the tiny robot brain',
  'Counting to a billion, twice',
  'Polishing the ones and zeros',
  'Asking the graphics card nicely',
  'Herding the tensors',
  'Alphabetizing the alphabet',
  'Defragmenting the daydreams',
  'Folding the matrices into swans',
  'Convincing the model it is a morning person',
  'Rounding pi to something friendlier',
  'Looking for the any key',
  'Brewing a pot of floating points',
  'Dusting off the attention heads',
  'Stretching before the heavy lifting',
  'Rehearsing the word "redacted"',
  'Checking under the couch for parameters',
  'Putting the bits back in order',
  'Whispering to the weights',
  'Reading the manual, finally',
  'Calibrating the suspicion meter',
  'Practising its poker face',
  'Loading the really big numbers first',
  'Unrolling the context window',
  'Inflating the vocabulary',
  'Aligning the sprockets of discretion',
  'Double-checking the triple checks',
  'Feeding the hamsters that power the fans',
  'Tuning the confidentiality antenna',
  'Locating the backup supply of common sense',
  'Counting the syllables in "anonymize"',
  'Spinning up the secret-keeping gears',
  'Translating from robot to human',
  'Ironing the wrinkles out of the latent space',
  'Negotiating with the cache',
  'Hiding the hiding places',
  'Waking the model gently, it bites',
  'Compiling a list of things to forget',
  'Converting coffee into inference',
  'Memorizing what not to remember',
  'Measuring twice, redacting once',
  'Borrowing a cup of memory from the neighbours',
  'Squinting at the fine print',
  'Shuffling the deck of probabilities',
  'Minding its own business, loudly',
  'Almost there, probably',
];

/** How long each line stays up, in milliseconds. */
export const MESSAGE_MS = 3600;

/** A fresh random order of the lines, so each wait reads differently. */
export function shuffledMessages(random: () => number = Math.random): number[] {
  const order = LOADING_MESSAGES.map((_, index) => index);
  for (let i = order.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    const held = order[i];
    order[i] = order[j];
    order[j] = held;
  }
  return order;
}

/**
 * The line to show `ms` into the wait. The first is always the plain `first`
 * line, so the user learns what is happening before the jokes start; after
 * that the shuffled lines play in order and come round again.
 */
export function loadingMessage(
  order: readonly number[],
  ms: number,
  first: string,
): string {
  const slot = Math.floor(Math.max(0, ms) / MESSAGE_MS);
  if (slot === 0 || order.length === 0) return first;
  return `${LOADING_MESSAGES[order[(slot - 1) % order.length]]}…`;
}

/**
 * Estimated progress of a cold start, 0 to 100. Chrome reports none while it
 * loads the model, so this eases towards 95% over the usual one to three
 * minutes and reaches 100 only when the model answers. It never goes back.
 */
export function warmPercent(ms: number, done: boolean): number {
  return done ? 100 : Math.round(95 * (1 - Math.exp(-Math.max(0, ms) / 60000)));
}
