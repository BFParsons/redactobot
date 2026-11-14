/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview "Waiting Room", an original eight-bar smooth-jazz loop played
 * while the on-device model starts. It is written here as data and synthesised
 * with the Web Audio API, so there is no audio file, no download and no
 * third-party recording or arrangement. Nothing is sent anywhere.
 */

/** One note to play: MIDI pitch, start and length in beats, and loudness. */
export interface JazzNote {
  voice: 'keys' | 'bass' | 'lead' | 'brush' | 'ride';
  /** MIDI note number. Unused by the percussion voices. */
  pitch: number;
  /** Start, in beats from the top of the bar (four beats to a bar). */
  beat: number;
  /** Length in beats. */
  beats: number;
  /** Loudness, 0 to 1. */
  level: number;
}

/** Beats per minute. Slow enough to be calm, quick enough to sway. */
export const TEMPO = 82;
/** Bars in the loop. */
export const BARS = 8;

// ii-V-I with a turnaround, then the same with a tritone substitution.
// Voicings are rootless, as a pianist would comp them over the bass.
const CHORDS: Array<{root: number; keys: number[]}> = [
  {root: 38, keys: [60, 64, 65, 69]}, // Dm9
  {root: 43, keys: [59, 64, 65, 69]}, // G13
  {root: 36, keys: [59, 62, 64, 67]}, // Cmaj9
  {root: 45, keys: [61, 65, 67, 72]}, // A7(#5)
  {root: 38, keys: [60, 64, 65, 69]}, // Dm9
  {root: 37, keys: [59, 63, 65, 67]}, // Db7(#11)
  {root: 36, keys: [59, 62, 64, 67]}, // Cmaj9
  {root: 36, keys: [57, 62, 64, 67]}, // C6/9
];

// The tune: [bar, beat, pitch, length]. Sparse, with room to breathe.
const MELODY: Array<[number, number, number, number]> = [
  [0, 0.5, 76, 1],
  [0, 1.5, 77, 0.5],
  [0, 2, 81, 1.75],
  [1, 0, 79, 0.5],
  [1, 0.66, 76, 0.5],
  [1, 1.5, 74, 2],
  [2, 0.5, 71, 0.5],
  [2, 1, 74, 0.5],
  [2, 1.66, 76, 2],
  [3, 1.5, 77, 0.5],
  [3, 2, 76, 0.5],
  [3, 2.66, 73, 1],
  [4, 0, 74, 1.5],
  [4, 2, 77, 0.5],
  [4, 2.66, 81, 1],
  [5, 0, 83, 0.75],
  [5, 1, 79, 0.5],
  [5, 1.66, 77, 1.5],
  [6, 0, 76, 3],
  [7, 1.5, 74, 0.5],
  [7, 2, 72, 0.5],
  [7, 2.66, 69, 1],
];

// Swing: the off-beat eighth lands two thirds of the way through the beat.
const SWUNG = 2 / 3;

/** Every note in one bar of the loop. The same bar always gives the same notes. */
export function jazzBar(bar: number): JazzNote[] {
  const index = ((bar % BARS) + BARS) % BARS;
  const chord = CHORDS[index];
  const next = CHORDS[(index + 1) % BARS];
  const notes: JazzNote[] = [];
  // Keys: a held chord on one, a soft push before three.
  for (const pitch of chord.keys) {
    notes.push({voice: 'keys', pitch, beat: 0, beats: 1.6, level: 0.5});
    notes.push({
      voice: 'keys',
      pitch,
      beat: 1 + SWUNG,
      beats: 2.2,
      level: 0.36,
    });
  }
  // Bass: root, fifth, then a step into the next chord.
  const approach = next.root > chord.root ? next.root - 1 : next.root + 1;
  notes.push({
    voice: 'bass',
    pitch: chord.root,
    beat: 0,
    beats: 1.5,
    level: 0.9,
  });
  notes.push({
    voice: 'bass',
    pitch: chord.root + 7,
    beat: 2,
    beats: 1,
    level: 0.7,
  });
  notes.push({voice: 'bass', pitch: approach, beat: 3, beats: 0.9, level: 0.6});
  // Brushes on two and four, a ride pattern with swung eighths.
  for (const beat of [1, 3]) {
    notes.push({voice: 'brush', pitch: 0, beat, beats: 0.4, level: 0.5});
  }
  for (const beat of [0, 1, 1 + SWUNG, 2, 3, 3 + SWUNG]) {
    notes.push({voice: 'ride', pitch: 0, beat, beats: 0.2, level: 0.22});
  }
  for (const [at, beat, pitch, beats] of MELODY) {
    if (at === index) {
      notes.push({voice: 'lead', pitch, beat, beats, level: 0.55});
    }
  }
  return notes;
}

const hertz = (pitch: number) => 440 * 2 ** ((pitch - 69) / 12);

type AudioContextConstructor = typeof AudioContext;

/** Plays the loop until stopped. Safe to construct where audio is missing. */
export class JazzPlayer {
  private context?: AudioContext;
  private master?: GainNode;
  private noise?: AudioBuffer;
  private timer?: ReturnType<typeof setInterval>;
  private nextBar = 0;
  private nextTime = 0;

  /** Whether music is playing now. */
  get playing(): boolean {
    return this.timer !== undefined;
  }

