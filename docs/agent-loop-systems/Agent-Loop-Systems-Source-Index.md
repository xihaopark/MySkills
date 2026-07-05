# Source Index: Agent Loop Systems

Created: 2026-07-05

Scope: English-language external sources on agent loops, harness design, HITL, guardrails, evals, memory, and community experience. Sources are grouped by relevance to scientific workflow agent design.

## High-Signal Primary / Vendor Sources

### Local Reference - Claude Science Design Philosophy Reading

- URL: [Claude Science Full Reference ZH](Claude-Science-Full-Reference-ZH.md)
- Category: scientific-agent system design, artifact-first research agent architecture
- Why it matters: long-form Chinese analysis of Claude Science as a scientific-computing agent platform. It is especially relevant to A scientific workflow agent because it frames agents as calibrated scientific instruments whose outputs are artifacts, provenance records, and grounded computations rather than chat answers.
- Key takeaways:
  - Treat the agent as a calibrated instrument, not a subordinate to be commanded.
  - Make artifacts first-class outputs and keep conversation as a navigation layer.
  - Put provenance into the system by construction, not by post-hoc explanation.
  - Prefer authoritative data/tool grounding over generation from memory.
  - Shape agents by purpose through tool and capability boundaries.
  - Use progressive disclosure so large skill libraries do not overwhelm context.
  - Self-extension should be measured, reviewed, and eval-backed.
- Design tags: `artifact_first`, `provenance_by_construction`, `grounding`, `purpose_shaped_agents`, `progressive_disclosure`, `self_extension`, `wiki`

### Anthropic - Building Effective Agents

- URL: https://www.anthropic.com/engineering/building-effective-agents
- Category: agent architecture patterns
- Why it matters: clean distinction between workflows and agents; emphasizes environment ground truth, checkpoints, blockers, and stopping conditions.
- Key takeaways:
  - Agents should observe real tool/environment feedback at each step.
  - Human feedback checkpoints and stopping conditions are first-class controls.
  - Simple composable patterns are often preferable to complex frameworks.
- Design tags: `ground_truth`, `checkpoint`, `stop_condition`, `tool_design`, `Core3-6`

### Anthropic - How We Built Our Multi-Agent Research System

- URL: https://www.anthropic.com/engineering/multi-agent-research-system
- Category: orchestrator-workers, research loops
- Why it matters: directly relevant to deep research and complex source-backed analysis.
- Key takeaways:
  - Lead agents need explicit delegation instructions, output formats, tool guidance, and task boundaries.
  - Agents over-spend effort unless the system gives scaling rules.
  - Tool descriptions and tool-selection heuristics materially affect outcomes.
- Design tags: `orchestrator_workers`, `task_boundaries`, `source_backed_analysis`, `tool_semantics`

### Anthropic - Effective Harnesses for Long-Running Agents

- URL: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Category: long-running coding harness
- Why it matters: shows a concrete harness that keeps multi-session agents coherent with progress files, feature lists, and environment setup.
- Key takeaways:
  - Long-running work needs an initializer/environment phase.
  - Feature/checklist artifacts prevent premature "done."
  - Progress state outside the context window is essential.
- Design tags: `harness`, `progress_file`, `checklist`, `context_reset`

### Anthropic - Harness Design for Long-Running Application Development

- URL: https://www.anthropic.com/engineering/harness-design-long-running-apps
- Category: planner-generator-evaluator architecture
- Why it matters: describes a three-agent planner/generator/evaluator system and why evaluator criteria matter.
- Key takeaways:
  - Generator-evaluator loops can improve both subjective and verifiable outputs.
  - Criteria wording shapes output behavior.
  - Structured artifacts between sessions are a major reliability lever.
- Design tags: `planner_runner_evaluator`, `review_agent`, `criteria`, `structured_handoff`

### Anthropic - Effective Context Engineering for AI Agents

- URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Category: context engineering
- Why it matters: A scientific workflow agent needs reviewed wiki retrieval and attention packets without overloading context.
- Key takeaways:
  - The challenge is choosing high-signal context, not maximizing context volume.
  - Multi-agent designs work when subagents return distilled summaries.
  - Compaction, note-taking, and subagents are different context strategies for different task shapes.
- Design tags: `wiki_retrieval`, `attention_packet`, `context_budget`

### Anthropic - Writing Effective Tools for Agents

- URL: https://www.anthropic.com/engineering/writing-tools-for-agents
- Category: tool design and tool evals
- Why it matters: A scientific workflow agent tools/gates must be designed for agent consumption, not only human CLI use.
- Key takeaways:
  - Tool interfaces are as important as prompts.
  - Good tools have clear namespacing, meaningful context returns, token-efficient outputs, and evals.
  - Tool descriptions can be iteratively improved using agent failures.
