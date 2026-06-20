# Reporting Lessons

Use this reference when simplifying a report package or deciding what humans should see first.

## Main Lesson

Evidence is not the same thing as explanation. A report can contain correct files and still fail if the reader cannot tell what the project does.

For unfamiliar audiences, start with the story of the workflow:

```text
Input -> agent workflow -> intermediate stages -> representative outputs -> final report -> review boundary
```

## What Worked

- A short DOCX as the main entry point.
- One representative example per workflow step.
- All result table pairs kept together, but outside the first narrative path.
- Final report DOCX placed in a clearly named folder.
- Source scripts and extracted tools included as a separate reference folder.
- Shallow folder structure.

## What Did Not Work

- A large comparison pack as the main deliverable.
- Many CSVs and PNGs without a reading path.
- Deep `origin/our/evidence` folders under every step for a non-technical reader.
- Starting with counts like "9/9 passed" before explaining what was being counted.
- Delivering raw PNG folders when the user wanted editable Word documents.

## Practical Package Progression

Start with the smallest package that answers the reader's question:

```text
Main_Report.docx
examples_by_step/
all_result_tables_pairs/
final_report_docx/
workflow_source/
```

Add a full audit package only when someone asks for traceability.

## Ten-Minute Review Test

Before shipping, ask:

- Can the reader identify the project in 30 seconds?
- Can the reader see the workflow stages on page 1?
- Can the reader open one folder and see examples, not a maze?
- Are the final deliverables obvious?
- Are details available without dominating the entry path?
- Is the number of documents realistic for the meeting?

If not, simplify.

## Good Wording

Use:

```text
这份材料让读者按 workflow 看：每一步做了什么、代表性结果长什么样、哪些地方有 origin 对照、最终报告在哪里。
```

Avoid:

```text
我们通过了很多 checks，所以这个包可以看。
```

The reader needs orientation before metrics.
