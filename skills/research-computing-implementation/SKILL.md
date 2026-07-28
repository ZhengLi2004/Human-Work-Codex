---
name: research-computing-implementation
description: Design, implement, or optimize scientific computing code under the repository's MATLAB-first non-plotting policy and Python plotting boundary while preserving the TODO's numerical semantics. Use for scaffolding, correctness references, profiling, redundant-work removal, vectorization, JIT-friendly MATLAB, MEX/code generation, parallel/GPU execution, neural networks, and storage. Do not choose a different scientific method.
---

# Research Computing Implementation

## Overview

Use this Skill whenever scientific code is created or materially optimized. Apply the repository's language rule and the phase order **“Make it work, make it right, make it fast.”** Do not use a speed assumption as benchmark evidence.

Read `references/python-matlab-guide.md` when choosing a language or package boundary, crossing Python/MATLAB, or generating a chart. Read `references/io-throughput.md` when result storage, file count, serialization, resume behavior, or I/O cost is material. Use `assets/python_buffered_results_template.py` or `assets/matlab_buffered_results_template.m` only when matching buffered-output boilerplate is useful.

## Apply the language boundary

Use MATLAB by default for every non-plotting computation, including numerical kernels, preprocessing, experiment orchestration, aggregation, and storage code.

Use Python for a non-plotting component only when:

- the TODO requires a Python-only package or interface, such as a PyTorch model that cannot be substituted without changing the method; or
- measured environment, compatibility, or capability evidence shows that MATLAB cannot implement the required component faithfully.

Existing Python convenience, familiarity, or a shorter implementation is not an exception. Record the exact exception, its affected component, and why it is required. Keep the rest of the non-plotting pipeline in MATLAB when the boundary remains coherent.

Use Python, Jupyter, Matplotlib, and SciencePlots for governed plotting. Follow the visualization artifact boundary in the reference even when MATLAB produces the numerical source.

Use a hybrid only when the interface is explicit and the serialization cost is justified. Prefer Parquet for tabular interchange and MAT v7.3/HDF5-compatible storage for large multidimensional arrays.

## Required phase order

### 1. Make it work

1. Extract numerical invariants, precision requirements, array shapes, and independent task units from the TODO.
2. Inspect the installed MATLAB release, licenses/toolboxes, compiler and GPU availability, data formats, existing code, and deployment constraints. Check Python only for plotting and documented exceptions.
3. Build a minimal end-to-end scaffold in the current environment with realistic interfaces, array shapes, one representative task unit, bulk output, logs, and recovery boundaries.
4. Design allocation, batching, storage, and worker isolation into the scaffold. A placeholder kernel must be labeled as scaffolding and cannot satisfy scientific-correctness predicates.
5. Run the scaffold and validate its environment, schema, stable identifiers, and artifact publication.

### 2. Make it right

1. Implement a clear correctness reference on an audited small case before optimizing the production path.
2. Replace scaffold placeholders with the TODO's exact formulas, controls, units, random process, metrics, and failure rules.
3. Self-check against the strongest available oracle: analytic result, independent implementation, property or metamorphic relation, or manually audited tiny case.
4. Use `$research-agile-testing` for shapes, types, indexing, determinism, storage/recovery, and scientific invariants.
5. Complete one representative combination and independent repeat end to end. Keep this correctness reference even after optimization.

### 3. Make it fast

1. Measure representative wall time, CPU and memory use, GPU use when applicable, data transfer, file count, and I/O before changing performance code.
2. Profile the actual workload and optimize measured bottlenecks in this order: eliminate redundant work and improve algorithmic complexity; improve data layout and allocation; use JIT-friendly functions and types; vectorize or use optimized built-ins; then consider MEX or generated code, parallel workers, GPU execution, and storage/partition changes.
3. Benchmark loops and vectorized forms rather than assuming vectorization wins; account for temporary-array memory.
4. Re-run the correctness reference and TODO-relevant tests after every material optimization. Record before/after measurements and retain a change only when its benefit and maintenance cost are justified.
5. Avoid nested worker pools, BLAS oversubscription, shared mutable result files, and CPU/GPU transfers inside hot loops.

## Python exception rules

- Prefer NumPy broadcasting, ufuncs, matrix operations, and SciPy routines over Python element loops when memory use remains controlled.
- Use pandas for moderate tabular transformations; use PyArrow/Parquet datasets, chunked readers, HDF5, or Zarr for large or partitioned data.
- Use PyTorch only when the TODO or required validated method depends on it; isolate data loading, model definition, training, evaluation, and checkpointing behind the documented boundary.
- Use `pytest`, `numpy.testing`, `pandas.testing`, and `torch.testing` as appropriate.
- Do not repeatedly call `pd.concat` on a growing DataFrame or call `to_csv` once per result row.

## MATLAB rules

- Put reusable numerical code in functions with stable input types and shapes so MATLAB's automatic execution-engine optimizations can operate effectively. Do not describe general MATLAB JIT as a manual switch.
- Remove loop-invariant and repeated computations first. Improve the algorithm before applying lower-level acceleration.
- Preallocate arrays, tables, cells, and structures. Use vectorized array/matrix operations when measured runtime and memory improve; modern MATLAB loops may already perform well.
- Use numerically appropriate solvers such as `A\b` rather than explicitly forming `inv(A)` when solving systems.
- Prefer optimized MATLAB and toolbox functions before custom compiled code.
- Consider a hand-written C/C++ MEX function or MATLAB Coder-generated MEX only for a stable, profiled hot kernel. Record compiler/toolbox requirements, source and build command, platform compatibility, MATLAB fallback, benchmark, and equivalence test. MATLAB Coder's `codegen -jit` is JIT MEX generation, not a switch for MATLAB's general JIT.
- Use `parfor`, `parfeval`, or batch execution only for independent work with measured benefit; control worker count, serialization, data transfer, and per-worker memory.
- Use `gpuArray` only for supported, sufficiently large operations with justified transfer cost, `gputimeit` measurements, and CPU/GPU equivalence checks.
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
- work/right/fast gate evidence, including the retained correctness reference and before/after profile;
- MATLAB techniques considered, accepted, or rejected with measured reasons;
- remaining performance or compatibility risks.
