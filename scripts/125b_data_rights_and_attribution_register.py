#!/usr/bin/env python3
# B125b - Data rights and attribution register
#
# Adds explicit rights/licence and attribution notes for the datasets used in
# the public atlas. This is documentation only: no map, data or scrolly changes.

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
BACKUP_DIR = ROOT / "_backup_before_b125b_data_rights_register"

REPORT = DOCS / "B125b_data_rights_and_attribution_register.md"
AUDIT = DOCS / "B125b_data_rights_and_attribution_audit.txt"
TODAY = date.today().isoformat()

MARKER_START = "<!-- B125B_DATA_RIGHTS_REGISTER -->"
MARKER_END = "<!-- /B125B_DATA_RIGHTS_REGISTER -->"
CSS_MARKER = "/* B125b data rights and attribution */"

RIGHTS_BLOCK = """
<!-- B125B_DATA_RIGHTS_REGISTER -->
<details open class="b125-rights">
  <summary>Nutzungsrechte und Datenlizenzen</summary>
  <p>
    Die folgende Übersicht dokumentiert die Rechte- und Quellenhinweise der in diesem Projekt verwendeten Datengrundlagen.
    Maßgeblich bleiben immer die verlinkten Originalbedingungen der jeweiligen Datenbereitsteller.
    Eigene Karten, Klassifikationen und Verschneidungen ändern die Nutzungsbedingungen der Ausgangsdaten nicht.
  </p>
  <div class="b125-rights-table" role="region" aria-label="Nutzungsrechte der Datengrundlagen">
    <table>
      <thead>
        <tr>
          <th>Datengrundlage</th>
          <th>Rechte / Lizenzhinweis</th>
          <th>Quellenvermerk in diesem Projekt</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Global Peatland Map 2.0 / Global Peatland Database</td>
          <td>Öffentlich bereitgestellte und frei herunterladbare globale Moorbodenkarte; die Projektseite verweist auf die Global Peatland Database und ihre Quelldaten. Für eine Weitergabe der Rohdaten sind die Originalbedingungen der Datenbereitsteller zu prüfen.</td>
          <td>Global Peatland Map 2.0 / Greifswald Mire Centre / Global Peatlands Initiative; eigene kartografische Aufbereitung.</td>
        </tr>
        <tr>
          <td>FAOSTAT</td>
          <td>FAO Statistical Database Terms of Use; Lizenz: CC BY 4.0. FAO verlangt Quellenangabe, Abrufdatum und Lizenzhinweis und untersagt eine Darstellung als FAO-Endorsement.</td>
          <td>FAO. FAOSTAT. Abgerufen für Emissionen aus drainierten organischen Böden; eigene Klassifikation und kartografische Aufbereitung. Lizenz: CC BY 4.0.</td>
        </tr>
        <tr>
          <td>Thünen-Kulisse organischer Böden</td>
          <td>Thünen-Atlas-Metadaten: Creative Commons Attribution 4.0 International (CC BY 4.0). Die Metadaten nennen als Attribution Wittnebel, Mareille / Frank, Stefan / Tiemeyer, Bärbel: Aktualisierte Kulisse organischer Böden in Deutschland.</td>
          <td>Thünen-Institut / Wittnebel, Frank &amp; Tiemeyer: Aktualisierte Kulisse organischer Böden in Deutschland; eigene kartografische Aufbereitung. Lizenz: CC BY 4.0.</td>
        </tr>
        <tr>
          <td>Eurostat GISCO NUTS / administrative Grenzen</td>
          <td>Eurostat/GISCO-Geodaten dürfen unter den dort genannten Bedingungen genutzt werden; für NUTS/administrative Grenzen ist die Quellenangabe und der Copyright-Hinweis zu EuroGeographics erforderlich. Für kommerzielle Nutzung gelten gesonderte EuroGeographics-Hinweise.</td>
          <td>Eurostat GISCO NUTS; © EuroGeographics bezüglich der Verwaltungsgrenzen; eigene Auswahl und kartografische Aufbereitung.</td>
        </tr>
        <tr>
          <td>FIONA Baden-Württemberg</td>
          <td>Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0). Nach Metadaten sind Datenhaltende Stelle und Jahr des Datenbezugs zu nennen.</td>
          <td>Datengrundlage: MLR Baden-Württemberg / FIONA 2024, Datenlizenz Deutschland – Namensnennung – Version 2.0; eigene Klassifikation und Verschneidung.</td>
        </tr>
        <tr>
          <td>LGRB / BK50 Baden-Württemberg</td>
          <td>Für LGRB-BK50-/GeoLa-Daten sind die jeweiligen LGRB-Produkt- und Metadatenbedingungen maßgeblich. LGRB-Metadaten nennen für offene GeoLa-/BK50-Themen die Datenlizenz Deutschland – Namensnennung – Version 2.0 mit Quellenvermerk „Regierungspräsidium Freiburg – LGRB, www.lgrb-bw.de“.</td>
          <td>Datenquelle: Regierungspräsidium Freiburg – LGRB, www.lgrb-bw.de; BK50 Moor-/Feuchtbodenkontext; eigene Auswahl, Klassifikation und kartografische Aufbereitung.</td>
        </tr>
        <tr>
          <td>LGL Baden-Württemberg / Geobasisdaten, soweit verwendet</td>
          <td>Offene Geobasisdaten und Geodatendienste der Vermessungsverwaltung Baden-Württemberg: Datenlizenz Deutschland – Namensnennung – Version 2.0; geforderter Quellenvermerk: „Datenquelle: LGL, www.lgl-bw.de, dl-de/by-2-0“.</td>
          <td>Datenquelle: LGL, www.lgl-bw.de, dl-de/by-2-0; eigene kartografische Aufbereitung.</td>
        </tr>
        <tr>
          <td>Eigene Auswertungen und Kartenexporte</td>
          <td>Eigene Auswahl, Klassifikation, Verschneidung, Generalisierung und kartografische Darstellung; keine Weiterlizenzierung der Ausgangsdaten. Die Rechte der Ausgangsdaten bleiben unberührt.</td>
          <td>Eigene Berechnung und kartografische Aufbereitung auf Basis der oben genannten Datengrundlagen.</td>
        </tr>
      </tbody>
    </table>
  </div>
</details>
<!-- /B125B_DATA_RIGHTS_REGISTER -->
"""

