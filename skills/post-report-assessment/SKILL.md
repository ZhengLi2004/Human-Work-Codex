---
name: post-report-assessment
description: Assess the expected information gain of the next research action after the human has written the experimental report. Use the TODO and complete results as facts and the human report as interpretation. Do not rewrite the report or automatically create/start another TODO.
---

# Post-Report Assessment

## Overview

Use this Skill after the human scientific report is available. Evaluate whether more work on the same question is likely to change a research decision, narrow an important uncertainty, or reveal a distinct new question.

## Required inputs

- the original TODO;
- task-state YAML and confirmed transition history, when lifecycle state exists;
- Codex result paths and complete tables;
- Work curated tables and figures, when available;
- the human experimental report;
- relevant neighboring TODOs or established project facts.

## Workflow

1. Read the current lifecycle state and confirmed history. Treat `completed` and `stopped` as terminal; do not reopen them through this assessment.
2. Extract the human report's scientific conclusions, limitations, and unresolved questions without rewriting them.
3. Cross-check that each factual premise is supported by the complete tables rather than only a selected figure.
4. Identify which uncertainty currently controls the next research decision.
5. Estimate the expected information gain of:
   - continuing the same design;
   - targeted additional evidence;
   - redesigning the method;
   - stopping the direction;
   - creating a new TODO for a genuinely separate phenomenon.
6. Compare expected information gain with cost, implementation risk, and redundancy with existing evidence.
7. Give one primary recommendation and bounded alternatives.
8. Require human approval before a new TODO is authored or executed.

## Boundaries

- Do not replace the human report's mechanism interpretation with a model-generated narrative.
- Do not use only favorable plots or rows.
- Do not create a second report or handoff document.
- Do not automatically create or start the next TODO.
- Do not mutate the terminal lifecycle state; additional scientific work requires a new TODO or an explicitly governed redesign.
- Use the report's established terminology where it is precise. Do not replace a concrete process or uncertainty with a newly coined abstract label, and tie evaluative language to the cited evidence.

## Output contract

Return in chat:

- the decision-controlling uncertainty;
- the evidence supporting and limiting the current conclusion;
- one primary recommendation: `Continue`, `Targeted Follow-up`, `Redesign`, `Stop`, or `New TODO`;
- expected information gain and cost/risk rationale;
- the smallest proposed next scope;
- the human decision required.
