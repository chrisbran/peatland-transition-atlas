#!/usr/bin/env python3
r"""
B16 — Refine transition-evidence storyline.

Run from repository root:

  python scripts\33_refine_transition_evidence_storyline.py

This adds framing sections that distinguish the atlas from a general peatland-awareness product.
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()
TRANSITION_LOGIC_HTML = '\n<section id="transitionLogic" class="transition-logic-block">\n  <p class="section-kicker">Atlas framing</p>\n  <h2>From peatland extent to transition priorities</h2>\n  <p class="transition-logic-lede">\n    This prototype is not a general peatland-awareness atlas. It tests how spatial peatland extent,\n    drained organic-soil emissions, national implementation layers and literature evidence can be linked\n    into a transition-priority workflow.\n  </p>\n\n  <div class="transition-chain" aria-label="Atlas evidence chain">\n    <article class="transition-chain-card">\n      <span class="chain-step">01</span>\n      <h3>Extent</h3>\n      <p>Global Peatland Map 2.0 shows where peat-dominated and peat-in-soil-mosaic areas occur.</p>\n      <small>Context layer</small>\n    </article>\n    <article class="transition-chain-card">\n      <span class="chain-step">02</span>\n      <h3>Pressure</h3>\n      <p>Country hotspot data show where drained organic-soil emissions are concentrated.</p>\n      <small>Emissions layer</small>\n    </article>\n    <article class="transition-chain-card">\n      <span class="chain-step">03</span>\n      <h3>Implementation</h3>\n      <p>Germany and Baden-Württemberg layers show how global evidence becomes spatially constrained.</p>\n      <small>Planning boundary</small>\n    </article>\n    <article class="transition-chain-card">\n      <span class="chain-step">04</span>\n      <h3>Pathways</h3>\n      <p>Literature evidence links spatial context to wet use, paludiculture, grazing, biomass and governance options.</p>\n      <small>Transition evidence</small>\n    </article>\n  </div>\n\n  <div class="atlas-boundary-grid">\n    <div>\n      <h3>What this atlas is</h3>\n      <p>\n        A data-visualization and decision-support prototype that connects spatial layers, emissions hotspots,\n        regional implementation constraints and evidence-based transition pathways.\n      </p>\n    </div>\n    <div>\n      <h3>What this atlas is not</h3>\n      <p>\n        It is not a parcel-level rewetting suitability map, not a substitute for hydrological planning,\n        and not a general educational Mooratlas replica.\n      </p>\n    </div>\n  </div>\n</section>\n'
PROVENANCE_HTML = '\n<section id="layerProvenance" class="layer-provenance-block">\n  <p class="section-kicker">Layer logic</p>\n  <h2>Each map layer answers a different question</h2>\n\n  <div class="layer-provenance-grid">\n    <article>\n      <span>Context</span>\n      <h3>Where are peatlands?</h3>\n      <p>GPM 2.0 global and Europe images provide spatial context only.</p>\n    </article>\n    <article>\n      <span>Pressure</span>\n      <h3>Where are emissions concentrated?</h3>\n      <p>Country-level drained organic-soil emissions identify hotspot countries.</p>\n    </article>\n    <article>\n      <span>Implementation</span>\n      <h3>Where do constraints become concrete?</h3>\n      <p>Germany and Baden-Württemberg layers bridge from global evidence to regional planning boundaries.</p>\n    </article>\n    <article>\n      <span>Evidence</span>\n      <h3>What transition pathways are plausible?</h3>\n      <p>Literature-derived pathways translate spatial pressure into possible land-use transitions.</p>\n    </article>\n  </div>\n</section>\n'
CSS = '\n/* B16 transition-evidence storyline refinement */\n.transition-logic-block,\n.layer-provenance-block {\n  max-width: 1180px;\n  margin: clamp(3rem, 8vw, 6rem) auto;\n  padding: clamp(1.5rem, 4vw, 3rem);\n  border: 1px solid rgba(232, 222, 159, .14);\n  border-radius: 28px;\n  background:\n    radial-gradient(circle at 92% 8%, rgba(151, 170, 112, .10), transparent 30%),\n    linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,.012));\n}\n\n.transition-logic-block h2,\n.layer-provenance-block h2 {\n  max-width: 760px;\n  margin: .35rem 0 1rem;\n  font-size: clamp(2rem, 5vw, 4.5rem);\n  line-height: .98;\n  letter-spacing: -.045em;\n}\n\n.transition-logic-lede {\n  max-width: 800px;\n  font-size: clamp(1.05rem, 1.7vw, 1.35rem);\n  line-height: 1.55;\n  color: rgba(238, 236, 219, .78);\n}\n\n.transition-chain {\n  display: grid;\n  grid-template-columns: repeat(4, minmax(0, 1fr));\n  gap: .9rem;\n  margin-top: 2rem;\n}\n\n.transition-chain-card,\n.layer-provenance-grid article {\n  padding: 1rem;\n  border-radius: 18px;\n  background: rgba(6, 14, 12, .58);\n  border: 1px solid rgba(232, 222, 159, .12);\n}\n\n.transition-chain-card h3,\n.layer-provenance-grid h3,\n.atlas-boundary-grid h3 {\n  margin: .4rem 0 .55rem;\n  font-size: 1.02rem;\n}\n\n.transition-chain-card p,\n.layer-provenance-grid p,\n.atlas-boundary-grid p {\n  margin: 0;\n  color: rgba(238, 236, 219, .70);\n  line-height: 1.45;\n}\n\n.transition-chain-card small,\n.layer-provenance-grid span,\n.chain-step {\n  display: inline-flex;\n  color: rgb(217, 223, 130);\n  font-size: .76rem;\n  text-transform: uppercase;\n  letter-spacing: .08em;\n}\n\n.atlas-boundary-grid {\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  gap: .9rem;\n  margin-top: 1rem;\n}\n\n.atlas-boundary-grid > div {\n  padding: 1.1rem;\n  border-radius: 18px;\n  background: rgba(8, 16, 14, .72);\n  border: 1px solid rgba(232, 222, 159, .10);\n}\n\n.layer-provenance-grid {\n  display: grid;\n  grid-template-columns: repeat(4, minmax(0, 1fr));\n  gap: .9rem;\n  margin-top: 1.5rem;\n}\n\n@media (max-width: 900px) {\n  .transition-chain,\n  .layer-provenance-grid,\n  .atlas-boundary-grid {\n    grid-template-columns: 1fr;\n  }\n}\n'
DOC = '# B16 — Transition-Evidence Storyline Refinement\n\nDate: 2026-06-18\n\n## Purpose\n\nSharpen the atlas so it does not read as a general peatland-awareness atlas.\n\nThe core framing is now:\n\n> From peatland extent to transition priorities.\n\n## Added sections\n\n- `#transitionLogic`\n- `#layerProvenance`\n\n## Core evidence chain\n\n1. Extent — Global Peatland Map 2.0 context images.\n2. Pressure — country-level drained organic-soil emissions hotspots.\n3. Implementation — Germany and Baden-Württemberg spatial layers.\n4. Pathways — literature-derived transition evidence.\n\n## Boundary statement\n\nThe atlas is a data-visualization and decision-support prototype. It is not a parcel-level rewetting suitability map, not a substitute for hydrological planning and not a general Mooratlas replica.\n\n## Next step\n\nB17 should link the transition-pathway evidence cards more explicitly to the spatial layers.\n'
TASK = '# Task B17 — Link Transition Pathway Evidence to Spatial Layers\n\n## Goal\n\nConnect the literature-derived transition pathways more explicitly to the spatial story.\n\n## Rationale\n\nThe atlas now has a clear spatial chain:\n\n1. global peatland extent,\n2. country emissions pressure,\n3. Europe context,\n4. Germany implementation layer,\n5. Baden-Württemberg planning boundary.\n\nThe next step is to make the transition-pathway evidence feel connected to this chain instead of appearing as a separate literature module.\n\n## Work items\n\n1. Add a compact pathway matrix: wet grazing, paludiculture biomass, water-level management, governance/adoption.\n2. For each pathway, add:\n   - evidence strength,\n   - spatial fit,\n   - implementation constraints,\n   - data gap.\n3. Add a visual link from South Germany/BW section to the pathway cards.\n4. Add caveat: pathway fit is evidence-informed, not a site-level recommendation.\n\n## Acceptance criteria\n\n- Evidence cards are connected to the map storyline.\n- The user understands which pathways are relevant where and why.\n- The atlas remains a prototype, not a prescriptive planning tool.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def insert_before(html: str, marker: str, block: str) -> str:
    if block.strip() in html:
        return html
    if marker in html:
        return html.replace(marker, block + "\n\n" + marker, 1)
    return html

def insert_after_closing_section(html: str, section_id: str, block: str) -> str:
    if block.strip() in html:
        return html

    start = html.find(f'<section id="{section_id}"')
    if start == -1:
        return html

    end = html.find("</section>", start)
    if end == -1:
        return html

    end += len("</section>")
    return html[:end] + "\n\n" + block + html[end:]

def main():
    root = Path.cwd()
    index = root / "index.html"
    styles = root / "src" / "styles.css"

    if not index.exists():
        raise SystemExit("Run from repository root. index.html not found.")
    if not styles.exists():
        raise SystemExit("src/styles.css not found.")

    html = read(index)

    if 'id="transitionLogic"' not in html:
        html = insert_before(html, '<section id="guidedStory"', TRANSITION_LOGIC_HTML)

    if 'id="layerProvenance"' not in html:
        html = insert_after_closing_section(html, "guidedStory", PROVENANCE_HTML)

    write(index, html)

    css_text = read(styles)
    if "B16 transition-evidence storyline refinement" not in css_text:
        write(styles, css_text + "\n" + CSS)

    write(root / "docs" / "B16_transition_evidence_storyline_refinement.md", DOC)
    write(root / "tasks" / "B17_link_transition_pathway_evidence_to_spatial_layers.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B16 completed" not in done_text:
        done_text += f"- {TODAY}: Task B16 completed — refined transition-evidence storyline and layer logic.\n"
        write(done, done_text)

    print("B16 transition-evidence storyline refinement applied.")
    print("Changed/created:")
    print("  index.html")
    print("  src/styles.css")
    print("  docs/B16_transition_evidence_storyline_refinement.md")
    print("  tasks/B17_link_transition_pathway_evidence_to_spatial_layers.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
