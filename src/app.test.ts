/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {beforeEach, describe, expect, it} from 'vitest';
import './app';
import {
  ACCURACY_TIERS,
  DATA_CLASSES,
  DEFAULT_CLASSES,
} from '../taxonomy/taxonomy.js';
import {SAMPLE} from './core/sample';

// The Material components are not registered here, so they are plain elements:
// enough to check what the app puts on the page and what it does with a choice.
// How it looks is checked in Chrome.
type App = HTMLElement & {updateComplete: Promise<boolean>} & Record<
    string,
    any
  >;

async function mount(): Promise<App> {
  document.body.innerHTML = '';
  const app = document.createElement('redactobot-app') as App;
  document.body.append(app);
  await app.updateComplete;
  return app;
}
const texts = (root: Element, selector: string) =>
  [...root.querySelectorAll(selector)].map(e =>
    e.textContent!.replace(/\s+/g, ' ').trim(),
  );

describe('choosing what to replace by type of data', () => {
  beforeEach(() => localStorage.clear());

  it('lists every type under its tier, most accurate first, with the measured rate', async () => {
    const app = await mount();
    await app.updateComplete;
    expect(texts(app, '.tier-head h3')).toEqual([
      ...ACCURACY_TIERS.map(t => t.label),
      'Flagged, not replaced',
    ]);
    expect(texts(app, 'label.pick-row > span:not(.rate)')).toEqual(
      DATA_CLASSES.map(c => c.label),
    );
    const rates = texts(app, 'label.pick-row .rate');
    expect(rates.length).toBe(DATA_CLASSES.length);
    // never a claim of perfection
    expect(rates.some(r => r.includes('100'))).toBe(false);
    const numbers = rates.slice(0, -1).map(r => parseInt(r, 10));
    // ranked from most to least accurate
    expect([...numbers].sort((a, b) => b - a)).toEqual(numbers);
    expect(rates[rates.length - 1]).toMatch(/flagged$/);
  });

  it('runs only the checks of the types that are ticked', async () => {
    const app = await mount();
    app.text = SAMPLE;
    app.setClasses(['phone', 'email']);
    await app.updateComplete;
    expect(app.plan.detectorIds).toEqual(['email', 'phone']);
    expect(app.plan.usesModel).toBe(false);
    expect(app.detections.map((d: {kind: string}) => d.kind).sort()).toEqual([
      'email',
      'phone',
    ]);
    expect(texts(app, 'p[role=status]')[0]).toContain('2 instant checks');
  });

  it('quick picks select by tier, and nothing chosen blocks the Find button', async () => {
    const app = await mount();
    app.text = SAMPLE;
    await app.updateComplete;
    const chips = [
      ...app
        .querySelectorAll('details.pick-section')[0]
        .querySelectorAll('md-filter-chip'),
    ] as HTMLElement[];
    expect(chips.map(c => c.getAttribute('label'))).toEqual([
      'Highly accurate only',
      'Highly accurate and accurate',
      'Everything',
    ]);
    chips[0].click();
    await app.updateComplete;
    const high = DATA_CLASSES.filter(
      c => c.tier === 'high' || c.action === 'flag',
    ).map(c => c.id);
    expect([...app.classes].sort()).toEqual([...high].sort());
    app.setClasses([]);
    await app.updateComplete;
    expect(texts(app, 'p[role=status]')[0]).toBe(
      'Choose at least one type of data.',
    );
    expect(
      app.querySelector('md-filled-button')!.hasAttribute('disabled'),
    ).toBe(true);
  });

  it('remembers the ticked types', async () => {
    let app = await mount();
    app.setClasses(['money', 'names']);
    app = await mount();
    expect([...app.classes]).toEqual(['money', 'names']);
    expect(DEFAULT_CLASSES.length).toBe(DATA_CLASSES.length);
  });

  it('regulations are shortcuts that tick and untick the data types they require', async () => {
    const app = await mount();
    expect([...app.rules]).toEqual([]); // every box starts blank, never a dash
    app.setClasses([]);
    app.toggleRule('pci', true);
    await app.updateComplete;
    expect(app.classes.has('card')).toBe(true);
    expect(app.rules.has('pci')).toBe(true);
    app.toggleClass([...app.classes][0], false);
    // a required type went off: the box is blank again
    expect(app.rules.has('pci')).toBe(false);
    app.setClasses([]);
    app.toggleRule('pci', true);
    app.toggleRule('pci', false);
    expect(app.rules.has('pci')).toBe(false);
    // alone, unticking removes the types it added
    expect(app.classes.size).toBe(0);
    app.toggleRule('frcp52', true);
    app.toggleRule('hipaa', true);
    app.toggleRule('hipaa', false);
    expect(app.rules.has('hipaa')).toBe(false); // unticking always unticks
    // types another ticked rule needs stay on
    expect(app.rules.has('frcp52')).toBe(true);
    await app.updateComplete;
    expect(app.querySelector('md-checkbox[indeterminate]')).toBeNull();
  });

  it('with every type on, a regulation can still be ticked and unticked', async () => {
    const app = await mount();
    app.toggleRule('glba', true);
    app.toggleRule('ccpa', true);
    app.toggleRule('glba', false);
    expect([...app.rules]).toEqual(['ccpa']);
    // types that were already on stay on
    expect(app.classes.size).toBe(DATA_CLASSES.length);
  });

  it('lists FOIA release under Regulatory and switches the output with it', async () => {
    const app = await mount();
    app.setClasses(['money']);
    app.toggleFoia(true);
    await app.updateComplete;
    expect(app.output).toBe('foia');
    expect(app.classes.size).toBe(DATA_CLASSES.length);
    expect(
      app.querySelector('md-checkbox[aria-label="FOIA release (US)"]'),
    ).not.toBeNull();
    expect(
      app.querySelector('md-filter-chip[label="Law practice"]'),
    ).toBeNull(); // audience shortcuts are gone
    app.toggleFoia(false);
    expect(app.output).toBe('ai');
  });

  it('opens Data type and keeps Regulatory collapsed to begin with', async () => {
    const app = await mount();
    const sections = [
      ...app.querySelectorAll('details.pick-section'),
    ] as HTMLDetailsElement[];
    expect(
      sections.map(
        d => d.querySelector('summary .md-typescale-title-small')!.textContent,
      ),
    ).toEqual(['Data type', 'Regulatory']);
    expect(sections.map(d => d.open)).toEqual([true, false]);
  });
});

