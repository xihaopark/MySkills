# Notes 04: Memory, Learning, and Wiki

## Central Pattern

External sources separate three things that are often conflated:

- context: what the model sees now;
- memory: durable records retrieved into context;
- learning: a reviewed process for deciding which experience becomes reusable memory or eval signal.

Oracle's agent-loop article makes a useful point for Scientific workflow agent: apparent in-session learning is retrieval, not model training. For 1.0, A scientific workflow agent should not claim the model learns; it should claim the system retrieves reviewed memory and proposes new learning candidates.

## Skill Library vs Wiki

Voyager-style skill libraries show the compounding power of reusable executable procedures. But ER Agent needs stronger governance:

- Skills: stable procedures and tools.
- Wiki: reviewed facts, decisions, patterns, known pitfalls, customer preferences, and examples.
- Learning candidates: unreviewed run observations.
- Evals: behavior cases that should keep passing.

A scientific workflow agent should avoid auto-editing skills from runtime. Wiki is the safer first self-evolution surface.

## Reviewed Wiki Retrieval

For wiki to "actually affect execution," retrieval must be part of the run loop:

1. Before a core starts, retrieve reviewed wiki pages relevant to the core/study/scenario.
2. Inject a bounded attention packet, not whole wiki pages.
3. Log retrieval in run-local evidence.
4. Require the runner/explainer to state which wiki items influenced decisions.
5. Produce new learning candidates at the end.
6. Human approves candidates before they enter reviewed wiki.

## Memory Contamination Risks

Community critiques are important:

- Agents imitate deprecated code and stale docs.
- If bad patterns remain visible, loops can keep reviving them.
- Token-heavy loops can read too much low-value context.
- Automatic memory can cement mistakes.

Reusable mitigations:

- Wiki pages need status: `approved`, `deprecated`, `superseded`, `draft`.
- Retrieval should prefer approved/current pages and avoid deprecated examples unless explicitly requested.
- Every learning candidate should include source refs and confidence.
- User should see and edit proposed memory before approval.

## Candidate Wiki Page Types

- `decisions/` - accepted architecture and workflow decisions.
- `patterns/` - reusable implementation or workflow patterns.
- `pitfalls/` - known failure modes and anti-patterns.
- `customer-feedback/` - reviewed customer-facing expectations.
- `study-notes/` - study/scenario-specific observations.
- `demo-scripts/` - stable demo path and narration.
- `eval-cases/` - links from product knowledge to tests/evals.

## Open Design Questions

- Should a personal reviewed wiki remain the source of truth, with project-local runtime copies or caches derived from it?
- Should wiki retrieval be mandatory for Core3-6 once stable, or only when matching pages exist?
- Should the user approve learning in Canvas, Claude popup, or a separate review command?
- Should approved wiki entries be versioned with frontmatter and changelog?

