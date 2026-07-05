# 笔记 04：记忆、学习与 Wiki（Memory / Learning / Wiki）

## 核心模式

外部资料反复区分三个容易混淆的概念：

- 上下文（context）：模型当前能看到的内容。
- 记忆（memory）：可被检索进上下文的持久记录。
- 学习（learning）：决定哪些经验能成为可复用记忆或 eval signal 的审核流程。

Oracle 的 agent loop 文章有一个对科研 workflow agent 很重要的提醒：会话内看似“学习”，本质上是 retrieval，不是模型权重训练。1.0 阶段不应声称模型会自动学习，而应说系统会检索 reviewed memory，并提出新的 learning candidates。

## Skill Library 与 Wiki

Voyager 风格的 skill library 展示了可复用执行程序的复利能力。但 ER Agent 需要更强治理：

- Skills：稳定 procedure 与工具。
- Wiki：经审核的事实、决策、模式、已知坑、客户偏好和案例。
- Learning candidates：未经审核的运行观察。
- Evals：必须持续通过的行为案例。

科研 workflow agent 不应在 runtime 自动改 skills。Wiki 是更稳健的第一层自进化表面。

## Reviewed Wiki Retrieval

如果希望 Wiki “真的影响执行”，retrieval 必须进入 run loop：

1. 每个 core 开始前，检索与 core / study / scenario 相关的 reviewed wiki pages。
2. 注入有边界的 attention packet，而不是整页 Wiki。
3. 在 run-local evidence 中记录 retrieval。
4. 要求 runner / explainer 说明哪些 wiki items 影响了决策。
5. 运行结束产出新的 learning candidates。
6. 人工批准后，候选才进入 reviewed wiki。

## 记忆污染风险

社区反方观点很重要：

- Agent 会模仿 deprecated code 和 stale docs。
- 如果坏模式仍可见，循环会不断复活它们。
- Token-heavy loops 可能读取过多低价值上下文。
- 自动记忆会固化错误。

可复用缓解：

- Wiki 页面需要状态：`approved`、`deprecated`、`superseded`、`draft`。
- Retrieval 应优先读取 approved / current 页面，除非用户显式要求，否则避免 deprecated examples。
- 每个 learning candidate 都应包含 source refs 和 confidence。
- 用户应能看到、编辑、批准或拒绝 proposed memory。

## 候选 Wiki 页面类型

- `decisions/`：已接受的架构和 workflow 决策。
- `patterns/`：可复用实现或工作流模式。
- `pitfalls/`：已知失败模式和反模式。
- `customer-feedback/`：经审核的客户期望。
- `study-notes/`：study / scenario-specific observations。
- `demo-scripts/`：稳定 demo 路径和讲解词。
- `eval-cases/`：从产品知识链接到 tests / evals 的案例。

## 开放问题

- 个人 reviewed wiki 是否应作为 source of truth，项目运行时只使用派生副本或缓存？
- Wiki retrieval 在 Core3-6 稳定后是否应强制启用，还是仅在匹配页面存在时启用？
- 用户应在 Canvas、Claude popup，还是单独 review command 中批准学习？
- Approved wiki entries 是否需要 frontmatter 和 changelog 版本化？
