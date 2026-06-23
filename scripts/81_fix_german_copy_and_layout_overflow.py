#!/usr/bin/env python3
"""
B81 - Fix German presentation hero copy and overflow issues

Purpose:
- Complete the visible German translation in the presentation hero.
- Remove leftover English/meta tool language from the visible top section.
- Fix layout overflow in the hero cards and prevent text from running outside frames.
- Reduce overlay artefacts without touching map logic.

Outputs:
- docs/B81_fix_german_copy_and_layout_overflow.md
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
DOC = DOCS / "B81_fix_german_copy_and_layout_overflow.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def replace_literal(text: str, old: str, new: str) -> str:
    return text.replace(old, new)


def replace_first_visible_tag_text(text: str, tag: str, old_text: str, new_text: str) -> str:
    pattern = re.compile(
        rf"(<{tag}\b[^>]*>)\s*{re.escape(old_text)}\s*(</{tag}>)",
        flags=re.IGNORECASE | re.DOTALL,
    )
    return pattern.sub(rf"\1{new_text}\2", text, count=1)


def replace_title(text: str, new_title: str) -> str:
    if re.search(r"<title>.*?</title>", text, flags=re.IGNORECASE | re.DOTALL):
        return re.sub(
            r"<title>.*?</title>",
            f"<title>{new_title}</title>",
            text,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )
    return text


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read(INDEX)
    css = read(CSS)
    today = date.today().isoformat()

    before_html = html
    before_css = css

    # --- Robust visible string replacements in the hero / top area ---
    replacements = {
        "PORTFOLIO PROTOTYPE · LITERATURE-DRIVEN MVP": "MOORE · KLIMASCHUTZ · REGIONALE UMSETZUNG",
        "Portfolio prototype · Literature-driven MVP": "Moore · Klimaschutz · regionale Umsetzung",
        "Peatland Transition Atlas": "Moorschutz braucht räumliche Orientierung",
        "Mapping the space between drainage-based agriculture and rewetting-compatible land use.": "Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung.",
        "Atlas framing": "Kernargument",
        "Story": "Problem",
        "Method": "Methode",
    }
    for old, new in replacements.items():
        html = replace_literal(html, old, new)

    html = replace_title(html, "Moorschutz braucht räumliche Orientierung")

    # Fallback tag-level replacements if exact literals survived in slightly altered markup.
    html = replace_first_visible_tag_text(html, "h1", "Peatland Transition Atlas", "Moorschutz braucht räumliche Orientierung")
    html = replace_first_visible_tag_text(
        html,
        "p",
        "Mapping the space between drainage-based agriculture and rewetting-compatible land use.",
        "Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung.",
    )

    # --- CSS: harden the German hero layout and fix overflows ---
    b81_css = r"""
/* B81 fix German copy and layout overflow */

/* Hard reset for the visible top presentation section.
   Prevent legacy grid/flex rules from forcing narrow columns or mixed alignments. */
#problem,
#problem.hero,
section#problem,
section#problem.hero,
.hero#problem {
  display: block !important;
  position: relative !important;
  max-width: 1240px !important;
  margin: 0 auto !important;
  padding: clamp(88px, 10vw, 136px) clamp(24px, 6vw, 72px) clamp(56px, 8vw, 84px) !important;
  min-height: 0 !important;
}

#problem > *,
#problem.hero > *,
section#problem > * {
  max-width: none !important;
  float: none !important;
  clear: both !important;
}

/* Stronger, deterministic hero typography */
#problem .kicker,
#problem .eyebrow,
#problem p.kicker,
#problem p.eyebrow {
  display: block !important;
  margin: 0 0 18px 0 !important;
  color: #9BAE56 !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  font-weight: 760 !important;
  font-size: 0.80rem !important;
}

#problem h1 {
  display: block !important;
  max-width: 900px !important;
  margin: 0 0 22px 0 !important;
  color: #221D18 !important;
  font-size: clamp(3rem, 6.4vw, 5.4rem) !important;
  line-height: 0.96 !important;
  letter-spacing: -0.06em !important;
}

#problem .lead,
#problem p.lead,
#problem > p:not(.kicker):not(.eyebrow):not(.section-kicker) {
  display: block !important;
  max-width: 780px !important;
  margin: 0 0 34px 0 !important;
  color: #3B3129 !important;
  font-size: clamp(1.18rem, 1.8vw, 1.55rem) !important;
  line-height: 1.38 !important;
}

/* Hero claim cards: remove narrow forced widths and text spillover */
#problem .b79-claim-grid {
  display: grid !important;
  grid-template-columns: repeat(3, minmax(240px, 1fr)) !important;
  gap: 22px !important;
  width: min(100%, 980px) !important;
  max-width: 980px !important;
  margin: 28px 0 0 0 !important;
  align-items: stretch !important;
  justify-content: start !important;
}

