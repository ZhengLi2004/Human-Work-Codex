---
name: research-confirmation
description: Execute the frozen complete Confirmation specification when `current.state` is `confirmation`.
---

# Research Confirmation

Require a matching TODO fingerprint, frozen specification and configuration, approved parameters, applicable sensitivity evidence, passing material tests, and usable storage.

## Workflow

1. Compare the frozen configuration with the TODO and generate the complete manifest.
2. Run material regression and boundary tests, then complete one formal combination/repeat as preflight.
3. Execute or ingest the frozen manifest through `$research-batch-execution`; runs over one hour follow its researcher handoff.
4. Use `$research-evidence-aggregation` to reconcile all states and produce complete validated tables.
5. Preserve supporting, limiting, contradictory, negative, and anomalous facts.
6. Record predicates and prepare every outgoing rule.

A documented implementation error, corruption, frozen-spec violation, or incomplete run may invalidate affected artifacts. Record the reason and stable IDs, repair in place, add regression protection, and rerun the frozen specification. Result direction is not an invalidation criterion.

## Output

Return the frozen specification, command, reconciliation, data/table paths, supporting and limiting facts, invalidations, and predicates.

## Guardrails

- Never tune metrics, parameters, or exclusions after observing Confirmation results.
- Non-significance is not proof of no effect; follow-ups remain outside the predefined primary analysis.
