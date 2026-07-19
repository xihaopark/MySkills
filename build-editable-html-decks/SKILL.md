---
name: build-editable-html-decks
description: "Create or revise polished single-file HTML presentation decks with 16:9 slide navigation, professional white technical diagrams, large readable typography, inline browser text editing, local persistence, and PNG copy/download for diagrams or full slides. Use when a user asks for an HTML PPT, technical architecture deck, editable web presentation, directly editable slide text, copyable flowcharts, or a presentation that must work from a local HTML file without a frontend server."
---

# Build Editable HTML Decks

Create a presentation as one self-contained HTML file. Treat it as a real slide
deck, not a long webpage divided into sections.

## Start From the Template

Copy `assets/editable-deck-template.html` to the requested destination, then
replace all sample content and the storage key.

Keep the output self-contained unless the user explicitly requests external
assets. Do not add a framework, build process, frontend server, or package
manager for a deck that can work as a local HTML file.

## Build the Narrative First

Before styling:

1. Identify the audience and presentation purpose.
2. Convert the source material into one argument per slide.
3. Put decisions and conclusions in slide titles.
4. Keep supporting text inside diagrams short enough to scan from a distance.
5. Separate customer-facing explanations from internal implementation detail.
6. Remove details that do not help the audience understand or trust the result.

For technical presentations, prefer this order:

```text
problem or journey
  -> architecture decision
  -> current system
  -> complete lifecycle
  -> critical subsystems
  -> verification
  -> invariants or conclusion
```

Do not make every available fact into a slide.

## Visual Contract

Use a professional white daytime style:

- Base canvas: near-white, with a very light technical grid if useful.
- Diagram nodes: pure white backgrounds.
- Meaning: communicate state with borders, top rules, or left rules.
- Text: near-black; secondary text: restrained gray-green.
- Accent palette: green, cyan, amber, coral, and violet.
- Cards: square or lightly rounded, never decorative floating cards.
- Typography: large enough for a projected 1440x900 slide.

Minimum desktop targets:

- Slide title: 48-64 px.
- Diagram section title: 18-26 px.
- Diagram body: 16-18 px.
- Technical labels and filenames: 13-14 px.
- Footer: 11-12 px.

Do not compensate for too much content by shrinking text. Reduce content,
increase node width, or split the slide.

## Diagram Contract

Build diagrams from semantic HTML and CSS so the agent can revise them.

- Add class `diagram` to the primary copyable visual on every slide.
- Use CSS Grid for architecture planes, lanes, matrices, and stage sequences.
- Keep every node background white.
- Use arrows only to express a real dependency or transition.
- Make group names visible when a diagram has branches or parallel lanes.
- Avoid bitmap diagrams as the primary source.
- Avoid SVG for ordinary boxes and arrows; use it only for genuinely graphical
  content that HTML/CSS cannot express clearly.

Each diagram must still be understandable when copied without the slide title.

## Inline Editing Contract

Preserve the template's edit mode:

- `Edit text` toggles terminal text blocks into `contenteditable` elements.
- Do not make nested text elements independently editable.
- Save only changed blocks to `localStorage`, keyed by stable slide and element
  positions.
- Reload saved edits at startup.
- Do not replace the entire deck with saved HTML; doing so would hide future
  source updates.
- Suppress slide navigation keys while the user is typing.
- Let `Escape` leave edit mode.
- Remove editing attributes from export clones.

Explain the persistence boundary accurately: browser edits survive refresh in
that browser, but do not rewrite the source HTML file.

## PNG Export Contract

Preserve both export controls:

- Copy the current primary diagram as PNG.
- Copy the current full slide as PNG.

Render at 2x resolution. Serialize the export clone with `XMLSerializer`, embed
it in SVG `foreignObject`, load it through a base64 data URL, draw it to canvas,
and export PNG.

Use the Clipboard API when available. If clipboard permission is blocked under
`file://`, automatically download the same PNG instead.

Do not generate permanent PNG files next to the HTML unless the user asks for
them.

## Interaction Rules

- Arrow keys, Page Up/Down, Space, Home, and End navigate slides.
- The URL hash identifies the visible slide.
- Editing text must not trigger navigation.
- Controls must remain usable on desktop and mobile.
- Do not place visible usage instructions inside the presentation.
- Use button labels and tooltips for controls.

## Validation

Run the static validator:

```bash
python3 scripts/validate_deck.py /absolute/path/to/deck.html
```

Add `--expected-slides N` when the slide count is fixed.

Then validate with Playwright or an equivalent real browser at:

- Desktop: 1440 x 900.
- Mobile: 390 x 844.

Required behavioral checks:

1. Every slide stays within the desktop viewport.
2. Mobile has no horizontal overflow.
3. Keyboard navigation updates the active slide and progress indicator.
4. Edit mode exposes text blocks and does not create nested editable regions.
5. A modified text block persists after reload.
6. Arrow keys do not navigate while typing.
7. `Escape` exits edit mode.
8. Every diagram and full slide produces a non-empty PNG.
9. Exported PNGs contain the current edited text.
10. No unrelated files are created.

Inspect screenshots of the densest slides. Numeric overflow checks alone do not
prove that the slide is readable.

## Completion

Deliver:

- The HTML file.
- A short description of the controls.
- The validation result.
- Any known persistence or browser-permission limitation.

Do not claim direct source-file editing when the implementation only uses
browser storage.
