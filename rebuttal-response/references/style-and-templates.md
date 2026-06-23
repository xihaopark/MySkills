# Rebuttal Style and Templates

## Default Voice

Write like a careful author:

```text
We thank the reviewer for this constructive comment.
We agree that the original manuscript did not sufficiently clarify [issue].
To address this, we have revised Section X.X and added [specific content].
The corresponding results are reported in Table X.
```

Keep the answer short. The reviewer asked for something; the author did it; the evidence is shown.

## Good Opening Sentences

```text
We thank the reviewer for this constructive comment.
We appreciate the reviewer's careful reading.
We agree that this point required a clearer explanation.
We agree that the original manuscript did not provide sufficient detail on this setting.
We recognize that the previous version could cause confusion about this design choice.
```

Use thanks once at the beginning of a reviewer section or for major comments. Do not thank the same reviewer in every small answer unless the target style requires it.

## Action Sentences

```text
In the revised manuscript, we have added ...
We have revised Section X.X to clarify ...
We have added a new paragraph explaining ...
We conducted additional experiments to evaluate ...
We reran all experiments during the major revision under the same protocol.
We added the requested references in Section X.
We added Table X to report the corresponding results.
We now explicitly discuss this limitation in Section X.
```

## Result Sentences

```text
The results are reported in Table X.
The new results show that ...
The comparison confirms that ...
The ablation results indicate that ...
These results support the revised claim that ...
```

Use only one result sentence unless the reviewer asked for detailed interpretation.

## Citation Requests

Use a direct reply:

```text
We thank the reviewer for pointing out these relevant references.
We have added all suggested references to Section X and revised the related discussion accordingly.
```

If listing references:

```text
Specifically, we added citations to [Author, Year], [Author, Year], and [Author, Year] in the revised manuscript.
```

Do not spend a long paragraph explaining that the references are important. The reviewer already thinks they are.

## Experiment / Ablation Template

```latex
\answer{
We thank the reviewer for this suggestion.
To address it, we conducted an additional ablation study on [component/setting].
The results are reported in Table~\ref{tab:r1-ablation}.
They show that [one short numerical conclusion].
}

\begin{table}[t]
\centering
\caption{Additional ablation results for Comment R1.X. Best results are highlighted in bold.}
\label{tab:r1-ablation}
\begin{tabular}{lcccc}
\toprule
Method & Dataset & Horizon & MSE & MAE \\
\midrule
Baseline & ETTh1 & 96  & 0.000 & 0.000 \\
Variant A & ETTh1 & 96 & 0.000 & 0.000 \\
Proposed & ETTh1 & 96 & \textbf{0.000} & \textbf{0.000} \\
\bottomrule
\end{tabular}
\end{table}
```

## Manuscript Excerpt Template

```latex
\begin{lstlisting}[language=inlineText]
<<Revised Manuscript, Section X.X>>
We added the following clarification:
...
\end{lstlisting}
```

Use excerpts for rewritten definitions, experimental settings, limitation paragraphs, and new related-work text.

## Table Rules

- Use real data values.
- Use judgment about which real values to show. Rebuttal tables are not experiment dumps; they should contain the rows needed to answer the current reviewer concern.
- Do not add unattractive or noisy rows only to look balanced. If those rows weaken the main point and are not required by the reviewer, omit them and narrow the claim.
- Use method/dataset/horizon/metric columns for forecasting and ML experiments.
- Use `\toprule`, `\midrule`, and `\bottomrule` unless the manuscript has a different established style.
- Keep result precision consistent with the paper.
- Bold best values, not whole rows.
- Do not add explanatory columns such as `Purpose`, `Takeaway`, `Evidence`, or `Interpretation`.
- If many datasets or horizons are included, match the manuscript's main-table grouping style.

## Phrases to Avoid

Avoid:

```text
tried our best
totally agree
flaw in our approach
I think
Thank for your comments
This comprehensive analysis
holistic understanding
significantly enhances the manuscript
```

Prefer:

```text
revised the manuscript accordingly
we agree that
this point was not sufficiently clear
we have added
we conducted
the results are reported in
```

## Short Review Checklist

For each response, ask:

```text
What exactly did the reviewer ask?
Did we answer that exact ask in the first two sentences?
Did we say what we changed or did?
Did we show the result or point to it?
Can one paragraph be deleted without losing the answer?
```
