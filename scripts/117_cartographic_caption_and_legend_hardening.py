#!/usr/bin/env python3
"""
B117 - Cartographic caption and legend hardening

Purpose
-------
Harden the public page's cartographic language and create a precise legend
rework specification for the next map-export pass.

B117 deliberately separates two issues:

1) Safe immediate HTML fixes:
   - remove/replace technical map-caption leftovers;
   - fix Thuenen -> Thünen;
   - reduce English/GIS-internal phrasing in captions;
   - prevent total-vs-density wording conflicts where exact text is known;
   - audit the live public HTML for cartographic risk terms.

2) Legend/color hardening specification:
   - define a clearer, color-blind-safer Oberschwaben legend palette;
   - document that final color changes should be applied together with map PNG
     re-export, not only to HTML legend dots, to avoid legend-map mismatch.

Changed:
- index.html
- docs/B117_cartographic_caption_and_legend_hardening.md
- docs/B117_cartographic_caption_audit.txt
- docs/B117_cartographic_text_findings.csv
- docs/B117_oberschwaben_legend_color_spec.md
- tasks/done.md

Not changed:
- src/styles.css
- public/maps/*
- data/*
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
BACKUP_DIR = ROOT / "_backup_before_b117_cartographic_hardening"

REPORT = DOCS / "B117_cartographic_caption_and_legend_hardening.md"
AUDIT = DOCS / "B117_cartographic_caption_audit.txt"
FINDINGS = DOCS / "B117_cartographic_text_findings.csv"
LEGEND_SPEC = DOCS / "B117_oberschwaben_legend_color_spec.md"

TODAY = date.today().isoformat()

# Exact immediate replacements. These are safe because they target public-facing
# caption/wording problems, not data or cartography.
REPLACEMENTS = [
    ("Thuenen", "Thünen"),
    ("Thuenen Kulisse", "Thünen-Kulisse"),
    ("Thünen Kulisse", "Thünen-Kulisse"),
    ("organic-soils Kulisse", "Kulisse organischer Böden"),
    ("organic-soils target area", "Kulisse organischer Böden"),
    ("Federal-state context", "Bund-Länder-Kontext"),
    ("Peatland context · Peat in soil mosaic", "Moor-/Feuchtbodenkontext · räumliche Einordnung"),
    ("BK50 peat / wetland soil context · Regional frame", "BK50 Moor-/Feuchtbodenkontext · regionale Einordnung"),
    ("BK50 BW layer: peat and wetland soil context shown as a single extent layer; no land-use or suitability classification is implied.",
     "BK50 Baden-Württemberg: Moor- und Feuchtbodenkontext als räumliche Einordnung; keine Landnutzungs- oder Eignungsklassifikation."),
    ("BW frame: regional context exported from the same 16:9 ArcGIS map frame.",
     "Baden-Württemberg: regionale Einordnung im einheitlichen Kartenrahmen."),
    ("GPM context underneath – same ArcGIS frame.",
     "Globaler Moorbodenkontext im einheitlichen Kartenrahmen."),
    ("GPM context underneath - same ArcGIS frame.",
     "Globaler Moorbodenkontext im einheitlichen Kartenrahmen."),
    ("exported from eigene kartografische Aufbereitung.",
     "eigene kartografische Aufbereitung."),
    ("exported from GLOBAL_FRAME_V1.",
     "eigene kartografische Aufbereitung."),
    ("GLOBAL_FRAME_V1", "eigene kartografische Aufbereitung"),
    ("same ArcGIS frame", "einheitlicher Kartenrahmen"),
    ("ArcGIS map frame", "Kartenrahmen"),
    ("rendered as a one-colour extent layer", "als einfarbige räumliche Kulisse dargestellt"),
    ("national peat and organic-soils target area", "nationale Kulisse organischer Böden"),
    ("emissions_total_kt_co2e", "Gesamtemissionen in kt CO₂e"),
    ("TOTAL EMISSIONS", "GESAMTEMISSIONEN"),
    ("Higher total emissions", "Höhere Gesamtemissionen"),
    ("Dichtekarten zeigen, wo Belastung räumlich besonders konzentriert ist.",
     "Hotspotkarten zeigen, wo Belastung räumlich besonders deutlich wird."),
    ("Größe und Intensität unterscheiden sich.", "Gesamtmenge und räumliche Konzentration müssen getrennt gelesen werden."),
    ("Baden-Württemberg wird konkret", "Baden-Württemberg ordnet den regionalen Kontext ein"),
    ("macht die Frage räumlich konkret", "führt zur regionalen Planungsfrage"),
]

# Terms that should not remain in public captions/text for an official review.
RISK_TERMS = [
    "Thuenen",
    "GLOBAL_FRAME_V1",
    "ArcGIS",
    "exported from",
    "rendered as",
    "same ArcGIS frame",
    "one-colour extent layer",
    "target area rendered",
    "emissions_total_kt_co2e",
    "TOTAL EMISSIONS",
    "Higher total emissions",
    "Federal-state context",
    "organic-soils target area",
    "BK50 peat / wetland soil context",
    "BW frame:",
    "GPM context underneath",
    "Dichtekarten zeigen",
    "leere Umrisslinie",
    "oberschwaben_lgl",
    "Datenquelle in Umstellung",
    "B98c",
    "Flächen-QA",
]

REQUIRED_TERMS = [
    "Thünen",
    "FIONA 2024",
    "BK50 Moor-/Feuchtbodenkontext",
    "GISCO NUTS 2024",
    "~19.900 ha",
    "keine Eignungskarte",
    "keine Priorisierung",
    "keine betriebliche Betroffenheitsanalyse",
]

LEGEND_LABELS = [
    "Ackerland",
    "Grünland",
    "Dauerkultur",
    "Moor-/Feuchtbodenkontext",
    "Schnittmenge",
]

LEGEND_PALETTE = [
    {
        "class": "Ackerland",
        "hex": "#C76E3F",
        "role": "warmer Braun-Orange-Ton für ackerbauliche Nutzung",
        "note": "klar von Grünland und Moor-/Feuchtbodenkontext getrennt",
    },
    {
        "class": "Grünland",
        "hex": "#5F8F4A",
        "role": "mittleres Grün für Grünland",
        "note": "nicht zu hell; muss gegenüber Moor-Blau unterscheidbar bleiben",
    },
    {
        "class": "Dauerkultur / Sondernutzung",
        "hex": "#8C5A9E",
        "role": "gedämpftes Violett für Sonder-/Dauerkultur",
        "note": "bewusst nicht grün/rosa, um kleine Klassen sichtbar zu halten",
    },
    {
        "class": "Moor-/Feuchtbodenkontext",
        "hex": "#4E7FA6",
        "role": "Blau für Wasser-/Feuchtbodenkontext",
        "note": "semantisch mit Wasserstand/Feuchte gekoppelt",
    },
    {
        "class": "Schnittmenge",
        "hex": "#043B36",
        "role": "dunkles Petrol als Kernaussage",
        "note": "höchster Kontrast; sollte in Karte und Legende dominant sein",
    },
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
    text = re.sub(r"\s+", " ", text).strip()
    return text


def apply_replacements(raw: str) -> tuple[str, list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    out = raw

    for old, new in REPLACEMENTS:
        before = out.count(old)
        if before:
            out = out.replace(old, new)
        rows.append({
            "type": "replacement",
            "term": old,
            "replacement": new,
            "count_before": str(before),
            "count_after": str(out.count(old)),
            "status": "changed" if before else "not_found",
        })

    return out, rows


def add_audit_rows(raw: str, rows: list[dict[str, str]]) -> dict[str, int]:
    text = visible_text(raw)

    risk_count = 0
    missing_required = 0
    missing_legend_labels = 0

    for term in RISK_TERMS:
        c = text.count(term)
        if c:
            risk_count += 1
        rows.append({
            "type": "risk_term_visible",
            "term": term,
            "replacement": "",
            "count_before": str(c),
            "count_after": str(c),
            "status": "REVIEW" if c else "OK",
        })

    for term in REQUIRED_TERMS:
        c = text.count(term)
        if not c:
            missing_required += 1
        rows.append({
            "type": "required_term_visible",
            "term": term,
            "replacement": "",
            "count_before": str(c),
            "count_after": str(c),
            "status": "OK" if c else "MISSING",
        })

    for label in LEGEND_LABELS:
        c = text.count(label)
        if not c:
            missing_legend_labels += 1
        rows.append({
            "type": "legend_label_visible",
            "term": label,
            "replacement": "",
            "count_before": str(c),
            "count_after": str(c),
            "status": "OK" if c else "MISSING",
        })

    # English caption watch: deliberately limited to obvious caption/prototype words.
    english_caption_watch_terms = [
        "layer:",
        "frame:",
        "context ·",
        "Regional frame",
        "Federal-state",
        "target area",
        "underneath",
        "rendered",
        "exported",
    ]
    english_watch = 0
    for term in english_caption_watch_terms:
        english_watch += text.count(term)

    return {
        "risk_count": risk_count,
        "missing_required": missing_required,
        "missing_legend_labels": missing_legend_labels,
        "english_watch": english_watch,
    }


def write_findings(rows: list[dict[str, str]]) -> None:
    fields = ["type", "term", "replacement", "count_before", "count_after", "status"]
    with FINDINGS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_legend_spec() -> None:
    lines = [
        "# B117 – Oberschwaben Legend Colour Specification",
        "",
        f"Stand: {TODAY}",
        "",
        "## Zweck",
        "",
        "Die aktuelle Oberschwaben-Legende ist fachlich richtig, aber die Klassen sind visuell zu ähnlich. "
        "B117 definiert deshalb eine klarere Zielpalette für den nächsten Kartenexport.",
        "",
        "Wichtig: Die Farbänderung sollte **nicht nur in der HTML-Legende** erfolgen. Karte und Legende müssen zusammen angepasst werden, sonst entsteht ein Legenden-Karten-Mismatch.",
        "",
        "## Zielpalette",
        "",
        "| Klasse | Hex | Rolle | Hinweis |",
        "|---|---|---|---|",
    ]

    for item in LEGEND_PALETTE:
        lines.append(f"| {item['class']} | `{item['hex']}` | {item['role']} | {item['note']} |")

    lines.extend([
        "",
        "## Kartografische Regeln",
        "",
        "1. Die Schnittmenge bleibt die visuell stärkste Klasse.",
        "2. Moor-/Feuchtbodenkontext darf nicht mit Grünland verwechselt werden.",
        "3. Ackerland und Dauerkultur müssen auch bei kleinen Flächen unterscheidbar bleiben.",
        "4. Die Legende muss in Graustufen und bei Rot-Grün-Sehschwäche lesbar bleiben.",
        "5. Quellen- und Caveat-Zeile bleiben unterhalb der Flächenbilanz, nicht als technische Karten-Caption.",
        "",
        "## Prüfauftrag B117b",
        "",
        "- Public PNGs aus der Oberschwaben-Karte mit Zielpalette neu exportieren.",
        "- HTML-Legende und Kartenfarben abgleichen.",
        "- Screenshot bei 1440 px und 1280 px prüfen.",
        "- Danach B58 erneut laufen lassen.",
        "",
    ])
    write_text(LEGEND_SPEC, "\n".join(lines))


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B117 - Cartographic caption and legend hardening"
    if marker in current:
        return
    entry = f"""
