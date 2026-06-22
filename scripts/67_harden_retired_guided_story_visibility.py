#!/usr/bin/env python3
"""
B67 - Harden retired guidedStory visibility

Purpose:
- Public site can still show the retired guidedStory if cached CSS is used.
- B64 hid #guidedStory via class/CSS; B67 adds native HTML hiding as a cache-resistant safeguard.
- Does not delete any section, script, data file, image or map asset.

Changes:
- Ensure #guidedStory section has:
  - class contains "is-retired"
  - hidden
  - aria-hidden="true"
  - data-retired="B64"
  - inline style contains "display: none !important;"
- Create docs/B67_harden_retired_guided_story_visibility.md
- Update tasks/done.md
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

SECTION_OPEN_RE = re.compile(
    r'(<section\b(?=[^>]*\bid=["\']guidedStory["\'])(?P<attrs>[^>]*)>)',
    re.IGNORECASE | re.DOTALL,
)

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")

def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def upsert_attr(attrs: str, name: str, value: str | None = None) -> str:
    # Boolean attr
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

def ensure_style(attrs: str, rule: str) -> str:
    m = re.search(r'\bstyle\s*=\s*["\']([^"\']*)["\']', attrs, flags=re.IGNORECASE)
    if not m:
        return attrs.rstrip() + f' style="{rule}"'
    style = m.group(1).strip()
    if "display" not in style.lower():
        style = (style.rstrip(";") + "; " + rule).strip("; ")
    elif "none" not in style.lower():
        style = style.rstrip(";") + "; " + rule
    new = f'style="{style}"'
    return attrs[:m.start()] + new + attrs[m.end():]

def patch_opening_tag(html: str) -> tuple[str, str, str]:
    m = SECTION_OPEN_RE.search(html)
    if not m:
        raise RuntimeError('Could not find opening tag for section id="guidedStory".')

    old_tag = m.group(1)
    attrs = m.group("attrs")

    attrs = ensure_class(attrs, "is-retired")
    attrs = upsert_attr(attrs, "hidden", None)
    attrs = upsert_attr(attrs, "aria-hidden", "true")
    attrs = upsert_attr(attrs, "data-retired", "B64")
    attrs = ensure_style(attrs, "display: none !important;")

    # Keep the same leading "<section" and updated attributes.
    new_tag = "<section" + attrs + ">"
    new_html = html[:m.start(1)] + new_tag + html[m.end(1):]
    return new_html, old_tag, new_tag

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read(INDEX)
    new_html, old_tag, new_tag = patch_opening_tag(html)

    if new_html != html:
        write(INDEX, new_html)

    check = read(INDEX)
    m = SECTION_OPEN_RE.search(check)
    if not m:
        raise RuntimeError("guidedStory opening tag missing after patch.")
    tag = m.group(1)
    required = ["is-retired", "hidden", 'aria-hidden="true"', 'data-retired="B64"', "display: none"]
    missing = [x for x in required if x not in tag]
    if missing:
        raise RuntimeError(f"guidedStory hard-retire tag missing expected markers: {missing}\nTag: {tag}")

    doc = f"""# B67 - Harden Retired guidedStory Visibility

Date: {date.today().isoformat()}

## 1. Purpose

B67 makes the B64 retirement of `#guidedStory` robust against public-site stylesheet caching.

B64 intentionally kept the old guided story in the HTML and hid it by class/CSS. On GitHub Pages or in a browser cache, an outdated stylesheet can still make the retired section visible. B67 therefore adds native HTML-level hiding to the `#guidedStory` section.

## 2. Changed files

- `index.html`
- `docs/B67_harden_retired_guided_story_visibility.md`
- `tasks/done.md`

## 3. Opening tag before patch

```html
{old_tag}
```

## 4. Opening tag after patch

```html
{new_tag}
```

## 5. Not changed

B67 does not delete:

- the `guidedStory` section content,
- any JavaScript file,
- any public data file,
- any map/image asset.

## 6. Reasoning

This is a defensive patch. It makes the retired section hidden even if the browser or GitHub Pages serves an outdated stylesheet.

## 7. Required QA

After B67:

1. Run `python scripts\\58_visual_qa_and_commit_check.py`.
2. Open `http://localhost:8000/?v=b67`.
3. Open `https://chrisbran.github.io/peatland-transition-atlas/?v=b67` after push.
4. Confirm that `guidedStory` is not visible in either version.
5. Confirm that the central PNG story, hotspots, evidence map, pathways and fit sections still render.
"""

    write(DOCS / "B67_harden_retired_guided_story_visibility.md", doc)

    done_entry = f"""
## B67 - Harden retired guidedStory visibility ({date.today().isoformat()})

- Added native HTML-level hiding to `#guidedStory`.
- Kept the retired section content in `index.html` for reversibility.
- Did not delete scripts, data files, images or map assets.
- Purpose: make B64 retirement robust against public stylesheet caching.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B67 - Harden retired guidedStory visibility" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B67 hardened retired guidedStory visibility complete.")
    print("Changed/created:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(DOCS / 'B67_harden_retired_guided_story_visibility.md')}")
    print(f"  {rel(DONE)}")

if __name__ == "__main__":
    main()
