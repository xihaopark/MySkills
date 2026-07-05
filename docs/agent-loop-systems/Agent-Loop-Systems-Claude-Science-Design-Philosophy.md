# 笔记 06：Claude Science 设计哲学

来源：`Claude-Science-Full-Reference-ZH.md`

这篇笔记把用户补充的 Claude Science 长文阅读提炼成科研 workflow agent 的设计原则。它并不把 Claude Science 当成目标产品，而是把它作为科学 agent 行为的参考架构（reference architecture）。

## 核心框架

原文中最有价值的一句话是：

> 把 agent 当成一个需要被“校准”的科学仪器，而不是一个需要被“命令”的下属。

对科研 workflow agent 来说，这意味着 Core3-6 不能靠更严格的 prompt 命令来解决。我们要校准的是整个 loop：

- agent 能看到什么证据；
- 它必须产出什么 artifacts；
- 它不能跨越哪些边界；
- 哪些用户决策是必需的；
- 哪些 evals 能证明循环在变好。

## 七条可迁移原则

### 1. Artifact-First

Claude Science 把 artifacts 当成主要产品，chat 只是连接层。

可复用映射：

- `<run evidence root>` 应继续作为 evidence root。
- Core3-6 应产出用户可读的 attention packets，并链接到 artifacts。
- Main conversation 应总结和导航 artifacts，而不是自己成为 artifact。

设计含义：

- 每张 Core3-6 card 都应指向具体 CSV / PNG / manifest / review files。
- “Selected result” 应是 artifact-backed context object，而不是复制出来的聊天文本。

### 2. 声明式计算 / 声明式工作流（Declarative Compute / Workflow）

Claude Science 使用声明式环境规格，把 job 需要什么与各后端如何运行分离。

可复用映射：

- ER workflow specs 应描述临床/统计意图和 source mappings。
- Runner code 应依据 specs 执行，而不是写死 study logic。
- Core3-6 gates 应修改显式 spec / decision state，而不是隐藏 prompt context。

设计含义：

- Gate decisions 应成为下游 runner 会消费的 typed state。
- 未来 Core3-6 改进应优先扩展 specs，而不是添加 ad hoc prompts。

### 3. Provenance by Construction

原文强调 execution logs、artifact versions、dependency DAGs、checksums 和 environment snapshots。

可复用映射：

- 我们已经有 artifact lanes、pipeline status、data auditor、gate records 和 `run evidence roots`。
- 当前缺口是用户可见 provenance：用户应能在不读 raw debug 的情况下理解 lineage。

设计含义：

- Core3-6 应增加紧凑 lineage summaries：
  - 使用了哪些 source files；
  - 消费了哪些 upstream artifacts；
  - 写出了哪些 outputs；
  - 哪些 gates / audits 影响了结果；
  - 仍有哪些 unresolved dependencies。

### 4. Grounding Over Generation

Claude Science 的原则是查询/计算权威来源，而不是从模型记忆中编答案。

可复用映射：

- Core3-6 不能从模型记忆推断临床/统计决策。
- 它应使用 source data、specs、prior artifacts、reviewed wiki 和 explicit gates。

设计含义：

- Core3 exposure metric 或 Core5 interpretation 必须引用支持它的 spec / gate / source artifact。
- 如果 source 不可用，应写 blocked manifest，而不是生成 synthetic placeholder claims。

### 5. Purpose-Shaped Agents

原文强调通过移除无关工具和能力来塑造 agent。

可复用映射：

- 不要做一个全能 ER agent。
- 使用 purpose-shaped roles：
  - Runner：执行确定性 core。
  - Auditor：检查 artifact / source / gate quality。
  - Explainer：生成 human decision packet。
  - Wiki Curator：提出 learning candidates，但永不自动 approve。

设计含义：

- Core3-6 不应默认使用 group chat。
- Review / audit roles 应有受限权限和清晰 output schemas。

### 6. Progressive Disclosure

Claude Science 让许多 skills 可用，但不会一次性把它们全部塞进上下文。

可复用映射：

- Reviewed wiki 应选择性检索成有边界的 attention packet。
- Skills 保存稳定 procedure；Wiki 提供 reviewed project knowledge。

设计含义：

- Wiki retrieval logs 应说明为什么检索某页。
- Agent 只应接收当前 core 所需的 distilled wiki context。

### 7. Measured Self-Extension

原文关于自进化最强的教训不是“自动写新 skills”，而是可测量的改进：

- 生成候选；
- 测试它；
- 对比结果；
- review regression risk；
- 然后才发布。

可复用映射：

- Runtime 可以写 learning candidates。
- 人类批准 wiki updates。
- Skills / registry / runner updates 需要显式开发流程和测试。

设计含义：

- Wiki learning 与 eval learning 应分开：
  - Wiki 记录 reviewed knowledge；
  - Eval cases 记录必须保持的行为。
- Learning candidate 只有带 source refs 和 review status 才能提升。

## 与当前状态的张力

当前 Core3-6 happy path 仍偏 automode。Claude Science 阅读推动我们走向：

- 更少静默自动化；
- 更多 artifact-backed user visibility；
- 更清晰的 decision boundaries；
- 更强的 provenance summaries；
- 真正影响执行的 reviewed memory；
- 由 eval 支撑的 self-evolution，而不是 runtime unchecked learning。

## 由此产生的设计问题

- 每个 Core3-6 输出是否都应包装为带 provenance 和 decision boundary 的 artifact card？
- Core3-6 runner 输出是否应包含 dependency DAG 或简化 lineage table？
- Wiki retrieval 是否应作为正式 source input 出现在 Core6 review package？
- “Agent learning” 是否总是产出两个 artifacts：wiki candidate 和 eval candidate？
- 每个 role 的 allowed tools 是否应作为 1.0 稳定性计划的一部分记录？
