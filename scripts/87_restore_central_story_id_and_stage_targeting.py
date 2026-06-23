#!/usr/bin/env python3
"""
B87 - Restore central map story id and class-targeted styling

Purpose:
- B86 showed that #centralGlobalMapStory was missing from index.html.
- This explains why B83-B85 CSS selectors targeting #centralGlobalMapStory did not affect
  the visible central story.
- Restore the canonical id on the actual central map story section if missing.
- Add a stable data attribute for future targeting.
- Add class-based CSS selectors so styling works even if the id is lost again.
- Keep central map logic, state names, maps and data unchanged.

Outputs:
- docs/B87_restore_central_story_id_and_stage_targeting.md
- modifies index.html
- modifies src/styles.css
- updates tasks/done.md
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
DOC = DOCS / "B87_restore_central_story_id_and_stage_targeting.md"


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


def add_or_replace_attr(opening: str, name: str, value: str) -> str:
    if re.search(rf"\b{name}\s*=", opening, flags=re.IGNORECASE):
        return re.sub(
            rf'\b{name}\s*=\s*(["\'])(.*?)\1',
            f'{name}="{value}"',
            opening,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )
    return opening[:-1] + f' {name}="{value}">'


def ensure_class(opening: str, class_name: str) -> str:
    m = re.search(r'\bclass\s*=\s*(["\'])(.*?)\1', opening, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return opening[:-1] + f' class="{class_name}">'
    classes = m.group(2).split()
    if class_name in classes:
        return opening
    classes.append(class_name)
    new = f'class="{ " ".join(classes) }"'
    return opening[:m.start()] + new + opening[m.end():]


def find_actual_central_section(html: str):
    """
    Prefer:
    1. existing #centralGlobalMapStory,
    2. section.central-map-story,
    3. nearest section containing central-map-sticky and central-map-step,
    4. nearest section containing data-global-state steps and central-map-layer images.
    """
    patterns = [
        r"<section\b(?=[^>]*\bid=[\"']centralGlobalMapStory[\"'])[^>]*>",
        r"<section\b(?=[^>]*\bclass=[\"'][^\"']*\bcentral-map-story\b[^\"']*[\"'])[^>]*>",
    ]
    for pat in patterns:
        bounds = find_element_bounds(html, "section", pat)
        if bounds:
            return bounds, "direct section selector"

    # Fallback: inspect all sections.
    section_pat = re.compile(r"<section\b[^>]*>", flags=re.IGNORECASE | re.DOTALL)
    candidates = []
    for m in section_pat.finditer(html):
        bounds = find_element_bounds(html[m.start():], "section", r"<section\b[^>]*>")
        if not bounds:
            continue
        s, oe, cs, ce = bounds
        s += m.start()
        oe += m.start()
        cs += m.start()
        ce += m.start()
        block = html[s:ce]
        score = 0
        reasons = []
        for token, weight in [
            ("central-map-sticky", 5),
            ("central-map-shell", 5),
            ("central-map-layer-stack", 5),
            ("central-map-layer", 4),
            ("central-map-step", 4),
            ("data-global-state", 4),
            ("layer-bw-bk50-extent", 3),
            ("global_gpm2_peat_extent.png", 3),
            ("bw_bk50_moor_extent.png", 3),
        ]:
            if token in block:
                score += weight
                reasons.append(token)
        if score:
            candidates.append((score, reasons, (s, oe, cs, ce)))
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        score, reasons, bounds = candidates[0]
        return bounds, "scored section: " + ", ".join(reasons)

    return None, "not found"


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    html = read(INDEX)
    css = read(CSS)

    original_has_id = 'id="centralGlobalMapStory"' in html or "id='centralGlobalMapStory'" in html

    found, reason = find_actual_central_section(html)
    if not found:
        doc = f"""# B87 - Restore Central Story ID and Stage Targeting

Date: {today}

## Result

FAIL: Could not find the actual central story section.

Reason attempted:

`{reason}`

