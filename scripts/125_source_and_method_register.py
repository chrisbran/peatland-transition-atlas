#!/usr/bin/env python3
# B125 - Source and method register
#
# Purpose:
# Add a compact, publication-ready source and method register after the central
# scrolly rebuild. This is intentionally limited to attribution and method
# framing. It does not add sender/contact/institutional framing.

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
BACKUP_DIR = ROOT / "_backup_before_b125_source_and_method_register"

REPORT = DOCS / "B125_source_and_method_register.md"
AUDIT = DOCS / "B125_source_and_method_audit.txt"
TODAY = date.today().isoformat()

B125_MARKER_START = "<!-- B125_SOURCE_AND_METHOD_REGISTER -->"
B125_MARKER_END = "<!-- /B125_SOURCE_AND_METHOD_REGISTER -->"
B125_CSS_MARKER = "/* B125 source and method register */"

SOURCE_REGISTER = f"""
{B125_MARKER_START}
<section id="quellen-methodik" class="b125-source-register" aria-labelledby="b125SourceTitle">
  <p class="b125-kicker">Quellen und Methodik</p>
  <h2 id="b125SourceTitle">Datenbasis, fachliche Grundlagen und Lesart</h2>
  <p class="b125-lead">
    Die Kurzangaben an Karten und Fachblöcken nennen die jeweils unmittelbare Datenbasis.
    Dieser Abschnitt bündelt die verwendeten Quellen und ordnet ein, wie die Karten zu lesen sind.
  </p>

  <div class="b125-source-grid">
    <details open>
      <summary>Klimawirkung und Moorbodenschutz</summary>
      <ul>
        <li><a href="https://www.ipcc-nggip.iges.or.jp/public/wetlands/" rel="noopener">IPCC Wetlands Supplement</a> – methodischer Referenzrahmen für Treibhausgasinventare zu Feuchtgebieten und drainierten organischen Böden.</li>
        <li><a href="https://www.umweltbundesamt.de/daten/umweltzustand-trends/klima/treibhausgas-emissionen-in-deutschland/emissionen-der-landnutzung-aenderung" rel="noopener">Umweltbundesamt: Emissionen der Landnutzung, Landnutzungsänderung und Forstwirtschaft</a> – nationale Einordnung von Emissionen aus Mooren und organischen Böden.</li>
        <li><a href="https://www.bundesumweltministerium.de/themen/naturschutz/moorschutz" rel="noopener">BMUV: Moorschutz</a> – politischer und fachlicher Rahmen des Moorschutzes auf Bundesebene.</li>
        <li><a href="https://www.lubw.baden-wuerttemberg.de/natur-und-landschaft/moorschutz" rel="noopener">LUBW: Moorschutz Baden-Württemberg</a> – landesfachlicher Kontext zu Mooren, Wiedervernässung und Extensivierung.</li>
      </ul>
    </details>

    <details open>
      <summary>Kartengrundlagen</summary>
      <ul>
        <li><a href="https://www.greifswaldmoor.de/global-peatland-database-en.html" rel="noopener">Global Peatland Map 2.0 / Global Peatland Database</a> – globale Moorverbreitung und räumlicher Kontext.</li>
        <li><a href="https://www.fao.org/faostat/" rel="noopener">FAOSTAT</a> – Länderwerte zu Emissionen aus drainierten organischen Böden; eigene Klassifikation und kartografische Aufbereitung.</li>
        <li><a href="https://atlas.thuenen.de/maps/243/metadata_detail" rel="noopener">Thünen-Kulisse organischer Böden</a> – Deutschland-Kontext organischer Böden und Moorbodenkategorien.</li>
        <li><a href="https://www.lgrb-bw.de/geologischer-dienst/boden/bodenkundliche-landesaufnahme" rel="noopener">LGRB Baden-Württemberg: Bodenkarte 1 : 50 000 (BK50)</a> – bodenkundliche Grundlage für Moor- und Feuchtbodenkontexte.</li>
        <li><a href="https://fiona.landbw.de/" rel="noopener">FIONA Baden-Württemberg</a> – landwirtschaftliche Nutzungsinformation für die Oberschwaben-Auswertung.</li>
        <li><a href="https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units/territorial-units-statistics" rel="noopener">Eurostat GISCO NUTS</a> – administrative Gebietskulissen und regionale Einordnung.</li>
      </ul>
    </details>

    <details open>
      <summary>Nutzungspfade und Transformation</summary>
      <ul>
        <li><a href="https://mlr.baden-wuerttemberg.de/de/unsere-themen/landwirtschaft/landwirtschaft-im-klimawandel/klimaschutzsystem/wald-boden-und-holz-der-lulucf-sektor/moore" rel="noopener">MLR Baden-Württemberg: Moore</a> – landwirtschaftlicher Kontext, Wiedervernässung und Paludikultur-Beispiele.</li>
        <li><a href="https://lazbw.landwirtschaft-bw.de/%2CLde/Startseite/Themen/Moorbodenbewirtschaftung" rel="noopener">LAZBW: Moorbodenbewirtschaftung</a> – Praxisbezug zu Moorbodenbewirtschaftung, Grünland und alternativer Wertschöpfung.</li>
        <li><a href="https://ltz.landwirtschaft-bw.de/%2CLen/Arbeitsfelder/Moorbodenschutz" rel="noopener">LTZ Augustenberg: Moorbodenschutz</a> – fachliche Informationen zu Paludikultur und Moorbodenschutz.</li>
        <li><a href="https://www.moorwissen.de/paludi-progress.html" rel="noopener">Moorwissen / Paludi-PROGRESS</a> – Entwicklungsstand von Paludikulturen und Wertschöpfungsketten.</li>
        <li><a href="https://430a.uni-hohenheim.de/solamo-bw" rel="noopener">SOLAMO-BW</a> – sozioökonomischer Forschungsrahmen für Nutzungskonzepte wiedervernässter landwirtschaftlicher Moorflächen in Baden-Württemberg.</li>
      </ul>
    </details>
  </div>

  <div class="b125-method-box">
    <h3>Methodischer Hinweis</h3>
    <p>
      Die Karten zeigen räumliche Orientierung auf Basis öffentlich verfügbarer beziehungsweise projektbezogener Datengrundlagen.
      Flächenwerte für Oberschwaben wurden aus eigener Auswahl, Klassifikation und Verschneidung von FIONA, BK50 Moor-/
      Feuchtbodenkontext und GISCO NUTS abgeleitet und gerundet.
    </p>
    <p>
      Die Darstellung ist keine Eignungskarte, keine Priorisierung, keine hydrologische Modellierung und keine betriebliche
      Betroffenheitsanalyse. Eine belastbare Standortentscheidung würde zusätzliche Prüfung von Wasserstand, Hydrologie,
      Eigentums- und Bewirtschaftungsstruktur, Schutzstatus, Förderung, Technik und Wertschöpfungsketten erfordern.
    </p>
  </div>
</section>
{B125_MARKER_END}
"""

