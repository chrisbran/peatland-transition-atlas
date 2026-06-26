#!/usr/bin/env python3
"""
B116 - Public page hardening

Hardens the public HTML for project-internal / MLR-BW / Uni-Hohenheim review:
- removes old English prototype/explorer blocks when markers are present;
- keeps the German main story and Oberschwaben sequence;
- strengthens GHG mechanism and Oberschwaben rationale;
- de-risks wording around affectedness, suitability, priority and GHG mitigation;
- simplifies Oberschwaben area-balance labels;
- replaces visible developer/caption leftovers when exact text matches are found.

No CSS, map or data files are changed.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import csv
import html as html_lib
import re
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b116_public_page_hardening"

REPORT = DOCS / "B116_public_page_hardening.md"
AUDIT = DOCS / "B116_public_page_hardening_audit.txt"
FINDINGS = DOCS / "B116_public_text_findings.csv"

TODAY = date.today().isoformat()

RANGE_REMOVALS = [
    ("remove_old_guided_english_map_story", "Geführte Kartenstory", "Globale Moorverbreitung"),
    ("remove_post_main_map_prototype_explorer", "After the main map", "Oberschwaben, wo Moorschutz auf Landwirtschaft trifft"),
]

SECTION_MARKERS_TO_REMOVE = [
    "This guided view is the bridge between the existing explorer layers",
    "Each map layer answers a different question",
    "The map below is the core narrative",
    "The rest of the page is an evidence explorer",
    "Evidence explorer: where are drained organic soil emissions concentrated",
    "Evidence explorer: cases and transition evidence",
    "South Germany fit: which pathways remain plausible",
    "Prototype appendix",
    "How to read this prototype",
    "Current prototype datasets",
    "Baden-Württemberg: where the peat and organic-soil context becomes spatial",
    "Loading country hotspot map",
    "Loading Baden-Württemberg BK50-Moor layer",
]

REPLACEMENTS = [
    ("Planbar wird Moorschutz erst, wenn Bodenkulissen, Nutzung, betriebliche Betroffenheit und mögliche Wertschöpfungsketten zusammen betrachtet werden.",
     "Planbar wird Moorschutz erst, wenn Bodenkulissen, Nutzungskontexte, Wasserstand, betriebliche Fragen und mögliche Wertschöpfungsketten zusammen betrachtet werden."),
    ("Dichtekarten zeigen, wo Belastung räumlich besonders konzentriert ist.",
     "Hotspotkarten zeigen, wo Belastung räumlich besonders deutlich wird."),
    ("Layerfolge: Global Peatland Map 2.0 als Kontext und Länder-Hotspot-Layer. Alle Bilder wurden aus demselben ArcGIS-Kartenrahmen exportiert.",
     "Datenbasis: Global Peatland Map 2.0 und FAOSTAT-Emissionsdaten zu drainierten organischen Böden; eigene kartografische Aufbereitung."),
    ("Ein Moor ist kein gewöhnlicher Boden. Solange Torf nass bleibt, speichert er Kohlenstoff; wird er entwässert, wird er zur dauerhaften Emissionsquelle. Darum führt die Oberschwaben-Story von Boden und Nutzung direkt zur Frage: Wie lässt sich Wasserstand verändern, ohne Betriebe und Landschaften zu überfordern?",
     "Moore sind Kohlenstoffspeicher, solange der Torf nass bleibt. Wird ein Moorboden entwässert, gelangt Sauerstoff in den Torfkörper; Torf wird abgebaut und es entstehen Treibhausgasemissionen. Darum führt die Oberschwaben-Story von Boden und Nutzung direkt zur Frage: Wo können höhere Wasserstände, angepasste Nutzung und regionale Wertschöpfung gemeinsam geprüft werden?"),
    ("Torf entsteht, wenn Pflanzenreste unter nassen, sauerstoffarmen Bedingungen langsamer abgebaut als aufgebaut werden. Sinkt der Wasserstand, gelangt Sauerstoff in den Torfkörper; Torf mineralisiert und setzt Treibhausgase frei.",
     "Torf entsteht, wenn Pflanzenreste unter nassen, sauerstoffarmen Bedingungen langsamer abgebaut als aufgebaut werden. Sinkt der Wasserstand, gelangt Sauerstoff in den Torfkörper; Torf mineralisiert und setzt vor allem CO₂ sowie weitere klimawirksame Gase frei. Höhere Wasserstände können den Torfabbau bremsen. Die Karte berechnet jedoch keine Treibhausgasminderung, sondern zeigt die räumliche Ausgangskulisse, in der Minderung durch Wasserstandsmanagement und angepasste Nutzung fachlich geprüft werden kann."),
    ("In Baden-Württemberg wird Moorschutz zur konkreten Frage: Welche Betriebe sind betroffen, welche Nutzungen bleiben möglich, welche Produkte tragen und welche Förderinstrumente sind nötig?",
     "In Baden-Württemberg wird Moorschutz zur konkreten Planungsfrage: Welche Nutzungskontexte sind berührt, welche betrieblichen Fragen entstehen, welche Produkte können tragfähig werden und welche Förderinstrumente wären nötig?"),
    ("### Betriebliche Betroffenheit", "### Betriebliche Fragen"),
    ("SOLAMO-BW untersucht regionale Betriebsmuster und die praktische Tragfähigkeit von Nutzungskonzepten auf wiedervernässten Moorflächen.",
     "SOLAMO-BW untersucht regionale Betriebsperspektiven und die praktische Tragfähigkeit von Nutzungskonzepten auf wiedervernässten landwirtschaftlichen Moorflächen."),
    ("nässeverträgliche Kulturen, robuste Weidesysteme und stoffliche oder energetische Nutzung benötigen tragfähige Märkte.",
     "Nässeverträgliche Kulturen, robuste Weidesysteme sowie stoffliche oder energetische Nutzung benötigen tragfähige Märkte."),
    ("~19.900 ha landwirtschaftliche Nutzung im Moor-/Feuchtbodenkontext ~82 % Grünland ~16 % Ackerland ohne Stilllegung und unklare Zuordnung ~2 % Stilllegung oder unklare Zuordnung separat geführt",
     "~19.900 ha landwirtschaftliche Nutzung im Moor-/Feuchtbodenkontext ~82 % Grünland ~16 % Ackerland ~2 % Stilllegung / unklare FIONA-Zuweisung"),
    ("Lesart: Diese Werte geben räumliche Orientierung. Sie sind keine Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.",
     "Lesart: Die Werte geben räumliche Orientierung. Sie sind keine Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse. Ackerland ist ohne separat geführte Stilllegung und unklare Zuordnungen dargestellt."),
    ("Welche Nutzung nasse Flächen tragen könnten",
     "Welche Nutzungen bei hohen Wasserständen tragfähig werden können"),
    ("Die Pfade werden erst tragfähig, wenn für Biomasse, Pflege, Energie oder Flächenorganisation verlässliche Abnahme und Erlöse entstehen. Die Matrix zeigt keine Empfehlung pro Standort, sondern typische Kombinationen aus Nutzung, Nutzung / Produkt und Engpass.",
     "Die Prüfpfade werden erst tragfähig, wenn für Biomasse, Pflege, Energie oder Flächenorganisation verlässliche Abnahme und Erlöse entstehen. Die Matrix zeigt keine Empfehlung pro Standort, sondern typische Kombinationen aus Nutzungskontext, Produktlogik und Engpass."),
    ("potenziell planbare Cashflows, aber hohe Qualitätsanforderungen",
     "mögliche Erlöse, aber hohe Prüf- und Qualitätsanforderungen"),
    ("Grundlage: kuratierte Literatur- und Projektauswertung zu Paludikultur, Nassgrünland, Nassweide, Sphagnum, Moor-PV und SOLAMO-BW-Wertschöpfungsketten; diese Matrix ist eine Orientierung, keine Standortempfehlung.",
     "Grundlage: kuratierte Literatur- und Projektauswertung zu Paludikultur, Nassgrünland, Nassweide, Sphagnum, Moor-PV und SOLAMO-BW-Wertschöpfungsketten. Die Matrix ist eine Orientierung für Prüfpfade, keine Standortempfehlung."),
    ("Thuenen", "Thünen"),
    ("Baden-Wuerttemberg", "Baden-Württemberg"),
    ("GLOBAL_FRAME_V1", "eigene kartografische Aufbereitung"),
    ("same ArcGIS frame", "einheitlicher Kartenrahmen"),
]

RISK_PATTERNS = [
    "This guided view",
    "Start with country-level emissions",
    "Then reveal the actual peat/organic-soil context",
    "Zoom to Europe",
    "Translate the hotspot view to Germany",
    "End at Baden-Württemberg",
    "Keep the boundary visible",
    "Suitability would require",
    "Each map layer answers a different question",
    "The map below is the core narrative",
    "The rest of the page is an evidence explorer",
    "Evidence explorer",
    "Prototype appendix",
    "How to read this prototype",
    "Current prototype datasets",
    "Loading country hotspot map",
    "Loading Baden-Württemberg BK50-Moor layer",
    "Click an evidence node",
    "South Germany fit",
    "asking which pathways",
    "source swap",
    "oberschwaben_lgl",
    "Datenquelle in Umstellung",
    "B98c",
    "Flächen-QA",
    "Klassifikations-QA",
    "betriebliche Betroffenheit",
    "Welche Betriebe sind betroffen",
    "potenziell planbare Cashflows",
]

REQUIRED_PATTERNS = [
    "Moorschutz braucht räumliche Orientierung",
    "Moorbodenkontext braucht konkrete Planung",
    "Die Karte berechnet jedoch keine Treibhausgasminderung",
    "Oberschwaben als Ausgangspunkt",
    "Oberschwaben, wo Moorschutz auf Landwirtschaft trifft",
    "~19.900 ha",
    "~82 % Grünland",
    "~16 % Ackerland",
    "~2 % Stilllegung / unklare FIONA-Zuweisung",
    "FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024",
    "keine Eignungskarte",
    "keine Priorisierung",
    "keine betriebliche Betroffenheitsanalyse",
    "Welche Nutzungen bei hohen Wasserständen tragfähig werden können",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_visible(raw: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_tag_start(raw: str, pos: int, tag: str = "section") -> int:
    matches = list(re.finditer(f"<{tag}\\b", raw[:pos], flags=re.IGNORECASE))
    return matches[-1].start() if matches else -1


def find_matching_tag_end(raw: str, start: int, tag: str = "section") -> int:
    token_re = re.compile(fr"</?{tag}\b[^>]*>", flags=re.IGNORECASE)
    depth = 0
    for m in token_re.finditer(raw, start):
        token = m.group(0)
        if token.startswith("</"):
            depth -= 1
            if depth == 0:
                return m.end()
        else:
            if not token.rstrip().endswith("/>"):
                depth += 1
    return -1


def remove_section_containing(raw: str, marker: str) -> tuple[str, bool, str]:
    pos = raw.find(marker)
    if pos < 0:
        return raw, False, "marker_not_found"
    start = find_tag_start(raw, pos, "section")
    if start < 0:
        return raw, False, "section_start_not_found"
    end = find_matching_tag_end(raw, start, "section")
    if end < 0:
        return raw, False, "section_end_not_found"
    return raw[:start] + "\n\n" + raw[end:], True, f"removed_section_{start}_{end}"


def remove_range_by_section_boundaries(raw: str, start_marker: str, end_marker: str) -> tuple[str, bool, str]:
    s_pos = raw.find(start_marker)
    e_pos = raw.find(end_marker)
    if s_pos < 0:
        return raw, False, "start_marker_not_found"
    if e_pos < 0:
        return raw, False, "end_marker_not_found"
    if e_pos <= s_pos:
        return raw, False, "end_marker_before_start_marker"

    start = find_tag_start(raw, s_pos, "section")
    if start < 0:
        start = s_pos

    end_section_start = find_tag_start(raw, e_pos, "section")
    if end_section_start < 0 or end_section_start <= start:
        end = e_pos
    else:
        end = end_section_start

    return raw[:start] + "\n\n" + raw[end:], True, f"removed_range_{start}_{end}"


def harden(raw: str) -> tuple[str, list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    out = raw

    for name, start_marker, end_marker in RANGE_REMOVALS:
        before_len = len(out)
        out, changed, note = remove_range_by_section_boundaries(out, start_marker, end_marker)
        rows.append({
            "type": "range_removal",
            "pattern": f"{start_marker} -> {end_marker}",
            "replacement": "",
            "count_before": str(before_len),
            "count_after": str(len(out)),
            "status": note if changed else f"not_changed:{note}",
        })

    for marker in SECTION_MARKERS_TO_REMOVE:
        removed = 0
        last_note = "not_attempted"
        for _ in range(5):
            out2, changed, note = remove_section_containing(out, marker)
            last_note = note
            if not changed:
                break
            out = out2
            removed += 1
        rows.append({
            "type": "section_removal",
            "pattern": marker,
            "replacement": "",
            "count_before": str(removed),
            "count_after": "0",
            "status": "removed" if removed else f"not_found_or_not_section:{last_note}",
        })

    for old, new in REPLACEMENTS:
        before = out.count(old)
        if before:
            out = out.replace(old, new)
        rows.append({
            "type": "replacement",
            "pattern": old,
            "replacement": new,
            "count_before": str(before),
            "count_after": str(out.count(old)),
            "status": "changed" if before else "not_found",
        })

    return out, rows


def add_audit_rows(raw: str, rows: list[dict[str, str]]) -> dict[str, int]:
    visible = strip_visible(raw)
    risk_remaining = 0
    missing_required = 0

    for p in RISK_PATTERNS:
        c = visible.count(p)
        risk_remaining += 1 if c else 0
        rows.append({
            "type": "risk_visible",
            "pattern": p,
            "replacement": "",
            "count_before": str(c),
            "count_after": str(c),
            "status": "REVIEW" if c else "OK",
        })

    for p in REQUIRED_PATTERNS:
        c = visible.count(p)
        missing_required += 1 if c == 0 else 0
        rows.append({
            "type": "required_visible",
            "pattern": p,
            "replacement": "",
            "count_before": str(c),
            "count_after": str(c),
            "status": "OK" if c else "MISSING",
        })

    english_watch_terms = ["This ", "The ", "where ", "which ", "Loading ", "prototype", "explorer", "dataset", "evidence", "actionable"]
    english_watch = sum(visible.count(t) for t in english_watch_terms)

    return {
        "risk_remaining": risk_remaining,
        "missing_required": missing_required,
        "english_watch": english_watch,
    }


def write_findings(rows: list[dict[str, str]]) -> None:
    fields = ["type", "pattern", "replacement", "count_before", "count_after", "status"]
    with FINDINGS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B116 - Public page hardening"
    if marker in current:
        return
    entry = f"""
