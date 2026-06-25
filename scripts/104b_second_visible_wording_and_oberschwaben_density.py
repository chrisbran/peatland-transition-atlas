#!/usr/bin/env python3
"""
B104b - Second visible wording polish and Oberschwaben card density pass

Purpose
-------
Targeted follow-up after B104 based on visual/text review.

Fixes:
- Removes remaining self-referential wording in the scale steps.
- Removes "30 Sekunden" from the primer details label.
- Reduces colon-heavy headings.
- Compresses the method-boundary wording.
- Removes the redundant B98c/pathway QA note from the public pathway section.
- Makes Oberschwaben step cards smaller and more spaced.
- Gives the Oberschwaben map slightly more visual priority on desktop.

Does NOT:
- remove hidden/retired archive sections
- change map image assets
- change GIS/data folders
- change JS layer-state logic
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REPORT = DOCS / "B104b_second_visible_wording_and_oberschwaben_density.md"
AUDIT = DOCS / "B104b_second_visible_wording_and_oberschwaben_density_audit.txt"

CSS_START = "/* B104B_VISIBLE_WORDING_AND_OBERSCHWABEN_DENSITY_START */"
CSS_END = "/* B104B_VISIBLE_WORDING_AND_OBERSCHWABEN_DENSITY_END */"
HTML_START = "<!-- B104B_VISIBLE_WORDING_POLISH_START -->"
HTML_END = "<!-- B104B_VISIBLE_WORDING_POLISH_END -->"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def replace_exact(text: str, old: str, new: str, changes: list[tuple[str, int]]) -> str:
    n = text.count(old)
    if n:
        text = text.replace(old, new)
    changes.append((old, n))
    return text


def replace_regex(text: str, pattern: str, repl: str, changes: list[tuple[str, int]], label: str, flags=0) -> str:
    text, n = re.subn(pattern, repl, text, flags=flags)
    changes.append((label, n))
    return text


def remove_pathway_qa_note(html: str, changes: list[tuple[str, int]]) -> str:
    """Remove the redundant B98c/B104 pathway note if present."""
    patterns = [
        r"\n\s*<div class=\"moore-pathway-note\">\s*<h3>Was die B98c-QA nahelegt</h3>.*?</div>\s*",
        r"\n\s*<div class=\"moore-pathway-note\">\s*<h3>Was die Verschneidung nahelegt</h3>.*?</div>\s*",
    ]
    total = 0
    for pat in patterns:
        html, n = re.subn(pat, "\n", html, flags=re.DOTALL)
        total += n
    changes.append(("remove redundant moore-pathway-note", total))
    return html


def insert_marker(html: str) -> str:
    if HTML_START in html:
        return html
    marker = f"\n{HTML_START}\n<!-- B104b applied second visible wording polish and Oberschwaben density override. -->\n{HTML_END}\n"
    pos = html.lower().rfind("</body>")
    if pos != -1:
        return html[:pos].rstrip() + marker + "\n" + html[pos:]
    return html.rstrip() + marker + "\n"


def apply_html(html: str) -> tuple[str, list[tuple[str, int]]]:
    changes: list[tuple[str, int]] = []
    t = html

    # Primer: keep optional detail, remove salesy/time claim.
    t = replace_exact(t, "Fachlicher Hintergrund in 30 Sekunden", "Fachlicher Hintergrund", changes)

    # Scale steps and remaining self-referential wording. Include old and B104 versions.
    t = replace_exact(t, "Deutschland ist eine Umsetzungsebene.", "Deutschland zeigt, wo Planung und Förderung ansetzen.", changes)
    t = replace_exact(t, "Nationale Kulissen übersetzen globale Relevanz in Planung und Förderung.", "Nationale Karten zeigen, wo Förderprogramme und Flächenkulissen greifen können.", changes)
    t = replace_exact(t, "Deutschland rahmt Planung und Förderung.", "Deutschland zeigt, wo Planung und Förderung ansetzen.", changes)
    t = replace_exact(t, "Nationale Kulissen zeigen, wo Planung und Förderung ansetzen können.", "Nationale Karten zeigen, wo Förderprogramme und Flächenkulissen greifen können.", changes)

    t = replace_exact(t, "Die Thünen-Kulisse konkretisiert organische Böden.", "Die Thünen-Kulisse zeigt organische Böden.", changes)
    t = replace_exact(t, "Sie macht sichtbar, wo organische Böden für nationale Umsetzung relevant werden.", "Sie zeigt, wo Moor- und organische Böden in der Bundesplanung eine Rolle spielen.", changes)
    t = replace_exact(t, "Sie macht sichtbar, wo organische Böden für Planung und Förderung relevant sind.", "Sie zeigt, wo Moor- und organische Böden in der Bundesplanung eine Rolle spielen.", changes)

    t = replace_exact(t, "BK50 zeigt Moor- und Feuchtbodenkontext.", "BK50 ordnet den Bodenkontext ein.", changes)
    t = replace_exact(t, "Die Karte ordnet räumlich ein, ersetzt aber keine Eignungs- oder Prioritätsprüfung.",
                      "Sie zeigt Moor- und Feuchtbodenbereiche, ersetzt aber keine Eignungsprüfung.", changes)

    t = replace_exact(t, "Europa wird zur Umsetzungsebene.", "Europa zeigt den politischen Maßstab.", changes)
    t = replace_exact(t, "Politische und administrative Grenzen übersetzen globale Relevanz in Handlungsräume.",
                      "Politische und administrative Grenzen bestimmen, wo geplant und gefördert werden kann.", changes)
    t = replace_exact(t, "Politische und administrative Grenzen bestimmen, wo aus globaler Relevanz Planung wird.",
                      "Politische und administrative Grenzen bestimmen, wo geplant und gefördert werden kann.", changes)

    # Headings: reduce colon rhythm.
    t = replace_exact(t, "Oberschwaben: regionale Ausgangslage", "Oberschwaben als Ausgangspunkt", changes)
    t = replace_exact(t, "Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird",
                      "Oberschwaben, wo Moorschutz auf Landwirtschaft trifft", changes)
    t = replace_exact(t, "Oberschwaben: Wo Moorschutz auf Landwirtschaft trifft",
                      "Oberschwaben, wo Moorschutz auf Landwirtschaft trifft", changes)

    # Method boundary: keep, but compress. It is necessary, not a large second story.
    t = replace_exact(
        t,
        "Einordnung statt Eignungskarte",
        "Was die Karten nicht leisten",
        changes
    )
    t = replace_exact(
        t,
        "Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung.\n          Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.",
        "Die Karten zeigen Bodenkontexte und räumliche Überschneidungen. Sie ersetzen keine Eignungsprüfung, Priorisierung oder betriebliche Betroffenheitsanalyse.",
        changes
    )
    t = replace_exact(
        t,
        "Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.",
        "Die Karten zeigen Bodenkontexte und räumliche Überschneidungen. Sie ersetzen keine Eignungsprüfung, Priorisierung oder betriebliche Betroffenheitsanalyse.",
        changes
    )
    t = replace_exact(
        t,
        "Datenbasis: Global Peatland Map 2.0, Thünen-Kulisse organischer Böden, BK50 Baden-Württemberg, LUBW/Moorschutzkonzeption, SOLAMO-BW-Projektinformationen.",
        "Daten: Global Peatland Map 2.0, Thünen-Kulisse organischer Böden, BK50 Baden-Württemberg, LUBW/Moorschutzkonzeption, SOLAMO-BW.",
        changes
    )

    # Oberschwaben wording, old and B104 variants.
    t = replace_exact(t, "Ein regionaler Umsetzungsraum", "Vier Landkreise als Planungsraum", changes)
    t = replace_exact(t, "Hier wird Moorschutz zur Umsetzungsfrage", "Hier beginnt die Planungsfrage", changes)
    t = replace_exact(t, "Hier beginnt die eigentliche Planungsfrage", "Hier beginnt die Planungsfrage", changes)
    t = replace_exact(t, "Transformationsfragen konkret werden", "konkrete Fragen entstehen", changes)

    # B101/B99 internal/source wording. Also catches B104 output.
    t = replace_exact(t, "Die interne Flächen-QA zeigt aber,", "Die Flächenverschneidung zeigt,", changes)
    t = replace_exact(t, "Die Flächenverschneidung zeigt,", "Die Verschneidung zeigt,", changes)
    t = replace_exact(t, "nicht nur visuell plausibel ist, sondern auch quantitativ trägt", "auch in der Bilanz sichtbar wird", changes)
    t = replace_exact(t, "eigene Verschneidung und B98c-Klassifikations-QA", "eigene Verschneidung und Prüfung der Nutzungsklassen", changes)
    t = replace_exact(t, "eigene Verschneidung und gesonderte Prüfung der Nutzungsklassen", "eigene Verschneidung und Prüfung der Nutzungsklassen", changes)
    t = replace_exact(t, "eigene räumliche Verschneidung und Klassifikations-QA", "eigene räumliche Verschneidung und Prüfung der Nutzungsklassen", changes)
    t = replace_exact(t, "eigene räumliche Verschneidung und gesonderte Prüfung der Nutzungsklassen", "eigene räumliche Verschneidung und Prüfung der Nutzungsklassen", changes)
    t = replace_exact(t, "interne Plausibilisierung", "Plausibilisierung", changes)

    # Remove the duplicated pathway QA note. B101 already carries the quantitative finding.
    t = remove_pathway_qa_note(t, changes)

    # A few precise micro-edits for less abstract tone.
    t = replace_exact(t, "Moorbodenkontext braucht Planung", "Moorbodenkontext braucht konkrete Planung", changes)
    t = replace_exact(t, "Bodenkontext prägt mögliche Nutzungspfade.", "Der Bodenkontext begrenzt, was möglich ist.", changes)
    t = replace_exact(t, "Welche Pfade aus nassen Flächen Wertschöpfung machen könnten", "Welche Nutzung nasse Flächen tragen könnten", changes)

    t = replace_regex(t, r"[ \t]{2,}", " ", changes, "collapse repeated spaces")
    t = insert_marker(t)
    return t, changes


def build_css_override() -> str:
    return f"""{CSS_START}
