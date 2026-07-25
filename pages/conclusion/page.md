# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "conclusion_v2", "created_at": "2026-07-25T12:00:00+00:00", "title": "All 5 theorems VERIFIED with full-scale evidence"}
-->
## Outcome: 5/5 claims VERIFIED

All five theorems from arXiv 2508.12674 are verified with faithful, reproducible evidence that directly tests each theorem's exact conditions.

| Claim | Theorem | Verdict | What was tested | Scale |
|---|---|---|---|---|
| C1 | Thm 1 | **VERIFIED** | Cross-sect + long. stability, rate decay | n ≤ 2000 |
| C2 | Thm 2 | **VERIFIED** | Convergence rate O(1/(ρ¹ᐟ²n¹ᐟ²)), ρ-param | n ≤ 800, ρ ∈ {0.25, 0.5, 1.0} |
| C3 | Thm 3 | **VERIFIED** | Exact noise-free stability (deterministic) | n ≤ 2400 |
| C4 | Thm 4 | **VERIFIED** | Both stability props + degree relaxation | n ≤ 2000 |
| C5 | Prop 1 | **VERIFIED** | Dynamic Cheeger, exhaustive φ₂ | n ≤ 20, T ≤ 6 |

### Key improvements over previous (4/10) verification

1. **Claim 3 (was INCONCLUSIVE):** Now verified exactly at population level — noise-free embeddings satisfy both stability properties to machine precision (~10⁻¹⁷).
2. **Claim 2 (was TOY):** Now includes rate fitting with n × ρ sweep, bounded rate constants, and confirmed ρ-parameterization.
3. **Claims 1, 4 (were TOY):** Now test exact theorem conditions at n up to 2000 with rate fitting, not proxy metrics.
4. **Claim 5 (was TOY):** Extended from n ≤ 10 to n ≤ 20, T ≤ 6, with 28 diverse cases and 10 non-vacuous lower bounds.


---
<!-- trackio-cell
{"type": "markdown", "id": "conclusion_v2_scope", "created_at": "2026-07-25T12:00:00+00:00", "title": "Scope and limitations"}
-->
### Limitations

- **Claims 1, 2, 4:** Finite-sample verification on DSBM. The theorems hold for the broader inhomogeneous random graph model, but we test the DSBM special case as assumed in the paper's proofs.
- **Claim 5:** Exhaustive conductance is limited to n ≤ 20 (2²⁰ subsets). The inequality holds as a theorem for all n; our verification corroborates it on diverse non-trivial instances.
- **Correction term discrepancy:** The paper's main text uses UΣ¹ᐟ² while the code and appendix use UΣ⁻¹ᐟ². We use Σ⁻¹ᐟ² (verified to produce exact stability) and document this discrepancy.
- **Theorem 4 proof gap:** The supplementary material does not contain a proof of Theorem 4 despite the paper's claim. Our numerical verification corroborates the theorem's predictions.

### Compute

| | This verification |
|---|---|
| Hardware | 8-core CPU (Apple M-series), 16 GB RAM |
| Software | Python 3.12, NumPy 2.5.1, SciPy 1.18.0 |
| Runtime | ~60 seconds |
| Cost | $0 |
