#!/usr/bin/env python3
# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Deterministic generator for the SECOND (held-out) Redactobot test corpus.

Run:  python3 -P evaluation/generate2.py

Writes (next to this file):
  corpus2/docs/doc-2NN.<ext>    the 60 documents (doc-201 .. doc-260)
  corpus2/keys/doc-2NN.json     machine-readable answer key
  corpus2/keys/doc-2NN.md       human-readable answer key
  corpus2/manifest.json

All document content is authored, fictional text held in
corpus2_src/batch_*.py with every sensitive value marked inline. The answer
keys are derived from that markup; occurrence counts are computed from the
document text model (longest value first, masked, standalone-token
boundaries). The build fails if any capitalised word, digit-bearing token or
email/URL-looking token is left that is not a key value, a distractor, or a
reviewed entry. verify_corpus2.py re-derives everything independently from
the files actually written.

The markup, keying conventions and the single rule for difficulty "hard" are
documented at the top of corpus2_src/core.py. No network, no clock.

Authoring aids:
  --batch a                      build only corpus2_src/batch_a.py into corpus2/.work/a/
  --mint KIND [-n N] [--salt S]  KIND = card | iban | aba | sin | ssn | imei
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from corpus2_src.core import main  # noqa: E402

if __name__ == "__main__":
    main()
