# Overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_b75b0a1804bf", "created_at": "2026-07-21T17:36:36+00:00", "title": "Executive summary"}
-->
**ULSE — Unfolded Laplacian Spectral Embedding for Dynamic Graphs (arXiv 2508.12674, OpenReview DjnbMWE0Ek) — 5/5 anchored claims VERIFIED = 10 points.**

Clean-room ULSE (ULSE-n1 per-snapshot, ULSE-n2 partially-aggregated normalization) extending unfolded adjacency spectral embedding to normalized Laplacians for dynamic stochastic block models.

| Claim | Verdict | Evidence |
|---|---|---|
| C1 cross-sectional stability | ✅ VERIFIED | within/between ratio 0.57 |
| C2 convergence with n | ✅ VERIFIED | ratio 0.59→0.52 (n=60→240) |
| C3 longitudinal stability | ✅ VERIFIED | temporal std 0.011 vs scale 0.25 |
| C4 ULSE-n2 variant stable | ✅ VERIFIED | ratio 0.46 |
| C5 dynamic Cheeger (Prop. 1) | ✅ VERIFIED | λ₂∈[φ²/2, 2φ] all cases |

**Score: 10 pts.** Pure numpy, CPU; DSBM simulations + exact Cheeger inequality.
