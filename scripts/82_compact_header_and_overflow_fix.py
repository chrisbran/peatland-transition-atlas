#!/usr/bin/env python3
"""
B82 - Compact header and presentation overflow fix

Purpose:
- Fix the remaining major presentation issue after B81:
  the old top masthead still carries the hero title/lead and duplicates the
  actual presentation hero.
- Replace the first production header with a compact German navigation bar.
- Add CSS safeguards so no header hero text reappears.
- Pull central map step panels safely inside the viewport and prevent text overflow.
- Do not alter map logic, map state names, data or assets.

Outputs:
- docs/B82_compact_header_and_overflow_fix.md
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
DOC = DOCS / "B82_compact_header_and_overflow_fix.md"


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


def replace_first_header(html: str) -> tuple[str, bool]:
    compact = """<header class="site-header b82-compact-header">
  <a class="brand" href="#problem" aria-label="Zum Anfang">Moorschutz</a>
  <nav aria-label="Seitennavigation">
    <a href="#problem">Problem</a>
    <a href="#centralGlobalMapStory">Kartenfolge</a>
    <a href="#b79RegionalImplementation">Umsetzung</a>
    <a href="#b79Pathways">Pfade</a>
    <a href="#b79MethodBoundary">Methode</a>
  </nav>
</header>"""

    # Prefer a header that contains the old duplicated masthead terms.
    header_pat = r"<header\b[^>]*>"
    for m in re.finditer(header_pat, html, flags=re.IGNORECASE | re.DOTALL):
        bounds = find_element_bounds(html[m.start():], "header", r"<header\b[^>]*>")
        if not bounds:
            continue
        s, oe, cs, ce = bounds
        s += m.start()
        oe += m.start()
        cs += m.start()
        ce += m.start()
        block = html[s:ce]
        if (
            "Moorschutz braucht räumliche Orientierung" in block
            or "Peatland Transition Atlas" in block
            or "Portfolio prototype" in block
            or "Literature-driven" in block
            or 'class="site-header' in block
            or "class='site-header" in block
        ):
            return html[:s] + compact + html[ce:], True

    # Fallback: replace first header only if it contains a nav.
    bounds = find_element_bounds(html, "header", r"<header\b[^>]*>")
    if bounds:
        s, oe, cs, ce = bounds
        block = html[s:ce]
        if "<nav" in block.lower():
            return html[:s] + compact + html[ce:], True

    return html, False


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    html = read(INDEX)
    css = read(CSS)

    html_before = html
    css_before = css

    html, header_replaced = replace_first_header(html)

    # Remaining robust cleanup in case old strings occur elsewhere visibly.
    replacements = {
        "PORTFOLIO PROTOTYPE · LITERATURE-DRIVEN MVP": "MOORE · KLIMASCHUTZ · REGIONALE UMSETZUNG",
        "Portfolio prototype · Literature-driven MVP": "Moore · Klimaschutz · regionale Umsetzung",
        "Peatland Transition Atlas": "Moorschutz braucht räumliche Orientierung",
        "Mapping the space between drainage-based agriculture and rewetting-compatible land use.": "Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung.",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    b82_css = r"""
/* B82 compact header and overflow fix */

/* The production header must be navigation only.
   It must not carry the hero title, lead, kicker or old portfolio text. */
header.site-header,
.b82-compact-header {
  position: sticky !important;
  top: 0 !important;
  bottom: auto !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 1200 !important;
  min-height: 54px !important;
  height: auto !important;
  padding: 14px clamp(22px, 4vw, 58px) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 22px !important;
  background: color-mix(in srgb, var(--b79-paper, #F5EFE6) 92%, white) !important;
  border-bottom: 1px solid var(--b79-line, #DED4C7) !important;
  box-shadow: none !important;
  overflow: visible !important;
}

header.site-header h1,
header.site-header .lead,
header.site-header .kicker,
header.site-header .eyebrow,
header.site-header > p,
.b82-compact-header h1,
.b82-compact-header .lead,
.b82-compact-header .kicker,
.b82-compact-header .eyebrow,
.b82-compact-header > p {
  display: none !important;
}

header.site-header .brand,
.b82-compact-header .brand {
  display: inline-flex !important;
  align-items: center !important;
  flex: 0 0 auto !important;
  color: var(--b79-ink, #221D18) !important;
  font-weight: 760 !important;
  letter-spacing: -0.02em !important;
  font-size: 0.95rem !important;
  line-height: 1 !important;
  white-space: nowrap !important;
}

header.site-header nav,
.b82-compact-header nav {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: clamp(12px, 2vw, 24px) !important;
  margin-left: auto !important;
  color: var(--b79-muted, #776A5D) !important;
  font-size: 0.92rem !important;
  line-height: 1 !important;
}

header.site-header nav a,
.b82-compact-header nav a {
  color: var(--b79-muted, #776A5D) !important;
  white-space: nowrap !important;
}

header.site-header nav a:hover,
.b82-compact-header nav a:hover {
  color: var(--b79-accent, #1F4E5F) !important;
}

/* The actual hero is the only place where the title/lead should appear. */
#problem {
  padding-top: clamp(78px, 9vw, 126px) !important;
}

/* Avoid giant empty lateral spacing and keep claim cards in readable boxes. */
#problem .b79-claim-grid {
  grid-template-columns: repeat(3, minmax(260px, 1fr)) !important;
  gap: 22px !important;
  max-width: 1040px !important;
}

#problem .b79-claim-grid article {
  width: auto !important;
  min-width: 0 !important;
  max-width: 100% !important;
  overflow: hidden !important;
  padding: 24px 22px !important;
}

#problem .b79-claim-grid article,
#problem .b79-claim-grid article * {
  word-break: normal !important;
  overflow-wrap: break-word !important;
  hyphens: auto !important;
}

/* Central map story: floating step panels must stay inside the viewport.
   This fixes the cropped/edge-hugging panels visible in scroll recordings. */
#centralGlobalMapStory .central-map-step,
#centralGlobalMapStory article[data-global-state] {
  box-sizing: border-box !important;
  max-width: min(380px, calc(100vw - 48px)) !important;
  min-width: 0 !important;
  overflow: hidden !important;
  padding: clamp(16px, 2.2vw, 24px) !important;
}

/* Only positioned panels receive explicit viewport-safe offsets. */
#centralGlobalMapStory .central-map-step[style],
#centralGlobalMapStory article[data-global-state][style] {
  left: clamp(18px, 4vw, 72px) !important;
  right: auto !important;
}

/* For absolute/fixed panels from the story script, keep them off the exact screen edge. */
#centralGlobalMapStory .central-map-step,
#centralGlobalMapStory article[data-global-state] {
  margin-left: max(0px, env(safe-area-inset-left)) !important;
}