## B117 - Cartographic caption and legend hardening ({TODAY})

- Replaced public-facing technical map-caption remnants where exact text matches were found.
- Fixed Thuenen/Thünen and several English/GIS-internal caption phrases.
- Audited cartographic risk terms, required source terms and Oberschwaben legend labels.
- Created a colour specification for the next Oberschwaben map/legend export.
- Did not modify CSS, map images or data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def write_report(summary: dict[str, int], rows: list[dict[str, str]], changed_index: bool) -> None:
    changed_repl = [r for r in rows if r["type"] == "replacement" and r["status"] == "changed"]
    flagged = [r for r in rows if r["status"] in {"REVIEW", "MISSING"}]
    status = "OK" if summary["risk_count"] == 0 and summary["missing_required"] == 0 and summary["missing_legend_labels"] == 0 else "REVIEW REQUIRED"

    lines = [
        "# B117 – Cartographic Caption and Legend Hardening",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Scope",
        "",
        "B117 cleans public-facing cartographic captions and creates the colour specification for an Oberschwaben legend/map re-export.",
        "",
        "No CSS, map PNG or data files were modified.",
        "",
        "## Summary",
        "",
        f"- index.html changed: {'YES' if changed_index else 'NO'}",
        f"- caption/text replacements applied: {len(changed_repl)}",
        f"- risk terms remaining: {summary['risk_count']}",
        f"- required source/caveat terms missing: {summary['missing_required']}",
        f"- Oberschwaben legend labels missing: {summary['missing_legend_labels']}",
        f"- English/caption watch count: {summary['english_watch']}",
        "",
        "## Applied replacements",
        "",
        "| Before | After |",
        "|---|---|",
    ]

    if changed_repl:
        for r in changed_repl:
            lines.append(f"| `{r['term'].replace('|', '\\|')}` | `{r['replacement'].replace('|', '\\|')}` |")
    else:
        lines.append("| none | none |")

    lines.extend([
        "",
        "## Flagged findings",
        "",
    ])
    if flagged:
        lines.append("| Type | Term | Count |")
        lines.append("|---|---|---:|")
        for r in flagged:
            lines.append(f"| {r['type']} | `{r['term']}` | {r['count_after']} |")
    else:
        lines.append("No REVIEW or MISSING findings.")

    lines.extend([
        "",
        "## Important",
        "",
        "The legend colour issue is not fully solved until the Oberschwaben map PNGs and the HTML legend are adjusted together. "
        "See `docs/B117_oberschwaben_legend_color_spec.md`.",
        "",
    ])
    write_text(REPORT, "\n".join(lines))


