# 笔记 01：循环与执行框架（Loop / Harness）

## 核心模式

高信号资料基本都收敛到一个分层视角：

1. 模型（model）：推理并决定下一步尝试什么。
2. 执行框架（harness）：组装上下文、执行工具、施加约束、持久化状态。
3. 工具与执行手（tools / hands）：执行外部动作。
4. 会话或运行日志（session / run log）：存在于模型上下文之外的持久事件记录。
5. 验证器或评估器（verification / evaluator）：决定循环应该继续、停止、重试还是升级。

最重要的结论是：当模型能力足够时，**agent 质量主要取决于 harness 质量**。

## Loop 与 Workflow 的区别

Anthropic 的区分很有用：

- 工作流（workflow）：开发者定义控制流。
- Agent：模型在有边界的循环中决定控制流。

对于科研 workflow agent，Core1-6 应该更接近 workflow，而不是开放式 agent。Agent 层适合决定表达方式、澄清问题和后续探索；临床/统计制品流水线应保持确定性、可审计。

## 最小循环分支

OpenAI SDK、框架解释文章和社区实践中反复出现的循环分支包括：

- 最终输出（final output）：无需更多工具工作，输出形态已经满足要求。
- 工具调用（tool call）：执行工具，追加结果，继续循环。
- 任务移交（handoff）：切换到专家或 worker，继续循环。
- 中断（interruption）：暂停等待人工审批或输入，并持久化状态。
- 失败或升级（failure / escalation）：带证据停止，并给出下一步动作。

可复用映射：

- `final_output` -> step report、selected result、Core6 review summary。
- `tool_call` -> 确定性 runner、R scripts、文件读取器、artifact scanner。
- `handoff` -> review / auditor 阶段，而不是无约束群聊。
- `interruption` -> Claude Code built-in popup gate。
- `failure/escalation` -> typed gate 的 `blocked` / `needs_review` 加 action item。

## 长运行 Harness 的实践

Anthropic 和 Cursor 的实践给出几条稳定经验：

- 需要初始化阶段（initializer / setup），写清项目状态和“完成”的定义。
- 进度必须存到上下文之外，例如 progress file、scratchpad、run log、checklist。
- 限制循环次数、耗时和 effort。
- 当 agent 可能修改文件时，使用 worktree 或 run isolation。
- “完成”必须由 artifacts / tests 可检查，而不是模型自信。

可复用映射：

- `<run evidence root>` 应作为正式持久运行根目录。
- 当前 Core1-6 happy path 应增加每个 core 的 progress / checklist 记录，而不只是 `pipeline_status.csv`。
- Core3-6 不应从用户视角静默 automode，需要可见 checkpoint。

## Orchestrator-Workers

Anthropic 多 agent 研究系统的经验与此高度相关：

- 子任务必须有 objective、output format、tool/source guidance 和边界。
- effort 应随任务复杂度伸缩。
- 工具描述和工具选择启发式会显著影响结果。

可复用映射：

- 避免 Core3-6 采用扁平 multi-agent chat。
- 使用一个 orchestrator / control surface，加少数有边界的 worker role：
  - Runner：执行确定性 core。
  - Auditor：检查 schema、data 和 gate。
  - Explainer：生成面向用户的 attention packet。
  - 可选 Reviewer：交付前做对抗式 review。

## 开放问题

- Core3-6 是否都需要正式的 `StepControl` 状态机文件？
- Runner 是否应在每个 core 后输出机器可读的 `next_required_user_decision.json`？
- “selected result as context” 应该建模为 loop state transition，而不是 UI-only state 吗？
