/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';

import {BARS, jazzBar, JazzPlayer} from './jazz';

describe('smooth jazz loop', () => {
  it('writes the same notes for the same bar, and loops after eight bars', () => {
    expect(jazzBar(3)).toEqual(jazzBar(3));
    expect(jazzBar(BARS + 2)).toEqual(jazzBar(2));
    expect(jazzBar(-1)).toEqual(jazzBar(BARS - 1));
  });

  it('keeps every note inside its bar, at a sensible pitch and loudness', () => {
    for (let bar = 0; bar < BARS; bar++) {
      const notes = jazzBar(bar);
      expect(notes.some(n => n.voice === 'bass')).toBe(true);
      expect(notes.filter(n => n.voice === 'keys').length).toBeGreaterThan(3);
      for (const note of notes) {
        expect(note.beat).toBeGreaterThanOrEqual(0);
        expect(note.beat).toBeLessThan(4);
        expect(note.beats).toBeGreaterThan(0);
        expect(note.level).toBeGreaterThan(0);
        expect(note.level).toBeLessThanOrEqual(1);
        if (note.voice !== 'brush' && note.voice !== 'ride') {
          expect(note.pitch).toBeGreaterThanOrEqual(33);
          expect(note.pitch).toBeLessThanOrEqual(88);
        }
      }
    }
  });

  it('has a melody across the loop', () => {
    const lead = Array.from({length: BARS}, (_, bar) => jazzBar(bar))
      .flat()
      .filter(n => n.voice === 'lead');
    expect(lead.length).toBeGreaterThan(15);
  });

  it('does nothing, without errors, where the browser has no audio', () => {
    const player = new JazzPlayer();
    expect(player.start()).toBe(false);
    expect(player.playing).toBe(false);
    player.stop();
  });
});
