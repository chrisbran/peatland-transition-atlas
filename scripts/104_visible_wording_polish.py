#!/usr/bin/env python3
"""
B104 - Visible wording polish and public copy cleanup

Purpose
-------
Apply a targeted, conservative polish to visible public copy based on B103b.

B103b showed:
- no visible prototype/explorer text
- 1 typo
- 2 visible English "peatland context" body/label strings
- repeated wording around "Umsetzung", "wird zu/zur", "übersetzen"
- internal public terms such as Flächen-QA, B98c, Klassifikations-QA

B104 fixes only those visible wording issues. It does NOT remove hidden/retired
archive sections and does NOT touch GIS data, map images or JS logic.

Changed files
-------------
- index.html
- docs/B104_visible_wording_polish.md
- docs/B104_visible_wording_polish_audit.txt
- tasks/done.md

Not changed intentionally
-------------------------
- src/styles.css
- JS logic
- map PNGs
- GIS/data folders
- hidden/retired archive sections except for harmless exact text replacements if the same string occurs there
"""

from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REPORT = DOCS / "B104_visible_wording_polish.md"
AUDIT = DOCS / "B104_visible_wording_polish_audit.txt"

HTML_START = "<!-- B104_VISIBLE_WORDING_POLISH_START -->"
HTML_END = "<!-- B104_VISIBLE_WORDING_POLISH_END -->"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def replace_exact(text: str, old: str, new: str, changes: list[tuple[str, int]]) -> str:
    count = text.count(old)
    if count:
        text = text.replace(old, new)
    changes.append((old, count))
    return text


def replace_regex(text: str, pattern: str, repl: str, changes: list[tuple[str, int]], label: str, flags=0) -> str:
    text, count = re.subn(pattern, repl, text, flags=flags)
    changes.append((label, count))
    return text


def insert_marker_note(html: str) -> str:
    """Add a lightweight HTML comment marker once, for traceability only."""
    if HTML_START in html:
        return html
    marker = f"\n{HTML_START}\n<!-- B104 applied visible wording polish. See docs/B104_visible_wording_polish.md. -->\n{HTML_END}\n"
    # Put near end of body if possible.
    pos = html.lower().rfind("</body>")
    if pos != -1:
        return html[:pos].rstrip() + marker + "\n" + html[pos:]
    return html.rstrip() + marker + "\n"


