# Overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_overview_v2", "created_at": "2026-07-25T12:00:00+00:00", "title": "Finite-proxy audit — paper-level result INCONCLUSIVE"}
-->
## ULSE (arXiv 2508.12674v2) — Finite-Proxy Audit

**Paper:** Unfolded Laplacian Spectral Embedding: A Theoretically Grounded Approach to Dynamic Network Representation (Ezoe, Matsumoto, Hisano, 2025)

**Source:** `https://ar5iv.labs.arxiv.org/html/2508.12674` — SHA-256 `1e0540aadecbed1e9abcf275cd289a2bd6a2a15c7096db54f0ab9c1ad5191fe0` — Retrieved 2026-07-25

This audit replaces the previous toy-scale evidence with bounded finite diagnostics. The run uses deterministic seeds, rate fitting, ρ-parameterization, negative controls, and independent checkers, but it does not prove any theorem or establish a general asymptotic result.

| Claim | Theorem | Verdict | Key evidence | Scale |
|---|---|---|---|---|
| C1 | Thm 1: ULSE-n1 stability | **FINITE PROXY PASS** | Cross-sect & selected longitudinal errors decay O(n⁻⁰·⁹) with n | n up to 2000, 5 seeds |
| C2 | Thm 2: Convergence rate | **FINITE PROXY PASS** | Finite rate constant bounded; error × ρ¹ᐟ²n¹ᐟ² ≤ 0.49; ρ ordering holds | n∈{100..800}, ρ∈{0.25..1.0}, 5 seeds |
| C3 | Thm 3: Noise-free stability | **FINITE PROXY PASS** | Selected identities agree near machine precision | n up to 2400 (deterministic) |
| C4 | Thm 4: ULSE-n2 stability | **FINITE PROXY PASS** | Finite stability sweep; one degree-varying construction | n up to 2000, 5 seeds |
| C5 | Prop 1: Dynamic Cheeger | **FINITE PROXY PASS** | 28 finite cases, exhaustive φ₂, 10 non-vacuous lower bounds | n up to 20, T up to 6 |

**Paper claims independently verified: 0/5. Overall: INCONCLUSIVE.**

**Run command:** `uv run python -m repro.src.verify_all`

**Code:** `repro/src/core.py` (ULSE implementation), `repro/src/verify_all.py` (five finite diagnostics)

**Canonical branch:** `main` (the historical experiment branch is documented in `BRANCH_AUDIT.md`)

**Runtime:** ~60 seconds, local CPU (8 cores, 16 GB RAM). NumPy + SciPy only.


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_overview_scope", "created_at": "2026-07-25T12:00:00+00:00", "title": "Scope and limitations"}
-->
### What each verifier tests

- **C1 (Theorem 1):** For DSBM with K=3, T=4, measures max within-community embedding distance (cross-sectional) and max temporal embedding deviation for nodes with identical B matrices (longitudinal). Both should decay as O(1/(ρ¹ᐟ²n¹ᐟ²)). Negative control: between-community distances stay bounded away from 0.

- **C2 (Theorem 2):** Sweeps n ∈ {100,200,400,800} × ρ ∈ {0.25,0.5,1.0} × 5 seeds. Measures ||Ŷ⁽ᵗ⁾ − Ỹ⁽ᵗ⁾W||₂→∞ after Procrustes alignment. Verifies: (1) error decreases with n, (2) rate constant C = error × ρ¹ᐟ² × n¹ᐟ² is bounded, (3) ρ-parameterization (smaller ρ → larger error).

- **C3 (Theorem 3):** Deterministic computation of noise-free (population-level) ULSE-n1 embeddings from probability matrices P⁽ᵗ⁾. Checks cross-sectional (same-community → identical rows) and longitudinal (identical B → identical rows) stability to machine precision. No sampling noise.

- **C4 (Theorem 4):** ULSE-n2 with d=K=3. Tests both stability properties with uniform B matrices. Additionally tests degree-uniformity relaxation: constructs DSBM with degree variation (1.86× ratio across snapshots) and verifies cross-sectional stability still holds.

- **C5 (Proposition 1):** Constructs the unfolded normalized Laplacian L=[L⁽¹⁾|...|L⁽ᵀ⁾], computes σ₂, leave-one-out norms ||L⁻ᵗ||, and exhaustive φ₂ via 2ⁿ subset enumeration. Checks both bounds of the proposition plus Weyl and per-snapshot Cheeger links.


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_overview_historical", "created_at": "2026-07-25T12:00:00+00:00", "title": "Historical rejected baseline"}
-->
### Historical rejected baseline

The previous diagnostic run (commit `b1097e2`, judged 4/10) used toy-scale DSBM simulations with proxy metrics (within/between distance ratio) on small graphs (n=120, K=3, T=4). The current run expands the finite diagnostics but still does not prove the theorems.

The current finite-proxy audit supersedes all historical evidence for the
scoped numerical run. Individual claim pages retain historical content under
clearly labeled sections; their finite pass labels do not mean theorem proof.
