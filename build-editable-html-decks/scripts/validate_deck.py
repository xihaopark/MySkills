#!/usr/bin/env python3
"""Validate the static contract of a self-contained editable HTML slide deck."""

from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_IDS = {
    "toggleEdit",
    "copyDiagram",
    "copySlide",
    "prev",
    "next",
    "progress",
    "copyToast",
}

REQUIRED_TOKENS = {
    "renderElementPng": "PNG renderer",
    "localStorage": "browser edit persistence",
    "contenteditable": "inline edit mode",
    "XMLSerializer": "XML-safe export serialization",
    "ClipboardItem": "clipboard PNG support",
    "downloadPng": "PNG download fallback",
}


class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slides: list[dict[str, str]] = []
        self.ids: list[str] = []
        self.diagrams = 0
        self.external_assets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        classes = set(attr.get("class", "").split())

        if tag == "section" and "slide" in classes:
            self.slides.append(attr)
        if "diagram" in classes:
            self.diagrams += 1
        if attr.get("id"):
            self.ids.append(attr["id"])

        if tag == "script" and attr.get("src"):
            self.external_assets.append(attr["src"])
        if tag == "link" and attr.get("href"):
            self.external_assets.append(attr["href"])
        if tag in {"img", "video", "audio", "source"}:
            source = attr.get("src", "")
            if source and not source.startswith("data:"):
                self.external_assets.append(source)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Path to the HTML slide deck")
    parser.add_argument("--expected-slides", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []

    if not args.html.is_file():
        print(f"ERROR: file not found: {args.html}", file=sys.stderr)
        return 1

    text = args.html.read_text(encoding="utf-8")
    parser = DeckParser()
    parser.feed(text)

    if not parser.slides:
        errors.append("no <section class=\"slide\"> elements found")
    if args.expected_slides is not None and len(parser.slides) != args.expected_slides:
        errors.append(
            f"expected {args.expected_slides} slides, found {len(parser.slides)}"
        )
    if parser.diagrams < len(parser.slides):
        errors.append(
            f"found {parser.diagrams} .diagram elements for {len(parser.slides)} slides"
        )

    duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicate_ids:
        errors.append(f"duplicate IDs: {', '.join(duplicate_ids)}")

    missing_ids = sorted(REQUIRED_IDS - set(parser.ids))
    if missing_ids:
        errors.append(f"missing control IDs: {', '.join(missing_ids)}")

    for token, capability in REQUIRED_TOKENS.items():
        if token not in text:
            errors.append(f"missing {capability}: token {token!r}")

    if parser.external_assets:
        errors.append(
            "deck is not self-contained; external assets: "
            + ", ".join(parser.external_assets)
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "OK: "
        f"{len(parser.slides)} slides, "
        f"{parser.diagrams} diagrams, "
        f"{len(parser.ids)} unique IDs, "
        "inline editing and PNG export hooks present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