def apply_polish(html: str) -> tuple[str, list[tuple[str, int]]]:
    changes: list[tuple[str, int]] = []
    t = html

    # Clear typo.
    t = replace_exact(t, "Nasseverträgliche", "nässeverträgliche", changes)
    t = replace_exact(t, "nasseverträgliche", "nässeverträgliche", changes)

    # Visible English/map-context copy. Keep dataset names, translate human-facing labels.
    t = replace_exact(t, "Global peatland context", "Globale Moorverbreitung", changes)
    t = replace_exact(t, "Peatlands are spatially concentrated.", "Moore sind räumlich stark konzentriert.", changes)
    t = replace_exact(t, "Peatland context", "Moorkontext", changes)
    t = replace_exact(t, "Layer stack: Global Peatland Map 2.0 context and country hotspot layers.",
                      "Layerfolge: Global Peatland Map 2.0 als Kontext und Länder-Hotspot-Layer.", changes)
    t = replace_exact(t, "All images exported from the same ArcGIS global map frame.",
                      "Alle Bilder wurden aus demselben ArcGIS-Kartenrahmen exportiert.", changes)

    # Hero / navigation / framing: reduce "Umsetzung" where it is not essential.
    t = replace_exact(t, "Moore · Klimaschutz · regionale Umsetzung",
                      "Moore · Klimaschutz · regionale Planung", changes)
    t = replace_exact(t, ">Umsetzung<", ">Region<", changes)
    t = replace_exact(t, "Globale Karten zeigen Relevanz.\n          Umsetzung entsteht erst auf nationaler, regionaler und betrieblicher Ebene.",
                      "Globale Karten zeigen Relevanz.\n          Planung beginnt dort, wo nationale, regionale und betriebliche Ebenen zusammenkommen.", changes)
    t = replace_exact(t, "Globale Karten zeigen Relevanz. Umsetzung entsteht erst auf nationaler, regionaler und betrieblicher Ebene.",
                      "Globale Karten zeigen Relevanz. Planung beginnt dort, wo nationale, regionale und betriebliche Ebenen zusammenkommen.", changes)

    # Core argument and scale-step copy.
    t = replace_exact(t, "Aus Moorbodenkontext wird eine Umsetzungsfrage",
                      "Moorbodenkontext braucht Planung", changes)
    t = replace_exact(t, "Moorschutz wird erst dann planbar, wenn räumliche Kulissen, regionale Nutzung, betriebliche Betroffenheit und mögliche Wertschöpfungsketten gemeinsam betrachtet werden.",
                      "Planbar wird Moorschutz erst, wenn Bodenkulissen, Nutzung, betriebliche Betroffenheit und mögliche Wertschöpfungsketten zusammen betrachtet werden.", changes)
    t = replace_exact(t, "Europa wird zur Umsetzungsebene.",
                      "Europa zeigt den politischen Maßstab.", changes)
    t = replace_exact(t, "Politische und administrative Grenzen übersetzen globale Relevanz in Handlungsräume.",
                      "Politische und administrative Grenzen bestimmen, wo aus globaler Relevanz Planung wird.", changes)
    t = replace_exact(t, "Deutschland ist eine Umsetzungsebene.",
                      "Deutschland rahmt Planung und Förderung.", changes)
    t = replace_exact(t, "Nationale Kulissen übersetzen globale Relevanz in Planung und Förderung.",
                      "Nationale Kulissen zeigen, wo Planung und Förderung ansetzen können.", changes)
    t = replace_exact(t, "Sie macht sichtbar, wo organische Böden für nationale Umsetzung relevant werden.",
                      "Sie macht sichtbar, wo organische Böden für Planung und Förderung relevant sind.", changes)
    t = replace_exact(t, "Unterschiedliche Bodenkontexte verlangen unterschiedliche Übergänge.",
                      "Je nach Bodenkontext kommen andere Wege infrage.", changes)
    t = replace_exact(t, "Baden-Württemberg wird konkret.",
                      "Baden-Württemberg macht die Frage räumlich konkret.", changes)
    t = replace_exact(t, "Auf regionaler Ebene werden Moor- und Feuchtbodenkontexte zur Planungsfrage.",
                      "Auf regionaler Ebene zeigt sich, welche Moor- und Feuchtbodenkontexte planerisch relevant sind.", changes)

    # Section labels/headings.
    t = replace_exact(t, "Regionale Umsetzung", "Regionale Planung", changes)
    t = replace_exact(t, "SOLAMO-BW untersucht regionale Betriebsmuster und die Umsetzbarkeit von Nutzungskonzepten auf wiedervernässten Moorflächen.",
                      "SOLAMO-BW untersucht regionale Betriebsmuster und die praktische Tragfähigkeit von Nutzungskonzepten auf wiedervernässten Moorflächen.", changes)
    t = replace_exact(t, "Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird",
                      "Oberschwaben: Wo Moorschutz auf Landwirtschaft trifft", changes)
    t = replace_exact(t, "Ein regionaler Umsetzungsraum",
                      "Vier Landkreise als Planungsraum", changes)
    t = replace_exact(t, "Hier wird Moorschutz zur Umsetzungsfrage",
                      "Hier beginnt die eigentliche Planungsfrage", changes)
    t = replace_exact(t, "markiert Räume, in denen Transformationsfragen konkret werden: Bewirtschaftung,\n          Wasserstand, Betriebslogik, Förderung und regionale Abstimmung.",
                      "markiert Räume, in denen konkrete Fragen entstehen: Bewirtschaftung,\n          Wasserstand, Betriebslogik, Förderung und regionale Abstimmung.", changes)
    t = replace_exact(t, "markiert Räume, in denen Transformationsfragen konkret werden: Bewirtschaftung, Wasserstand, Betriebslogik, Förderung und regionale Abstimmung.",
                      "markiert Räume, in denen konkrete Fragen entstehen: Bewirtschaftung, Wasserstand, Betriebslogik, Förderung und regionale Abstimmung.", changes)

    # B101 key figures: remove internal QA/build wording from public copy.
    t = replace_exact(t, "Interne Verschneidung", "Flächenbilanz", changes)
    t = replace_exact(t, "Die interne Flächen-QA zeigt aber,",
                      "Die Flächenverschneidung zeigt,", changes)
    t = replace_exact(t, "dass die Schnittmenge aus landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext\n        nicht nur visuell plausibel ist, sondern auch quantitativ trägt.",
                      "dass die Überschneidung von landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext\n        auch in der Bilanz sichtbar wird.", changes)
    t = replace_exact(t, "dass die Schnittmenge aus landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext nicht nur visuell plausibel ist, sondern auch quantitativ trägt.",
                      "dass die Überschneidung von landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext auch in der Bilanz sichtbar wird.", changes)
    t = replace_exact(t, "Ackerland, bereinigt um Sonderfälle",
                      "Ackerland ohne Stilllegung und unklare Zuordnung", changes)
    t = replace_exact(t, "Stilllegung oder unklare FIONA-Zuweisung getrennt geprüft",
                      "Stilllegung oder unklare Zuordnung separat geführt", changes)
    t = replace_exact(t, "Diese Werte beschreiben eine Such- und Gesprächskulisse.",
                      "Diese Werte geben räumliche Orientierung.", changes)
    t = replace_exact(t, "eigene Verschneidung und B98c-Klassifikations-QA. Werte gerundet.",
                      "eigene Verschneidung und gesonderte Prüfung der Nutzungsklassen. Werte gerundet.", changes)

    # B99 pathways: reduce abstract/conceptual phrasing.
    t = replace_exact(t, "Von der Schnittmenge zu handhabbaren Transformationspfaden",
                      "Was aus der Schnittmenge folgt", changes)
    t = replace_exact(t, "Die Oberschwaben-Karte zeigt nicht, was auf einer einzelnen Fläche getan werden muss.\n    Sie zeigt, wo unterschiedliche Transformationspfade verhandelt werden müssen:",
                      "Die Oberschwaben-Karte entscheidet nicht über einzelne Flächen.\n    Sie zeigt, wo unterschiedliche Wege zu prüfen sind:", changes)
    t = replace_exact(t, "Die Oberschwaben-Karte zeigt nicht, was auf einer einzelnen Fläche getan werden muss. Sie zeigt, wo unterschiedliche Transformationspfade verhandelt werden müssen:",
                      "Die Oberschwaben-Karte entscheidet nicht über einzelne Flächen. Sie zeigt, wo unterschiedliche Wege zu prüfen sind:", changes)
    t = replace_exact(t, "Die Schnittmenge ist eine Such- und Gesprächskulisse.",
                      "Die Schnittmenge ist ein Ausgangspunkt für Prüfung und Abstimmung.", changes)
    t = replace_exact(t, "Was die B98c-QA nahelegt",
                      "Was die Verschneidung nahelegt", changes)
    t = replace_exact(t, "Die interne Flächen-QA stützt die qualitative Erzählung: Die Schnittmenge ist",
                      "Die Verschneidung stützt die Aussage der Karte: Die Schnittmenge ist", changes)
    t = replace_exact(t, "eigene räumliche Verschneidung und Klassifikations-QA.\n    Zahlen dienen hier\n    der internen Plausibilisierung, nicht als flächenscharfe Planungsaussage.",
                      "eigene räumliche Verschneidung und gesonderte Prüfung der Nutzungsklassen.\n    Die Zahlen dienen\n    der Plausibilisierung, nicht als flächenscharfe Planungsaussage.", changes)
    t = replace_exact(t, "eigene räumliche Verschneidung und Klassifikations-QA. Zahlen dienen hier der internen Plausibilisierung, nicht als flächenscharfe Planungsaussage.",
                      "eigene räumliche Verschneidung und gesonderte Prüfung der Nutzungsklassen. Die Zahlen dienen der Plausibilisierung, nicht als flächenscharfe Planungsaussage.", changes)

    # B102 matrix: keep the matrix, but make labels less report-like.
    t = replace_exact(t, "Welche Pfade aus nassen Flächen Wertschöpfung machen könnten",
                      "Welche Nutzung nasse Flächen tragen könnten", changes)
    t = replace_exact(t, "Die Transformationspfade werden erst tragfähig, wenn aus Biomasse, Pflege,\n      Energie oder Flächenorganisation reale Abnahme- und Erlöslogiken entstehen.",
                      "Die Pfade werden erst tragfähig, wenn für Biomasse, Pflege,\n      Energie oder Flächenorganisation verlässliche Abnahme und Erlöse entstehen.", changes)
    t = replace_exact(t, "Die Transformationspfade werden erst tragfähig, wenn aus Biomasse, Pflege, Energie oder Flächenorganisation reale Abnahme- und Erlöslogiken entstehen.",
                      "Die Pfade werden erst tragfähig, wenn für Biomasse, Pflege, Energie oder Flächenorganisation verlässliche Abnahme und Erlöse entstehen.", changes)
    t = replace_exact(t, "Produktlogik", "Nutzung / Produkt", changes)
    t = replace_exact(t, "Reifegrad", "Stand", changes)
    t = replace_exact(t, "Hauptengpass", "Wo es klemmt", changes)

    # General cleanup for double spaces created by replacements.
    t = replace_regex(t, r"[ \t]{2,}", " ", changes, "collapse repeated spaces")
    t = insert_marker_note(t)

    return t, changes


