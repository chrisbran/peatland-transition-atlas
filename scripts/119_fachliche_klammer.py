#!/usr/bin/env python3
"""
B119 - Fachliche Klammer

Purpose
-------
Re-introduce the focused technical frame that was intentionally kept light
during public hardening:

A) a concise GHG / water-table mechanism block;
B) a clearer "Warum Oberschwaben?" rationale;
C) stronger coupling of transformation pathways to current land-use contexts.

This patch keeps the page as an information/story page, not a SOLAMO project
brochure. SOLAMO is only used as research and implementation context.

Changed:
- index.html
- src/styles.css
- docs/B119_fachliche_klammer.md
- docs/B119_fachliche_klammer_audit.txt
- tasks/done.md

Not changed:
- public/maps/*
- data/*
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import html as html_lib
import re
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b119_fachliche_klammer"

REPORT = DOCS / "B119_fachliche_klammer.md"
AUDIT = DOCS / "B119_fachliche_klammer_audit.txt"

TODAY = date.today().isoformat()

B119_CLIMATE_MARKER = "<!-- B119_CLIMATE_MECHANISM -->"
B119_OB_MARKER = "<!-- B119_WHY_OBERSCHWABEN -->"
B119_TRANSFORM_MARKER = "<!-- B119_TRANSFORM_CONTEXT_INTRO -->"
B119_CSS_MARKER = "/* B119 Fachliche Klammer */"

CLIMATE_BLOCK = f"""
{B119_CLIMATE_MARKER}
<section id="b119ClimateMechanism" class="b119-fachblock" aria-labelledby="b119ClimateMechanismTitle">
  <p class="b119-kicker">Fachliche Klammer</p>
  <h2 id="b119ClimateMechanismTitle">Warum Wasserstand über Klimawirkung entscheidet</h2>
  <p>
    Moorböden speichern Kohlenstoff im Torf. Werden sie entwässert, gelangt Sauerstoff in den Torfkörper;
    Torf wird abgebaut und es entstehen langfristige Treibhausgasemissionen – vor allem CO₂, ergänzt durch
    CH₄- und N₂O-Komponenten.
  </p>
  <p>
    Höhere Wasserstände können den Torfabbau deutlich bremsen. Die tatsächliche Klimawirkung hängt jedoch
    vom Standort, vom Zielwasserstand und von der künftigen Nutzung ab. Diese Seite berechnet deshalb keine
    Treibhausgasminderung. Sie zeigt die räumliche Ausgangskulisse, in der Minderung durch Wasserstandsmanagement
    und angepasste Nutzung fachlich geprüft werden kann.
  </p>
  <p class="b119-source-note">
    Fachliche Grundlage:
    <a href="https://www.ipcc-nggip.iges.or.jp/public/wetlands/" rel="noopener">IPCC Wetlands Supplement</a>,
    <a href="https://www.umweltbundesamt.de/daten/umweltzustand-trends/klima/treibhausgas-emissionen-in-deutschland/emissionen-der-landnutzung-aenderung" rel="noopener">Umweltbundesamt</a>,
    <a href="https://www.bundesumweltministerium.de/themen/naturschutz/moorschutz" rel="noopener">BMUV</a>,
    <a href="https://www.lubw.baden-wuerttemberg.de/natur-und-landschaft/moorschutz" rel="noopener">LUBW</a>.
  </p>
</section>
"""

OBERSCHWABEN_BLOCK = f"""
{B119_OB_MARKER}
<section id="b119WhyOberschwaben" class="b119-fachblock b119-fachblock--compact" aria-labelledby="b119WhyOberschwabenTitle">
  <p class="b119-kicker">Fokusraum</p>
  <h2 id="b119WhyOberschwabenTitle">Warum Oberschwaben?</h2>
  <p>
    Oberschwaben ist für Baden-Württemberg ein zentraler Fokusraum, weil sich hier Moor- und Feuchtbodenkontexte,
    landwirtschaftliche Nutzung und Fragen künftiger Wertschöpfung besonders deutlich überlagern. Der Blick auf
    die Region macht die Transformationsfrage konkret: Wo treffen Klimaschutz, Wasserstand, heutige Nutzung,
    betriebliche Umstellung und regionale Kooperation aufeinander?
  </p>
  <p class="b119-source-note">
    Fachliche Einordnung:
    <a href="https://lazbw.landwirtschaft-bw.de/%2CLde/Startseite/Themen/Moorbodenbewirtschaftung" rel="noopener">LAZBW Moorbodenbewirtschaftung</a>,
    <a href="https://mlr.baden-wuerttemberg.de/de/unsere-themen/landwirtschaft/landwirtschaft-im-klimawandel/moore" rel="noopener">MLR BW Moore</a>,
    <a href="https://430a.uni-hohenheim.de/solamo-bw" rel="noopener">SOLAMO-BW</a>.
  </p>
