#!/usr/bin/env python3
"""Lightweight checks for Chinese-first MySkills docs maintenance."""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

DISALLOWED_UI_PHRASES = [
    "Knowledge Base",
    "Current focus",
    "Recommended reading path",
    "Start Here",
    "Topic Notes",
    "Open section",
    "Browse sources",
    "Read notes",
    "Why it matters:",
    "Key takeaways:",
    "Category:",
    "Created:",
    "Scope:",
]

REQUIRED_FILES = [
    DOCS / "index.md",
    DOCS / "agent-loop-systems" / "index.md",
    DOCS / "agent-loop-systems" / "Home.md",
    DOCS / "agent-loop-systems" / "_Sidebar.md",
    MKDOCS,
]


def has_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def main() -> int:
    failures: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if not has_cjk(text):
            failures.append(f"no Chinese text found: {path.relative_to(ROOT)}")

    for path in [MKDOCS, *DOCS.rglob("*.md")]:
        text = path.read_text(encoding="utf-8")
        for phrase in DISALLOWED_UI_PHRASES:
            if phrase in text:
                failures.append(f"{path.relative_to(ROOT)} contains English UI phrase: {phrase}")

    index = (DOCS / "index.md").read_text(encoding="utf-8")
    section = (DOCS / "agent-loop-systems" / "index.md").read_text(encoding="utf-8")
    for path, text in [
        (DOCS / "index.md", index),
        (DOCS / "agent-loop-systems" / "index.md", section),
    ]:
        if "kb-card" not in text:
            failures.append(f"{path.relative_to(ROOT)} does not use kb-card layout")
        if "grid cards" in text:
            failures.append(f"{path.relative_to(ROOT)} still uses grid cards layout")

    if failures:
        print("Translation maintenance check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Translation maintenance check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