def visible_counts(html: str) -> dict[str, int]:
    """Simple post-change visible-ish counts; not a full parser, but useful as smoke test."""
    patterns = {
        "Nasseverträgliche": r"Nasseverträgliche|nasseverträgliche",
        "prototype/explorer": r"\b(?:prototype|explorer)\b",
        "peatland context": r"peatland context|Peatland context|Global peatland context",
        "Umsetzung*": r"\bUmsetzung\w*",
        "wird zu/zur/zum/eine": r"\bwird\s+(?:zu|zur|zum|eine|einem|einer)\b",
        "übersetz*": r"\bübersetz\w*",
        "Flächen-QA": r"Flächen-QA",
        "B98c": r"\bB98c\b",
        "Klassifikations-QA": r"Klassifikations-QA",
    }
    return {k: len(re.findall(p, html, flags=re.IGNORECASE)) for k, p in patterns.items()}


def write_report(today: str, changes: list[tuple[str, int]], before_counts: dict[str, int], after_counts: dict[str, int]) -> None:
    md = [
        "# B104 - Visible Wording Polish",
        "",
        f"Date: {today}",
        "",
        "## Result",
        "",
        "B104 applied a targeted polish to visible public wording based on B103b.",
        "",
        "## Changed files",
        "",
        "- `index.html`",
        "- `docs/B104_visible_wording_polish.md`",
        "- `docs/B104_visible_wording_polish_audit.txt`",
        "- `tasks/done.md`",
        "",
        "## Not changed",
        "",
        "- `src/styles.css`",
        "- JS logic",
        "- map PNGs",
        "- GIS/data folders",
        "- hidden/retired archive sections were not intentionally removed",
        "",
        "## Replacement counts",
        "",
        "| Pattern / old text | Replacements |",
        "|---|---:|",
    ]
    for old, count in changes:
        if count:
            shown = old.replace("\n", " ")
            if len(shown) > 100:
                shown = shown[:97] + "..."
            md.append(f"| `{shown}` | {count} |")

    md.extend([
        "",
        "## Smoke-test counts in HTML after replacement",
        "",
        "| Pattern | Before | After |",
        "|---|---:|---:|",
    ])
    for key in before_counts:
        md.append(f"| {key} | {before_counts[key]} | {after_counts[key]} |")

    md.extend([
        "",
        "## Editorial intent",
        "",
        "- Keep the existing structure and matrix.",
        "- Remove the obvious typo.",
        "- Translate visible English map-context labels.",
        "- Reduce the repeated `Umsetzung / wird zu / übersetzen` rhythm.",
        "- Replace internal QA/build terms in visible public copy with reader-facing wording.",
        "",
        "## Next step",
        "",
        "Run B103b again and compare `docs/B103b_visible_findings.csv` and `docs/B103b_wording_frequency.csv`.",
        "",
    ])
    write_text(REPORT, "\n".join(md))


