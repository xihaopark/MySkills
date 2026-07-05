# 资料索引：Agent Loop 系统

创建日期：2026-07-05

范围：英文社区和一手资料中关于 agent loop、harness 设计、人工介入（HITL）、护栏（guardrails）、评估（evals）、记忆（memory）和社区实践的讨论。这里按它们对科研 workflow agent 的设计价值分组。

## 高信号一手资料 / 厂商资料

### Local Reference - Claude Science Design Philosophy Reading

- URL: [Claude Science 长文参考](Claude-Science-Full-Reference-ZH.md)
- 类别：scientific-agent system design、artifact-first research agent architecture
- 为什么重要：这是一篇中文长文，把 Claude Science 拆解为一个科学计算 agent 平台。它对科研 workflow agent 很关键，因为它把 agent 视为需要校准的科学仪器，其输出应是 artifacts、provenance records 和 grounded computations，而不是聊天回答。
- 关键启发：
  - 把 agent 当成需要校准的仪器，而不是需要命令的下属。
  - 把 artifacts 作为一等输出，conversation 只是导航层。
  - Provenance 应通过系统结构自然产生，而不是事后解释。
  - 优先接权威数据源和工具，不依赖模型记忆生成。
  - 通过工具和能力边界塑造 purpose-shaped agents。
  - 使用 progressive disclosure，避免大型 skill library 压垮上下文。
  - 自扩展必须可测量、可 review、受 eval 支撑。
- 设计标签：`artifact_first`、`provenance_by_construction`、`grounding`、`purpose_shaped_agents`、`progressive_disclosure`、`self_extension`、`wiki`

### Anthropic - Building Effective Agents

- URL: https://www.anthropic.com/engineering/building-effective-agents
- 类别：agent architecture patterns
- 为什么重要：清晰区分 workflows 与 agents，并强调环境 ground truth、checkpoints、blockers 和 stopping conditions。
- 关键启发：
  - Agent 每一步都应观察真实工具或环境反馈。
  - 人类 feedback checkpoint 和 stopping condition 是一等控制。
  - 简单、可组合的模式通常优于复杂框架。
- 设计标签：`ground_truth`、`checkpoint`、`stop_condition`、`tool_design`、`Core3-6`

### Anthropic - How We Built Our Multi-Agent Research System

- URL: https://www.anthropic.com/engineering/multi-agent-research-system
- 类别：orchestrator-workers、research loops
- 为什么重要：直接对应深度研究和 source-backed analysis。
- 关键启发：
  - Lead agent 需要明确 delegation instructions、output formats、tool guidance 和 task boundaries。
  - 没有 scaling rules 时，agents 容易过度消耗 effort。
  - Tool descriptions 和 tool-selection heuristics 会实质影响结果。
- 设计标签：`orchestrator_workers`、`task_boundaries`、`source_backed_analysis`、`tool_semantics`

### Anthropic - Effective Harnesses for Long-Running Agents

- URL: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 类别：long-running coding harness
- 为什么重要：展示了通过 progress files、feature lists 和 environment setup 维持多会话 agent 连贯性的具体 harness。
- 关键启发：
  - 长运行任务需要 initializer / environment phase。
  - Feature / checklist artifacts 能避免过早宣称完成。
  - Progress state 必须存在于 context window 之外。
- 设计标签：`harness`、`progress_file`、`checklist`、`context_reset`

### Anthropic - Harness Design for Long-Running Application Development

- URL: https://www.anthropic.com/engineering/harness-design-long-running-apps
- 类别：planner-generator-evaluator architecture
- 为什么重要：描述 planner / generator / evaluator 三角色系统，并解释 evaluator criteria 为什么关键。
- 关键启发：
  - Generator-evaluator loops 能改进主观输出和可验证输出。
  - Criteria 的措辞会塑造输出行为。
  - 跨会话 structured artifacts 是可靠性的关键杠杆。
- 设计标签：`planner_runner_evaluator`、`review_agent`、`criteria`、`structured_handoff`