- Design tags: `tool_contract`, `gate_tooling`, `artifact_contract`

### Anthropic - Demystifying Evals for AI Agents

- URL: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Category: evals
- Why it matters: Core3-6 should be evaluated by workflow behavior and evidence quality, not only unit tests.
- Key takeaways:
  - Evals prevent reactive loops where production failures create regressions.
  - Agent evals are harder because agents use tools, modify state, and adapt across turns.
  - Evaluation should become a lifecycle discipline, not a one-time test.
- Design tags: `evals`, `contract_tests`, `workflow_evidence`

### Anthropic - Scaling Managed Agents: Decoupling the Brain From the Hands

- URL: https://www.anthropic.com/engineering/managed-agents
- Category: durable agent infrastructure and sandbox separation
- Why it matters: useful framing for separating Workflow control, runner/tools, and durable session/run logs.
- Key takeaways:
  - Separate brain/harness, hands/tools/sandboxes, and durable session event log.
  - Tool/sandbox failures should be recoverable through standard tool error paths.
  - Session logs should live outside the model context window.
- Design tags: `event_log`, `session_log`, `sandbox`, `recoverability`, `run evidence roots`

### OpenAI - Running Agents

- URL: https://developers.openai.com/api/docs/guides/agents/running-agents
- Category: agent loop runtime
- Why it matters: provides a concise formal loop: model call, tool calls, handoff, final output; also stresses state strategy.
- Key takeaways:
  - Tools, handoffs, approvals, and streaming sit on top of the core loop.
  - Pick one conversation/state strategy to avoid context duplication.
  - Sessions are the default when durable memory or resumable approval flows are needed.
- Design tags: `agent_loop`, `session_strategy`, `handoff`, `state`

### OpenAI - Guardrails and Human Review

- URL: https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
- Category: guardrails and HITL
- Why it matters: maps cleanly to Core gate design.
- Key takeaways:
  - Guardrails and human review decide continue, pause, or stop.
  - Input, output, and tool guardrails handle different risks.
  - Human review is the right control before sensitive actions or consequential tool calls.
- Design tags: `typed_gate`, `approval`, `pause_resume`, `side_effects`

### OpenAI - Integrations and Observability

- URL: https://developers.openai.com/api/docs/guides/agents/integrations-observability
- Category: MCP and tracing
- Why it matters: A scientific workflow agent needs visible run traces without showing raw debug in the main conversation.
- Key takeaways:
  - Decide which external surfaces live inside the agent loop.
  - Runtime should own local/private MCP connectivity, filtering, and approvals.
  - Traces should capture model calls, tools, handoffs, guardrails, and custom spans.
- Design tags: `tracing`, `MCP`, `observability`, `raw_events`

### LangGraph - Interrupts

- URL: https://docs.langchain.com/oss/python/langgraph/interrupts
- Category: dynamic HITL interrupts
- Why it matters: best concrete model for gate popup pause/resume semantics.
- Key takeaways:
  - Interrupts pause execution, persist graph state, and resume with external input.
  - A thread id is the resume pointer.
  - Interrupt payloads should be JSON-serializable and side effects before interrupt must be idempotent.
- Design tags: `interrupt`, `checkpoint`, `run_scoped_gate`, `resume`

### LangChain - Making It Easier to Build HITL Agents With Interrupt

- URL: https://www.langchain.com/blog/making-it-easier-to-build-human-in-the-loop-agents-with-interrupt
- Category: HITL product pattern
- Why it matters: explains interrupt as production replacement for terminal `input()`.
- Key takeaways:
  - Persistence is the foundation for human-in-the-loop.
  - Humans can approve/reject, review/edit state, review tool calls, or participate in multi-turn interaction.
  - Interrupted threads should not consume resources while waiting.
- Design tags: `human_review`, `edit_state`, `approval_card`

### Microsoft AutoGen - Reflection Pattern

- URL: https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/reflection.html
- Category: reflection / reviewer loop
- Why it matters: direct support for separating runner and reviewer roles.
- Key takeaways:
  - Reflection uses a generator and reviewer loop with structured message protocols.
  - Loop stops on approval or max iterations.
  - Message protocols matter as much as agent prompts.
- Design tags: `maker_checker`, `review_agent`, `message_protocol`

### Microsoft Azure Architecture Center - Agent Orchestration Patterns

- URL: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- Category: orchestration patterns
- Why it matters: cautions against overusing group chat when deterministic workflows suffice.
- Key takeaways:
  - Group chat is useful for review, validation, and multidisciplinary discussion.
  - It is not ideal when deterministic linear processing is sufficient.
  - More agents increase control complexity; keep the agent count small.
