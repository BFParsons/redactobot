/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Fills in the contact email link on the privacy page. The
 * address is stored reversed in data attributes and assembled here, so it does
 * not appear in the page source for address-harvesting bots. Without scripts
 * the page shows a spelled-out fallback.
 */

for (const link of document.querySelectorAll('a[data-contact]')) {
  const reverse = value => [...value].reverse().join('');
  const address = `${reverse(link.dataset.u)}@${reverse(link.dataset.d)}`;
  link.href = `mailto:${address}`;
  link.textContent = address;
}
