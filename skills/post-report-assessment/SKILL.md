---
name: post-report-assessment
description: Assess the information value of a next research action after the human report is available.
---

# Post-Report Assessment

Use the TODO and complete results as facts and the human report as interpretation. Read the task state/history, tables, figures, report, and relevant neighboring work.

## Workflow

1. Verify the report's factual premises against complete tables, not selected figures.
2. Identify the uncertainty controlling the next decision.
3. Compare continuation, targeted evidence, redesign, stopping, and a separate TODO by expected information gain, cost, implementation risk, and overlap.
4. Recommend one option and its smallest useful scope; include an alternative only when it materially changes the tradeoff.
5. Request approval before authoring or executing another TODO.

Keep `completed` and `stopped` terminal. Preserve the human's interpretation, use established terminology, and do not create a second report or select favorable evidence.

## Output

Return the controlling uncertainty, supporting and limiting evidence, recommendation (`Continue`, `Targeted Follow-up`, `Redesign`, `Stop`, or `New TODO`), tradeoff, smallest next scope, and required decision.
