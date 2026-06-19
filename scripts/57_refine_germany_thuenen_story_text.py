#!/usr/bin/env python3
r"""
57 - Refine Germany / Thuenen story text.

Run from repository root:
  python scripts\57_refine_germany_thuenen_story_text.py

Purpose:
- Sharpen the text for the Germany / Thuenen scrolly steps.
- Keep the current map/layer logic untouched.
- Update central metadata text where applicable.
"""

from pathlib import Path
import datetime
import re

TODAY = datetime.date.today().isoformat()

ARTICLES = {
    "germany-context": """    <article class="central-map-step" data-global-state="germany-context">
      <span>07 · Germany frame</span>
      <h3>Germany is where peatland transition becomes an implementation problem.</h3>
      <p>
        The story now shifts from continental patterns to national planning geography. In Germany,
        federal structures, land use, drainage history, and soil classification determine where transition
        is technically and politically feasible.
      </p>
    </article>""",
    "germany-thuenen-extent": """    <article class="central-map-step" data-global-state="germany-thuenen-extent">
      <span>08 · Thuenen Kulisse</span>
      <h3>The Thuenen Kulisse identifies the national peat and organic-soils target area.</h3>
      <p>
        The one-colour layer first establishes the spatial footprint: where peat and organic soils are
        relevant for mitigation, rewetting, agricultural adaptation, and land-use planning.
      </p>
    </article>""",
    "germany-thuenen-types": """    <article class="central-map-step" data-global-state="germany-thuenen-types">
      <span>09 · Moor and soil types</span>
      <h3>The type distinction is not cosmetic — it changes the transition logic.</h3>
      <p>
        Fen, raised bog, transformed peat soils, deeply ploughed classes, and covered organic soils imply
        different hydrological constraints, restoration potential, agricultural trade-offs, and evidence needs.
      </p>
    </article>"""
}

META_REPLACEMENTS = {
    "Germany is the national implementation frame.": "Germany is where peatland transition becomes an implementation problem.",
    "The national peat and organic-soils Kulisse is spatially concentrated.": "The Thuenen Kulisse identifies the national peat and organic-soils target area.",
    "Type differentiation matters for transition pathways.": "The type distinction is not cosmetic — it changes the transition logic.",
    "Germany frame: NUTS 1 / federal-state context exported from GERMANY_FRAME_V1.": "Germany frame: national implementation scale with NUTS 1 / federal-state context.",
    "Thuenen Kulisse rendered as national extent layer · Germany frame.": "Thuenen Kulisse: national peat and organic-soils target area rendered as a one-colour extent layer.",
    "Thuenen Kulisse symbolized by KAT_LANG / moor and soil type.": "Thuenen Kulisse symbolized by KAT_LANG to distinguish moor and soil types relevant for transition pathways."
}

DOC = """# B57 - Refine Germany / Thuenen Story Text

Date: {date}

## Purpose

Sharpen the Germany / Thuenen section so it reads less like a generic map caption and more like a clear argument.

## Revised logic

1. Germany is the implementation scale.
2. The Thuenen Kulisse first establishes the spatial footprint.
3. The soil-type distinction changes the transition logic.

## Files patched

- `index.html`
- `src/central_step_state_bridge.js` if matching metadata text exists
- `src/central_global_map_story.js` if matching metadata text exists

## Acceptance check

The Germany sequence should now read as a short argument:

- Germany: implementation problem
- Thuenen extent: national target area
- Thuenen types: hydrological and land-use relevance
""".format(date=TODAY)

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def replace_article(html: str, state: str, replacement: str) -> str:
    pattern = re.compile(
        r'    <article class="central-map-step" data-global-state="' + re.escape(state) + r'">.*?</article>',
        re.DOTALL
    )
    if not pattern.search(html):
        raise SystemExit(f"Could not find article for state {state} in index.html.")
    return pattern.sub(replacement, html, count=1)

def patch_index(path: Path) -> bool:
    text = read(path)
    patched = text
    for state, article in ARTICLES.items():
        patched = replace_article(patched, state, article)
    if patched != text:
        write(path, patched)
        return True
    return False

def patch_metadata_file(path: Path) -> bool:
    if not path.exists():
        return False
    text = read(path)
    patched = text
    for old, new in META_REPLACEMENTS.items():
        patched = patched.replace(old, new)
    if patched != text:
        write(path, patched)
        return True
    return False

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    changed = []

    if patch_index(root / "index.html"):
        changed.append("index.html")

    for rel in [
        "src/central_step_state_bridge.js",
        "src/central_global_map_story.js",
    ]:
        if patch_metadata_file(root / rel):
            changed.append(rel)

    write(root / "docs" / "B57_refine_germany_thuenen_story_text.md", DOC)
    changed.append("docs/B57_refine_germany_thuenen_story_text.md")

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B57 completed" not in done_text:
        done_text += f"- {TODAY}: Task B57 completed - refined Germany / Thuenen story text.\n"
        write(done, done_text)
        changed.append("tasks/done.md")

    print("B57 Germany / Thuenen story text refined.")
    print("Changed/created:")
    for rel in changed:
        print(" ", rel)
    print()
    print("Checks:")
    print('  Select-String -Path index.html -Pattern "implementation problem|national peat and organic-soils target area|not cosmetic"')
    print('  Select-String -Path src\\central_step_state_bridge.js -Pattern "implementation problem|not cosmetic"')
    print()
    print("Then hard reload browser with Ctrl+F5.")

if __name__ == "__main__":
    main()
