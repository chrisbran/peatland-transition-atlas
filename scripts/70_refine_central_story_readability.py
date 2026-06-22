#!/usr/bin/env python3
"""
B70 - Refine central story readability

Purpose:
- Improve the readability of the central PNG sticky-map story.
- Make every central map step answer one simple question:
  What scale are we at, what is being added, and why does it matter?
- Keep state names, layer bindings, images, scripts and data untouched.

Changes:
- Rewrite text inside .central-map-step articles in #centralGlobalMapStory.
- Add a short "read the map sequence" note to the central story intro if not present.
- Add compact CSS refinements for central step readability.
- Create docs/B70_refine_central_story_readability.md.
- Update tasks/done.md.

Does NOT:
- change data-global-state values,
- change central JS state metadata,
- change map PNG assets,
- remove scripts,
- delete sections.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

STEP_TEXT = {
    "extent": {
        "span": "01 · Extent",
        "h3": "Where are the world’s peatlands?",
        "p": "Start with the spatial base layer: peatland extent. This is the area where transition questions can arise."
    },
    "total": {
        "span": "02 · Pressure",
        "h3": "Where does peatland pressure accumulate?",
        "p": "Total emissions highlight countries where peatland drainage creates large absolute climate pressure."
    },
    "density": {
        "span": "03 · Intensity",
        "h3": "Where is pressure most concentrated?",
        "p": "Emission density shifts the view from large countries to places where pressure is intense relative to area."
    },
    "compare": {
        "span": "04 · Reading hotspots",
        "h3": "Total and density tell different stories.",
        "p": "A hotspot can matter because it is large, intense, or both. The atlas keeps both readings visible."
    },
    "europe-borders": {
        "span": "05 · Europe",
        "h3": "Europe turns global pressure into policy context.",
        "p": "The European frame links peatland transition to regulation, agricultural land use and implementation capacity."
    },
    "europe-peat": {
        "span": "06 · European extent",
        "h3": "Peatland patterns continue across borders.",
        "p": "European peatlands form a shared transition space, but implementation still depends on national and regional settings."
    },
    "germany-context": {
        "span": "07 · Germany",
        "h3": "Germany is an implementation scale.",
        "p": "The national frame connects peatland transition to agricultural policy, planning responsibilities and data availability."
    },
    "germany-thuenen-extent": {
        "span": "08 · Thuenen Kulisse",
        "h3": "The national transition area becomes concrete.",
        "p": "The Thuenen Kulisse translates broad peatland context into mapped organic-soil and moor-related implementation areas."
    },
    "germany-thuenen-types": {
        "span": "09 · Soil context",
        "h3": "Different soil contexts imply different pathways.",
        "p": "Moor and soil categories help distinguish where rewetting, wet use, grazing or other transition options may be plausible."
    },
    "bw-context": {
        "span": "10 · Baden-Wuerttemberg",
        "h3": "The story reaches regional planning scale.",
        "p": "Baden-Wuerttemberg narrows the national frame to a region where land-use conflicts and practical implementation can be discussed."
    },
    "bw-bk50-extent": {
        "span": "11 · BK50 context",
        "h3": "BK50 shows the regional peat and wetland soil context.",
        "p": "This layer shows where relevant soil contexts occur. It does not yet classify land use, suitability or priority."
    },
}

INTRO_NOTE = """
      <p class="central-story-read-note">
        Read the sequence as a scale transition: peatland extent first, pressure second,
        implementation context third, pathway interpretation last.
      </p>
"""

CSS_BLOCK = """
/* B70 central story readability pass */
.central-story-read-note {
  max-width: 780px;
  color: var(--muted);
  font-size: 0.94rem;
  line-height: 1.55;
  margin-top: 0.75rem;
}

.central-map-step span {
  letter-spacing: 0.06em;
}

.central-map-step h3 {
  max-width: 30rem;
}

.central-map-step p {
  max-width: 31rem;
  line-height: 1.48;
}

