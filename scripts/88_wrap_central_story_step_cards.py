#!/usr/bin/env python3
"""
B88 - Wrap central story step cards

Purpose:
- B87 restored selector targeting and the map stage now responds.
- Remaining visual issue: B84/B87 broad CSS styled the whole scrollytelling
  trigger article as a dark panel, creating giant dark blocks/columns.
- Fix by separating trigger geometry from visible text card:
  - wrap the contents of each data-global-state article in .b88-step-card,
  - reset the article/trigger itself to transparent,
  - style only the .b88-step-card as the dark readable panel.
- Keep central map logic, map state names, assets and data unchanged.

Outputs:
- docs/B88_wrap_central_story_step_cards.md
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
DOC = DOCS / "B88_wrap_central_story_step_cards.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def find_element_bounds(text: str, tag: str, start_pos: int):
    open_match = re.match(rf"<{tag}\b[^>]*>", text[start_pos:], flags=re.IGNORECASE | re.DOTALL)
    if not open_match:
        return None
    start = start_pos
    open_end = start_pos + open_match.end()
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


def wrap_state_articles(html: str) -> tuple[str, int]:
    # Find article openings with data-global-state.
    openings = list(re.finditer(r"<article\b(?=[^>]*\bdata-global-state=)[^>]*>", html, flags=re.IGNORECASE | re.DOTALL))
    if not openings:
        return html, 0

    # Process from the end to keep indices valid.
    count = 0
    for m in reversed(openings):
        bounds = find_element_bounds(html, "article", m.start())
        if not bounds:
            continue
        start, open_end, close_start, close_end = bounds
        inner = html[open_end:close_start]
        if "b88-step-card" in inner:
            continue

        # Preserve whitespace but wrap visible card content.
        stripped = inner.strip()
        if not stripped:
            continue

        wrapped = "\n      <div class=\"b88-step-card\">\n" + stripped + "\n      </div>\n    "
        html = html[:open_end] + wrapped + html[close_start:]
        count += 1
    return html, count


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    html = read(INDEX)
    css = read(CSS)

    html, wrapped_count = wrap_state_articles(html)
    if wrapped_count:
        write(INDEX, html)

    b88_css = r"""
/* B88 wrap central story step cards */

/*
  Do not style the whole scrollytelling trigger article as a card.
  The article controls scroll geometry; only .b88-step-card is the visible panel.
*/
#centralGlobalMapStory article[data-global-state],
.central-map-story article[data-global-state],
[data-b87-central-story="true"] article[data-global-state],
#centralGlobalMapStory .central-map-step[data-global-state],
.central-map-story .central-map-step[data-global-state],
[data-b87-central-story="true"] .central-map-step[data-global-state] {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  overflow: visible !important;
  color: inherit !important;
}

/* Suppress older pseudo-panel styling on the trigger itself. */
#centralGlobalMapStory article[data-global-state]::before,
#centralGlobalMapStory article[data-global-state]::after,
.central-map-story article[data-global-state]::before,
.central-map-story article[data-global-state]::after,
[data-b87-central-story="true"] article[data-global-state]::before,
[data-b87-central-story="true"] article[data-global-state]::after {
  content: none !important;
  display: none !important;
}

/* The actual visible card. */
#centralGlobalMapStory .b88-step-card,
.central-map-story .b88-step-card,
[data-b87-central-story="true"] .b88-step-card {
  width: min(380px, calc(100vw - 56px)) !important;
  max-width: min(380px, calc(100vw - 56px)) !important;
  min-width: 0 !important;
  padding: clamp(18px, 2.2vw, 26px) !important;
  background: rgba(9, 18, 15, 0.88) !important;
  color: #F5F0E7 !important;
  border: 1px solid rgba(245, 240, 231, 0.16) !important;
  border-radius: 16px !important;
  box-shadow: 0 18px 54px rgba(0, 0, 0, 0.28) !important;
  backdrop-filter: blur(9px) saturate(0.92) !important;
  -webkit-backdrop-filter: blur(9px) saturate(0.92) !important;
  overflow: hidden !important;
}

