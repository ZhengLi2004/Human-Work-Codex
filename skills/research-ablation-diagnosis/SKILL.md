---
name: research-ablation-diagnosis
description: Test a bounded set of component contributions or failure explanations when `current.state` is `ablation_diagnosis`.
---

# Research Ablation and Diagnosis

Distinguish only the approved candidate explanations while changing the target factor and holding controls fixed.

## Workflow

1. State each candidate and the observation that would strengthen or weaken it.
2. Design the smallest discriminating intervention and verify that only the intended factor changes.
3. Use computing, testing, batch, and aggregation Skills only where the design needs them.
4. Preserve null, contradictory, failed, and unresolved outcomes; stop at the approved design boundary.
5. Record artifacts and predicates with evidence, then use `$research-state-transition` to prepare every outgoing rule.

## Output

Return candidates, interventions, commands, observed facts, unresolved explanations, artifacts, and predicate evidence.

## Guardrails

- Keep diagnosis bounded to the approved candidates and controls.
- Do not treat implementation debugging as mechanism evidence or change scientific scope without an approved TODO revision.
