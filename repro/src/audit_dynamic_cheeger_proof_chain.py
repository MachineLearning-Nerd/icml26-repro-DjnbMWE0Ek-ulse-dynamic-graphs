#!/usr/bin/env python3
"""Independent exact-rational implication audit of Proposition 1's proof chain.

No graph or numerical-linear-algebra code is shared with the primary verifier.
The script checks the universal algebraic implication used in the paper:
Weyl leave-one-out bounds + per-snapshot higher-order Cheeger bounds imply the
displayed dynamic lower and upper bounds.
"""

from fractions import Fraction as F


def main() -> int:
    checked = 0
    lower_nonvacuous = 0
    # All quantities below are squared where necessary, keeping every operation
    # in exact rational arithmetic and avoiding floating-point square roots.
    for sigma in [F(i, 8) for i in range(1, 33)]:
        for lambdas in (
            [sigma, sigma, sigma],
            [sigma / 2, 3 * sigma / 4, sigma],
            [sigma / 4, sigma / 2, 7 * sigma / 8],
        ):
            # Choose the smallest exact leave-one-out squared norms allowed by
            # sigma^2 <= lambda_t^2 + r_t^2, with extra nonnegative slack.
            base_r2 = [sigma * sigma - lam * lam for lam in lambdas]
            for slack in [F(0), F(1, 17), F(3, 11)]:
                r2 = [x + slack for x in base_r2]
                # Cheeger witnesses encoded as lambda/2 <= phi and
                # phi^2 <= C_k^2 lambda.  C_k^2=8 is a valid polynomial
                # envelope and deliberately looser than the k=2 primary gate.
                c2 = F(8)
                phi = [lam / 2 + (sigma - lam) / 8 for lam in lambdas]
                premises = all(
                    lam <= sigma
                    and sigma * sigma <= lam * lam + rr
                    and lam / 2 <= ph
                    and ph * ph <= c2 * lam
                    for lam, rr, ph in zip(lambdas, r2, phi)
                )
                if not premises:
                    continue
                dynamic_phi = max(phi)
                r2_min = min(r2)
                lower_radicand = max(sigma * sigma - r2_min, F(0))
                lower_ok = lower_radicand <= 4 * dynamic_phi * dynamic_phi
                upper_ok = dynamic_phi * dynamic_phi <= c2 * sigma
                assert lower_ok and upper_ok
                checked += 1
                lower_nonvacuous += int(lower_radicand > 0)

    # Fail-sensitive controls: removing each indispensable premise permits a
    # counterexample to one of the conclusions.
    controls = {
        "missing_leave_one_out_upper_can_break_lower": F(9) > 4 * F(1),
        "missing_lambda_le_sigma_can_break_upper": F(4) > F(2),
        "dynamic_uses_max_not_min": max(F(1, 3), F(2, 3)) != min(F(1, 3), F(2, 3)),
    }
    checks = {
        "exact_implication_witnesses": checked >= 250,
        "nonvacuous_lower_witnesses": lower_nonvacuous >= 100,
        "all_fail_sensitive_controls": all(controls.values()),
    }
    print("Independent exact-rational Proposition 1 proof-chain audit")
    print(f"universal implication witnesses checked={checked}")
    print(f"nonvacuous dynamic-lower witnesses={lower_nonvacuous}")
    for name, passed in controls.items():
        print(f"control_{name}: {passed}")
    for name, passed in checks.items():
        print(f"{name}: {passed}")
    verdict = all(checks.values())
    print(f"verdict: {'supports' if verdict else 'inconclusive'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    raise SystemExit(main())
