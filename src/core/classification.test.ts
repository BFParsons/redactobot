/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

import {describe, expect, it} from 'vitest';
import {
  applyRedactions,
  buildDetections,
  NO_TOPICS,
  restore,
  type Detection,
} from './redact';

const ids = [
  'names',
  'places',
  'region',
  'street',
  'record',
  'sensitive_topics',
];
const empty = {people: [], companies: []};
const at = (ds: Detection[], text: string) => ds.filter(d => d.text === text);

describe('categories without relaxing redaction', () => {
  it('keeps Seattle separate from a clinic named after the city, including inferred short forms', () => {
    const text =
      'Visit Seattle Children’s Clinic in Seattle, WA 98101. The family keeps a Seattle address.';
    const ds = buildDetections(
      text,
      ids,
      {people: ['Seattle'], companies: ['Seattle Children’s Clinic']},
      [],
      new Set(),
      {...NO_TOPICS, places: ['Seattle']},
    );
    expect(at(ds, 'Seattle').map(d => d.kind)).toEqual(['places', 'places']);
    expect(at(ds, 'Seattle').every(d => d.enabled)).toBe(true);
    expect(at(ds, 'Seattle Children’s Clinic')[0].kind).toBe('company');
    const red = applyRedactions(text, ds);
    const city = at(ds, 'Seattle').map(d => red.placeholders.get(d.id));
    expect(new Set(city).size).toBe(1);
    expect(city[0]).toMatch(/^PLACE_/);
    expect(restore(red.cleaned, red.map)).toContain('a Seattle address');
  });

  it('uses address evidence even when the model has not returned places', () => {
    const text =
      'Seattle Children’s Clinic, Seattle, WA 98101. They kept their Seattle address.';
    const ds = buildDetections(text, ids, {
      ...empty,
      companies: ['Seattle Children’s Clinic'],
    });
    expect(at(ds, 'Seattle').map(d => d.kind)).toEqual(['places', 'places']);
    expect(at(ds, 'Seattle Children’s Clinic')[0].kind).toBe('company');
  });

  it('shares a city placeholder across capitalization without restoring the clinic name', () => {
    const text =
      'Seattle Children’s Clinic, SEATTLE, WA 98101. They kept their Seattle address.';
    const ds = buildDetections(text, ids, {
      ...empty,
      companies: ['Seattle Children’s Clinic'],
    });
    const cities = ds.filter(d => d.text.toLowerCase() === 'seattle');
    expect(cities).toHaveLength(2);
    expect(cities.every(d => d.kind === 'places' && d.enabled)).toBe(true);
    const red = applyRedactions(text, ds);
    const placeholders = cities.map(d => red.placeholders.get(d.id)!);
    expect(new Set(placeholders).size).toBe(1);
    expect(red.map.get(placeholders[0])?.toLowerCase()).toBe('seattle');
  });

  it('distinguishes a person and a place with the same name', () => {
    const text =
      'Jordan Vale lives in Jordan, MN 55352. Jordan called yesterday.';
    const ds = buildDetections(
      text,
      ids,
      {people: ['Jordan Vale', 'Jordan'], companies: []},
      [],
      new Set(),
      {...NO_TOPICS, places: ['Jordan']},
    );
    expect(at(ds, 'Jordan').map(d => d.kind)).toEqual(['places', 'person']);
    expect(at(ds, 'Jordan Vale')[0].kind).toBe('person');
    expect(ds.every(d => d.enabled)).toBe(true);
  });

  it('keeps an organization alias in an organization context and a city in a location context', () => {
    const text =
      'Seattle Logistics LLC ("Seattle") approved the invoice. Seattle invoiced us. We live in Seattle, WA 98101.';
    const ds = buildDetections(
      text,
      ids,
      {...empty, companies: ['Seattle Logistics LLC']},
      [],
      new Set(),
      {...NO_TOPICS, places: ['Seattle']},
    );
    expect(at(ds, 'Seattle').map(d => d.kind)).toEqual([
      'company',
      'company',
      'places',
    ]);
  });

  it('retains a clinic short form when the sentence refers to its department', () => {
    const text =
      'Seattle Children’s Clinic is in Seattle, WA 98101. The emergency department at Seattle treated her.';
    const ds = buildDetections(
      text,
      ids,
      {...empty, companies: ['Seattle Children’s Clinic']},
      [],
      new Set(),
      {...NO_TOPICS, places: ['Seattle']},
    );
    expect(at(ds, 'Seattle').map(d => d.kind)).toEqual(['places', 'company']);
  });

  it('recategorizes diagnoses and ICD codes while keeping them selected for replacement', () => {
    const text =
      'Dr. Mira Calder treated Chronic Lumbar Radiculopathy and Bronchial Asthma (ICD-10: J45.41).';
    const ds = buildDetections(
      text,
      ids,
      {
        people: [
          'Mira Calder',
          'Chronic Lumbar Radiculopathy',
          'Bronchial Asthma',
        ],
        companies: [],
      },
      [],
      new Set(),
      {
        ...NO_TOPICS,
        health: ['Chronic Lumbar Radiculopathy', 'Bronchial Asthma', 'J45.41'],
      },
    );
    for (const phrase of [
      'Chronic Lumbar Radiculopathy',
      'Bronchial Asthma',
      'J45.41',
    ]) {
      expect(at(ds, phrase)[0], phrase).toMatchObject({
        kind: 'health',
        base: 'HEALTH_DETAIL',
        defaultOn: true,
        enabled: true,
      });
    }
    expect(at(ds, 'Mira Calder')[0].kind).toBe('person');
    expect(applyRedactions(text, ds).cleaned).not.toContain('Bronchial Asthma');
  });

  it('recognizes clinical phrases without needing the model to classify them', () => {
    const text =
      'She developed Bronchial Asthma and Post-Traumatic Stress Disorder.';
    const ds = buildDetections(text, ids, empty);
    const names = ds.filter(d => d.kind === 'person' || d.kind === 'company');
    expect(names).toEqual([]);
    expect(ds.some(d => d.kind === 'health' && d.enabled)).toBe(true);
  });

  it('preserves medical organizations, people, and actual record IDs', () => {
    const text =
      'Dr. James Parkinson at Asthma Research Foundation reviewed case no. J45.41.';
    const ds = buildDetections(
      text,
      ids,
      {people: ['James Parkinson'], companies: ['Asthma Research Foundation']},
      [],
      new Set(),
      {...NO_TOPICS, health: ['Parkinson', 'Asthma']},
    );
    expect(at(ds, 'James Parkinson')[0].kind).toBe('person');
    expect(at(ds, 'Asthma Research Foundation')[0].kind).toBe('company');
    expect(at(ds, 'J45.41')[0].kind).toBe('record');
  });

  it('labels generic headings and billing descriptions without uncovering them', () => {
    const text =
      'Primary Applicant\nCase Worker\nInpatient Room & Board\t$200\nDiagnostic Imaging\t$300\nAttestation & Digital Signatures';
    const ds = buildDetections(text, ids, {
      people: ['Primary Applicant', 'Case Worker'],
      companies: [
        'Inpatient Room & Board',
        'Diagnostic Imaging',
        'Attestation & Digital Signatures',
      ],
    });
    for (const phrase of [
      'Primary Applicant',
      'Case Worker',
      'Attestation & Digital Signatures',
    ]) {
      expect(at(ds, phrase)[0], phrase).toMatchObject({
        kind: 'other',
        base: 'REDACTED',
        enabled: true,
      });
    }
    for (const phrase of ['Inpatient Room & Board', 'Diagnostic Imaging']) {
      expect(at(ds, phrase)[0], phrase).toMatchObject({
        kind: 'health',
        base: 'HEALTH_DETAIL',
        enabled: true,
      });
    }
  });

  it('keeps an explicitly named diagnostic imaging provider as an organization', () => {
    const text =
      'Diagnostic Imaging LLC sent the bill. Contact Diagnostic Imaging about it.';
    const ds = buildDetections(text, ids, {
      ...empty,
      companies: ['Diagnostic Imaging LLC'],
    });
    expect(at(ds, 'Diagnostic Imaging LLC')[0].kind).toBe('company');
    expect(at(ds, 'Diagnostic Imaging')[0].kind).toBe('company');
  });

  it('corrects a company alias mislabelled as a person', () => {
    const text =
      'Harbourlight Health Insurance reviewed the claim. Harbourlight Health approved it.';
    const ds = buildDetections(text, ids, {
      people: ['Harbourlight Health'],
      companies: ['Harbourlight Health Insurance'],
    });
    expect(at(ds, 'Harbourlight Health')[0].kind).toBe('company');
    const red = applyRedactions(text, ds);
    expect(red.placeholders.get(at(ds, 'Harbourlight Health')[0].id)).toBe(
      red.placeholders.get(at(ds, 'Harbourlight Health Insurance')[0].id),
    );
  });

  it('preserves a manual category and the user’s keep-as-written choice', () => {
    const text =
      'Seattle Children’s Clinic in Seattle, WA 98101. She developed Bronchial Asthma.';
    const names = {
      people: ['Bronchial Asthma'],
      companies: ['Seattle Children’s Clinic'],
    };
    const topics = {
      ...NO_TOPICS,
      places: ['Seattle'],
      health: ['Bronchial Asthma'],
    };
    const initial = buildDetections(text, ids, names, [], new Set(), topics);
    const health = at(initial, 'Bronchial Asthma')[0];
    const again = buildDetections(
      text,
      ids,
      names,
      [{text: 'Seattle', kind: 'person'}],
      new Set([health.id]),
      topics,
    );
    expect(
      at(again, 'Seattle').every(
        d => d.kind === 'person' && d.source === 'manual',
      ),
    ).toBe(true);
    expect(at(again, 'Bronchial Asthma')[0]).toMatchObject({
      kind: 'health',
      defaultOn: true,
      enabled: false,
      id: health.id,
    });
  });

  it('requires grounded evidence before accepting conflicting model topic labels', () => {
    const text =
      'Amity Harrow works for Riverbend Builders LLC. Amity attends St. Briar Academy. Riverbend is the general contractor.';
    const ds = buildDetections(
      text,
      ids,
      {
        people: ['Amity Harrow', 'Amity'],
        companies: ['Riverbend Builders LLC', 'St. Briar Academy'],
      },
      [],
      new Set(),
      {
        places: ['Amity Harrow', 'Riverbend Builders LLC', 'Riverbend'],
        health: ['St. Briar Academy'],
        sensitive: ['Amity'],
        names: [],
      },
    );
    expect(at(ds, 'Amity Harrow')[0].kind).toBe('person');
    expect(at(ds, 'Amity').every(d => d.kind === 'person')).toBe(true);
    expect(at(ds, 'Riverbend')[0].kind).toBe('company');
    expect(at(ds, 'Riverbend Builders LLC')[0].kind).toBe('company');
    expect(at(ds, 'St. Briar Academy')[0].kind).toBe('company');
  });

  it('does not turn a surname into an organization through an uppercase alias', () => {
    const text =
      'Oren Hargrove owns HARGROVE TOOL & DIE LLC. Hargrove will attend.';
    const ds = buildDetections(text, ids, {
      people: ['Oren Hargrove'],
      companies: ['HARGROVE TOOL & DIE LLC'],
    });
    expect(at(ds, 'Hargrove')[0].kind).toBe('person');
  });

  it('does not mistake an employee ID for an Idaho postal address', () => {
    const text =
      'Reported by\tMalik Farrow, ID 20418\nRespondent\tTobin Harrow, ID 17733';
    const ds = buildDetections(
      text,
      ids,
      {people: ['Malik Farrow', 'Tobin Harrow'], companies: []},
      [],
      new Set(),
      {...NO_TOPICS, places: ['Malik Farrow', 'Tobin Harrow']},
    );
    expect(at(ds, 'Malik Farrow')[0].kind).toBe('person');
    expect(at(ds, 'Tobin Harrow')[0].kind).toBe('person');
  });

  it('labels insurance adjustments and copay descriptions as billing text', () => {
    const text =
      'Contractual Insurance\t-$250.00\nOut-of-Pocket Co-Payments\t$100.00';
    const ds = buildDetections(text, ids, {
      ...empty,
      companies: ['Contractual Insurance', 'Out-of-Pocket Co'],
    });
    for (const phrase of ['Contractual Insurance', 'Out-of-Pocket Co']) {
      expect(at(ds, phrase)[0]).toMatchObject({
        kind: 'other',
        label: 'Billing description',
        enabled: true,
      });
    }
  });
});
