# 笔记 03：验证、评估与可观测性（Verification / Evals / Observability）

## 核心模式

外部共识很明确：agent loop 会把瓶颈从“生成”转移到“验证”。

循环系统必须回答：

- 尝试完成的目标是什么？
- 使用了哪些工具或动作？
- 产出了哪些 artifacts？
- 哪些检查通过或失败？
- 用户批准了什么？
- 还有什么被阻塞？
- “完成”的证据是什么？

## 验证层次

科研 workflow agent 推荐使用多层验证：

1. Schema / contract tests：artifact 名称、字段、状态枚举、run-id 隔离。
2. Data audit：source dependency、data quality、denominator、missingness、provenance。
3. Visual / figure audit：manifest、非空输出、style / semantic contract。
4. Model audit：ready / skip status、minimum event threshold、interpretation boundary。
5. User-facing review：简洁 attention packet，而不是 raw debug。
6. End-to-end eval：重复 mock run，对比 run structure、gates、selected result、wiki retrieval。

## Harness-First Verification

Datadog 的 harness-first 观点很有价值：

- Harness 应快速、自动地完成验证。
- 人工 review 应聚焦高价值判断，而不是扫描所有 raw event。
- 当 test harness 假设与真实生产行为分叉时，telemetry / observability 负责闭环。

可复用映射：

- Core3-6 需要机器可验证的 step reports。
- Main conversation 默认隐藏 raw/system/tool debug。
- Raw events、tool invocations、snapshots 和 artifacts 必须可追溯。

## Evals 作为产品记忆

Anthropic 和 LangChain 都把 evals 视为生命周期资产：

- 从少量真实 use cases 开始。
- 把 manual testing 中有价值的失败加入 eval。
- 让 human reviewer 标注 traces / evals。
- 在改 prompts / tools / harness 之前看 eval delta。

可复用映射：

- 客户反馈应转化为 acceptance / eval cases。
- Core3-6 demo 失败应转成 tests 或 checklist rows。
- Wiki candidates 和 eval candidates 相关但不相同：
  - wiki 存 reviewed project knowledge；
  - evals 存必须持续成立的行为。

## 可观测性要求

每次正式 run 应保留：

- run id 和 display name，并保持二者分离；
- cwd / project root / plugin root；
- core start/end status；
- model / tool / handoff events，如果可用；
- file artifacts 和 manifests；
- gate request / decision；
- selected result context additions；
- wiki retrieval log；
- learning candidate log；
- audit / action item output。

## 开放问题

- Core3-6 是否都应输出紧凑的 `attention_packet.md` 和 `attention_packet.json`？
- 每个 core 的 “done” 是否应是 artifacts / gates / audits 上的 predicate，而不是脚本 exit code？
- Core6 是否不仅聚合 review gates，也聚合“用户可见的未解决决策”？
