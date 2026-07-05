# Notes 06: Claude Science Design Philosophy

Source: `../sources/claude-science-design-philosophy-zh.md`

This note distills the user-added Claude Science reading into design principles for scientific workflow agent. It does not claim Claude Science is the target product; it uses the reading as a reference architecture for scientific-agent behavior.

## Core Frame

The useful sentence from the source:

> Treat the agent as a scientific instrument that must be calibrated, not as a subordinate that must be commanded.

For a scientific workflow agent, this means we should not solve Core3-6 by adding stricter prompt commands. We should calibrate the loop:

- what evidence the agent sees;
- what artifacts it must produce;
- what boundaries it cannot cross;
- what user decisions are required;
- what evals show the loop is improving.

## Seven Transferable Principles

### 1. Artifact-First

Claude Science treats artifacts as the main product and chat as the connective layer.

Reusable mapping:

- `<run evidence root>` should remain the evidence root.
- Core3-6 should produce user-facing attention packets that link to artifacts.
- Main conversation should summarize and navigate artifacts, not become the artifact.

Design implication:

- Every Core3-6 card should point to concrete CSV/PNG/manifest/review files.
- "Selected result" should be an artifact-backed context object, not copied chat text.

### 2. Declarative Compute / Declarative Workflow

Claude Science uses declarative environment specs to separate what a job needs from how each backend runs it.

Reusable mapping:

- ER workflow specs should describe clinical/statistical intent and source mappings.
- Runner code should execute against those specs without hardcoded study logic.
- Core3-6 gates should mutate explicit spec/decision state, not hidden prompt context.

Design implication:

- Gate decisions should be represented as typed state that downstream runners consume.
- Future Core3-6 improvements should prefer spec extensions over ad hoc prompts.

### 3. Provenance by Construction

The source emphasizes execution logs, artifact versions, dependency DAGs, checksums, and environment snapshots.

Reusable mapping:

- We already have artifact lanes, pipeline status, data auditor, gate records, and `run evidence roots`.
- The gap is user-facing provenance: the user should see enough lineage to trust what happened without reading raw debug.

Design implication:

- Core3-6 should add compact lineage summaries:
  - source files used;
  - upstream artifacts consumed;
  - outputs written;
  - gates/audits affecting result;
  - unresolved dependencies.

### 4. Grounding Over Generation

Claude Science's rule is compute/query authoritative sources rather than inventing answers.

Reusable mapping:

- Core3-6 cannot infer clinical/statistical decisions from model memory.
- It should use source data, specs, prior artifacts, reviewed wiki, and explicit gates.

Design implication:

- A Core3 exposure metric or Core5 interpretation must cite the exact spec/gate/source artifact that supports it.
- If a source is unavailable, write a blocked manifest rather than creating synthetic placeholder claims.

### 5. Purpose-Shaped Agents

The source highlights agents shaped by removing irrelevant tools and capabilities.

Reusable mapping:

- Do not make one all-powerful ER agent.
- Use purpose-shaped roles:
  - Runner: execute deterministic core.
  - Auditor: inspect artifact/source/gate quality.
  - Explainer: produce human decision packet.
  - Wiki Curator: propose learning candidates, never auto-approve.

Design implication:

- Core3-6 should not use group chat as the default.
- Review/audit roles should have constrained authority and clear output schemas.

### 6. Progressive Disclosure

Claude Science keeps many skills available without loading them all into context.

Reusable mapping:

- Reviewed wiki should be retrieved selectively into a bounded attention packet.
- Skills should stay stable procedure; wiki should provide reviewed project knowledge.

Design implication:

- Wiki retrieval logs should show why a page was retrieved.
- The agent should only receive distilled wiki context needed for the current core.

### 7. Measured Self-Extension

The source's strongest self-evolution lesson is not "auto-write new skills." It is measured improvement:

- generate candidate;
- test it;
- compare results;
- review regression risk;
- only then publish.

Reusable mapping:

- Runtime can write learning candidates.
- Humans approve wiki updates.
- Skills/registry/runner updates require explicit development workflow and tests.

Design implication:

- Wiki learning and eval learning should be separate:
  - wiki records reviewed knowledge;
  - eval cases record behavior we must preserve.
- A learning candidate should be promoted only with source refs and review status.

## Tension With Current A scientific workflow agent State

Current Core3-6 happy path is mostly automode. The Claude Science reading pushes us toward:

- less silent automation;
- more artifact-backed user visibility;
- clearer decision boundaries;
- stronger provenance summaries;
- reviewed memory that affects execution;
- eval-backed self-evolution rather than unchecked runtime learning.

## Design Questions Added by This Source

- Should every Core3-6 output be wrapped as an artifact card with provenance and decision boundary?
- Should Core3-6 runner output include a dependency DAG or simplified lineage table?
- Should wiki retrieval be treated as a formal source input and appear in Core6 review package?
- Should "agent learning" always produce two artifacts: a wiki candidate and an eval candidate?
- Should each role's allowed tools be documented as part of the 1.0 stability plan?

