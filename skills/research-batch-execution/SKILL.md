---
name: research-batch-execution
description: Build or review a resumable scientific batch runner for multi-unit, I/O-heavy, or long work.
---

# Research Batch Execution

Read `references/batch-run-contract.md` before implementing a formal runner. Use `$research-computing-implementation` for language, performance, and storage choices.

## Workflow

1. Freeze the complete manifest and stable task keys before inspecting outcomes.
2. Build one idempotent, resumable command with explicit task states, validated completion, isolated atomic outputs, and separate logs.
3. Derive concurrency from measured runtime, CPU, memory, GPU memory, and I/O; report unit-based progress and ETA when meaningful.
4. Test interruption, duplicate launch, corrupt output, and resume on a small manifest.
5. Reconcile every planned state before aggregation.

Keep runner and measurement code in `exp/`; keep manifests, checkpoints, logs, and outputs in `data/`.

## Runs over one hour

When estimated minimum runtime exceeds one hour, finish preflight and give the researcher the command, working directory, configuration, resources, outputs, resume instructions, and completion/failure criteria. Keep the stage open until outputs return.

## Output

Return the manifest and task-key definition, commands, recovery and storage design, resource profile, progress/log paths, failure-test results, reconciliation, and raw-output index.
