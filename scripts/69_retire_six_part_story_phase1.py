#!/usr/bin/env python3
"""
B69 - Retire six-part story phase 1

Purpose:
- Reduce the last major redundancy before the central atlas story.
- Retire the old #story / "Six-part story" section reversibly.
- Keep #transitionLogic and #mvpStoryline as the concise conceptual entry.
- Do not delete content, scripts, data, images, or map assets.

Changes:
- Add HTML-level retirement to #story:
  - class contains "is-retired"
  - hidden
  - aria-hidden="true"
  - data-retired="B69"
  - data-story-role="retired-intro-overview"
  - inline style contains "display: none !important;"
- Retarget nav links from #story to #transitionLogic if present.
- Create docs/B69_retire_six_part_story_phase1.md.
- Update tasks/done.md.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

SECTION_ID = "story"

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")

def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def find_section_open(html: str, section_id: str) -> re.Match[str] | None:
    return re.search(
        rf'<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])(?P<attrs>[^>]*)>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )

def upsert_attr(attrs: str, name: str, value: str | None = None) -> str:
    if value is None:
        if re.search(rf'\b{name}\b', attrs, flags=re.IGNORECASE):
            return attrs
        return attrs.rstrip() + f" {name}"

    pattern = re.compile(rf'\b{name}\s*=\s*["\'][^"\']*["\']', re.IGNORECASE)
    if pattern.search(attrs):
        return pattern.sub(f'{name}="{value}"', attrs)
    return attrs.rstrip() + f' {name}="{value}"'

def ensure_class(attrs: str, cls: str) -> str:
    m = re.search(r'\bclass\s*=\s*["\']([^"\']*)["\']', attrs, flags=re.IGNORECASE)
    if not m:
        return attrs.rstrip() + f' class="{cls}"'

    classes = m.group(1).split()
    if cls not in classes:
        classes.append(cls)

    new = f'class="{" ".join(classes)}"'
    return attrs[:m.start()] + new + attrs[m.end():]

def ensure_style_hidden(attrs: str) -> str:
    rule = "display: none !important;"
    m = re.search(r'\bstyle\s*=\s*["\']([^"\']*)["\']', attrs, flags=re.IGNORECASE)
    if not m:
        return attrs.rstrip() + f' style="{rule}"'

    style = m.group(1).strip()
    style_l = style.lower()
    if "display" not in style_l:
        style = style.rstrip(";") + "; " + rule
    elif "none" not in style_l:
        style = style.rstrip(";") + "; " + rule

    new = f'style="{style}"'
    return attrs[:m.start()] + new + attrs[m.end():]

def retire_section_opening_tag(html: str) -> tuple[str, str, str]:
    m = find_section_open(html, SECTION_ID)
    if not m:
        raise RuntimeError(f'Could not find opening tag for section id="{SECTION_ID}".')

    old_tag = m.group(0)
    attrs = m.group("attrs")

    attrs = ensure_class(attrs, "is-retired")
    attrs = upsert_attr(attrs, "hidden", None)
    attrs = upsert_attr(attrs, "aria-hidden", "true")
    attrs = upsert_attr(attrs, "data-retired", "B69")
    attrs = upsert_attr(attrs, "data-story-role", "retired-intro-overview")
    attrs = ensure_style_hidden(attrs)

    new_tag = "<section" + attrs + ">"
    new_html = html[:m.start()] + new_tag + html[m.end():]
    return new_html, old_tag, new_tag

def retarget_nav(html: str) -> tuple[str, int]:
    # Avoid a navigation link to a hidden section. Keep the label if unknown.
    # Common case: <a href="#story">Story</a>
    pattern = re.compile(r'(<a\b[^>]*\bhref=["\'])#story(["\'][^>]*>)', flags=re.IGNORECASE)
    html2, n = pattern.subn(r'\1#transitionLogic\2', html)
    return html2, n

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read(INDEX)

    if not find_section_open(html, "transitionLogic"):
        raise RuntimeError("Missing #transitionLogic. Refusing to retire #story because no replacement entry point was found.")
    if not find_section_open(html, "mvpStoryline"):
        raise RuntimeError("Missing #mvpStoryline. Run B68/B68b before B69.")

    html, old_tag, new_tag = retire_section_opening_tag(html)
    html, nav_links_changed = retarget_nav(html)

    write(INDEX, html)

    check = read(INDEX)
    m = find_section_open(check, SECTION_ID)
    if not m:
        raise RuntimeError("#story opening tag missing after patch.")
    tag = m.group(0)
    required = ["is-retired", "hidden", 'aria-hidden="true"', 'data-retired="B69"', 'data-story-role="retired-intro-overview"', "display: none"]
    missing = [x for x in required if x not in tag]
    if missing:
        raise RuntimeError(f"#story retirement tag missing expected markers: {missing}\nTag: {tag}")

    doc = f"""# B69 - Retire Six-Part Story Phase 1

Date: {date.today().isoformat()}

## 1. Purpose

B69 reduces the last major redundancy before the central atlas story.

After B68/B68b, the page already has:

- a conceptual frame: `#transitionLogic`,
- a compact main-atlas-story bridge: `#mvpStoryline`,
- the central PNG sticky map story: `#centralGlobalMapStory`.

The old `#story` / "Six-part story" section now duplicates that setup and delays the main atlas story.

## 2. Changed files

- `index.html`
- `docs/B69_retire_six_part_story_phase1.md`
- `tasks/done.md`

## 3. What changed

The opening tag of `#story` was changed from:

```html
{old_tag}
```

to:

```html
{new_tag}
```

Navigation links from `#story` to `#transitionLogic` changed:

```text
{nav_links_changed}
```

## 4. What B69 does not do

B69 does not:

- delete the `#story` section content,
- remove scripts,
- remove data files,
- remove map/image assets,
- alter the central map controller,
- alter BW/BK50 layer handling,
- alter lower evidence modules.

## 5. Rationale

The page should not become more complete at this stage. It should become more understandable.

The visible entry sequence after B69 should be:

1. Hero.
2. Transition logic.
3. Compact main atlas story bridge.
4. Central PNG sticky map story.
5. Supporting evidence / explorer modules.

## 6. Required QA

After B69:

1. Run `python scripts\\58_visual_qa_and_commit_check.py`.
2. Open `http://localhost:8000/?v=b69`.
3. Confirm that the old Six-part story is not visible.
4. Confirm that `#transitionLogic` remains visible.
5. Confirm that the central PNG sticky map story still works.
6. Confirm that lower evidence/pathway modules still render.
"""

    write(DOCS / "B69_retire_six_part_story_phase1.md", doc)

    done_entry = f"""
## B69 - Retire six-part story phase 1 ({date.today().isoformat()})

- Reversibly retired the old `#story` / Six-part story section.
- Retargeted navigation links from `#story` to `#transitionLogic` if present.
- Kept `#transitionLogic`, `#mvpStoryline` and `#centralGlobalMapStory` as the visible story entry.
- Did not delete sections, scripts, data files, images or map assets.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B69 - Retire six-part story phase 1" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B69 retired six-part story phase 1 complete.")
    print(f"Navigation links retargeted from #story to #transitionLogic: {nav_links_changed}")
    print("Changed/created:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(DOCS / 'B69_retire_six_part_story_phase1.md')}")
    print(f"  {rel(DONE)}")

if __name__ == "__main__":
    main()
