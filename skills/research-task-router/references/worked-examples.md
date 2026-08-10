# Worked Routing Examples

These examples illustrate control flow only. Replace every identifier, predicate value, and artifact path with evidence from the active TODO and task-state file.

## Example 1: an unknown predicate blocks a forward transition

Situation:

- `current.state: development`;
- the smoke test passed;
- whether controls remain comparable is not documented;
- `development.self` is always eligible.

Correct route:

1. Record the missing comparability evidence as `unknown`, not `false` or `true`.
2. Mark `development.to_pilot` ineligible if one of its required predicates remains unknown.
3. Keep `development.self` eligible and normally recommend it while the evidence is completed.
4. Wait for an exact human rule-path selection before changing state.

Keep the missing predicate `unknown`; the passing smoke test supplies only technical evidence.

## Example 2: figures require three lifecycle states

Situation:

- complete raw, condition-merged, and row-preserving curated tables exist;
- the table contains method, noise level, repeat, estimate, uncertainty, and failure-count fields.

Correct route:

1. In `work_postprocessing`, curate the table, inspect relevant paper figures when available, map every method and noise condition to drafts, and render the governed set from an executed notebook using a SciencePlots stack based on `science`.
2. Evaluate `work_postprocessing.to_figure_review`; do not call the drafts final.
3. In `figure_review`, show the drafts and coverage summary and wait for the researcher to request inclusion, exclusion, revisions, or a supplemental schematic.
4. After the review output is recorded and the transition is approved, enter `figure_production`.
5. Produce the final figures and audit condition coverage, statistical units, titles, axes, units, legends, series, and missingness before evaluating completion.

Incorrect route: curate the table, draw only the clearest two conditions, and transition directly from `work_postprocessing` to `completed`.

A standalone `.py` layout preview must not serve as a draft. Keep its script and images under the platform temporary directory and reproduce any retained design in the executed notebook.

## Example 3: use standard terms or describe the process

Avoid:

> Apply a holistic evidence harmonization layer.

Prefer:

> Validate stable keys, left-join observed runs onto the planned-condition table, and summarize across independent repeats.

The second version names checkable operations with established terms.

## Example 4: Development preserves phase order

Situation: a TODO requires a large numerical sweep, and the repository contains a convenient Python prototype but no Python-only dependency.

Correct route:

1. Use MATLAB for the non-plotting pipeline.
2. Make it work with one representative end-to-end task, realistic shapes, and buffered output.
3. Make it right by implementing the TODO and comparing it with an audited small reference case.
4. Make it fast by profiling, removing repeated work, then measuring vectorization, MEX, parallel, or GPU options as applicable; retain only changes that pass equivalence tests and improve representative runtime.

Incorrect route: translate the prototype directly to a parallel Python run because Python is already familiar, or compile a MEX kernel before a correctness reference exists.

## Example 5: a verified parameter changes the active TODO

Situation: Pilot evaluated every approved regularization value under a predefined selection rule, the complete table includes failures and ties, and the researcher approves the rule-supported value.

Correct route:

1. Preserve the full grid and selection artifact under the result root.
2. Have Work rewrite the TODO with the approved fixed value and only the work that remains; remove the completed search instructions, rejected candidates, and obsolete alternatives from the active TODO.
3. Have Codex increment task-state revision, refresh the TODO fingerprint, record approval/evidence references, and reevaluate every outgoing rule.

Incorrect route: keep the old candidate grid beside the selected value in a downstream TODO, delete losing runs, or apply the transition review computed from the pre-rewrite TODO.