CSS_BLOCK = """
/* B125 source and method register */
.b125-source-register {
  width: min(1100px, calc(100% - 2rem));
  margin: clamp(4rem, 8vw, 7rem) auto clamp(3rem, 6vw, 5rem);
  padding: clamp(1.35rem, 3vw, 2.4rem);
  border: 1px solid rgba(31, 42, 34, .14);
  border-radius: 1.35rem;
  background: rgba(255, 253, 246, .92);
  box-shadow: 0 18px 54px rgba(31, 38, 33, .08);
}
.b125-kicker {
  margin: 0 0 .5rem;
  color: #657c38;
  font-size: .78rem;
  font-weight: 760;
  letter-spacing: .12em;
  text-transform: uppercase;
}
.b125-source-register h2 {
  margin: 0 0 .8rem;
  max-width: 780px;
  font-size: clamp(1.55rem, 3vw, 2.25rem);
  line-height: 1.08;
}
.b125-lead {
  max-width: 860px;
  margin: 0 0 1.55rem;
  line-height: 1.56;
  color: rgba(31, 42, 34, .82);
}
.b125-source-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}
.b125-source-grid details {
  background: rgba(255, 250, 240, .78);
  border: 1px solid rgba(31, 42, 34, .13);
  border-radius: 1rem;
  padding: 1rem 1rem .9rem;
}
.b125-source-grid summary {
  cursor: pointer;
  font-weight: 760;
  margin-bottom: .65rem;
}
.b125-source-grid ul {
  margin: .7rem 0 0;
  padding-left: 1.05rem;
}
.b125-source-grid li {
  margin: .55rem 0;
  line-height: 1.42;
  font-size: .94rem;
}
.b125-source-register a {
  color: inherit;
  text-decoration-color: rgba(101, 124, 56, .55);
  text-underline-offset: .18em;
}
.b125-method-box {
  margin-top: 1.4rem;
  padding: 1.15rem 1.25rem;
  border-left: 4px solid #657c38;
  border-radius: .9rem;
  background: rgba(244, 238, 225, .68);
}
.b125-method-box h3 {
  margin: 0 0 .55rem;
  font-size: 1rem;
}
.b125-method-box p {
  max-width: 920px;
  margin: .55rem 0 0;
  line-height: 1.52;
}
@media (max-width: 900px) {
  .b125-source-grid {
    grid-template-columns: 1fr;
  }
}
"""

