---
name: research-ablation-diagnosis
description: Test a bounded set of component contributions or failure explanations when `current.state` is `ablation_diagnosis`.
---

# Research Ablation and Diagnosis

Distinguish only the approved candidate explanations while changing the target factor and holding controls fixed.

## Stage outcome

Connect each approved candidate to an observation that would distinguish it. Implement the smallest approved intervention that can resolve the question, keeping the controls comparable. Propose a scientific revision if the existing design cannot discriminate the candidates.

Use computing, testing, batch, aggregation, and statistical Skills only as the design requires. Preserve null, contradictory, failed, and unresolved outcomes. At the approved design boundary, record evidence and predicates and prepare every outgoing rule through `$research-state-transition`.

## Output

Link the intervention and result evidence, explain which candidates remain distinguishable or unresolved, and present the prepared lifecycle decision.

## Guardrails

- Keep diagnosis bounded to the approved candidates and controls.
- Do not treat implementation debugging as mechanism evidence or change scientific scope without an approved TODO revision.
