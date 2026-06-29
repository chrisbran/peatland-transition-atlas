#!/usr/bin/env python3
# B125c - Compact source, method and rights accordion
#
# Purpose:
# Consolidate B125/B125b into one professional, compact and fully collapsible
# source/method/rights block. Remove duplicated method-note wording.
#
# Changed:
# - index.html
# - src/styles.css
# - docs/B125c_compact_source_method_rights.md
# - docs/B125c_compact_source_method_rights_audit.txt
# - tasks/done.md

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
BACKUP_DIR = ROOT / "_backup_before_b125c_compact_source_method_rights"

REPORT = DOCS / "B125c_compact_source_method_rights.md"
AUDIT = DOCS / "B125c_compact_source_method_rights_audit.txt"
TODAY = date.today().isoformat()

B125_START = "<!-- B125_SOURCE_AND_METHOD_REGISTER -->"
B125_END = "<!-- /B125_SOURCE_AND_METHOD_REGISTER -->"
B125B_START = "<!-- B125B_DATA_RIGHTS_REGISTER -->"
B125B_END = "<!-- /B125B_DATA_RIGHTS_REGISTER -->"
CSS_MARKER = "/* B125c compact source method rights */"

DUPLICATE_METHOD_NOTE_PATTERNS = [
    r"\s*<p>\s*Methodischer Hinweis:\s*Die Einordnung basiert auf kuratierter Literatur- und Projektauswertung\.\s*Die Bewertungen sind qualitativ;\s*Evidenzpunkte sind ungefähre visuelle Anker\.\s*Weitere räumliche Auswertungen werden nur nach gesonderter Datenprüfung ergänzt\.\s*</p>\s*",
    r"\s*Methodischer Hinweis:\s*Die Einordnung basiert auf kuratierter Literatur- und Projektauswertung\.\s*Die Bewertungen sind qualitativ;\s*Evidenzpunkte sind ungefähre visuelle Anker\.\s*Weitere räumliche Auswertungen werden nur nach gesonderter Datenprüfung ergänzt\.\s*",
]