### Anthropic - Effective Context Engineering for AI Agents

- URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 类别：context engineering
- 为什么重要：科研 workflow agent 需要 reviewed wiki retrieval 和 attention packets，但不能让上下文失控。
- 关键启发：
  - 难点不是最大化上下文，而是选择高信号上下文。
  - Multi-agent design 在 subagents 返回 distilled summaries 时更有效。
  - Compaction、note-taking 和 subagents 适用于不同任务形态。
- 设计标签：`wiki_retrieval`、`attention_packet`、`context_budget`

### Anthropic - Writing Effective Tools for Agents

- URL: https://www.anthropic.com/engineering/writing-tools-for-agents
- 类别：tool design and tool evals
- 为什么重要：科研 workflow agent 的 tools / gates 必须为 agent consumption 设计，而不仅是人类 CLI。
- 关键启发：
  - Tool interface 与 prompt 一样重要。
  - 好工具有清晰 namespacing、有效 context returns、token-efficient outputs 和 evals。
  - Tool descriptions 可通过 agent failures 迭代改进。
- 设计标签：`tool_contract`、`gate_tooling`、`artifact_contract`

### Anthropic - Demystifying Evals for AI Agents

- URL: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- 类别：evals
- 为什么重要：Core3-6 应按 workflow behavior 和 evidence quality 评估，而不是只跑 unit tests。
- 关键启发：
  - Evals 能避免生产失败驱动的反应式修改造成回归。
  - Agent evals 更难，因为 agents 会用工具、改状态并跨 turn 适应。
  - Evaluation 应成为生命周期纪律，而不是一次性测试。
- 设计标签：`evals`、`contract_tests`、`workflow_evidence`

### Anthropic - Scaling Managed Agents: Decoupling the Brain From the Hands

- URL: https://www.anthropic.com/engineering/managed-agents
- 类别：durable agent infrastructure、sandbox separation
- 为什么重要：帮助区分 workflow control、runner / tools 和 durable session / run logs。
- 关键启发：
  - 分离 brain / harness、hands / tools / sandboxes 和 durable session event log。
  - Tool / sandbox failures 应通过标准 tool error paths 恢复。
  - Session logs 应存在于 model context window 之外。
- 设计标签：`event_log`、`session_log`、`sandbox`、`recoverability`、`run_evidence_roots`

### OpenAI - Running Agents

- URL: https://developers.openai.com/api/docs/guides/agents/running-agents
- 类别：agent loop runtime
- 为什么重要：给出简洁的形式化循环：model call、tool calls、handoff、final output，并强调 state strategy。
- 关键启发：
  - Tools、handoffs、approvals 和 streaming 都建立在核心 loop 之上。
  - 需要选择一种 conversation / state strategy，避免上下文重复。
  - 当需要 durable memory 或可恢复 approval flow 时，sessions 是默认选择。
- 设计标签：`agent_loop`、`session_strategy`、`handoff`、`state`

### OpenAI - Guardrails and Human Review

- URL: https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
- 类别：guardrails、HITL
- 为什么重要：可以直接映射到 Core gate design。
- 关键启发：
  - Guardrails 和 human review 决定 continue、pause 或 stop。
  - Input、output 和 tool guardrails 处理不同风险。
  - 在敏感动作或有后果的工具调用前，human review 是合适控制。
- 设计标签：`typed_gate`、`approval`、`pause_resume`、`side_effects`

### OpenAI - Integrations and Observability

- URL: https://developers.openai.com/api/docs/guides/agents/integrations-observability
- 类别：MCP、tracing
- 为什么重要：科研 workflow agent 需要可见 run traces，但不能把 raw debug 暴露到 main conversation。
- 关键启发：
  - 需要决定哪些外部 surface 进入 agent loop。
  - Runtime 应负责本地/私有 MCP 连接、过滤和 approvals。
  - Traces 应捕获 model calls、tools、handoffs、guardrails 和 custom spans。
- 设计标签：`tracing`、`MCP`、`observability`、`raw_events`

### LangGraph - Interrupts

