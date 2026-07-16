---
name: research-batch-execution
description: Build or review a resumable scientific batch executor with a frozen task manifest, checkpoints, progress, logs, failure isolation, resource limits, and high-throughput result storage. Use for multi-condition, multi-repeat, heavy-I/O, or long-running jobs. Do not generate tasks after seeing results.
---

# Research Batch Execution

## Overview

Give every planned experiment unit a stable identity, explicit state, and traceable output so interruption, concurrency, and failures cannot silently omit, duplicate, or overwrite evidence.

Read `references/batch-run-contract.md` and `references/io-throughput-checklist.md` before implementing a formal runner.

## Required inputs

- the complete TODO and task-state current state;
- the full condition set and controls;
- the independent-repeat definition;
- predefined failure, missingness, invalidation, and comparability rules;
- `.research/policy.yaml` resource and long-run policy;
- result root, code/data/config versions, and aggregation entry point.

Stop if the complete planned task set cannot be generated before execution.

## Workflow

1. Generate and persist the complete task manifest.
2. Derive a stable task key from all variables, controls, repeat identifiers, data scope, and version fingerprints.
3. Use explicit states such as `pending`, `running`, `complete`, `failed`, `skipped`, and `invalid`.
4. Isolate each task or worker output so concurrent workers do not append to the same scientific result table.
5. Buffer records in memory or write task/chunk files in bulk; publish completed files atomically.
6. Mark a task complete only after validating its expected artifacts.
7. Make the same command resumable and idempotent; valid completed units are not recomputed or recounted by default.
8. Isolate failures so one task cannot erase other results.
9. Report progress, ETA, completed/failed counts, and a timer-driven status line when interactive; degrade to ordinary logs when not interactive.
10. Write operational logs to terminal and file, separate from bulk result data.
11. Derive concurrency from measured single-task CPU, memory, GPU memory, runtime, and I/O behavior.
12. Test interruption/resume, duplicate launch, invalid output, and damaged checkpoint behavior on a small task set.
13. Reconcile planned, completed, failed, missing, invalid, duplicate, and pending units before aggregation.

## Mandatory I/O safeguards

- Never open and rewrite a CSV or spreadsheet once per result row.
- Never append one result row per task to a shared CSV from multiple workers.
- Never repeatedly concatenate a growing pandas DataFrame inside the task loop.
- Never call MATLAB `writetable` for every row or task.
- Prefer immutable per-task files followed by one merge, or buffered/partitioned Parquet, HDF5, Zarr, NPZ, or MAT v7.3 outputs.
- For a logically single table that is physically partitioned, provide one dataset directory and stable schema.
- Use line-oriented writes only for logs and small checkpoint metadata.
- During preflight, inspect file-open count, bytes written, serialization time, and storage wait when I/O may be material.
- If I/O dominates, increase chunk granularity, reduce file count, use columnar/binary storage, or move aggregation out of the inner loop before adding workers.

## Long-running gate

At or above the policy threshold:

1. complete tests and one-combination/one-repeat preflight;
2. verify storage, checkpoint, resume, progress, logging, and aggregation;
3. provide one command, working directory, expected resources, result path, completion criteria, and failure criteria;
4. invoke `$human-research-review-gate`;
5. do not launch the formal job.

## Guardrails

- Do not add or remove tasks after observing results.
- Do not treat file existence as valid completion without content validation.
- Do not overwrite historical raw artifacts when resuming.
- Do not silently retry until a favorable result appears; every retry has a new recorded attempt.
- Do not increase resource limits without approval.
- Do not let parallel scheduling alter the sample set or random process.

## Output contract

Return the task manifest, task-key definition, commands, checkpoint/resume design, storage layout, measured resource and I/O profile, progress/log paths, fault-injection results, final task reconciliation, and raw-output index for aggregation.
