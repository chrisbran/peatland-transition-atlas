#!/usr/bin/env python3
"""
B121 - Raster caption and final wording cleanup

Purpose
-------
Final pre-publication cleanup after B120:
- remove/translate remaining HTML-visible English/internal map-caption remnants;
- harmonize final wording in "Moore verstehen", transformation matrix and final method note;
- create a raster-caption review page for map PNGs because text embedded inside PNGs
  cannot be found by Select-String/B103b;
- audit visible text for prototype, English, encoding and overclaiming risks.

Important
---------
This script does NOT modify PNG files. It deliberately separates:
1) HTML wording cleanup that can be done safely in code; and
2) raster-caption review that must be checked visually or fixed by re-exporting maps.

Changed:
- index.html
- docs/B121_raster_caption_and_final_wording_cleanup.md
- docs/B121_final_wording_audit.txt
- docs/B121_raster_caption_review.html
- docs/B121_raster_caption_review.csv
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
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b121_raster_caption_cleanup"

REPORT = DOCS / "B121_raster_caption_and_final_wording_cleanup.md"
AUDIT = DOCS / "B121_final_wording_audit.txt"
RASTER_REVIEW_HTML = DOCS / "B121_raster_caption_review.html"
RASTER_REVIEW_CSV = DOCS / "B121_raster_caption_review.csv"

TODAY = date.today().isoformat()

REPLACEMENTS = [
    # HTML-visible map/caption remnants
    ("Peatland context · Peat in soil mosaic", "Moorkontext · Torf im Bodenmosaik"),
    ("Peatland context · peat in soil mosaic", "Moorkontext · Torf im Bodenmosaik"),
    ("Global Peatland Map 2.0 context · exported from GLOBAL_FRAME_V1", "Datenbasis: Global Peatland Map 2.0; eigene kartografische Aufbereitung."),
    ("Global Peatland Map 2.0 context · eigene kartografische Aufbereitung", "Datenbasis: Global Peatland Map 2.0; eigene kartografische Aufbereitung."),
    ("Global Peatland Map 2.0 context", "Global Peatland Map 2.0: Moorkontext"),
    ("exported from GLOBAL_FRAME_V1", "eigene kartografische Aufbereitung"),
    ("GLOBAL_FRAME_V1", "eigene kartografische Aufbereitung"),
    ("same ArcGIS frame", "einheitlicher Kartenrahmen"),
    ("ArcGIS frame", "Kartenrahmen"),
    ("ArcGIS map frame", "Kartenrahmen"),
    ("rendered as a one-colour extent layer", "als räumliche Kulisse dargestellt"),
    ("Thuenen Kulisse", "Thünen-Kulisse"),
    ("Thuenen", "Thünen"),

    # Final wording cleanup
    (
        "Solange Torf nass bleibt, speichert er Kohlenstoff; wird er entwässert, wird er zur dauerhaften Emissionsquelle.",
        "Solange Torf nass bleibt, kann Kohlenstoff im Torf erhalten bleiben. Wird der Boden entwässert, gelangt Sauerstoff in den Torfkörper; Torf wird abgebaut und es entstehen Treibhausgasemissionen.",
    ),
    (
        "Torf mineralisiert und setzt Treibhausgase frei.",
        "Torf mineralisiert; dabei entstehen vor allem CO₂ sowie weitere klimawirksame Gase.",
    ),
    (
        "Die Matrix zeigt keine Empfehlung pro Standort, sondern typische Kombinationen aus Nutzung, Nutzung / Produkt und Engpass.",
        "Die Matrix zeigt keine Empfehlung pro Standort, sondern typische Kombinationen aus Nutzungskontext, Produktlogik, Entwicklungsstand und Engpass.",
    ),
    (
        "typische Kombinationen aus Nutzung, Nutzung / Produkt und Engpass",
        "typische Kombinationen aus Nutzungskontext, Produktlogik, Entwicklungsstand und Engpass",
    ),
    (
        "Arbeitsstand auf Basis kuratierter Literaturcodierung",
        "Methodischer Hinweis: Die Einordnung basiert auf kuratierter Literatur- und Projektauswertung",
    ),
    (
        "Arbeitsstand auf Basis kuratierter Literatur- und Projektauswertung",
        "Methodischer Hinweis: Die Einordnung basiert auf kuratierter Literatur- und Projektauswertung",
    ),
    (
        "Die Bewertungen sind qualitativ und ersetzen keine Standortprüfung.",
        "Die Bewertungen sind qualitativ und ersetzen keine Standortprüfung.",
    ),
    (
        "Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen.",
        "Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen. Werte gerundet.",
    ),
]

# Risk patterns in visible HTML text. Rasterized text inside PNGs is handled via visual review HTML.
RISK_PATTERNS = [
    "This guided view",
    "Evidence explorer",
    "Prototype appendix",
    "Current prototype datasets",
    "Loading country hotspot map",
    "Click an evidence node",
    "Suitability would require",
    "Layer logic",
    "The map below is the core narrative",
    "The rest of the page is an evidence explorer",
    "Scrollytelling structure",
    "Six-part story",
    "Peatland context · Peat in soil mosaic",
    "exported from GLOBAL_FRAME_V1",
    "GLOBAL_FRAME_V1",
    "same ArcGIS frame",
    "ArcGIS frame",
    "rendered as a one-colour extent layer",
    "Thuenen",
    "source swap",
    "oberschwaben_lgl",
    "B98c",
    "Flächen-QA",
    "Klassifikations-QA",
    "Datenquelle in Umstellung",
    "berechnetes Treibhausgasminderungspotenzial",
    "THG-Minderungspotenzial der gezeigten Flächen",
    "Eignung für Wiedervernässung",
    "priorisierte Flächen",
    "müssen wiedervernässt werden",
    "Diese Flächen sollen wiedervernässt werden",
    "Welche Betriebe sind betroffen",
    "Ã",
    "�",
]

REQUIRED_PATTERNS = [
    "Moorschutz braucht räumliche Orientierung",
    "Warum Wasserstand über Klimawirkung entscheidet",
    "Diese Seite berechnet deshalb keine Treibhausgasminderung",
    "Warum Oberschwaben?",
    "Oberschwaben ist für Baden-Württemberg ein zentraler Fokusraum",
    "~19.900 ha",
    "~82 % Grünland",
    "~16 % Ackerland",
    "~2 % Stilllegung / unklare FIONA-Zuweisung",
    "Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen. Werte gerundet.",
    "FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024",
    "keine Eignungskarte",
    "keine Priorisierung",
    "keine betriebliche Betroffenheitsanalyse",
    "Welche Prüfpfade folgen aus unterschiedlichen Nutzungskontexten?",
    "typische Kombinationen aus Nutzungskontext, Produktlogik, Entwicklungsstand und Engpass",
]

RASTER_RISK_KEYWORDS = [
    "GLOBAL_FRAME_V1",
    "exported from",
    "ArcGIS",
    "same ArcGIS frame",
    "Peatland context",
    "Peat in soil mosaic",
    "Thuenen",
    "rendered as",
    "one-colour extent layer",
    "TOTAL EMISSIONS",
    "emissions_total_kt_co2e",
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


def apply_replacements(raw: str) -> tuple[str, list[dict[str, str]]]:
    out = raw
    rows: list[dict[str, str]] = []
    for old, new in REPLACEMENTS:
        n = out.count(old)
        if n:
            out = out.replace(old, new)
        rows.append({
            "pattern": old,
            "replacement": new,
            "count": str(n),
            "status": "changed" if n else "not_found",
        })
    return out, rows


def extract_image_sources(raw: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    img_re = re.compile(r"<img\b(?P<attrs>[^>]+)>", flags=re.IGNORECASE | re.DOTALL)
    attr_re = re.compile(r"(?P<name>[a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*['\"](?P<value>.*?)['\"]", flags=re.DOTALL)

    for m in img_re.finditer(raw):
        attrs = {a.group("name").lower(): html_lib.unescape(a.group("value")) for a in attr_re.finditer(m.group("attrs"))}
        src = attrs.get("src", "")
        if not src:
            continue
        src_clean = unquote(src.split("?", 1)[0].split("#", 1)[0])
        path = (ROOT / src_clean).resolve() if not re.match(r"^https?://", src_clean) else None
        is_local = path is not None and str(path).startswith(str(ROOT.resolve()))
        exists = bool(is_local and path.exists())
        alt = attrs.get("alt", "")
        cls = attrs.get("class", "")
        rows.append({
            "src": src,
            "local_path": rel(path) if exists and path is not None else "",
            "exists": "YES" if exists else "NO",
            "alt": alt,
            "class": cls,
            "review_priority": review_priority(src, alt, cls),
            "review_instruction": "Check raster text inside the image: remove/replace GLOBAL_FRAME_V1, exported from, ArcGIS, English legend/caption terms.",
        })
    return rows


def review_priority(src: str, alt: str, cls: str) -> str:
    hay = " ".join([src, alt, cls]).lower()
    if any(k in hay for k in ["global", "gpm", "peatland", "world", "thuenen", "germany", "bw", "oberschwaben"]):
        return "HIGH"
    if any(k in hay for k in ["map", "karte", "moor", "soil", "boden"]):
        return "MEDIUM"
    return "LOW"


def write_raster_review(rows: list[dict[str, str]]) -> None:
    with RASTER_REVIEW_CSV.open("w", encoding="utf-8", newline="") as f:
        fields = ["review_priority", "src", "local_path", "exists", "alt", "class", "review_instruction"]
        writer = csv.DictWriter(f, delimiter=";", fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    high_rows = [r for r in rows if r["review_priority"] in {"HIGH", "MEDIUM"}]

    html_lines = [
        "<!doctype html>",
        '<html lang="de">',
        "<head>",
        '  <meta charset="utf-8">',
        "  <title>B121 Raster Caption Review</title>",
        "  <style>",
        "    body{font-family:system-ui,Segoe UI,Arial,sans-serif;background:#f6f1e7;color:#1f2a22;margin:2rem;}",
        "    h1{font-size:1.8rem} .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:1rem;}",
        "    figure{background:#fffaf0;border:1px solid #ddd0bc;border-radius:12px;padding:1rem;box-shadow:0 8px 24px rgba(0,0,0,.08)}",
        "    img{display:block;max-width:100%;height:auto;background:#10231f;border-radius:6px;}",
        "    figcaption{font-size:.88rem;line-height:1.45;margin-top:.75rem;}",
        "    code{background:#eee4d4;padding:.1rem .25rem;border-radius:.25rem;}",
        "    .prio{font-weight:700;color:#5d6f31}.warn{color:#8b3a2b;font-weight:700}",
        "  </style>",
        "</head>",
        "<body>",
        "  <h1>B121 Raster Caption Review</h1>",
        "  <p>Diese Seite prüft Kartenbilder visuell. HTML-Audits finden keine Texte, die direkt in PNGs eingebrannt sind.</p>",
        "  <p class='warn'>Bitte in jedem Bild nach folgenden Rastertexten suchen: GLOBAL_FRAME_V1, exported from, ArcGIS, Peatland context, Peat in soil mosaic, Thuenen, rendered as, TOTAL EMISSIONS.</p>",
        "  <div class='grid'>",
    ]

    for r in high_rows:
        src = html_lib.escape(r["src"])
        html_lines.extend([
            "    <figure>",
            f"      <img src='../{src}' alt=''>",
            "      <figcaption>",
            f"        <div class='prio'>Priority: {html_lib.escape(r['review_priority'])}</div>",
            f"        <div><strong>src:</strong> <code>{src}</code></div>",
            f"        <div><strong>alt:</strong> {html_lib.escape(r['alt'])}</div>",
            f"        <div><strong>Instruction:</strong> {html_lib.escape(r['review_instruction'])}</div>",
            "      </figcaption>",
            "    </figure>",
        ])

    html_lines.extend([
        "  </div>",
        "</body>",
        "</html>",
    ])
    write_text(RASTER_REVIEW_HTML, "\n".join(html_lines))


def audit(raw: str) -> dict[str, object]:
    vis = visible_text(raw)
    risk_counts = {p: vis.count(p) for p in RISK_PATTERNS}
    required_counts = {p: vis.count(p) for p in REQUIRED_PATTERNS}
    english_watch_patterns = ["structure", "story", "Loading", "Click", "prototype", "explorer", "layer:", "frame:"]
    english_watch_counts = {p: vis.count(p) for p in english_watch_patterns}
    return {
        "risk_counts": risk_counts,
        "required_counts": required_counts,
        "english_watch_counts": english_watch_counts,
        "risk_findings": sum(1 for v in risk_counts.values() if v > 0),
        "missing_required": sum(1 for v in required_counts.values() if v == 0),
        "english_watch": sum(english_watch_counts.values()),
    }


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B121 - Raster caption and final wording cleanup"
    if marker in current:
        return
    entry = f"""
