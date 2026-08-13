# Claim 5 — Dynamic Cheeger (Proposition 1)


---
<!-- trackio-cell
{"type": "markdown", "id": "c5_v2_claim", "created_at": "2026-07-25T12:00:00+00:00", "title": "Proposition 1 — exact claim"}
-->
## Proposition 1 (Dynamic Cheeger bound)

**Source:** Section 3.4, Proposition 1. SHA-256 `1e0540aa...`

**Exact claim:** For the unfolded normalized Laplacian L of ULSE-n1, with σ_k its k-th singular value and L⁻ᵗ the operator with snapshot t removed:

√(max{σ_k² − min_t ||L⁻ᵗ||², 0}) / 2 ≤ φ_k(𝒢) ≤ poly(k) √σ_k

where φ_k(𝒢) = max_t φ_k(G⁽ᵗ⁾) is the dynamic k-way conductance.


---
<!-- trackio-cell
{"type": "markdown", "id": "c5_v2_method", "created_at": "2026-07-25T12:00:00+00:00", "title": "Method — direct unfolded operator, exhaustive conductance"}
-->
## Method

For k=2, we construct the unfolded normalized Laplacian and verify both bounds:

1. Build L = [L⁽¹⁾ | ... | L⁽ᵀ⁾] from per-snapshot normalized Laplacians
2. Compute σ₂ (second smallest singular value of L)
3. Compute leave-one-out norms ||L⁻ᵗ||₂ for each t
4. **Exhaustive φ₂:** enumerate all 2ⁿ vertex subsets (up to 2²⁰ ≈ 1M) per snapshot
5. Check: lower = √(max{σ₂² − min||L⁻ᵗ||², 0})/2 ≤ max_t φ₂(G⁽ᵗ⁾) ≤ √(2σ₂) = upper
6. Check Weyl links: λ_k(L⁽ᵗ⁾) ≤ σ_k ≤ √(λ_k² + ||L⁻ᵗ||²)
7. Check per-snapshot Cheeger: λ₂/2 ≤ φ₂ ≤ √(2λ₂)

**28 test cases:** repeated complete graphs (n=6..16), mixed cycle+complete (n=8..20), path+cycle (n=10..20), random graphs (n=10..20, varying density), complete graphs with varying T (T=3..6).


---
<!-- trackio-cell
{"type": "markdown", "id": "c5_v2_results", "created_at": "2026-07-25T12:00:00+00:00", "title": "Results — FINITE PROXY PASS"}
-->
## Results

**Summary:** 28/28 cases pass. Max n=20, max T=6. 10 non-vacuous lower bounds.

**Non-vacuous cases** (lower bound > 0):

| Case | σ₂ | Lower bound | φ₂ (exhaustive) | Upper bound |
|---|---|---|---|---|
| repeated_complete_6 | 2.078 | 0.600 | 0.600 | 2.039 |
| repeated_complete_8 | 1.979 | 0.571 | 0.571 | 1.990 |
| repeated_complete_10 | 1.925 | 0.556 | 0.556 | 1.962 |
| repeated_complete_12 | 1.890 | 0.545 | 0.545 | 1.944 |
| repeated_complete_14 | 1.865 | 0.538 | 0.538 | 1.931 |
| repeated_complete_16 | 1.848 | 0.533 | 0.533 | 1.922 |
| complete_10_T3 | 1.925 | 0.556 | 0.556 | 1.962 |
| complete_10_T4 | 2.222 | 0.556 | 0.556 | 2.108 |
| complete_10_T5 | 2.485 | 0.556 | 0.556 | 2.229 |
| complete_10_T6 | 2.722 | 0.556 | 0.556 | 2.333 |

The non-vacuous lower bounds are tight (lower = φ₂ for complete graphs).

All Weyl links and per-snapshot Cheeger inequalities hold in every case.

**FINITE PROXY PASS.** Both inequality directions hold for the 28 selected
finite cases, including 10 non-vacuous lower bounds. This does not replace the
general proposition or its proof.

**Code:** `repro/src/verify_all.py` → `verify_claim5()`. Also see independent audit: `repro/src/verify_dynamic_cheeger_exact.py` and `repro/src/audit_dynamic_cheeger_proof_chain.py`


---
<!-- trackio-cell
{"type": "markdown", "id": "c5_historical", "created_at": "2026-07-25T12:00:00+00:00", "title": "Historical rejected baseline"}
-->
---

## Historical rejected baseline

The previous dynamic Cheeger verification tested very small graphs (n=6,8,10, T=3,4). The current verification extends to n=20 and T=6 with 28 diverse cases. See also the exact audit page for the independent proof-chain verification.
