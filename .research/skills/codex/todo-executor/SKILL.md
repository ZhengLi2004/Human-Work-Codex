# Skill: Codex — TODO Executor

## 目标

把 Work 编制且经人类批准的一个 TODO 作为一次持续执行调用完成。Codex 在阶段、方案分歧和长时运行处直接阻塞等待人类；得到人类回复后在原上下文继续。整个 TODO 完成前不返回 Work。

## 启动输入

依次读取：

1. `AGENTS.md`；
2. 人类研究报告的相关章节；
3. 当前 `TODO.md`；
4. 当前 `workflow.yaml`；
5. 静态 `pipeline.yaml`；
6. 当前阶段 Skill；
7. `human-review-gate`、`agile-testing`、`evidence-aggregation`；
8. 需要时的 `batch-execution`。

开始前必须满足：

- TODO 已由人类批准；
- `codex_call.approved_scope` 明确；
- 当前阶段和装填 Skill 一致；
- Work 已完成第 1-2 节；
- 不存在未解决的研究语义冲突。

## 持续执行循环

```text
while Codex 执行未完成：
    装填当前阶段 Skill
    将批准范围拆成最小可工作的纵向切片
    实现一个切片
    运行该切片最小充分的风险驱动测试
    继续直至完成当前批准范围

    若产生实验数据：
        保存不可变原始数据
        生成 runs、aggregate_full、aggregation_manifest
        校验全部组合和重复

    向 TODO 追加 T-xx 与 E-xx
    生成 CODEX_STAGE_REVIEW
    提出 Codex 初始建议和精确下一范围
    直接阻塞等待人类

    收到人类决定后：
        忠实写入 workflow 与阶段审查包
        若继续或转换阶段：重建 Codex 自己的 loadout 并原地恢复
        若要求补证：只执行批准的补证范围
        若批准完成：生成 CODEX_EXECUTION_BUNDLE 并返回 Work
        若停止：保存现有证据并返回 Work
```

## 直接人类交互

Codex 的阶段建议必须包含：

- 已完成事实；
- 测试与证据；
- 缺失和异常；
- 自己的初始判断；
- 推荐动作；
- 下一步的精确边界；
- 需要人类决定的事项。

Codex 不得默认建议被批准，也不得要求 Work 转译或确认。

## TODO 更新权限

Codex 只可：

- 追加第 3 节 `T-xx` 技术事实；
- 追加第 4 节 `E-xx` 证据引用；
- 更新顶部状态字段；
- 在人类批准后记录批准的实质变化。

Codex 不得重写 Work 在第 1-2 节定义的研究问题、技术手段、变量、控制和完成证据。

## 长时运行

预计超过 30 分钟时：

1. 完成与风险相称的自动化测试；
2. 完成一个组合、一次重复的端到端预检；
3. 验证 checkpoint、进度、日志和聚合；
4. 向人类提交一行命令与资源说明；
5. 工作流进入等待人类运行状态；
6. 人类运行后在同一 Codex 调用中继续。

## 返回 Work 的完成条件

只有人类批准完成或停止时，才返回 Work。返回前必须：

- TODO 已引用全部阶段证据；
- 所有实验指标均有完整聚合或明确不完整状态；
- `aggregate_full` 保留全部计划组合；
- 所有阶段审查和人类决定可追溯；
- 已生成 `CODEX_EXECUTION_BUNDLE.md`。
