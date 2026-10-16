---
name: research-agile-testing
description: Select and run the minimum risk-driven tests needed to protect scientific semantics, data contracts, recovery, and numerical equivalence.
---

# Research Agile Testing

Test the defects most likely to change a research conclusion, not nominal coverage. Consult `references/test-selection-matrix.md` when the appropriate oracle or test type is unclear.

## Test selection

Identify the material failure modes and choose the strongest practical oracle: analytic value, independent implementation, invariant, metamorphic relation, or audited case. Cover those risks with focused tests and the relevant boundary or smoke path. Reuse valid checks whose inputs and contracts have not changed; no fixed test count or coverage quota is required.

Use fixed seeds to check determinism and independent repeats for the TODO-defined scientific uncertainty. Exercise interruption, duplicate execution, corruption, or partial output when runner changes expose those risks. Compare optimized paths with the retained reference at scientifically justified tolerances. For changed aggregates or figures, run their contract checks and provided validators; statistical validity additionally uses `$research-statistical-analysis`.

Preserve reproduced defects as regressions. Once affected checks and required validators pass, continue the stage unless a new failure or unresolved risk justifies broader testing.

## Guardrails

- A zero exit code, non-empty file, or non-NaN value is not a correctness oracle.
- Never loosen tolerances or remove failing cases to obtain a pass.
- Pilot and Confirmation are scientific stages, not test suites.
- Accept a performance change only with end-to-end benefit and equivalence evidence.

## Output

Record commands, oracles, and outcomes; summarize whether the evidence covers the material risks and what remains unresolved.