CSS_BLOCK = """
/* B125b data rights and attribution */
.b125-rights {
  margin: 1.2rem 0 0;
  padding: 1rem 1rem .95rem;
  border: 1px solid rgba(31, 42, 34, .14);
  border-radius: 1rem;
  background: rgba(255, 250, 240, .78);
}
.b125-rights summary {
  cursor: pointer;
  font-weight: 780;
}
.b125-rights p {
  max-width: 940px;
  margin: .75rem 0 .95rem;
  line-height: 1.52;
  color: rgba(31, 42, 34, .82);
}
.b125-rights-table {
  overflow-x: auto;
}
.b125-rights-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: .9rem;
  line-height: 1.38;
}
.b125-rights-table th,
.b125-rights-table td {
  vertical-align: top;
  text-align: left;
  padding: .72rem .65rem;
  border-top: 1px solid rgba(31, 42, 34, .12);
}
.b125-rights-table th {
  color: #314127;
  font-weight: 760;
  background: rgba(101, 124, 56, .08);
}
.b125-rights-table td:first-child {
  width: 23%;
  font-weight: 700;
}
@media (max-width: 900px) {
  .b125-rights-table table {
    min-width: 780px;
  }
}
"""

REQUIRED = [
    "Nutzungsrechte und Datenlizenzen",
    "Global Peatland Map 2.0 / Global Peatland Database",
    "frei herunterladbare globale Moorbodenkarte",
    "FAO Statistical Database Terms of Use",
    "CC BY 4.0",
    "Thünen-Atlas-Metadaten",
    "Eurostat GISCO NUTS",
    "© EuroGeographics bezüglich der Verwaltungsgrenzen",
    "FIONA Baden-Württemberg",
    "Datenlizenz Deutschland – Namensnennung – Version 2.0",
    "MLR Baden-Württemberg / FIONA 2024",
    "Regierungspräsidium Freiburg – LGRB",
    "Datenquelle: LGL, www.lgl-bw.de, dl-de/by-2-0",
    "Eigene Auswertungen und Kartenexporte",
    "keine Weiterlizenzierung der Ausgangsdaten",
]

