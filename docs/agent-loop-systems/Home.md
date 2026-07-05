# MySkills Wiki

This wiki is XiHao Park's long-term personal knowledge base for reusable agent-system design, workflow skills, and collaboration patterns.

Current section: agent loop systems for scientific and evidence-heavy workflows.

## Start Here

- [Agent Loop Systems Source Index](Agent-Loop-Systems-Source-Index)
- [Scientific Workflow Agent Design Questions](Scientific-Workflow-Agent-Design-Questions)
- [Claude Science Design Philosophy](Agent-Loop-Systems-Claude-Science-Design-Philosophy)
- [Claude Science Full Reference ZH](Claude-Science-Full-Reference-ZH)

## Topic Notes

- [Loop and Harness Architecture](Agent-Loop-Systems-Loop-and-Harness-Architecture)
- [Human-in-the-Loop and Guardrails](Agent-Loop-Systems-Human-in-the-Loop-and-Guardrails)
- [Verification, Evals, and Observability](Agent-Loop-Systems-Verification-Evals-and-Observability)
- [Memory, Learning, and Wiki](Agent-Loop-Systems-Memory-Learning-and-Wiki)
- [Community Risks and Counterpoints](Agent-Loop-Systems-Community-Risks-and-Counterpoints)

## Working Premise

The useful shift is not "make the agent more autonomous." It is to design the loop that decides what the agent sees, what it may do, how it gets ground truth, when it pauses for the user, how it verifies work, and what reviewed memory becomes available next time.

For scientific workflow agents, this points toward deterministic runners plus explicit human decision cards, review/audit loops, and reviewed wiki memory that can be retrieved at execution time.