No files were changed.
"""
        write(DOC, doc)
        print("B87 failed: central story section not found.")
        print(f"Changed/created: {rel(DOC)}")
        return

    start, open_end, close_start, close_end = found
    opening = html[start:open_end]
    before_opening = opening

    opening = add_or_replace_attr(opening, "id", "centralGlobalMapStory")
    opening = add_or_replace_attr(opening, "data-b87-central-story", "true")
    opening = ensure_class(opening, "central-map-story")

    html = html[:start] + opening + html[open_end:]

    # Ensure nav target remains valid.
    html = html.replace('href="#kartenfolge"', 'href="#centralGlobalMapStory"')

    write(INDEX, html)

    b87_css = r"""
/* B87 central story id restore and class-targeted stage styling */

/*
  Target both the canonical id and the stable class/data attribute.
  B86 showed that id-based targeting can silently fail if the id is lost.
*/
#centralGlobalMapStory,
.central-map-story,
[data-b87-central-story="true"] {
  position: relative !important;
  background:
    linear-gradient(
      180deg,
      rgba(245, 239, 230, 0.0) 0%,
      rgba(9, 18, 15, 0.40) 9%,
      rgba(9, 18, 15, 0.48) 50%,
      rgba(9, 18, 15, 0.38) 91%,
      rgba(245, 239, 230, 0.0) 100%
    ) !important;
}

/* Sticky visual stage: target actual historic classes from the central PNG story. */
#centralGlobalMapStory .central-map-sticky,
.central-map-story .central-map-sticky,
[data-b87-central-story="true"] .central-map-sticky {
  position: sticky !important;
  top: clamp(68px, 8vh, 106px) !important;
  z-index: 2 !important;
}

#centralGlobalMapStory .central-map-shell,
.central-map-story .central-map-shell,
[data-b87-central-story="true"] .central-map-shell {
  background: #07120F !important;
  border: 1px solid rgba(245, 240, 231, 0.16) !important;
  border-radius: clamp(16px, 2vw, 28px) !important;
  box-shadow: 0 26px 90px rgba(0, 0, 0, 0.32) !important;
  overflow: hidden !important;
}

/* Preserve stacked PNG layer behaviour. */
#centralGlobalMapStory .central-map-layer-stack,
.central-map-story .central-map-layer-stack,
[data-b87-central-story="true"] .central-map-layer-stack {
  background: #07120F !important;
}

#centralGlobalMapStory .central-map-layer,
.central-map-story .central-map-layer,
[data-b87-central-story="true"] .central-map-layer {
  background: transparent !important;
}

/* Step cards: target id, class and stable data attribute. */
#centralGlobalMapStory .central-map-step,
.central-map-story .central-map-step,
[data-b87-central-story="true"] .central-map-step,
#centralGlobalMapStory [data-global-state],
.central-map-story [data-global-state],
[data-b87-central-story="true"] [data-global-state] {
  background: rgba(9, 18, 15, 0.88) !important;
  color: #F5F0E7 !important;
  border: 1px solid rgba(245, 240, 231, 0.16) !important;
  box-shadow: 0 18px 54px rgba(0, 0, 0, 0.28) !important;
  z-index: 6 !important;
  overflow: hidden !important;
}

#centralGlobalMapStory .central-map-step h3,
.central-map-story .central-map-step h3,
[data-b87-central-story="true"] .central-map-step h3,
#centralGlobalMapStory [data-global-state] h3,
.central-map-story [data-global-state] h3,
[data-b87-central-story="true"] [data-global-state] h3 {
  color: #F5F0E7 !important;
}

#centralGlobalMapStory .central-map-step p,
.central-map-story .central-map-step p,
[data-b87-central-story="true"] .central-map-step p,
#centralGlobalMapStory [data-global-state] p,
.central-map-story [data-global-state] p,
[data-b87-central-story="true"] [data-global-state] p {
  color: rgba(245, 240, 231, 0.78) !important;
}

#centralGlobalMapStory .central-map-step span,
.central-map-story .central-map-step span,
[data-b87-central-story="true"] .central-map-step span,
#centralGlobalMapStory [data-global-state] span,
.central-map-story [data-global-state] span,
[data-b87-central-story="true"] [data-global-state] span {
  color: #55A3B5 !important;
}

