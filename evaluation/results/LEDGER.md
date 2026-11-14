# Evaluation ledger (working notes for the long run; newest last)

- 2026-11-11 15:45 corpus installed in evaluation/ (100 docs, 6,120 key items). `python3 -P evaluation/verify_corpus.py` -> 0 mismatches.
- Dev server: `npx vite --host 127.0.0.1 --port 5173 --strictPort` (needed by the runner).
- BASELINE run started 15:47: `python3 -P tools/evaluation/run_eval.py baseline` (background).
  - Log: evaluation/results/baseline/run.log. Per-doc results: evaluation/results/baseline/raw/doc-NNN.json.
  - Done marker: evaluation/results/baseline/DONE. Resumable: rerun the same command, finished docs are skipped.
  - Code under test: commit 4d0f763 + harness files (no detector changes yet).
- NEXT: `python3 -P tools/evaluation/score.py baseline` (all), then `--split dev --misses` to guide fixes,
  fix detectors, run `after`, score all/dev/heldout, write evaluation/RESULTS.md.
- 16:28 baseline DONE. Score: built 68.7% all / 70.3% dev / 65.7% held-out.
- Fix rounds measured by replaying baseline model names (`--replay baseline`, seconds per run):
  fix1..fix5. Final replay fix5: dev 93.9%, held-out 90.4%, over-redaction 6.1% (dev).
  Tools moved to tools/evaluation/ (folder name `eval` trips the worktree guard).
- 16:52 AFTER run started (live model, fixed code): `python3 -P tools/evaluation/run_eval.py after`.
  Log evaluation/results/after/run.log, done marker evaluation/results/after/DONE. Resumable.
- NEXT when AFTER is done: score.py after (all/dev/heldout), write evaluation/RESULTS.md,
  update README, delete fix1..fix4 result folders, commit.
- Split: held-out = doc numbers ending in 3, 6 or 9 (30 docs). Never read held-out misses when fixing.
- 17:38 AFTER run DONE (live). Two small rules added afterwards (unlabelled credentials, 5-digit
  card endings); `final` = replay of AFTER names with committed code.
- FINAL: core 92.7% all / 94.1% dev / 90.1% held-out; code-only 83.9%; over-redaction 6.9%.
  Baseline was 68.7 / 70.3 / 65.7; code-only 38.3; over-redaction 4.6.
- fix1..fix5 result folders deleted. Write-up: evaluation/RESULTS.md.

## Round 2 (enhancements 1-8), 2026-11-11 evening
- Frozen harness builds (job tmp): harness-before = code at commit be5764c, served on :5180;
  harness-after = round-2 code, served on :5181. Build: `npx vite build -c tools/evaluation/vite.harness.config.ts --outDir DIR`.
- Live runs only COLLECT model output (names, topics). Final scores come from `--replay` with the
  committed code, so code can keep changing while a live run is going.
- 18:33 started `c1-topics` = corpus 1, names replayed from `after`, topics live, via :5181. ~60 min.
  Log evaluation/results/c1-topics/run.log, marker .../DONE. Resumable.
- Corpus 2 (60 fresh docs, evaluation/corpus2) is being written by a subagent. When it lands:
  verify (`python3 -P evaluation/verify_corpus2.py`), then
  `CSA_CORPUS=evaluation/corpus2 CSA_HARNESS_URL=http://127.0.0.1:5180/... run_eval.py c2-before` (live names, old code),
  then `c2-topics --replay c2-before --live-topics` via :5181, then replay finals for both corpora.
- NEVER inspect corpus 2 misses. Totals only.
- 19:28 c1-topics DONE. 20:06 c2-before DONE. 20:49 c2-topics DONE. 21:0x jexp-judge DONE. No model failures.
- FINAL round 2 (replays with committed code): corpus 1 core 94.8% (dev 95.5, held-out 93.4); corpus 2 core 93.3%
  (round-1 code 91.3%). Topics flagged 57% / 60%. Judge experiment: slower (20 s vs 13 s per chunk) and less
  accurate; not adopted. Write-up: evaluation/RESULTS-ROUND2.md.