/* Text inside actual visible card. */
#centralGlobalMapStory .b88-step-card span,
.central-map-story .b88-step-card span,
[data-b87-central-story="true"] .b88-step-card span {
  display: inline-block !important;
  color: #55A3B5 !important;
  font-weight: 800 !important;
  letter-spacing: 0.08em !important;
  margin-bottom: 0.75rem !important;
}

#centralGlobalMapStory .b88-step-card h3,
.central-map-story .b88-step-card h3,
[data-b87-central-story="true"] .b88-step-card h3 {
  color: #F5F0E7 !important;
  margin: 0 0 0.65rem !important;
  line-height: 1.1 !important;
}

#centralGlobalMapStory .b88-step-card p,
.central-map-story .b88-step-card p,
[data-b87-central-story="true"] .b88-step-card p {
  color: rgba(245, 240, 231, 0.78) !important;
  margin: 0 !important;
  line-height: 1.42 !important;
}

#centralGlobalMapStory .b88-step-card *,
.central-map-story .b88-step-card *,
[data-b87-central-story="true"] .b88-step-card * {
  max-width: 100% !important;
  overflow-wrap: break-word !important;
  word-break: normal !important;
  hyphens: auto !important;
}

/* Keep map stage above the grey field and behind the cards. */
#centralGlobalMapStory .central-map-sticky,
.central-map-story .central-map-sticky,
[data-b87-central-story="true"] .central-map-sticky {
  z-index: 2 !important;
}

#centralGlobalMapStory article[data-global-state],
.central-map-story article[data-global-state],
[data-b87-central-story="true"] article[data-global-state] {
  z-index: 5 !important;
}

/* Mobile fallback. */
@media (max-width: 900px) {
  #centralGlobalMapStory .b88-step-card,
  .central-map-story .b88-step-card,
  [data-b87-central-story="true"] .b88-step-card {
    width: calc(100vw - 32px) !important;
    max-width: calc(100vw - 32px) !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
  }
}
/* End B88 wrap central story step cards */
"""

    if "/* B88 wrap central story step cards */" not in css:
        css = css.rstrip() + "\n\n" + b88_css.strip() + "\n"
        write(CSS, css)

    doc = f"""# B88 - Wrap Central Story Step Cards

Date: {today}

## 1. Why B88 was needed

After B87, the selector targeting finally reached the central story, but the visible result showed a new problem:

- the map stage responded,
- but whole scrollytelling trigger articles were styled as dark cards,
- this created large dark columns/blocks on the left,
- the actual text cards were not visually separated from the scroll geometry.

## 2. Fix

B88 separates two things:

1. **Trigger geometry**  
   The `article[data-global-state]` element remains available for scroll/state logic but becomes visually transparent.

2. **Visible text card**  
   The contents of each state article are wrapped in:

```html
<div class="b88-step-card">...</div>
```

Only `.b88-step-card` receives the dark card styling.

## 3. Files changed

- `index.html`
- `src/styles.css`
- `docs/B88_wrap_central_story_step_cards.md`
- `tasks/done.md`

## 4. Wrapped state articles

`{wrapped_count}`

## 5. Manual QA

Check:

1. Large dark columns/blocks on the left are gone.
2. Steps 01-11 show compact dark cards.
3. Cards remain readable.
4. The map remains visible as the central visual anchor.
5. Scroll/state switching still works.
6. Hero, header and lower German sections remain stable.
"""
    write(DOC, doc)

    done_entry = f"""
## B88 - Wrap central story step cards ({today})

- Wrapped central `article[data-global-state]` contents in `.b88-step-card`.
- Reset scroll-trigger articles to transparent so they no longer render as giant dark blocks.
- Styled only `.b88-step-card` as the visible dark step panel.
- Created `docs/B88_wrap_central_story_step_cards.md`.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B88 - Wrap central story step cards" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B88 wrap central story step cards complete.")
    print("Changed:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOC)}")
    print(f"  {rel(DONE)}")
    print(f"Wrapped state articles: {wrapped_count}")


if __name__ == "__main__":
    main()
