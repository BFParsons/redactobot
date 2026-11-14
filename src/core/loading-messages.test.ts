/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';

import {
  LOADING_MESSAGES,
  loadingMessage,
  MESSAGE_MS,
  shuffledMessages,
  warmPercent,
} from './loading-messages';

describe('loading messages', () => {
  it('has fifty distinct lines', () => {
    expect(LOADING_MESSAGES).toHaveLength(50);
    expect(new Set(LOADING_MESSAGES).size).toBe(50);
    for (const line of LOADING_MESSAGES) {
      expect(line.length).toBeLessThanOrEqual(48);
      expect(line.endsWith('.')).toBe(false);
    }
  });

  it('shuffles every line into each order', () => {
    const order = shuffledMessages();
    expect([...order].sort((a, b) => a - b)).toEqual(
      LOADING_MESSAGES.map((_, i) => i),
    );
  });

  it('starts plainly, then plays each line once before repeating', () => {
    const order = shuffledMessages(() => 0.5);
    expect(loadingMessage(order, 0, 'Starting…')).toBe('Starting…');
    expect(loadingMessage(order, MESSAGE_MS - 1, 'Starting…')).toBe(
      'Starting…',
    );
    const seen = new Set<string>();
    for (let slot = 1; slot <= 50; slot++) {
      seen.add(loadingMessage(order, slot * MESSAGE_MS, 'Starting…'));
    }
    expect(seen.size).toBe(50);
    expect(loadingMessage(order, 51 * MESSAGE_MS, 'Starting…')).toBe(
      loadingMessage(order, MESSAGE_MS, 'Starting…'),
    );
  });

  it('estimates progress that only moves forward and never claims done early', () => {
    let last = -1;
    for (let ms = 0; ms <= 600_000; ms += 5000) {
      const pct = warmPercent(ms, false);
      expect(pct).toBeGreaterThanOrEqual(last);
      expect(pct).toBeLessThanOrEqual(95);
      last = pct;
    }
    expect(warmPercent(1000, true)).toBe(100);
  });
});
