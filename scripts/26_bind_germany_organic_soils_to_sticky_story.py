#!/usr/bin/env python3
r"""
B14d — Bind Germany organic-soils layer to the sticky story.

Run from repository root:

  python scripts\26_bind_germany_organic_soils_to_sticky_story.py

Precondition:
  public/data/germany_organic_soils_simplified.geojson exists.
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()
CSS_APPEND = '\n/* B14d real Germany organic-soils sticky-story layer */\n.story-germany-organic {\n  stroke: rgba(12, 20, 18, .82);\n  stroke-width: .42;\n  opacity: .86;\n}\n\n.story-germany-organic:hover {\n  opacity: 1;\n  stroke: rgba(232,222,159,.88);\n  stroke-width: 1.1;\n}\n\n.story-germany-type-0 { fill: rgba(75, 120, 96, .72); }\n.story-germany-type-1 { fill: rgba(108, 141, 101, .72); }\n.story-germany-type-2 { fill: rgba(139, 124, 87, .76); }\n.story-germany-type-3 { fill: rgba(92, 111, 132, .72); }\n.story-germany-type-4 { fill: rgba(159, 128, 96, .76); }\n.story-germany-type-5 { fill: rgba(119, 103, 139, .72); }\n.story-germany-type-6 { fill: rgba(149, 158, 111, .72); }\n.story-germany-type-7 { fill: rgba(91, 132, 136, .72); }\n.story-germany-type-8 { fill: rgba(171, 151, 104, .74); }\n'
METHOD = '# B14d — Germany Organic-Soils Layer Bound to Sticky Story\n\nDate: 2026-06-18\n\n## Purpose\n\nReplace the Germany placeholder in the sticky-scroll story with the real simplified Germany organic-soils layer.\n\n## Input\n\n`public/data/germany_organic_soils_simplified.geojson`\n\n## Sticky story status after this step\n\n| Step | Status |\n|---|---|\n| World emissions | Real country hotspot layer |\n| Global peat/organic soils | Planned placeholder |\n| Europe | Planned placeholder |\n| Germany | Real organic-soils layer |\n| Baden-Württemberg | Real BK50-Moor layer |\n| Interpretation boundary | Caveat panel |\n\n## Interpretation boundary\n\nThe Germany layer is a national organic-soils context layer. It is not a local rewetting suitability map.\n\n## Technical approach\n\n- no external map library,\n- no build system,\n- SVG rendering from simplified GeoJSON,\n- bounding-box fit for Germany layer,\n- class-based color assignment.\n'
TASK = '# Task B15 — Process Europe Wetland/Peat Layer\n\n## Agent\n\nData & GIS Agent + Visualization Engineer Agent + QA Critic Agent\n\n## Goal\n\nReplace the Europe placeholder in the sticky-scroll story with a real European wetland/peat context layer.\n\n## Candidate source\n\nEuropean Wetland Map / Zenodo.\n\n## Recommended approach\n\n1. Download relevant European Wetland Map data.\n2. Identify classes suitable for peatland/organic-soil context.\n3. Clip or simplify for web display.\n4. Export to `public/data/europe_peat_wetland_simplified.geojson`.\n5. Bind the Europe sticky-story step to the real layer.\n6. Document caveats and source attribution.\n\n## Acceptance criteria\n\n- public file is small enough for GitHub Pages,\n- Europe layer is clearly labelled as wetland/peat context,\n- class meanings are documented,\n- no raw files under `data/external/` are committed,\n- story still distinguishes extent/context from suitability.\n'
RENDER_GERMANY_FUNCTION = '\n  function renderGermany() {\n    const features = (cache.germany?.features || []).filter(f => f.geometry);\n    const project = makeBBoxProject(features);\n\n    const paths = features.map((f, idx) => {\n      const props = f.properties || {};\n      const typeIdx = idx % 9;\n      const title = `${props.class || "Organic soils"} · ${props.class_long || ""} · ${props.source_area_ha || ""} ha`;\n      return `<path class="story-germany-organic story-germany-type-${typeIdx}" d="${geometryToPath(f.geometry, project)}">\n        <title>${title}</title>\n      </path>`;\n    }).join("");\n\n    return `\n      <svg class="story-real-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" preserveAspectRatio="xMidYMid meet">\n        <rect class="story-real-ocean" x="0" y="0" width="${WIDTH}" height="${HEIGHT}"></rect>\n        ${paths}\n      </svg>\n      <div class="story-real-caption">\n        <strong>Real layer:</strong> Germany organic-soils context layer · <span>${features.length.toLocaleString("en-US")} dissolved classes · public/data/germany_organic_soils_simplified.geojson</span>\n      </div>\n    `;\n  }\n\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main():
    root = Path.cwd()
    js_path = root / "src" / "scrolly_story_layers.js"
    styles = root / "src" / "styles.css"
    germany_data = root / "public" / "data" / "germany_organic_soils_simplified.geojson"

    if not js_path.exists():
        raise SystemExit("src/scrolly_story_layers.js not found. Run B13 first.")
    if not germany_data.exists():
        raise SystemExit("public/data/germany_organic_soils_simplified.geojson not found. Run B14c first.")

    js = read(js_path)

    if 'germany: "public/data/germany_organic_soils_simplified.geojson"' not in js:
        old = '    bw: "public/data/bw_bk50_moor_simplified.geojson"'
        new = '    bw: "public/data/bw_bk50_moor_simplified.geojson",\n    germany: "public/data/germany_organic_soils_simplified.geojson"'
        if old not in js:
            raise SystemExit("Could not find URLS.bw entry in scrolly_story_layers.js.")
        js = js.replace(old, new)

    if "function renderGermany()" not in js:
        anchor = "  function renderEuropeOrGermany(state) {"
        if anchor not in js:
            raise SystemExit("Could not find renderEuropeOrGermany insertion point.")
        js = js.replace(anchor, RENDER_GERMANY_FUNCTION + anchor)

    if "fetchJSON(URLS.germany)" not in js:
        old = "      fetchJSON(URLS.bw)\n    ]);"
        new = "      fetchJSON(URLS.bw),\n      fetchJSON(URLS.germany)\n    ]);"
        if old not in js:
            raise SystemExit("Could not find Promise.allSettled fetch insertion point.")
        js = js.replace(old, new)

    if "const [base, hotspots, bw, germany]" not in js:
        old = "    const [base, hotspots, bw] = await Promise.allSettled(["
        new = "    const [base, hotspots, bw, germany] = await Promise.allSettled(["
        if old not in js:
            raise SystemExit("Could not find Promise.allSettled destructuring.")
        js = js.replace(old, new)

    if "cache.germany = germany.value" not in js:
        old = '    if (bw.status === "fulfilled") cache.bw = bw.value;'
        new = '    if (bw.status === "fulfilled") cache.bw = bw.value;\n    if (germany.status === "fulfilled") cache.germany = germany.value;'
        if old not in js:
            raise SystemExit("Could not find cache.bw insertion point.")
        js = js.replace(old, new)

    old_required = "    if (!cache.base || !cache.hotspots || !cache.bw) {"
    if old_required in js:
        js = js.replace(old_required, "    if (!cache.base || !cache.hotspots || !cache.bw || !cache.germany) {")

    old_branch = '      else if (key === "europe" || key === "germany") htmlCache[key] = renderEuropeOrGermany(key);\n      else if (key === "bw") htmlCache[key] = renderBW();'
    new_branch = '      else if (key === "europe") htmlCache[key] = renderEuropeOrGermany(key);\n      else if (key === "germany") htmlCache[key] = renderGermany();\n      else if (key === "bw") htmlCache[key] = renderBW();'
    if old_branch in js:
        js = js.replace(old_branch, new_branch)

    write(js_path, js)

    css = read(styles)
    if "B14d real Germany organic-soils sticky-story layer" not in css:
        write(styles, css + "\n" + CSS_APPEND)

    write(root / "docs" / "B14d_bind_germany_organic_soils_to_sticky_story.md", METHOD)
    write(root / "tasks" / "B15_process_europe_wetland_peat_layer.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B14d completed" not in done_text:
        done_text += f"- {TODAY}: Task B14d completed — bound Germany organic-soils layer to sticky story.\n"
        write(done, done_text)

    print("B14d Germany layer bound to sticky story.")
    print("Changed/created:")
    print("  src/scrolly_story_layers.js")
    print("  src/styles.css")
    print("  docs/B14d_bind_germany_organic_soils_to_sticky_story.md")
    print("  tasks/B15_process_europe_wetland_peat_layer.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
