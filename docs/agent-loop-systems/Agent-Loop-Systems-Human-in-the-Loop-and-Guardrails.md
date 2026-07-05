# 笔记 02：人工介入与护栏（HITL / Guardrails）

## 核心模式

高质量资料都认为：人工介入（human-in-the-loop, HITL）应实现为可持久化的中断（durable interrupt），而不是一句 prompt 指令“需要时询问用户”。

关键机制：

- 在明确位置暂停执行。
- 持久化当前状态。
- 向人展示小而结构化的 payload。
- 接收类型化决策，例如 approve / edit / reject / respond。
- 从同一个 run / thread state 恢复。
- 记录决策、选项文本和用户选择。

## 护栏分类

OpenAI 的分类可以很好地映射到科研 workflow agent：

- 输入护栏（input guardrails）：拦截或重路由不合适的初始请求。
- 工具护栏（tool guardrails）：围绕副作用校验工具输入/输出。
- 输出护栏（output guardrails）：校验系统最终给出的内容。
- 人工 review（human review）：在敏感或有后果的动作前暂停。

可复用映射：

- Core gates 不是 notice，而是 human review interrupt。
- Audit notices 可以保持 context-only，但不能伪装成 gate。
- Core3-6 中会影响解释的决策，应使用 typed popup gate。

## 哪些内容应该成为 Gate？

ER workflow 中的 gate 候选：

- Core3：
  - exposure metric definitions；
  - posthoc/source mapping；
  - BLQ/LLOQ 处理策略；
  - exposure windows；
  - observed vs modeled provenance。
- Core4：
  - ER question matrix；
  - endpoint family 和 exposure axis list；
  - plot batch approval；
  - model-readiness route。
- Core5：
  - model family；
  - minimum event threshold；
  - dose adjustment；
  - censoring / TTE rules；
  - interpretation level。
- Core6：
  - readiness status；
  - must-resolve actions；
  - selected results 是否进入后续上下文。
- Wiki：
  - 学习候选进入 reviewed wiki 前，需要 approve / reject / edit。

## 界面形态

最好的 HITL payload 不是完整 transcript，而应包含：

- decision title；
- 为什么这个决策重要；
- 当前证据；
- 选项及精确 option text；
- 在安全时给出 recommended option；
- 对下游 core 的影响；
- 指向 source artifacts 的链接；
- free-form comment；
- resume behavior。

## 需要避免的失败模式

- 副作用已经发生后才请求 approval。
- 等待用户输入时丢失状态。
- 不记录用户选择的精确 option text。
- 把巨大 raw CSV / debug log 放进用户 gate。
- 在临床/统计解释中把“用户未回答”当作 implicit approval。
- 在没有 run-scoped record 的情况下跨 run 复用 gate decision。

## 开放问题

- Core3-6 gates 是否应使用 Core1 data cutoff 同一类 typed schema？
- 每个 gate 是否都写 `gate_request.json` 和 `gate_decision.jsonl`？
- UI 是否需要区分 “approve for this run only” 和 “approve and propose wiki memory”？