</section>
"""

TRANSFORM_INTRO = f"""
{B119_TRANSFORM_MARKER}
<div class="b119-transform-intro">
  <p>
    Transformationspfade entstehen nicht allein aus dem Bodenkontext. Entscheidend ist, welche heutige Nutzung
    betroffen ist, welche Wasserstände erreichbar sind und ob passende Technik, Verarbeitung und Absatzwege
    vorhanden sind.
  </p>
  <p>
    Grünlanddominierte Schnittmengen führen eher zu Prüfpfaden wie Nasswiese, Nassweide oder extensiver
    Beweidung. Ackerbaulich genutzte Schnittmengen bedeuten meist stärkere Umstellung und benötigen andere
    Kulturen, Technik und Wertschöpfungsketten. Sonder- und Dauerkulturen sind als Einzelfall zu prüfen.
    Größere Flächenverbünde führen schnell zu Kooperationsfragen: Wasserstand, Gräben, Flächentausch,
    Verarbeitung und Abnahme lassen sich selten einzelbetrieblich lösen.
  </p>
</div>
"""

CSS_BLOCK = f"""
{B119_CSS_MARKER}
.b119-fachblock {{
  width: min(980px, calc(100% - 2rem));
  margin: clamp(3.5rem, 7vw, 6rem) auto;
  padding: clamp(1.35rem, 3vw, 2.3rem);
  border: 1px solid rgba(30, 42, 34, 0.14);
  border-radius: 1.25rem;
  background: rgba(255, 253, 246, 0.88);
  box-shadow: 0 18px 48px rgba(31, 38, 33, 0.08);
}}

.b119-fachblock--compact {{
  margin-top: clamp(2.5rem, 5vw, 4rem);
  margin-bottom: clamp(2.5rem, 5vw, 4rem);
}}

.b119-kicker {{
  margin: 0 0 .45rem;
  color: #657c38;
  font-size: .78rem;
  font-weight: 760;
  letter-spacing: .12em;
  text-transform: uppercase;
}}

.b119-fachblock h2 {{
  margin: 0 0 .85rem;
  max-width: 760px;
  font-size: clamp(1.45rem, 3vw, 2.35rem);
  line-height: 1.05;
}}

.b119-fachblock p {{
  max-width: 850px;
  margin: .75rem 0 0;
  line-height: 1.58;
}}

.b119-source-note {{
  font-size: .9rem;
  color: rgba(37, 47, 39, .72);
}}

.b119-source-note a {{
  color: inherit;
  text-decoration-color: rgba(101, 124, 56, .5);
  text-underline-offset: .18em;
}}

.b119-transform-intro {{
  max-width: 920px;
  margin: 1.2rem auto 1.8rem;
  padding: 1.15rem 1.25rem;
  border-left: 4px solid #657c38;
  border-radius: .9rem;
  background: rgba(255, 253, 246, .74);
}}

.b119-transform-intro p {{
  margin: 0;
  line-height: 1.55;
}}