- Design tags: `orchestration_choice`, `multi_agent_limit`, `quality_control`

### AWS Prescriptive Guidance - Evaluator Reflect-Refine Loop

- URL: https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/evaluator-reflect-refine-loop-patterns.html
- Category: evaluator loop
- Why it matters: concise enterprise description of generator/evaluator/refiner loops with retry limits.
- Key takeaways:
  - Loop repeats until criteria are met, approval occurs, or a retry limit is reached.
  - Evaluators need rubrics or criteria.
  - Escalation is a valid terminal state.
- Design tags: `retry_limit`, `criteria`, `escalation`

## Coding-Agent and Loop-Engineering Practice Sources

### Addy Osmani - Loop Engineering

- URL: https://addyosmani.com/blog/loop-engineering/
- Category: loop engineering overview
- Why it matters: widely cited framing of loops as systems that prompt agents.
- Key takeaways:
  - Loop engineering replaces the human as the repeated prompter.
  - Useful loops need automation, worktrees, skills, connectors, subagents, and memory.
  - Memory must live outside the single conversation.
- Design tags: `loop_engineering`, `memory`, `skills`, `connectors`

### Cursor - Best Practices for Coding With Agents

- URL: https://cursor.com/blog/agent-best-practices
- Category: practical coding agent workflow
- Why it matters: concrete hook-based long-running loop with max iteration cap and scratchpad.
- Key takeaways:
  - Skills package domain knowledge and reusable workflows.
  - Long-running loops work best when success is verifiable.
  - Hooks can continue a loop until a scratchpad says done or iteration cap is reached.
- Design tags: `skills`, `scratchpad`, `max_iterations`, `verifiable_goal`

### Cursor - Scaling Long-Running Autonomous Coding

- URL: https://cursor.com/blog/scaling-agents
- Category: multi-agent coordination at scale
- Why it matters: real failure modes from many concurrent agents.
- Key takeaways:
  - Shared-file self-coordination and locks can become brittle bottlenecks.
  - Planner/worker designs are more stable than flat peer coordination.
  - Large parallelism increases coordination complexity faster than productivity.
- Design tags: `planner_worker`, `coordination`, `avoid_flat_multi_agent`

### Steve Kinney - The Anatomy of an Agent Loop

- URL: https://stevekinney.com/writing/agent-loops
- Category: technical explainer
- Why it matters: simple framework-level view of agent loops and stop branches.
- Key takeaways:
  - An agent loop is essentially reason/act/observe/repeat.
  - Frameworks converge on branches such as final output, handoff, run again, and interruption.
  - Max turns and interruption are core loop controls.
- Design tags: `loop_anatomy`, `interruption`, `max_turns`

### Oracle Developers - The Agent Loop Decoded

- URL: https://blogs.oracle.com/developers/the-agent-loop-decoded-three-levels-every-agent-engineer-must-know
- Category: harness vs model, memory levels
- Why it matters: useful language for separating model, harness, memory, and stopping conditions.
- Key takeaways:
  - Most agent engineering work happens in the harness, not in the model.
  - Stopping must include goal-completion checks, iteration caps, wall-clock timeouts, unrecoverable errors, and repeated-action detection.
  - Apparent learning inside a session is retrieval, not model-weight learning.
- Design tags: `harness`, `stop_conditions`, `memory_aware_agent`, `wiki`

### Firecrawl - Loop Engineering

- URL: https://www.firecrawl.dev/blog/loop-engineering
- Category: practitioner overview
- Why it matters: concise definition of loop engineering as a program that handles discovery, planning, execution, verification, and iteration.
- Key takeaways:
  - The model becomes a subroutine inside the loop.
  - The loop must include a schedule or trigger and a stopping condition.
  - Prompting remains, but moves into the system design.
- Design tags: `model_as_subroutine`, `schedule`, `verification`

### Datadog - Closing the Verification Loop

- URL: https://www.datadoghq.com/blog/ai/harness-first-agents/
- Category: harness-first verification and observability
- Why it matters: strong argument that verification quality determines agent quality.
- Key takeaways:
  - A strong harness makes iteration cheap; a weak harness cannot be fixed by better models or more human review.
  - Fast automated checks should do the work humans cannot scale.
  - Production telemetry closes the loop when modeled behavior diverges from reality.
- Design tags: `verification_loop`, `observability`, `artifact_audit`, `telemetry`

## Academic Foundations

### ReAct - Synergizing Reasoning and Acting in Language Models