/*
  B104b density and behaviour pass for Oberschwaben:
  - cards are smaller relative to their text,
  - cards are spaced farther apart,
  - the first card no longer sits immediately beside/over the map at section start,
  - desktop layout gives the map slightly more room,
  - active state is visible without making inactive cards feel like dead content.
*/

@media (min-width: 1101px) {{
  .moore-ob-grid {{
    grid-template-columns: minmax(760px, 2.08fr) minmax(280px, 0.54fr) !important;
    gap: clamp(2.4rem, 4.5vw, 5.6rem) !important;
  }}

  .moore-ob-stage-column {{
    top: clamp(0.85rem, 6vh, 3.8rem) !important;
  }}

  .moore-ob-steps {{
    padding-top: clamp(8rem, 22vh, 15rem) !important;
    padding-bottom: clamp(14rem, 30vh, 24rem) !important;
    gap: clamp(5.5rem, 15vh, 10rem) !important;
  }}

  .moore-ob-step {{
    min-height: auto !important;
    padding: clamp(0.9rem, 1.55vw, 1.18rem) !important;
    border-radius: 0.85rem !important;
    max-width: 360px !important;
    background: rgba(255, 252, 244, 0.66) !important;
  }}

  .moore-ob-step.is-active {{
    background: rgba(255, 252, 244, 0.76) !important;
    border-color: rgba(48, 58, 51, 0.22) !important;
  }}

  .moore-ob-step h3 {{
    font-size: clamp(1.02rem, 1.32vw, 1.28rem) !important;
    line-height: 1.14 !important;
  }}

  .moore-ob-step p:not(.moore-ob-step-label) {{
    margin-top: 0.62rem !important;
    font-size: clamp(0.86rem, 0.92vw, 0.95rem) !important;
    line-height: 1.45 !important;
  }}

  .moore-ob-step-label {{
    margin-bottom: 0.42rem !important;
    font-size: 0.66rem !important;
    letter-spacing: 0.09em !important;
  }}
}}

