# Methods


---
<!-- trackio-cell
{"type": "markdown", "id": "methods_v2", "created_at": "2026-07-25T12:00:00+00:00", "title": "Implementation — faithful ULSE-n1/n2"}
-->
## Implementation

**Code:** `repro/src/core.py` — clean-room ULSE implementation matching the paper and official code (github.com/hisanor013/ULSE).

### ULSE-n1 (Theorems 1–3)

1. **Normalized Laplacian:** L⁽ᵗ⁾ = I − D_r⁻¹ᐟ² A⁽ᵗ⁾ D_r⁻¹ᐟ², where D_r = D + 0.1I (regularization per paper §4)
2. **Unfolded operator:** L = [L⁽¹⁾ | ... | L⁽ᵀ⁾] ∈ ℝⁿˣⁿᵀ
3. **Spectral decomposition:** Eigendecompose M = LL^T = Σₜ L⁽ᵗ⁾L⁽ᵗ⁾ᵀ for numerical stability
4. **Selection:** Bottom K eigenpairs, exclude smallest (trivial), take K−1 informative directions (d = K−1)
5. **Embedding:** Ŷ⁽ᵗ⁾ = (L⁽ᵗ⁾ − I) U Σ⁻¹ᐟ² (derived from V⁽ᵗ⁾Σ¹ᐟ² − UΣ⁻¹ᐟ² via V⁽ᵗ⁾ = L⁽ᵗ⁾UΣ⁻¹)

**Note on correction term:** The paper's main text states Ŷ⁽ᵗ⁾ = V⁽ᵗ⁾Σ¹ᐟ² − UΣ¹ᐟ², but the official code and Appendix C proof use Σ⁻¹ᐟ². The finite population diagnostic produces exact agreement with Σ⁻¹ᐟ² in the selected construction while Σ¹ᐟ² does not. We follow the code/appendix version.

### ULSE-n2 (Theorem 4)

1. **Partially aggregated normalization:** L⁽ᵗ⁾ = −D^{(1:T)}⁻¹ᐟ² A⁽ᵗ⁾ D⁽ᵗ⁾⁻¹ᐟ²
2. **Selection:** Top K eigenpairs (largest singular values)
3. **Embedding:** Ŷ⁽ᵗ⁾ = L⁽ᵗ⁾ U Σ⁻¹ᐟ² (no correction term)

### Noise-free embeddings

Replace A⁽ᵗ⁾ with P⁽ᵗ⁾ everywhere. Identical computation otherwise.

### DSBM generator

P_{ij}⁽ᵗ⁾ = ρ B_{z_i z_j}⁽ᵗ⁾. Community labels drawn from categorical(π). B matrices follow the paper's merging pattern: t=0 distinct, t=1 merge 0&1, t≥2 merge 1&2.


---
<!-- trackio-cell
{"type": "markdown", "id": "methods_v2_env", "created_at": "2026-07-25T12:00:00+00:00", "title": "Environment"}
-->
## Environment

- **Python:** ≥3.11, <3.14
- **Dependencies:** numpy ≥2.0, scipy ≥1.13 (managed via `uv`)
- **Lockfile:** `uv.lock` (exact versions: numpy 2.5.1, scipy 1.18.0)
- **Run command:** `uv run python -m repro.src.verify_all`
- **Runtime:** ~60 seconds on 8-core CPU

````python title=pyproject.toml
[project]
name = "ulse-repro"
requires-python = ">=3.11,<3.14"
dependencies = ["numpy>=2.0,<3.0", "scipy>=1.13,<2.0"]
````


---
<!-- trackio-cell
{"type": "markdown", "id": "methods_v2_seeds", "created_at": "2026-07-25T12:00:00+00:00", "title": "Reproducibility"}
-->
## Reproducibility

- Deterministic seeds: `SEED_BASE = 20260725`, per-configuration seeds derived deterministically
- Claim 3 (noise-free): fully deterministic, no RNG
- Claims 1, 2, 4: 5 seeds per configuration
- Claim 5: fully deterministic graph families + `rng = np.random.default_rng(42)` for random graphs
- All raw data saved to `repro/outputs/verify_all_results.json`
