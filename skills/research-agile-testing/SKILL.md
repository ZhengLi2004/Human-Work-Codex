---
name: research-agile-testing
description: Design and run the minimum risk-driven tests needed to protect scientific semantics in Python or MATLAB code, data pipelines, controls, metrics, randomness, storage, and recovery. Do not treat experimental outcomes as implementation tests.
---

# Research Agile Testing

## Overview

Find the defects most likely to produce an incorrect research conclusion with the fastest discriminating tests. Optimize for scientific risk reduction rather than test count or nominal coverage.

Read `references/test-selection-matrix.md` for risk-to-test mapping.

## Workflow

1. Identify one to three highest-risk failure modes in the current change.
2. Extract the scientific invariants that must hold.
3. Select the strongest available oracle: analytic result, independent reference, invariant, metamorphic relation, or manually audited tiny case.
4. Preserve a minimal failing example or baseline before the fix.
5. Implement fast unit or contract tests first, then add only the integration tests needed at risky boundaries.
6. Keep a small real end-to-end smoke test for the full chain.
7. For random code, use fixed seeds to test implementation determinism; estimate research uncertainty with independent repeats, not repeated unit tests.
8. For parallel and resume logic, inject interruption, duplicate launch, corruption, and partial-output cases.
9. For optimized Python/MATLAB code, compare against the correctness reference within scientifically justified tolerances.
10. Run the affected tests and report commands, environment, results, and uncovered risk.
11. Convert reproducible real defects into regression tests.
12. For figures, verify that governed outputs come from the executed notebook, temporary `.py` previews remain under the platform temporary directory, and every chart records a SciencePlots stack based on `science`. Reconcile stable keys and planned conditions against the coverage manifest, then inspect every final title, axis, scale, unit, legend, curve, mark, and schematic label.

## Language-specific tools

### Python

Use as appropriate:

- `pytest` and parametrization;
- `numpy.testing` for arrays and tolerances;
- `pandas.testing` for tables and indexes;
- `scipy` reference computations;
- `torch.testing` and small deterministic model/data cases;
- temporary directories for atomic-write and resume tests.

### MATLAB

Use as appropriate:

- `matlab.unittest.TestCase`;
- `verifyEqual`, `verifyThat`, and explicit tolerances;
- function-based tests for small numerical units;
- temporary folders for MAT/Parquet/checkpoint tests;
- serial-versus-`parfor` and CPU-versus-`gpuArray` equivalence checks.

## I/O test requirements

When result storage changes, test:

- buffered/chunked write behavior rather than per-row mutation;
- atomic publication and recovery from an interrupted temporary file;
- no duplicate counting after resume;
- schema and stable identifiers across partitions;
- final row-count reconciliation;
- a benchmark or operation-count check when excessive file I/O is the reported risk.

## Guardrails

- A zero exit code, non-empty file, or non-NaN value is not a sufficient correctness oracle.
- Do not loosen tolerances merely to pass.
- Do not delete failing cases to reduce burden.
- Do not run an entire Pilot or Confirmation as a routine test suite.
- Do not test unrelated modules to create the appearance of thoroughness.

## Output contract

Return the risk list, selected tests and oracles, files changed, commands and results, skipped or unrun tests, uncovered risks, and whether the evidence is sufficient for the current implementation slice.
