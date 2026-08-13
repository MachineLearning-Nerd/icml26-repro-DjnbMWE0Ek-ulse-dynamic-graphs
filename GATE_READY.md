# Publication gate

This repository is ready to publish as an **honest finite-proxy audit**. It is
not marked as a full reproduction of the ULSE paper.

## Decision

- Overall: `INCONCLUSIVE`
- Finite proxy diagnostics: 5/5
- Paper claims independently verified: 0/5
- Full paper reproduction: `false`
- Gate: `PASS` for the stated scope

Run `uv run python -m repro.src.verify_all` followed by
`uv run python -m repro.src.finalize_gate` to refresh the raw measurements and
the canonical gate. A passing gate means the finite evidence record and its
limitations are internally consistent; it does not mean the theorems have
been proved or fully reproduced.
