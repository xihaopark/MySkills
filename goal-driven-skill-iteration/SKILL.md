---
name: goal-driven-skill-iteration
description: "Use Goal mode to iteratively improve project skills, agent workflows, and reusable automation through concrete runs, evidence, tests, retrospectives, and skill updates. Use when a project is being developed by repeated Codex/Claude Code runs, when failures reveal missing skill instructions, when a workflow needs to become reusable rather than one-off, or when the team wants to turn project lessons into personal or shared skills."
---

# Goal Driven Skill Iteration

## Purpose

Use this skill when the work is not a single code change, but a loop: run the agent, observe where it succeeds or fails, update the skill, run again, and package the learning so future projects start better.

The goal is to turn project experience into reusable operating knowledge without prematurely freezing a bad workflow.

## Core Loop

Run this cycle until the workflow is stable enough to hand to another agent or human:

1. Define one concrete goal.
2. Run the project workflow from real inputs.
3. Collect outputs, failures, logs, user feedback, and evidence.
4. Classify the failure: missing context, weak instruction, wrong abstraction, bad tool boundary, missing validation, or bad report.
5. Patch the skill or supporting tool.
6. Re-run the same acceptance path.
7. Write down what changed and what boundary is still open.

Do not broaden the goal mid-run. If a new concern appears, record it as the next goal.

## When To Use Goal Mode

Use Goal mode when:

- The task spans many turns or multiple pipeline runs.
- The user wants steady progress without restarting context.
- The output quality depends on repeated evidence-backed iteration.
- The team is discovering how the skill should work.
- A workflow must become runnable by Claude Code or Codex end to end.

Avoid Goal mode for one-off edits, simple command outputs, or exploratory conversation where the user has not committed to implementation.

## Goal Shape

Write goals as outcomes, not activities:

```text
Good: Make mock01 run end to end and produce a reviewable output package.
Weak: Work on the mock01 pipeline.
```

A good goal has:

- A concrete artifact or behavior.
- A known acceptance command or review gate.
- A stopping condition.
- A list of evidence files or outputs to inspect.
- A clear human-facing result if the user needs one.

## Skill Update Rules

Update a skill when the run reveals a reusable lesson:

- The agent repeatedly asks for context that could be encoded.
- The agent makes the same wrong assumption across runs.
- The user corrects the project philosophy, not just a small bug.
- A tool boundary becomes clear, such as "copy/wrap original plotting code instead of rewriting plots."
- A validation phrase needs discipline, such as contract pass vs accuracy.
- A reporting pattern becomes obvious, such as DOCX for human review and CSV for evidence.

Do not update a skill with project-specific filenames unless the skill is explicitly project-specific. Put general principles in the skill and project examples in references.

## Skill Structure Pattern

Use this structure for reusable project skills:

- `SKILL.md`: the core operating procedure and trigger description.
- `references/lessons.md`: examples, failure modes, and retrospective notes.
- `references/checklists.md`: optional repeatable gates or review questions.
- `scripts/`: only when deterministic helper code is repeatedly needed.
- `assets/`: only for templates or output resources.

Keep `SKILL.md` short enough that another agent can read it and act. Move long examples to references.

## Retrospective Questions

At the end of a goal, ask:

- What did the agent do correctly?
- What did the user have to correct?
- Which correction is project-specific, and which is reusable?
- Which result is truly validated, and which only passed a weaker boundary?
- Which output was useful for machines but confusing for humans?
- What should the next agent know before starting?

Read `references/iteration-lessons.md` for a fuller checklist and common failure patterns.

## Completion Criteria

A goal-driven skill iteration is complete when:

- The run has reproducible commands or clear manual steps.
- The acceptance evidence is saved.
- The skill has been updated for reusable lessons.
- Claims are boundary-aware.
- The user-facing artifact matches the audience.
- Remaining issues are recorded as future goals, not hidden in prose.
