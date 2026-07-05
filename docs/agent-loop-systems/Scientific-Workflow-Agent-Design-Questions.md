# Scientific Workflow Agent Design Questions From External Research

Created: 2026-07-05

This file records questions, not conclusions. Use it before changing runtime or public documentation.

## 1. What Is the Actual Loop Unit?

Candidates:

- Whole workflow run: `/ERcoding:start` to Core6.
- Per core: Core1, Core2, Core3, Core4, Core5, Core6 each as a loop.
- Per decision: each gate or selected result branch as a loop.

Working hypothesis: use **per-core loop units** inside a whole-run controller.

Required loop phases:

1. retrieve reviewed wiki context;
2. assemble core input and prior artifacts;
3. run deterministic core;
4. collect artifacts/manifests;
5. audit and review;
6. create user attention packet;
7. pause if human decision is required;
8. persist decision and selected result context;
9. write learning candidates.

## 2. Where Must Core3-6 Stop for the User?

Core3:

- before using exposure metric definitions as governed axes;
- before accepting posthoc/source mapping;
- before BLQ/LLOQ policy affects metrics;
- before unresolved source dependency is treated as available.

Core4:

- before generating large ER plot batches;
- before locking ER question matrix;
- before marking model readiness as accepted by user.

Core5:

- before fitting or reporting nontrivial models if interpretation boundary is unclear;
- before dose-adjusted claims;
- before promoting exploratory results.

Core6:

- before claiming package is review-ready;
- before selected results become downstream context;
- before any output is framed as customer-ready.

## 3. What Should the User See?

Not raw debug by default. Each card should show:

- current core and run id;
- what the agent found;
- exact evidence files;
- what decision is needed;
- options and downstream consequences;
- recommended option if safe;
- unresolved risks;
- resume behavior.

## 4. What Does Wiki Influence Look Like?

A run should be able to answer:

- Which wiki pages were retrieved?
- Why were they retrieved?
- Which claims or decisions did they influence?
- What pages were ignored or stale?
- What new candidates were proposed?
- Did the user approve, edit, or reject candidates?

## 5. What Is the Minimum Stable Architecture?

Avoid a complex multi-agent product. Prefer:

- Workflow control as orchestrator.
- Deterministic runner as deterministic execution.
- Data Auditor / Review Agent as checker.
- Human decision surface as human decision surface.
- Wiki retrieval as bounded context.
- `<run evidence root>` as event/artifact evidence root.

## 6. What Should Be Explicitly Out of 1.0?

- automatic skill updates;
- automatic gate registry updates;
- automatic wiki promotion;
- autonomous customer-facing claims;
- group-chat multi-agent run execution;
- uncontrolled experimental artifacts in formal evidence chain.

## 7. What Needs a New Contract?

Candidate contracts:

- `core_attention_packet.schema.json`
- `wiki_retrieval_log.schema.json`
- `learning_candidate.schema.json`
- `human_decision_gate.schema.json`
- `selected_result_context.schema.json`
- `core_completion_predicate.schema.json`

## 8. First Experiment to Run

Run a mock Core3-6 pass in a fresh run with:

- wiki retrieval enabled;
- one forced Core3 decision card;
- one Core4 ER pair selection card;
- Core5 exploratory interpretation boundary card;
- Core6 review readiness card;
- learning candidates generated but not auto-approved.

Acceptance should be based on whether a user can understand and intervene without reading raw CSVs or debug logs.

## 9. Claude Science-Inspired Check

For each proposed Core3-6 design, ask:

- Artifact-first: what durable artifact is the user actually getting?
- Provenance: can we trace the artifact to source data, code, gate decisions, wiki context, and audits?
- Grounding: did the agent compute/query/read evidence, or did it infer from memory?
- Purpose-shaped role: which role is allowed to do this, and what tools are intentionally unavailable?
- Progressive disclosure: what exact wiki/skill context was loaded, and why only that?
- Measured self-extension: if this run teaches us something, is it a reviewed wiki candidate, an eval case, or a code change proposal?
