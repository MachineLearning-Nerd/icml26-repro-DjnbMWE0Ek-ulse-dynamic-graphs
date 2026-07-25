# Claim 3 — Noise-free Stability (Theorem 3)


---
<!-- trackio-cell
{"type": "markdown", "id": "c3_v2_claim", "created_at": "2026-07-25T12:00:00+00:00", "title": "Theorem 3 — exact claim"}
-->
## Theorem 3 (Stability of noise-free ULSE-n1)

**Source:** Section 3.2, Theorem 3; proof in Appendix D. SHA-256 `1e0540aa...`

**Exact claim:** The noise-free embeddings Ỹ⁽ᵗ⁾ satisfy:

1. **Cross-sectional:** P_i:⁽ᵗ⁾ = P_j:⁽ᵗ⁾ ⟹ Ỹ_i:⁽ᵗ⁾ = Ỹ_j:⁽ᵗ⁾
2. **Longitudinal:** P_i:⁽ᵗ⁾ = P_i:⁽ᵘ⁾ and D̃⁽ᵗ⁾ = D̃⁽ᵘ⁾ ⟹ Ỹ_i:⁽ᵗ⁾ = Ỹ_i:⁽ᵘ⁾

**Key insight from proof (Appendix D):** Ỹ_i:⁽ᵗ⁾ = −d̃_i⁻¹ᐟ² P_i:⁽ᵗ⁾ D̃⁻¹ᐟ² Ṽ Σ̃¹ᐟ², which depends only on P_i:⁽ᵗ⁾ and community-level quantities. In DSBM, P_i:⁽ᵗ⁾ = ρB_{z_i:}⁽ᵗ⁾, so same community ⟹ same row.


---
<!-- trackio-cell
{"type": "markdown", "id": "c3_v2_method", "created_at": "2026-07-25T12:00:00+00:00", "title": "Method — exact population-level computation"}
-->
## Method

This is a **deterministic, exact computation** — no sampling noise. For DSBM with K=3, T=4:

1. Construct probability matrices P⁽ᵗ⁾ from B matrices and community labels
2. Build noise-free normalized Laplacians L̃⁽ᵗ⁾ = I − D̃_r⁻¹ᐟ² P⁽ᵗ⁾ D̃_r⁻¹ᐟ²
3. Eigendecompose M = Σₜ L̃⁽ᵗ⁾ L̃⁽ᵗ⁾ᵀ to get Ũ and Σ̃
4. Compute Ỹ⁽ᵗ⁾ = (L̃⁽ᵗ⁾ − I) Ũ Σ̃⁻¹ᐟ²
5. **Cross-sectional check:** max |Ỹ_i:⁽ᵗ⁾ − Ỹ_j:⁽ᵗ⁾| over same-community pairs — should be ~0 (machine precision)
6. **Longitudinal check:** max |Ỹ_i:⁽²⁾ − Ỹ_i:⁽³⁾| — snapshots 2,3 have identical B, should be exactly 0
7. **Negative control:** min distance between different-community embeddings — should be > 0

n ∈ {300, 600, 1200, 2400}.


---
<!-- trackio-cell
{"type": "markdown", "id": "c3_v2_results", "created_at": "2026-07-25T12:00:00+00:00", "title": "Results — VERIFIED (exact to machine precision)"}
-->
## Results

| n | Cross-sectional error | Longitudinal error | Min different-comm distance |
|---|---|---|---|
| 300 | 2.26 × 10⁻¹⁷ | 0 (exact) | 0.000514 |
| 600 | 1.47 × 10⁻¹⁷ | 0 (exact) | 0.000181 |
| 1200 | 1.39 × 10⁻¹⁷ | 0 (exact) | 0.000064 |
| 2400 | 1.04 × 10⁻¹⁷ | 0 (exact) | 0.000023 |

Cross-sectional errors are at machine precision (~10⁻¹⁷), confirming that nodes with identical latent positions receive identical noise-free embeddings.

Longitudinal errors are exactly 0, confirming that snapshots with identical B matrices produce identical embeddings for every node.

Negative control: different-community embeddings are well-separated (min distance > 0).

**VERDICT: VERIFIED.** The noise-free ULSE-n1 embeddings satisfy both stability properties exactly, at machine precision, for all tested n values up to 2400.

**Code:** `repro/src/verify_all.py` → `verify_claim3()`

**Raw data:** `repro/outputs/verify_all_results.json` → `claim3_theorem3`


---
<!-- trackio-cell
{"type": "markdown", "id": "c3_historical", "created_at": "2026-07-25T12:00:00+00:00", "title": "Historical rejected baseline"}
-->
---

## Historical rejected baseline

The previous verification only ran finite-sample DSBM simulations and checked temporal std (0.011 vs 0.25). No analytical or population-level verification of the noise-free stability was performed. Superseded by the exact computation above.
