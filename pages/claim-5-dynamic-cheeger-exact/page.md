# Claim 5 — exact dynamic Cheeger audit

---
<!-- trackio-cell
{"type":"markdown","id":"c5_dynamic_scope","created_at":"2026-07-22T16:25:47+00:00","title":"Proposition 1 exact scope"}
-->
## Claim — supported at the actual dynamic-operator level

Proposition 1 bounds the dynamic `k`-way conductance
`phi_k(G) = max_t phi_k(G^(t))` using the singular value `sigma_k` of the
**unfolded normalized Laplacian**, together with the norm of each unfolded
operator with snapshot `t` removed. This audit replaces the earlier static-only
check with the exact dynamic quantities in the proposition.

Paper source: `https://ar5iv.labs.arxiv.org/html/2508.12674` (retrieved
2026-07-22; scope: Section 3.4, Proposition 1, proof sketch, and full
supplementary proof; SHA-256
`1e0540aadecbed1e9abcf275cd289a2bd6a2a15c7096db54f0ab9c1ad5191fe0`).

The displayed proposition is

```text
sqrt(max{sigma_k^2 - min_t ||L^(-t)||^2, 0}) / 2
    <= phi_k(dynamic graph)
    <= poly(k) sqrt(sigma_k).
```

---
<!-- trackio-cell
{"type":"markdown","id":"c5_dynamic_method","created_at":"2026-07-22T16:25:47+00:00","title":"Direct construction and exhaustive conductance"}
-->
## Direct test of the unfolded operator

For four deterministic dynamic graph families (`n=6,8,10`, `T=3,4`), the
primary verifier constructs every snapshot normalized Laplacian, horizontally
unfolds `L=[L^(1)|...|L^(T)]`, computes `sigma_2`, and computes every
`||L^(-t)||`. It also enumerates every admissible vertex subset—up to 1,022
cuts per snapshot—to obtain the exact two-way conductance rather than a
partition heuristic.

The source is visible at `repro/src/verify_dynamic_cheeger_exact.py`. Its core
dynamic calculation is:

```python
unfolded = np.concatenate(laps, axis=1)
sigma2 = float(np.sort(np.linalg.svd(unfolded, compute_uv=False))[1])
minus_norm = [
    float(np.linalg.norm(np.concatenate(laps[:t] + laps[t + 1:], axis=1), 2))
    for t in range(len(laps))
]
lower = 0.5 * sqrt(max(sigma2**2 - min(minus_norm)**2, 0.0))
dynamic_phi = max(exhaustive_phi2(snapshot) for snapshot in snapshots)
```

For `k=2`, the proposition's polynomial upper envelope specializes through the
standard Cheeger upper bound to `phi_2 <= sqrt(2 sigma_2)`. The verifier checks
both sides of the dynamic proposition, every per-snapshot Cheeger premise, and
every Weyl leave-one-out link used in the paper's proof.

---
<!-- trackio-cell
{"type":"code","id":"c5_dynamic_primary","created_at":"2026-07-22T16:25:47+00:00","title":"Primary dynamic execution","command":["uv","run","repro/src/verify_dynamic_cheeger_exact.py"],"exit_code":0,"duration_s":3.4}
-->
````bash
$ uv run repro/src/verify_dynamic_cheeger_exact.py
````

````output
Proposition 1 dynamic Cheeger audit (k=2 specialization)
source_sha256=1e0540aadecbed1e9abcf275cd289a2bd6a2a15c7096db54f0ab9c1ad5191fe0
repeated_complete_6: sigma2=2.078460969 leaveout_min=1.697056275 lower=0.600000000 <= phi_dynamic=0.600000000 <= upper=2.038853094; nonvacuous=True
  case_gates=True
repeated_complete_8: sigma2=2.285714286 leaveout_min=1.979486637 lower=0.571428571 <= phi_dynamic=0.571428571 <= upper=2.138089935; nonvacuous=True
  case_gates=True
mixed_regular_8: sigma2=1.427190815 leaveout_min=2.424168227 lower=0.000000000 <= phi_dynamic=0.333333333 <= upper=1.689491530; nonvacuous=False
  case_gates=True
mixed_regular_10: sigma2=1.154896114 leaveout_min=3.464101615 lower=0.000000000 <= phi_dynamic=0.333333333 <= upper=1.519800062; nonvacuous=False
  case_gates=True
all_20_case_level_gates_pass: True
at_least_two_nonvacuous_dynamic_lower_bounds: True
every_conductance_is_exhaustive: True
varied_dynamic_graphs_included: True
verdict: supports
RESULTS_SHA256=b79120fe892f8e79214c9ffc63865e52d5d43b0f9d9b88ca1807c3f8ef29e6bc
````

The repeated complete-graph cases make the lower bound non-vacuous and tight;
the mixed regular cases exercise different snapshots and the proposition's
explicit zero-clipping branch.

---
<!-- trackio-cell
{"type":"code","id":"c5_dynamic_independent","created_at":"2026-07-22T16:25:47+00:00","title":"Independent exact proof-chain audit","command":["python3","repro/src/audit_dynamic_cheeger_proof_chain.py"],"exit_code":0,"duration_s":0.1}
-->
````bash
$ python3 repro/src/audit_dynamic_cheeger_proof_chain.py
````

````output
Independent exact-rational Proposition 1 proof-chain audit
universal implication witnesses checked=288
nonvacuous dynamic-lower witnesses=272
control_missing_leave_one_out_upper_can_break_lower: True
control_missing_lambda_le_sigma_can_break_upper: True
control_dynamic_uses_max_not_min: True
exact_implication_witnesses: True
nonvacuous_lower_witnesses: True
all_fail_sensitive_controls: True
verdict: supports
````

The independent standard-library script shares no graph or linear-algebra code.
Using exact fractions, it verifies the general-`k` implication used by the
paper: the two Weyl inequalities and the per-snapshot higher-order Cheeger
bounds imply both displayed dynamic bounds. It covers 288 premise-satisfying
witness families, 272 with a positive lower radicand, plus three fail-sensitive
controls.

---
<!-- trackio-cell
{"type":"markdown","id":"c5_dynamic_result","created_at":"2026-07-22T16:25:47+00:00","title":"Result and artifact integrity"}
-->
## Result

**Supported.** The audit directly measures the unfolded spectrum, the
leave-one-snapshot-out norms, and the worst snapshot conductance required by
Proposition 1. All 20 numerical case gates pass, including two tight,
non-vacuous lower bounds. The independent rational audit confirms the full
proof-chain implication rather than substituting the ordinary static Cheeger
inequality for the dynamic claim.

Artifacts:

- Primary verifier SHA-256: `47d4d6f0af84a5d9a0d39bcf90345f2e1026a4c1e2e98231190af74e04dcdf42`
- Independent auditor SHA-256: `a55d3dc521b59463289748f17364ccd2e6d2887c1c53a1b8da328a4f10dcb17c`
- Saved JSON SHA-256: `d3a84034c4577d461f15fc24740aa564c867cdd22cbf4f30dd8ab27d9795f093`