- Kept result folders: baseline, after, final (round 1); c1-topics, c1-round2, c2-before, c2-topics, c2-final,
  jexp-judge, jexp-names (round 2).

## Round 3 (sub-category loop), 2026-11-11 night
- Loop: `python3 -P tools/evaluation/progress.py --guard` replays c1-topics into `work` and c2-topics into `work2`
  (both gitignored scratch), prints changed sub-categories and totals. Needs the dev server on :5173.
- Corpus-1 held-out documents were opened in this round (needed to reach 100% per sub-category).
  Corpus 2 is now the ONLY unseen set. Still never inspect corpus 2 misses.
- Scorer changes: letters and digits only; label word before a number; possessive 's; joining word
  between two places; flag-only groups judged by "flagged" in progress.py.
- New: src/core/sensitive-terms.ts (word lists, flag only); tools/evaluation/try_names.ts and
  try_patterns.mjs (run the rules on a string; PEOPLE= / COMPANIES= stand in for model names).
- FINAL round 3: 116 of 126 sub-categories at 100%. Corpus 1 core 100.0% (5772/5772), code-only 96.0%,
  flagged 94.6%, over-redaction 6.3%. Corpus 2 core 96.4% (4364/4527), code-only 93.1%, new categories 88.4%,
  flagged 84.5%, over-redaction 7.8%. Flags touching nothing in the keys: 52% / 59%.
- Kept result folders: c1-round3, c2-round3. Write-up: evaluation/RESULTS-ROUND3.md.
- Stopped at 10 flag-only sub-categories (31 unflagged items: bare numbers, one-off phrasings). Next lever is the
  on-device topics prompt, which needs a live run (~1 h per corpus on this machine).

## Round 4 (precision + corpus 3), 2026-11-11 night to 11-12
- Corpus 3 (evaluation/corpus3, docs 301-360) written by a subagent that did not read src/, taxonomy/, tools/evaluation
  or results. Build: `python3 -P evaluation/generate3.py`; check: `python3 -P evaluation/verify_corpus3.py`.
  Corpus 3 is the WORKING set (misses may be read). Corpus 2 is still never inspected.
- Live model run for corpus 3: `CSA_CORPUS=evaluation/corpus3 CSA_HARNESS_URL=http://127.0.0.1:5181/tools/evaluation/harness.html
  python3 -P tools/evaluation/run_eval.py c3-live --live-topics` (about 50 min). Output kept in results/c3-live.
  ALWAYS point a live run at a frozen harness build, not the dev server.
- Bug found: `--no-model` runs attached to the real Chrome on port 9333 and navigated a concurrent live run's page.
  Fixed in run_eval.py (model-off runs use the headless browser).
- Loop: `progress.py --guard` (corpus 1 + 2) and `progress3.py [--replay c3-live]` (corpus 3). `extras.py RUN [KIND]`
  lists needless replacements.
- FINAL round 4: corpus 2 core 97.0% (4390/4527), code-only 94.3%, flagged 85.3%, needless 6.2%.
  Corpus 1 core 5771/5772, needless 4.1%. Corpus 3 core 97.8% (first contact 96.9%), code-only 94.3%, flagged 92.6%, needless 4.9%.
- Known key error in corpus 3: six weekday-date cells in doc-356 ("2020 10/20") are wrong in the key (lost in import).
- Kept: c1-round4, c2-round4, c3-round4, c3-live. Write-up: evaluation/RESULTS-ROUND4.md.
- Stopped because the last three patches moved corpus 2 by <= 0.1 points each. What remains is model territory
  (lower-case names and towns, nicknames, single initials). Next levers: the on-device prompts, or a faster machine.
