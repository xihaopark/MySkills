# 笔记 05：社区风险与反方观点

## 为什么要纳入怀疑性资料

Loop engineering 是有用的框架，但社区讨论反复提醒：循环会放大系统已有弱点。对科研 workflow agent 来说，这些批评比宣传更有价值。

## 反复出现的批评

### 成本与 Token 消耗

Reddit、HN 和技术媒体讨论都指出：长循环、subagents、重复文件读取会迅速变贵。

可复用含义：

- 增加 iteration、time、token / effort budgets。
- 按任务复杂度伸缩 effort。
- 确定性检查足够时，不要使用 subagents。
- 优先使用紧凑 artifacts 和 wiki attention packets，而不是大范围重读 repo。

### 验证瓶颈

HN 讨论强调：loop 的质量取决于它闭环到什么反馈上。

可复用含义：

- Core3-6 的 “done” 必须能由 artifacts、gates、audit state 和用户可见 summary 检查。
- Tests 应验证 behavior / evidence，而不仅是文件存在。
- Reviewer / auditor loop 应独立于 runner。

### 从坏上下文中学习

“learn from your worst code” 的批评直接映射到 Wiki / memory 风险。

可复用含义：

- 不要把 runtime observations 自动提升为 reviewed memory。
- 显式 deprecated stale docs。
- 让 wiki status 可见。
- Retrieval 应引用 page path / version，使用户能纠正记忆来源。

### 过度 Agent 化

多篇资料提醒：扁平 multi-agent system 会增加协调失败。Cursor 的 scaling 文章展示了过多 agents 自协调时，locks 和 status files 会变成脆弱瓶颈。

可复用含义：

- Core3-6 应保持“确定性 workflow + 少数有边界角色”。
- 普通 run execution 不使用 group chat。
- 只在每个角色有清晰 contract 时使用 planner / runner / evaluator。

### 虚假的“完成”

长运行 agent 经常因为上下文满了、测试太浅，或模型相信 checklist 已足够而停止。

可复用含义：

- Completion predicates 必须显式。
- Core6 应保持保守：review-ready 不等于 final-report-ready。
- Main conversation 每次都应显示“仍未解决的内容”。

## 对 AZ 的实际平衡

稳定产品不应销售“自治”。它应销售：

- 可重复性；
- 可追溯性；
- 清晰的人类决策点；
- 基于 artifact 的声明；
- reviewed memory；
- 更低的人工反复 prompting 负担。
