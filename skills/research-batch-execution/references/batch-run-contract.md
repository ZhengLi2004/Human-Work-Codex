# Batch Run Contract

## Identity

A task key must include every dimension that can change the scientific output: TODO identifier, data unit, condition values, controls, repeat/seed, method/config fingerprint, and code/data version when applicable.

## Frozen manifest

Generate the complete task manifest before execution and store it under `TODO_###/data/`. Keep its runner under `TODO_###/exp/`. The manifest is not a handoff document and is never expanded or pruned after outcomes are observed.

Recommended columns:

- `task_id`
- condition/control columns
- independent repeat/seed
- input identifiers
- configuration fingerprint
- expected output location
- current execution state
- attempt identifier

## States

Use explicit states such as `pending`, `running`, `complete`, `failed`, `missing`, `skipped`, and `invalid`. A task is `complete` only after its output validates.

## Storage

- Use independently valid per-task or per-chunk outputs with stable schema.
- Prefer partitioned Parquet for large run-level tables and HDF5/MAT v7.3 for compatible numerical arrays.
- Never update a scientific CSV/table one row at a time.
- Never have multiple workers append to one shared result table.
- Keep checkpoint metadata small and separate from bulk results.
- Publish a chunk atomically after validation.

## Resume

The same command must be idempotent. On resume:

1. read the frozen manifest and configuration fingerprint;
2. validate existing completed outputs;
3. skip only valid completed units;
4. rerun failed/incomplete units according to the recorded retry policy;
5. record a debug invalidation before deleting or replacing a proven invalid attempt;
6. reconcile final task counts.

## Progress and logging

Progress is based on stable task units, not internal loop iterations. Report completed, failed, invalid, and remaining counts plus ETA when meaningful. Timer-driven live status must degrade safely to ordinary logs in non-interactive environments.

## Preflight

Measure records and bytes per flush, serialization/write time, file count, peak buffered memory, compute/I/O ratio, and throughput at one and proposed worker counts. Test interruption during compute and publication, valid and corrupt resume, duplicate launch, and schema/configuration mismatch.

## Long-run boundary

When estimated minimum runtime exceeds three hours, Codex prepares and validates the resumable script or command, batching, checkpoints, progress, logs, resource profile, and result paths, then hands it to the researcher for execution.
