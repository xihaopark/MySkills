# 科研 Workflow Agent 设计问题

创建日期：2026-07-05

这份文件记录问题，而不是结论。修改 runtime 或 public documentation 之前，先用它做设计检查。

## 1. 实际的 Loop 单元是什么？

候选：

- 整个 workflow run：从 `/ERcoding:start` 到 Core6。
- 每个 core：Core1、Core2、Core3、Core4、Core5、Core6 分别作为 loop。
- 每个 decision：每个 gate 或 selected result branch 作为 loop。

工作假设：在 whole-run controller 内使用 **per-core loop units**。

必需 loop phases：

1. 检索 reviewed wiki context。
2. 组装 core input 和 prior artifacts。
3. 运行 deterministic core。
4. 收集 artifacts / manifests。
5. audit 和 review。
6. 创建用户 attention packet。
7. 如果需要人类决策，则暂停。
8. 持久化 decision 和 selected result context。
9. 写入 learning candidates。

## 2. Core3-6 必须在哪里停下来让用户介入？

Core3：

- 使用 exposure metric definitions 作为 governed axes 之前；
- 接受 posthoc / source mapping 之前；
- BLQ / LLOQ policy 影响 metrics 之前；
- unresolved source dependency 被当成 available 之前。

Core4：

- 生成大批 ER plot batches 之前；
- 锁定 ER question matrix 之前；
- 把 model readiness 标记为 user-accepted 之前。

Core5：

- interpretation boundary 不清晰时，拟合或报告非平凡模型之前；
- 产生 dose-adjusted claims 之前；
- 提升 exploratory results 之前。

Core6：

- 声称 package review-ready 之前；
- selected results 进入下游 context 之前；
- 任何输出被表述为 customer-ready 之前。

## 3. 用户应该看到什么？

默认不展示 raw debug。每张 card 应显示：

- 当前 core 和 run id；
- agent 发现了什么；
- 精确 evidence files；
- 需要什么 decision；
- options 和 downstream consequences；
- 在安全时给出 recommended option；
- unresolved risks；
- resume behavior。

## 4. Wiki 影响执行应该是什么样？

一次 run 应能回答：

- 检索了哪些 wiki pages？
- 为什么检索它们？
- 哪些 claims 或 decisions 受它们影响？
- 哪些 pages 被忽略或判定 stale？
- 提出了哪些新 candidates？
- 用户 approve、edit 还是 reject 了 candidates？

## 5. 最小稳定架构是什么？

避免复杂 multi-agent 产品。优先使用：

- Workflow control 作为 orchestrator。
- Deterministic runner 执行确定性逻辑。
- Data Auditor / Review Agent 作为 checker。
- Human decision surface 承载人类决策。
- Wiki retrieval 作为有边界上下文。
- `<run evidence root>` 作为 event / artifact evidence root。

## 6. 1.0 明确不做什么？

- 自动修改 skills；
- 自动修改 gate registry；
- 自动提升 wiki 内容；
- 自主生成 customer-facing claims；
- group-chat multi-agent run execution；
- uncontrolled experimental artifacts 进入正式 evidence chain。

## 7. 哪些地方需要新 contract？

候选 contracts：

- `core_attention_packet.schema.json`
- `wiki_retrieval_log.schema.json`
- `learning_candidate.schema.json`
- `human_decision_gate.schema.json`
- `selected_result_context.schema.json`
- `core_completion_predicate.schema.json`

## 8. 第一个实验

在全新 run 中跑一次 mock Core3-6：

- 启用 wiki retrieval；
- 强制一个 Core3 decision card；
- 一个 Core4 ER pair selection card；
- 一个 Core5 exploratory interpretation boundary card；
- 一个 Core6 review readiness card；
- 生成 learning candidates，但不自动 approve。

Acceptance 应基于：用户是否能在不阅读 raw CSV 或 debug logs 的情况下理解并介入。

## 9. Claude Science 启发的检查

对每个 Core3-6 设计，询问：

- Artifact-first：用户实际拿到的 durable artifact 是什么？
- Provenance：能否追踪到 source data、code、gate decisions、wiki context 和 audits？
- Grounding：agent 是计算/查询/读取了证据，还是从记忆里推断？
- Purpose-shaped role：哪个 role 被允许做这件事？哪些工具被刻意禁用？
- Progressive disclosure：加载了哪些 wiki / skill context？为什么只加载这些？
- Measured self-extension：如果这次 run 教会了我们什么，它是 reviewed wiki candidate、eval case，还是 code change proposal？