@media (max-width: 1100px) {{
  .moore-ob-steps {{
    gap: clamp(2.2rem, 8vh, 4rem) !important;
  }}

  .moore-ob-step {{
    min-height: auto !important;
    padding: clamp(1rem, 3vw, 1.35rem) !important;
  }}
}}

/* Keep the method note compact where the surrounding theme has made it too large. */
.method-card,
.moore-method-card {{
  padding-block: clamp(1rem, 2vw, 1.4rem) !important;
}}

.method-card p,
.moore-method-card p {{
  max-width: 860px !important;
}}
{CSS_END}"""


def insert_css(css: str) -> tuple[str, str]:
    block = build_css_override()
    pat = re.compile(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), re.DOTALL)
    if pat.search(css):
        return pat.sub(block, css), "replaced existing B104b CSS override"
    return css.rstrip() + "\n\n" + block + "\n", "appended B104b CSS override"


def simple_counts(text: str) -> dict[str, int]:
    patterns = {
        "30 Sekunden": r"30 Sekunden",
        "B98c": r"\bB98c\b",
        "Flächen-QA": r"Flächen-QA",
        "Klassifikations-QA": r"Klassifikations-QA",
        "Methodeische": r"Methodeische",
        "Nasseverträgliche": r"Nasseverträgliche",
        "Umsetzungsebene": r"Umsetzungsebene",
        "Umsetzungsfrage": r"Umsetzungsfrage",
        "übersetzen": r"übersetzen",
        "Oberschwaben colon headings": r"Oberschwaben:",
        "moore-pathway-note": r"moore-pathway-note",
    }
    return {k: len(re.findall(p, text, flags=re.IGNORECASE)) for k, p in patterns.items()}


def write_report(today: str, changes: list[tuple[str, int]], css_action: str, before: dict[str, int], after: dict[str, int]) -> None:
    lines = [
        "# B104b - Second Visible Wording Polish and Oberschwaben Density Pass",
        "",
        f"Date: {today}",
        "",
        "## Result",
        "",
        "B104b applied a second targeted public-copy polish and a CSS-only density pass for the Oberschwaben scrolly cards.",
        "",
        "## Changed files",
        "",
        "- `index.html`",
        "- `src/styles.css`",
        "- `docs/B104b_second_visible_wording_and_oberschwaben_density.md`",
        "- `docs/B104b_second_visible_wording_and_oberschwaben_density_audit.txt`",
        "- `tasks/done.md`",
        "",
        "## Design/editorial decisions",
        "",
        "- Keep the method boundary, but make it read like a compact note rather than a second story block.",
        "- Remove the redundant B98c/pathway QA note because B101 already carries the quantitative evidence.",
        "- Keep the Oberschwaben scrolly, but reduce card size and increase card spacing.",
        "- Avoid additional sticky modules until the current flow is visually stable.",
        "",
        "## CSS action",
        "",
        f"- {css_action}",
        "",
        "## Replacement counts",
        "",
        "| Text / pattern | Count |",
        "|---|---:|",
    ]
    for old, n in changes:
        if n:
            shown = old.replace("\n", " ")
            if len(shown) > 110:
                shown = shown[:107] + "..."
            lines.append(f"| `{shown}` | {n} |")

    lines.extend([
        "",
        "## Smoke-test counts",
        "",
        "| Pattern | Before | After |",
        "|---|---:|---:|",
    ])
    for key in before:
        lines.append(f"| {key} | {before[key]} | {after[key]} |")

    lines.extend([
        "",
        "## Next step",
        "",
        "Run B103b again and review the corrected visible findings. Then inspect the Oberschwaben scrolly locally.",
        "",
    ])

    write_text(REPORT, "\n".join(lines))


def write_audit(before: dict[str, int], after: dict[str, int]) -> None:
    lines = [
        "# B104b audit",
        "",
        "## Text checks",
        "",
        f"- `30 Sekunden` removed: {'OK' if after.get('30 Sekunden', 1) == 0 else 'REVIEW'}",
        f"- `B98c` removed/reduced: before {before.get('B98c', 0)}, after {after.get('B98c', 0)}",
        f"- `Flächen-QA` removed/reduced: before {before.get('Flächen-QA', 0)}, after {after.get('Flächen-QA', 0)}",
        f"- `Klassifikations-QA` removed/reduced: before {before.get('Klassifikations-QA', 0)}, after {after.get('Klassifikations-QA', 0)}",
        f"- `Oberschwaben:` colon headings reduced: before {before.get('Oberschwaben colon headings', 0)}, after {after.get('Oberschwaben colon headings', 0)}",
        f"- redundant `.moore-pathway-note` removed: {'OK' if after.get('moore-pathway-note', 1) == 0 else 'REVIEW'}",
        "",
        "## Visual checks",
        "",
        "- Oberschwaben cards should be smaller relative to their text.",
        "- The gap between Oberschwaben cards should be larger.",
        "- The first Oberschwaben card should no longer feel pinned to the map from the first moment.",
        "- The map should feel slightly more dominant on desktop.",
        "- The method boundary should read as a compact note, not as a full extra section.",
        "",
        "## Commands",
        "",
        "```powershell",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ]
    write_text(AUDIT, "\n".join(lines))


def update_done(today: str) -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B104b - Second visible wording polish and Oberschwaben density"
    if marker in current:
        return
    entry = f"""
