# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "conclusion_v2", "created_at": "2026-07-25T12:00:00+00:00", "title": "Five finite diagnostics pass; paper-level result INCONCLUSIVE"}
-->
## Outcome: 5/5 finite diagnostics pass; 0/5 paper claims verified

The audit produces reproducible finite evidence for five selected constructions
from arXiv 2508.12674v2. These computations do not prove the theorems or
establish their asymptotic and general-model claims, so the paper-level result
remains **INCONCLUSIVE**.

| Claim | Theorem | Verdict | What was tested | Scale |
|---|---|---|---|---|
| C1 | Thm 1 | **FINITE PROXY PASS** | Cross-sect + selected longitudinal stability, rate decay | n ≤ 2000 |
| C2 | Thm 2 | **FINITE PROXY PASS** | Finite convergence-rate diagnostic, ρ ordering | n ≤ 800, ρ ∈ {0.25, 0.5, 1.0} |
| C3 | Thm 3 | **FINITE PROXY PASS** | Selected population identities near machine precision | n ≤ 2400 |
| C4 | Thm 4 | **FINITE PROXY PASS** | Finite stability sweep and one degree-varying construction | n ≤ 2000 |
| C5 | Prop 1 | **FINITE PROXY PASS** | Dynamic Cheeger inequalities on finite graphs | n ≤ 20, T ≤ 6 |

### Key improvements over previous (4/10) diagnostic run

1. **Claim 3 (was INCONCLUSIVE):** Adds a finite population-identity check with errors near 10⁻¹⁷.
2. **Claim 2 (was TOY):** Adds rate fitting with an n × ρ sweep and bounded finite rate constants.
3. **Claims 1 and 4 (were TOY):** Use larger finite DSBM sweeps and selected stability metrics.
4. **Claim 5 (was TOY):** Extends the finite graph suite to n ≤ 20, T ≤ 6, with 28 cases.


---
<!-- trackio-cell
{"type": "markdown", "id": "conclusion_v2_scope", "created_at": "2026-07-25T12:00:00+00:00", "title": "Scope and limitations"}
-->
### Limitations

- **Claims 1, 2, 4:** Finite diagnostics on DSBM. The theorems cover broader models and asymptotic statements that are not established here.
- **Claim 5:** Exhaustive conductance is limited to n ≤ 20 (2²⁰ subsets); finite inequality checks do not replace the general proof.
- **Correction term discrepancy:** The paper's main text uses UΣ¹ᐟ² while the code and appendix use UΣ⁻¹ᐟ². We use Σ⁻¹ᐟ²; the selected finite population construction passes with that convention, and the discrepancy is documented.
- **Theorem 4 proof gap:** The supplementary material does not contain a proof of Theorem 4 despite the paper's claim. This audit records finite numerical evidence only.

### Compute

| | This verification |
|---|---|
| Hardware | 8-core CPU (Apple M-series), 16 GB RAM |
| Software | Python 3.12, NumPy 2.5.1, SciPy 1.18.0 |
| Runtime | ~60 seconds |
| Cost | $0 |
