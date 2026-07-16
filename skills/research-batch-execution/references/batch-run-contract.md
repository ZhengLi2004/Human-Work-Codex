# Batch Run Contract

## Identity

A task key must include every dimension that can change the scientific output: TODO identifier, data unit, condition values, controls, repeat/seed, method/config fingerprint, and code/data version when applicable.

## Frozen manifest

Generate the complete task manifest before execution. The manifest is a technical artifact under the TODO result directory, not a handoff document. It must not be expanded or pruned after outcomes are observed.

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

- Use immutable per-task or per-chunk outputs with stable schema.
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
5. never overwrite historical attempts silently;
6. reconcile final task counts.

## Progress and logging

Progress is based on stable task units, not internal loop iterations. Report completed, failed, invalid, and remaining counts plus ETA when meaningful. Timer-driven live status must degrade safely to ordinary logs in non-interactive environments.

## Long-run boundary

At or above the policy threshold, Codex prepares and validates the command, checkpoint/resume behavior, resource profile, and result paths, then stops for a human launch decision.
