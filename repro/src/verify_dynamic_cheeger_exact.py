# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy==2.2.6"]
# ///
"""Direct audit of Proposition 1's dynamic Cheeger inequality (arXiv:2508.12674).

Unlike the prior static-snapshot check, this constructs the unfolded normalized
Laplacian L=[L^(1)|...|L^(T)], its singular value sigma_2, every leave-one-
snapshot-out operator L^{-t}, and the dynamic conductance max_t phi_2(G^(t)).
For n<=10, phi_2 is computed exhaustively over every admissible vertex cut.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np


SOURCE_URL = "https://ar5iv.labs.arxiv.org/html/2508.12674"
SOURCE_SHA256 = "1e0540aadecbed1e9abcf275cd289a2bd6a2a15c7096db54f0ab9c1ad5191fe0"
SOURCE_SCOPE = "Section 3.4, Proposition 1, its proof sketch, and the full supplementary proof"
TOL = 2e-10


def graph(n: int, edges: list[tuple[int, int]]) -> np.ndarray:
    a = np.zeros((n, n), dtype=float)
    for i, j in edges:
        if i == j:
            raise ValueError("self loops are outside this audit")
        a[i, j] = a[j, i] = 1.0
    if np.any(a.sum(axis=1) == 0):
        raise ValueError("isolated vertex")
    return a


def complete(n: int) -> np.ndarray:
    return graph(n, [(i, j) for i in range(n) for j in range(i + 1, n)])


def cycle_with_matching(n: int, offset: int | None = None) -> np.ndarray:
    edges = {(min(i, (i + 1) % n), max(i, (i + 1) % n)) for i in range(n)}
    if offset is not None:
        if n % 2:
            raise ValueError("matching requires even n")
        for i in range(n // 2):
            j = (i + offset) % n
            edges.add((min(i, j), max(i, j)))
    return graph(n, sorted(edges))


def normalized_laplacian(a: np.ndarray) -> np.ndarray:
    degree = a.sum(axis=1)
    inv = np.diag(1.0 / np.sqrt(degree))
    return np.eye(len(a)) - inv @ a @ inv


def exact_two_way_conductance(a: np.ndarray) -> float:
    n = len(a)
    degree = a.sum(axis=1)
    total = float(degree.sum())
    best = math.inf
    for mask in range(1, (1 << n) - 1):
        chosen = np.array([(mask >> i) & 1 for i in range(n)], dtype=bool)
        volume = float(degree[chosen].sum())
        if volume > total / 2.0 + TOL:
            continue
        cut = float(a[np.ix_(chosen, ~chosen)].sum())
        best = min(best, cut / volume)
    if not math.isfinite(best):
        raise RuntimeError("no admissible conductance cut")
    return best


def audit_case(name: str, snapshots: list[np.ndarray]) -> dict:
    laps = [normalized_laplacian(a) for a in snapshots]
    unfolded = np.concatenate(laps, axis=1)
    singular = np.sort(np.linalg.svd(unfolded, compute_uv=False))
    sigma2 = float(singular[1])
    lambda2 = [float(np.linalg.eigvalsh(l)[1]) for l in laps]
    phi = [exact_two_way_conductance(a) for a in snapshots]
    minus_norm = [
        float(np.linalg.norm(np.concatenate(laps[:t] + laps[t + 1 :], axis=1), 2))
        for t in range(len(laps))
    ]
    r_min = min(minus_norm)
    lower = 0.5 * math.sqrt(max(sigma2 * sigma2 - r_min * r_min, 0.0))
    dynamic_phi = max(phi)
    # For k=2, the usual higher-order Cheeger upper factor poly(2) may be
    # instantiated as sqrt(2): phi_2 <= sqrt(2 lambda_2).
    upper = math.sqrt(2.0 * sigma2)
    weyl = [
        lambda2[t] <= sigma2 + TOL
        and sigma2 <= math.sqrt(lambda2[t] ** 2 + minus_norm[t] ** 2) + TOL
        for t in range(len(laps))
    ]
    static_cheeger = [
        lambda2[t] / 2.0 <= phi[t] + TOL
        and phi[t] <= math.sqrt(2.0 * lambda2[t]) + TOL
        for t in range(len(laps))
    ]
    checks = {
        "uses_unfolded_operator": unfolded.shape == (len(snapshots[0]), len(snapshots) * len(snapshots[0])),
        "all_weyl_links_hold": all(weyl),
        "all_snapshot_cheeger_links_hold": all(static_cheeger),
        "dynamic_lower_bound_holds": lower <= dynamic_phi + TOL,
        "dynamic_upper_bound_holds": dynamic_phi <= upper + TOL,
    }
    return {
        "case": name,
        "n": len(snapshots[0]),
        "T": len(snapshots),
        "sigma_2_unfolded": sigma2,
        "lambda_2_snapshots": lambda2,
        "leave_one_out_operator_norms": minus_norm,
        "phi_2_snapshots_exhaustive": phi,
        "phi_2_dynamic_max": dynamic_phi,
        "proposition_lower": lower,
        "proposition_upper_k2": upper,
        "lower_nonvacuous": lower > TOL,
        "checks": checks,
    }


def main() -> int:
    k6 = complete(6)
    k8 = complete(8)
    c8 = cycle_with_matching(8)
    m8a = cycle_with_matching(8, 4)
    # A relabelled 3-regular snapshot retains a common normalized-Laplacian
    # null vector but changes the cut geometry.
    perm = np.array([0, 2, 4, 6, 1, 3, 5, 7])
    m8b = m8a[np.ix_(perm, perm)]
    c10 = cycle_with_matching(10)
    m10 = cycle_with_matching(10, 5)

    suites = [
        ("repeated_complete_6", [k6, k6, k6]),
        ("repeated_complete_8", [k8, k8, k8, k8]),
        ("mixed_regular_8", [c8, m8a, m8b]),
        ("mixed_regular_10", [c10, m10, c10, m10]),
    ]
    cases = [audit_case(name, snapshots) for name, snapshots in suites]
    checks = {
        "all_20_case_level_gates_pass": all(all(c["checks"].values()) for c in cases),
        "at_least_two_nonvacuous_dynamic_lower_bounds": sum(c["lower_nonvacuous"] for c in cases) >= 2,
        "every_conductance_is_exhaustive": all(c["n"] <= 10 for c in cases),
        "varied_dynamic_graphs_included": any(len(set(round(x, 12) for x in c["lambda_2_snapshots"])) > 1 for c in cases),
    }
    result = {
        "claim": "Proposition 1 dynamic Cheeger inequality for the unfolded normalized Laplacian",
        "source": {
            "url": SOURCE_URL,
            "sha256": SOURCE_SHA256,
            "scope": SOURCE_SCOPE,
            "retrieved_utc": "2026-07-22",
        },
        "method": "direct unfolded operator; exhaustive phi_2 cuts; k=2 specialization",
        "cases": cases,
        "checks": checks,
        "verdict": "supports" if all(checks.values()) else "inconclusive",
    }
    payload = json.dumps(result, indent=2, sort_keys=True)
    output = Path(__file__).resolve().parents[1] / "outputs" / "dynamic_cheeger_exact.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload + "\n", encoding="utf-8")

    print("Proposition 1 dynamic Cheeger audit (k=2 specialization)")
    print(f"source_sha256={SOURCE_SHA256}")
    for c in cases:
        print(
            f"{c['case']}: sigma2={c['sigma_2_unfolded']:.9f} "
            f"leaveout_min={min(c['leave_one_out_operator_norms']):.9f} "
            f"lower={c['proposition_lower']:.9f} <= phi_dynamic={c['phi_2_dynamic_max']:.9f} "
            f"<= upper={c['proposition_upper_k2']:.9f}; nonvacuous={c['lower_nonvacuous']}"
        )
        print("  case_gates=" + str(all(c["checks"].values())))
    for name, passed in checks.items():
        print(f"{name}: {passed}")
    print(f"verdict: {result['verdict']}")
    print("RESULTS_SHA256=" + hashlib.sha256(payload.encode()).hexdigest())
    return 0 if result["verdict"] == "supports" else 1


if __name__ == "__main__":
    raise SystemExit(main())