## B116 - Public page hardening ({TODAY})

- Removed old English prototype/explorer sections from the public page when matching markers were present.
- Strengthened the GHG mechanism and Oberschwaben planning rationale.
- De-risked wording around farm affectedness, suitability, priority, GHG mitigation and Moor-PV cashflow.
- Simplified the Oberschwaben area-balance labels.
- Did not modify CSS, map images or data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def write_report(rows: list[dict[str, str]], summary: dict[str, int], changed_index: bool) -> None:
    status = "OK" if summary["risk_remaining"] == 0 and summary["missing_required"] == 0 else "REVIEW REQUIRED"
    changed_repl = [r for r in rows if r["type"] == "replacement" and r["status"] == "changed"]
    risk_rows = [r for r in rows if r["type"] == "risk_visible" and r["status"] == "REVIEW"]
    missing_rows = [r for r in rows if r["type"] == "required_visible" and r["status"] == "MISSING"]

    report = [
        "# B116 - Public Page Hardening",
        "",
        f"Date: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Summary",
        "",
        f"- index.html changed: {'YES' if changed_index else 'NO'}",
        f"- targeted replacements applied: {len(changed_repl)}",
        f"- risk/prototype visible patterns remaining: {summary['risk_remaining']}",
        f"- required public patterns missing: {summary['missing_required']}",
        f"- English/prototype watch count: {summary['english_watch']}",
        "",
        "## Applied replacements",
        "",
        "| Before | After |",
        "|---|---|",
    ]
    if changed_repl:
        for r in changed_repl:
            report.append(f"| `{r['pattern'].replace('|','\\|')}` | `{r['replacement'].replace('|','\\|')}` |")
    else:
        report.append("| none | none |")

    report.extend(["", "## Risk findings", ""])
    if risk_rows:
        report.append("| Pattern | Count |")
        report.append("|---|---:|")
        for r in risk_rows:
            report.append(f"| `{r['pattern']}` | {r['count_after']} |")
    else:
        report.append("No visible risk/prototype patterns remain.")

    report.extend(["", "## Missing required findings", ""])
    if missing_rows:
        report.append("| Pattern | Count |")
        report.append("|---|---:|")
        for r in missing_rows:
            report.append(f"| `{r['pattern']}` | {r['count_after']} |")
    else:
        report.append("No required public patterns are missing.")

    report.extend([
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B116_public_page_hardening_audit.txt",
        "Import-Csv docs\\B116_public_text_findings.csv -Delimiter ';' | Where-Object {$_.status -in @('REVIEW','MISSING')} | Format-Table -Auto",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "```",
        "",
    ])
    write_text(REPORT, "\n".join(report))


