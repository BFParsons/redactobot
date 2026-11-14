/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview TEST BUILD ONLY. Replaces Chrome's on-device model in the
 * extension's offscreen scanner with a deterministic stand-in, so the paste
 * flow can be tested in Chromium builds that have no Gemini Nano. Never
 * included in `npm run build:extension`.
 */

(() => {
  // Fictional entities the fake "model" recognizes, with the kind it reports.
  const ENTITIES = [
    ['Margaret Whitfield', 'person'],
    ['Tom Whitfield', 'person'],
    ['Priya Raman', 'person'],
    ['Harbourline Marine Supply', 'company'],
    ['Northgate Bookkeeping', 'company'],
    ['Tofino', 'place'],
    ['diabetes', 'health'],
    ['Quillon', 'uncertain_person'],
  ];
  const text = contents => JSON.stringify(contents);
  class Session {
    contextWindow = 9216;
    contextUsage = 700;
    async prompt(contents) {
      const input = text(contents);
      if (input.includes('E2E_MODEL_FAIL')) {
        throw new Error('Fake on-device model failure.');
      }
      if (input.includes('E2E_MODEL_SLOW')) {
        await new Promise(r => setTimeout(r, 4000));
      }
      const active = (input.match(/Active categories: ([^.]*)\./) || [
        '',
        '',
      ])[1].split(', ');
      const found = ENTITIES.filter(
        ([name, kind]) =>
          input.includes(name) &&
          active.includes(kind.replace('uncertain_', '')),
      ).map(([name, kind]) => `${kind}: ${name}`);
      return JSON.stringify(found);
    }
    async measureContextUsage(value) {
      return Math.ceil(String(value).length / 4);
    }
    async clone() {
      return new Session();
    }
    destroy() {}
  }
  const FakeLanguageModel = {
    async availability() {
      return 'available';
    },
    async create() {
      return new Session();
    },
    async params() {
      return {
        defaultTopK: 3,
        maxTopK: 8,
        defaultTemperature: 1,
        maxTemperature: 2,
      };
    },
  };
  Object.defineProperty(globalThis, 'LanguageModel', {
    value: FakeLanguageModel,
    configurable: true,
    writable: true,
  });
})();