- URL: https://docs.langchain.com/oss/python/langgraph/interrupts
- 类别：dynamic HITL interrupts
- 为什么重要：是 gate popup pause / resume 语义的优秀具体模型。
- 关键启发：
  - Interrupts 暂停执行、持久化 graph state，并用外部输入恢复。
  - Thread id 是 resume pointer。
  - Interrupt payload 应可 JSON serialize；interrupt 前副作用必须 idempotent。
- 设计标签：`interrupt`、`checkpoint`、`run_scoped_gate`、`resume`

### LangChain - Making It Easier to Build HITL Agents With Interrupt

- URL: https://www.langchain.com/blog/making-it-easier-to-build-human-in-the-loop-agents-with-interrupt
- 类别：HITL product pattern
- 为什么重要：解释 interrupt 如何替代生产中不可靠的 terminal `input()`。
- 关键启发：
  - Persistence 是 HITL 的基础。
  - 人可以 approve / reject、review / edit state、review tool calls，或参与多轮互动。
  - Interrupted threads 等待期间不应消耗资源。
- 设计标签：`human_review`、`edit_state`、`approval_card`

### Microsoft AutoGen - Reflection Pattern

- URL: https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/reflection.html
- 类别：reflection / reviewer loop
- 为什么重要：支持把 runner 和 reviewer 角色分开。
- 关键启发：
  - Reflection 使用 generator / reviewer loop 和结构化 message protocol。
  - Loop 在 approval 或 max iterations 时停止。
  - Message protocol 与 agent prompt 同样重要。
- 设计标签：`maker_checker`、`review_agent`、`message_protocol`

### Microsoft Azure Architecture Center - Agent Orchestration Patterns

- URL: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- 类别：orchestration patterns
- 为什么重要：提醒不要在确定性 workflow 足够时过度使用 group chat。
- 关键启发：
  - Group chat 适合 review、validation 和多学科讨论。
  - 确定性线性处理不适合用 group chat。
  - Agent 数量越多，控制复杂度越高；保持小而清晰。
- 设计标签：`orchestration_choice`、`multi_agent_limit`、`quality_control`

### AWS Prescriptive Guidance - Evaluator Reflect-Refine Loop

- URL: https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/evaluator-reflect-refine-loop-patterns.html
- 类别：evaluator loop
- 为什么重要：企业场景中对 generator / evaluator / refiner loop 和 retry limit 的简洁描述。
- 关键启发：
  - 循环应在 criteria 满足、approval 达成或 retry limit 触发时停止。
  - Evaluator 需要 rubrics 或 criteria。
  - Escalation 是有效终态。
- 设计标签：`retry_limit`、`criteria`、`escalation`

## Coding Agent 与 Loop Engineering 实践

### Addy Osmani - Loop Engineering

- URL: https://addyosmani.com/blog/loop-engineering/
- 类别：loop engineering overview
- 为什么重要：广泛传播的框架：把“反复提示 agent 的人”变成系统循环。
- 关键启发：
  - Loop engineering 用系统循环替代人工重复 prompt。
  - 有用的 loops 需要 automation、worktrees、skills、connectors、subagents 和 memory。
  - Memory 必须存在于单次 conversation 之外。
- 设计标签：`loop_engineering`、`memory`、`skills`、`connectors`

### Cursor - Best Practices for Coding With Agents

- URL: https://cursor.com/blog/agent-best-practices
- 类别：practical coding agent workflow
- 为什么重要：提供基于 hooks 的 long-running loop、max iteration cap 和 scratchpad 实践。
- 关键启发：
  - Skills 封装 domain knowledge 和 reusable workflows。
  - Long-running loops 在目标可验证时效果最好。
  - Hooks 可让 loop 持续运行，直到 scratchpad 标记 done 或 iteration cap 触发。
- 设计标签：`skills`、`scratchpad`、`max_iterations`、`verifiable_goal`

### Cursor - Scaling Long-Running Autonomous Coding

