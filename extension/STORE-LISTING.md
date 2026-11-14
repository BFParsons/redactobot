# Chrome Web Store listing

Everything to paste into the Chrome Web Store developer dashboard for Redactobot.
Build the upload with `npm run package:extension`; it writes
`extension/releases/redactobot-extension-<version>.zip`.

## Store listing tab

**Name** (from the manifest): Redactobot

**Summary** (from the manifest, 132 characters at most):

> Technology demo. Checks pastes locally on ChatGPT, Claude and Gemini and removes
> private details. Privacy policy: see Settings.

**Category:** Productivity (alternative: Privacy & Security under Tools)

**Language:** English

**Description:**

```text
Redactobot removes private details from text before you paste it into an AI chat.

Switch it on under the chat box on ChatGPT, Claude or Gemini, then paste as usual.
Names, email addresses, phone numbers, addresses, account and card numbers,
government IDs, passwords, dates and other private details are replaced with
placeholders such as [PERSON_1] before the text reaches the chat box. If something
is uncertain, a small review asks you first. Redactobot never presses Send.

EVERYTHING STAYS ON YOUR DEVICE
• Detection runs in your browser, using pattern rules and Gemini Nano, the AI model
  built into Chrome.
• This extension makes no network requests. It asks for no access to other sites.
• Pasted text is held in memory only while it is checked, then discarded.
• Only your settings are saved.

HOW IT WORKS
1. Open ChatGPT, Claude or Gemini. A Redactobot switch appears under the chat box.
   It starts off every time a page loads.
2. Switch it on. After a break, Chrome may need a minute or two to start its
   on-device model; a progress bar shows it.
3. Paste. Clear private details are replaced automatically.
4. If a detail is uncertain, review it, then choose "Use this text" or "Ignore".
5. Choose which of 12 kinds of detail to check under "Data types".

WHAT IT CHECKS
People and organizations · email addresses and phone numbers · addresses and places ·
government IDs and record numbers · payment cards and bank accounts · passwords and
login details · web, device and vehicle identifiers · dates · money amounts · health
details · other sensitive personal facts · indirect identity clues.

PLEASE READ
Redactobot is a technology demonstration, not a validated privacy or compliance
tool. Automatic detection misses things, and text with the names removed can still
identify someone. Do not rely on it for real sensitive data, and always read the
result before you send it. It checks pasted and dropped text only: not what you
type, files you upload, or images.

REQUIREMENTS
Desktop Chrome 148 or later on a computer that can run Gemini Nano (about 22 GB of
free disk space, and 16 GB of memory or a graphics card with more than 4 GB).
Names, places and sensitive topics need the on-device model; contact details,
numbers and IDs work without it.

Open source (Apache 2.0): https://github.com/BFParsons/redactobot
Web app, with optional cloud cleanup: https://redactobot.org
Privacy policy: https://redactobot.org/privacy
```

**Screenshots** (1280 × 800, in `extension/store/`):

1. `1-paste-cleaned.png` Paste as usual; private details are replaced first.
2. `2-review.png` Unsure? It asks you first.
3. `3-dark.png` One switch under the chat box, matching the site.
4. `4-settings.png` Choose what to check.
5. `5-cold-start.png` A progress bar while the on-device model starts.

**Small promo tile** (440 × 280): `extension/store/promo-small-440x280.png`

**Marquee promo tile** (1400 × 560, optional): `extension/store/promo-marquee-1400x560.png`

**Store icon** (128 × 128): `extension/icons/icon-128.png` (already in the zip)

**Homepage URL:** https://redactobot.org

**Support URL:** https://github.com/BFParsons/redactobot/issues

## Privacy practices tab

**Single purpose:**

> Redactobot checks text the user pastes or drops into the message box on ChatGPT,
> Claude and Gemini, on the user's device, and replaces private details with
> placeholders before the text is inserted.

**Permission justifications:**

| Permission | Justification |
| --- | --- |
| `storage` | Saves the user's settings: which kinds of detail to check, which of the three sites show the switch, and whether to load the on-device model at startup. No pasted text is stored. |
| `offscreen` | Runs detection in an offscreen document: a web worker for the pattern rules, and Chrome's built-in Gemini Nano model, which is only available to a document, not to the service worker. |
| Host access (content scripts on chatgpt.com, chat.openai.com, claude.ai, gemini.google.com) | The extension's whole purpose is to intercept paste and drop events in the message box on these three chat sites, check the text locally, and insert the cleaned text. It shows one switch under the message box. It does not read the conversation, the rest of the page, or anything typed. |

**Remote code:** No. All code is in the package. The extension loads no remote
scripts and makes no network requests (`connect-src 'none'`).

**Data usage.** What the extension collects: nothing is collected or transmitted.
For the dashboard's checkboxes, tick none of the data types, because no user data
leaves the device or is collected by the developer:

- Personally identifiable information: not collected
- Health information: not collected
- Financial and payment information: not collected
- Authentication information: not collected
- Personal communications: not collected
- Location: not collected
- Web history: not collected
- User activity: not collected
- Website content: not collected (pasted text is processed in memory on the device
  and discarded; it is never sent anywhere)

Then certify all three statements:

- I do not sell or transfer user data to third parties, outside of the approved use
  cases.
- I do not use or transfer user data for purposes that are unrelated to my item's
  single purpose.
- I do not use or transfer user data to determine creditworthiness or for lending
  purposes.

**Privacy policy URL:** https://redactobot.org/privacy

## Distribution tab

- **Visibility:** Public (or Unlisted while testing)
- **Regions:** All regions
- **Pricing:** Free

## Notes for the reviewer (the "test instructions" box)

```text
No account or login is needed.

1. Open https://chatgpt.com, https://claude.ai or https://gemini.google.com.
2. A "Redactobot" switch appears under the message box. Click it to switch it on.
   The first time, Chrome may take a minute or two to start its built-in model
   (Gemini Nano); a progress bar shows this. On a device without the built-in model,
   pattern checks (emails, phone numbers, card numbers, IDs) still work.
3. Paste this fictional text into the message box:
   Email margaret@whitfield.example or call 604-555-0142. Card 4111 1111 1111 1111.
4. The text is inserted with placeholders such as [EMAIL_1] in place of each detail.
   The extension never sends the message.
5. Settings: click the extension's toolbar icon, or "Data types" beside the switch.

The extension makes no network requests and stores only the user's settings.
```

## After it is published

- Add the store link to `README.md` and to the web app's "Get the Chrome extension"
  section.
- For each update: raise `version` in `extension/manifest.json`, run
  `npm run package:extension`, and upload the new zip.