## B121 - Raster caption and final wording cleanup ({TODAY})

- Cleaned remaining HTML-visible English/internal map-caption remnants.
- Harmonized final wording in Moore-verstehen, the transformation matrix and the final method note.
- Created a raster-caption review page because embedded PNG text cannot be found by HTML audits.
- Did not modify maps, map colours, CSS or data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def write_report(replacement_rows: list[dict[str, str]], image_rows: list[dict[str, str]], result: dict[str, object]) -> None:
    status = "OK" if result["risk_findings"] == 0 and result["missing_required"] == 0 else "REVIEW REQUIRED"
    changed_rows = [r for r in replacement_rows if r["status"] == "changed"]
    high_image_count = sum(1 for r in image_rows if r["review_priority"] == "HIGH")

    lines = [
        "# B121 – Raster Caption and Final Wording Cleanup",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Zweck",
        "",
        "B121 bereinigt letzte HTML-Wording-Reste und erzeugt eine visuelle Prüfliste für Texte, die direkt in PNG-Karten eingebrannt sein können.",
        "",
        "## Ergebnis",
        "",
        f"- HTML replacements applied: {len(changed_rows)}",
        f"- Map images listed for raster review: {len(image_rows)}",
        f"- High-priority raster checks: {high_image_count}",
        f"- Visible-text risk findings: {result['risk_findings']}",
        f"- Missing required findings: {result['missing_required']}",
        "",
        "## Applied replacements",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ]
    if changed_rows:
        for r in changed_rows:
            lines.append(f"| `{r['pattern'].replace('|', '\\|')}` | {r['count']} |")
    else:
        lines.append("| none | 0 |")

    lines.extend([
        "",
        "## Raster-caption review",
        "",
        f"Open `{rel(RASTER_REVIEW_HTML)}` locally and inspect all HIGH/MEDIUM map images visually.",
        "",
        "Terms that must not remain in raster images:",
        "",
    ])
    for term in RASTER_RISK_KEYWORDS:
        lines.append(f"- `{term}`")

    lines.extend([
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B121_final_wording_audit.txt -Encoding UTF8",
        "Start-Process docs\\B121_raster_caption_review.html",
        "Select-String -Encoding UTF8 -Path index.html -Pattern \"GLOBAL_FRAME_V1\",\"exported from\",\"Peatland context\",\"Nutzung / Produkt\",\"Arbeitsstand\",\"Methodischer Hinweis\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "```",
        "",
    ])
    write_text(REPORT, "\n".join(lines))

    risk_counts = result["risk_counts"]
    required_counts = result["required_counts"]
    english_watch_counts = result["english_watch_counts"]

    audit_lines = [
        "# B121 final wording audit",
        "",
        f"- Status: {status}",
        f"- Risk findings: {result['risk_findings']}",
        f"- Missing required findings: {result['missing_required']}",
        f"- English watch hits: {result['english_watch']}",
        "",
        "## Risk patterns",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ]
    for p, c in risk_counts.items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Required patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in required_counts.items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## English watch patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in english_watch_counts.items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend([
        "",
        "## Raster review reminder",
        "",
        "HTML audits cannot see text embedded in PNG files. Use `docs/B121_raster_caption_review.html`.",
        "",
    ])
    write_text(AUDIT, "\n".join(audit_lines))


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    backup = BACKUP_DIR / "index_before_b121.html"
    if not backup.exists():
        shutil.copy2(INDEX, backup)

    html = read_text(INDEX)
    html, replacement_rows = apply_replacements(html)
    write_text(INDEX, html)

    image_rows = extract_image_sources(html)
    write_raster_review(image_rows)

    update_done()
    result = audit(html)
    write_report(replacement_rows, image_rows, result)

    print("B121 raster caption and final wording cleanup complete.")
    print("Changed/created:")
    for p in [INDEX, REPORT, AUDIT, RASTER_REVIEW_HTML, RASTER_REVIEW_CSV, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(backup)}")
    print("")
    print(f"Status: {'OK' if result['risk_findings'] == 0 and result['missing_required'] == 0 else 'REVIEW REQUIRED'}")
    print(f"Risk findings: {result['risk_findings']}")
    print(f"Missing required findings: {result['missing_required']}")
    print(f"English watch hits: {result['english_watch']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B121_final_wording_audit.txt -Encoding UTF8")
    print("  Start-Process docs\\B121_raster_caption_review.html")
    print("  Select-String -Encoding UTF8 -Path index.html -Pattern \"GLOBAL_FRAME_V1\",\"exported from\",\"Peatland context\",\"Nutzung / Produkt\",\"Arbeitsstand\",\"Methodischer Hinweis\",\"Ã\",\"�\"")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