- URL: https://cursor.com/blog/scaling-agents
- 类别：multi-agent coordination at scale
- 为什么重要：来自大量并发 agents 的真实失败模式。
- 关键启发：
  - 共享文件自协调和 locks 会变成脆弱瓶颈。
  - Planner / worker 设计比扁平 peer coordination 更稳定。
  - 大规模并行带来的协调复杂度增长快于生产力增长。
- 设计标签：`planner_worker`、`coordination`、`avoid_flat_multi_agent`

### Steve Kinney - The Anatomy of an Agent Loop

- URL: https://stevekinney.com/writing/agent-loops
- 类别：technical explainer
- 为什么重要：用简单方式解释 agent loop 和停止分支。
- 关键启发：
  - Agent loop 基本上是 reason / act / observe / repeat。
  - 框架最终都收敛到 final output、handoff、run again 和 interruption 等分支。
  - Max turns 和 interruption 是核心 loop controls。
- 设计标签：`loop_anatomy`、`interruption`、`max_turns`

### Oracle Developers - The Agent Loop Decoded

- URL: https://blogs.oracle.com/developers/the-agent-loop-decoded-three-levels-every-agent-engineer-must-know
- 类别：harness vs model、memory levels
- 为什么重要：提供区分 model、harness、memory 和 stopping conditions 的语言。
- 关键启发：
  - 大部分 agent engineering 工作发生在 harness，而不是 model。
  - Stopping 必须包括 goal-completion checks、iteration caps、wall-clock timeouts、unrecoverable errors 和 repeated-action detection。
  - 会话内表面上的学习是 retrieval，不是 model-weight learning。
- 设计标签：`harness`、`stop_conditions`、`memory_aware_agent`、`wiki`

### Firecrawl - Loop Engineering

- URL: https://www.firecrawl.dev/blog/loop-engineering
- 类别：practitioner overview
- 为什么重要：把 loop engineering 定义为处理 discovery、planning、execution、verification 和 iteration 的程序。
- 关键启发：
  - Model 成为 loop 内部的 subroutine。
  - Loop 必须有 schedule / trigger 和 stopping condition。
  - Prompting 仍然存在，但位置变成系统设计的一部分。
- 设计标签：`model_as_subroutine`、`schedule`、`verification`

### Datadog - Closing the Verification Loop

- URL: https://www.datadoghq.com/blog/ai/harness-first-agents/
- 类别：harness-first verification、observability
- 为什么重要：强调 verification quality 决定 agent quality。
- 关键启发：
  - 强 harness 让 iteration 便宜；弱 harness 不能靠更好模型或更多人工 review 修好。
  - Fast automated checks 应承担人无法规模化完成的检查。
  - Production telemetry 在模型化行为偏离现实时负责闭环。
- 设计标签：`verification_loop`、`observability`、`artifact_audit`、`telemetry`

## 学术基础

### ReAct - Synergizing Reasoning and Acting in Language Models

- URL: https://arxiv.org/abs/2210.03629
- 类别：academic foundation
- 为什么重要：工具型 agent 的 reason-act-observe loop 基础论文。
- 关键启发：
  - 交织 reasoning 和 actions 能帮助 agent 更新计划并处理异常。
  - 外部环境交互能减少知识任务中的幻觉和错误传播。
  - 当 reasoning 和 actions 可见时，可解释性更好。
- 设计标签：`reason_act_observe`、`tool_feedback`、`interpretability`

### Reflexion - Language Agents With Verbal Reinforcement Learning

- URL: https://arxiv.org/abs/2303.11366
- 类别：academic foundation
- 为什么重要：支持不改变模型权重、通过反馈改进后续表现的学习模式。
- 关键启发：
  - Agents 可以把来自反馈的 reflective text 存入 episodic memory。
  - Verbal feedback 无需 fine-tuning 就能改善后续 trials。
  - Memory quality 和 feedback source 很关键。
- 设计标签：`learning_candidate`、`episodic_memory`、`wiki_review`

### Voyager - Open-Ended Embodied Agent With LLMs

