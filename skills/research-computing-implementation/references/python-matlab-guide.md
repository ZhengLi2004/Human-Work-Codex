# Python and MATLAB Scientific-Computing Guide

Use this reference after the TODO has fixed the scientific meaning. Language and package choices are engineering decisions unless the TODO explicitly fixes them.

## Contents

- [Selection matrix](#selection-matrix)
- [Python implementation guidance](#python-implementation-guidance)
- [MATLAB implementation guidance](#matlab-implementation-guidance)
- [MATLAB optimization ladder](#matlab-optimization-ladder)
- [Visualization artifact boundary](#visualization-artifact-boundary)
- [Cross-language boundary](#cross-language-boundary)
- [Authoritative MATLAB references](#authoritative-matlab-references)

## Selection matrix

This repository deliberately defaults to MATLAB for non-plotting computation. That policy is not a universal performance claim; representative benchmarks still decide whether an optimization is effective.

| Requirement | Repository decision | Required record |
|---|---|---|
| Numerical kernels, preprocessing, orchestration, aggregation, or storage | MATLAB | Release, toolboxes, environment, and work/right/fast evidence |
| TODO-required Python-only package or interface, such as a required PyTorch implementation | Python for the smallest coherent component | Exact dependency, why substitution would change or prevent the method, and boundary tests |
| MATLAB cannot implement the required component faithfully in the current environment | Python exception | Measured capability or compatibility evidence and human-visible rationale |
| Governed plotting | Python/Jupyter, Matplotlib, and SciencePlots | Executed notebook and exact style stack |
| Cross-language tabular interchange | Parquet with an explicit schema | Round-trip schema and key test |
| Cross-language large numeric arrays | MAT v7.3 or HDF5 | Dataset names, shape, dtype, axis order, and round-trip test |

Existing Python code, convenience, familiarity, or syntax length does not by itself satisfy the exception. Avoid a hybrid when conversion, duplicated dependencies, or debugging cost is larger than the isolated benefit.

## Python implementation guidance

Apply this section only to governed plotting or a documented non-plotting exception.

### Array and numerical work

- Use NumPy broadcasting, slicing, reductions, `einsum`, `matmul`, or SciPy routines instead of Python loops over dense numeric dimensions when this preserves semantics.
- Use `numpy.linalg` or `scipy.linalg` solvers rather than forming an inverse explicitly.
- Keep dtype and device transitions explicit. Do not silently downcast scientific arrays.
- Avoid unnecessary copies: inspect contiguity, views, broadcasting, and temporary allocation for large arrays.
- For sparse problems, use `scipy.sparse` and matching sparse solvers; do not densify by accident.
- For repeated transforms, precompute invariant terms only after proving that they are independent of the task/repeat.

### Tabular and large-data work

- Use pandas for schema-aware manipulation and PyArrow/Parquet for large, typed, columnar storage.
- Build a list of records or column arrays and construct a DataFrame once per chunk. Never grow a DataFrame row by row.
- Perform `pd.concat` once per bounded batch or at final merge, never on an ever-growing accumulator in the inner result loop.
- Use projected columns, predicate filters, and partition-aware scans when only a subset is needed.
- Use `read_csv(..., chunksize=...)` only for unavoidable large CSV inputs. Convert reusable large tables to Parquet after validation.
- Keep logs and checkpoint metadata separate from scientific result tables.

### Parallel and GPU work

- Use `concurrent.futures`, `multiprocessing`, joblib, or the project scheduler only after measuring one task.
- Avoid nested process pools and BLAS/OpenMP oversubscription. Record thread settings such as `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, and PyTorch worker counts when relevant.
- Use PyTorch `Dataset`/`DataLoader` for large training inputs. Tune batch size and worker count from measured throughput, CPU memory, and GPU memory.
- Use automatic mixed precision only when the TODO permits it and equivalence/tolerance tests show that scientific conclusions are unchanged.
- Treat `torch.compile`, multiprocessing start methods, pinned memory, and persistent workers as measured optimizations rather than unconditional defaults.
- Seed every independent randomness source required by the TODO and record deterministic limitations.

### Testing

Use `pytest` for unit/integration/regression tests and explicit numerical tests such as:

```python
import numpy as np

np.testing.assert_allclose(actual, expected, rtol=1e-7, atol=1e-10)
```

Tolerance must follow the algorithm, dtype, and scientific decision boundary; do not copy a generic tolerance blindly.

## MATLAB implementation guidance

### Functions, execution engine, and algorithm structure

- Put reusable hot code in functions; keep input classes and shapes stable when the algorithm permits.
- MATLAB's execution engine applies optimizations automatically. There is no general manual JIT switch to enable. Measure representative functions after warm-up.
- Remove unnecessary evaluations, repeated parsing/conversion, repeated factorizations, and loop-invariant work before tuning syntax.
- Improve asymptotic complexity, exploit sparsity or structure, and select an appropriate numerical algorithm before adding workers or a GPU.

### Array and matrix work

- Express dense numerical work with matrix multiplication, broadcasting/implicit expansion, logical indexing, reductions, `pagemtimes`, and appropriate toolbox routines.
- Preallocate numeric arrays, cell arrays, structures, and table variables before loops when output size is known.
- Use `A\b`, decomposition objects, or iterative solvers instead of `inv(A)*b`.
- Move invariant work outside loops only after proving the value does not depend on the iteration.
- Avoid repeated conversion among tables, cells, structures, and numeric arrays inside hot loops. Convert once at a clear boundary.
- Use MATLAB Profiler to locate bottlenecks and `timeit`/`gputimeit` for representative kernels. Re-profile the complete workload after local changes because the bottleneck can move.

### Large data and storage

- Use `matfile` for partial access to MAT v7.3 variables when the access pattern is compatible.
- Use `datastore`/`tall` for collections too large for memory when the supported operations match the algorithm.
- Use `parquetread`/`parquetwrite` for typed tabular interchange when available.
- Preallocate table variables or accumulate a bounded structure/table chunk, then write once per chunk.
- Never call `writetable` for each result row or repeatedly rewrite one CSV/XLSX table in a task loop.
- Use one output file per meaningful task/chunk/worker and merge once; avoid millions of tiny files.

### Parallel and GPU work

- Use `parfor` for independent iterations with sliced variables and no order dependence.
- Use `parfeval` when asynchronous scheduling, explicit futures, or heterogeneous task duration matters.
- Keep worker outputs isolated; do not have workers append to one table file.
- Use `gpuArray` and GPU-enabled functions only for sufficiently large operations and measure transfer overhead.
- Validate CPU/GPU numerical equivalence at TODO-appropriate tolerances.
- Do not open a large parallel pool before measuring per-worker memory and BLAS/thread behavior.

### MEX and generated code

- Consider C/C++ MEX only after profiling identifies a stable hot kernel that MATLAB and toolbox functions do not address adequately.
- Keep the MATLAB reference implementation and test MEX output against it at TODO-justified tolerances.
- Record C/C++ source, headers, build command, supported MATLAB releases/platforms, compiler, architecture, external-library versions, and a MATLAB fallback.
- Treat MATLAB Coder as an optional licensed toolchain. `codegen` can generate C/C++ or MEX for supported MATLAB code; `codegen -jit` refers specifically to JIT MEX generation, not general MATLAB execution.
- Include compile/startup cost when it is material, and benchmark the representative end-to-end workload rather than only the fastest inner call.

### Testing

Use `matlab.unittest` and numerical constraints, for example:

```matlab
import matlab.unittest.TestCase
import matlab.unittest.constraints.IsEqualTo
import matlab.unittest.constraints.RelativeTolerance

testCase = TestCase.forInteractiveUse;
testCase.verifyThat(actual, IsEqualTo(expected, ...
    'Within', RelativeTolerance(1e-7)));
```

## MATLAB optimization ladder

Apply each rung only to a measured bottleneck and preserve the prior correctness oracle.

1. **Eliminate work:** cache proven invariants, remove duplicate conversions and reads, fuse repeated passes when semantics permit, and avoid computing unused outputs.
2. **Improve the algorithm:** reduce complexity, exploit matrix/sparse/streaming structure, use stable decompositions or iterative solvers, and improve task granularity.
3. **Improve memory behavior:** preallocate, reuse buffers, avoid accidental copies and oversized temporaries, choose appropriate dtypes, and batch I/O.
4. **Use MATLAB effectively:** functions with stable types/shapes, measured vectorization, optimized built-ins, decomposition objects, and suitable toolbox routines.
5. **Compile a stable kernel:** hand-written MEX or MATLAB Coder-generated MEX when toolchain and portability costs are justified.
6. **Parallelize independent work:** `parfor`, `parfeval`, batch jobs, or distributed arrays after measuring transfer, scheduling, memory, and oversubscription.
7. **Use the GPU:** keep data resident, use supported large operations, minimize transfers, and measure with `gputimeit`.
8. **Re-profile end to end:** record before/after wall time and resources, rerun equivalence tests, and reject changes that lack useful net benefit.

## Visualization artifact boundary

Use Python, Matplotlib, and SciencePlots for chart rendering in this repository, even when MATLAB produces the numerical source data.

- Governed draft and final research figures come from an executed Jupyter notebook so code, configuration, and cell outputs remain reviewable together.
- A standalone `.py` file may inspect metadata or render disposable layout, style, legend, scale, or other diagnostic cues. Create the script and all of its images under the platform temporary directory, not the repository, result root, or figure directory.
- A temporary diagnostic cannot become a draft, final figure, scientific artifact, or predicate reference. Reproduce any retained choice in the executed notebook.
- Import `scienceplots` before applying styles. Every Python chart uses a stack whose base is `science`; use `science` plus `no-latex` unless a tested environment and output requirement justify another recorded stack.
- Treat a missing SciencePlots dependency as a blocker. Do not silently substitute Matplotlib defaults, seaborn defaults, or a MATLAB figure.

## Cross-language boundary

For every exchanged artifact, record:

- schema or dataset names;
- row/key uniqueness rules;
- array shape and axis order;
- dtype and missing-value representation;
- categorical encoding;
- time units and time-zone rules;
- compression and partitioning;
- producing code version and configuration;
- a small round-trip test in both languages when both consume the artifact.

MATLAB is column-major and uses 1-based indexing; NumPy is usually row-major in presentation and uses 0-based indexing. Never translate index arrays, reshape operations, or flattened matrices without an explicit equivalence test.

## Authoritative MATLAB references

- [Techniques to Improve Performance](https://www.mathworks.com/help/matlab/matlab_prog/techniques-for-improving-performance.html): functions, preallocation, and general performance practices.
- [Profile Your Code to Improve Performance](https://www.mathworks.com/help/matlab/matlab_prog/profiling-for-improving-performance.html) and [`timeit`](https://www.mathworks.com/help/matlab/ref/timeit.html): representative profiling and timing.
- [Improve `parfor` Performance](https://www.mathworks.com/help/parallel-computing/improve-parfor-performance.html): transfer, worker, and scheduling costs.
- [`gpuArray`](https://www.mathworks.com/help/parallel-computing/gpuarray.html) and [Measure and Improve GPU Performance](https://www.mathworks.com/help/parallel-computing/measure-and-improve-gpu-performance.html): supported GPU execution, transfer cost, and `gputimeit`.
- [C MEX functions](https://www.mathworks.com/help/matlab/matlab_external/c-mex-functions.html) and [Build C MEX programs](https://www.mathworks.com/help/matlab/matlab_external/build-c-mex-programs.html): native extension interface and compiler/build requirements.
- [Generate C/C++ Code](https://www.mathworks.com/help/coder/generating-code.html) and [`codegen`](https://www.mathworks.com/help/coder/ref/codegen.html): MATLAB Coder generation and JIT MEX options.