## B104b - Second visible wording polish and Oberschwaben density ({today})

- Removed remaining self-referential wording and reduced colon-heavy headings.
- Removed `30 Sekunden` from the moor-primer detail label.
- Kept the method boundary but compressed its wording.
- Removed redundant public B98c/pathway QA note.
- Added CSS override to make Oberschwaben step cards smaller and more spaced.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    if not INDEX.exists():
        print(f"B104b cannot run. Missing {rel(INDEX)}")
        sys.exit(1)
    if not CSS.exists():
        print(f"B104b cannot run. Missing {rel(CSS)}")
        sys.exit(1)

    today = date.today().isoformat()

    html = read_text(INDEX)
    css = read_text(CSS)

    before = simple_counts(html)
    new_html, changes = apply_html(html)
    after = simple_counts(new_html)

    new_css, css_action = insert_css(css)

    write_text(INDEX, new_html)
    write_text(CSS, new_css)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    write_report(today, changes, css_action, before, after)
    write_audit(before, after)
    update_done(today)

    print("B104b second visible wording polish and Oberschwaben density pass complete.")
    print("Changed/created:")
    for p in [INDEX, CSS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print("Next review:")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  Get-Content docs\\B104b_second_visible_wording_and_oberschwaben_density_audit.txt")


if __name__ == "__main__":
    main()