RISK = [
    "GLOBAL_FRAME_V1",
    "EUROPE_FRAME_V1",
    "Country hotspot layer:",
    "Thuenen",
    "ArcGIS",
    "Peatland context",
    "TOTAL EMISSIONS",
    "Ã",
    "�",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def backup(path: Path) -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    dest = BACKUP_DIR / rel(path).replace("/", "__").replace("\\", "__")
    if path.exists() and not dest.exists():
        shutil.copy2(path, dest)


def visible_text(raw: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def remove_existing(raw: str) -> str:
    return re.sub(
        r"\n?<!-- B125B_DATA_RIGHTS_REGISTER -->.*?<!-- /B125B_DATA_RIGHTS_REGISTER -->\n?",
        "\n",
        raw,
        flags=re.DOTALL,
    )


def insert_rights(raw: str) -> tuple[str, str]:
    raw = remove_existing(raw)

    # Preferred location: after the B125 source grid and before method box.
    pattern = r'(</div>\s*<div class="b125-method-box">)'
    match = re.search(pattern, raw)
    if match:
        replacement = "</div>\n\n" + RIGHTS_BLOCK.strip() + "\n\n<div class=\"b125-method-box\">"
        return raw[:match.start()] + replacement + raw[match.end():], "inserted_before_method_box"

    # Fallback: inside the source register before its closing section.
    pos = raw.find("</section>", raw.find('class="b125-source-register"'))
    if pos >= 0:
        return raw[:pos] + "\n\n" + RIGHTS_BLOCK.strip() + "\n" + raw[pos:], "inserted_before_source_section_close"

    return raw.rstrip() + "\n\n" + RIGHTS_BLOCK.strip() + "\n", "appended_at_end"


def patch_css(css: str) -> tuple[str, str]:
    css = re.sub(
        r"\n?/\* B125b data rights and attribution \*/.*?(?=\n/\* |\Z)",
        "\n",
        css,
        flags=re.DOTALL,
    )
    return css.rstrip() + "\n\n" + CSS_BLOCK.strip() + "\n", "inserted_or_replaced"


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B125b - Data rights and attribution register"
    if marker in current:
        return
    entry = f"""
## B125b - Data rights and attribution register ({TODAY})

- Added explicit rights, licence and attribution notes for project data sources.
- Covered GPM 2.0, FAOSTAT, Thünen, GISCO, FIONA, LGRB/BK50, LGL and own derived outputs.
- Clarified that own map exports do not relicense the underlying datasets.
- Did not modify maps, data or scrolly logic.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def audit(html: str, css: str) -> dict[str, object]:
    vis = visible_text(html)
    required_counts = {p: vis.count(p) for p in REQUIRED}
    risk_counts = {p: vis.count(p) for p in RISK}
    return {
        "required_counts": required_counts,
        "risk_counts": risk_counts,
        "missing_required": sum(1 for v in required_counts.values() if v == 0),
        "risk_findings": sum(1 for v in risk_counts.values() if v > 0),
        "rights_section_count": html.count(MARKER_START),
        "css_marker_count": css.count(CSS_MARKER),
    }


def write_docs(result: dict[str, object], insert_status: str, css_status: str) -> None:
    ok = (
        result["missing_required"] == 0
        and result["risk_findings"] == 0
        and result["rights_section_count"] == 1
        and result["css_marker_count"] == 1
    )
    status = "OK" if ok else "REVIEW REQUIRED"

    report = [
        "# B125b – Data Rights and Attribution Register",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B125b ergänzt B125 um genaue Rechte-, Lizenz- und Quellenhinweise zu den verwendeten Datengrundlagen.",
        "",
        "## Änderungen",
        "",
        f"- Rechteblock: `{insert_status}`",
        f"- CSS: `{css_status}`",
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['risk_findings']}",
        f"- Rights section count: {result['rights_section_count']}",
        f"- CSS marker count: {result['css_marker_count']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B125b_data_rights_and_attribution_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html -Pattern \"Nutzungsrechte und Datenlizenzen\",\"CC BY 4.0\",\"Datenlizenz Deutschland\",\"EuroGeographics\",\"Regierungspräsidium Freiburg\",\"keine Weiterlizenzierung\",\"GLOBAL_FRAME_V1\",\"Thuenen\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ]
    write_text(REPORT, "\n".join(report))

    audit_lines = [
        "# B125b data rights and attribution audit",
        "",
        f"- Status: {status}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['risk_findings']}",
        f"- Rights section count: {result['rights_section_count']}",
        f"- CSS marker count: {result['css_marker_count']}",
        "",
        "## Required patterns",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ]
    for p, c in result["required_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Risk patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["risk_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    write_text(AUDIT, "\n".join(audit_lines))


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)
    if not CSS.exists():
        print(f"Missing {rel(CSS)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    backup(INDEX)
    backup(CSS)

    html = read_text(INDEX)
    css = read_text(CSS)

    html, insert_status = insert_rights(html)
    css, css_status = patch_css(css)

    write_text(INDEX, html)
    write_text(CSS, css)
    update_done()

    result = audit(html, css)
    write_docs(result, insert_status, css_status)

    ok = (
        result["missing_required"] == 0
        and result["risk_findings"] == 0
        and result["rights_section_count"] == 1
        and result["css_marker_count"] == 1
    )

    print("B125b data rights and attribution register complete.")
    print("Changed/created:")
    for p in [INDEX, CSS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"Missing required entries: {result['missing_required']}")
    print(f"Visible risk findings: {result['risk_findings']}")
    print(f"Rights section count: {result['rights_section_count']}")
    print(f"CSS marker count: {result['css_marker_count']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B125b_data_rights_and_attribution_audit.txt -Encoding UTF8")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  python -m http.server 8000")


if __name__ == "__main__":
    main()
