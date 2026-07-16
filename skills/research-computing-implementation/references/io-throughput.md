# Scientific Result I/O Throughput

## Failure pattern to prevent

The prohibited pattern is an inner compute loop that opens, appends one row to, or rewrites a CSV/XLSX/table file for every result. Variants include repeated `DataFrame.concat`, repeated `to_csv`, repeated MATLAB `writetable`, and multiple workers appending to one shared table.

This pattern wastes compute through file-open overhead, serialization, metadata updates, lock contention, repeated parsing, and quadratic copying. It can also corrupt or silently interleave concurrent output.

## Required architecture

1. Define one stable result record schema before the run.
2. Accumulate records in bounded in-memory buffers or compute a meaningful task chunk.
3. Flush one chunk in a typed bulk format.
4. Write to a temporary path on the destination filesystem.
5. Validate the chunk schema, row count, stable IDs, and required fields.
6. Atomically rename/move it to its final immutable path.
7. Record completion in small checkpoint metadata only after the artifact is valid.
8. Merge or scan partitioned chunks after task execution, not inside every task.

## Storage choices

| Artifact | Default | Alternatives | Avoid |
|---|---|---|---|
| Large run-level table | Partitioned Parquet | Arrow IPC, HDF5 when schema fits | Row-wise CSV append |
| Small interchange table | CSV plus schema/manifest | Parquet | XLSX as computational store |
| Dense numeric arrays | NPY/NPZ for Python-only; HDF5 for cross-language | MAT v7.3 | Thousands of tiny text files |
| Model/checkpoint state | Framework-native checkpoint plus metadata | HDF5/MAT where appropriate | Mixing checkpoint bytes into result tables |
| Logs | Line-oriented text/JSONL | Structured logging backend | Using logs as scientific result storage |

HDF5 usually requires a single-writer design unless the environment and implementation explicitly support safe parallel access. Prefer worker-isolated files followed by merge when uncertain.

## Buffer and partition design

Choose a flush boundary based on all of:

- target chunk size in bytes;
- maximum tolerated data loss between checkpoints;
- per-worker memory;
- task duration;
- downstream scan/filter keys;
- file-count limits of the storage system.

Partition by stable, commonly filtered dimensions with moderate cardinality. Do not partition by a near-unique identifier such as every trial or timestamp.

## Measurement

During representative preflight record:

- compute time;
- serialization time;
- file-open/write/rename time;
- bytes and rows written;
- number and median size of files;
- storage wait or queue time when observable;
- peak memory while the buffer is full;
- throughput before and after concurrency.

When I/O is material, fix format, buffer size, partitioning, merge placement, or file count before adding compute workers. More workers can make a storage bottleneck worse.

## Acceptance checks

- No scientific result write occurs once per result row.
- No shared CSV/table append occurs from concurrent workers.
- No growing DataFrame/table is copied on every iteration.
- Resume does not duplicate valid rows or overwrite immutable chunks.
- The final table reconciles exactly to the planned task manifest.
- A result row is traceable to one stable task/repeat ID and raw artifact.
