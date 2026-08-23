---
name: research-agile-testing
description: Select and run the minimum risk-driven tests needed to protect scientific semantics, data contracts, recovery, and numerical equivalence.
---

# Research Agile Testing

Test the defects most likely to change a research conclusion, not nominal coverage. Consult `references/test-selection-matrix.md` when the appropriate oracle or test type is unclear.

## Workflow

1. Identify one to three material failure modes and the invariants they threaten.
2. Choose the strongest practical oracle: analytic value, independent reference, invariant, metamorphic relation, or audited tiny case.
3. Preserve a minimal failing case or baseline; add the smallest focused tests before boundary integration and one real smoke path.
4. Use fixed seeds for implementation determinism and independent repeats for scientific uncertainty.
5. Test interruption, duplicate launch, corruption, and partial output only when recovery or parallel behavior changes.
6. Compare every optimized path with the retained reference at scientifically justified tolerances.
7. For changed aggregates or figures, run their contract checks and provided validators.
8. Run affected tests, convert reproduced defects into regressions, and report remaining risk.

## Guardrails

- A zero exit code, non-empty file, or non-NaN value is not a correctness oracle.
- Never loosen tolerances or remove failing cases to obtain a pass.
- Pilot and Confirmation are scientific stages, not test suites.
- Accept a performance change only with end-to-end benefit and equivalence evidence.

## Output

Return risks, oracles, tests, commands and results, uncovered risks, and evidence sufficiency.
