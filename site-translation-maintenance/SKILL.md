---
name: site-translation-maintenance
description: "Maintain the MySkills documentation site for Chinese readers. Use when adding or revising docs, navigation, MkDocs pages, GitHub Wiki pages, source indexes, or translation style for this repository."
---

# Site Translation Maintenance

## Purpose

Use this skill to keep the MySkills documentation site readable for Chinese readers while preserving important English technical terms.

The site is not an English docs mirror. It is a Chinese-first knowledge base with English terms kept only when they help future search, implementation, or agent collaboration.

## Translation Contract

For user-facing site content:

1. Use Chinese as the main language.
2. Keep key technical terms in English on first mention, usually in parentheses:
   - 人工介入（HITL）
   - 护栏（guardrails）
   - 评估（evals）
   - 执行框架（harness）
   - 任务移交（handoff）
   - 可观测性（observability）
3. Keep URLs, file names, schema names, code identifiers, and command names unchanged.
4. Preserve article titles and product names in English when they are source titles:
   - Anthropic - Building Effective Agents
   - ReAct
   - Reflexion
5. Translate explanatory fields such as category, why it matters, key takeaways, reading path, and page summaries.
6. Avoid machine-translation tone. Prefer concise Chinese with stable technical wording.

## Navigation Rules

MkDocs navigation should be Chinese-first:

- Good: `人工介入与护栏（HITL / Guardrails）`
- Good: `外部资料索引（Source Index）`
- Weak: `Human-in-the-Loop and Guardrails`
- Weak: `Source Index`

Top-level UI should use Chinese labels. English may appear as a search keyword or term annotation, not as the main label.

## Page Layout Rules

Do not use Markdown list cards inside raw HTML when the visual result matters. Use explicit HTML card markup:

```html
<section class="kb-grid" markdown>
<a class="kb-card" href="...">
  <span class="kb-card__eyebrow">中文标签 English Term</span>
  <strong>中文标题</strong>
  <span>中文说明。</span>
</a>
</section>
```

This prevents MkDocs/Markdown parsing from splitting a card title, body, and link into different visual columns.

## Maintenance Workflow

1. Update Markdown and `mkdocs.yml`.
2. Run `python3 scripts/check-site-translation.py`.
3. Run `mkdocs build --strict`.
4. Inspect the homepage in the browser at desktop width.
5. If Wiki pages changed, run `scripts/sync-agent-loop-wiki.sh`.
6. Deploy with `mkdocs gh-deploy --force`.

## Review Checklist

- Site title, nav, homepage, section pages, and Wiki Home are Chinese-first.
- Professional terms are annotated, not blindly translated away.
- Source Index keeps all source URLs.
- Cards render as complete cards: eyebrow, title, description, and link target stay together.
- Chinese paragraphs have comfortable line height and no overly wide reading line.
- No English-only UI labels remain unless they are proper nouns or technical terms.
