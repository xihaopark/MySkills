---
name: bio-analysis-pipeline
description: "Reproduce, audit, and package clinical biostatistics or bioanalysis pipelines from source data, legacy scripts, statistical outputs, figures, and human review requirements. Use when taking on an AZ-like task: porting an existing R/SAS/Rmd analysis workflow, comparing generated tables or plots to origin outputs, extracting reusable plotting/statistical tools, building evidence packs, or preparing human-readable review deliverables for non-technical stakeholders."
---

# Bio Analysis Pipeline

## Purpose

Use this skill to handle an existing biomedical analysis workflow without confusing "the agent produced files" with "the scientific and statistical result is correct." The default strategy is source-first reproduction: identify the original scripts, data contracts, statistical intent, and expected outputs before building new runtime code.

If the task resembles "take this sponsor/vendor/analyst project and make Claude Code run it end to end," treat it as a reproduction and tool-extraction project, not a fresh implementation project.

## Operating Principles

1. Preserve the oracle before optimizing the runtime.
2. Reuse original analysis and plotting code whenever possible.
3. Separate statistical result accuracy, plotting-data accuracy, visual rendering quality, and report usability.
4. Keep machine evidence exhaustive, but keep human reports short and editable.
5. Never claim figure correctness from file existence, column checks, or contract pass alone.

Read `references/lessons.md` when the task involves reviewing a previous failed/unclear run, deciding whether to rewrite vs port legacy code, or designing the report package for mixed technical and business audiences.

## Intake Checklist

Start by locating and inventorying:

- Original source scripts: Rmd, R, SAS, Python, shell, notebooks, and helper libraries.
- Original inputs: raw data, ADaM/SDTM-like tables, mock datasets, metadata, manifests, and config files.
- Original outputs: tables, figures, listings, Word/PDF reports, CSVs, logs, and rendered notebooks.
- Expected comparisons: origin vs generated, source tables vs analysis frames, plotted data vs visual layers.
- Human workflow: who runs the pipeline, who reviews it, which outputs are for machines, and which outputs are for meetings.

Create a run map early:

```text
source scripts -> input data -> intermediate analysis frames -> tables/figures -> evidence -> human report
```

If any arrow is unknown, pause expansion and recover that provenance first.

## Phase 1: Baseline Reproduction

Goal: make the original workflow observable before changing it.

- Run or inspect the original scripts enough to identify table and figure generation logic.
- Capture script sections and line ranges for each output family.
- Build an output inventory with stable IDs, filenames, owners, plot/table classes, source scripts, and source data.
- Preserve original outputs as comparison baselines.
- Record environment requirements and data assumptions instead of silently patching them.

Do not start by rewriting plots from memory. If a figure looks bad, first ask why the original plotting function was not extracted or wrapped.

## Phase 2: Semantic Contract

Goal: define what each output requires before judging whether it is correct.

For each table:

- Identify source table(s), row filters, grouping variables, denominators, statistics, formatting rules, and expected precision.
- Compare generated values against origin values with numeric tolerances and explicit unmatched rows/columns.

For each figure:

- Identify input frame, required columns, grouping variables, endpoint definition, censoring/event logic, exposure/time range, and layer mappings.
- Classify the plotter origin as one of:
  - `legacy_direct`: original code is copied/wrapped directly.
  - `legacy_semantic_port`: original logic is ported into a new runtime module.
  - `new_runtime_plotter`: new plotting code written by the agent.
  - `adapter_preview`: preview generated from partial adapters or mock frames.
  - `unknown`: provenance not established.

Contract pass means the expected files, input frames, and required fields exist. It does not mean visual or statistical accuracy is complete.

## Phase 3: Tool Extraction

Goal: turn trusted legacy logic into stable reusable tools.

Prefer this order:

1. Wrap the original plotting/statistical function with minimal interface changes.
2. Extract the original function and dependencies into a runtime module.
3. Port logic semantically only when direct reuse is impossible.
4. Write new code only when no reliable legacy implementation exists.

When extracting tools:

- Keep input schemas explicit.
- Add smoke tests with tiny deterministic data.
- Add parity tests against original output data or rendered examples when available.
- Keep provenance comments short: original file, function, line range, and intentional deviations.
- Avoid cosmetic rewrites until parity evidence exists.

## Phase 4: Figure Audit

Goal: classify every figure honestly.

Create a per-figure audit table with at least:

- `figure_id`
- `plot_class`
- `baseline_file`
- `generated_file`
- `input_frame`
- `required_columns_present`
- `source_table`
- `source_table_match_status`
- `n_rows_input`
- `n_subjects`
- `n_events`
- `range_checks`
- `plotter_origin`
- `legacy_reference`
- `input_accuracy_status`
- `primary_issue_class`
- `issue_reason`
- `next_action`

Use these issue classes:

- `input_or_statistical_result_error`
- `plot_mapping_or_script_error`
- `rendering_or_visual_encoding_issue`
- `manifest_or_inventory_issue`
- `review_gate_or_clinical_semantics_unconfirmed`
- `pass_current_boundary`

If layer-level plotted-data comparison is not implemented, say so directly. Do not upgrade "contract pass" to "figure accuracy."

## Phase 5: Human Report Package

Goal: explain the project to someone who does not know the pipeline.

Keep the primary package small and editable. Prefer DOCX for business/scientific review unless the user asks for HTML or PDF.

Recommended deliverables:

- One overview DOCX: what this pipeline is, what it takes as input, what it produces, how an analyst/agent interacts with it, what has been validated, and what remains open.
- One main-results DOCX: origin/generated table pairs in editable Word tables.
- One example-comparison DOCX: one representative origin/generated example per output family, plus one table comparison group.
- Optional machine evidence folder or zip only when needed for technical reviewers.

Do not make the first reading path a large side-by-side evidence website unless the audience is explicitly technical. Machine checks belong in an appendix, not the opening narrative.

## Status Language

Use precise claims:

- "Tables matched origin within tolerance" when numeric reproduction evidence exists.
- "Figures passed semantic contract" when files, frames, and required columns exist.
- "Input accuracy audit complete" only after per-figure source/input checks are computed.
- "Ready for review" when evidence is organized for a human reviewer.
- "Decision-ready" only when statistical, visual, and clinical semantics review gates are closed.

Avoid these claims unless proven:

- "All figures are correct."
- "100% figure accuracy."
- "The pipeline is validated."
- "The new plotter matches the original" without origin plotted-data or visual parity evidence.

## Completion Criteria

A run is not complete until it has:

- Reproducible command(s) from clean inputs to outputs.
- Output inventory with source provenance.
- Table reproduction evidence.
- Figure contract and input audit evidence.
- Clear classification of legacy reuse vs new runtime code.
- Human-readable report package tailored to the audience.
- A short list of unresolved issues with owners and next actions.
