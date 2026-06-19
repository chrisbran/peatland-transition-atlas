#!/usr/bin/env python3
r"""
B18b-new — Add central global map story using ArcGIS-rendered layer stack.

Run from repository root:

  python scripts\39_add_central_global_map_story.py
"""

from pathlib import Path
import datetime
import re

TODAY = datetime.date.today().isoformat()
SECTION_HTML = '\n<section id="centralGlobalMapStory" class="central-map-story" data-state="extent">\n  <div class="central-map-sticky" aria-live="polite">\n    <div class="central-map-shell" role="img" aria-label="Scroll-driven global peatland and emissions map">\n      <div class="central-map-titlebar">\n        <span id="centralMapMode">Global peatland context</span>\n        <strong id="centralMapTitle">Peatlands are spatially concentrated.</strong>\n      </div>\n\n      <div class="central-map-layer-stack">\n        <img class="central-map-layer layer-gpm" src="public/maps/global/global_gpm2_peat_extent.png" alt="">\n        <img class="central-map-layer layer-total" src="public/maps/global/global_hotspots_total.png" alt="">\n        <img class="central-map-layer layer-density" src="public/maps/global/global_hotspots_density.png" alt="">\n        <img class="central-map-layer layer-borders" src="public/maps/global/global_country_borders.png" alt="">\n      </div>\n\n      <div id="centralMapLegend" class="central-map-legend">\n        <span><i class="legend-peat"></i>Peatland context</span>\n      </div>\n\n      <p id="centralMapSource" class="central-map-source">\n        Layer stack: Global Peatland Map 2.0 context and country hotspot layers. All images exported from the same ArcGIS global map frame.\n      </p>\n    </div>\n  </div>\n\n  <div class="central-map-steps">\n    <article class="central-map-step is-active" data-global-state="extent">\n      <span>01 · Extent</span>\n      <h3>Peatlands are not everywhere — they are spatially concentrated.</h3>\n      <p>\n        The first question is geographic: where are peat-dominated areas and peat-in-soil-mosaic areas located?\n        The map starts with peatland extent before adding emissions pressure.\n      </p>\n    </article>\n\n    <article class="central-map-step" data-global-state="total">\n      <span>02 · Absolute pressure</span>\n      <h3>Total emissions identify national climate relevance.</h3>\n      <p>\n        Absolute drained-organic-soil emissions show which countries dominate the global mitigation signal.\n        This is the first prioritisation view, but not the only one.\n      </p>\n    </article>\n\n    <article class="central-map-step" data-global-state="density">\n      <span>03 · Intensity</span>\n      <h3>Emission density changes the interpretation.</h3>\n      <p>\n        Density asks a different question: where is pressure concentrated relative to the mapped drained\n        organic-soil area? The same geography now tells a different story.\n      </p>\n    </article>\n\n    <article class="central-map-step" data-global-state="compare">\n      <span>04 · Read together</span>\n      <h3>Transition priorities need both views.</h3>\n      <p>\n        High totals indicate global climate relevance. High density indicates intensity. A transition atlas\n        should not force users to choose one metric; it should show why both are needed.\n      </p>\n    </article>\n  </div>\n</section>\n'
JS = '/*\nB18b-new — Central global map story.\n\nUses four ArcGIS-rendered PNG layers exported from the same GLOBAL_FRAME_V1.\nThe scroll state controls layer opacity only. The map frame, projection, size and placement remain fixed.\n*/\n\n(function () {\n  const STATE_META = {\n    extent: {\n      mode: "Global peatland context",\n      title: "Peatlands are spatially concentrated.",\n      legend: `\n        <span><i class="legend-peat"></i>Peatland context</span>\n        <span><i class="legend-mosaic"></i>Peat in soil mosaic</span>\n      `,\n      source: "Global Peatland Map 2.0 context · exported from GLOBAL_FRAME_V1."\n    },\n    total: {\n      mode: "Total emissions",\n      title: "Absolute emissions show national climate pressure.",\n      legend: `\n        <span><i class="legend-peat"></i>Peatland context</span>\n        <span><i class="legend-risk"></i>Higher total emissions</span>\n      `,\n      source: "Country hotspot layer: emissions_total_kt_co2e · GPM context underneath · same ArcGIS frame."\n    },\n    density: {\n      mode: "Emission density",\n      title: "Density reveals concentrated pressure.",\n      legend: `\n        <span><i class="legend-peat"></i>Peatland context</span>\n        <span><i class="legend-risk"></i>Higher emission density</span>\n      `,\n      source: "Country hotspot layer: emissions_density_t_co2e_per_ha · GPM context underneath · same ArcGIS frame."\n    },\n    compare: {\n      mode: "Metric comparison",\n      title: "Both views are needed for prioritisation.",\n      legend: `\n        <span><i class="legend-risk"></i>Total emissions</span>\n        <span><i class="legend-density"></i>Emission density</span>\n        <span><i class="legend-border"></i>Country frame</span>\n      `,\n      source: "The same global frame keeps the spatial comparison stable while the metric changes."\n    }\n  };\n\n  function setState(state) {\n    const section = document.querySelector("#centralGlobalMapStory");\n    if (!section || !STATE_META[state]) return;\n\n    section.setAttribute("data-state", state);\n\n    document.querySelectorAll(".central-map-step").forEach(step => {\n      step.classList.toggle("is-active", step.getAttribute("data-global-state") === state);\n    });\n\n    const meta = STATE_META[state];\n\n    const mode = document.querySelector("#centralMapMode");\n    const title = document.querySelector("#centralMapTitle");\n    const legend = document.querySelector("#centralMapLegend");\n    const source = document.querySelector("#centralMapSource");\n\n    if (mode) mode.textContent = meta.mode;\n    if (title) title.textContent = meta.title;\n    if (legend) legend.innerHTML = meta.legend;\n    if (source) source.textContent = meta.source;\n  }\n\n  function init() {\n    const section = document.querySelector("#centralGlobalMapStory");\n    if (!section) return;\n\n    const steps = Array.from(document.querySelectorAll(".central-map-step"));\n    if (!steps.length) return;\n\n    const observer = new IntersectionObserver(entries => {\n      const visible = entries\n        .filter(entry => entry.isIntersecting)\n        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];\n\n      if (!visible) return;\n\n      const state = visible.target.getAttribute("data-global-state");\n      setState(state);\n    }, {\n      threshold: [0.35, 0.5, 0.7],\n      rootMargin: "-28% 0px -38% 0px"\n    });\n\n    steps.forEach(step => observer.observe(step));\n    setState("extent");\n  }\n\n  window.addEventListener("DOMContentLoaded", init);\n})();\n'
CSS = '\n/* B18b-new central global map story */\n.central-map-story {\n  position: relative;\n  min-height: 430vh;\n  margin: clamp(2.5rem, 7vw, 6rem) 0;\n  background:\n    linear-gradient(180deg, rgba(5, 12, 10, 0), rgba(10, 18, 15, .42) 18%, rgba(10, 18, 15, .42) 82%, rgba(5, 12, 10, 0));\n}\n\n.central-map-sticky {\n  position: sticky;\n  top: 0;\n  height: 100vh;\n  display: grid;\n  place-items: center;\n  overflow: hidden;\n  pointer-events: none;\n}\n\n.central-map-shell {\n  position: relative;\n  width: min(1320px, calc(100vw - 2.5rem));\n  aspect-ratio: 16 / 9;\n  border-radius: 30px;\n  overflow: hidden;\n  background: rgba(9, 18, 16, .94);\n  border: 1px solid rgba(232, 222, 159, .14);\n  box-shadow: 0 24px 80px rgba(0, 0, 0, .28);\n}\n\n.central-map-layer-stack {\n  position: absolute;\n  inset: 0;\n}\n\n.central-map-layer {\n  position: absolute;\n  inset: 0;\n  width: 100%;\n  height: 100%;\n  object-fit: contain;\n  transition: opacity .7s ease;\n  user-select: none;\n  -webkit-user-drag: none;\n}\n\n.layer-gpm { opacity: .95; }\n.layer-total { opacity: 0; }\n.layer-density { opacity: 0; }\n.layer-borders { opacity: .82; }\n\n.central-map-story[data-state="extent"] .layer-gpm { opacity: .95; }\n.central-map-story[data-state="extent"] .layer-total { opacity: 0; }\n.central-map-story[data-state="extent"] .layer-density { opacity: 0; }\n.central-map-story[data-state="extent"] .layer-borders { opacity: .62; }\n\n.central-map-story[data-state="total"] .layer-gpm { opacity: .24; }\n.central-map-story[data-state="total"] .layer-total { opacity: .92; }\n.central-map-story[data-state="total"] .layer-density { opacity: 0; }\n.central-map-story[data-state="total"] .layer-borders { opacity: .82; }\n\n.central-map-story[data-state="density"] .layer-gpm { opacity: .22; }\n.central-map-story[data-state="density"] .layer-total { opacity: 0; }\n.central-map-story[data-state="density"] .layer-density { opacity: .92; }\n.central-map-story[data-state="density"] .layer-borders { opacity: .86; }\n\n.central-map-story[data-state="compare"] .layer-gpm { opacity: .12; }\n.central-map-story[data-state="compare"] .layer-total { opacity: .54; }\n.central-map-story[data-state="compare"] .layer-density { opacity: .48; }\n.central-map-story[data-state="compare"] .layer-borders { opacity: .90; }\n\n.central-map-titlebar {\n  position: absolute;\n  z-index: 3;\n  left: clamp(.8rem, 1.8vw, 1.35rem);\n  top: clamp(.8rem, 1.8vw, 1.35rem);\n  max-width: min(640px, calc(100% - 2rem));\n  padding: .7rem .85rem;\n  border-radius: 18px;\n  background: rgba(5, 11, 10, .70);\n  border: 1px solid rgba(232, 222, 159, .12);\n  backdrop-filter: blur(8px);\n}\n\n.central-map-titlebar span {\n  display: block;\n  color: rgb(217, 223, 130);\n  font-size: .72rem;\n  text-transform: uppercase;\n  letter-spacing: .09em;\n  margin-bottom: .2rem;\n}\n\n.central-map-titlebar strong {\n  display: block;\n  color: rgba(238, 236, 219, .92);\n  font-size: clamp(1rem, 1.7vw, 1.5rem);\n  line-height: 1.08;\n  letter-spacing: -.02em;\n}\n\n.central-map-legend {\n  position: absolute;\n  z-index: 3;\n  left: clamp(.8rem, 1.8vw, 1.35rem);\n  bottom: clamp(.8rem, 1.8vw, 1.35rem);\n  display: flex;\n  flex-wrap: wrap;\n  gap: .4rem .75rem;\n  max-width: min(740px, calc(100% - 2rem));\n  padding: .55rem .7rem;\n  border-radius: 999px;\n  background: rgba(5, 11, 10, .72);\n  border: 1px solid rgba(232, 222, 159, .12);\n  backdrop-filter: blur(8px);\n}\n\n.central-map-legend span {\n  display: inline-flex;\n  align-items: center;\n  gap: .35rem;\n  color: rgba(238, 236, 219, .74);\n  font-size: .76rem;\n  white-space: nowrap;\n}\n\n.central-map-legend i {\n  width: .95rem;\n  height: .55rem;\n  border-radius: 999px;\n  display: inline-block;\n}\n\n.legend-peat { background: #4B7860; }\n.legend-mosaic { background: #A5A877; }\n.legend-risk { background: #CF6546; }\n.legend-density { background: #BE7A52; }\n.legend-border {\n  background: transparent;\n  border: 1px solid rgba(216, 214, 197, .85);\n}\n\n.central-map-source {\n  position: absolute;\n  z-index: 3;\n  right: clamp(.8rem, 1.8vw, 1.35rem);\n  bottom: clamp(.8rem, 1.8vw, 1.35rem);\n  max-width: min(420px, 38%);\n  margin: 0;\n  color: rgba(238, 236, 219, .48);\n  font-size: .72rem;\n  line-height: 1.35;\n  text-align: right;\n}\n\n.central-map-steps {\n  position: relative;\n  z-index: 4;\n  width: min(430px, calc(100vw - 2rem));\n  margin-left: clamp(1rem, 7vw, 7rem);\n  padding-top: 22vh;\n  padding-bottom: 48vh;\n  pointer-events: auto;\n}\n\n.central-map-step {\n  min-height: 78vh;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  opacity: .55;\n  transition: opacity .2s ease;\n}\n\n.central-map-step.is-active {\n  opacity: 1;\n}\n\n.central-map-step > span,\n.central-map-step h3,\n.central-map-step p {\n  display: block;\n  max-width: 100%;\n  padding-left: .9rem;\n  padding-right: .9rem;\n}\n\n.central-map-step > span {\n  padding-top: .85rem;\n  color: rgb(217, 223, 130);\n  font-size: .72rem;\n  text-transform: uppercase;\n  letter-spacing: .09em;\n}\n\n.central-map-step h3 {\n  margin: .35rem 0 .45rem;\n  color: rgba(238, 236, 219, .94);\n  font-size: clamp(1.25rem, 2.4vw, 2rem);\n  line-height: 1.04;\n  letter-spacing: -.03em;\n}\n\n.central-map-step p {\n  margin: 0;\n  padding-bottom: .9rem;\n  color: rgba(238, 236, 219, .72);\n  line-height: 1.5;\n}\n\n.central-map-step::before {\n  content: "";\n  display: block;\n  position: absolute;\n  width: min(430px, calc(100vw - 2rem));\n  min-height: 11rem;\n  border-radius: 22px;\n  background: rgba(5, 11, 10, .74);\n  border: 1px solid rgba(232, 222, 159, .13);\n  box-shadow: 0 18px 52px rgba(0, 0, 0, .22);\n  backdrop-filter: blur(10px);\n  z-index: -1;\n}\n\n@media (max-width: 980px) {\n  .central-map-story {\n    min-height: auto;\n    margin: clamp(2rem, 6vw, 4rem) 0;\n  }\n\n  .central-map-sticky {\n    position: relative;\n    height: auto;\n    min-height: auto;\n    padding: 1rem;\n  }\n\n  .central-map-shell {\n    width: 100%;\n    border-radius: 22px;\n  }\n\n  .central-map-steps {\n    margin: 1rem auto 0;\n    padding: 0 1rem 2rem;\n    width: min(720px, 100%);\n  }\n\n  .central-map-step {\n    min-height: auto;\n    margin-bottom: 1rem;\n  }\n\n  .central-map-step::before {\n    width: min(720px, calc(100vw - 2rem));\n  }\n\n  .central-map-source {\n    display: none;\n  }\n}\n\n@media (max-width: 680px) {\n  .central-map-titlebar,\n  .central-map-legend {\n    position: relative;\n    left: auto;\n    bottom: auto;\n    top: auto;\n    max-width: none;\n    margin: .55rem;\n    border-radius: 16px;\n  }\n\n  .central-map-layer-stack {\n    position: relative;\n    aspect-ratio: 16 / 9;\n  }\n\n  .central-map-shell {\n    display: flex;\n    flex-direction: column;\n  }\n\n  .central-map-legend {\n    order: 3;\n  }\n}\n'
DOC = '# B18b-new — Central Global Map Story\n\nDate: 2026-06-18\n\n## Purpose\n\nReplace the growing multi-map approach with one central scroll-driven global map stage.\n\n## Input assets\n\nAll map assets must be exported from the same ArcGIS `GLOBAL_FRAME_V1` layout:\n\n- `public/maps/global/global_gpm2_peat_extent.png`\n- `public/maps/global/global_hotspots_total.png`\n- `public/maps/global/global_hotspots_density.png`\n- `public/maps/global/global_country_borders.png`\n\nAll files must be exactly 1600 x 900 px.\n\n## Design decision\n\nThe map frame, projection and placement remain fixed. Scroll states only change layer opacity and the explanatory text.\n\n## Story states\n\n1. Extent — GPM 2.0 peatland context.\n2. Total emissions — absolute drained-organic-soil emissions.\n3. Emission density — pressure relative to mapped drained organic-soil area.\n4. Compare — both views are needed for prioritisation.\n\n## Removed/replaced\n\nThe script removes earlier experimental sections if present:\n\n- `#emissionsMetricScrolly`\n- `#mapEvidencePanels`\n\nIt also removes script tags for:\n\n- `src/emissions_metric_scrolly.js`\n- `src/map_evidence_panels.js`\n\nThe files themselves are not deleted automatically.\n'
TASK = '# Task B18c — Add Global Peat/Hotspot Callouts\n\n## Goal\n\nMake the central global map story more interpretive without adding click interactions.\n\n## Work items\n\n1. Add scroll-state-specific callout labels for key countries or regions.\n2. Keep labels sparse and statement-driven.\n3. For total emissions, call out major absolute contributors.\n4. For emission density, call out countries where intensity changes the interpretation.\n5. Keep GPM context visible but subordinate.\n6. Do not over-label the map.\n\n## Acceptance criteria\n\n- The user can understand the metric shift without reading the ranking table.\n- Labels do not clutter the map.\n- The global map remains the central visual object.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def remove_section(html: str, section_id: str) -> str:
    start = html.find(f'<section id="{section_id}"')
    if start == -1:
        return html
    end = html.find("</section>", start)
    if end == -1:
        return html
    end += len("</section>")
    return html[:start] + html[end:]

