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

The passing smoke test does not supply the missing predicate.

## Example 2: figures require three lifecycle states

Situation:

- complete raw, condition-merged, and row-preserving curated tables exist;
- the table contains method, noise level, repeat, estimate, uncertainty, and failure-count fields.

Correct route:

1. In `work_postprocessing`, curate the table, inspect relevant paper figures when available, map every method and noise condition to drafts, and write the coverage manifest.
2. Evaluate `work_postprocessing.to_figure_review`; do not call the drafts final.
3. In `figure_review`, show the drafts and coverage summary and wait for the researcher to request inclusion, exclusion, revisions, or a supplemental schematic.
4. After the review output is recorded and the transition is approved, enter `figure_production`.
5. Produce the final figures and audit condition coverage, statistical units, titles, axes, units, legends, series, and missingness before evaluating completion.

Incorrect route: curate the table, draw only the clearest two conditions, and transition directly from `work_postprocessing` to `completed`.

## Example 3: use standard terms or describe the process

Avoid:

> Apply a holistic evidence harmonization layer.

Prefer:

> Validate stable keys, left-join observed runs onto the planned-condition table, and summarize across independent repeats.

The second version names operations that can be checked. It does not introduce a new term whose meaning is unclear.