  /**
   * Start playing. Must be called from a click or key press, as browsers
   * require. Returns false where the browser has no Web Audio.
   */
  start(): boolean {
    if (this.playing) return true;
    const scope = globalThis as unknown as {
      AudioContext?: AudioContextConstructor;
      webkitAudioContext?: AudioContextConstructor;
    };
    const Context = scope.AudioContext ?? scope.webkitAudioContext;
    if (!Context) return false;
    const context = new Context();
    this.context = context;
    void context.resume();
    const master = context.createGain();
    master.gain.setValueAtTime(0, context.currentTime);
    master.gain.linearRampToValueAtTime(0.75, context.currentTime + 0.6);
    // A short, quiet echo stands in for a room.
    const echo = context.createDelay();
    echo.delayTime.value = 0.23;
    const feedback = context.createGain();
    feedback.gain.value = 0.22;
    master.connect(context.destination);
    master.connect(echo);
    echo.connect(feedback);
    feedback.connect(echo);
    feedback.connect(context.destination);
    this.master = master;
    const buffer = context.createBuffer(
      1,
      Math.floor(context.sampleRate / 2),
      context.sampleRate,
    );
    const samples = buffer.getChannelData(0);
    for (let i = 0; i < samples.length; i++) {
      samples[i] = Math.random() * 2 - 1;
    }
    this.noise = buffer;
    this.nextBar = 0;
    this.nextTime = context.currentTime + 0.1;
    this.schedule();
    this.timer = setInterval(() => this.schedule(), 200);
    return true;
  }

  /** Fade out and release the audio device. */
  stop(): void {
    if (this.timer === undefined) return;
    clearInterval(this.timer);
    this.timer = undefined;
    const context = this.context;
    const master = this.master;
    this.context = undefined;
    this.master = undefined;
    if (!context || !master) return;
    const now = context.currentTime;
    master.gain.cancelScheduledValues(now);
    master.gain.setValueAtTime(master.gain.value, now);
    master.gain.linearRampToValueAtTime(0, now + 0.5);
    setTimeout(() => void context.close().catch(() => {}), 700);
  }

  // Queue whole bars a little ahead of the clock, so timing stays steady even
  // when the page is busy loading the model.
  private schedule() {
    const context = this.context;
    if (!context) return;
    const beat = 60 / TEMPO;
    while (this.nextTime < context.currentTime + 1.2) {
      for (const note of jazzBar(this.nextBar)) {
        this.play(note, this.nextTime + note.beat * beat, note.beats * beat);
      }
      this.nextBar++;
      this.nextTime += 4 * beat;
    }
  }

  private play(note: JazzNote, at: number, length: number) {
    const context = this.context;
    const master = this.master;
    if (!context || !master) return;
    const gain = context.createGain();
    gain.connect(master);
    if (note.voice === 'brush' || note.voice === 'ride') {
      const source = context.createBufferSource();
      source.buffer = this.noise ?? null;
      const filter = context.createBiquadFilter();
      filter.type = note.voice === 'ride' ? 'highpass' : 'bandpass';
      filter.frequency.value = note.voice === 'ride' ? 7000 : 2200;
      source.connect(filter);
      filter.connect(gain);
      gain.gain.setValueAtTime(note.level * 0.25, at);
      gain.gain.exponentialRampToValueAtTime(0.001, at + length);
      source.start(at);
      source.stop(at + length + 0.05);
      return;
    }
    const filter = context.createBiquadFilter();
    filter.type = 'lowpass';
    filter.connect(gain);
    const tone = context.createOscillator();
    tone.frequency.value = hertz(note.pitch);
    tone.connect(filter);
    const end = at + length;
    if (note.voice === 'bass') {
      tone.type = 'triangle';
      filter.frequency.value = 420;
      gain.gain.setValueAtTime(0, at);
      gain.gain.linearRampToValueAtTime(note.level * 0.5, at + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, end + 0.15);
    } else if (note.voice === 'keys') {
      // Electric piano: a soft sine with a quiet bell an octave up.
      tone.type = 'sine';
      filter.frequency.value = 2600;
      const bell = context.createOscillator();
      bell.type = 'sine';
      bell.frequency.value = hertz(note.pitch + 12) * 1.003;
      const bellGain = context.createGain();
      bellGain.gain.setValueAtTime(0.22, at);
      bellGain.gain.exponentialRampToValueAtTime(0.001, at + 0.5);
      bell.connect(bellGain);
      bellGain.connect(filter);
      bell.start(at);
      bell.stop(end + 0.5);
      gain.gain.setValueAtTime(0, at);
      gain.gain.linearRampToValueAtTime(note.level * 0.2, at + 0.015);
      gain.gain.exponentialRampToValueAtTime(0.001, end + 0.4);
    } else {
      // Lead: a breathy reed, with vibrato that arrives late in the note.
      tone.type = 'sawtooth';
      filter.frequency.value = 1500;
      filter.Q.value = 2;
      const vibrato = context.createOscillator();
      vibrato.frequency.value = 5.2;
      const depth = context.createGain();
      depth.gain.setValueAtTime(0, at);
      depth.gain.linearRampToValueAtTime(5, at + Math.min(0.5, length));
      vibrato.connect(depth);
      depth.connect(tone.frequency);
      vibrato.start(at);
      vibrato.stop(end + 0.3);
      gain.gain.setValueAtTime(0, at);
      gain.gain.linearRampToValueAtTime(note.level * 0.16, at + 0.06);
      gain.gain.setValueAtTime(note.level * 0.16, Math.max(at + 0.06, end));
      gain.gain.exponentialRampToValueAtTime(0.001, end + 0.25);
    }
    tone.start(at);
    tone.stop(end + 0.5);
  }
}
