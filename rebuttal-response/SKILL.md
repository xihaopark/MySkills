---
name: rebuttal-response
description: Draft, audit, or revise point-by-point academic rebuttal and reviewer-response letters with a concise evidence-first style. Use when responding to reviewer/editor comments, revising a rebuttal, aligning answers with reviewer intent, adding manuscript-change excerpts, inserting real experiment tables, reducing AI-like over-explanation, or making responses sound human, direct, and specific.
---

# Rebuttal Response

## Purpose

Use this skill to write reviewer responses that feel like a careful author answering a concrete request, not a model explaining the paper.

The default style is: **answer every comment directly, say what was added or done, show where it was changed, and put the result there.**

## Core Contract

For each reviewer comment, satisfy this contract:

1. Answer the specific point the reviewer raised.
2. State the concrete action: what was added, revised, rerun, tested, clarified, or cited.
3. Point to the exact manuscript location: section, table, figure, appendix, page if stable.
4. Show evidence in the response itself when useful: revised-text excerpt, real numerical table, figure reference, or citation list.
5. Stop once the concern is answered.

Do not turn a response into a mini introduction, method tutorial, or broad defense of the paper.

## Response Shape

Use this order for most comments:

```text
Thank/acknowledge briefly.
We agree/recognize that [specific issue] was unclear or missing.
To address this, we added/revised/conducted [specific change].
The result/change is shown in [Section/Table/Figure].
[Optional: one-sentence key result.]
```

For experiment-related comments, use the tighter shape:

```text
We thank the reviewer for this suggestion.
To address it, we conducted [new experiment/ablation/rerun].
The results are reported in Table X.
[One sentence: what the numbers show.]
```

The intended feeling is: **you asked for X; we did X; the result is here.**

## Evidence Rules

- Include real experimental results near the relevant answer when the comment asks for validation, ablation, comparison, robustness, statistics, or additional baselines.
- Select evidence strategically. Do not include every experiment simply to appear fair; include the results that directly answer the reviewer, support the revision claim, and can be interpreted cleanly.
- Do not foreground weak, noisy, or unattractive results unless they are necessary to answer the comment or to avoid a misleading claim.
- When a result is mixed but not central, narrow the claim and omit the distracting table rows; use a short limitation sentence instead of giving the weak result extra visual weight.
- Use tables for numbers, not prose summaries disguised as tables.
- Put only experimental variables and metrics in result tables. Avoid columns like `Purpose`, `Interpretation`, `Finding`, or `Conclusion`.
- Bold best values when appropriate.
- Keep captions factual: what comparison the table reports and which comment it addresses.
- If the user says references were added, state that the requested references were added and list or point to them; do not re-argue why they matter unless needed.
- If experiments were rerun, say they were rerun during revision under the revised protocol. Do not imply the earlier work was invalid unless the user explicitly wants that stance.

## Human Style

Prefer short, natural author language:

- "We have added ..."
- "We have revised ..."
- "We conducted additional experiments ..."
- "The results are reported in ..."
- "We added the requested references ..."
- "We now clarify this point in ..."

Avoid AI-like language:

- "This comprehensive analysis demonstrates ..."
- "It is worth noting that ..."
- "To further enhance the manuscript ..."
- "This provides a holistic understanding ..."
- Long paragraphs that explain background before answering the reviewer.

Avoid unnecessary self-criticism:

- Do not say "flaw", "defect", "invalid", or "failed" unless it is true and intended.
- Prefer "was not sufficiently clear", "was missing from the original version", or "needed more detail".

## Comment Alignment

Before editing an answer, identify the reviewer's actual ask:

- Model design / ablation: answer with model-component ablations and design rationale.
- Baselines / fairness: answer with same protocol, reruns, seeds, splits, and result tables.
- Missing citations: say the references were added and where.
- Clarity / writing: say which section or paragraph was rewritten.
- Limitations: add a limitations paragraph without overstating weakness.
- Significance / novelty: explain the difference from closest work, then point to experiments or text changes.

If the current draft answers a different question, rewrite the opening so it addresses the reviewer first.

## Manuscript Excerpts

When useful, include a short revised-manuscript excerpt after the answer:

```latex
\begin{lstlisting}[language=inlineText]
<<Revised Manuscript, Section X.X>>
We added the following clarification:
...
\end{lstlisting}
```

Keep excerpts short. Their job is to prove that the manuscript was changed, not to duplicate the paper.

## Tables

When the project has a manuscript table style, match it. Otherwise use simple booktabs tables.

Load `references/style-and-templates.md` when drafting reusable phrases, LaTeX response blocks, or result-table templates.

## Final Audit

Before finishing a rebuttal pass, check:

- Every reviewer comment has a direct answer.
- Each answer states an action taken.
- Experiment claims have nearby real numbers or a precise table/figure pointer.
- Citation requests say the requested references were added.
- First responses thank the reviewer; later responses do not mechanically repeat thanks.
- Long sentences are split into readable sentences.
- TeX line breaks occur at sentence boundaries when possible.
- No result table is merely a conclusion table.