- URL: https://arxiv.org/abs/2305.16291
- 类别：skill library、lifelong learning
- 为什么重要：对 skill library 和 reviewed reusable procedure 有强类比价值，虽然其自治程度高于科研 workflow agent 应采用的程度。
- 关键启发：
  - Skill libraries 能复利式提高 agent 能力。
  - 带环境反馈和 self-verification 的迭代 prompting 能提升 executable code skills。
  - 自动 curriculum 对受监管 ER workflows 有风险；真正可取的是 skill reuse。
- 设计标签：`skill_library`、`self_verification`、`reviewed_procedure`

### Generative Agents - Interactive Simulacra of Human Behavior

- URL: https://arxiv.org/abs/2304.03442
- 类别：memory、reflection、planning
- 为什么重要：经典 memory architecture：observation、reflection、planning。
- 关键启发：
  - Agents 存储 observations，综合 higher-level reflections，并检索相关 memories 用于 planning。
  - Reflection 只有在 grounded in stored experience 时才有价值。
  - Human-visible memory 可以逐渐塑造 agent 行为。
- 设计标签：`memory`、`reflection`、`planning`、`wiki`

## 英文社区讨论 / 反方观点

### Hacker News - The Coming Loop

- URL: https://news.ycombinator.com/item?id=48643180
- 类别：community critique
- 为什么重要：提醒没有 objective checks 的 loop engineering 会放大 evaluation problem。
- 关键启发：
  - 核心瓶颈变成评估 agentic coding 是否正确。
  - Checklist files 和 tests 能帮助模型理解当前状态，但不能替代独立验证。
- 设计标签：`evaluation_bottleneck`、`checklist`、`risk`

### Hacker News - Loop Engineering: Designing Loops That Prompt Coding Agents

- URL: https://news.ycombinator.com/item?id=48514387
- 类别：community discussion
- 为什么重要：呈现 practitioners 对 maker-checker 的直觉。
- 关键启发：
  - 有人认为任何 direct model answer 都不应未经另一个 agent 或流程 digest / verify 就给用户。
  - 这支持在 raw run 和 user-facing answer 之间设置可见 review layer。
- 设计标签：`maker_checker`、`verified_summary`

### Reddit r/ClaudeAI - Agent Loops Are Great Until They Learn From Your Worst Code

- URL: https://www.reddit.com/r/ClaudeAI/comments/1u1fpdj/agent_loops_are_great_until_they_learn_from_your/
- 类别：community critique
- 为什么重要：直接对应 wiki / memory contamination。
- 关键启发：
  - Agents 会模仿它们看到的代码和文档，包括 deprecated 或 bad patterns。
  - 如果缺少 curation，memory 和 retrieval 会放大坏例子。
  - Token cost 和 unbounded file reading 是实际约束。
- 设计标签：`memory_contamination`、`deprecated_patterns`、`reviewed_wiki`、`token_budget`

### Reddit r/coding_agents - What's Missing From Loop Engineering: Budgets and Local Models

- URL: https://www.reddit.com/r/coding_agents/comments/1u11mbq/whats_missing_from_loop_engineering_budgets_and/
- 类别：community critique
- 为什么重要：loop 设计容易忽略 cost 和 budget controls。
- 关键启发：
  - 用户希望以 dollars / tokens / iterations 表达明确 task budgets。
  - Harness 应在可能时把便宜检查路由给便宜或本地 agents。
- 设计标签：`budget`、`token_control`、`effort_scaling`

### Reddit r/myclaw - Is Loop Engineering Buzzword or Workflow Design?

- URL: https://www.reddit.com/r/myclaw/comments/1u047p8/so_is_loop_engineering_the_next_ai_dev_buzzword/
- 类别：community framing
- 为什么重要：有用的怀疑性总结：真正持久的是 workflow design，而不是 buzzword。
- 关键启发：
  - 有价值的是 workflow design，不是“loop engineering”这个词本身。
  - Loops 适合把重复或高风险环节包进 memory、verification 和 guardrails。
- 设计标签：`buzzword_filter`、`guardrails`、`workflow_design`
