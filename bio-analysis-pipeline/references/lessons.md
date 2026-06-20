# Lessons From AZ-Like Bioanalysis Pipeline Work

Use this reference when the task has already become confusing, the agent has produced many artifacts, or the team needs to decide what to trust.

## The Main Failure Mode

The common failure is treating an agent-generated runtime as the source of truth. In an AZ-like task, the original analyst scripts and outputs are the oracle until proven otherwise.

Bad framing:

```text
Our generated plotting code has bugs, so fix the generated plotting code.
```

Better framing:

```text
Why did we not extract the original plotting code into a reusable tool, and where did the generated code diverge from it?
```

## What Went Right In The Reference Case

- Table reproduction was strong because origin tables and generated tables were compared directly.
- Semantic contracts were useful because they forced each figure to declare required inputs and columns.
- An acceptance run was useful because it proved the workflow could execute end to end.
- Splitting machine evidence from human presentation made the result easier to explain.

## What Went Wrong

- "Figure exists" and "contract passes" were initially too easy to confuse with "figure is correct."
- New plotting code was written before sufficiently extracting the original plotting functions.
- A large comparison pack was useful as evidence but poor as a first-read report.
- PNG-heavy delivery was not ideal for stakeholders who wanted editable review documents.
- Script provenance was not explicit enough: reviewers needed to know which outputs came from original code, semantic ports, or new runtime code.

## Recommended Reset When Things Get Messy

Pause new feature work and create three inventories:

1. Output inventory: every table/figure/listing, its baseline file, generated file, and owner.
2. Provenance inventory: source script, function, line range, data frame, filters, and endpoint logic.
3. Issue inventory: input/statistical error, plot mapping error, rendering issue, manifest issue, clinical review gate, or pass within current boundary.

Then choose the next action by issue type:

- Statistical/input errors require data-frame and source-table debugging.
- Plot mapping errors require checking aesthetics, grouping, endpoints, censoring, and layer data.
- Rendering issues require styling/layout fixes after data parity is credible.
- Manifest issues require inventory or file naming fixes.
- Clinical semantics gates require human domain review and should not be closed by code alone.

## How To Start A New AZ-Like Task

Start with a narrow reproduction slice:

1. Pick one table and one figure family that represent the core statistical logic.
2. Run or inspect the original script section that produced them.
3. Save origin output, generated output, and intermediate input frames.
4. Build a minimal comparison harness.
5. Only then generalize to all outputs.

This prevents building a polished runtime around unverified assumptions.

## Reporting For Different Audiences

For technical reviewers:

- Include manifests, CSV diffs, contract tables, logs, plotted-data summaries, and reproducible commands.
- Keep filenames stable and machine-readable.

For business or management readers:

- Start with what the system does, how a person uses it, and what a stage output looks like.
- Show one representative example per result type.
- Put detailed evidence in an appendix or separate technical folder.
- Prefer DOCX when the reader needs to edit, comment, or reuse the report.

Chinese stakeholder wording that usually works:

```text
这份材料不是让读者检查每一个 CSV，而是让读者在十分钟内理解：
我们拿到了什么输入，Claude Code 做了什么，产出了什么结果，
哪些结果已经和原始结果对齐，哪些还只是通过了结构检查，
下一步需要谁看、看什么。
```

## Claim Discipline

Use boundary-aware language:

- Say "table reproduction passed" only when numeric table comparison passed.
- Say "figure semantic contract passed" only when the expected artifact and required input fields exist.
- Say "input audit passed" only when input frames and source-table links have been checked.
- Say "visual parity passed" only when layer-level plotted data or human visual review supports it.
- Say "ready for review" before "decision-ready."

When unsure, choose the weaker claim and add the missing evidence as the next action.