NEW_BLOCK = """
<!-- B125_SOURCE_AND_METHOD_REGISTER -->
<section id="quellen-methodik" class="b125-source-register b125-source-register--compact" aria-labelledby="b125SourceTitle">
  <details class="b125-master-disclosure">
    <summary>
      <span class="b125-kicker">Quellen, Methodik und Nutzungsrechte</span>
      <span id="b125SourceTitle" class="b125-summary-title">Datenbasis, fachliche Grundlagen und Rechtehinweise</span>
      <span class="b125-summary-note">kompakt öffnen</span>
    </summary>

    <div class="b125-compact-body">
      <p class="b125-lead">
        Die Seite ist eine räumliche Orientierung. Sie kombiniert öffentliche und projektbezogene Datengrundlagen mit
        eigener Auswahl, Klassifikation, Verschneidung und kartografischer Aufbereitung. Maßgeblich bleiben die
        Originalbedingungen der jeweiligen Datenbereitsteller.
      </p>

      <div class="b125-compact-grid">
        <article class="b125-compact-card">
          <h3>Fachliche Grundlagen</h3>
          <ul>
            <li><a href="https://www.ipcc-nggip.iges.or.jp/public/wetlands/" rel="noopener">IPCC Wetlands Supplement</a> – methodischer Referenzrahmen für Treibhausgasinventare zu Feuchtgebieten und drainierten organischen Böden.</li>
            <li><a href="https://www.umweltbundesamt.de/daten/umweltzustand-trends/klima/treibhausgas-emissionen-in-deutschland/emissionen-der-landnutzung-aenderung" rel="noopener">Umweltbundesamt</a>, <a href="https://www.bundesumweltministerium.de/themen/naturschutz/moorschutz" rel="noopener">BMUV</a> und <a href="https://www.lubw.baden-wuerttemberg.de/natur-und-landschaft/moorschutz" rel="noopener">LUBW</a> – Einordnung von Mooren, organischen Böden, Wiedervernässung und Klimawirkung.</li>
            <li><a href="https://mlr.baden-wuerttemberg.de/de/unsere-themen/landwirtschaft/landwirtschaft-im-klimawandel/klimaschutzsystem/wald-boden-und-holz-der-lulucf-sektor/moore" rel="noopener">MLR Baden-Württemberg</a>, <a href="https://lazbw.landwirtschaft-bw.de/%2CLde/Startseite/Themen/Moorbodenbewirtschaftung" rel="noopener">LAZBW</a>, <a href="https://ltz.landwirtschaft-bw.de/%2CLen/Arbeitsfelder/Moorbodenschutz" rel="noopener">LTZ Augustenberg</a>, <a href="https://www.moorwissen.de/paludi-progress.html" rel="noopener">Moorwissen / Paludi-PROGRESS</a> und <a href="https://430a.uni-hohenheim.de/solamo-bw" rel="noopener">SOLAMO-BW</a> – Nutzungspfade, Paludikultur, Nassgrünland und Wertschöpfung.</li>
          </ul>
        </article>

        <article class="b125-compact-card">
          <h3>Methodische Lesart</h3>
          <p>
            Die Karten zeigen Bodenkontexte und räumliche Überschneidungen. Flächenwerte für Oberschwaben beruhen auf
            eigener Auswahl, Klassifikation und Verschneidung von FIONA, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS;
            Werte sind gerundet.
          </p>
          <p>
            Die Darstellung ist keine Eignungskarte, keine Priorisierung, keine hydrologische Modellierung und keine
            betriebliche Betroffenheitsanalyse. Standortentscheidungen erfordern zusätzliche Prüfung von Wasserstand,
            Hydrologie, Eigentums- und Bewirtschaftungsstruktur, Schutzstatus, Förderung, Technik und Wertschöpfungsketten.
          </p>
        </article>
      </div>

      <div class="b125-rights-compact" aria-label="Nutzungsrechte der Datengrundlagen">
        <h3>Datengrundlagen, Rechte und Quellenvermerke</h3>
        <table>
          <thead>
            <tr>
              <th>Datengrundlage</th>
              <th>Rechte / Lizenz</th>
              <th>Quellenvermerk im Projekt</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><a href="https://www.greifswaldmoor.de/global-peatland-database-en.html" rel="noopener">Global Peatland Map 2.0 / Global Peatland Database</a></td>
              <td>Öffentlich bereitgestellt; Originalbedingungen der Datenbereitsteller beachten.</td>
              <td>Global Peatland Map 2.0 / Greifswald Mire Centre / Global Peatlands Initiative; eigene kartografische Aufbereitung.</td>
            </tr>
            <tr>
              <td><a href="https://www.fao.org/faostat/" rel="noopener">FAOSTAT</a></td>
              <td>FAO Statistical Database Terms of Use; CC BY 4.0; kein FAO-Endorsement.</td>
              <td>FAO. FAOSTAT. Emissionen aus drainierten organischen Böden; eigene Klassifikation und kartografische Aufbereitung. Lizenz: CC BY 4.0.</td>
            </tr>
            <tr>
              <td><a href="https://atlas.thuenen.de/maps/243/metadata_detail" rel="noopener">Thünen-Kulisse organischer Böden</a></td>
              <td>Creative Commons Attribution 4.0 International (CC BY 4.0).</td>
              <td>Thünen-Institut / Wittnebel, Frank &amp; Tiemeyer: Aktualisierte Kulisse organischer Böden in Deutschland; eigene kartografische Aufbereitung.</td>
            </tr>
            <tr>
              <td><a href="https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units/territorial-units-statistics" rel="noopener">Eurostat GISCO NUTS</a></td>
              <td>Eurostat/GISCO-Bedingungen; bei Verwaltungsgrenzen: © EuroGeographics.</td>
              <td>Eurostat GISCO NUTS; © EuroGeographics bezüglich der Verwaltungsgrenzen; eigene Auswahl und kartografische Aufbereitung.</td>
            </tr>
            <tr>
              <td><a href="https://fiona.landbw.de/" rel="noopener">FIONA Baden-Württemberg</a></td>
              <td>Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0).</td>
              <td>MLR Baden-Württemberg / FIONA 2024; eigene Klassifikation und Verschneidung.</td>
            </tr>
            <tr>
              <td><a href="https://www.lgrb-bw.de/geologischer-dienst/boden/bodenkundliche-landesaufnahme" rel="noopener">LGRB / BK50 Baden-Württemberg</a></td>
              <td>Datenproduktspezifische LGRB-Bedingungen; offene GeoLa-/BK50-Themen nach dl-de/by-2-0.</td>
              <td>Datenquelle: Regierungspräsidium Freiburg – LGRB, www.lgrb-bw.de; BK50 Moor-/Feuchtbodenkontext; eigene Aufbereitung.</td>
            </tr>
            <tr>
              <td>LGL Baden-Württemberg, soweit verwendet</td>
              <td>Offene Geobasisdaten nach dl-de/by-2-0.</td>
              <td>Datenquelle: LGL, www.lgl-bw.de, dl-de/by-2-0; eigene kartografische Aufbereitung.</td>
            </tr>
            <tr>
              <td>Eigene Auswertungen und Kartenexporte</td>
              <td>Eigene Auswahl, Klassifikation, Verschneidung und Darstellung; keine Weiterlizenzierung der Ausgangsdaten.</td>
              <td>Eigene Berechnung und kartografische Aufbereitung auf Basis der genannten Datengrundlagen.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </details>
</section>
<!-- /B125_SOURCE_AND_METHOD_REGISTER -->
"""

