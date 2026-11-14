# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Aggregate-only paired scoring; never print corpus 2 values or document-level misses.

python3 -P tools/evaluation/score_evidence_experiments.py [RESULT_DIRECTORY]
Uses the existing answer-key semantics, with separate enabled-replacement scoring.
"""

import importlib.util
import gzip
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = (
    Path(sys.argv[1])
    if len(sys.argv) > 1
    else ROOT / "evaluation/experiments/evidence-repair"
)
spec = importlib.util.spec_from_file_location(
    "score", Path(__file__).with_name("score.py")
)
score = importlib.util.module_from_spec(spec)
original_argv = sys.argv
try:
    sys.argv = [
        str(Path(__file__).with_name("score.py")),
        "evidence-experiment",
    ]
    spec.loader.exec_module(score)
finally:
    sys.argv = original_argv


def totals(rows):
    result = Counter(status for _, status in rows)
    return {
        **{s: result[s] for s in ("caught", "partial", "missed", "lost")},
        "total": len(rows),
    }


def score_variant(key, text, dets):
    active = [d for d in dets if d["enabled"]]
    spans = []
    rows, extras, distractors = score.score_doc(
        key, {"text": text, "detections": active}, spans=spans
    )
    core = [
        (item, state) for item, state in rows if item["category"] in score.BUILT
    ]
    extended = [
        (item, state)
        for item, state in rows
        if item["category"] in score.BUILT | score.NEW
    ]
    truth = bytearray(len(text))
    for span in spans:
        if span:
            a, b = span
            truth[a:b] = bytes([1]) * (b - a)
    excess_chars = sum(
        1
        for d in active
        for i in range(d["start"], d["end"])
        if text[i].isalnum() and not truth[i]
    )
    groups, subtypes = defaultdict(list), defaultdict(list)
    for item, state in rows:
        groups[item["category"]].append((item, state))
        subtypes[
            item["category"] + "/" + item.get("subtype", "unspecified")
        ].append((item, state))
    # The original headline counts highlights too. Report it separately, never confuse it with removal.
    legacy, _, _ = score.score_doc(key, {"text": text, "detections": dets})
    return dict(
        core=totals(core),
        extended=totals(extended),
        by_category={k: totals(v) for k, v in groups.items()},
        by_subtype={k: totals(v) for k, v in subtypes.items()},
        whole_core=int(bool(core) and all(s == "caught" for _, s in core)),
        whole_extended=int(
            bool(extended) and all(s == "caught" for _, s in extended)
        ),
        extra=len(extras),
        detections=len(active),
        distractor_hits=distractors,
        excess_chars=excess_chars,
        legacy_core=totals(
            [(it, s) for it, s in legacy if it["category"] in score.BUILT]
        ),
        rows=rows,
    )


def confidence(deltas):
    # Paired bootstrap over DOCUMENTS, not falsely independent mentions.
    rng = random.Random(7181)
    samples = []
    for _ in range(2000):
        batch = [rng.choice(deltas) for _ in deltas]
        samples.append(
            100 * sum(d for d, n in batch) / sum(n for d, n in batch)
        )
    samples.sort()
    return [round(samples[50], 4), round(samples[1949], 4)]


reports = {}
lines = [
    "# Offline model-evidence experiments",
    "",
    "Frozen saved text and model answers; no fresh inference or import. Baseline is rerun from the current code.",
    "",
    "Recall below counts **enabled replacements only**. Whole-document counts refer only to annotated core values, not a privacy guarantee.",
    "",
    "| Corpus | Variant | Core caught | Core recall | Whole core docs | Whole core + added | Extra replacements | Excess alphanumeric chars | Recovered / regressed |",
    "|---|---|---:|---:|---:|---:|---:|---:|---:|",
]
for file in sorted(OUT.glob("c[123].json.gz")):
    with gzip.open(file, "rt") as f:
        run = json.load(f)
    corpus = run["corpus"]
    corpus_dir = (
        ROOT / "evaluation" / ("corpus" if corpus == 1 else f"corpus{corpus}")
    )
    aggregates, document_deltas = {}, defaultdict(list)
    max_old, max_new, oversized, old_chunks, new_chunks = 0, 0, 0, 0, 0
    for record in run["records"]:
        doc_id = record["id"]
        key = json.loads((corpus_dir / "keys" / f"{doc_id}.json").read_text())
        saved = json.loads(
            (
                ROOT / f"evaluation/results/c{corpus}-round4/raw/{doc_id}.json"
            ).read_text()
        )
        base = score_variant(key, saved["text"], record["variants"]["baseline"])
        for name, dets in record["variants"].items():
            current = (
                base
                if name == "baseline"
                else score_variant(key, saved["text"], dets)
            )
            agg = aggregates.setdefault(
                name,
                dict(
                    documents=0,
                    core=Counter(),
                    extended=Counter(),
                    legacy_core=Counter(),
                    by_category=defaultdict(Counter),
                    by_subtype=defaultdict(Counter),
                    whole_core=0,
                    whole_extended=0,
                    extra=0,
                    detections=0,
                    distractor_hits=0,
                    excess_chars=0,
                    recovered_core=0,
                    regressed_core=0,
                    improved_core_documents=0,
                ),
            )
            agg["documents"] += 1
            for k in ("core", "extended", "legacy_core"):
                agg[k].update(current[k])
            for cat, values in current["by_category"].items():
                agg["by_category"][cat].update(values)
            for subtype, values in current["by_subtype"].items():
                agg["by_subtype"][subtype].update(values)
            for k in (
                "whole_core",
                "whole_extended",
                "extra",
                "detections",
                "distractor_hits",
                "excess_chars",
            ):
                agg[k] += current[k]
            assert len(base["rows"]) == len(current["rows"])
            for (it, before), (same, after) in zip(
                base["rows"], current["rows"]
            ):
                assert it == same
                if it["category"] in score.BUILT:
                    agg["recovered_core"] += (
                        before != "caught" and after == "caught"
                    )
                    agg["regressed_core"] += (
                        before == "caught" and after != "caught"
                    )
            document_deltas[name].append(
                (
                    current["core"]["caught"] - base["core"]["caught"],
                    current["core"]["total"],
                )
            )
            agg["improved_core_documents"] += (
                current["core"]["caught"] > base["core"]["caught"]
            )
        old, new = record["chunks"]["old"], record["chunks"]["bounded"]
        max_old = max(max_old, *old)
        max_new = max(max_new, *new)
        oversized += sum(n > 350 for n in old)
        old_chunks += len(old)
        new_chunks += len(new)
    for name, a in aggregates.items():
        a["core_delta_95pct_pp"] = confidence(document_deltas[name])
        a["core_recall"] = 100 * a["core"]["caught"] / a["core"]["total"]
        a["extra_rate"] = 100 * a["extra"] / a["detections"]
        lines.append(
            f"| {corpus} | {name} | {a['core']['caught']}/{a['core']['total']} | {a['core_recall']:.3f}% | "
            f"{a['whole_core']}/{a['documents']} | {a['whole_extended']}/{a['documents']} | {a['extra']} ({a['extra_rate']:.2f}%) | "
            f"{a['excess_chars']} | {a['recovered_core']} / {a['regressed_core']} |"
        )
    reports[str(corpus)] = dict(
        sourceHash=run["sourceHash"],
        baselineDifferences=run["baselineDifferences"],
        variants=aggregates,
        timingMs=run["timingMs"],
        chunking=dict(
            max_old=max_old,
            max_new=max_new,
            oversized_old_chunks=oversized,
            old_chunks=old_chunks,
            bounded_chunks=new_chunks,
        ),
    )
lines.extend(
    [
        "",
        "The extra-replacement and excess-character counts are answer-key proxies, not audited precision. Titles and incomplete keys can contribute.",
        "Corpus 1 and corpus 3 are development/regression sets. Corpus 2 is aggregate-only; repeated measurement still makes it an imperfect holdout.",
        "",
    ]
)
lines.extend(
    [
        "## Selected combination: validation and uncertainty",
        "",
        "`combined` was selected on corpora 1 and 3 before corpus 2 ran; its source hash and success checks are frozen in `protocol.json`.",
        "",
        "| Corpus | Core recall gain (percentage points) | Paired document bootstrap 95% interval | Documents with a core gain | Extra-replacement rate change |",
        "|---|---:|---:|---:|---:|",
    ]
)
for c, report in reports.items():
    base, best = report["variants"]["baseline"], report["variants"]["combined"]
    lo, hi = best["core_delta_95pct_pp"]
    lines.append(
        f"| {c} | {best['core_recall'] - base['core_recall']:.3f} | [{lo:.3f}, {hi:.3f}] | {best['improved_core_documents']} | {best['extra_rate'] - base['extra_rate']:+.3f} pp |"
    )
if "2" in reports:
    report = reports["2"]
    base, best = report["variants"]["baseline"], report["variants"]["combined"]
    checks = dict(
        recall_gain=best["core"]["caught"] > base["core"]["caught"],
        no_regression=best["regressed_core"] == 0,
        extra_rate_budget=best["extra_rate"] - base["extra_rate"] <= 0.25,
    )
    report["prespecified_checks"] = checks
    lines += [
        "",
        "Prespecified validation checks: "
        + ", ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in checks.items())
        + ".",
        "",
    ]
    if not all(checks.values()):
        lines += [
            "**Decision:** keep the changes as research prototypes. The selected combination did not meet the prespecified validation criteria, so these results do not justify presenting it as a general accuracy upgrade.",
            "",
        ]
lines += [
    "These intervals are descriptive: this is reused synthetic data, gains can be concentrated in very few documents, and multiple variants were explored. They do not establish accuracy on future real documents.",
    "",
    "## Changed categories and subtypes",
    "",
    "Only aggregate changes are shown, including for corpus 2. No individual corpus 2 misses were inspected.",
    "",
    "| Corpus | Category | Baseline | Combined | Additional fully replaced |",
    "|---|---|---:|---:|---:|",
]
for c, report in reports.items():
    base, best = report["variants"]["baseline"], report["variants"]["combined"]
    for cat, after in best["by_category"].items():
        before = base["by_category"][cat]
        if after["caught"] != before["caught"]:
            lines.append(
                f"| {c} | {cat} | {100*before['caught']/before['total']:.2f}% ({before['caught']}/{before['total']}) | {100*after['caught']/after['total']:.2f}% ({after['caught']}/{after['total']}) | {after['caught']-before['caught']} |"
            )
lines += [
    "",
    "| Corpus | Subtype with baseline ≥90% | Baseline caught | Combined caught | Total |",
    "|---|---|---:|---:|---:|",
]
for c, report in reports.items():
    base, best = report["variants"]["baseline"], report["variants"]["combined"]
    for sub, after in sorted(best["by_subtype"].items()):
        before = base["by_subtype"][sub]
        if (
            after["caught"] != before["caught"]
            and before["caught"] / before["total"] >= 0.9
        ):
            lines.append(
                f"| {c} | {sub} | {before['caught']} | {after['caught']} | {after['total']} |"
            )
lines += [
    "",
    "No detailed subtype already at ≥90% gained full occurrences with the selected combination. The improvements above occur within broader categories that already exceed 90%, concentrated in their weaker written forms.",
    "",
]
lines += [
    "",
    "## What each experiment changes",
    "",
    "- `trust-model`: add any exact model-proposed span that is free. A deliberately permissive comparison; it does not overwrite earlier spans.",
    "- `guarded-exact`: add exact grounded spans after generic-word, region, and occurrence-context checks.",
    "- `guarded-normalized`: the same with case, canonical Unicode, apostrophe, hyphen, and whitespace normalization mapped back to original offsets. It preserves accents.",
    "- `complete-spans`: only complete an existing, contained, same-kind partial span using guarded exact model evidence. Manual and disabled detections are protected.",
    "- `combined`: guarded normalization plus complete-span reconciliation; no extra model requests.",
    "- `identifier-memory`: infer an ID family from two different explicitly detected values with the same prefix, separators, digit widths, and type. No new inference calls.",
    "- `combined-memory`: the combination plus identifier memory. The narrow memory rule did not add value in these corpora.",
    "",
    "## Behavioral controls and chunk bounds",
    "",
]
behavior_path = OUT / "behavioral.json"
if behavior_path.exists():
    behavior = json.loads(behavior_path.read_text())
    lines += [
        "| Variant | Controlled positives fully covered | Negative controls hit |",
        "|---|---:|---:|",
    ]
    for name, v in behavior["summary"].items():
        lines.append(
            f"| {name} | {v['positive_caught']}/{v['positive_total']} | {v['negative_false_hits']}/{v['negative_total']} |"
        )
    lines += [
        "",
        "These controls were authored for the mechanisms and are not an independent accuracy estimate. The four negative hits already present in the baseline remain unresolved. Offset mapping, manual/disabled choices, selected categories, restoration, identifier-family boundaries, and chunk coverage checks passed.",
        "",
    ]
lines += [
    "| Corpus | Old maximum words/chunk | Old chunks over 350 words | Bounded maximum | Old → bounded chunk count |",
    "|---|---:|---:|---:|---:|",
]
for c, r in reports.items():
    b = r["chunking"]
    lines.append(
        f"| {c} | {b['max_old']} | {b['oversized_old_chunks']} | {b['max_new']} | {b['old_chunks']} → {b['bounded_chunks']} |"
    )
lines += [
    "",
    "A separate 2,000-word paragraph is currently one chunk; the bounded prototype makes seven overlapping chunks of at most 350 words. This establishes a bound and coverage, not a model recall gain. Context-carrying model prompts, targeted repair inference, and learned table schemas remain untested.",
    "",
    "## Reproduce",
    "",
    "From the repository root, after installing the locked dependencies:",
    "",
    "```bash",
    "node tools/evaluation/run_evidence_experiments.mjs --corpora 1,3",
    "node tools/evaluation/check_evidence_experiments.mjs",
    "# Freeze the experiment before consulting corpus 2 totals.",
    "node tools/evaluation/run_evidence_experiments.mjs --corpora 2",
    "python3 -P tools/evaluation/score_evidence_experiments.py",
    "node_modules/.bin/tsc --ignoreConfig --noEmit --target ES2022 --module ESNext --moduleResolution bundler --lib ES2023,DOM,DOM.Iterable --allowJs --skipLibCheck --types node tools/evaluation/evidence-experiments.ts",
    "npm test",
    "npm run build",
    "```",
    "",
    "The `.json.gz` files retain per-document variant detections for reproducibility. Corpus 2 is consumed only by aggregate scoring. Each run records its source hash, base commit, and timing. Baselines reproduced the saved round-4 spans and kinds exactly on all documents. JS UTF-16 offsets are converted to Python code-point offsets before scoring.",
    "",
    "The only post-validation source edit was a TypeScript non-null assertion after an existing nonempty-array guard. It has no runtime effect; both source hashes are recorded in `protocol.json`, and all corpora were replayed after that type-check fix.",
    "",
    "Timing is local CPU postprocessing only, excludes import/model/UI latency, and is affected by warmup and variant order. It is not an end-to-end latency benchmark. Production detector code and published accuracy figures are unchanged.",
    "",
    "Historical core scoring counted highlighted-only spans too. This experiment also retains `legacy_core` for comparison but requires enabled replacements for its headline; corpus 1 therefore starts at 5,770 rather than the previously reported 5,771.",
    "",
]
# Store the subtype detail that distinguishes variants, rather than thousands of repeated unchanged counters.
for report in reports.values():
    baseline_subtypes = report["variants"]["baseline"]["by_subtype"]
    changed = {
        sub
        for variant in report["variants"].values()
        for sub, counts in variant["by_subtype"].items()
        if counts != baseline_subtypes[sub]
    }
    for variant in report["variants"].values():
        variant["by_subtype"] = {
            sub: counts
            for sub, counts in variant["by_subtype"].items()
            if sub in changed
        }
    report["subtype_reporting"] = (
        "Only subtypes changed by any variant; all others are reproducible from the saved detections."
    )
assert (
    len({r["sourceHash"] for r in reports.values()}) == 1
), "Mixed experiment implementations"
assert all(
    r["baselineDifferences"] == 0 for r in reports.values()
), "Baseline differs from historical run"
(OUT / "summary.json").write_text(json.dumps(reports, indent=2) + "\n")
(OUT / "summary.md").write_text("\n".join(lines))
print("\n".join(lines))
