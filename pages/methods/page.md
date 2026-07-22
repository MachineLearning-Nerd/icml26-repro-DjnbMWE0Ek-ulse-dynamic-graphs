# Methods


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_8a720c8a386c", "created_at": "2026-07-21T17:36:40+00:00", "title": "Clean-room ULSE + DSBM + Cheeger"}
-->
**Core** `repro/src/core.py`: normalized Laplacian (n1 per-snapshot, n2 aggregated-degree), unfolded L=[L^(1)|...|L^(T)], rank-d truncated SVD (d smallest non-trivial singular values), anchor X̂=UΣ^{1/2} + dynamic Ŷ^(t)=V^(t)Σ^{1/2}−UΣ^{-1/2}; DSBM generator; conductance; k-way conductance.

**Verification:** stability checked as within/between-community embedding-distance ratios and temporal variance on DSBM simulations; Cheeger checked as the exact eigenvalue-conductance inequality on normalized Laplacians. Deterministic RNG.
