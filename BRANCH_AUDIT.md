# Branch and attribution audit

## Historical state

- Repository: `icml26-repro-DjnbMWE0Ek-ulse-dynamic-graphs`
- Initial publication branch: `main`
- Experiment branch: `orx/ulse-full-scale-theorem-verification`
- The experiment branch contained the full-scale run history; its relevant
  code and outputs were incorporated into `main`.
- Historical commits used Dinesh Jinjala's work email and are normalized below.

## Publication state

- Canonical repository: `icml26-ulse-dynamic-graphs`
- Canonical branch: `main`
- Legacy experiment branch: removed after `main` became the complete
  publication surface
- Default branch: `main`
- Expected remote branch set: `main` only

All reachable published commits must use:

```text
MachineLearning-Nerd
37579156+MachineLearning-Nerd@users.noreply.github.com
```

No Claude co-author trailer or `orx/*` branch is part of the canonical state.
Branch cleanup is administrative hygiene and does not increase scientific
evidence.

## Live verification

The final publication check must confirm:

1. GitHub metadata uses `icml26-ulse-dynamic-graphs` and `main` as default.
2. The only remote branch is `main`.
3. `main` contains the README, status, gate, branch audit, raw results,
   conservative verdict, and publication gate.
4. Reachable commit author and committer fields use the MachineLearning-Nerd
   no-reply identity.
5. The remote homepage points to `https://arxiv.org/abs/2508.12674`.

GitHub metadata, branch state, and commit attribution are administrative
checks; they are not paper-claim evidence.
