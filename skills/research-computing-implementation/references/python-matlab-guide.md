# Python and MATLAB Scientific-Computing Guide

Use this reference after the TODO has fixed the scientific meaning. Language and package choices are engineering decisions unless the TODO explicitly fixes them.

## Contents

- [Selection matrix](#selection-matrix)
- [Python implementation guidance](#python-implementation-guidance)
- [MATLAB implementation guidance](#matlab-implementation-guidance)
- [Visualization artifact boundary](#visualization-artifact-boundary)
- [Cross-language boundary](#cross-language-boundary)

## Selection matrix

| Workload characteristic | Prefer Python | Prefer MATLAB |
|---|---|---|
| Large heterogeneous tabular datasets, partitioned files, or distributed preprocessing | pandas, PyArrow, Polars only when approved, Dask only when justified | `datastore` and `tall` can work, but cross-file table engineering is usually less flexible |
| Dense linear algebra already expressed as array equations | NumPy/SciPy | Native MATLAB arrays and matrix operations are often the clearest choice |
| Existing MATLAB algorithm/toolbox code with validated numerical behavior | Port only with explicit need and equivalence tests | Keep MATLAB and improve vectorization/preallocation first |
| Neural networks or custom GPU training | PyTorch is the default; TensorFlow/JAX only when the project already requires them | `trainnet`, `dlnetwork`, and Deep Learning Toolbox are suitable when the project is MATLAB-centered |
| Complex figure/data-product pipeline after Codex | Python/Jupyter | Use MATLAB figures only when the TODO or existing validated workflow requires them |
| Cross-language tabular interchange | Parquet with an explicit schema | `parquetread` / `parquetwrite` when supported by the installed release |
| Cross-language large numeric arrays | HDF5 with named datasets, shapes, dtypes, and axis metadata | MAT v7.3 or HDF5; verify Python reader compatibility |

Do not choose a language only because a single operation is syntactically shorter. Consider existing validated code, data volume, library support, reproducibility, and the cost of cross-language conversion.

## Python implementation guidance

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

### Array and matrix work

- Express dense numerical work with matrix multiplication, broadcasting/implicit expansion, logical indexing, reductions, `pagemtimes`, and appropriate toolbox routines.
- Preallocate numeric arrays, cell arrays, structures, and table variables before loops when output size is known.
- Use `A\b`, decomposition objects, or iterative solvers instead of `inv(A)*b`.
- Move invariant work outside loops only after proving the value does not depend on the iteration.
- Avoid repeated conversion among tables, cells, structures, and numeric arrays inside hot loops. Convert once at a clear boundary.
- Use MATLAB Profiler and `timeit`/`gputimeit` for representative kernels.

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
