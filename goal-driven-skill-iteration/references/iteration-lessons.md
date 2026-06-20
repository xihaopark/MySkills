# Iteration Lessons

Use this reference when converting a difficult project run into durable skill improvements.

## The Pattern That Worked

The effective loop was:

1. Create or resume a focused goal.
2. Run the pipeline or acceptance test.
3. Inspect concrete outputs rather than trusting logs.
4. Ask what the user was actually trying to review.
5. Update the skill/tool/report boundary.
6. Re-run and package the result.

This matters because long projects drift. Goal mode keeps the agent attached to the current objective while still allowing multiple implementation and verification passes.

## Common Failure Modes

### The agent optimizes the wrong object

Example:

```text
The generated plot is bad, so fix the generated plotting code.
```

Better:

```text
Why did the workflow not reuse the original plotting code as a stable tool?
```

The lesson belongs in the skill because it changes future behavior.

### Evidence is mistaken for communication

Machine evidence can be exhaustive and still fail as a report. A good skill should instruct the agent to create both:

- an evidence layer for auditability
- a human layer for understanding

### The agent overclaims

Examples of overclaiming:

- "All figures are correct" when only file existence and columns were checked.
- "Decision-ready" when human clinical semantics review is still open.
- "Validated" when only one run passed.

Use weaker, exact claims.

## What To Capture After Each Run

Record:

- Run directory or artifact path.
- Commands executed.
- Tests or checks passed.
- Tests or checks skipped.
- User corrections.
- Output files that matter.
- Open issues and owner.
- Whether the skill should change.

## How To Decide Whether To Patch Code Or Skill

Patch code when the implementation is wrong for the current project.

Patch the skill when future agents are likely to make the same wrong decision.

Patch both when a code change reveals a general operating rule.

## Good Skill Retrospective Output

Good:

```text
Future AZ-like tasks should start by locating the original Rmd plotting functions and extracting them as tools before writing new plotters.
```

Weak:

```text
Fix plots earlier next time.
```

Good:

```text
Human report packs should start with what the project is, how a person uses it, and one representative result per workflow step. Put exhaustive evidence in a secondary appendix.
```

Weak:

```text
Make the report simpler.
```
