# Experiment: a small on-device tagger (masker-mini) between the rules and Gemini Nano

14 November 2026. Follows [RESEARCH-FAST-PII-METHODS.md](RESEARCH-FAST-PII-METHODS.md).

## Setup

- Model: masker-mini v3 (huggingface.co/amsintelligence/masker-mini), 35M-parameter MiniLM-class
  token classifier, ONNX int4 (22 MB), Apache-2.0, BIOES tags for given name, surname, city, street,
  building number, zip, phone, email, card, date, age, government ID. No organization tag.
- Run with ONNX Runtime 1.32 (Python, CPU) on the same ~150-word pieces as the rules runs
  (`tools/evaluation/export_pieces.ts`), spans trimmed and unioned with the rules' findings
  (`tools/evaluation/masker_experiment.py`). Nano spans come from the saved live runs (document-app
  prompts; an approximation of the paste gate's prompt). Scored with `tools/evaluation/score.py`.

## Accuracy (corpus 2, unseen; paste-sized)

| | person | org | critical | not in keys (absolute) |
|---|---|---|---|---|
| rules only | 86.1% | 86.5% | 90.9% | 324 |
| masker-mini alone | 76.4% | 9.9% | 68.2% | - |
| rules + masker names only | 91.5% | 88.7% | 93.8% | 372 |
| **rules + masker (all tags)** | **92.0%** | **92.3%** | **94.9%** | 438 |
| rules + Nano (today) | 93.9% | 94.5% | 95.1% | 376 |

Corpus 3 agrees (rules + masker 93.7% person vs rules + Nano 94.3%).

## Speed (CPU, int4, ~230 tokens per piece)

| threads | median | p90 |
|---|---|---|
| 1 | 57-111 ms | 135-160 ms |
| 4 | 36 ms | 51 ms |
| 8 | 21 ms | 30 ms |

Nano: 0.3-1.5 s warm, 1-3 minutes cold. Browser WASM is typically slower than native ORT; WebGPU faster.

## Cascade: Nano only for the pieces masker is least sure about

Uncertainty = tokens whose winning label beats the runner-up by < 0.5 probability
(`tools/evaluation/cascade_experiment.py`). Corpus 2 (unseen):

| Nano on | person | critical | org | random pieces instead (person) |
|---|---|---|---|---|
| 0% | 92.0% | 94.9% | 92.3% | - |
| 10% | 93.2% | 95.5% | 93.8% | 92.1% |
| 25% | 93.6% | 95.8% | 94.5% | 92.4% |
| 50% | 94.1% | 96.1% | 95.1% | 93.6% |
| 100% (rules + masker + Nano) | **95.6%** | **96.9%** | **97.4%** | - |

Routing by uncertainty beats random routing at every budget. With Nano on the 10% least certain
pieces, critical recall already exceeds today's Nano-on-everything path.

## Conclusion and risks

A 22 MB tagger closes most of the rules-to-Nano gap at ~20-110 ms, and as a cascade it lets the
extension call Nano on a minority of pastes (hiding Nano's cold start) with better recall than today.
Open questions before shipping: ONNX Runtime Web support and speed for the int4 model in the
extension's offscreen worker (CSP `'wasm-unsafe-eval'`, threads need cross-origin isolation); where
the 22 MB lives (bundled vs downloaded once); the training data's licence (openpii) beyond the model's
Apache-2.0; more false positives than rules alone (+114 on corpus 2 with all tags, +48 with names only).