#problem .b79-claim-grid article {
  display: block !important;
  min-width: 0 !important;
  min-height: 0 !important;
  width: auto !important;
  height: auto !important;
  padding: 24px 22px !important;
  overflow: hidden !important;
  background: rgba(255, 252, 247, 0.86) !important;
  border: 1px solid rgba(222, 212, 199, 0.96) !important;
  box-shadow: none !important;
}

#problem .b79-claim-grid article * {
  max-width: 100% !important;
  overflow-wrap: anywhere !important;
  word-break: normal !important;
  hyphens: auto !important;
}

#problem .b79-claim-grid .b79-num {
  display: inline-block !important;
  margin-bottom: 10px !important;
}

#problem .b79-claim-grid h3 {
  margin: 0 0 10px 0 !important;
  font-size: 0.98rem !important;
  line-height: 1.15 !important;
  color: #221D18 !important;
}

#problem .b79-claim-grid p {
  margin: 0 !important;
  font-size: 0.96rem !important;
  line-height: 1.36 !important;
  color: #5F554B !important;
}

/* Central map steps and other cards: no overflow outside their frames */
#centralGlobalMapStory .central-map-step,
#centralGlobalMapStory article[data-global-state],
.b79-card-grid article,
.b79-section article {
  overflow: hidden !important;
}

#centralGlobalMapStory .central-map-step *,
#centralGlobalMapStory article[data-global-state] *,
.b79-card-grid article *,
.b79-section article * {
  max-width: 100% !important;
  overflow-wrap: anywhere !important;
  word-break: normal !important;
  hyphens: auto !important;
}

/* Remove residual grey overlays from earlier styles */
#centralGlobalMapStory .central-map-step::before,
#centralGlobalMapStory .central-map-step::after,
#centralGlobalMapStory article[data-global-state]::before,
#centralGlobalMapStory article[data-global-state]::after,
#problem .b79-claim-grid article::before,
#problem .b79-claim-grid article::after {
  content: none !important;
  display: none !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* Mobile fallback */
@media (max-width: 980px) {
  #problem .b79-claim-grid {
    grid-template-columns: 1fr !important;
    width: 100% !important;
    max-width: 100% !important;
  }

  #problem h1 {
    max-width: 100% !important;
  }

  #problem .lead,
  #problem p.lead,
  #problem > p:not(.kicker):not(.eyebrow):not(.section-kicker) {
    max-width: 100% !important;
  }
}
/* End B81 fix German copy and layout overflow */
"""
    if "/* B81 fix German copy and layout overflow */" not in css:
        css = css.rstrip() + "\n\n" + b81_css.strip() + "\n"

    if html != before_html:
        write(INDEX, html)
    if css != before_css:
        write(CSS, css)

    doc = f"""# B81 - Fix German copy and layout overflow

Date: {today}

## Ziel

B81 behebt die im Scroll-Video sichtbaren Restprobleme nach B79/B80:

1. sichtbare englische Hero-/Meta-Texte oben auf der Seite,
2. Layout-Überläufe in den Hero-Karten,
3. Texte, die aus ihren Rahmen laufen,
4. störende Overlay-/Ghost-Artefakte.

## Änderungen

### Inhalt / Copy
Sichtbare Resttexte wurden auf Deutsch gesetzt:

- `PORTFOLIO PROTOTYPE · LITERATURE-DRIVEN MVP`
  → `MOORE · KLIMASCHUTZ · REGIONALE UMSETZUNG`
- `Peatland Transition Atlas`
  → `Moorschutz braucht räumliche Orientierung`
- `Mapping the space between drainage-based agriculture and rewetting-compatible land use.`
  → `Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung.`

### Layout
- Hero-Bereich hart auf einen klaren einspaltigen Präsentationsaufbau gesetzt.
- Claim-Karten auf belastbare Grid-Spalten mit Mindestbreiten umgestellt.
- Overflow-Wrapping für Karten- und Step-Texte verschärft.
- Pseudo-Element-Overlays in Hero-/Kartensteps unterdrückt.

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `docs/B81_fix_german_copy_and_layout_overflow.md`
- `tasks/done.md`

## Manuelle QA

Nach B81 prüfen:

1. Oberster Block komplett auf Deutsch.
2. Keine sichtbaren Begriffe wie `prototype`, `atlas`, `literature-driven`, `mapping the space ...`.
3. Hero-Karten brechen sauber um.
4. Kein Text läuft über Kartenränder hinaus.
5. Zentrale Kartenfolge funktioniert weiter.
"""
    write(DOC, doc)

    done_entry = f"""
## B81 - Fix German copy and layout overflow ({today})

- Replaced remaining visible English/meta hero texts with German copy.
- Hardened hero layout to prevent narrow columns and overflow.
- Added stronger wrapping/overflow rules for hero cards and central story cards.
- Suppressed residual overlay artefacts.
- Created `docs/B81_fix_german_copy_and_layout_overflow.md`.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B81 - Fix German copy and layout overflow" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B81 fix German copy and layout overflow complete.")
    print("Changed:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOC)}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
