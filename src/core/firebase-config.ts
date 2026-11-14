/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

const env = import.meta.env;
/** Firebase project settings, read from VITE_FIREBASE_* build variables. */
export const firebaseConfig = {
  apiKey: env.VITE_FIREBASE_API_KEY as string | undefined,
  authDomain: env.VITE_FIREBASE_AUTH_DOMAIN as string | undefined,
  projectId: env.VITE_FIREBASE_PROJECT_ID as string | undefined,
  appId: env.VITE_FIREBASE_APP_ID as string | undefined,
};
/** Whether the build has the Firebase settings that cloud requests need. */
export const cloudConfigured = Boolean(
  firebaseConfig.apiKey && firebaseConfig.projectId && firebaseConfig.appId,
);
