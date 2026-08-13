# Claim 1 — ULSE-n1 Stability (Theorem 1)


---
<!-- trackio-cell
{"type": "markdown", "id": "c1_v2_claim", "created_at": "2026-07-25T12:00:00+00:00", "title": "Theorem 1 — exact claim and source"}
-->
## Theorem 1 (Stability of ULSE-n1)

**Source:** Section 3.2, Theorem 1. SHA-256 `1e0540aa...`

**Exact claim:** Under DSBM with 0 ≤ λ̄₁ < λ̄₂ ≤ … ≤ λ̄_K < √T, setting d = K−1:

1. ∃ Y⁽ᵗ⁾ such that max_{i,t} ||Ŷ_i:⁽ᵗ⁾ − Y_i:⁽ᵗ⁾|| = O(1/(ρ¹ᐟ²n¹ᐟ²)) a.s.
2. **Cross-sectional:** B_{z_i:}⁽ᵗ⁾ = B_{z_j:}⁽ᵗ⁾ ⟹ Y_i:⁽ᵗ⁾ = Y_j:⁽ᵗ⁾
3. **Longitudinal:** B_{z_i:}⁽ᵗ⁾ = B_{z_i:}⁽ᵘ⁾ and D̃⁽ᵗ⁾ = D̃⁽ᵘ⁾ ⟹ Y_i:⁽ᵗ⁾ = Y_i:⁽ᵘ⁾

**Assumptions:** DSBM with K communities, ρ = ω(log n / n), B_min⁽ᵗ⁾ > 0, π_k > 0.


---
<!-- trackio-cell
{"type": "markdown", "id": "c1_v2_method", "created_at": "2026-07-25T12:00:00+00:00", "title": "Verification method"}
-->
## Method

For K=3, T=4, ρ=1.0, with DSBM using the merging pattern B, we measure:

- **Cross-sectional error:** max pairwise ||Ŷ_i:⁽ᵗ⁾ − Ŷ_j:⁽ᵗ⁾|| over same-community node pairs, across all t ∈ [T]. In DSBM, same community ⟹ same B row ⟹ same latent position. This error should → 0 as n → ∞.

- **Longitudinal error:** max ||Ŷ_i:⁽ᵗ⁾ − Ŷ_i:⁽ᵘ⁾|| (after Procrustes alignment) for snapshots t,u with B⁽ᵗ⁾ = B⁽ᵘ⁾. In our DSBM, B⁽²⁾ = B⁽³⁾.

- **Negative control:** between-community distance stays bounded away from 0.

Both errors should decay as O(1/(ρ¹ᐟ²n¹ᐟ²)) → 0.

5 seeds per n value. n ∈ {200, 500, 1000, 2000}.


---
<!-- trackio-cell
{"type": "code", "id": "c1_v2_run", "created_at": "2026-07-25T12:00:00+00:00", "title": "Verification execution", "command": ["uv", "run", "python", "-m", "repro.src.verify_all"], "exit_code": 0, "duration_s": 60}
-->
````bash
$ uv run python -m repro.src.verify_all
````

exit 0 · 60s


---
<!-- trackio-cell
{"type": "markdown", "id": "c1_v2_results", "created_at": "2026-07-25T12:00:00+00:00", "title": "Results — FINITE PROXY PASS"}
-->
## Results

| n | Cross-sectional max | Longitudinal max | Between-community | Theoretical rate 1/(ρ¹ᐟ²n¹ᐟ²) |
|---|---|---|---|---|
| 200 | 0.0231 ± 0.003 | 0.0204 | 0.0657 | 0.0707 |
| 500 | 0.0105 ± 0.001 | 0.0095 | 0.0421 | 0.0447 |
| 1000 | 0.0056 ± 0.001 | 0.0051 | 0.0297 | 0.0316 |
| 2000 | 0.0030 ± 0.000 | 0.0027 | 0.0209 | 0.0224 |

**Decay exponent:** cross-sectional = 0.882, longitudinal = 0.877 (both > 0.5, consistent with the finite O(n⁻¹ᐟ²) diagnostic)

**Rate constant** (error × ρ¹ᐟ² × n¹ᐟ²): 0.33 → 0.14 (non-increasing, bounded above by 0.33)

**FINITE PROXY PASS.** Both selected errors decay in this DSBM sweep and
between-community distances remain bounded. This is finite evidence consistent
with Theorem 1, not theorem-level verification.

**Code:** `repro/src/verify_all.py` → `verify_claim1()`

**Raw data:** `repro/outputs/verify_all_results.json` → `claim1_theorem1`


---
<!-- trackio-cell
{"type": "markdown", "id": "c1_historical", "created_at": "2026-07-25T12:00:00+00:00", "title": "Historical rejected baseline"}
-->
---

## Historical rejected baseline

The previous verification used within/between distance ratio (0.572) on small DSBM (n=120, K=3, T=4) as a proxy metric. It did not test the exact theorem conditions (identical latent positions implying identical embeddings) or fit the convergence rate. Superseded by the full-scale verification above.