def write_audit(summary: dict[str, int], rows: list[dict[str, str]]) -> None:
    status = "OK" if summary["risk_remaining"] == 0 and summary["missing_required"] == 0 else "REVIEW REQUIRED"
    lines = [
        "# B116 public page hardening audit",
        "",
        f"- Status: {status}",
        f"- Risk/prototype visible patterns remaining: {summary['risk_remaining']}",
        f"- Required public patterns missing: {summary['missing_required']}",
        f"- English/prototype watch count: {summary['english_watch']}",
        "",
        "## REVIEW / MISSING rows",
        "",
    ]
    flagged = [r for r in rows if r["status"] in {"REVIEW", "MISSING"}]
    if flagged:
        lines.append("| Type | Pattern | Count |")
        lines.append("|---|---|---:|")
        for r in flagged:
            lines.append(f"| {r['type']} | `{r['pattern']}` | {r['count_after']} |")
    else:
        lines.append("No REVIEW or MISSING rows.")

    lines.extend([
        "",
        "## Next checks",
        "",
        "```powershell",
        "Select-String -Path index.html -Pattern \"This guided view\",\"Evidence explorer\",\"Prototype appendix\",\"Loading country\",\"B98c\",\"Flächen-QA\",\"betriebliche Betroffenheit\",\"FIONA 2024\",\"~19.900\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ])
    write_text(AUDIT, "\n".join(lines))


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    original = read_text(INDEX)
    backup = BACKUP_DIR / "index_before_b116.html"
    if not backup.exists():
        shutil.copy2(INDEX, backup)

    hardened, rows = harden(original)
    changed_index = hardened != original
    if changed_index:
        write_text(INDEX, hardened)

    summary = add_audit_rows(hardened, rows)
    write_findings(rows)
    write_report(rows, summary, changed_index)
    write_audit(summary, rows)
    update_done()

    print("B116 public page hardening complete.")
    print("Changed/created:")
    for p in [INDEX, REPORT, AUDIT, FINDINGS, DONE]:
        if p.exists():
            print(f"  {rel(p)}")
    print(f"  {rel(backup)}")
    print("")
    print(f"Status: {'OK' if summary['risk_remaining'] == 0 and summary['missing_required'] == 0 else 'REVIEW REQUIRED'}")
    print(f"Risk/prototype visible patterns remaining: {summary['risk_remaining']}")
    print(f"Required public patterns missing: {summary['missing_required']}")
    print(f"English/prototype watch count: {summary['english_watch']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B116_public_page_hardening_audit.txt")
    print("  Import-Csv docs\\B116_public_text_findings.csv -Delimiter ';' | Where-Object {$_.status -in @('REVIEW','MISSING')} | Format-Table -Auto")


if __name__ == "__main__":
    main()