def write_audit(before_counts: dict[str, int], after_counts: dict[str, int]) -> None:
    lines = [
        "# B104 visible wording polish audit",
        "",
        "## Expected changes",
        "",
        f"- Typo `Nasseverträgliche`: {'OK' if after_counts.get('Nasseverträgliche', 1) == 0 else 'REVIEW'}",
        f"- Visible `peatland context` English labels reduced: before {before_counts.get('peatland context', 0)}, after {after_counts.get('peatland context', 0)}",
        f"- `Flächen-QA` removed/reduced: before {before_counts.get('Flächen-QA', 0)}, after {after_counts.get('Flächen-QA', 0)}",
        f"- `B98c` removed/reduced from public copy: before {before_counts.get('B98c', 0)}, after {after_counts.get('B98c', 0)}",
        f"- `Klassifikations-QA` removed/reduced: before {before_counts.get('Klassifikations-QA', 0)}, after {after_counts.get('Klassifikations-QA', 0)}",
        "",
        "## Manual review",
        "",
        "- Re-run `python scripts\\103b_corrected_visible_text_audit.py`.",
        "- Check only corrected visible findings, not hidden findings.",
        "- Scroll the page and confirm the wording still reads naturally.",
        "- Confirm no map or scrolly behavior changed.",
        "",
    ]
    write_text(AUDIT, "\n".join(lines))


