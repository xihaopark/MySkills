# 站点中文化维护模块

这个站点采用中文优先的维护策略：面向中文读者组织内容，同时保留关键英文术语，方便检索、实现和 agent 协作。

## 维护原则

- 正文、导航、首页、章节页和 Wiki Home 使用中文主文。
- 关键术语第一次出现时保留英文括注，例如人工介入（HITL）、护栏（guardrails）、评估（evals）、执行框架（harness）。
- URL、文件名、schema 名、命令、代码标识符不翻译。
- 外部文章标题和产品名保留英文，但解释、分类和 takeaways 使用中文。
- 首页和章节页使用 `kb-card` 显式卡片结构，避免 Markdown 卡片被解析错位。

## 维护流程

1. 修改 Markdown 和 `mkdocs.yml`。
2. 运行 `python3 scripts/check-site-translation.py`。
3. 运行 `mkdocs build --strict`。
4. 在浏览器检查首页与章节页。
5. 如果 Wiki 内容变更，运行 `scripts/sync-agent-loop-wiki.sh`。
6. 使用 `mkdocs gh-deploy --force` 发布 GitHub Pages。

## 给后续 Agent 的入口

后续维护者应先读取仓库根目录的 `site-translation-maintenance/SKILL.md`，再更新站点内容。