def remove_script_tag(html: str, src: str) -> str:
    pattern = re.compile(r'\s*<script\s+src="' + re.escape(src) + r'"></script>\s*')
    return pattern.sub("\n", html)

def insert_before_markers(html: str, block: str) -> str:
    if 'id="centralGlobalMapStory"' in html:
        return html

    markers = [
        '<section id="pathwayEvidenceMatrix"',
        '<section id="layerProvenance"',
        '<section id="prototypeDebate"',
        '</body>'
    ]

    for marker in markers:
        if marker in html:
            if marker == "</body>":
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

    required = [
        root / "public" / "maps" / "global" / "global_gpm2_peat_extent.png",
        root / "public" / "maps" / "global" / "global_hotspots_total.png",
        root / "public" / "maps" / "global" / "global_hotspots_density.png",
        root / "public" / "maps" / "global" / "global_country_borders.png",
    ]

    for path in required:
        if not path.exists():
            raise SystemExit(f"Missing required map asset: {path}")

    html = read(index)

    html = remove_section(html, "emissionsMetricScrolly")
    html = remove_section(html, "mapEvidencePanels")

    html = remove_script_tag(html, "src/emissions_metric_scrolly.js")
    html = remove_script_tag(html, "src/map_evidence_panels.js")

    html = insert_before_markers(html, SECTION_HTML)

    tag = '<script src="src/central_global_map_story.js"></script>'
    if tag not in html:
        if "</body>" in html:
            html = html.replace("</body>", "  " + tag + "\n</body>", 1)
        else:
            html += "\n" + tag

    write(index, html)
    write(root / "src" / "central_global_map_story.js", JS)

    css_text = read(styles)
    if "B18b-new central global map story" not in css_text:
        write(styles, css_text + "\n" + CSS)

    write(root / "docs" / "B18b_new_central_global_map_story.md", DOC)
    write(root / "tasks" / "B18c_global_peat_hotspot_callouts.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B18b-new completed" not in done_text:
        done_text += f"- {TODAY}: Task B18b-new completed — added central global map story using ArcGIS-rendered layer stack.\n"
        write(done, done_text)

    print("B18b-new central global map story added.")
    print("Changed/created:")
    print("  index.html")
    print("  src/central_global_map_story.js")
    print("  src/styles.css")
    print("  docs/B18b_new_central_global_map_story.md")
    print("  tasks/B18c_global_peat_hotspot_callouts.md")
    print("  tasks/done.md")
    print()
    print("Removed from index.html if present:")
    print("  #emissionsMetricScrolly")
    print("  #mapEvidencePanels")
    print("  script src/emissions_metric_scrolly.js")
    print("  script src/map_evidence_panels.js")
    print()
    print("Check:")
    print("  Select-String -Path index.html -Pattern \"centralGlobalMapStory\"")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