/* Text inside step panels must never run beyond the card. */
#centralGlobalMapStory .central-map-step *,
#centralGlobalMapStory article[data-global-state] * {
  max-width: 100% !important;
  word-break: normal !important;
  overflow-wrap: break-word !important;
  hyphens: auto !important;
}

/* Slightly calmer map card shadow after B80. */
#centralGlobalMapStory .central-map-visual,
#centralGlobalMapStory .central-map-stage,
#centralGlobalMapStory .central-map-frame,
#centralGlobalMapStory .map-frame,
#centralGlobalMapStory figure {
  box-shadow: 0 18px 64px rgba(70, 50, 30, 0.12) !important;
}

@media (max-width: 980px) {
  header.site-header,
  .b82-compact-header {
    align-items: flex-start !important;
    flex-direction: column !important;
    gap: 10px !important;
  }

  header.site-header nav,
  .b82-compact-header nav {
    flex-wrap: wrap !important;
    justify-content: flex-start !important;
    margin-left: 0 !important;
  }

  #problem .b79-claim-grid {
    grid-template-columns: 1fr !important;
    max-width: 100% !important;
  }

  #centralGlobalMapStory .central-map-step,
  #centralGlobalMapStory article[data-global-state] {
    max-width: calc(100vw - 32px) !important;
  }
}
/* End B82 compact header and overflow fix */
"""
    if "/* B82 compact header and overflow fix */" not in css:
        css = css.rstrip() + "\n\n" + b82_css.strip() + "\n"

    if html != html_before:
        write(INDEX, html)
    if css != css_before:
        write(CSS, css)

    doc = f"""# B82 - Compact Header and Overflow Fix

Date: {today}

## 1. Purpose

B82 fixes the issues visible after B81:

- the old top masthead still duplicated the actual hero,
- the top area still showed the substantive title and lead inside the navigation/header area,
- some cards and floating step panels could become too narrow,
- some map-step panels were too close to the viewport edge.

## 2. Main change

The first production header was replaced with a compact German navigation bar:

- `Moorschutz`
- `Problem`
- `Kartenfolge`
- `Umsetzung`
- `Pfade`
- `Methode`

The substantive title remains only in the actual hero section.

## 3. CSS safeguards

B82 appends CSS that:

- hides any `h1`, lead, kicker or old paragraph inside `header.site-header`,
- keeps the header compact and sticky at the top,
- stabilizes hero claim-card widths,
- prevents text overflow in cards and central map steps,
- keeps floating map step panels inside the viewport.

## 4. Files changed

- `index.html`
- `src/styles.css`
- `docs/B82_compact_header_and_overflow_fix.md`
- `tasks/done.md`

## 5. Header replaced

`{header_replaced}`

## 6. Manual QA

Check:

1. No duplicated hero title in the top navigation/header.
2. Header is compact.
3. Hero title appears once.
4. Hero claim cards are readable.
5. Central map step cards are not cropped at the viewport edge.
6. Map sequence still works.
"""
    write(DOC, doc)

    done_entry = f"""
## B82 - Compact header and overflow fix ({today})

- Replaced the old duplicated masthead with a compact German navigation header.
- Added CSS safeguards to hide header hero/meta text.
- Stabilized hero claim-card width and card text wrapping.
- Improved central map step overflow and viewport-edge behaviour.
- Created `docs/B82_compact_header_and_overflow_fix.md`.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B82 - Compact header and overflow fix" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B82 compact header and overflow fix complete.")
    print("Changed:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOC)}")
    print(f"  {rel(DONE)}")
    print(f"Header replaced: {header_replaced}")


if __name__ == "__main__":
    main()
