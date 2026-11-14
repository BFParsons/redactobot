# Research: fast on-device PII and name detection (14 November 2026)

Question: are there high-speed methods for finding personal information in text that this
project has not considered? Context: rules (2-85 ms, ~86% person recall on 150-word pastes,
95-100% on structured IDs) plus Gemini Nano (0.3-1.5 s, ~93% names, 1-3 min cold start).
Sources were opened and checked; figures marked "unconfirmed" could not be verified at source.

## What is new to us: small token classifiers that run in the browser

| model | size | licence | names on real text | browser latency | organizations |
|---|---|---|---|---|---|
| masker-mini v3 (huggingface.co/amsintelligence/masker-mini; card says divergentlabs) | 22 MB ONNX int4, 35M params, MiniLM-class distilled from mDeBERTa | Apache-2.0 | names F1 0.865 (TAB legal 0.887, CoNLL-2002 Dutch 0.843) | not published | no label |
| Rampart (huggingface.co/nationaldesignstudio/rampart, npm @nationaldesignstudio/rampart) | 14.7 MB q4, 18.5M params | CC BY 4.0 | strict span F1 0.528; non-Latin names ~14% recall | measured: WASM p50 12.6 ms / p95 35.5 ms; WebGPU p50 3.9 ms | no label |
| knowledgator gliner-pii (small/base/large/edge) | ONNX ~197 MB uint8 | Apache-2.0 | F1 75.5-83.3 on its own synthetic set | not published (est. 100-300 ms) | yes (zero-shot labels) |
| urchade gliner_multi_pii-v1 | ~349 MB int8 | Apache-2.0 | - | not published | yes |
| GLiNER2-PII (arXiv 2605.09973, May 2026; fastino/gliner2-privacy-filter-PII-multi) | 0.3B, safetensors only | Apache-2.0 | best of 5 on SPY span F1 (figures unconfirmed) | - | no label |
| OpenAI Privacy Filter (huggingface.co/openai/privacy-filter, Apr 2026) | ~0.8-0.9 GB q4, MoE 1.5B/50M active | Apache-2.0 | F1 96% on PII-Masking-300k (press; unconfirmed) | WebGPU only (reported) | no label |
| dslim/distilbert-NER | ~65 MB int8 (est.) | Apache-2.0 | CoNLL-03 F1 0.922 (news, cased) | est. 15-40 ms | yes |

Not usable: piiranha (CC-BY-NC-ND), ai4privacy-trained fine-tunes (dataset licence restricts larger
for-profit use), Presidio/spaCy/Flair (Python only).

Runtimes: Transformers.js v4 (WebGPU) or ONNX Runtime Web (WASM SIMD/threads, WebGPU), inside the
extension's offscreen document + worker (not the service worker). Needs `'wasm-unsafe-eval'` in the
extension CSP; threads need cross-origin isolation. Chrome has no built-in entity-extraction API; the
Language Detector API (stable since 138) could route non-English text.

## Closest prior art (same product category)

- Casper (arXiv 2408.07004, 2024): browser extension, regex -> bert-base-NER in Transformers.js
  (~0.2 s) -> Llama-3-8B via WebLLM (~2.15 s). 98.5% PII true positives, 13.3% false positives.
- Rescriber (arXiv 2410.11876, CHI 2025): extension + local Llama3-8B via Ollama; user study only.
- RECAP (arXiv 2510.07551, 2025): regex + LLM refinement, 13 locales; relative gains only.

## Methods worth borrowing

- Confidence-routed cascades: LinkNER (arXiv 2402.10573) and UCCI (arXiv 2605.18796, isotonic-
  calibrated token-margin uncertainty; 31% fewer escalations at micro-F1 0.91). Send only uncertain
  spans to Nano.
- LLM-annotated distillation (NuNER, Otter arXiv 2601.06347): label lots of paste-like text with a
  big model, train a ~20-30M encoder. Casing augmentation (Mayhew et al., arXiv 1912.07095) targets
  ALL-CAPS and lowercase names, which every cased model misses.
- Public benchmarks (REDACT, PIIBench, SPY, hivetrace pii-bench) are self-reported and disagree;
  our corpora remain the yardstick.

## Recommendation

1. Prototype masker-mini int4 as a middle tier: rules -> masker-mini (est. 10-40 ms) -> Nano only
   when uncertain or for organizations/health. Score it on corpus 2/3 pieces in Node first
   (onnxruntime-node) before any browser work; union its spans with the rules.
2. If it helps but misses casing variants, distill our own tagger (MiniLM-L6 class) from Nano or
   GLiNER2-PII labels with casing, nickname and initial augmentation.
3. Keep GLiNER-PII (lazy 200 MB download) as the organization-capable option; OpenAI Privacy Filter
   as an offline teacher/benchmark, not shipped.
