# Notes 03: Verification, Evals, and Observability

## Central Pattern

The external consensus is that agent loops move the bottleneck from generation to verification.

The loop should answer:

- What objective was attempted?
- What tools/actions were used?
- What artifacts were produced?
- What checks passed or failed?
- What did the user approve?
- What remains blocked?
- What evidence supports "done"?

## Verification Layers

Recommended layers for Scientific workflow agent:

1. Schema/contract tests: artifact names, columns, status enums, run-id isolation.
2. Data audit: source dependency, data quality, denominator, missingness, provenance.
3. Visual/figure audit: manifest, non-empty outputs, style/semantic contracts.
4. Model audit: ready/skip status, min event threshold, interpretation boundary.
5. User-facing review: concise attention packet, not raw debug.
6. End-to-end eval: repeat mock run and compare run structure, gates, selected result, wiki retrieval.

## Harness-First Verification

Datadog's harness-first framing is useful:

- The harness should verify quickly and automatically.
- Human review should focus on high-value judgment, not scanning every raw event.
- Telemetry/observability closes the loop when test harness assumptions diverge from reality.

Reusable mapping:

- Core3-6 need machine-verifiable step reports.
- The main conversation should hide raw/system/tool debug by default.
- Raw events, tool invocations, snapshots, and artifacts must remain traceable.

## Evals as Product Memory

Anthropic and LangChain both frame evals as lifecycle assets:

- Start with a small set of realistic use cases.
- Add interesting failures from manual testing.
- Let human reviewers annotate traces/evals.
- Use eval deltas before changing prompts/tools/harness.

Reusable mapping:

- Customer feedback items should produce acceptance/eval cases.
- Core3-6 demo failures should be converted into tests or checklist rows.
- Wiki candidates and eval candidates are related but separate:
  - wiki stores reviewed project knowledge;
  - evals store behavior that must remain true.

## Observability Requirements

For each formal run, preserve:

- run id and display name separately;
- cwd / project root / plugin root;
- core start/end status;
- model/tool/handoff events, if available;
- file artifacts and manifests;
- gate request/decision;
- selected result context additions;
- wiki retrieval log;
- learning candidate log;
- audit/action item output.

## Open Design Questions

- Should Core3-6 each emit a compact `attention_packet.md` plus `attention_packet.json`?
- Should "done" for each core be a predicate over artifacts/gates/audits rather than a script exit code?
- Should Core6 aggregate not only review gates but also "user visible unresolved decisions"?

