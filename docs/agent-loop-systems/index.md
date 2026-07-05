# Agent Loop 系统

本节整理面向科研、证据链和高可靠工作流的 agent system 研究与设计笔记。这里的重点不是“让 agent 更自治”，而是设计一个清晰、可验证、可介入、可学习的运行循环。

!!! tip "建议阅读路径"
    如果想看资料来源，先读外部资料索引（Source Index）。如果正在设计真实系统，先读科研工作流设计问题。

<section class="kb-grid" markdown>

<a class="kb-card" href="Agent-Loop-Systems-Source-Index/">
  <span class="kb-card__eyebrow">资料索引 Source Index</span>
  <strong>外部资料索引</strong>
  <span>按循环架构、护栏、评估、记忆和 Wiki 实践整理外部资料。</span>
</a>

<a class="kb-card" href="Scientific-Workflow-Agent-Design-Questions/">
  <span class="kb-card__eyebrow">设计问题 Design Questions</span>
  <strong>科研工作流设计问题</strong>
  <span>用于设计具备清晰人工介入点的科研 workflow agent。</span>
</a>

<a class="kb-card" href="Agent-Loop-Systems-Claude-Science-Design-Philosophy/">
  <span class="kb-card__eyebrow">Claude Science</span>
  <strong>设计哲学</strong>
  <span>从 artifact-first、provenance-aware 的科研 agent 环境中提炼原则。</span>
</a>

<a class="kb-card" href="Agent-Loop-Systems-Memory-Learning-and-Wiki/">
  <span class="kb-card__eyebrow">记忆 Memory</span>
  <strong>记忆、学习与 Wiki</strong>
  <span>让经人工审核的 Wiki 真正影响执行，而不是只做缓存。</span>
</a>

</section>

## 先读这些

- [外部资料索引（Source Index）](Agent-Loop-Systems-Source-Index.md)
- [科研工作流 Agent 设计问题](Scientific-Workflow-Agent-Design-Questions.md)
- [Claude Science 设计哲学](Agent-Loop-Systems-Claude-Science-Design-Philosophy.md)
- [Claude Science 长文参考](Claude-Science-Full-Reference-ZH.md)

## 主题笔记

- [循环与执行框架（Loop / Harness）](Agent-Loop-Systems-Loop-and-Harness-Architecture.md)
- [人工介入与护栏（HITL / Guardrails）](Agent-Loop-Systems-Human-in-the-Loop-and-Guardrails.md)
- [验证、评估与可观测性（Verification / Evals / Observability）](Agent-Loop-Systems-Verification-Evals-and-Observability.md)
- [记忆、学习与 Wiki](Agent-Loop-Systems-Memory-Learning-and-Wiki.md)
- [社区风险与反方观点](Agent-Loop-Systems-Community-Risks-and-Counterpoints.md)
