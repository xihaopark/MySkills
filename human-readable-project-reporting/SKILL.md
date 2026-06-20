---
name: human-readable-project-reporting
description: "Create human-readable project report packages from complex technical outputs, analysis runs, evidence files, tables, figures, and workflow artifacts. Use when the audience does not already understand the project, when a large evidence pack is too complex, when results need to be presented as editable DOCX or a small package, or when deciding what to show in a 5-10 minute review."
---

# Human Readable Project Reporting

## Purpose

Use this skill to turn complex project outputs into a report package that a real person can read quickly. The goal is not to show every check, but to help the reader understand what the project is, what went in, what came out, what the workflow stages look like, and what still needs review.

Default to editable DOCX when the user wants to revise, comment, or share the report.

## Audience First

Before building a report, identify the reader:

- First-time business or management reader: explain the project, workflow, and representative outputs.
- Scientific or clinical reviewer: show results, boundaries, and review gates.
- Technical reviewer: include evidence files, manifests, diffs, logs, and reproducibility commands.
- Future agent or engineer: include source paths, scripts, config, and acceptance tests.

Do not use one package shape for all audiences.

## What People Usually Need First

For a reader who has not lived inside the project, start with:

1. What is this project?
2. What input does it take?
3. What does the agent/system do?
4. What outputs does it produce?
5. What does each workflow stage look like?
6. What examples should I inspect?
7. What has been checked, and what has not?
8. Where is the final report result?

Do not open with "9/9 tables matched" unless the reader already knows what those tables are.

## Recommended Package Shapes

### Simple human package

Use this when the reader has limited time.

```text
package/
  Main_Report.docx
  examples_by_step/
  all_result_tables_pairs/
  final_report_docx/
  workflow_source/
```

Keep folder depth shallow. One or two clicks should reach the result.

### Full audit package

Use this only when technical traceability matters more than readability.

```text
package/
  index_or_summary.docx
  steps/
    01_step/
      origin_available/
      our_outputs/
      comparison_examples/
      evidence/
```

This is useful for audit but too complex as the primary reading path.

## Report Content Rules

The main report should:

- Use plain language.
- Explain the workflow stages.
- Show one representative example per major output type.
- Include the final report/result document.
- State what is solid and what remains open.
- Link or name where detailed evidence lives.
- Avoid long tables of machine checks in the first pages.

Put exhaustive evidence in an appendix or secondary folder.

## Editable Deliverables

Prefer editable formats when the user says they want to revise the report:

- Use DOCX for narrative reports, workflow summaries, and table comparisons.
- Use editable Word tables for CSV previews or result tables when practical.
- Embed representative plots inside DOCX when the original plot artifact is raster.
- Avoid exposing many loose PNG files unless the user explicitly wants raw image artifacts.

Be explicit about the boundary: embedded raster plots in DOCX are not editable plot layers, but the report text, captions, layout, and tables are editable.

## What Not To Do

Avoid:

- A giant HTML side-by-side comparison as the only entry point.
- Eight documents when the reader has ten minutes.
- Deep folder structures for a management audience.
- Leading with check counts before explaining the workflow.
- Claiming scientific correctness from file generation or schema checks.
- Mixing machine evidence and human narrative without a clear hierarchy.

## Claim Discipline

Use exact status language:

- "Ready for review" means the evidence and examples are organized for humans.
- "Decision-ready" means statistical, visual, and domain review gates are closed.
- "Contract passed" means expected files/columns/frames exist.
- "Input accuracy checked" means the relevant input/source table linkage was verified.
- "Visual parity checked" means layer-level diff or human visual review supports it.

Read `references/reporting-lessons.md` for examples of good and bad package structures.

## Completion Criteria

A report package is complete when:

- The main entry point is obvious.
- A new reader can explain the project after reading the first page.
- The workflow stages are visible.
- Representative results are included.
- Detailed evidence is available but not forced into the first read.
- File count and folder depth match the audience.
- The final result document is included and easy to find.