def write_audit(summary: dict[str, int], rows: list[dict[str, str]]) -> None:
    status = "OK" if summary["risk_count"] == 0 and summary["missing_required"] == 0 and summary["missing_legend_labels"] == 0 else "REVIEW REQUIRED"
    lines = [
        "# B117 cartographic caption audit",
        "",
        f"- Status: {status}",
        f"- Risk terms remaining: {summary['risk_count']}",
        f"- Required terms missing: {summary['missing_required']}",
        f"- Legend labels missing: {summary['missing_legend_labels']}",
        f"- English/caption watch count: {summary['english_watch']}",
        "",
        "## REVIEW / MISSING rows",
        "",
    ]

    flagged = [r for r in rows if r["status"] in {"REVIEW", "MISSING"}]
    if flagged:
        lines.append("| Type | Term | Count |")
        lines.append("|---|---|---:|")
        for r in flagged:
            lines.append(f"| {r['type']} | `{r['term']}` | {r['count_after']} |")
    else:
        lines.append("No REVIEW or MISSING rows.")

    lines.extend([
        "",
        "## Recommended checks",
        "",
        "```powershell",
        "Select-String -Path index.html -Pattern \"Thuenen\",\"ArcGIS\",\"GLOBAL_FRAME_V1\",\"rendered as\",\"emissions_total_kt_co2e\",\"TOTAL EMISSIONS\",\"Dichtekarten\",\"FIONA 2024\",\"~19.900\"",
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

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    original = read_text(INDEX)
    backup = BACKUP_DIR / "index_before_b117.html"
    if not backup.exists():
        shutil.copy2(INDEX, backup)

    hardened, rows = apply_replacements(original)
    changed_index = hardened != original
    if changed_index:
        write_text(INDEX, hardened)

    summary = add_audit_rows(hardened, rows)
    write_findings(rows)
    write_legend_spec()
    write_report(summary, rows, changed_index)
    write_audit(summary, rows)
    update_done()

    print("B117 cartographic caption and legend hardening complete.")
    print("Changed/created:")
    for p in [INDEX, REPORT, AUDIT, FINDINGS, LEGEND_SPEC, DONE]:
        if p.exists():
            print(f"  {rel(p)}")
    print(f"  {rel(backup)}")
    print("")
    print(f"Status: {'OK' if summary['risk_count'] == 0 and summary['missing_required'] == 0 and summary['missing_legend_labels'] == 0 else 'REVIEW REQUIRED'}")
    print(f"Risk terms remaining: {summary['risk_count']}")
    print(f"Required terms missing: {summary['missing_required']}")
    print(f"Legend labels missing: {summary['missing_legend_labels']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B117_cartographic_caption_audit.txt")
    print("  Get-Content docs\\B117_oberschwaben_legend_color_spec.md")
    print("  Import-Csv docs\\B117_cartographic_text_findings.csv -Delimiter ';' | Where-Object {$_.status -in @('REVIEW','MISSING')} | Format-Table -Auto")


if __name__ == "__main__":
    main()
