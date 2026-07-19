# Test Selection Matrix

| Risk | Preferred test | Minimum useful scope |
|---|---|---|
| Formula or local transform | unit, property, differential, metamorphic | deterministic micro-example |
| Data semantics, units, shapes | schema and contract assertions | loader boundary |
| Indexing or label alignment | parameterized boundary cases | smallest mismatched case |
| Data leakage | split-membership and provenance checks | one representative partition |
| Control fairness | configuration diff / invariant checks | paired control and treatment |
| Module boundary | focused integration test | one path across the boundary |
| Full experiment chain | end-to-end smoke test | one combination, one repeat |
| Defect repair | regression test | minimal reproducer |
| Randomness | fixed-seed determinism + independent-repeat checks | two reruns |
| Checkpoint/resume | interruption and idempotence test | two recoverable task units |
| Numerical optimization | reference/differential test + benchmark | same inputs, dtype, and justified tolerance |
| CPU/GPU equivalence | numerical comparison + decision-boundary check | representative small and memory-relevant cases |
| Python vectorization | loop/reference equivalence + memory benchmark | representative array shape |
| MATLAB vectorization | scalar/loop reference + `matlab.unittest` comparison | representative matrix/page shape |
| Cross-language interchange | round-trip schema, dtype, shape, key, and index test | one representative artifact |
| Aggregation | synthetic complete/incomplete grids | every status class |
| Buffered/partitioned I/O | interruption, duplicate, schema, row-count, and atomic-publish tests | two chunks and one damaged chunk |
| Parallel scheduling | serial/parallel equivalence + duplicate/missing task reconciliation | small complete manifest |
| Figure source completeness | stable-key/coverage comparison against logical source | one figure specification |
| Figure title, axes, legend, or unexplained series | manifest-to-render audit plus visual inspection | every final figure |
| Researcher figure recommendation | recommendation-to-manifest trace check | every requested include, exclude, revision, or schematic |
| Generalized diagram mistaken for data | kind/label/source audit | every schematic |

## Oracle priority

1. Analytic expected value.
2. Trusted independent reference implementation.
3. Scientific invariant or conservation relation.
4. Metamorphic relationship.
5. Manually audited tiny case.
6. Snapshot/characterization only when no stronger oracle exists.

## Language-specific tools

- Python: `pytest`, `numpy.testing`, `pandas.testing`, `scipy` reference routines, and `torch.testing` when applicable.
- MATLAB: `matlab.unittest`, numerical constraints, deterministic fixtures, and CPU/GPU or loop/vectorized differential tests.

A performance improvement is not accepted merely because it is faster. It must preserve the TODO-defined numerical behavior and result population.