.b119-transform-intro p + p {{
  margin-top: .7rem;
}}
"""


HEADING_REPLACEMENTS = [
    ("Welche Nutzungen bei hohen Wasserständen tragfähig werden können", "Welche Prüfpfade folgen aus unterschiedlichen Nutzungskontexten?"),
    ("Welche Nutzung nasse Flächen tragen könnten", "Welche Prüfpfade folgen aus unterschiedlichen Nutzungskontexten?"),
    ("Welche Pfade aus nassen Flächen Wertschöpfung machen könnten", "Welche Prüfpfade folgen aus unterschiedlichen Nutzungskontexten?"),
    ("Welche Nutzung nasse Flächen tragen könnte", "Welche Prüfpfade folgen aus unterschiedlichen Nutzungskontexten?"),
]

RISK_PATTERNS = [
    "berechnetes Treibhausgasminderungspotenzial",
    "THG-Minderungspotenzial der gezeigten Flächen",
    "Eignung für Wiedervernässung",
    "priorisierte Flächen",
    "müssen wiedervernässt werden",
    "Diese Flächen sollen wiedervernässt werden",
    "Welche Betriebe sind betroffen",
    "This guided view",
    "Evidence explorer",
    "Prototype appendix",
    "Ã",
    "�",
]

REQUIRED_PATTERNS = [
    "Warum Wasserstand über Klimawirkung entscheidet",
    "Diese Seite berechnet deshalb keine Treibhausgasminderung",
    "Warum Oberschwaben?",
    "Oberschwaben ist für Baden-Württemberg ein zentraler Fokusraum",
    "Welche Prüfpfade folgen aus unterschiedlichen Nutzungskontexten?",
    "Transformationspfade entstehen nicht allein aus dem Bodenkontext",
    "IPCC Wetlands Supplement",
    "Umweltbundesamt",
    "LUBW",
    "LAZBW Moorbodenbewirtschaftung",
    "SOLAMO-BW",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def visible_text(raw: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def find_section_start_by_id(raw: str, section_id: str) -> int:
    pattern = re.compile(rf"<section\b(?=[^>]*\bid=['\"]{re.escape(section_id)}['\"])[^>]*>", flags=re.IGNORECASE)
    m = pattern.search(raw)
    return m.start() if m else -1


def find_section_start_before(raw: str, pos: int) -> int:
    matches = list(re.finditer(r"<section\b[^>]*>", raw[:pos], flags=re.IGNORECASE))
    return matches[-1].start() if matches else -1


def insert_once(raw: str, marker: str, insert_at: int, block: str) -> tuple[str, bool, str]:
    if marker in raw:
        return raw, False, "already_present"
    if insert_at < 0 or insert_at > len(raw):
        return raw, False, "invalid_insert_position"
    return raw[:insert_at] + "\n\n" + block.strip() + "\n\n" + raw[insert_at:], True, "inserted"


def replace_headings(raw: str) -> tuple[str, list[str]]:
    out = raw
    changed: list[str] = []
    for old, new in HEADING_REPLACEMENTS:
        if old in out:
            out = out.replace(old, new)
            changed.append(old)
    return out, changed


def insert_transform_intro(raw: str) -> tuple[str, bool, str]:
    if B119_TRANSFORM_MARKER in raw:
        return raw, False, "already_present"

    heading = "Welche Prüfpfade folgen aus unterschiedlichen Nutzungskontexten?"
    pos = raw.find(heading)
    if pos < 0:
        return raw, False, "heading_not_found"

    closing_candidates = []
    for close in ("</h2>", "</h3>", "</h1>"):
        c = raw.find(close, pos)
        if c >= 0:
            closing_candidates.append((c + len(close), close))
    if not closing_candidates:
        return raw, False, "heading_close_not_found"

    insert_at = min(closing_candidates)[0]
    return raw[:insert_at] + "\n\n" + TRANSFORM_INTRO.strip() + "\n\n" + raw[insert_at:], True, "inserted"


def add_css_once(css: str) -> tuple[str, bool]:
    if B119_CSS_MARKER in css:
        return css, False
    return css.rstrip() + "\n\n" + CSS_BLOCK.strip() + "\n", True


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B119 - Fachliche Klammer"
    if marker in current:
        return
    entry = f"""
## B119 - Fachliche Klammer ({TODAY})

