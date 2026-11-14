/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

// @vitest-environment jsdom
import {it, expect} from 'vitest';
import {readFileSync} from 'node:fs';
import {renderReview} from './review';
import {makeReport} from './policy';
import {NO_TOPICS} from '../core/redact';
import {fallbackTheme} from './themes';
it('keeps an edited review and removal choices intact through live theme changes', () => {
  document.documentElement.innerHTML = readFileSync(
    'extension/review.html',
    'utf8',
  ).replace(/<script[^>]*>[\s\S]*?<\/script>/g, '');
  let receive = (_message: any) => {};
  const sent: any[] = [];
  renderReview({
    name: 'review',
    postMessage: m => sent.push(m),
    disconnect() {},
    onMessage: {
      addListener: fn => {
        receive = fn;
      },
    },
    onDisconnect: {addListener() {}},
  });
  const text = '[PERSON_OLD_1] knows Avery Bennett and Morgan Ellis.';
  const report = makeReport(
    text,
    {people: ['Avery Bennett', 'Morgan Ellis'], companies: []},
    NO_TOPICS,
    [],
    'TEST',
  );
  receive({
    type: 'review-state',
    text,
    report,
    theme: fallbackTheme('claude', false),
    contextChanged: false,
  });
  const preview = document.querySelector<HTMLTextAreaElement>('#preview')!;
  expect(preview.value).toBe(report.cleaned);
  document.querySelector<HTMLInputElement>('#findings input')!.click();
  expect(preview.value).toBe(report.cleaned);
  expect(
    document.querySelector<HTMLInputElement>('#findings input')!.disabled,
  ).toBe(true);
  preview.value = 'My edited safe text';
  preview.dispatchEvent(new Event('input'));
  receive({type: 'theme', theme: fallbackTheme('claude', true)});
  expect(preview.value).toBe('My edited safe text');
  expect(document.documentElement.style.colorScheme).toBe('dark');
  expect(
    document.querySelector<HTMLInputElement>('#findings input')!.disabled,
  ).toBe(true);
  // Without cloud cleanup, Use this text is the main action and pastes the box
  // as written.
  expect(document.querySelector<HTMLButtonElement>('#approve')!.hidden).toBe(
    true,
  );
  expect(document.querySelector('#use')!.className).toBe('primary');
  document.querySelector<HTMLButtonElement>('#use')!.click();
  expect(sent.at(-1)).toEqual({type: 'use', text: 'My edited safe text'});
});
it('offers Ignore to paste the original, and keeps cloud cleanup as the main action when enabled', () => {
  document.documentElement.innerHTML = readFileSync(
    'extension/review.html',
    'utf8',
  ).replace(/<script[^>]*>[\s\S]*?<\/script>/g, '');
  let receive = (_message: any) => {};
  const sent: any[] = [];
  renderReview({
    name: 'review',
    postMessage: m => sent.push(m),
    disconnect() {},
    onMessage: {
      addListener: fn => {
        receive = fn;
      },
    },
    onDisconnect: {addListener() {}},
  });
  const text = 'Avery Bennett has diabetes.';
  const report = makeReport(
    text,
    {people: ['Avery Bennett'], companies: []},
    {...NO_TOPICS, health: ['diabetes']},
    [],
    'TEST',
  );
  receive({
    type: 'review-state',
    text,
    report,
    theme: fallbackTheme('chatgpt', false),
    contextChanged: false,
    cloudCleanup: true,
  });
  const approve = document.querySelector<HTMLButtonElement>('#approve')!;
  expect(approve.hidden).toBe(false);
  expect(approve.textContent).toBe('Clean up this preview in cloud');
  expect(document.querySelector('#use')!.className).toBe('secondary');
  document.querySelector<HTMLButtonElement>('#ignore')!.click();
  expect(sent.at(-1)).toEqual({type: 'ignore'});
  expect(
    approve.disabled &&
      document.querySelector<HTMLButtonElement>('#use')!.disabled,
  ).toBe(true);
});
it('shows the exact first-stage cloud preview with identities locked and sensitive facts optional', () => {
  document.documentElement.innerHTML = readFileSync(
    'extension/review.html',
    'utf8',
  ).replace(/<script[^>]*>[\s\S]*?<\/script>/g, '');
  let receive = (_message: any) => {};
  const sent: any[] = [];
  renderReview({
    name: 'review',
    postMessage: m => sent.push(m),
    disconnect() {},
    onMessage: {
      addListener: fn => {
        receive = fn;
      },
    },
    onDisconnect: {addListener() {}},
  });
  const text = 'Avery Bennett has diabetes.';
  const report = makeReport(
    text,
    {people: ['Avery Bennett'], companies: []},
    {...NO_TOPICS, health: ['diabetes']},
    [],
    'TEST',
  );
  receive({
    type: 'review-state',
    text,
    report,
    theme: fallbackTheme('gemini', true),
    contextChanged: false,
    cloudCleanup: true,
  });
  const preview = document.querySelector<HTMLTextAreaElement>('#preview')!;
  expect(preview.value).toBe(report.cloudText);
  expect(preview.value).not.toContain('Avery');
  expect(preview.value).toContain('diabetes');
  const checks = [
    ...document.querySelectorAll<HTMLInputElement>('#findings input'),
  ];
  expect(checks[0].disabled).toBe(true);
  expect(checks[1].checked).toBe(false);
  checks[1].click();
  expect(preview.value).not.toContain('diabetes');
  document.querySelector<HTMLButtonElement>('#approve')!.click();
  expect(sent.at(-1).kept).toEqual([]);
});
it('offers to scan an incomplete report again instead of pasting it', () => {
  document.documentElement.innerHTML = readFileSync(
    'extension/review.html',
    'utf8',
  ).replace(/<script[^>]*>[\s\S]*?<\/script>/g, '');
  let receive = (_message: any) => {};
  const sent: any[] = [];
  renderReview({
    name: 'review',
    postMessage(m: any) {
      sent.push(m);
    },
    disconnect() {},
    onMessage: {
      addListener: fn => {
        receive = fn;
      },
    },
    onDisconnect: {addListener() {}},
  });
  const report = makeReport(
    'A note.',
    {people: [], companies: []},
    NO_TOPICS,
    [],
    'TEST',
    false,
  );
  receive({
    type: 'review-state',
    text: 'A note.',
    report,
    theme: fallbackTheme('claude', false),
    contextChanged: false,
  });
  receive({type: 'error', message: 'The full scan must finish.'});
  const approve = document.querySelector<HTMLButtonElement>('#approve')!;
  expect(approve.disabled).toBe(false);
  expect(approve.textContent).toBe('Scan again');
  approve.click();
  expect(sent).toEqual([
    {type: 'approve', kept: [], edited: undefined, rescan: true},
  ]);
});
