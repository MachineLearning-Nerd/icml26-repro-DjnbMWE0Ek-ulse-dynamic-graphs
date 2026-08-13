# Claim 4 — ULSE-n2 Stability (Theorem 4)


---
<!-- trackio-cell
{"type": "markdown", "id": "c4_v2_claim", "created_at": "2026-07-25T12:00:00+00:00", "title": "Theorem 4 — exact claim"}
-->
## Theorem 4 (Stability of ULSE-n2)

**Source:** Section 3.3, Theorem 4. SHA-256 `1e0540aa...`

**Exact claim:** If M̄ has rank K, setting d = K:

1. ∃ Y⁽ᵗ⁾ such that max_{i,t} ||Ŷ_i:⁽ᵗ⁾ − Y_i:⁽ᵗ⁾|| = O(1/(ρ¹ᐟ²n¹ᐟ²)) a.s.
2. **Cross-sectional:** B_{z_i:}⁽ᵗ⁾ = B_{z_j:}⁽ᵗ⁾ ⟹ Y_i:⁽ᵗ⁾ = Y_j:⁽ᵗ⁾
3. **Longitudinal:** B_{z_i:}⁽ᵗ⁾ = B_{z_i:}⁽ᵘ⁾ ⟹ Y_i:⁽ᵗ⁾ = Y_i:⁽ᵘ⁾

**Key difference from ULSE-n1:** Longitudinal stability does NOT require D̃⁽ᵗ⁾ = D̃⁽ᵘ⁾. Only B⁽ᵗ⁾ = B⁽ᵘ⁾ is needed. This is the degree-uniformity relaxation.

**ULSE-n2 normalization:** L⁽ᵗ⁾ = −D^{(1:T)}⁻¹ᐟ² A⁽ᵗ⁾ D⁽ᵗ⁾⁻¹ᐟ² (partially time-aggregated). No correction term: Ŷ⁽ᵗ⁾ = V⁽ᵗ⁾Σ¹ᐟ².


---
<!-- trackio-cell
{"type": "markdown", "id": "c4_v2_method", "created_at": "2026-07-25T12:00:00+00:00", "title": "Method — both stability properties + degree relaxation"}
-->
## Method

**Part 1 — Stability with uniform B:** K=3, T=4, ρ=1.0, identical B across all snapshots. Measures cross-sectional (within-community) and longitudinal (across-time, after Procrustes) embedding errors. n ∈ {200, 500, 1000, 2000}, 5 seeds.

**Part 2 — Degree-uniformity relaxation:** Constructs DSBM with degree variation across snapshots by scaling B matrices by different factors (1.0, 0.7, 1.3, 0.9). This creates 1.86× degree ratio across snapshots while preserving the relative community structure. Verifies that cross-sectional stability still holds.


---
<!-- trackio-cell
{"type": "markdown", "id": "c4_v2_results", "created_at": "2026-07-25T12:00:00+00:00", "title": "Results — FINITE PROXY PASS"}
-->
## Results — Uniform B stability

| n | Cross-sectional max | Longitudinal max | Between-community |
|---|---|---|---|
| 200 | 0.0225 | 0.0204 | 0.0651 |
| 500 | 0.0099 | 0.0089 | 0.0415 |
| 1000 | 0.0054 | 0.0048 | 0.0292 |
| 2000 | 0.0029 | 0.0025 | 0.0208 |

**Cross-sectional decay exponent:** 0.890 (> 0.5, consistent with the finite O(n⁻¹ᐟ²) diagnostic)

Both selected errors decay to zero in this finite DSBM sweep.

## Results — Degree-uniformity relaxation

| Configuration | Degree ratio | Cross-sectional error |
|---|---|---|
| B scaled [1.0, 0.7, 1.3, 0.9] | 1.86× | 0.0127 |

Cross-sectional stability holds in the selected degree-varying construction,
providing finite evidence consistent with the relaxation in Theorem 4.

**FINITE PROXY PASS.** The selected ULSE-n2 sweep and degree-varying
construction pass their local criteria. They do not establish the general
Theorem 4 statement.

**Code:** `repro/src/verify_all.py` → `verify_claim4()`

**Raw data:** `repro/outputs/verify_all_results.json` → `claim4_theorem4`


---
<!-- trackio-cell
{"type": "markdown", "id": "c4_historical", "created_at": "2026-07-25T12:00:00+00:00", "title": "Historical rejected baseline"}
-->
---

## Historical rejected baseline

The previous verification tested ULSE-n2 with d=3=K on small DSBM (n=120) measuring only cross-sectional separation ratio (0.455). It did not verify both stability properties, test the convergence rate, or test the relaxation of the degree-uniformity assumption. Superseded by the full-scale verification above.
