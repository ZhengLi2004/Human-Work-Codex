# Research Task System

Research Task System turns one complete research TODO into a rule-driven Work/Codex workflow with explicit human decisions.

~~~text
Research TODO
    ↓
Current-action implementation TODO
    ↓
Fingerprint and initialize task-state YAML
    ↓
Evaluate and human-confirm one eligible rule path
    ↓
Execute only the recorded state
    ↓
Preserve complete evidence and validate aggregation
    ↓
Curate tables and prepare draft figures
    ↓
Researcher reviews every draft and its coverage
    ↓
Produce and validate final figures
    ↓
Finish, rework, redesign, or stop by an eligible rule path
~~~

## Repository layout

~~~text
.
├── .codex-plugin/plugin.json
├── .agents/plugins/marketplace.json
├── agents/openai.yaml
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
│   └── workflow/
├── requirements.txt
├── AGENTS.md
└── README.md
~~~

## Path 1: clone and prepare the environment

Clone the current remote and enter the repository:

~~~bash
git clone https://github.com/ZhengLi2004/Human-Work-Codex.git
cd Human-Work-Codex
~~~

Create an isolated Python environment and install the plotting and notebook-validation dependencies.

macOS or Linux:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
~~~

Windows PowerShell:

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
~~~

MATLAB remains the default production environment for non-plotting computation. Check the installed release and licensed toolboxes separately:

~~~bash
matlab -batch "disp(version); ver"
~~~

The TODO and existing project code determine which toolboxes are required. Install MATLAB and its required toolboxes separately from the Python environment.

## Import into Codex

After Path 1, choose Path 2 or Path 3. The Plugin path is recommended because it preserves the packaged interface and makes the Skills available outside this repository.

### Path 2: recommended local Plugin

1. Open the cloned repository as the workspace in Codex desktop.
2. Restart Codex so it reloads the local marketplace metadata.
3. Open the Plugins view, select the **Research Task System (Local)** marketplace, and install **Research Task System**.
4. Start a new task in the repository. A new task is required after Plugin installation so the Plugin Skills and the repository-root AGENTS.md are loaded together.

The equivalent Codex CLI commands, run from the repository root, are:

~~~bash
codex plugin marketplace add .
codex plugin add research-task-system@research-task-system-local
~~~

Use this Plugin path for Codex desktop and Codex CLI. For a Codex IDE extension, use the repo-scoped Skills path below.

### Path 3: repository-scoped Skills without Plugin installation

Codex discovers repository Skills under **.agents/skills**. This repository keeps the canonical files under **skills/**, so create a link rather than copying them.

macOS or Linux:

~~~bash
ln -s ../skills .agents/skills
~~~

Windows PowerShell:

~~~powershell
$skillTarget = (Resolve-Path .\skills).Path
New-Item -ItemType Junction -Path .\.agents\skills -Target $skillTarget
~~~

Then restart Codex or start a new task in the repository. The repository-root AGENTS.md is discovered automatically from the Git-root instruction chain; the junction adds only the repo-scoped Skills.

### Fallback: repository instructions only

Opening the repository in Codex loads `AGENTS.md` by itself. Install the Plugin or expose the repo-scoped Skills to add the reusable workflows; use the `AGENTS.md`-only setup for inspection.

## Verify the import

In a new Codex task:

1. Run **/skills** and confirm that **research-task-router** is available.
2. Use this read-only prompt:

   ~~~text
   Summarize the active repository AGENTS.md instructions and name the Research Task System entry Skill. Do not modify files or external state.
   ~~~

3. For a Plugin installation, list the local marketplace:

   ~~~bash
   codex plugin list --marketplace research-task-system-local
   ~~~

The entry point for broad requests is **$research-task-router**.

Current official references:

- [Codex Plugins](https://developers.openai.com/codex/plugins)
- [Build skills](https://developers.openai.com/codex/skills)
- [AGENTS.md guidance](https://developers.openai.com/codex/guides/agents-md)
- [Plugin packaging](https://developers.openai.com/plugins/build/plugins)

## Artifact responsibilities

| File or directory | Purpose |
|---|---|
| TODO.md | Complete current-action scientific specification and output path references |
| results/{todo_id}/task-state.yaml | Current lifecycle state, TODO fingerprint, evaluations, approvals, and immutable transition history |
| .research/workflow/state-machine.yaml | Reusable predicates, states, and transition rules |
| .research/policy.yaml | Adjustable resource, storage, validation, and figure policy |
| aggregation-validation.json | Source, grain, key, coverage, join, calculation, and publication-safety checks for aggregate tables |
| SKILL.md | Reusable workflow, guardrails, and output contract |
| AGENTS.md | Permanent scientific and execution governance |
| results/{todo_id}/ | State, logs, checkpoints, immutable raw outputs, tables, notebooks, and figures |

## Typical prompts

Create a TODO:

~~~text
Use $research-task-router to create a current-action TODO from [materials].
Save it as TODO/[name].md.
~~~

Initialize state and evaluate without applying:

~~~text
Use $research-task-router for TODO/[name].md.
Initialize state and evaluate transitions. Do not apply.
~~~

Execute the recorded state:

~~~text
Use $research-task-router for TODO/[name].md.
Execute only the recorded current state.
~~~

Confirm and execute an eligible transition:

~~~text
Approve [rule_id] and execute the target state.
~~~

Prepare draft figures after the approved transition to work_postprocessing:

~~~text
Use $research-task-router for TODO/[name].md.
Curate the validated complete tables and run $research-figure-production in Planning mode.
~~~

Review drafts after the approved transition to figure_review:

~~~text
Use $research-task-router for TODO/[name].md.
Present every draft figure and its complete condition coverage, then wait for my recommendations.
~~~

Produce final figures only after the approved transition to figure_production:

~~~text
Use $research-task-router for TODO/[name].md.
Implement my recorded figure recommendations and run the final figure and Notebook integrity checks.
~~~
