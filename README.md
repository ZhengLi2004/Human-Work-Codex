# Research Task System v3

该仓库描述下述研究逻辑：

```text
人类：宏观研究
  完整研究报告、研究问题、研究假设、初步研究方案
        ↓
Work：抽象与实现衔接
  结合项目事实拆分 TODO、定义技术边界、变量与证据要求
        ↓
Codex：实现与实验
  在一次持续的 TODO 执行调用中完成各阶段；阶段之间阻塞并等待人类审查
        ↓
Work：结果整理
  在 Codex 返回后校验并整理数据
        ↓
人类：科学报告
  观察数据、分析规律、总结机制并撰写实验报告
```

以人类提交的完整研究报告为研究设计，Work 和 Codex 负责忠实落地、形成可审计证据。

## Codex 运行模型

```text
Work.dispatch(TODO)
└── Codex.execute(TODO)
    ├── Exploration
    ├── await human_review()     # Codex 直接给出事实、建议并阻塞
    ├── Development
    ├── await human_review()
    ├── Pilot
    ├── await human_review()
    ├── Confirmation
    ├── await human_review()
    └── return execution_bundle  # 整个 TODO 完成后才返回 Work
```

Codex 内部分为 Exploration、Development、Pilot 和 Confirmation 四个阶段。

## 两类人类在环

### 1. Codex 执行内部

在 Codex 的各个内部阶段中，模型进行代码开发后需根据风险安排测试。若此过程中产生了实验指标，则需要立即保存原始数据与聚合后的数据，并将文件在磁盘上的位置引用添加到 TODO 中。而后，向人类提交阶段事实、已知问题、Codex 的初始建议和下一步精确范围。Codex 在这之后等待人类批准，并在得到批准后继续执行任务。

此外，若代码运行预计超过 30 分钟，Codex 将单行的运行脚本交给人类并阻塞。在人类运行完成后，其进行数据核验、聚合和审查。

### 2. TODO 间

Codex 完成整个 TODO 并返回 Work 后，Work 校验其产生数据的完整性并整理，而后将结果移交给人类。人类观察数据、分析规律、总结机制并撰写实验报告，Work 根据人类报告评估是否值得继续进行同类实验，并在获得批准的情况下撰写后续 TODO。

## 数据证据层级

```text
不可变原始数据
→ 原始结果：每个独立运行一行
→ 聚合结果：每个计划任务变量组合恰好一行，基于同一控制条件下的多次重复
→ 发表结果：Work 保持行数不变，只做论文展示所需的列级整理
```

## 测试模型

采取基于科学错误风险驱动的测试模型：

- Exploration 使用最小探针、断言、特征测试和人工可判定样例；
- Development 对核心算法使用单元、性质、差分或变形测试，对接口使用契约与集成测试；
- Pilot 在一个组合上完成端到端冒烟测试后再执行小规模完整网格；
- Confirmation 执行冻结规格预检、关键回归、checkpoint 恢复与正式入口验证；
- 缺陷修复必须增加能够阻止同类错误复现的回归测试。

测试应在每个纵向切片后运行，阶段审查前运行当前阶段的最小充分套件。

## 目录

```text
AGENTS.md
.research/
├── ENTRYPOINTS.md
├── templates/
│   ├── TODO.md
│   ├── CODEX_STAGE_REVIEW.md
│   ├── CODEX_EXECUTION_BUNDLE.md
│   └── RESULT_PACKAGE.md
├── workflow/
│   ├── pipeline.yaml
│   └── task.workflow.yaml
└── skills/
    ├── codex/
    │   ├── todo-executor/SKILL.md
    │   ├── exploration/SKILL.md
    │   ├── development/SKILL.md
    │   ├── pilot/SKILL.md
    │   ├── confirmation/SKILL.md
    │   └── ablation-diagnosis/SKILL.md
    ├── capabilities/
    │   ├── human-review-gate/SKILL.md
    │   ├── agile-testing/SKILL.md
    │   ├── evidence-aggregation/SKILL.md
    │   └── batch-execution/SKILL.md
    └── work/
        ├── research-report-to-todos/SKILL.md
        ├── publication-table-curation/SKILL.md
        └── post-report-assessment/SKILL.md
```

## 文件内容

- `AGENTS.md`：不可违反的角色边界、测试、资源、学术诚信和数据约束。
- `Skills`：某一角色或阶段如何工作。
- `workflow.yaml`：Codex 当前执行栈、阶段、阻塞点、人类决定和产物状态。
- `TODO.md`：研究任务、项目化技术手段、实际实现事实、实验结果引用和最终交接。
- `CODEX_STAGE_REVIEW.md`：Codex 阶段结束时直接提交给人类的审查材料。
- `CODEX_EXECUTION_BUNDLE.md`：整个 TODO 执行完成后，Codex 返回 Work 的事实性结果索引。
- `RESULT_PACKAGE.md`：Work 对表格做列级整理后提交给人类的结果包。