.central-map-step[data-global-state="extent"] h3,
.central-map-step[data-global-state="total"] h3,
.central-map-step[data-global-state="density"] h3,
.central-map-step[data-global-state="compare"] h3,
.central-map-step[data-global-state="europe-borders"] h3,
.central-map-step[data-global-state="europe-peat"] h3,
.central-map-step[data-global-state="germany-context"] h3,
.central-map-step[data-global-state="germany-thuenen-extent"] h3,
.central-map-step[data-global-state="germany-thuenen-types"] h3,
.central-map-step[data-global-state="bw-context"] h3,
.central-map-step[data-global-state="bw-bk50-extent"] h3 {
  text-wrap: balance;
}
"""

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")

def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def article_pattern(state: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?P<open><article\b(?=[^>]*\bclass=["\'][^"\']*\bcentral-map-step\b[^"\']*["\'])(?=[^>]*\bdata-global-state=["\']{re.escape(state)}["\'])[^>]*>)'
        rf'(?P<body>[\s\S]*?)'
        rf'(?P<close></article>)',
        re.IGNORECASE,
    )

def replace_or_insert_tag(body: str, tag: str, text: str) -> str:
    pattern = re.compile(rf'<{tag}\b[^>]*>[\s\S]*?</{tag}>', re.IGNORECASE)
    repl = f'<{tag}>{text}</{tag}>'
    if pattern.search(body):
        return pattern.sub(repl, body, count=1)
    return "\n      " + repl + body

def replace_step(html: str, state: str, spec: dict[str, str]) -> tuple[str, bool]:
    pat = article_pattern(state)
    m = pat.search(html)
    if not m:
        return html, False

    body = m.group("body")
    body = replace_or_insert_tag(body, "span", spec["span"])
    body = replace_or_insert_tag(body, "h3", spec["h3"])
    body = replace_or_insert_tag(body, "p", spec["p"])

    # Normalize body indentation lightly.
    body = "\n      " + "\n      ".join(
        line.strip() for line in body.strip().splitlines() if line.strip()
    ) + "\n    "

    new_article = m.group("open") + body + m.group("close")
    html = html[:m.start()] + new_article + html[m.end():]
    return html, True

def add_intro_note(html: str) -> str:
    if "central-story-read-note" in html:
        return html

    # Insert after the first centralGlobalMapStory section heading paragraph block if possible.
    section_m = re.search(
        r'(<section\b(?=[^>]*\bid=["\']centralGlobalMapStory["\'])[\s\S]*?<div class=["\']section-heading["\'][^>]*>)(?P<body>[\s\S]*?)(</div>)',
        html,
        flags=re.IGNORECASE,
    )
    if not section_m:
        return html

    body = section_m.group("body")
    # Add before closing section-heading div.
    new_body = body.rstrip() + "\n" + INTRO_NOTE
    return html[:section_m.start("body")] + new_body + html[section_m.end("body"):]

def patch_css(css: str) -> str:
    if "/* B70 central story readability pass */" in css:
        return css
    return css.rstrip() + "\n\n" + CSS_BLOCK.strip() + "\n"

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read(INDEX)

    if 'id="centralGlobalMapStory"' not in html and "id='centralGlobalMapStory'" not in html:
        raise RuntimeError("Missing #centralGlobalMapStory. Refusing B70 patch.")

    changed_states = []
    missing_states = []

    for state, spec in STEP_TEXT.items():
        html, ok = replace_step(html, state, spec)
        if ok:
            changed_states.append(state)
        else:
            missing_states.append(state)

    if missing_states:
        raise RuntimeError(f"Missing central story step articles for states: {missing_states}")

    html = add_intro_note(html)
    write(INDEX, html)

    css = read(CSS)
    write(CSS, patch_css(css))

    doc = f"""# B70 - Refine Central Story Readability

Date: {date.today().isoformat()}

## 1. Purpose

B70 improves the readability of the central PNG sticky-map story.

The goal is not to add more information. The goal is to make each step easier to read and easier to understand.

## 2. Changed files

- `index.html`
- `src/styles.css`
- `docs/B70_refine_central_story_readability.md`
- `tasks/done.md`

## 3. Updated central story states

{chr(10).join(f"- `{state}`" for state in changed_states)}

## 4. Readability rule

Each step should answer one simple question:

1. What scale are we at?
2. What layer or signal is being added?
3. Why does it matter for peatland transition?

## 5. What B70 does not change

B70 does not:

- change `data-global-state` values,
- change central JS state metadata,
- change layer opacity logic,
- change PNG assets,
- remove scripts,
- remove sections,
- remove data files.

## 6. Next recommended patch

Recommended B71:

`B71_refine_central_story_meta_panel`

Scope:

- only if needed after visual review,
- align the central map panel titles/sources with the clearer step wording,
- do not change state names or layer bindings.

## 7. Visual QA checklist

After B70:

1. The central story step texts are shorter and more functional.
2. The map sequence still moves through all 11 states.
3. No central map layer disappears unexpectedly.
4. Lower evidence modules still render.
5. No legacy guided story or six-part story is visible.
"""

    write(DOCS / "B70_refine_central_story_readability.md", doc)

    done_entry = f"""
## B70 - Refine central story readability ({date.today().isoformat()})

- Rewrote central sticky-map step text for clarity and shorter interpretation.
- Added a compact read-note explaining the scale-transition sequence.
- Added small CSS refinements for central step readability.
- Did not change central map state names, layer bindings, scripts, data files, images or map assets.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B70 - Refine central story readability" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B70 central story readability pass complete.")
    print("Updated states:")
    for state in changed_states:
        print(f"  - {state}")
    print("Changed/created:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOCS / 'B70_refine_central_story_readability.md')}")
    print(f"  {rel(DONE)}")

if __name__ == "__main__":
    main()
