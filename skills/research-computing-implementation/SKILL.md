---
name: research-computing-implementation
description: Implement or optimize scientific code under the MATLAB-first computation policy and separate SciencePlots Python-script boundary.
---

# Research Computing Implementation

Apply **Make it work, make it right, make it fast** in that order. Read `references/python-matlab-guide.md` for language-specific or acceleration choices and `references/io-throughput.md` when storage or file count is material.

Put maintainable method/framework code in optional `code/`, task-local experiment code in `exp/`, and experimental data and artifacts in `data/`. `code/` follows the repository documentation and code-smell rules; `exp/` has no prescribed architecture.

## Language boundary

- Use MATLAB for non-plotting work. A Python component requires a Python-only capability or measured constraint.
- Render governed figures from a separate Matplotlib/SciencePlots script that consumes complete produced quantities.
- For hybrid work, test an explicit interchange schema; prefer Parquet for tables and MAT v7.3/HDF5 for large arrays.

## Work

1. Extract invariants, precision, shapes, task units, environment constraints, and the `code/` versus `exp/` boundary.
2. Build one realistic end-to-end slice with stable interfaces, bulk output, and recovery boundaries.
3. Validate environment, schema, stable IDs, and publication; label placeholder kernels as scaffolding.

## Right

1. Implement the TODO's formulas, controls, units, randomness, metrics, and failure rules.
2. Retain an audited small reference using the strongest available oracle.
3. Run risk-matched tests and one representative combination/repeat end to end.

## Fast

1. Profile representative medium-scale data where fixed costs do not dominate; record those costs.
2. Check a larger scale when scaling can change the chosen optimization.
3. Follow the optimization ladder in `references/python-matlab-guide.md` for the measured bottleneck.
4. Retain a change only after end-to-end improvement and equivalence testing.

Use the buffered-output assets only when their structure fits the task.

## Output

Return the language decision, dependencies, changed files, correctness and equivalence evidence, profiles, retained optimizations, storage choices, and remaining risks.
