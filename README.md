# Research Task System

Research Task System runs one scientific TODO through a rule-based lifecycle in Codex. The researcher controls scientific and lifecycle decisions; Codex authors and revises TODOs, implements, tests, runs shorter jobs, aggregates evidence, curates tables, and produces figures.

## Skill organization and working style

`research-task-router` selects the recorded lifecycle stage. Stage Skills define the evidence needed to finish that stage; capability Skills handle computing, testing, batch execution, aggregation, statistics, and figures. `research-state-transition` owns atomic decisions and `human-research-review-gate` presents choices reserved to the researcher. Scientific meaning stays in the TODO, rules in the state machine, adjustable limits in policy, and detailed procedures in capability references.

The prompts are written for Astra with outcome-oriented instructions, bounded engineering discretion, focused clarification, and risk-proportional verification, following [OpenAI's Astra prompting guidance](https://developers.openai.com/api/docs/guides/latest-model) (reviewed 2026-09-20). They retain the scientific and lifecycle invariants and do not change the selected model or runtime settings. The entry prompts state the desired result without repeating the full workflow.

## Research priorities

Work from problem to metrics to framework to parameters. Spend most effort on modeling, derivation, and analysis; refine only after framework validation. Judge primary criteria and explicit tradeoffs against fair baselines; keep secondary measures within justified bounds. A failing framework prompts reassessment before more tuning. The 80/20 split guides effort rather than enforcing a time quota.

Long-run handoff starts above three hours of estimated minimum runtime. Inspect images only when needed, using thumbnails; preserve full-resolution deliverables and record unresolved visual limits.

## Statistical design and reporting

`research-statistical-analysis` connects TODO design, Confirmation freeze, complete result tables, and figure captions. It covers independent units and exact n, sample-size rationale, dependence, effect estimates and uncertainty, applicable tests and multiplicity, assumptions, exclusions/missingness, and reproducible reporting. Deterministic or descriptive tasks record applicability without adding unnecessary tests. The engineering preflight repeat default is not a scientific sample-size rule.

See the [CNS source notes](skills/research-statistical-analysis/references/cns-statistical-reporting.md) for journal-specific provenance and retrieval limits, and the [statistical evidence contract](skills/research-statistical-analysis/references/statistical-evidence-contract.md) for artifact integration. These are a reporting baseline, not a guarantee of Cell, Nature, or Science acceptance or submission compliance.

Rule set 8 retains statistical evidence and adds problem-led framework validation and thumbnail-based inspection to existing predicates. Existing tasks migrate with evidence preserved, pending decisions invalidated, and affected predicates re-evaluated; see the [state-file contract](skills/research-state-transition/references/state-file-contract.md). Historical terminal tasks remain terminal.

## Repository layout

```text
.
├── .codex-plugin/plugin.json
├── .agents/plugins/marketplace.json
├── .research/
│   ├── ENTRYPOINTS.md
│   ├── policy.yaml
│   ├── templates/
│   └── workflow/
├── agents/openai.yaml
├── skills/
├── AGENTS.md
├── requirements.txt
└── README.md
```

Each task has one repository-root directory:

```text
TODO_001/
├── TODO.md
├── task-state.yaml
├── code/        # optional reusable method/framework code
├── exp/         # experiment, metric, aggregation, and plotting code
└── data/        # experimental data and generated artifacts
```

Use exactly `TODO_###` with three digits. `exp/` and `data/` are required; omit `code/` when the TODO needs no method implementation. Keep `code/` cohesive, documented with Google-style Python docstrings and MATLAB help comments, and free of known code smells. `exp/` has no prescribed architecture or documentation style; it only needs to complete the required experiment.

## Clone and install dependencies

```bash
git clone https://github.com/ZhengLi2004/Human-Work-Codex.git
cd Human-Work-Codex
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Import into Codex

### Recommended: local Plugin

1. Open the cloned repository in Codex desktop.
2. Restart Codex.
3. Install **Research Task System** from **Research Task System (Local)**.
4. Start a new task so Plugin Skills and repository `AGENTS.md` load together.

CLI equivalent from the repository root:

```bash
codex plugin marketplace add .
codex plugin add research-task-system@research-task-system-local
```

### Repository-scoped Skills without the Plugin

macOS or Linux:

```bash
ln -s ../skills .agents/skills
```

Windows PowerShell:

```powershell
$skillTarget = (Resolve-Path .\skills).Path
New-Item -ItemType Junction -Path .\.agents\skills -Target $skillTarget
```

Restart Codex or start a new task. Repository-root `AGENTS.md` loads automatically; the link exposes the Skills.

## Verify installation

In a new Codex task, run `/skills` and confirm `research-task-router` is available. A read-only check is:

```text
Summarize the active repository AGENTS.md instructions and name the Research Task System entry Skill. Do not modify files or external state.
```

For the Plugin path:

```bash
codex plugin list --marketplace research-task-system-local
```

Official references: [Plugins](https://developers.openai.com/codex/plugins), [Build skills](https://developers.openai.com/codex/skills), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), and [plugin packaging](https://developers.openai.com/plugins/build/plugins).

## Lifecycle

States are:

```text
todo_ready
development
pilot
confirmation
ablation_diagnosis
figure_review
figure_production
completed | stopped
```

`todo_ready` includes TODO validation plus bounded project-mapping, data-semantic, and feasibility exploration; there is no separate Exploration or Evaluate state. It then presents every eligible rule, including self. Each later stage prepares its outgoing paths at its own decision boundary, and confirmation begins the target immediately.

## Main artifacts

| Artifact | Purpose |
|---|---|
| `TODO_###/TODO.md` | Current scientific specification and standard task paths |
| `TODO_###/task-state.yaml` | State, fingerprint, evidence-backed choices, and history |
| `.research/workflow/state-machine.yaml` | States, predicates, and rules |
| `.research/policy.yaml` | Adjustable implementation, evidence, and figure policy |
| `TODO_###/data/tables/aggregation-validation.json` | Source, grain, key, coverage, join, and calculation validation |
| `TODO_###/exp/figures/` and `TODO_###/data/figures/` | Plotting code and governed figure artifacts |

## Typical prompts

Create a TODO:

```text
Use $research-task-router to create a current-action TODO from [materials].
```

Initialize and show eligible starting paths:

```text
Use $research-task-router for TODO_001/TODO.md. Initialize todo_ready, resolve bounded project and data questions, and show every eligible rule.
```

Confirm and begin a target:

```text
Approve [rule_id].
```

Run figure review:

```text
Use $research-task-router for TODO_001/TODO.md. Produce the complete figure-review set with clear comparisons, uncertainty, and coverage, then present it for my feedback.
```

Produce final figures:

```text
Use $research-task-router for TODO_001/TODO.md. Implement my recorded figure feedback and deliver final exports with their integrity evidence.
```
