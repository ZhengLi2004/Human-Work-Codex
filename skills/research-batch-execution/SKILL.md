---
name: research-batch-execution
description: Build or review a resumable scientific batch runner for multi-unit, I/O-heavy, or long work.
---

# Research Batch Execution

Read `references/batch-run-contract.md` before implementing a formal runner. Use `$research-computing-implementation` for language, performance, and storage choices.

## Runner contract

Freeze the complete manifest and stable task keys before inspecting outcomes. Provide an idempotent, resumable command with explicit task states, validated completion, isolated atomic outputs, and separate logs. Choose batching and concurrency from measured runtime, CPU, memory, GPU memory, and I/O; report progress by completed units and an ETA when supported.

Demonstrate interruption, duplicate-launch, corrupt-output, and resume handling on a small manifest, reusing valid evidence for unchanged recovery logic. Reconcile every planned state before aggregation. Execution retries preserve the original independent-unit identity.

Keep runner and measurement code in `exp/`; keep manifests, checkpoints, logs, and outputs in `data/`.

## Runs over three hours

When estimated minimum runtime exceeds three hours, finish preflight and give the researcher the command, working directory, configuration, resources, outputs, resume instructions, and completion/failure criteria. Keep the stage open until outputs return.

## Output

Keep the manifest, stable-key definition, recovery evidence, resource measurements, and output index in task artifacts. Provide the executable command, relevant paths, reconciliation outcome, and any researcher handoff in the response.
