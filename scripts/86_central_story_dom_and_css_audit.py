#!/usr/bin/env python3
"""
B86 - Central story DOM and CSS audit

Purpose:
- Stop guessing at CSS selectors after B85 did not change the visible central map stage.
- Inspect the actual production DOM and CSS around #centralGlobalMapStory.
- Report:
  - section opening tag,
  - immediate child elements,
  - class/id inventory,
  - data-global-state articles,
  - likely map containers,
  - relevant CSS rules and JS selectors.
- Do not modify production website files.

Outputs:
- docs/B86_central_story_dom_and_css_audit.md
- docs/B86_central_story_section_excerpt.html
- tasks/done.md

Does NOT:
- modify index.html
- modify CSS
- modify JavaScript
- alter maps/data/assets
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SRC = ROOT / "src"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REPORT = DOCS / "B86_central_story_dom_and_css_audit.md"
EXCERPT = DOCS / "B86_central_story_section_excerpt.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def find_element_bounds(text: str, tag: str, start_pattern: str):
    m = re.search(start_pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    start = m.start()
    open_end = m.end()
    token_re = re.compile(rf"</?{tag}\b[^>]*>", flags=re.IGNORECASE | re.DOTALL)
    depth = 1
    for tm in token_re.finditer(text, open_end):
        token = tm.group(0)
        if token.lower().startswith(f"</{tag.lower()}"):
            depth -= 1
            if depth == 0:
                return start, open_end, tm.start(), tm.end()
        else:
            depth += 1
    return None


@dataclass
class Element:
    depth: int
    tag: str
    attrs: dict[str, str]


class SectionParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.elements: list[Element] = []
        self.text_bits: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = {k: (v or "") for k, v in attrs}
        self.elements.append(Element(self.depth, tag.lower(), d))
        self.depth += 1

    def handle_endtag(self, tag):
        self.depth = max(0, self.depth - 1)

    def handle_data(self, data):
        s = data.strip()
        if s:
            self.text_bits.append(s)


def attr_summary(attrs: dict[str, str]) -> str:
    parts = []
    for key in ["id", "class", "data-global-state", "data-retired", "aria-hidden", "hidden", "style"]:
        if key in attrs:
            val = attrs[key]
            if key == "style" and len(val) > 90:
                val = val[:90] + "..."
            parts.append(f'{key}="{val}"')
    return " ".join(parts)


def grep_css(css: str) -> list[str]:
    terms = [
        "centralGlobalMapStory",
        "central-map",
        "central-story",
        "data-global-state",
        "map-stage",
        "map-frame",
        "sticky",
        "b79",
        "b80",
        "b81",
        "b82",
        "b83",
        "b84",
        "b85",
    ]
    lines = css.splitlines()
    hits = []
    for i, line in enumerate(lines, start=1):
        low = line.lower()
        if any(t.lower() in low for t in terms):
            hits.append(f"{i}: {line.rstrip()}")
    return hits


def grep_js_selectors() -> list[str]:
    hits = []
    patterns = [
        "centralGlobalMapStory",
        "data-global-state",
        "querySelector",
        "textContent",
        "classList",
        "style.",
    ]
    for path in sorted(SRC.glob("*.js")):
        txt = read(path)
        for i, line in enumerate(txt.splitlines(), start=1):
            low = line.lower()
            if any(p.lower() in low for p in patterns) and ("central" in low or "global-state" in low or "textcontent" in low):
                hits.append(f"{rel(path)}:{i}: {line.rstrip()}")
    return hits


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    html = read(INDEX)
    css = read(CSS) if CSS.exists() else ""

    bounds = find_element_bounds(
        html,
        "section",
        r"<section\b(?=[^>]*\bid=[\"']centralGlobalMapStory[\"'])[^>]*>",
    )

    if not bounds:
        report = f"""# B86 - Central Story DOM and CSS Audit

Date: {today}

## Result

FAIL: `#centralGlobalMapStory` was not found in `index.html`.

