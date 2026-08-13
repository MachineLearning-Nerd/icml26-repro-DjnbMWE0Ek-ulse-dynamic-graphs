---
title: "ICML 2026 — ULSE Dynamic Graph Embedding"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - icml2026-repro
 - paper-audit
 - paper-DjnbMWE0Ek
---

# ICML 2026 — ULSE Dynamic Graph Embedding

Paper-level status: **INCONCLUSIVE**

This repository is an independent, clean-room audit of *Unfolded Laplacian
Spectral Embedding: A Theoretically Grounded Approach to Dynamic Network
Representation*. It runs bounded numerical diagnostics for five theoretical
claims. It does not prove the theorems or reproduce every model assumption,
real-world experiment, baseline, or asymptotic result.

The canonical repository name is `icml26-ulse-dynamic-graphs`. The original
collection name was `icml26-repro-DjnbMWE0Ek-ulse-dynamic-graphs`.

## Paper

- Title: *Unfolded Laplacian Spectral Embedding: A Theoretically Grounded Approach to Dynamic Network Representation*
- Authors: Haruka Ezoe, Hiroki Matsumoto, and Ryohei Hisano
- Audit source: [arXiv:2508.12674v2](https://arxiv.org/abs/2508.12674v2), last revised 2026-02-23
- OpenReview: [DjnbMWE0Ek](https://openreview.net/forum?id=DjnbMWE0Ek)
- Venue record: ICML 2026
- Clean-room implementation: `repro/src/core.py`
- Source snapshot used by the raw run: [ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2508.12674), captured 2026-07-25

The paper introduces ULSE-n1 and ULSE-n2, unfolded normalized-Laplacian
embeddings for dynamic networks. Its theory studies cross-sectional and
longitudinal stability under a dynamic stochastic block model and gives a
dynamic Cheeger-type inequality. The paper also reports synthetic and
real-world dynamic-network experiments.

## Audit result

**Finite proxy diagnostics:** 5/5 pass<br>
**Paper claims independently verified:** 0/5<br>
**Paper-level result:** **INCONCLUSIVE**

The raw numerical labels are stored in
[`repro/outputs/verify_all_results.json`](repro/outputs/verify_all_results.json).
The conservative paper-level ledger is
[`repro/outputs/verdict.json`](repro/outputs/verdict.json), and the publication
gate is [`publication_gate.json`](publication_gate.json). A finite diagnostic
passing is evidence that the scoped computation ran and met its local
criterion; it is not proof of the associated theorem.

## Claim-to-evidence ledger

| ID | Paper target | Evidence produced here | Status |
| --- | --- | --- | --- |
| C1 | Theorem 1: ULSE-n1 cross-sectional and longitudinal stability | Five-seed DSBM sweep at `n` in `{200, 500, 1000, 2000}`; same-community and equal-`B` snapshot errors decrease, with a finite rate proxy | `FINITE_DSBM_STABILITY_PROXY` |
| C2 | Theorem 2: `O(1/(rho^1/2 n^1/2))` two-to-infinity convergence | `n` × `rho` × seed sweep, Procrustes alignment, log-log slope, bounded finite rate constants, and rho ordering | `FINITE_RATE_PROXY` |
| C3 | Theorem 3: noise-free ULSE-n1 stability | Deterministic population matrices at `n` up to 2400; selected same-community and repeated-snapshot rows agree to floating-point tolerance | `FINITE_POPULATION_IDENTITY_PROXY` |
| C4 | Theorem 4: ULSE-n2 stability and degree relaxation | Finite ULSE-n2 DSBM sweep plus one selected degree-varying construction with approximately `1.86x` degree ratio | `FINITE_DEGREE_RELAXATION_PROXY` |
| C5 | Proposition 1: dynamic Cheeger inequality | 28 finite graph cases, exhaustive two-way conductance for `n` up to 20 and `T` up to 6; 10 lower bounds are non-vacuous | `FINITE_CHEEGER_PROXY` |

Every row is narrower than its paper target. The numerical evidence does not
establish a proof, almost-sure asymptotic statement, or general result over
all admissible graphs and parameters.

## How each claim is produced

Run the raw experiment and then finalize the conservative ledger:

```bash
uv run python -m repro.src.verify_all
uv run python -m repro.src.finalize_gate
python3 -m json.tool repro/outputs/verdict.json
python3 -m json.tool publication_gate.json
```

The raw verifier writes `repro/outputs/verify_all_results.json`; the finalizer
reads those measurements and writes `repro/outputs/verdict.json`,
`repro/outputs/gate.json`, and `publication_gate.json`.

1. **C1:** `verify_claim1()` samples DSBM adjacency matrices, builds ULSE-n1
   embeddings, measures maximum same-community and repeated-`B` temporal
   errors after alignment, and fits their finite decay across `n`.
2. **C2:** `verify_claim2()` compares sampled and population ULSE-n1
   embeddings after Procrustes alignment, sweeps `n`, `rho`, and five seeds,
   and checks a finite log-log slope and scaled-error diagnostic.
3. **C3:** `verify_claim3()` replaces adjacency matrices by DSBM probability
   matrices and checks selected population identities at machine precision;
   this is a finite algebraic construction check.
4. **C4:** `verify_claim4()` runs ULSE-n2 on uniform-structure DSBM instances,
   then evaluates one degree-varying construction to test the claimed
   relaxation in a bounded setting.
5. **C5:** `verify_claim5()` builds complete, cycle, path, and random dynamic
   graphs, enumerates two-way cuts, computes the unfolded spectral quantities,
   and checks both finite inequality directions.

## What is not reproduced

- The proofs, almost-sure limits, general constants, and full admissible model
  classes for Theorems 1–4.
- The full inhomogeneous random-graph parameter space beyond the selected DSBM
  constructions.
- Paper-scale real-world dynamic-network data, baselines, figures, and
  ablations.
- A general proof of the degree-uniformity relaxation in Theorem 4.
- Dynamic Cheeger verification beyond the finite exhaustive graphs possible in
  this checkout.

The implementation follows the normalized-Laplacian constructions documented
in the paper and records a discrepancy where the paper's main-text correction
term differs from the code/appendix convention. That implementation choice is
documented in `reports/ulse-theorem-verification/report.md`; it is not treated
as independent proof of the theorem.

## Branches

| Branch | Role | Status |
| --- | --- | --- |
| `main` | Canonical publication surface containing the code, raw results, conservative gate, report, and logbook | Current default branch |
| `orx/ulse-full-scale-theorem-verification` | Historical experiment branch used for the full-scale run; its relevant content was incorporated into `main` | Removed after publication |

Branch cleanup is repository hygiene. It does not increase scientific
evidence. See [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md) for the migration and
attribution record.

## Repository map

- `repro/src/core.py` — clean-room ULSE-n1/n2 implementation and utilities.
- `repro/src/verify_all.py` — raw finite diagnostics for C1–C5.
- `repro/src/finalize_gate.py` — conservative claim ledger and publication gate.
- `repro/outputs/verify_all_results.json` — raw measurements and finite pass labels.
- `repro/outputs/verdict.json` — canonical paper-level evidence ledger.
- `repro/outputs/gate.json` — machine-readable scoped gate.
- `publication_gate.json` — root-level publication summary.
- `reports/ulse-theorem-verification/report.md` — detailed finite-evidence report.
- `pages/` and `index.html` — Trackio-style human-readable logbook.
- `STATUS.md` and `GATE_READY.md` — concise handoff and gate decision.
- `BRANCH_AUDIT.md` — branch roles, migration, and commit attribution.

## Citation

```bibtex
@inproceedings{ezoe2026ulse,
  title={Unfolded Laplacian Spectral Embedding: A Theoretically Grounded Approach to Dynamic Network Representation},
  author={Ezoe, Haruka and Matsumoto, Hiroki and Hisano, Ryohei},
  booktitle={Proceedings of the 43rd International Conference on Machine Learning},
  year={2026},
  url={https://arxiv.org/abs/2508.12674v2}
}
```

## Thank you

Thank you to Haruka Ezoe, Hiroki Matsumoto, and Ryohei Hisano for developing
ULSE and sharing a clear mathematical framework for stable dynamic-network
representations. The paper's separation of cross-sectional, longitudinal, and
spectral guarantees provided a useful structure for this bounded audit.

## Attribution

This independent audit and its documentation are maintained by
[MachineLearning-Nerd](https://github.com/MachineLearning-Nerd). The paper's
ideas, terminology, figures, and scientific claims remain the authors' work.