/* Undo pale pseudo panels. */
#centralGlobalMapStory .central-map-step::before,
#centralGlobalMapStory .central-map-step::after,
.central-map-story .central-map-step::before,
.central-map-story .central-map-step::after,
[data-b87-central-story="true"] .central-map-step::before,
[data-b87-central-story="true"] .central-map-step::after {
  content: none !important;
  display: none !important;
}

/* Keep the central titlebar/legend/source readable on dark map shell. */
#centralGlobalMapStory .central-map-titlebar,
.central-map-story .central-map-titlebar,
[data-b87-central-story="true"] .central-map-titlebar,
#centralGlobalMapStory .central-map-legend,
.central-map-story .central-map-legend,
[data-b87-central-story="true"] .central-map-legend,
#centralGlobalMapStory .central-map-source,
.central-map-story .central-map-source,
[data-b87-central-story="true"] .central-map-source {
  color: rgba(245, 240, 231, 0.78) !important;
}

/* Intro text should remain warm-paper dark, not dark card. */
#centralGlobalMapStory > .section-heading,
.central-map-story > .section-heading,
[data-b87-central-story="true"] > .section-heading {
  background: transparent !important;
  color: var(--b79-ink, #221D18) !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* Mobile fallback. */
@media (max-width: 900px) {
  #centralGlobalMapStory .central-map-sticky,
  .central-map-story .central-map-sticky,
  [data-b87-central-story="true"] .central-map-sticky {
    position: relative !important;
    top: auto !important;
  }
}
/* End B87 central story id restore and class-targeted stage styling */
"""

    if "/* B87 central story id restore and class-targeted stage styling */" not in css:
        css = css.rstrip() + "\n\n" + b87_css.strip() + "\n"
        write(CSS, css)

    doc = f"""# B87 - Restore Central Story ID and Stage Targeting

Date: {today}

## 1. Why B87 was needed

B86 reported that `#centralGlobalMapStory` was not found in `index.html`. That explains why B83-B85 selectors targeting `#centralGlobalMapStory` did not visibly affect the central story.

## 2. What B87 did

B87 located the actual central story section using fallback signals:

- `central-map-sticky`
- `central-map-shell`
- `central-map-layer-stack`
- `central-map-layer`
- `central-map-step`
- `data-global-state`
- BW map-layer references

Then it restored:

- `id="centralGlobalMapStory"`
- `class="central-map-story"` if missing
- `data-b87-central-story="true"`

It also appended CSS that targets all three:

- `#centralGlobalMapStory`
- `.central-map-story`
- `[data-b87-central-story="true"]`

## 3. Detection

Original had canonical id:

`{original_has_id}`

Detection reason:

`{reason}`

Opening tag before:

```html
{before_opening}
```

Opening tag after:

```html
{opening}
```

## 4. Files changed

- `index.html`
- `src/styles.css`
- `docs/B87_restore_central_story_id_and_stage_targeting.md`
- `tasks/done.md`

## 5. Manual QA

Check:

1. The central story is still visible.
2. Steps 01-11 use dark panels.
3. The map stage remains visually present through the central scroll sequence.
4. Global, Europe, Germany and BW/BK50 states still switch.
5. Header and hero remain stable.
"""
    write(DOC, doc)

    done_entry = f"""
## B87 - Restore central story id and stage targeting ({today})

- Restored canonical `id="centralGlobalMapStory"` on the actual central story section.
- Added `data-b87-central-story="true"` for stable future targeting.
- Added class/id/data-attribute CSS targeting for the central map stage and cards.
- Created `docs/B87_restore_central_story_id_and_stage_targeting.md`.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B87 - Restore central story id and stage targeting" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B87 restore central story id and stage targeting complete.")
    print("Changed:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOC)}")
    print(f"  {rel(DONE)}")
    print(f"Original had id centralGlobalMapStory: {original_has_id}")
    print(f"Detection reason: {reason}")


if __name__ == "__main__":
    main()
