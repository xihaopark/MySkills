# Notes 02: Human-in-the-Loop and Guardrails

## Core Pattern

Strong sources agree that HITL should be implemented as a durable interrupt, not as a prompt instruction like "ask the user if needed."

Key mechanics:

- pause execution at a specific point;
- persist state;
- surface a small structured payload to the human;
- accept a typed decision such as approve/edit/reject/respond;
- resume from the same run/thread state;
- record the decision and option text.

## Guardrail Taxonomy

OpenAI's division maps well to Scientific workflow agent:

- Input guardrails: block or reroute unsuitable initial requests.
- Tool guardrails: validate tool inputs/outputs around side effects.
- Output guardrails: validate what leaves the system.
- Human review: pause before sensitive or consequential actions.

Reusable mapping:

- Core gates are not "notices"; they are human review interrupts.
- Audit notices can remain context-only, but must not masquerade as a gate.
- Core3-6 decisions that affect interpretation should use typed popup gates.

## What Should Become a Gate?

Gate candidates from ER workflow:

- Core3:
  - exposure metric definitions;
  - posthoc/source mapping;
  - BLQ/LLOQ handling;
  - exposure windows;
  - observed vs modeled provenance.
- Core4:
  - ER question matrix;
  - endpoint family and exposure axis list;
  - plot batch approval;
  - model-readiness route.
- Core5:
  - model family;
  - minimum event threshold;
  - dose adjustment;
  - censoring/TTE rules;
  - interpretation level.
- Core6:
  - readiness status;
  - must-resolve actions;
  - whether selected results enter downstream context.
- Wiki:
  - approve/reject/edit learning candidates before entering reviewed wiki.

## Interface Shape

The best HITL payload is not a full transcript. It should include:

- decision title;
- why the decision matters;
- current evidence;
- options with exact option text;
- recommended option, if safe;
- impact on downstream cores;
- links to source artifacts;
- free-form comment slot;
- resume behavior.

## Failure Modes to Avoid

- Asking for approval after the side effect already happened.
- Losing state while waiting for user input.
- Hiding the exact option text that was chosen.
- Putting huge raw CSV/debug logs in the user-facing gate.
- Treating "user did not answer" as implicit approval for clinical/statistical interpretation.
- Reusing a gate decision across runs without a run-scoped record.

## Open Design Questions

- Should Core3-6 gates use the same typed schema family as Core1 data cutoff?
- Should each gate write both `gate_request.json` and `gate_decision.jsonl`?
- Should UI allow "approve for this run only" vs "approve and propose wiki memory"?

