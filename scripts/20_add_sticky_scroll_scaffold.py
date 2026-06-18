#!/usr/bin/env python3
r"""
B12 — Add first sticky-scroll story scaffold.

Run from repository root:

  python scripts\20_add_sticky_scroll_scaffold.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()
SCROLLY_JS = '/*\nB12 sticky-scroll scaffold.\n\nThis is intentionally a light, dependency-free scaffold. It creates active\nstory states while the existing explorer sections remain unchanged below.\n*/\n\n(function () {\n  const steps = Array.from(document.querySelectorAll(".story-step"));\n  const visual = document.querySelector("#storyVisual");\n  const titleEl = document.querySelector("#storyVisualTitle");\n  const textEl = document.querySelector("#storyVisualText");\n  const stageEl = document.querySelector("#storyStage");\n  const layerEls = Array.from(document.querySelectorAll("[data-story-layer]"));\n\n  if (!steps.length || !visual || !titleEl || !textEl || !stageEl) return;\n\n  function setActive(step) {\n    const state = step.dataset.state || "world-emissions";\n    const title = step.dataset.visualTitle || step.querySelector("h3")?.textContent || "";\n    const text = step.dataset.visualText || step.querySelector("p")?.textContent || "";\n\n    steps.forEach(el => el.classList.toggle("active", el === step));\n\n    visual.dataset.state = state;\n    stageEl.dataset.state = state;\n    titleEl.textContent = title;\n    textEl.textContent = text;\n\n    layerEls.forEach(el => {\n      const activeStates = (el.dataset.storyLayer || "").split(/\\s+/);\n      el.classList.toggle("active", activeStates.includes(state));\n    });\n  }\n\n  const observer = new IntersectionObserver((entries) => {\n    const visible = entries\n      .filter(entry => entry.isIntersecting)\n      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];\n\n    if (visible) setActive(visible.target);\n  }, {\n    root: null,\n    threshold: [0.25, 0.45, 0.65, 0.85],\n    rootMargin: "-18% 0px -35% 0px"\n  });\n\n  steps.forEach(step => observer.observe(step));\n  setActive(steps[0]);\n})();\n'
CSS_APPEND = '\n/* B12 sticky-scroll guided story scaffold */\n.guided-story {\n  margin-top: 4rem;\n  padding-top: 2rem;\n}\n\n.scrolly-layout {\n  display: grid;\n  grid-template-columns: minmax(280px, .85fr) minmax(0, 1.15fr);\n  gap: 1.5rem;\n  align-items: start;\n}\n\n.story-steps {\n  display: grid;\n  gap: 72vh;\n  padding-bottom: 28vh;\n}\n\n.story-step {\n  min-height: 52vh;\n  display: grid;\n  align-items: center;\n  opacity: .45;\n  transition: opacity .18s ease, transform .18s ease;\n}\n\n.story-step.active {\n  opacity: 1;\n  transform: translateX(.25rem);\n}\n\n.story-step-card {\n  background: rgba(255,255,255,.045);\n  border: 1px solid rgba(255,255,255,.08);\n  border-radius: 1.1rem;\n  padding: 1.1rem;\n  box-shadow: 0 18px 42px rgba(0,0,0,.18);\n}\n\n.story-step.active .story-step-card {\n  border-color: rgba(212,196,118,.34);\n  background: rgba(212,196,118,.055);\n}\n\n.story-step-number {\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  width: 1.85rem;\n  height: 1.85rem;\n  border-radius: 999px;\n  margin-bottom: .65rem;\n  font-size: .78rem;\n  font-weight: 800;\n  color: var(--bg);\n  background: rgba(212,196,118,.82);\n}\n\n.story-step h3 {\n  margin: 0 0 .55rem;\n}\n\n.story-step p {\n  margin-bottom: .8rem;\n}\n\n.story-step .caveat {\n  margin-top: .75rem;\n}\n\n.story-visual-wrap {\n  position: sticky;\n  top: 1.2rem;\n  min-height: 74vh;\n}\n\n.story-visual {\n  min-height: 74vh;\n  display: grid;\n  grid-template-rows: auto 1fr auto;\n  background:\n    radial-gradient(circle at 45% 35%, rgba(212,196,118,.08), transparent 34%),\n    rgba(255,255,255,.035);\n  border: 1px solid rgba(255,255,255,.08);\n  border-radius: 1.3rem;\n  overflow: hidden;\n}\n\n.story-visual-header {\n  padding: 1rem 1.1rem .7rem;\n  border-bottom: 1px solid rgba(255,255,255,.07);\n}\n\n.story-visual-header p {\n  margin: .35rem 0 0;\n  color: var(--muted);\n}\n\n.story-stage {\n  position: relative;\n  min-height: 420px;\n  overflow: hidden;\n}\n\n.story-map-bg {\n  position: absolute;\n  inset: 1.1rem;\n  border-radius: 1rem;\n  background:\n    radial-gradient(ellipse at 25% 45%, rgba(81,110,102,.30), transparent 18%),\n    radial-gradient(ellipse at 55% 38%, rgba(96,123,111,.34), transparent 20%),\n    radial-gradient(ellipse at 72% 58%, rgba(82,116,96,.26), transparent 17%),\n    rgba(11,19,17,.9);\n  border: 1px solid rgba(255,255,255,.055);\n}\n\n.story-layer {\n  position: absolute;\n  opacity: 0;\n  transform: scale(.985);\n  transition: opacity .28s ease, transform .28s ease;\n  pointer-events: none;\n}\n\n.story-layer.active {\n  opacity: 1;\n  transform: scale(1);\n}\n\n.story-layer.world-emissions {\n  inset: 18% 12% 18% 12%;\n  background:\n    radial-gradient(circle at 63% 32%, rgba(202,112,82,.80), transparent 7%),\n    radial-gradient(circle at 49% 34%, rgba(204,160,91,.76), transparent 8%),\n    radial-gradient(circle at 34% 39%, rgba(202,112,82,.62), transparent 7%),\n    radial-gradient(circle at 54% 54%, rgba(165,172,105,.72), transparent 8%);\n  filter: blur(.2px);\n}\n\n.story-layer.global-peat {\n  inset: 12% 9%;\n  background:\n    radial-gradient(ellipse at 47% 24%, rgba(66,128,99,.62), transparent 5%),\n    radial-gradient(ellipse at 57% 27%, rgba(66,128,99,.56), transparent 7%),\n    radial-gradient(ellipse at 43% 41%, rgba(66,128,99,.46), transparent 6%),\n    radial-gradient(ellipse at 72% 48%, rgba(66,128,99,.42), transparent 6%);\n  filter: blur(.6px);\n}\n\n.story-layer.europe-zoom {\n  inset: 22% 37% 40% 38%;\n  border: 2px solid rgba(212,196,118,.72);\n  border-radius: 38% 42% 35% 45%;\n  box-shadow: 0 0 0 999px rgba(0,0,0,.22), 0 0 35px rgba(212,196,118,.18);\n}\n\n.story-layer.germany-zoom {\n  inset: 32% 45% 48% 46%;\n  border: 2px solid rgba(232,222,159,.92);\n  border-radius: 42% 38% 48% 37%;\n  background: rgba(212,196,118,.16);\n  box-shadow: 0 0 28px rgba(212,196,118,.22);\n}\n\n.story-layer.bw-zoom {\n  inset: 40% 49% 51% 49%;\n  border: 2px solid rgba(232,222,159,.98);\n  border-radius: 45%;\n  background: rgba(212,196,118,.28);\n  box-shadow: 0 0 36px rgba(212,196,118,.36);\n}\n\n.story-layer.boundary {\n  inset: 20% 14%;\n  border: 1px dashed rgba(232,222,159,.72);\n  border-radius: 1.2rem;\n  background: rgba(212,196,118,.045);\n}\n\n.story-state-label {\n  position: absolute;\n  left: 1.35rem;\n  bottom: 1.35rem;\n  right: 1.35rem;\n  display: grid;\n  gap: .45rem;\n  max-width: 36rem;\n}\n\n.story-state-label strong {\n  color: var(--text);\n  font-size: 1.2rem;\n}\n\n.story-state-label span {\n  color: var(--muted);\n}\n\n.story-layer-list {\n  display: flex;\n  flex-wrap: wrap;\n  gap: .45rem;\n  padding: .85rem 1.1rem 1.05rem;\n  border-top: 1px solid rgba(255,255,255,.07);\n}\n\n.story-layer-pill {\n  border: 1px solid rgba(255,255,255,.10);\n  border-radius: 999px;\n  padding: .35rem .6rem;\n  color: var(--muted);\n  font-size: .78rem;\n}\n\n.story-layer-pill.active {\n  color: var(--bg);\n  background: rgba(212,196,118,.82);\n  border-color: rgba(212,196,118,.88);\n}\n\n.story-links {\n  display: flex;\n  gap: .5rem;\n  flex-wrap: wrap;\n  margin-top: .8rem;\n}\n\n@media (max-width: 980px) {\n  .scrolly-layout {\n    grid-template-columns: 1fr;\n  }\n\n  .story-visual-wrap {\n    position: relative;\n    top: auto;\n    min-height: auto;\n    order: -1;\n  }\n\n  .story-visual {\n    min-height: 520px;\n  }\n\n  .story-steps {\n    gap: 1rem;\n    padding-bottom: 0;\n  }\n\n  .story-step {\n    min-height: auto;\n    opacity: 1;\n    transform: none;\n  }\n}\n'
SECTION_HTML = '\n<section id="guidedStory" class="section guided-story">\n  <div class="section-kicker">Guided scrollytelling prototype</div>\n  <h2>From national emission hotspots to real peatland landscapes</h2>\n  <p class="section-lead">\n    This guided view is the bridge between the existing explorer layers. It turns the atlas into a\n    scroll-driven narrative: country emissions first, then peat/organic-soil extent, and finally the\n    regional Baden-Württemberg layer.\n  </p>\n\n  <div class="scrolly-layout">\n    <div class="story-steps">\n      <article class="story-step"\n        data-state="world-emissions"\n        data-visual-title="Country-level emissions hotspot view"\n        data-visual-text="National drained-organic-soils emissions identify where the accounting hotspots are.">\n        <div class="story-step-card">\n          <span class="story-step-number">1</span>\n          <h3>Start with country-level emissions</h3>\n          <p>\n            The first map answers a screening question: which countries report large drained-organic-soils emissions?\n          </p>\n          <p class="caveat">This is a national accounting layer, not a local peatland map.</p>\n          <div class="story-links"><a class="button ghost" href="#hotspots">Open hotspot explorer</a></div>\n        </div>\n      </article>\n\n      <article class="story-step"\n        data-state="global-peat"\n        data-visual-title="Peat and organic soils become the spatial context"\n        data-visual-text="The story then shifts from countries to the underlying land: where peat and organic soils occur.">\n        <div class="story-step-card">\n          <span class="story-step-number">2</span>\n          <h3>Then reveal the actual peat/organic-soil context</h3>\n          <p>\n            Emissions are reported nationally, but transition happens in real landscapes. A peat/organic-soils layer\n            makes that spatial context visible.\n          </p>\n        </div>\n      </article>\n\n      <article class="story-step"\n        data-state="europe"\n        data-visual-title="Zoom to Europe"\n        data-visual-text="The European step should connect global peatland patterns with continental policy and land-use contexts.">\n        <div class="story-step-card">\n          <span class="story-step-number">3</span>\n          <h3>Zoom to Europe</h3>\n          <p>\n            Europe is the bridge scale: detailed enough for policy and land-use comparison, but still broad enough\n            to show cross-country contrasts.\n          </p>\n        </div>\n      </article>\n\n      <article class="story-step"\n        data-state="germany"\n        data-visual-title="Germany as the national bridge layer"\n        data-visual-text="Germany links the country hotspot layer to national organic-soils spatial data.">\n        <div class="story-step-card">\n          <span class="story-step-number">4</span>\n          <h3>Translate the hotspot view to Germany</h3>\n          <p>\n            Germany can become the national bridge layer: from total drained-organic-soils emissions toward the\n            actual organic-soil distribution.\n          </p>\n        </div>\n      </article>\n\n      <article class="story-step"\n        data-state="bw"\n        data-visual-title="Baden-Württemberg: regional soil context"\n        data-visual-text="The BK50-Moor layer is the first concrete regional endpoint of the zoom story.">\n        <div class="story-step-card">\n          <span class="story-step-number">5</span>\n          <h3>End at Baden-Württemberg</h3>\n          <p>\n            The regional BK50-Moor layer shows where moor, moor-like and humus-rich groundwater soils occur.\n            This is the scale where transition questions start to become concrete.\n          </p>\n          <div class="story-links"><a class="button ghost" href="#bwPeatLayer">Open BW layer</a></div>\n        </div>\n      </article>\n\n      <article class="story-step"\n        data-state="boundary"\n        data-visual-title="The interpretation boundary"\n        data-visual-text="Peat/organic-soil extent is necessary context, but not sufficient for rewetting suitability.">\n        <div class="story-step-card">\n          <span class="story-step-number">6</span>\n          <h3>Keep the boundary visible</h3>\n          <p>\n            A peat/organic-soils map is not a rewetting suitability map. Suitability would require hydrology,\n            land use, management, ownership, policy and economic context.\n          </p>\n          <p class="caveat">This boundary is part of the atlas, not a footnote.</p>\n        </div>\n      </article>\n    </div>\n\n    <div class="story-visual-wrap">\n      <div id="storyVisual" class="story-visual" data-state="world-emissions">\n        <div class="story-visual-header">\n          <p class="eyebrow">Scroll-driven map states</p>\n          <h3 id="storyVisualTitle">Country-level emissions hotspot view</h3>\n          <p id="storyVisualText">National drained-organic-soils emissions identify where the accounting hotspots are.</p>\n        </div>\n\n        <div id="storyStage" class="story-stage" data-state="world-emissions">\n          <div class="story-map-bg"></div>\n          <div class="story-layer world-emissions active" data-story-layer="world-emissions"></div>\n          <div class="story-layer global-peat" data-story-layer="global-peat"></div>\n          <div class="story-layer europe-zoom" data-story-layer="europe"></div>\n          <div class="story-layer germany-zoom" data-story-layer="germany"></div>\n          <div class="story-layer bw-zoom" data-story-layer="bw"></div>\n          <div class="story-layer boundary" data-story-layer="boundary"></div>\n          <div class="story-state-label">\n            <strong>Prototype visual state</strong>\n            <span>The next implementation will bind these states to real map layers.</span>\n          </div>\n        </div>\n\n        <div class="story-layer-list">\n          <span class="story-layer-pill active" data-story-layer="world-emissions">World emissions</span>\n          <span class="story-layer-pill" data-story-layer="global-peat">Peat/organic soils</span>\n          <span class="story-layer-pill" data-story-layer="europe">Europe</span>\n          <span class="story-layer-pill" data-story-layer="germany">Germany</span>\n          <span class="story-layer-pill" data-story-layer="bw">Baden-Württemberg</span>\n          <span class="story-layer-pill" data-story-layer="boundary">Caveat</span>\n        </div>\n      </div>\n    </div>\n  </div>\n</section>\n'
METHOD = '# B12 — Sticky Scroll Scaffold\n\nDate: 2026-06-18\n\n## Purpose\n\nCreate the first guided scrollytelling section without removing the existing explorer sections.\n\n## What this adds\n\n- `#guidedStory` section,\n- sticky visual container,\n- six narrative scroll steps,\n- IntersectionObserver-based active-step handling,\n- abstract visual states for world emissions, peat/organic-soil context, Europe, Germany, Baden-Württemberg and interpretation boundary.\n\n## Design decision\n\nThis is a scaffold, not the final animated atlas. The existing explorer sections remain intact.\n\n## Why scaffold first?\n\nThe project now has several functioning components:\n\n- country hotspot map,\n- regional Baden-Württemberg BK50-Moor layer,\n- evidence/pathway sections.\n\nThe sticky-scroll section provides the narrative spine that can later bind those components into a guided story.\n\n## Next step\n\nB13 should replace the abstract visual states with real map layer states where feasible.\n'
TASK = '# Task B13 — Bind Sticky Story to Real Map Layers\n\n## Agent\n\nVisualization Engineer Agent + Data & GIS Agent + Story Editor Agent\n\n## Goal\n\nConnect the sticky-scroll scaffold to real atlas layers.\n\n## Candidate binding steps\n\n1. World emissions step → reuse country hotspot map state.\n2. Global peat/organic-soils step → placeholder until global layer is processed.\n3. Europe step → placeholder until European Wetland Map layer is processed.\n4. Germany step → placeholder until Germany organic-soils layer is processed.\n5. Baden-Württemberg step → reuse `bw_bk50_moor_simplified.geojson`.\n6. Boundary step → show caveat panel and layer interpretation.\n\n## Acceptance criteria\n\n- existing explorer sections still work,\n- sticky story remains readable,\n- no heavy framework is introduced,\n- unsupported layers are visibly labelled as planned/future rather than pretending to be complete.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def insert_guided_story(html: str) -> str:
    if 'id="guidedStory"' in html:
        return html

    markers = [
        '<section id="hotspots"',
        '<section id="hotspotLayer"',
        '<section id="evidence"',
        '<section id="bwPeatLayer"',
        '</main>'
    ]

    for marker in markers:
        if marker in html:
            if marker == '</main>':
                return html.replace(marker, SECTION_HTML + "\n" + marker)
            return html.replace(marker, SECTION_HTML + "\n" + marker)

    raise SystemExit("Could not find insertion point for guided story section.")

def main():
    root = Path.cwd()
    index = root / "index.html"
    if not index.exists():
        raise SystemExit("Run from repository root. index.html not found.")

    write(root / "src" / "scrolly_story.js", SCROLLY_JS)

    html = read(index)
    html = insert_guided_story(html)

    if 'src="src/scrolly_story.js"' not in html:
        marker = '<script src="src/bw_peat_layer.js"></script>'
        if marker in html:
            html = html.replace(marker, marker + '\n  <script src="src/scrolly_story.js"></script>')
        elif "</body>" in html:
            html = html.replace("</body>", '  <script src="src/scrolly_story.js"></script>\n</body>')
        else:
            raise SystemExit("Could not insert scrolly_story.js script tag.")

    write(index, html)

    styles = root / "src" / "styles.css"
    css = read(styles)
    if "B12 sticky-scroll guided story scaffold" not in css:
        write(styles, css + "\n" + CSS_APPEND)

    write(root / "docs" / "B12_sticky_scroll_scaffold.md", METHOD)
    write(root / "tasks" / "B13_bind_sticky_story_to_real_layers.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B12 completed" not in done_text:
        done_text += f"- {TODAY}: Task B12 completed — added first sticky-scroll guided story scaffold.\n"
        write(done, done_text)

    print("B12 sticky-scroll scaffold added.")
    print("Changed/created:")
    print("  index.html")
    print("  src/scrolly_story.js")
    print("  src/styles.css")
    print("  docs/B12_sticky_scroll_scaffold.md")
    print("  tasks/B13_bind_sticky_story_to_real_layers.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
