# Python and MATLAB Scientific-Computing Guide

Use this reference after the TODO fixes scientific meaning. Benchmark material performance changes on representative work.

## Selection

| Need | Choice | Record |
|---|---|---|
| Numerical kernels, preprocessing, orchestration, aggregation, storage | MATLAB | Release, toolboxes, environment, Work/Right/Fast evidence |
| Required Python-only package or interface | Smallest coherent Python component | Dependency, why substitution fails, boundary tests |
| Measured environment constraint requires Python | Documented Python exception | Capability evidence and rationale |
| Governed plotting | Separate Matplotlib/SciencePlots `.py` script | Script, hashes, command, style stack |
| Cross-language tables | Parquet with explicit schema | Keys, types, missing values, round-trip test |
| Cross-language large arrays | MAT v7.3 or HDF5 | Dataset names, shapes, dtypes, axis order |

Convenience, familiarity, existing Python code, or shorter syntax does not justify an exception.

## Python exception guidance

- Prefer NumPy/SciPy array operations and solvers over Python loops or explicit matrix inversion when semantics and memory permit.
- Keep dtype, device movement, sparse/dense conversion, and randomness explicit.
- Build tabular output by bounded batches; use pandas for moderate tables and PyArrow/Parquet, HDF5, or Zarr for larger data.
- Measure process/thread pools, BLAS oversubscription, data loading, GPU transfer, mixed precision, and `torch.compile` end to end before retaining them.
- Use PyTorch only when the required method depends on it; isolate loading, model, training, evaluation, and checkpoints behind the recorded boundary.
- Test with `pytest`, `numpy.testing`, `pandas.testing`, or `torch.testing` as applicable. Derive tolerances from the algorithm, dtype, and decision boundary.

## MATLAB guidance

- Put reusable hot code in functions with stable types and shapes; MATLAB optimizes execution automatically and has no general manual JIT switch.
- Eliminate repeated work and improve the algorithm before tuning syntax.
- Preallocate outputs, avoid repeated representation conversion, exploit appropriate matrix/sparse structure, and use stable solvers such as `A\b`.
- Compare loops, vectorization, and optimized built-ins on representative shapes; include temporary-array memory.
- Use MATLAB Profiler for bottlenecks and `timeit` or `gputimeit` after warm-up.
- Use `matfile`, `datastore`/`tall`, Parquet, or MAT v7.3 when their access model fits. Follow `io-throughput.md` for batching and atomic publication.
- Keep worker outputs isolated. Use `parfor` for independent sliced iterations and `parfeval` for asynchronous or uneven tasks only after measuring transfer, memory, and scheduling cost.
- Use `gpuArray` only for supported, sufficiently large work with transfer-aware timing and CPU/GPU equivalence tests.
- Consider hand-written or generated MEX only for a stable profiled kernel. Keep the MATLAB reference and record source, build command, compiler/toolbox, platform support, fallback, benchmark, and equivalence test. `codegen -jit` means JIT MEX generation, not general MATLAB JIT.
- Use `matlab.unittest` with explicit, scientifically justified tolerances.

## Optimization options

Choose from these options for the measured bottleneck. Preserve Work/Right/Fast dependencies; there is no requirement to try every technique or exhaust them in this order.

1. Eliminate unnecessary work and repeated I/O.
2. Improve complexity, numerical method, and task granularity.
3. Improve allocation, memory layout, batching, and storage.
4. Measure loops, vectorization, built-ins, and toolbox routines.
5. Compile a stable hot kernel when justified.
6. Parallelize independent work after resource measurement.
7. Use a GPU when transfer-aware speedup and equivalence are demonstrated.
8. Re-profile end to end and retain only useful net improvements.

## Cross-language boundary

Record schema/dataset names, unique keys, shapes and axis order, dtypes, missing and categorical encodings, units/timezones, compression/partitioning, producer version, and a round-trip test. Check MATLAB's 1-based column-major conventions against Python's indexing and array layout explicitly.

Plotting scripts follow `$research-figure-production`; they must not become the production implementation of metrics, inference, fitting, exclusions, or aggregation.

## MATLAB references

- [Improve Performance](https://www.mathworks.com/help/matlab/matlab_prog/techniques-for-improving-performance.html)
- [Profile Code](https://www.mathworks.com/help/matlab/matlab_prog/profiling-for-improving-performance.html) and [`timeit`](https://www.mathworks.com/help/matlab/ref/timeit.html)
- [`parfor` performance](https://www.mathworks.com/help/parallel-computing/improve-parfor-performance.html)
- [`gpuArray`](https://www.mathworks.com/help/parallel-computing/gpuarray.html) and [GPU performance](https://www.mathworks.com/help/parallel-computing/measure-and-improve-gpu-performance.html)
- [C MEX functions](https://www.mathworks.com/help/matlab/matlab_external/c-mex-functions.html)
- [MATLAB Coder](https://www.mathworks.com/help/coder/generating-code.html) and [`codegen`](https://www.mathworks.com/help/coder/ref/codegen.html)
