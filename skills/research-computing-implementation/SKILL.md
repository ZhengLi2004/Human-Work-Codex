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

Establish a realistic runnable path through the environment, interfaces, scientific units, and bulk storage. Validate its schema, stable IDs, and publication/recovery boundaries. Clearly identify any placeholder kernel so scaffold success is not mistaken for scientific correctness.

## Right

Implement the approved scientific specification and retain an independent oracle or audited small case. Choose focused checks for the formulas, controls, units, randomness, and failure behavior that could alter the conclusion, plus a representative end-to-end path. Use `$research-statistical-analysis` for statistical estimators and uncertainty.

## Fast

Profile representative medium-scale work and quantify fixed costs. Choose optimizations for the measured bottleneck using `references/python-matlab-guide.md`; its options are not a mandatory ladder. Check a larger scale when batch behavior can change the conclusion. Retain changes supported by end-to-end improvement and numerical/scientific equivalence.

Use the buffered-output assets only when their structure fits the task.

## Output

Record implementation, environment, storage, correctness, and performance evidence in the task artifacts. Summarize the changes, validation, material limitations, and any decision needed.
