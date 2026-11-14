/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {afterEach, beforeEach, expect, it, vi} from 'vitest';
import {NO_TOPICS} from './core/redact';
import {applyCloudCleanup, takeCloudText} from './core/cloud-gate';
const fake = vi.hoisted(() => ({
  extract: vi.fn(),
  cleanup: vi.fn(),
  ask: vi.fn(),
}));
vi.mock('./extension/model', () => ({
  prepareModel: async () => {},
  extract: (...args: any[]) => fake.extract(...args),
}));
vi.mock('./core/cloud-client', () => ({
  cloudSetupProblem: () => undefined,
  cleanupCloud: (...args: any[]) => fake.cleanup(...args),
  askCloud: (...args: any[]) => fake.ask(...args),
}));
vi.mock('./core/ai', () => ({
  deviceStatus: async () => 'available',
  detectNames: vi.fn(),
  detectTopics: vi.fn(),
  prepareDevice: vi.fn(),
  warmDevice: async () => {},
  wakeDevice: async () => {},
}));
import {RedactobotApp} from './app';
let app: any;
beforeEach(() => {
  vi.clearAllMocks();
  vi.spyOn(window, 'scrollTo').mockImplementation(() => {});
  fake.extract.mockResolvedValue({
    names: {people: ['Avery Bennett'], companies: []},
    topics: {...NO_TOPICS, health: ['diabetes']},
    ambiguous: [],
    identifying: [],
  });
  fake.cleanup.mockImplementation(async input =>
    applyCloudCleanup(input, {complete: true, findings: []}),
  );
  fake.ask.mockImplementation(async input => {
    takeCloudText(input);
    return 'A fictional answer.';
  });
  app = new RedactobotApp();
  app.text = 'Avery Bennett has diabetes.';
  app.question = 'Send the summary to contact@example.com.';
  app.view = 'review';
  app.imported = {
    name: 'Avery-Bennett-private-record.docx',
    notes: ['Private metadata'],
  };
  document.body.append(app);
});
afterEach(() => {
  app.remove();
  vi.restoreAllMocks();
});
it('previews the complete document and question locally without making a cloud call', async () => {
  await app.prepareCloud();
  expect(fake.extract.mock.calls[0][0]).toContain(app.question);
  expect(app.cloudCandidate.preview).not.toMatch(
    /Avery Bennett|contact@example.com|Avery-Bennett-private-record|Private metadata/,
  );
  expect(app.cloudCandidate.preview).toContain('diabetes');
  expect(fake.cleanup).not.toHaveBeenCalled();
  expect(fake.ask).not.toHaveBeenCalled();
  await app.send();
  expect(fake.cleanup).toHaveBeenCalledOnce();
  expect(fake.ask).toHaveBeenCalledOnce();
  expect(fake.ask.mock.calls[0][0].text).not.toMatch(
    /Avery Bennett|contact@example.com|diabetes/,
  );
});
it('rejects a stale preview after the question changes', async () => {
  await app.prepareCloud();
  app.question = 'Contact new@example.com.';
  await app.send();
  expect(fake.cleanup).not.toHaveBeenCalled();
  expect(app.answerError).toContain('current cloud preview');
});
it('requires explicit review of ambiguous local context', async () => {
  app.text = 'I have diabetes.';
  app.question = '';
  await app.prepareCloud();
  await app.send();
  expect(fake.cleanup).not.toHaveBeenCalled();
  expect(app.answerError).toContain('Review');
  app.cloudReviewed = true;
  await app.send();
  expect(fake.cleanup).toHaveBeenCalledOnce();
  expect(fake.ask).not.toHaveBeenCalled();
});
it('does not answer when cloud cleanup fails or after starting over', async () => {
  await app.prepareCloud();
  fake.cleanup.mockRejectedValueOnce(new Error('Cloud failure'));
  await app.send();
  expect(fake.ask).not.toHaveBeenCalled();
  expect(app.answerError).toBe('Cloud failure');
  let resolve!: (result: any) => void;
  fake.cleanup.mockImplementationOnce(
    () =>
      new Promise(r => {
        resolve = r;
      }),
  );
  const pending = app.send();
  await Promise.resolve();
  const input = fake.cleanup.mock.calls.at(-1)![0];
  const result = applyCloudCleanup(input, {complete: true, findings: []});
  app.startOver();
  resolve(result);
  await pending;
  expect(fake.ask).not.toHaveBeenCalled();
  expect(app.cloudResult).toBeUndefined();
  expect(app.view).toBe('compose');
});
it('keeps names from the review scan when the second local pass misses them', async () => {
  fake.extract.mockResolvedValueOnce({
    names: {people: [], companies: []},
    topics: {...NO_TOPICS, health: ['diabetes']},
    ambiguous: [],
    identifying: [],
  });
  // A lowercase handle that only the on-device model, not the local rules,
  // recognizes.
  app.text = 'Notes from zephyrine about diabetes.';
  app.names = {people: ['zephyrine'], companies: []};
  await app.prepareCloud();
  expect(app.cloudCandidate.preview).not.toContain('zephyrine');
});
