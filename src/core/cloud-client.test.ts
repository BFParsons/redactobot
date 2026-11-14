/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {afterEach, beforeEach, expect, it, vi} from 'vitest';
const fake = vi.hoisted(() => ({
  generate: vi.fn(),
  model: vi.fn(),
  token: vi.fn(),
  initialize: vi.fn(),
}));
vi.mock('firebase/app-check', () => ({
  initializeAppCheck: (...args: any[]) => {
    fake.initialize(...args);
    return {};
  },
  ReCaptchaEnterpriseProvider: class {},
  CustomProvider: class {},
  getToken: (...args: any[]) => fake.token(...args),
}));
vi.mock('firebase/ai', () => ({
  getAI: () => ({}),
  GoogleAIBackend: class {},
  InferenceMode: {ONLY_IN_CLOUD: 'only_in_cloud'},
  Schema: {
    object: (v: any) => v,
    array: (v: any) => v,
    boolean: () => ({}),
    string: () => ({}),
    enumString: (v: any) => v,
  },
  getGenerativeModel: (...args: any[]) => {
    fake.model(...args);
    return {generateContent: fake.generate};
  },
}));
beforeEach(() => {
  vi.resetModules();
  vi.clearAllMocks();
  vi.stubEnv('VITE_FIREBASE_API_KEY', 'fictional-test-key');
  vi.stubEnv('VITE_FIREBASE_PROJECT_ID', 'cloud-gate-test');
  vi.stubEnv('VITE_FIREBASE_APP_ID', '1:123:web:cloud-gate-test');
  vi.stubEnv('VITE_APPCHECK_DEBUG_TOKEN', 'fictional-registered-token');
  vi.stubEnv('VITE_RECAPTCHA_ENTERPRISE_SITE_KEY', '');
  fake.token.mockResolvedValue({token: 'fictional-attestation'});
  fake.generate.mockResolvedValue({
    response: {text: () => '{"complete":true,"findings":[]}'},
  });
});
afterEach(() => {
  vi.unstubAllEnvs();
  Reflect.deleteProperty(globalThis, 'FIREBASE_APPCHECK_DEBUG_TOKEN');
});
async function fixture() {
  const gate = await import('./cloud-gate');
  const {makeReport} = await import('../extension/policy');
  const {NO_TOPICS} = await import('./redact');
  const text =
    'Contact Avery Bennett at avery@example.com.\n\nDiagnosis: diabetes.';
  const report = makeReport(
    text,
    {people: ['Avery Bennett'], companies: []},
    {...NO_TOPICS, health: ['diabetes']},
    [],
    'TEST',
  );
  return {...gate, input: gate.prepareCloudInput(text, report, 'TEST')};
}
it('validates runtime approval before Firebase or attestation setup', async () => {
  const {cleanupCloud} = await import('./cloud-client');
  await expect(
    cleanupCloud({kind: 'approved-cloud-input', text: 'Raw fictional note'}),
  ).rejects.toThrow('local privacy check');
  expect(fake.initialize).not.toHaveBeenCalled();
  expect(fake.token).not.toHaveBeenCalled();
  expect(fake.generate).not.toHaveBeenCalled();
});
it('sends only approved text in ONLY_IN_CLOUD mode and scrubs known sensitive details', async () => {
  const {input} = await fixture();
  const {cleanupCloud} = await import('./cloud-client');
  const result = await cleanupCloud(input);
  const body = fake.generate.mock.calls[0][0];
  expect(body).toBe(`Approved document:\n${JSON.stringify(input.text)}`);
  expect(body).not.toMatch(/Avery Bennett|avery@example.com/);
  expect(body).toContain('diabetes');
  expect(fake.model.mock.calls[0][1]).toMatchObject({
    mode: 'only_in_cloud',
    inCloudParams: {model: 'gemini-3.5-flash-lite'},
  });
  expect(fake.token).toHaveBeenCalledOnce();
  expect(result.report.cleaned).not.toContain('diabetes');
});
it('holds the document when App Check fails', async () => {
  const {input} = await fixture();
  fake.token.mockRejectedValueOnce(new Error('Attestation failed'));
  const {cleanupCloud} = await import('./cloud-client');
  await expect(cleanupCloud(input)).rejects.toThrow('Attestation');
  expect(fake.generate).not.toHaveBeenCalled();
});
it('does not use a cleanup approval to skip directly to answering', async () => {
  const {input} = await fixture();
  const {askCloud} = await import('./cloud-client');
  await expect(askCloud(input)).rejects.toThrow('privacy stage');
  expect(fake.initialize).not.toHaveBeenCalled();
  expect(fake.generate).not.toHaveBeenCalled();
});
it('holds cloud requests when project configuration is missing', async () => {
  vi.stubEnv('VITE_FIREBASE_API_KEY', '');
  const {input} = await fixture();
  const {cleanupCloud} = await import('./cloud-client');
  await expect(cleanupCloud(input)).rejects.toThrow('Connect a Firebase');
  expect(fake.initialize).not.toHaveBeenCalled();
});
it('rejects malformed output and ignores an answer that arrives after cancellation', async () => {
  const {input} = await fixture();
  const {cleanupCloud} = await import('./cloud-client');
  fake.generate.mockResolvedValueOnce({response: {text: () => 'not JSON'}});
  await expect(cleanupCloud(input)).rejects.toThrow();
  const again = (await fixture()).input;
  const controller = new AbortController();
  fake.generate.mockImplementationOnce(async () => {
    controller.abort();
    return {response: {text: () => '{"complete":true,"findings":[]}'}};
  });
  await expect(cleanupCloud(again, controller.signal)).rejects.toThrow();
});