- URL: https://arxiv.org/abs/2210.03629
- Category: academic foundation
- Why it matters: foundational reason-act-observe loop for tool-using agents.
- Key takeaways:
  - Interleaving reasoning and actions helps agents update plans and handle exceptions.
  - External environment interaction reduces hallucination/error propagation in knowledge tasks.
  - Interpretability improves when reasoning and actions are visible.
- Design tags: `reason_act_observe`, `tool_feedback`, `interpretability`

### Reflexion - Language Agents With Verbal Reinforcement Learning

- URL: https://arxiv.org/abs/2303.11366
- Category: academic foundation
- Why it matters: supports learning from feedback without changing model weights.
- Key takeaways:
  - Agents can store reflective text from feedback in episodic memory.
  - Verbal feedback improves subsequent trials without fine-tuning.
  - Memory quality and feedback source matter.
- Design tags: `learning_candidate`, `episodic_memory`, `wiki_review`

### Voyager - Open-Ended Embodied Agent With LLMs

- URL: https://arxiv.org/abs/2305.16291
- Category: skill library / lifelong learning
- Why it matters: strong analogy for skill-library and reviewed reusable procedure, though much more autonomous than A scientific workflow agent should be.
- Key takeaways:
  - Skill libraries can compound agent ability.
  - Iterative prompting with environment feedback and self-verification improves executable code skills.
  - Automatic curriculum is risky for regulated ER workflows; skill reuse is the useful piece.
- Design tags: `skill_library`, `self_verification`, `reviewed_procedure`

### Generative Agents - Interactive Simulacra of Human Behavior

- URL: https://arxiv.org/abs/2304.03442
- Category: memory, reflection, planning
- Why it matters: classic memory architecture with observation, reflection, planning.
- Key takeaways:
  - Agents store observations, synthesize higher-level reflections, and retrieve relevant memories for planning.
  - Reflection is useful only when grounded in stored experience.
  - Human-visible memory can shape agent behavior over time.
- Design tags: `memory`, `reflection`, `planning`, `wiki`

## English Community Discussion / Counterpoints

### Hacker News - The Coming Loop

- URL: https://news.ycombinator.com/item?id=48643180
- Category: community critique
- Why it matters: highlights that loop engineering can worsen evaluation problems if done without objective checks.
- Key takeaways:
  - The core bottleneck becomes evaluating whether agentic coding is correct.
  - Checklist files and tests help the model know current status, but do not replace independent verification.
- Design tags: `evaluation_bottleneck`, `checklist`, `risk`

### Hacker News - Loop Engineering: Designing Loops That Prompt Coding Agents

- URL: https://news.ycombinator.com/item?id=48514387
- Category: community discussion
- Why it matters: captures the maker-checker intuition from practitioners.
- Key takeaways:
  - Some practitioners argue no direct model answer should go to a user without another agent or process digesting/verifying it.
  - This supports a visible review layer between raw run and user-facing answer.
- Design tags: `maker_checker`, `verified_summary`

### Reddit r/ClaudeAI - Agent Loops Are Great Until They Learn From Your Worst Code

- URL: https://www.reddit.com/r/ClaudeAI/comments/1u1fpdj/agent_loops_are_great_until_they_learn_from_your/
- Category: community critique
- Why it matters: directly relevant to wiki/memory contamination.
- Key takeaways:
  - Agents imitate the code and documents they see, including deprecated or bad patterns.
  - Memory and retrieval can amplify poor examples if curation is weak.
  - Token cost and unbounded file reading are practical constraints.
- Design tags: `memory_contamination`, `deprecated_patterns`, `reviewed_wiki`, `token_budget`

### Reddit r/coding_agents - What's Missing From Loop Engineering: Budgets and Local Models

- URL: https://www.reddit.com/r/coding_agents/comments/1u11mbq/whats_missing_from_loop_engineering_budgets_and/
- Category: community critique
- Why it matters: cost and budget controls are easy to miss in loop design.
- Key takeaways:
  - Users want explicit task budgets in dollars/tokens/iterations.
  - Harnesses should route cheaper checks to cheaper/local agents where possible.
- Design tags: `budget`, `token_control`, `effort_scaling`

### Reddit r/myclaw - Is Loop Engineering Buzzword or Workflow Design?

- URL: https://www.reddit.com/r/myclaw/comments/1u047p8/so_is_loop_engineering_the_next_ai_dev_buzzword/
- Category: community framing
- Why it matters: useful skeptical summary: memory, verification, guardrails around repetitive or risky parts.
- Key takeaways:
  - The durable content is workflow design, not the buzzword.
  - Loops are valuable when they wrap repetitive/risky parts with memory, verification, and guardrails.
- Design tags: `buzzword_filter`, `guardrails`, `workflow_design`
