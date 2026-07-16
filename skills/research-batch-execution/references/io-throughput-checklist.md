# Batch I/O Throughput Checklist

Use this checklist before a Pilot or Confirmation runner is accepted.

## Inner-loop audit

- Search Python code for `to_csv`, `to_excel`, `to_parquet`, `DataFrame.append`, and `pd.concat` inside task/result loops.
- Search MATLAB code for `writetable`, `writematrix`, `save`, and table/array growth inside loops.
- Search worker functions for appends to shared paths.
- Confirm logs are separate from scientific records.

Any scientific table write per result row is a blocking defect unless the artifact is inherently one-row-per-expensive-task and file-count/storage measurements justify one immutable file per task.

## Bulk-write design

- Stable record schema is defined before execution.
- Buffer/chunk size is bounded and configurable.
- Each worker owns distinct temporary and final paths.
- Temporary output is written on the destination filesystem.
- Publish uses atomic rename/move where supported.
- Chunk validation precedes checkpoint completion.
- Final merge occurs once or the partitioned dataset is consumed directly.
- Schema evolution and incompatible resumptions are rejected.

## Preflight measurements

- Rows/records per flush
- Bytes per flush
- Serialization seconds per flush
- Write seconds per flush
- File count and size distribution
- Peak worker memory with a full buffer
- Compute/I/O time ratio
- Throughput at 1 worker and proposed worker count

## Failure tests

- Interrupt during computation.
- Interrupt during temporary-file write.
- Interrupt after file publish but before checkpoint update.
- Restart with a valid completed chunk.
- Restart with a truncated/corrupt chunk.
- Launch a duplicate task.
- Change schema/configuration while checkpoints exist.

## Pass criteria

The runner resumes without duplicate scientific rows, does not overwrite valid historical chunks, reconciles every planned task state, and does not perform row-at-a-time table I/O.
