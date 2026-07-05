# MySkills Wiki

这是 XiHao Park 长期维护的个人知识库，用于整理可复用的 agent system 设计、工作流技能和协作模式。

当前章节：面向科研与证据密集型工作流的 Agent Loop 系统。

## 先读这些

- [外部资料索引（Source Index）](Agent-Loop-Systems-Source-Index)
- [科研 Workflow Agent 设计问题](Scientific-Workflow-Agent-Design-Questions)
- [Claude Science 设计哲学](Agent-Loop-Systems-Claude-Science-Design-Philosophy)
- [Claude Science 长文参考](Claude-Science-Full-Reference-ZH)

## 主题笔记

- [循环与执行框架（Loop / Harness）](Agent-Loop-Systems-Loop-and-Harness-Architecture)
- [人工介入与护栏（HITL / Guardrails）](Agent-Loop-Systems-Human-in-the-Loop-and-Guardrails)
- [验证、评估与可观测性（Verification / Evals）](Agent-Loop-Systems-Verification-Evals-and-Observability)
- [记忆、学习与 Wiki](Agent-Loop-Systems-Memory-Learning-and-Wiki)
- [社区风险与反方观点](Agent-Loop-Systems-Community-Risks-and-Counterpoints)

## 工作前提

真正有价值的转变不是“让 agent 更自治”，而是设计一个循环：决定 agent 能看到什么、能做什么、如何获得 ground truth、何时停下来问用户、如何验证工作，以及哪些 reviewed memory 能在下一次运行中被检索。

对于科研 workflow agent，这指向确定性 runner、明确的人类 decision cards、review / audit loops，以及会在执行时被检索的 reviewed wiki memory。
