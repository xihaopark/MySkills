# Notes 01: Loop and Harness Architecture

## Central Pattern

Most high-signal sources converge on a layered view:

1. Model: reasons and decides what to try next.
2. Harness: assembles context, executes tools, enforces constraints, persists state.
3. Tools/hands: perform external actions.
4. Session/run log: durable event record outside the model context.
5. Verification/evaluator: decides whether the loop may continue, stop, retry, or escalate.

The strongest lesson is that **agent quality is mostly harness quality** once the model is capable enough.

## Loop vs Workflow

Anthropic draws a useful distinction:

- Workflow: developer defines the control flow.
- Agent: model decides the control flow inside a bounded loop.

For scientific workflow agent, Core1-6 should remain closer to workflow than open-ended agent. The agent layer should decide presentation, clarification, and follow-up exploration; the clinical/statistical artifact pipeline should stay deterministic and auditable.

## Minimum Loop Branches

Common loop branches across OpenAI SDK, framework explainers, and community writeups:

- final output: no more tool work, output shape is satisfied.
- tool call: execute tool, append result, continue.
- handoff: switch to specialist/worker, continue.
- interruption: pause for human approval/input, persist state.
- failure/escalation: stop with evidence and next action.

Reusable mapping:

- `final_output` -> step report / selected result / Core6 review summary.
- `tool_call` -> deterministic runner, R scripts, file readers, artifact scanners.
- `handoff` -> review/auditor stage, not uncontrolled group chat.
- `interruption` -> Claude Code built-in popup gate.
- `failure/escalation` -> typed gate blocked/needs_review plus action item.

## Long-Running Harness Practices

Best practices from Anthropic/Cursor:

- Use an initializer/setup phase to write the state of the project and what "done" means.
- Store progress outside context, e.g. progress file, scratchpad, run log, checklist.
- Cap loop iterations and wall-clock time.
- Use worktrees or run isolation when agents may modify files.
- Make "done" checkable by artifacts/tests, not by model confidence.

Reusable mapping:

- `<run evidence root>` is the correct durable run root.
- The current six-core happy path should gain a per-core progress/checklist record, not only `pipeline_status.csv`.
- Core3-6 should not run as silent automode from user perspective; they need visible checkpoints.

## Orchestrator-Workers

Anthropic's research-system lessons are directly relevant:

- Subtasks require objective, output format, tool/source guidance, and boundaries.
- Effort should scale to query complexity.
- Tool descriptions and selection heuristics matter.

Reusable mapping:

- Avoid a flat multi-agent chat for Core3-6.
- Use one orchestrator/control surface plus bounded worker roles:
  - Runner: deterministic core execution.
  - Auditor: schema/data/gate checker.
  - Explainer: user-facing attention packet.
  - Optional Reviewer: adversarial review before handoff.

## Open Design Questions

- Should Core3-6 each have a formal `StepControl` state machine file?
- Should the runner emit a machine-readable `next_required_user_decision.json` after every core?
- Should "selected result as context" be modeled as a loop state transition rather than UI-only state?