This explains why CSS targeting `#centralGlobalMapStory` would not affect the visible central story.
"""
        write(REPORT, report)
        print("B86 audit complete: centralGlobalMapStory not found.")
        print(f"Changed/created: {rel(REPORT)}")
        return

    start, open_end, close_start, close_end = bounds
    section_html = html[start:close_end]
    opening_tag = html[start:open_end]
    write(EXCERPT, section_html)

    parser = SectionParser()
    parser.feed(section_html)

    class_counter: Counter[str] = Counter()
    id_counter: Counter[str] = Counter()
    tag_counter: Counter[str] = Counter()
    state_elements = []
    immediate_children = []
    likely_map = []

    for el in parser.elements:
        tag_counter[el.tag] += 1
        if el.attrs.get("class"):
            for cls in el.attrs["class"].split():
                class_counter[cls] += 1
        if el.attrs.get("id"):
            id_counter[el.attrs["id"]] += 1
        if el.attrs.get("data-global-state"):
            state_elements.append(el)
        if el.depth == 1:
            immediate_children.append(el)

        text = " ".join([el.tag, el.attrs.get("id", ""), el.attrs.get("class", ""), el.attrs.get("data-global-state", "")]).lower()
        if any(k in text for k in ["map", "layer", "stage", "visual", "sticky", "frame"]):
            likely_map.append(el)

    immediate_md = "\n".join(
        f"- depth={el.depth} `<{el.tag}>` {attr_summary(el.attrs)}"
        for el in immediate_children[:80]
    ) or "- none"

    states_md = "\n".join(
        f"- depth={el.depth} `<{el.tag}>` {attr_summary(el.attrs)}"
        for el in state_elements
    ) or "- none"

    map_md = "\n".join(
        f"- depth={el.depth} `<{el.tag}>` {attr_summary(el.attrs)}"
        for el in likely_map[:120]
    ) or "- none"

    classes_md = "\n".join(f"- `{cls}`: {n}" for cls, n in class_counter.most_common(100)) or "- none"
    ids_md = "\n".join(f"- `{id_}`: {n}" for id_, n in id_counter.most_common(80)) or "- none"
    tags_md = "\n".join(f"- `{tag}`: {n}" for tag, n in tag_counter.most_common(50)) or "- none"

    css_hits = grep_css(css)
    css_md = "\n".join(f"- `{h}`" for h in css_hits[-220:]) or "- none"

    js_hits = grep_js_selectors()
    js_md = "\n".join(f"- `{h}`" for h in js_hits[:220]) or "- none"

    text_snippets = [t for t in parser.text_bits if len(t) <= 160]
    text_md = "\n".join(f"- {t}" for t in text_snippets[:120]) or "- none"

    report = f"""# B86 - Central Story DOM and CSS Audit

Date: {today}

## 1. Purpose

B85 did not visibly change the central map stage. That means our CSS selectors are not matching the actual controlling wrappers, or a later/stronger rule or script positioning is overriding the intended stage styling.

B86 does not modify the website. It records the actual DOM and relevant CSS/JS so the next patch can target the real elements instead of guessing.

## 2. Section opening tag

```html
{opening_tag}
```

## 3. Immediate children of `#centralGlobalMapStory`

{immediate_md}

## 4. `data-global-state` elements

{states_md}

## 5. Likely map/stage/layer elements

{map_md}

## 6. Class inventory inside central section

{classes_md}

## 7. ID inventory inside central section

{ids_md}

## 8. Tag inventory

{tags_md}

## 9. Text snippets inside central section

{text_md}

## 10. Relevant CSS hits

Showing the last relevant hits, because later CSS usually wins.

{css_md}

## 11. Relevant JS hits

{js_md}

## 12. Raw excerpt

The full central section was written to:

- `docs/B86_central_story_section_excerpt.html`

## 13. Next step

Use this report to create B87 with selectors that match the actual DOM. Avoid another blind CSS patch.
"""
    write(REPORT, report)

    done_entry = f"""
## B86 - Central story DOM and CSS audit ({today})

- Audited the actual `#centralGlobalMapStory` DOM and relevant CSS/JS.
- Created `docs/B86_central_story_dom_and_css_audit.md`.
- Created `docs/B86_central_story_section_excerpt.html`.
- Did not modify production HTML, CSS, JS, maps or data.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B86 - Central story DOM and CSS audit" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B86 central story DOM and CSS audit complete.")
    print("Changed/created:")
    print(f"  {rel(REPORT)}")
    print(f"  {rel(EXCERPT)}")
    print(f"  {rel(DONE)}")
    print("")
    print("Please post these excerpts:")
    print('  Select-String -Path docs\\B86_central_story_dom_and_css_audit.md -Pattern "Immediate children|data-global-state|Likely map|Class inventory|Relevant CSS hits" -Context 0,35')


if __name__ == "__main__":
    main()
