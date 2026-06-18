#!/usr/bin/env python3
r"""
B17b — Force insert pathway evidence matrix with non-conflicting ID.

Run from repository root:

  python scripts\35_force_insert_pathway_evidence_matrix.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()
HTML = '\n<section id="pathwayEvidenceMatrix" class="pathway-matrix-block">\n  <p class="section-kicker">Transition pathway bridge</p>\n  <h2>Spatial pressure only becomes useful when linked to feasible pathways</h2>\n  <p class="pathway-matrix-lede">\n    The atlas now separates context, pressure and implementation layers. This section connects those layers\n    to evidence-informed transition pathways. The matrix is not a prescription; it is a prototype logic for\n    asking which pathways are worth testing where.\n  </p>\n\n  <div class="pathway-matrix">\n    <article class="pathway-card">\n      <div class="pathway-card-head">\n        <span class="pathway-tag">Wet grazing</span>\n        <strong>Best fit</strong>\n      </div>\n      <h3>Wet grassland use under raised water tables</h3>\n      <dl>\n        <div><dt>Spatial signal</dt><dd>Regional organic-soil and BK50-Moor layers where agricultural use remains relevant.</dd></div>\n        <div><dt>Evidence role</dt><dd>Links climate mitigation to continued extensive land use and biodiversity co-benefits.</dd></div>\n        <div><dt>Constraint</dt><dd>Water-level control, animal management, fodder quality and farm acceptance.</dd></div>\n        <div><dt>Data gap</dt><dd>Local hydrology, trafficability, stocking systems and farm economics.</dd></div>\n      </dl>\n    </article>\n\n    <article class="pathway-card">\n      <div class="pathway-card-head">\n        <span class="pathway-tag">Paludiculture biomass</span>\n        <strong>Market dependent</strong>\n      </div>\n      <h3>Biomass production on rewetted peat soils</h3>\n      <dl>\n        <div><dt>Spatial signal</dt><dd>Large organic-soil clusters where harvesting logistics and land aggregation may be feasible.</dd></div>\n        <div><dt>Evidence role</dt><dd>Connects rewetting to productive use via reed, cattail, sedges or other wet biomass chains.</dd></div>\n        <div><dt>Constraint</dt><dd>Processing markets, machinery, contracts, subsidies and reliable water regimes.</dd></div>\n        <div><dt>Data gap</dt><dd>Crop suitability, biomass yields, transport distances and buyer infrastructure.</dd></div>\n      </dl>\n    </article>\n\n    <article class="pathway-card">\n      <div class="pathway-card-head">\n        <span class="pathway-tag">Water management</span>\n        <strong>Hydrology first</strong>\n      </div>\n      <h3>Raised water table, controlled drainage and partial rewetting</h3>\n      <dl>\n        <div><dt>Spatial signal</dt><dd>Hotspot countries and national organic-soil layers identify where hydrological transition matters most.</dd></div>\n        <div><dt>Evidence role</dt><dd>Frames the core mechanism behind emissions reduction: reducing aerobic peat decomposition.</dd></div>\n        <div><dt>Constraint</dt><dd>Neighbouring land, drainage infrastructure, flood risk, legal rights and water availability.</dd></div>\n        <div><dt>Data gap</dt><dd>Water-table depth, drainage networks, catchment boundaries and climate-water balance.</dd></div>\n      </dl>\n    </article>\n\n    <article class="pathway-card">\n      <div class="pathway-card-head">\n        <span class="pathway-tag">Governance & adoption</span>\n        <strong>Implementation risk</strong>\n      </div>\n      <h3>Payments, cooperation models and transition governance</h3>\n      <dl>\n        <div><dt>Spatial signal</dt><dd>Where emissions pressure overlaps with dense land-use claims and fragmented ownership.</dd></div>\n        <div><dt>Evidence role</dt><dd>Explains why technically plausible rewetting can fail without incentives and coordination.</dd></div>\n        <div><dt>Constraint</dt><dd>Income risk, policy uncertainty, institutional capacity and social acceptance.</dd></div>\n        <div><dt>Data gap</dt><dd>Ownership, farm typology, opportunity costs, programme uptake and advisory structures.</dd></div>\n      </dl>\n    </article>\n  </div>\n\n  <div class="pathway-interpretation-note">\n    <strong>Prototype rule:</strong>\n    a pathway should only move from “interesting” to “actionable” when spatial fit, hydrological feasibility,\n    farm economics and governance conditions can be checked together.\n  </div>\n</section>\n'
CSS = '\n/* B17b pathway evidence linked to spatial layers */\n.pathway-matrix-block {\n  max-width: 1180px;\n  margin: clamp(3rem, 8vw, 6rem) auto;\n  padding: clamp(1.5rem, 4vw, 3rem);\n  border: 1px solid rgba(232, 222, 159, .14);\n  border-radius: 28px;\n  background:\n    radial-gradient(circle at 12% 92%, rgba(151, 170, 112, .10), transparent 28%),\n    linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,.012));\n}\n\n.pathway-matrix-block h2 {\n  max-width: 860px;\n  margin: .35rem 0 1rem;\n  font-size: clamp(2rem, 5vw, 4.25rem);\n  line-height: .98;\n  letter-spacing: -.045em;\n}\n\n.pathway-matrix-lede {\n  max-width: 820px;\n  color: rgba(238, 236, 219, .76);\n  font-size: clamp(1.02rem, 1.6vw, 1.28rem);\n  line-height: 1.55;\n}\n\n.pathway-matrix {\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  gap: .95rem;\n  margin-top: 1.75rem;\n}\n\n.pathway-card {\n  padding: 1rem;\n  border-radius: 20px;\n  border: 1px solid rgba(232, 222, 159, .12);\n  background: rgba(6, 14, 12, .62);\n}\n\n.pathway-card-head {\n  display: flex;\n  justify-content: space-between;\n  gap: .75rem;\n  align-items: center;\n  margin-bottom: .8rem;\n}\n\n.pathway-card-head strong {\n  color: rgba(238, 236, 219, .58);\n  font-size: .72rem;\n  text-transform: uppercase;\n  letter-spacing: .08em;\n  white-space: nowrap;\n}\n\n.pathway-tag {\n  display: inline-flex;\n  align-items: center;\n  padding: .32rem .55rem;\n  border-radius: 999px;\n  color: rgb(217, 223, 130);\n  border: 1px solid rgba(217, 223, 130, .22);\n  background: rgba(217, 223, 130, .06);\n  font-size: .74rem;\n  text-transform: uppercase;\n  letter-spacing: .08em;\n}\n\n.pathway-card h3 {\n  margin: 0 0 .95rem;\n  font-size: clamp(1.05rem, 1.7vw, 1.35rem);\n  line-height: 1.15;\n}\n\n.pathway-card dl {\n  margin: 0;\n  display: grid;\n  gap: .65rem;\n}\n\n.pathway-card dl > div {\n  display: grid;\n  grid-template-columns: 8.5rem 1fr;\n  gap: .75rem;\n  padding-top: .55rem;\n  border-top: 1px solid rgba(232, 222, 159, .08);\n}\n\n.pathway-card dt {\n  color: rgba(217, 223, 130, .86);\n  font-size: .78rem;\n  text-transform: uppercase;\n  letter-spacing: .06em;\n}\n\n.pathway-card dd {\n  margin: 0;\n  color: rgba(238, 236, 219, .72);\n  line-height: 1.42;\n}\n\n.pathway-interpretation-note {\n  margin-top: 1rem;\n  padding: 1rem;\n  border-radius: 18px;\n  border: 1px solid rgba(217, 223, 130, .14);\n  background: rgba(217, 223, 130, .055);\n  color: rgba(238, 236, 219, .78);\n  line-height: 1.5;\n}\n\n.pathway-interpretation-note strong {\n  color: rgb(217, 223, 130);\n}\n\n@media (max-width: 900px) {\n  .pathway-matrix {\n    grid-template-columns: 1fr;\n  }\n\n  .pathway-card dl > div {\n    grid-template-columns: 1fr;\n    gap: .25rem;\n  }\n}\n'
DOC = '# B17b — Force Insert Pathway Evidence Matrix\n\nDate: 2026-06-18\n\n## Problem\n\nA previous B17 script checked for `id="pathwayMatrix"` before inserting the new section. The page already had an existing placeholder/div with this ID:\n\n`<div id="pathwayMatrix" class="matrix"></div>`\n\nTherefore the script skipped insertion.\n\n## Fix\n\nThis patch inserts the new evidence section with a non-conflicting ID:\n\n`#pathwayEvidenceMatrix`\n\n## Purpose\n\nConnect literature-derived transition pathways to the spatial storyline:\n\n- wet grazing,\n- paludiculture biomass,\n- water management,\n- governance and adoption.\n\nEach pathway is described through spatial signal, evidence role, constraint and data gap.\n'
TASK = '# Task B18 — Page Tightening and Story Copy Polish\n\n## Goal\n\nTighten the prototype after adding the full spatial and evidence chain.\n\n## Work items\n\n1. Review full page flow from top to bottom.\n2. Remove or compress redundant explanatory cards.\n3. Rewrite sticky-story step text around the sequence:\n   - extent,\n   - pressure,\n   - implementation,\n   - pathways.\n4. Shorten weak copy that duplicates the transition-logic and pathway-matrix sections.\n5. Check visual rhythm and vertical spacing.\n6. Make source/provenance notes more compact and consistent.\n\n## Acceptance criteria\n\n- The page reads as one coherent prototype.\n- The user is not overburdened with repeated caveats.\n- The difference from a general Mooratlas is obvious.\n- The site feels suitable as a portfolio project.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def insert_after_closing_section(html: str, section_id: str, block: str) -> str:
    if 'id="pathwayEvidenceMatrix"' in html:
        return html

    start = html.find(f'<section id="{section_id}"')
    if start != -1:
        end = html.find("</section>", start)
        if end != -1:
            end += len("</section>")
            return html[:end] + "\n\n" + block + html[end:]

    markers = [
        '<section id="southGermany"',
        '<section id="prototypeDebate"',
        '<section id="pathways"',
        '<section id="evidence"',
        '</body>'
    ]
    for marker in markers:
        if marker in html:
            if marker == '</body>':
                return html.replace(marker, block + "\n" + marker, 1)
            return html.replace(marker, block + "\n\n" + marker, 1)

    return html + "\n" + block

def main():
    root = Path.cwd()
    index = root / "index.html"
    styles = root / "src" / "styles.css"

    if not index.exists():
        raise SystemExit("Run from repository root. index.html not found.")
    if not styles.exists():
        raise SystemExit("src/styles.css not found.")

    html = read(index)
    html = insert_after_closing_section(html, "layerProvenance", HTML)
    write(index, html)

    css_text = read(styles)
    if "B17b pathway evidence linked to spatial layers" not in css_text:
        write(styles, css_text + "\n" + CSS)

    write(root / "docs" / "B17b_force_insert_pathway_evidence_matrix.md", DOC)
    write(root / "tasks" / "B18_page_tightening_and_story_copy_polish.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B17b completed" not in done_text:
        done_text += f"- {TODAY}: Task B17b completed — inserted pathway evidence matrix with non-conflicting ID.\n"
        write(done, done_text)

    print("B17b pathway evidence matrix inserted.")
    print("Changed/created:")
    print("  index.html")
    print("  src/styles.css")
    print("  docs/B17b_force_insert_pathway_evidence_matrix.md")
    print("  tasks/B18_page_tightening_and_story_copy_polish.md")
    print("  tasks/done.md")
    print()
    print("Check:")
    print("  Select-String -Path index.html -Pattern \"pathwayEvidenceMatrix\"")
    print("  Select-String -Path index.html -Pattern \"Spatial pressure only becomes useful\"")

if __name__ == "__main__":
    main()