- Added a concise GHG/water-table mechanism block.
- Added a focused Oberschwaben rationale without turning the page into a SOLAMO project brochure.
- Reframed transformation pathways as land-use-context-specific Prüfpfade.
- Added compact public source links to IPCC, UBA, BMUV, LUBW, LAZBW, MLR BW and SOLAMO-BW.
- Did not modify maps, map data, map colours or raw data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def write_report(actions: list[tuple[str, str]]) -> None:
    lines = [
        "# B119 – Fachliche Klammer",
        "",
        f"Stand: {TODAY}",
        "",
        "## Zweck",
        "",
        "B119 stärkt die fachliche Klammer der Seite, ohne sie zu einer Projektvorstellungsseite umzubauen.",
        "",
        "## Eingebaut",
        "",
        "- Wasserstand-/Treibhausgas-Mechanismus",
        "- Oberschwaben als fachlich begründeter Fokusraum",
        "- Transformationspfade als Prüfpfade aus Nutzungskontexten",
        "- kompakte Quellenhinweise zu offiziellen und methodischen Grundlagen",
        "",
        "## Actions",
        "",
        "| Action | Status |",
        "|---|---|",
    ]
    for name, status in actions:
        lines.append(f"| `{name}` | `{status}` |")
    lines.extend([
        "",
        "## Review",
        "",
        "```powershell",
        "Get-Content docs\\B119_fachliche_klammer_audit.txt",
        "Select-String -Encoding UTF8 -Path index.html -Pattern \"Warum Wasserstand\",\"berechnet deshalb keine Treibhausgasminderung\",\"Warum Oberschwaben\",\"Prüfpfade\",\"Ã\",\"Evidence explorer\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ])
    write_text(REPORT, "\n".join(lines))


def write_audit(raw: str, actions: list[tuple[str, str]]) -> None:
    vis = visible_text(raw)
    risk_counts = {p: vis.count(p) for p in RISK_PATTERNS}
    required_counts = {p: vis.count(p) for p in REQUIRED_PATTERNS}

    status = "OK" if all(v == 0 for v in risk_counts.values()) and all(v > 0 for v in required_counts.values()) else "REVIEW REQUIRED"

    lines = [
        "# B119 fachliche Klammer audit",
        "",
        f"- Status: {status}",
        f"- Risk findings: {sum(1 for v in risk_counts.values() if v > 0)}",
        f"- Missing required findings: {sum(1 for v in required_counts.values() if v == 0)}",
        "",
        "## Actions",
        "",
        "| Action | Status |",
        "|---|---|",
    ]
    for name, action_status in actions:
        lines.append(f"| `{name}` | `{action_status}` |")

    lines.extend([
        "",
        "## Risk patterns",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ])
    for p, c in risk_counts.items():
        lines.append(f"| `{p}` | {c} |")

    lines.extend([
        "",
        "## Required patterns",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ])
    for p, c in required_counts.items():
        lines.append(f"| `{p}` | {c} |")

    lines.extend([
        "",
        "## Recommended checks",
        "",
        "```powershell",
        "Select-String -Encoding UTF8 -Path index.html -Pattern \"Warum Wasserstand\",\"berechnet deshalb keine Treibhausgasminderung\",\"Warum Oberschwaben\",\"Prüfpfade\",\"IPCC\",\"Umweltbundesamt\",\"LAZBW\",\"SOLAMO-BW\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "```",
        "",
    ])
    write_text(AUDIT, "\n".join(lines))


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)
    if not CSS.exists():
        print(f"Missing {rel(CSS)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    index_backup = BACKUP_DIR / "index_before_b119.html"
    css_backup = BACKUP_DIR / "styles_before_b119.css"
    if not index_backup.exists():
        shutil.copy2(INDEX, index_backup)
    if not css_backup.exists():
        shutil.copy2(CSS, css_backup)

    html = read_text(INDEX)
    css = read_text(CSS)
    actions: list[tuple[str, str]] = []

    # Normalize transformation heading first, so the intro can be inserted.
    html, changed_headings = replace_headings(html)
    actions.append(("replace transformation heading", "changed:" + ",".join(changed_headings) if changed_headings else "not_found_or_already_changed"))

    # Insert climate block before the main map story.
    central_start = find_section_start_by_id(html, "centralGlobalMapStory")
    html, changed, status = insert_once(html, B119_CLIMATE_MARKER, central_start, CLIMATE_BLOCK)
    actions.append(("insert climate mechanism block before centralGlobalMapStory", status))

    # Insert Oberschwaben rationale before the Oberschwaben focus section.
    ob_pos = html.find("Oberschwaben, wo Moorschutz auf Landwirtschaft trifft")
    ob_start = find_section_start_before(html, ob_pos) if ob_pos >= 0 else -1
    html, changed, status = insert_once(html, B119_OB_MARKER, ob_start, OBERSCHWABEN_BLOCK)
    actions.append(("insert Warum Oberschwaben block before Oberschwaben focus section", status))

    # Insert transformation intro after heading.
    html, changed, status = insert_transform_intro(html)
    actions.append(("insert land-use-context transformation intro", status))

    # Add CSS.
    css, css_changed = add_css_once(css)
    actions.append(("append B119 CSS", "inserted" if css_changed else "already_present"))

    write_text(INDEX, html)
    write_text(CSS, css)
    update_done()
    write_report(actions)
    write_audit(html, actions)

    print("B119 fachliche Klammer complete.")
    print("Changed/created:")
    for p in [INDEX, CSS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(index_backup)}")
    print(f"  {rel(css_backup)}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B119_fachliche_klammer_audit.txt")
    print("  Select-String -Encoding UTF8 -Path index.html -Pattern \"Warum Wasserstand\",\"berechnet deshalb keine Treibhausgasminderung\",\"Warum Oberschwaben\",\"Prüfpfade\",\"Ã\",\"Evidence explorer\"")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
