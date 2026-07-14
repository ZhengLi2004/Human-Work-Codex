# Entry Prompts

人类研究报告没有固定模板，直接作为上位输入。

## 1. Work：由人类研究报告创建 TODO

```text
你负责把人类提供的完整研究报告忠实映射为当前项目中的科研 TODO，不重写研究问题，不实现代码。

读取：
1. [人类研究报告路径]
2. [项目根目录、已有结果和相关任务]
3. AGENTS.md
4. .research/templates/TODO.md
5. .research/workflow/task.workflow.yaml
6. .research/skills/work/research-report-to-todos/SKILL.md

完成项目对象映射、技术手段衔接、任务变量、控制变量、指标、重复要求、完成证据和 TODO 拆分。状态设为 awaiting_human_todo_approval。人类批准后，把整个 TODO dispatch 给 Codex。
```

## 2. Codex：开始并持续执行整个 TODO

```text
你负责在一次持续调用中执行已经由人类批准的整个 TODO。

读取：
1. AGENTS.md
2. [人类研究报告相关章节]
3. [TODO 路径]
4. [workflow 路径]
5. .research/workflow/pipeline.yaml
6. .research/skills/codex/todo-executor/SKILL.md
7. 当前阶段 Skill 与能力 Skills

以最小纵向切片实现，并采用风险驱动、测试金字塔式的敏捷测试。每个阶段完成后，若产生实验数据，立即生成 runs、aggregate_full 和 aggregation_manifest，并把磁盘引用追加到 TODO。然后直接向人类提交 CODEX_STAGE_REVIEW、给出初始建议并等待审批。不要返回 Work；得到人类决定后在同一执行上下文继续。只有人类批准完成整个 TODO 时，生成 CODEX_EXECUTION_BUNDLE 并返回 Work。
```

## 3. Codex：阶段审查后恢复

```text
人类已经直接回复 Codex 的阶段审查请求。

读取当前会话中的人类决定、CODEX_STAGE_REVIEW、TODO 和 workflow。忠实记录决定与批准范围，保留全部历史证据；根据批准的目标阶段重建 Codex loadout，并在同一 TODO 执行中继续。若人类批准完成，生成 Codex Execution Bundle 并返回 Work。
```

## 4. Codex：向人类交付超过 30 分钟的运行

```text
当前运行预计超过 30 分钟。先完成相关快速测试、一个组合一次重复的正式配置预检、checkpoint 恢复检查、日志与聚合校验。然后直接向人类提供一行命令、预计时间和资源、checkpoint、日志、结果位置和完成判据，并在 Codex 执行内部等待。人类运行后继续核验和聚合。
```

## 5. Work：Codex 返回后整理论文候选表

```text
Codex 已完成整个 TODO，并返回 CODEX_EXECUTION_BUNDLE。

读取：
1. TODO 与 workflow
2. Codex Execution Bundle
3. 所有 runs、aggregate_full 和 aggregation_manifest
4. .research/templates/RESULT_PACKAGE.md
5. .research/skills/work/publication-table-curation/SKILL.md

先验证完整组合、重复、控制条件和追踪关系。每个 aggregate_full 单独生成一个行数完全相同的 publication_table；只做列选择、改名、枚举可读化、排序和显示舍入，不得筛选、合并或重新聚合行。生成列变换清单、Result Package，并更新 TODO 第 5 节。不要替人类分析机制或撰写实验报告。
```

## 6. Work：读取人类实验报告并评估下一 TODO

```text
人类已经基于 Result Package 完成实验报告。

读取人类实验报告、原始研究报告、当前 TODO、完整聚合表、publication_table、列变换清单和 .research/skills/work/post-report-assessment/SKILL.md。

以人类报告为科学解释来源，评估继续相同实验的预期信息增益。可以建议继续、定向补充、先重设计、证据充分而停止、信息增益过低而停止，或提出独立候选新现象实验。任何下一 TODO 都只作为建议并等待人类批准。
```
