# Research Task System

Research Task System turns one complete research TODO into a rule-driven Work/Codex workflow with explicit human decisions.

```text
Research TODO (Written by researcher)
    ↓
Write an implementation TODO (Better with GPT work)
    ↓
Initialize research state YAML (From now on better with Codex)
    ↓
Recommend and confirm outgoing state
    ↓
Execute the recorded state
    ↓
Update research state YAML
    ↓
...... (loop)
    ↓
Curate tables and prepares drafts (Better with GPT work)
    ↓
Review the drafts and supplies recommendations (Written by researcher)
    ↓
Produce and check final figures (Better with GPT work)
    ↓
Finish
```

## Repository layout

```text
.
├── .codex-plugin/
│   └── plugin.json
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── agents/
│   └── openai.yaml
├── skills/
│   ├── research-task-router/
│   ├── research-todo-executor/
│   ├── research-state-transition/
│   ├── research-exploration/
│   ├── research-development/
│   ├── research-pilot/
│   ├── research-confirmation/
│   ├── research-ablation-diagnosis/
│   ├── research-computing-implementation/
│   ├── research-agile-testing/
│   ├── research-batch-execution/
│   ├── research-evidence-aggregation/
│   ├── human-research-review-gate/
│   ├── research-report-to-todos/
│   ├── publication-table-curation/
│   ├── research-figure-production/
│   └── post-report-assessment/
├── .research/
│   ├── ENTRYPOINTS.md
│   ├── policy.yaml
│   ├── templates/
│   │   ├── TODO.md
│   │   └── task-state.yaml
│   └── workflow/
│       ├── pipeline.yaml
│       └── state-machine.yaml
├── requirements.txt
├── AGENTS.md
└── README.md
```

## Installation and discovery

The repository is an installable local Plugin and includes:

- `.codex-plugin/plugin.json`;
- `.agents/plugins/marketplace.json`;
- `skills/`.

Use `$research-task-router` as the entry point after installation.

For direct repository-scoped Codex discovery without installing the Plugin, create a symlink:

```bash
mkdir -p .agents
ln -s ../skills .agents/skills
```

## Artifacts

| File or directory | Purpose |
|---|---|
| `TODO.md` | Complete scientific specification and output path references |
| `results/{todo_id}/task-state.yaml` | Current lifecycle state, rule evaluation, approvals, revision, and versioned evaluation history |
| `.research/workflow/state-machine.yaml` | Reusable predicates, states, and transition rules |
| `SKILL.md` | Reusable workflow, guardrails, and output contract |
| `AGENTS.md` | Permanent scientific and execution governance |
| `.research/policy.yaml` | Adjustable resource, storage, and transition policy |
| `results/{todo_id}/` | State, logs, checkpoints, raw outputs, tables, notebooks, and figures |

## Usage

Setup the environment by:

```bash
python -m pip install -r requirements.txt
```

Write TODOs by:
```text
Use @Research Task System to create a TODO from [materials].
Save it as TODO/[name].md
```

Initialize research state YAML by:
```text
Use $research-task-router for TODO/[name].md.
Initialize state and evaluate transitions. Do not apply.
```

Confirm research state transition by:
```text
Approve [rule_id] and execute the target state.
```

Continue the current research state by:
```text
Use $research-task-router for TODO/[name].md.
Execute the recorded current state.
```

Start table curation and figure planning by:
```text
Use @Research Task System to process TODO/[name].md.
```

Review draft figures after the approved transition to `figure_review`:

```text
Use $research-task-router for TODO/[name].md.
Present every draft figure and its coverage of all applicable data, then wait for my recommendations.
```

Produce final figures only after the approved transition to `figure_production`:

```text
Use $research-task-router for TODO/[name].md.
Implement my recorded figure recommendations and run the final figure integrity audit.
```

Infer the outgoing state by:
```text
Use $research-task-router for TODO/[name].md.
Evaluate outgoing rules. Do not apply.
```

## Communication discipline

The system uses established scientific and engineering terms when available. It describes concrete operations before introducing a necessary local label, ties evaluative terms to explicit criteria, and uses only a small number of examples to clarify fragile rules.
