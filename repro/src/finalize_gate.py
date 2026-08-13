"""Convert the raw ULSE run into a conservative paper-level audit gate."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "repro" / "outputs" / "verify_all_results.json"
VERDICT_PATH = ROOT / "repro" / "outputs" / "verdict.json"
GATE_PATH = ROOT / "repro" / "outputs" / "gate.json"
PUBLICATION_GATE_PATH = ROOT / "publication_gate.json"


CLAIMS = {
    "c1": {
        "raw_key": "claim1_theorem1",
        "paper_statement": "Theorem 1 gives ULSE-n1 cross-sectional and longitudinal stability under the stated asymptotic model conditions.",
        "status": "FINITE_DSBM_STABILITY_PROXY",
        "limitations": [
            "The run uses finite DSBM instances, fixed K/T, rho=1, five seeds, and a finite n sweep.",
            "Numerical decay does not establish the almost-sure theorem or its full inhomogeneous random-graph scope.",
        ],
    },
    "c2": {
        "raw_key": "claim2_theorem2",
        "paper_statement": "Theorem 2 gives an O(1/(rho^1/2 n^1/2)) two-to-infinity convergence bound for ULSE-n1.",
        "status": "FINITE_RATE_PROXY",
        "limitations": [
            "The rate fit tests selected finite DSBM samples and a bounded diagnostic constant.",
            "A finite slope and parameter sweep do not prove an asymptotic almost-sure upper bound.",
        ],
    },
    "c3": {
        "raw_key": "claim3_theorem3",
        "paper_statement": "Theorem 3 gives exact noise-free cross-sectional and longitudinal ULSE-n1 stability.",
        "status": "FINITE_POPULATION_IDENTITY_PROXY",
        "limitations": [
            "The check evaluates selected finite probability matrices in IEEE floating point.",
            "Machine-precision agreement in those constructions is not a proof for every admissible population model.",
        ],
    },
    "c4": {
        "raw_key": "claim4_theorem4",
        "paper_statement": "Theorem 4 gives ULSE-n2 stability and supports a degree-uniformity relaxation.",
        "status": "FINITE_DEGREE_RELAXATION_PROXY",
        "limitations": [
            "The run uses finite DSBM samples and a selected degree-varying construction.",
            "It does not establish the theorem, its full assumptions, or a general degree-relaxation result.",
        ],
    },
    "c5": {
        "raw_key": "claim5_proposition1",
        "paper_statement": "Proposition 1 gives dynamic Cheeger bounds for the unfolded normalized Laplacian.",
        "status": "FINITE_CHEEGER_PROXY",
        "limitations": [
            "The exhaustive conductance calculation covers 28 finite graphs with n<=20 and T<=6.",
            "Finite inequality checks do not replace the proposition's general proof or all graph sizes.",
        ],
    },
}


with RAW_PATH.open(encoding="utf-8") as handle:
    raw = json.load(handle)

claims = {}
for claim_id, spec in CLAIMS.items():
    evidence = raw.get(spec["raw_key"], {})
    finite_passed = evidence.get("verdict") == "FINITE_PROXY_PASS"
    claims[claim_id] = {
        "paper_statement": spec["paper_statement"],
        "finite_proxy_passed": finite_passed,
        "paper_claim_verified": False,
        "status": spec["status"] if finite_passed else "FINITE_PROXY_FAIL",
        "raw_verdict": evidence.get("verdict", "MISSING"),
        "evidence_source": f"repro/outputs/verify_all_results.json#{spec['raw_key']}",
        "limitations": spec["limitations"],
    }

finite_passed = sum(claim["finite_proxy_passed"] for claim in claims.values())
if finite_passed != len(CLAIMS):
    raise SystemExit(
        f"Finite diagnostic gate failed: {finite_passed}/{len(CLAIMS)} proxies passed"
    )

verdict = {
    "paper": "DjnbMWE0Ek",
    "title": "Unfolded Laplacian Spectral Embedding: A Theoretically Grounded Approach to Dynamic Network Representation",
    "authors": ["Haruka Ezoe", "Hiroki Matsumoto", "Ryohei Hisano"],
    "arxiv": "2508.12674",
    "arxiv_version_pinned": "v2 (last revised 2026-02-23)",
    "openreview": "DjnbMWE0Ek",
    "scope": "Independent finite DSBM, population-identity, degree-relaxation, and dynamic-Cheeger diagnostics; no proof verification or full empirical reproduction.",
    "claims": claims,
    "overall_status": "INCONCLUSIVE",
    "finite_proxy_diagnostics_passed": finite_passed,
    "finite_proxy_diagnostics_total": len(CLAIMS),
    "paper_claims_verified": 0,
    "paper_claims_total": len(CLAIMS),
    "full_paper_reproduction": False,
    "raw_run_source": raw.get("source"),
    "not_reproduced": [
        "theorem proofs and almost-sure asymptotics",
        "the full inhomogeneous random-graph parameter space",
        "the general ULSE-n1/n2 assumptions and constants",
        "real-world dynamic-network experiments",
        "paper-scale baselines, figures, and ablations",
    ],
}

gate = {
    "paper": verdict["paper"],
    "arxiv": verdict["arxiv"],
    "arxiv_version_pinned": verdict["arxiv_version_pinned"],
    "overall_status": verdict["overall_status"],
    "finite_proxy_diagnostics_passed": finite_passed,
    "finite_proxy_diagnostics_total": len(CLAIMS),
    "paper_claims_verified": 0,
    "paper_claims_total": len(CLAIMS),
    "full_paper_reproduction": False,
    "publication_gate_passed": True,
    "meaning": "The finite audit is internally consistent; paper-level claims remain unverified.",
    "claim_statuses": {name: claim["status"] for name, claim in claims.items()},
}

publication_gate = {
    "paper": verdict["paper"],
    "arxiv": verdict["arxiv"],
    "arxiv_version_pinned": verdict["arxiv_version_pinned"],
    "tests_passed": True,
    "publication_gate_passed": True,
    "overall_status": verdict["overall_status"],
    "finite_proxy_diagnostics_passed": finite_passed,
    "finite_proxy_diagnostics_total": len(CLAIMS),
    "claims_verified": 0,
    "claims_total": len(CLAIMS),
    "full_paper_reproduction": False,
}

for path, payload in (
    (VERDICT_PATH, verdict),
    (GATE_PATH, gate),
    (PUBLICATION_GATE_PATH, publication_gate),
):
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

print(
    f"Publication gate: PASS; finite proxies {finite_passed}/{len(CLAIMS)}; "
    "paper claims 0/5; overall INCONCLUSIVE"
)
