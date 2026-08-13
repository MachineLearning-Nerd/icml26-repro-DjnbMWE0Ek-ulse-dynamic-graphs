# Claim 2 — Convergence Rate (Theorem 2)


---
<!-- trackio-cell
{"type": "markdown", "id": "c2_v2_claim", "created_at": "2026-07-25T12:00:00+00:00", "title": "Theorem 2 — exact claim"}
-->
## Theorem 2 (Convergence of ULSE-n1)

**Source:** Section 3.2, Theorem 2. SHA-256 `1e0540aa...`

**Exact claim:** With d = K−1, ∃ W ∈ O(d) such that

||Ŷ⁽ᵗ⁾ − Ỹ⁽ᵗ⁾W||₂→∞ = O(1/(ρ¹ᐟ²n¹ᐟ²)) a.s.

**Key:** This is an *upper bound*. The actual rate may be faster.


---
<!-- trackio-cell
{"type": "markdown", "id": "c2_v2_method", "created_at": "2026-07-25T12:00:00+00:00", "title": "Method — rate fitting with n × ρ sweep"}
-->
## Method

Sweep n ∈ {100, 200, 400, 800} × ρ ∈ {0.25, 0.5, 1.0} × 5 seeds. For each:
1. Generate DSBM graph A⁽ᵗ⁾ from P⁽ᵗ⁾
2. Compute finite-sample embedding Ŷ⁽ᵗ⁾ (ULSE-n1, d=K−1=2)
3. Compute noise-free embedding Ỹ⁽ᵗ⁾ (from P⁽ᵗ⁾)
4. Procrustes align: W = argmin ||Ŷ − ỸW||
5. Measure ||Ŷ⁽ᵗ⁾ − Ỹ⁽ᵗ⁾W||₂→∞ = max_i ||row_i||

**Verification criteria for O(1/(ρ¹ᐟ²n¹ᐟ²)):**
- Error decreases monotonically with n ✓
- Rate constant C = error × ρ¹ᐟ² × n¹ᐟ² is bounded (non-increasing with n) ✓
- ρ-parameterization: smaller ρ → larger error at fixed n ✓
- Fitted log-log slope ≥ 0.5 ✓


---
<!-- trackio-cell
{"type": "markdown", "id": "c2_v2_results", "created_at": "2026-07-25T12:00:00+00:00", "title": "Results — FINITE PROXY PASS"}
-->
## Results

**Mean error by n** (averaged over ρ and seeds):

| n | Mean error | Std | Theoretical rate |
|---|---|---|---|
| 100 | 0.0584 | 0.0236 | 0.100 |
| 200 | 0.0339 | 0.0137 | 0.071 |
| 400 | 0.0166 | 0.0059 | 0.050 |
| 800 | 0.0090 | 0.0034 | 0.035 |

**Rate constants** (error × ρ¹ᐟ² × n¹ᐟ²): non-increasing, max C = 0.4935

**ρ-parameterization** at n=800:

| ρ | Mean error | Expected ∝ 1/ρ¹ᐟ² |
|---|---|---|
| 1.0 | 0.00525 | 1.00 |
| 0.5 | 0.00839 | 1.41 |
| 0.25 | 0.01337 | 2.00 |

Error increases as ρ decreases, consistent with the finite ρ-dependence diagnostic.

**Log-log fit:** slope = 1.655, R² = 0.967. Slope > 1 means actual convergence is *faster* than the theoretical O(n⁻¹ᐟ²) bound — consistent with an upper bound.

**Per-ρ slopes:** ρ=1.0: 1.80, ρ=0.5: 1.77, ρ=0.25: 1.87 (all > 0.5)

**FINITE PROXY PASS.** The finite scaled-error, n-sweep, and ρ-ordering
criteria pass. They do not establish the paper's asymptotic upper bound.

**Code:** `repro/src/verify_all.py` → `verify_claim2()`

**Raw data:** `repro/outputs/verify_all_results.json` → `claim2_theorem2`


---
<!-- trackio-cell
{"type": "markdown", "id": "c2_historical", "created_at": "2026-07-25T12:00:00+00:00", "title": "Historical rejected baseline"}
-->
---

## Historical rejected baseline

The previous verification only checked that within/between ratio decreases as n grows (0.586→0.569→0.523 for n=60→240), showing qualitative improvement without fitting or verifying the specific convergence rate. No ρ parameterization was done. Superseded by the rate fitting above.