RISK_PATTERNS = [
    "GLOBAL_FRAME_V1",
    "EUROPE_FRAME_V1",
    "Country hotspot layer:",
    "GPM context underneath",
    "same ArcGIS frame",
    "Europe frame:",
    "Germany frame:",
    "BW frame:",
    "Thuenen",
    "ArcGIS",
    "Peatland context",
    "Peat in soil mosaic",
    "Higher total emissions",
    "Higher emission density",
    "TOTAL EMISSIONS",
    "EMISSION DENSITY",
    "INTERPRETATION",
    "Ã",
    "�",
]

REQUIRED_PATTERNS = [
    "Quellen und Methodik",
    "Datenbasis, fachliche Grundlagen und Lesart",
    "Klimawirkung und Moorbodenschutz",
    "Kartengrundlagen",
    "Nutzungspfade und Transformation",
    "Methodischer Hinweis",
    "IPCC Wetlands Supplement",
    "Umweltbundesamt",
    "BMUV",
    "LUBW",
    "Global Peatland Map 2.0",
    "FAOSTAT",
    "Thünen-Kulisse organischer Böden",
    "Bodenkarte 1 : 50 000",
    "FIONA Baden-Württemberg",
    "Eurostat GISCO NUTS",
    "MLR Baden-Württemberg",
    "LAZBW",
    "LTZ Augustenberg",
    "Moorwissen / Paludi-PROGRESS",
    "SOLAMO-BW",
    "keine Eignungskarte",
    "keine Priorisierung",
    "keine hydrologische Modellierung",
    "keine betriebliche Betroffenheitsanalyse",
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


def remove_old_blocks(raw: str) -> str:
    raw = re.sub(
        r"\n?<!-- B125_SOURCE_AND_METHOD_REGISTER -->.*?<!-- /B125_SOURCE_AND_METHOD_REGISTER -->\n?",
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
    raw = re.sub(
        r"\n?<!-- B122_SOURCE_METHOD_REGISTER -->.*?<!-- /B122_SOURCE_METHOD_REGISTER -->\n?",
        "\n",
        raw,
        flags=re.DOTALL,
    )
    return raw


def insert_register(raw: str) -> tuple[str, str]:
    raw = remove_old_blocks(raw)
    pos = raw.rfind("</main>")
    if pos >= 0:
        return raw[:pos] + "\n\n" + SOURCE_REGISTER.strip() + "\n\n" + raw[pos:], "inserted_before_main_close"
    pos = raw.rfind("</body>")
    if pos >= 0:
        return raw[:pos] + "\n\n" + SOURCE_REGISTER.strip() + "\n\n" + raw[pos:], "inserted_before_body_close"
    return raw.rstrip() + "\n\n" + SOURCE_REGISTER.strip() + "\n", "appended_at_end"


def patch_css(css: str) -> tuple[str, str]:
    css = re.sub(
        r"\n?/\* B125 source and method register \*/.*?(?=\n/\* |\Z)",
        "\n",
        css,
        flags=re.DOTALL,
    )
    css = re.sub(
        r"\n?/\* B122 source and method register \*/.*?(?=\n/\* |\Z)",
        "\n",
        css,
        flags=re.DOTALL,
    )
    return css.rstrip() + "\n\n" + CSS_BLOCK.strip() + "\n", "inserted_or_replaced"


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B125 - Source and method register"
    if marker in current:
        return
    entry = f"""
## B125 - Source and method register ({TODAY})

- Added a consolidated source and method register after the central scrolly rebuild.
- Grouped attribution into climate/moor protection, cartographic foundations and transformation pathways.
- Added a method note clarifying that the page is orientation, not suitability mapping, prioritization, hydrological modelling or farm-level affectedness analysis.
- Did not add sender/contact/institutional framing.
- Did not modify maps, map state logic or data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def audit(raw: str, css: str) -> dict[str, object]:
    vis = visible_text(raw)
    risk_counts = {p: vis.count(p) for p in RISK_PATTERNS}
    required_counts = {p: vis.count(p) for p in REQUIRED_PATTERNS}
    link_count = raw.count('class="b125-source-register"') + raw.count('class="b125-source-grid"')
    css_count = css.count(B125_CSS_MARKER)
    href_count = raw.count('href="')
    source_section_count = raw.count(B125_MARKER_START)

    return {
        "risk_counts": risk_counts,
        "required_counts": required_counts,
        "risk_findings": sum(1 for v in risk_counts.values() if v > 0),
        "missing_required": sum(1 for v in required_counts.values() if v == 0),
        "source_section_count": source_section_count,
        "css_marker_count": css_count,
        "href_count": href_count,
        "layout_marker_count": link_count,
    }


def write_docs(result: dict[str, object], insert_status: str, css_status: str) -> None:
    status = "OK" if result["risk_findings"] == 0 and result["missing_required"] == 0 and result["source_section_count"] == 1 and result["css_marker_count"] == 1 else "REVIEW REQUIRED"

    report = [
        "# B125 – Source and Method Register",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B125 ergänzt nach dem stabilisierten B124/B124b-Stand einen kompakten Quellen- und Methodikbereich.",
        "",
        "## Änderungen",
        "",
        f"- Register: `{insert_status}`",
        f"- CSS: `{css_status}`",
        f"- Visible risk findings: {result['risk_findings']}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Source section count: {result['source_section_count']}",
        f"- CSS marker count: {result['css_marker_count']}",
        f"- href count in page: {result['href_count']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B125_source_and_method_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html -Pattern \"Quellen und Methodik\",\"IPCC Wetlands Supplement\",\"FAOSTAT\",\"Thünen-Kulisse\",\"FIONA Baden-Württemberg\",\"SOLAMO-BW\",\"keine hydrologische Modellierung\",\"GLOBAL_FRAME_V1\",\"Thuenen\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ]
    write_text(REPORT, "\n".join(report))

    audit_lines = [
        "# B125 source and method audit",
        "",
        f"- Status: {status}",
        f"- Visible risk findings: {result['risk_findings']}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Source section count: {result['source_section_count']}",
        f"- CSS marker count: {result['css_marker_count']}",
        f"- href count in page: {result['href_count']}",
        "",
        "## Risk patterns",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ]
    for p, c in result["risk_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Required patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["required_counts"].items():
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

    html, insert_status = insert_register(html)
    css, css_status = patch_css(css)

    write_text(INDEX, html)
    write_text(CSS, css)
    update_done()

    result = audit(html, css)
    write_docs(result, insert_status, css_status)

    ok = (
        result["risk_findings"] == 0
        and result["missing_required"] == 0
        and result["source_section_count"] == 1
        and result["css_marker_count"] == 1
    )

    print("B125 source and method register complete.")
    print("Changed/created:")
    for p in [INDEX, CSS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"Visible risk findings: {result['risk_findings']}")
    print(f"Missing required entries: {result['missing_required']}")
    print(f"Source section count: {result['source_section_count']}")
    print(f"CSS marker count: {result['css_marker_count']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B125_source_and_method_audit.txt -Encoding UTF8")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  python -m http.server 8000")


if __name__ == "__main__":
    main()