describe('verdict after a scan', () => {
  it('is green only when nothing is left in doubt, otherwise orange with the reason', async () => {
    const app = await mount();
    app.text = 'please email margaret@whitfield.example about the invoice.';
    app.view = 'review';
    app.scan = {state: 'done'};
    app.scanErrors = 0;
    await app.updateComplete;
    expect(app.querySelector('.verdict.clean')?.textContent).toContain(
      'Your text looks clean',
    );
    expect(app.querySelector('md-primary-tab')?.textContent).toBe(
      'Cleaned text',
    );
    app.scanErrors = 1;
    await app.updateComplete;
    expect(app.querySelector('.verdict.review')?.textContent).toContain(
      'names were not fully checked',
    );
    app.scanErrors = 0;
    app.text = 'please note the client has diabetes.';
    await app.updateComplete;
    expect(app.querySelector('.verdict.review')?.textContent).toContain(
      'cloud cleanup',
    );
  });
});

describe('flagged details in the cleaned text', () => {
  it('shows a flagged, unremoved detail in red, and a click removes it', async () => {
    const app = await mount();
    app.text = 'please note the client has diabetes.';
    app.view = 'review';
    app.scan = {state: 'done'};
    app.scanErrors = 0;
    app.anim = null;
    await app.updateComplete;
    const flagged = app.querySelector('.flagged-detail') as HTMLElement;
    expect(flagged?.textContent).toBe('diabetes');
    flagged.click();
    await app.updateComplete;
    expect(app.querySelector('.flagged-detail')).toBeNull();
    expect(app.querySelector('.doc .ph')?.textContent).toMatch(/^\[HEALTH/);
  });
});
