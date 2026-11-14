/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

// Fonts and icons are bundled with the app so no third-party server is
// contacted.
import '@fontsource/roboto/latin-400.css';
import '@fontsource/roboto/latin-500.css';
import './theme/tokens.css';
import './theme/app.css';

import {styles as typescale} from '@material/web/typography/md-typescale-styles.js';

import '@material/web/button/filled-button.js';
import '@material/web/button/filled-tonal-button.js';
import '@material/web/button/outlined-button.js';
import '@material/web/button/text-button.js';
import '@material/web/checkbox/checkbox.js';
import '@material/web/chips/assist-chip.js';
import '@material/web/chips/chip-set.js';
import '@material/web/chips/filter-chip.js';
import '@material/web/chips/input-chip.js';
import '@material/web/dialog/dialog.js';
import '@material/web/divider/divider.js';
import '@material/web/icon/icon.js';
import '@material/web/iconbutton/icon-button.js';
import '@material/web/labs/card/outlined-card.js';
import '@material/web/labs/card/filled-card.js';
import '@material/web/list/list.js';
import '@material/web/list/list-item.js';
import '@material/web/progress/linear-progress.js';
import '@material/web/radio/radio.js';
import '@material/web/tabs/tabs.js';
import '@material/web/tabs/primary-tab.js';
import '@material/web/tabs/secondary-tab.js';
import '@material/web/textfield/outlined-text-field.js';

import './app';

// Material 3 type scale classes (md-typescale-*).
if (typescale.styleSheet) {
  document.adoptedStyleSheets.push(typescale.styleSheet);
}