CSS_BLOCK = """
/* B125c compact source method rights */
.b125-source-register--compact {
  width: min(980px, calc(100% - 2rem));
  margin: clamp(3.5rem, 7vw, 6rem) auto clamp(2.5rem, 5vw, 4rem);
  padding: 0;
  border: 0;
  background: transparent;
  box-shadow: none;
}
.b125-master-disclosure {
  border: 1px solid rgba(31, 42, 34, .16);
  border-radius: 1.2rem;
  background: rgba(255, 253, 246, .94);
  box-shadow: 0 18px 54px rgba(31, 38, 33, .08);
  overflow: hidden;
}
.b125-master-disclosure > summary {
  list-style: none;
  cursor: pointer;
  display: grid;
  gap: .28rem;
  padding: clamp(1rem, 2.4vw, 1.45rem) clamp(1rem, 2.7vw, 1.65rem);
}
.b125-master-disclosure > summary::-webkit-details-marker {
  display: none;
}
.b125-master-disclosure > summary::before {
  content: "▸";
  justify-self: start;
  color: #657c38;
  font-weight: 900;
  transform: translateY(.1rem);
}
.b125-master-disclosure[open] > summary::before {
  content: "▾";
}
.b125-source-register--compact .b125-kicker {
  margin: 0;
  color: #657c38;
  font-size: .74rem;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
}
.b125-summary-title {
  display: block;
  max-width: 760px;
  color: #252019;
  font-size: clamp(1.25rem, 2.4vw, 1.8rem);
  font-weight: 820;
  line-height: 1.12;
}
.b125-summary-note {
  color: rgba(31, 42, 34, .58);
  font-size: .9rem;
}
.b125-compact-body {
  padding: 0 clamp(1rem, 2.7vw, 1.65rem) clamp(1rem, 2.8vw, 1.65rem);
}
.b125-source-register--compact .b125-lead {
  max-width: 860px;
  margin: 0 0 1rem;
  line-height: 1.5;
  color: rgba(31, 42, 34, .82);
}
.b125-compact-grid {
  display: grid;
  grid-template-columns: 1.05fr .95fr;
  gap: .85rem;
  margin-bottom: .9rem;
}
.b125-compact-card,
.b125-rights-compact {
  border: 1px solid rgba(31, 42, 34, .13);
  border-radius: .9rem;
  background: rgba(255, 250, 240, .78);
  padding: .95rem 1rem;
}
.b125-compact-card h3,
.b125-rights-compact h3 {
  margin: 0 0 .55rem;
  font-size: .98rem;
  line-height: 1.22;
}
.b125-compact-card p {
  margin: .5rem 0 0;
  line-height: 1.48;
}
.b125-compact-card ul {
  margin: .4rem 0 0;
  padding-left: 1.05rem;
}
.b125-compact-card li {
  margin: .45rem 0;
  line-height: 1.4;
}
.b125-source-register--compact a {
  color: inherit;
  text-decoration-color: rgba(101, 124, 56, .55);
  text-underline-offset: .18em;
}
.b125-rights-compact {
  margin-top: .9rem;
  overflow-x: auto;
}
.b125-rights-compact table {
  width: 100%;
  border-collapse: collapse;
  font-size: .86rem;
  line-height: 1.33;
}
.b125-rights-compact th,
.b125-rights-compact td {
  vertical-align: top;
  text-align: left;
  padding: .62rem .55rem;
  border-top: 1px solid rgba(31, 42, 34, .12);
}
.b125-rights-compact th {
  color: #314127;
  font-weight: 780;
  background: rgba(101, 124, 56, .08);
}
.b125-rights-compact td:first-child {
  width: 22%;
  font-weight: 720;
}
@media (max-width: 900px) {
  .b125-compact-grid {
    grid-template-columns: 1fr;
  }
  .b125-rights-compact table {
    min-width: 760px;
  }
}
"""