def update_done(today: str) -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B104 - Visible wording polish"
    if marker in current:
        return

    entry = f"""
## B104 - Visible wording polish ({today})

- Fixed visible typo `Nasseverträgliche` -> `nässeverträgliche`.
- Translated visible English peatland-context labels.
- Reduced repeated `Umsetzung`, `wird zu/zur`, and `übersetzen` phrasing.
- Replaced public internal QA wording (`Flächen-QA`, `B98c`, `Klassifikations-QA`) with reader-facing wording.
- Did not intentionally remove hidden/retired prototype/archive sections.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    if not INDEX.exists():
        print(f"B104 cannot run. Missing {rel(INDEX)}")
        sys.exit(1)

    today = date.today().isoformat()
    html = read_text(INDEX)
    before_counts = visible_counts(html)
    new_html, changes = apply_polish(html)
    after_counts = visible_counts(new_html)

    write_text(INDEX, new_html)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    write_report(today, changes, before_counts, after_counts)
    write_audit(before_counts, after_counts)
    update_done(today)

    print("B104 visible wording polish complete.")
    print("Changed/created:")
    for p in [INDEX, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print("Review next:")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  Get-Content docs\\B104_visible_wording_polish_audit.txt")
    print("  Import-Csv docs\\B103b_visible_findings.csv -Delimiter ';' | Format-Table -Auto")
    print("")
    print("Note:")
    print("  B104 does not intentionally remove hidden/retired archive sections.")


if __name__ == "__main__":
    main()
