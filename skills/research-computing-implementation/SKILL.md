---
name: research-computing-implementation
description: Design, implement, or optimize scientific computing code in Python or MATLAB while preserving the TODO's numerical semantics. Use for vectorization, matrix operations, large data, neural networks, parallel/GPU execution, and storage. Do not choose a different scientific method.
---

# Research Computing Implementation

## Overview

Use this Skill whenever scientific code is created or materially optimized. Select Python, MATLAB, or an explicit hybrid boundary based on the computational workload and the existing codebase, not personal preference.

Read:

- `references/python-matlab-guide.md` for package and function guidance;
- `references/io-throughput.md` for bulk I/O rules and anti-patterns;
- `assets/python_buffered_results_template.py` and `assets/matlab_buffered_results_template.m` when a starting implementation is useful.

## Choose the implementation language

Prefer MATLAB when:

- dense matrix algebra and vectorized numerical operations dominate;
- the validated codebase or required toolbox is already MATLAB;
- direct use of MATLAB signal processing, statistics, optimization, or parallel/GPU functions reduces semantic translation risk.

Prefer Python when:

- large multi-file or heterogeneous data processing dominates;
- deep learning or neural-network training is central;
- the workflow benefits from NumPy/SciPy/pandas/PyArrow/PyTorch and Python orchestration tools;
- reproducible notebooks or integration with a broader Python analysis stack is required.

Use a hybrid only when the interface is explicit and the serialization cost is justified. Prefer Parquet for tabular interchange and MAT v7.3/HDF5-compatible storage for large multidimensional arrays.

## Implementation workflow

1. Extract numerical invariants, precision requirements, array shapes, and independent task units from the TODO.
2. Inspect the existing language, packages/toolboxes, data formats, and deployment environment.
3. Build a correctness-first reference on a tiny representative case.
4. Choose vectorization and batching that preserve the reference behavior.
5. Preallocate or batch data structures rather than growing them in hot loops.
6. Design bulk storage before parallel scaling.
7. Add parallelism only after measuring one task's runtime, memory, and I/O.
8. Avoid CPU oversubscription from nested worker pools and multithreaded BLAS.
9. Add GPU execution only for supported operations and verify CPU/GPU equivalence within justified tolerances.
10. Profile the actual bottleneck before broad optimization.
11. Use `$research-agile-testing` to validate equivalence, shapes, dtypes, determinism, and storage/recovery invariants.
12. Record the language rationale, package/toolbox requirements, and representative performance measurements in the chat handoff and technical manifests.

## Python rules

- Prefer NumPy broadcasting, ufuncs, matrix operations, and SciPy routines over Python element loops when memory use remains controlled.
- Use pandas for moderate tabular transformations; use PyArrow/Parquet datasets, chunked readers, HDF5, or Zarr for large or partitioned data.
- Use PyTorch for neural networks and GPU training when the TODO requires them; isolate data loading, model definition, training, evaluation, and checkpointing.
- Use `pytest`, `numpy.testing`, `pandas.testing`, and `torch.testing` as appropriate.
- Do not repeatedly call `pd.concat` on a growing DataFrame or call `to_csv` once per result row.

## MATLAB rules

- Prefer vectorized array and matrix operations and preallocate arrays, tables, cells, and structures.
- Use numerically appropriate solvers such as `A\b` rather than explicitly forming `inv(A)` when solving systems.
- Use `parfor` only for independent iterations with measured benefit; control data transfer and worker count.
- Use `gpuArray` only for supported operations with justified transfer cost and equivalence checks.
- Use `matfile`, MAT v7.3, `datastore`, `tall`, or Parquet functions for large data as appropriate.
- Use `matlab.unittest` for automated tests.
- Do not grow tables in a loop or call `writetable` for each result row.

## I/O rules

- Logs may be line-oriented; scientific result tables may not be written row by row.
- Prefer one immutable file per independent task or worker, then merge once, or write buffered chunks to a partitioned dataset.
- Use temporary files and atomic rename/move for completed chunks.
- Separate checkpoint metadata from bulk numerical arrays.
- Validate schema, row count, stable IDs, and file integrity after publishing a chunk.
- If preflight shows I/O dominates runtime, change format, batch size, partitioning, or task granularity before increasing compute parallelism.

## Output contract

Return:

- selected language and rationale;
- package/toolbox and version requirements;
- implementation and storage architecture;
- files created or changed;
- vectorization, parallel, GPU, and I/O decisions;
- tests and numerical equivalence checks;
- representative runtime, memory, GPU memory, and I/O measurements;
- remaining performance or compatibility risks.
