# Notes 05: Community Risks and Counterpoints

## Why Include Skeptical Sources

Loop engineering is a useful framing, but community discussions repeatedly warn that loops can amplify existing system weaknesses. For a scientific workflow agent, these critiques are more valuable than hype.

## Recurrent Critiques

### Cost and Token Burn

Reddit and Business/tech press discussions repeatedly point out that long loops, subagents, and repeated file reads can become expensive.

Reusable implications:

- Add iteration, time, and token/effort budgets.
- Scale effort by task complexity.
- Avoid subagents when deterministic checks suffice.
- Prefer compact artifacts and wiki attention packets over broad repo rereads.

### Verification Bottleneck

HN discussions emphasize that the loop is only as good as the feedback it closes against.

Reusable implications:

- Core3-6 "done" must be checkable by artifacts, gates, audit state, and user-visible summaries.
- Tests should verify behavior/evidence, not only that files exist.
- Reviewer/auditor loops should be independent from the runner.

### Learning From Bad Context

The "learn from your worst code" critique maps directly to A scientific workflow agent wiki risks.

Reusable implications:

- Do not auto-promote runtime observations into reviewed memory.
- Deprecate stale docs explicitly.
- Make wiki status visible.
- Retrieval should cite page path/version, so users can correct the memory source.

### Over-Agentification

Several sources caution that flat multi-agent systems add coordination failure. Cursor's scaling writeup shows brittle locks and status files when too many agents self-coordinate.

Reusable implications:

- Keep Core3-6 as deterministic workflow plus small number of bounded roles.
- Avoid group chat for normal run execution.
- Use planner/runner/evaluator only where each role has a clear contract.

### False "Done"

Long-running agents often stop because context is full, tests are shallow, or they believe a checklist is enough.

Reusable implications:

- Completion predicates should be explicit.
- Core6 should remain conservative: review-ready is not final-report-ready.
- Main conversation should show "what remains unresolved" every time.

## Practical Counter-Balance for AZ

The stable product should not sell "autonomy." It should sell:

- repeatability;
- traceability;
- clear human decision points;
- artifact-backed claims;
- reviewed memory;
- lower manual prompting burden.

