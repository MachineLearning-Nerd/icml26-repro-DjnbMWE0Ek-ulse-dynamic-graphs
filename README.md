---
title: "Repro - ULSE Dynamic Graph Embedding (arXiv 2508.12674)"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-DjnbMWE0Ek
---

# Reproduction: ULSE — Unfolded Laplacian Spectral Embedding (arXiv 2508.12674)

**Paper:** Unfolded Laplacian Spectral Embedding: A Theoretically Grounded Approach to Dynamic Network Representation (Ezoe, Matsumoto, Hisano, 2025)

**OpenReview:** https://openreview.net/forum?id=DjnbMWE0Ek

## What was tested

All five theoretical claims of the paper are verified with faithful, full-scale evidence:

| Claim | Theorem | Assessment | Paper claim | Observed | Scale |
|---|---|---|---|---|---|
| C1 | Thm 1: ULSE-n1 stability | **VERIFIED** | Cross-sect & long. stability at rate O(1/(ρ¹ᐟ²n¹ᐟ²)) | Errors decay as n⁻⁰·⁹, within-comm → 0 | n ≤ 2000 |
| C2 | Thm 2: Convergence rate | **VERIFIED** | O(1/(ρ¹ᐟ²n¹ᐟ²)) | Rate constant C ≤ 0.49, bounded | n ≤ 800 |
| C3 | Thm 3: Noise-free stability | **VERIFIED** | Exact cross-sect & long. stability | Errors ~10⁻¹⁷ (machine precision) | n ≤ 2400 |
| C4 | Thm 4: ULSE-n2 stability | **VERIFIED** | Both stability props + degree relaxation | Both decay; degree var (1.86×) doesn't break stability | n ≤ 2000 |
| C5 | Prop 1: Dynamic Cheeger | **VERIFIED** | Spectral-conductance inequality | 28/28 cases pass, 10 non-vacuous | n ≤ 20 |

**Compute:** Local CPU (8 cores), ~60 seconds total. NumPy + SciPy only. No GPU.

**Substitutions:** None — all claims tested at the paper's stated assumptions (DSBM model).

## Experiment log

| Branch | Purpose | Run command | Outcome | Compute |
|---|---|---|---|---|
| `main` | Publication surface (logbook pages) | Not run as an experiment (publication surface) | — | — |
| `orx/ulse-full-scale-theorem-verification` | Full-scale theorem verification | `uv run python -m repro.src.verify_all` | All 5 claims VERIFIED (56s) | Local CPU |

## How to reproduce

```bash
uv run python -m repro.src.verify_all
```

This runs all 5 claim verifiers and saves results to `repro/outputs/verify_all_results.json`.

## Detailed report

See `reports/ulse-theorem-verification/report.md` for the full visual report with figures, implementation details, and per-claim analysis.

## Code

- `repro/src/core.py` — ULSE-n1/n2 implementation (DSBM, Laplacians, embeddings, Procrustes, conductance)
- `repro/src/verify_all.py` — All 5 claim verifiers
- `repro/src/verify_dynamic_cheeger_exact.py` — Independent dynamic Cheeger audit
- `repro/src/audit_dynamic_cheeger_proof_chain.py` — Exact-rational proof-chain audit

An open experiment logbook, published with [Trackio](https://github.com/gradio-app/trackio).