REQUIRED = [
    "Quellen, Methodik und Nutzungsrechte",
    "Datenbasis, fachliche Grundlagen und Rechtehinweise",
    "Fachliche Grundlagen",
    "Methodische Lesart",
    "Datengrundlagen, Rechte und Quellenvermerke",
    "IPCC Wetlands Supplement",
    "FAOSTAT",
    "CC BY 4.0",
    "Thünen-Kulisse organischer Böden",
    "Eurostat GISCO NUTS",
    "© EuroGeographics",
    "FIONA Baden-Württemberg",
    "Datenlizenz Deutschland – Namensnennung – Version 2.0",
    "Regierungspräsidium Freiburg – LGRB",
    "Datenquelle: LGL, www.lgl-bw.de, dl-de/by-2-0",
    "keine Eignungskarte",
    "keine Priorisierung",
    "keine hydrologische Modellierung",
    "keine betriebliche Betroffenheitsanalyse",
    "keine Weiterlizenzierung der Ausgangsdaten",
]

RISK = [
    "Nutzungsrechte und Datenlizenzen",  # old standalone block title should be gone
    "Klimawirkung und Moorbodenschutz",  # old three-box heading should be gone
    "Kartengrundlagen",  # old three-box heading should be gone
    "Methodischer Hinweis:",  # duplicate old sentence should be gone
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


def remove_old_source_block(raw: str) -> str:
    raw = re.sub(
        r"\n?<!-- B125_SOURCE_AND_METHOD_REGISTER -->.*?<!-- /B125_SOURCE_AND_METHOD_REGISTER -->\n?",
        "\n",
        raw,
        flags=re.DOTALL,
    )
    raw = re.sub(
        r"\n?<!-- B125B_DATA_RIGHTS_REGISTER -->.*?<!-- /B125B_DATA_RIGHTS_REGISTER -->\n?",
        "\n",
        raw,
        flags=re.DOTALL,
    )
    raw = re.sub(
        r"\n?<!-- B122_SOURCE_AND_METHOD_REGISTER -->.*?<!-- /B122_SOURCE_AND_METHOD_REGISTER -->\n?",
        "\n",
        raw,
        flags=re.DOTALL,
    )
    return raw


def remove_duplicate_method_note(raw: str) -> tuple[str, int]:
    total = 0
    for pattern in DUPLICATE_METHOD_NOTE_PATTERNS:
        raw, n = re.subn(pattern, "\n", raw, flags=re.IGNORECASE | re.DOTALL)
        total += n
    return raw, total


def insert_new_block(raw: str) -> tuple[str, str, int]:
    raw = remove_old_source_block(raw)
    raw, removed_notes = remove_duplicate_method_note(raw)

    pos = raw.rfind("</main>")
    if pos >= 0:
        return raw[:pos] + "\n\n" + NEW_BLOCK.strip() + "\n\n" + raw[pos:], "inserted_before_main_close", removed_notes

    pos = raw.rfind("</body>")
    if pos >= 0:
        return raw[:pos] + "\n\n" + NEW_BLOCK.strip() + "\n\n" + raw[pos:], "inserted_before_body_close", removed_notes

    return raw.rstrip() + "\n\n" + NEW_BLOCK.strip() + "\n", "appended_at_end", removed_notes


def patch_css(css: str) -> tuple[str, str]:
    for marker in [
        "/* B125 source and method register */",
        "/* B125b data rights and attribution */",
        "/* B125c compact source method rights */",
    ]:
        css = re.sub(
            r"\n?" + re.escape(marker) + r".*?(?=\n/\* |\Z)",
            "\n",
            css,
            flags=re.DOTALL,
        )
    return css.rstrip() + "\n\n" + CSS_BLOCK.strip() + "\n", "inserted_or_replaced"


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B125c - Compact source method rights"
    if marker in current:
        return
    entry = f"""
## B125c - Compact source method rights ({TODAY})

- Consolidated B125 and B125b into one fully collapsible source, method and rights block.
- Replaced separate long source and rights sections with a compact professional disclosure.
- Moved method notes into the same disclosure and removed duplicate method-note wording.
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
        "source_section_count": html.count(B125_START),
        "old_rights_section_count": html.count(B125B_START),
        "css_marker_count": css.count(CSS_MARKER),
        "outer_details_count": html.count('class="b125-master-disclosure"'),
        "open_attribute_count": html.count('<details class="b125-master-disclosure" open'),
    }


def write_docs(result: dict[str, object], insert_status: str, css_status: str, removed_notes: int) -> None:
    ok = (
        result["missing_required"] == 0
        and result["risk_findings"] == 0
        and result["source_section_count"] == 1
        and result["old_rights_section_count"] == 0
        and result["css_marker_count"] == 1
        and result["outer_details_count"] == 1
        and result["open_attribute_count"] == 0
    )
    status = "OK" if ok else "REVIEW REQUIRED"

    report = [
        "# B125c – Compact Source, Method and Rights",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B125c fasst Quellen, Methodik und Nutzungsrechte in einen gemeinsamen, vollständig einklappbaren Abschnitt zusammen.",
        "",
        "## Änderungen",
        "",
        f"- Register: `{insert_status}`",
        f"- CSS: `{css_status}`",
        f"- Removed duplicate method-note fragments: {removed_notes}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['risk_findings']}",
        f"- Source section count: {result['source_section_count']}",
        f"- Old rights section count: {result['old_rights_section_count']}",
        f"- CSS marker count: {result['css_marker_count']}",
        f"- Outer details count: {result['outer_details_count']}",
        f"- Open attribute count: {result['open_attribute_count']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B125c_compact_source_method_rights_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html -Pattern \"Quellen, Methodik und Nutzungsrechte\",\"Datengrundlagen, Rechte und Quellenvermerke\",\"Nutzungsrechte und Datenlizenzen\",\"Methodischer Hinweis:\",\"CC BY 4.0\",\"Datenlizenz Deutschland\",\"EuroGeographics\",\"Regierungspräsidium Freiburg\",\"Thuenen\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ]
    write_text(REPORT, "\n".join(report))

    audit_lines = [
        "# B125c compact source method rights audit",
        "",
        f"- Status: {status}",
        f"- Removed duplicate method-note fragments: {removed_notes}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['risk_findings']}",
        f"- Source section count: {result['source_section_count']}",
        f"- Old rights section count: {result['old_rights_section_count']}",
        f"- CSS marker count: {result['css_marker_count']}",
        f"- Outer details count: {result['outer_details_count']}",
        f"- Open attribute count: {result['open_attribute_count']}",
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

    html, insert_status, removed_notes = insert_new_block(html)
    css, css_status = patch_css(css)

    write_text(INDEX, html)
    write_text(CSS, css)
    update_done()

    result = audit(html, css)
    write_docs(result, insert_status, css_status, removed_notes)

    ok = (
        result["missing_required"] == 0
        and result["risk_findings"] == 0
        and result["source_section_count"] == 1
        and result["old_rights_section_count"] == 0
        and result["css_marker_count"] == 1
        and result["outer_details_count"] == 1
        and result["open_attribute_count"] == 0
    )

    print("B125c compact source/method/rights register complete.")
    print("Changed/created:")
    for p in [INDEX, CSS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"Missing required entries: {result['missing_required']}")
    print(f"Visible risk findings: {result['risk_findings']}")
    print(f"Removed duplicate method-note fragments: {removed_notes}")
    print(f"Open attribute count: {result['open_attribute_count']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B125c_compact_source_method_rights_audit.txt -Encoding UTF8")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  python -m http.server 8000")


if __name__ == "__main__":
    main()
