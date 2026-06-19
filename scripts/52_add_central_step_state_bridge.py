#!/usr/bin/env python3
r"""
52 - Add central step state bridge.

Run from repository root:
  python scripts\52_add_central_step_state_bridge.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()

BRIDGE_JS = '/*\n * B52 central map step-state bridge.\n *\n * Purpose:\n * Ensure every .central-map-step[data-global-state] actively drives\n * .central-map-story[data-state]. This is needed for newly inserted\n * Europe/Germany steps when the original controller does not recognize them.\n */\n(function () {\n  const story = document.querySelector(".central-map-story");\n  const steps = Array.from(document.querySelectorAll(".central-map-step[data-global-state]"));\n\n  if (!story || !steps.length) return;\n\n  const META = {\n    "europe-borders": {\n      mode: "Europe frame",\n      title: "Europe needs its own regional map frame.",\n      legend: `\n        <span><i class="legend-border"></i>European country borders</span>\n      `,\n      source: "Europe frame: GISCO country boundaries · exported from EUROPE_FRAME_V1."\n    },\n    "europe-peat": {\n      mode: "European peat context",\n      title: "European peatlands are spatially concentrated.",\n      legend: `\n        <span><i class="legend-peat"></i>Peatland context</span>\n        <span><i class="legend-mosaic"></i>Peat in soil mosaic</span>\n        <span><i class="legend-border"></i>Country frame</span>\n      `,\n      source: "GPM2 peatland context rendered in Europe frame · ETRS89 / LAEA Europe."\n    },\n    "germany-context": {\n      mode: "Germany frame",\n      title: "Germany is the national implementation frame.",\n      legend: `\n        <span><i class="legend-border"></i>Federal-state context</span>\n      `,\n      source: "Germany frame: NUTS 1 / federal-state context exported from GERMANY_FRAME_V1."\n    },\n    "germany-thuenen-extent": {\n      mode: "Thuenen Kulisse",\n      title: "The national peat and organic-soils Kulisse is spatially concentrated.",\n      legend: `\n        <span><i class="legend-thuenen-extent"></i>Thuenen peat / organic-soils Kulisse</span>\n        <span><i class="legend-border"></i>Federal-state context</span>\n      `,\n      source: "Thuenen Kulisse rendered as national extent layer · Germany frame."\n    },\n    "germany-thuenen-types": {\n      mode: "Moor and soil types",\n      title: "Type differentiation matters for transition pathways.",\n      legend: `\n        <span><i class="legend-thuenen-hh"></i>Hochmoorboden</span>\n        <span><i class="legend-thuenen-nh"></i>Niedermoorboden</span>\n        <span><i class="legend-thuenen-mf"></i>Moorfolgeboden</span>\n        <span><i class="legend-thuenen-tief-hh"></i>Tiefumbruchboden aus Hochmoor</span>\n        <span><i class="legend-thuenen-tief-nh"></i>Tiefumbruchboden aus Niedermoor</span>\n        <span><i class="legend-thuenen-flach-hh"></i>flach ueberdeckter Hochmoorboden</span>\n        <span><i class="legend-thuenen-flach-nh"></i>flach ueberdeckter Niedermoorboden</span>\n        <span><i class="legend-thuenen-maechtig-hh"></i>maechtig ueberdeckter Hochmoorboden</span>\n        <span><i class="legend-thuenen-maechtig-nh"></i>maechtig ueberdeckter Niedermoorboden</span>\n      `,\n      source: "Thuenen Kulisse symbolized by KAT_LANG / moor and soil type."\n    }\n  };\n\n  function first(selectors) {\n    for (const selector of selectors) {\n      const el = story.querySelector(selector) || document.querySelector(selector);\n      if (el) return el;\n    }\n    return null;\n  }\n\n  function setText(selectors, value) {\n    const el = first(selectors);\n    if (el && value) el.textContent = value;\n  }\n\n  function setHTML(selectors, value) {\n    const el = first(selectors);\n    if (el && value) el.innerHTML = value;\n  }\n\n  function updateMeta(state) {\n    const meta = META[state];\n    if (!meta) return;\n\n    setText([\n      "[data-central-map-mode]",\n      "[data-map-mode]",\n      ".central-map-mode",\n      ".central-map-kicker",\n      ".central-stage-mode",\n      ".map-mode",\n      ".map-chip"\n    ], meta.mode);\n\n    setText([\n      "[data-central-map-title]",\n      "[data-map-title]",\n      ".central-map-title",\n      ".central-stage-title",\n      ".map-title"\n    ], meta.title);\n\n    setHTML([\n      "[data-central-map-legend]",\n      "[data-map-legend]",\n      ".central-map-legend",\n      ".central-stage-legend",\n      ".map-legend"\n    ], meta.legend);\n\n    setText([\n      "[data-central-map-source]",\n      "[data-map-source]",\n      ".central-map-source",\n      ".central-stage-source",\n      ".map-source"\n    ], meta.source);\n  }\n\n  function applyState(state) {\n    if (!state) return;\n\n    if (story.getAttribute("data-state") !== state) {\n      story.setAttribute("data-state", state);\n    }\n\n    updateMeta(state);\n\n    if (typeof window.__applyCentralMapState === "function") {\n      window.__applyCentralMapState(state);\n    }\n  }\n\n  function activeStepByPosition() {\n    const anchor = window.innerHeight * 0.48;\n    let best = null;\n    let bestDistance = Infinity;\n\n    for (const step of steps) {\n      const rect = step.getBoundingClientRect();\n      const center = rect.top + rect.height * 0.5;\n      const distance = Math.abs(center - anchor);\n\n      if (rect.bottom >= 0 && rect.top <= window.innerHeight && distance < bestDistance) {\n        best = step;\n        bestDistance = distance;\n      }\n    }\n\n    return best;\n  }\n\n  let ticking = false;\n  function refresh() {\n    ticking = false;\n    const active = activeStepByPosition();\n    if (!active) return;\n    applyState(active.dataset.globalState);\n  }\n\n  function requestRefresh() {\n    if (ticking) return;\n    ticking = true;\n    window.requestAnimationFrame(refresh);\n  }\n\n  const observer = new IntersectionObserver((entries) => {\n    const visible = entries\n      .filter((entry) => entry.isIntersecting)\n      .sort((a, b) => b.intersectionRatio - a.intersectionRatio);\n\n    if (visible.length) {\n      applyState(visible[0].target.dataset.globalState);\n    } else {\n      requestRefresh();\n    }\n  }, {\n    root: null,\n    rootMargin: "-30% 0px -45% 0px",\n    threshold: [0, 0.15, 0.35, 0.6, 0.85]\n  });\n\n  steps.forEach((step) => observer.observe(step));\n  window.addEventListener("scroll", requestRefresh, { passive: true });\n  window.addEventListener("resize", requestRefresh);\n\n  document.addEventListener("DOMContentLoaded", requestRefresh);\n  window.addEventListener("load", requestRefresh);\n  setTimeout(requestRefresh, 50);\n  setTimeout(requestRefresh, 250);\n\n  window.__centralStepStateBridgeRefresh = refresh;\n})();\n'
DOC_TEMPLATE = "# B52 - Central Step State Bridge\n\nDate: {date}\n\n## Issue\n\nAfter adding the hard layer controller, the Germany layers disappeared because the central map story's `data-state` was not updated when the newly inserted Germany steps became active.\n\nThe text card could move to a Germany step while the map stage remained in a previous Europe state.\n\n## Fix\n\nThis patch adds `src/central_step_state_bridge.js`.\n\nThe bridge:\n\n- observes all `.central-map-step[data-global-state]` elements\n- sets `.central-map-story[data-state]` to the active step's state\n- calls `window.__applyCentralMapState(state)` from the hard layer controller if available\n- includes fallback scroll-position logic\n- updates common metadata/legend fields if matching elements exist\n\n## Expected result\n\n- Europe steps show Europe layers.\n- Germany steps show Germany layers.\n- Germany layers no longer overlay Europe/global states.\n- Germany no longer disappears when its steps are active.\n"

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def patch_index(path: Path):
    text = read(path)
    if "src/central_step_state_bridge.js" in text:
        return False

    new_tag = '  <script src="src/central_step_state_bridge.js"></script>\n'

    after = '<script src="src/central_layer_state_hardener.js"></script>'
    idx = text.find(after)
    if idx != -1:
        insert_at = idx + len(after)
        text = text[:insert_at] + "\n" + new_tag.rstrip() + text[insert_at:]
        write(path, text)
        return True

    after = '<script src="src/central_global_map_story.js"></script>'
    idx = text.find(after)
    if idx != -1:
        insert_at = idx + len(after)
        text = text[:insert_at] + "\n" + new_tag.rstrip() + text[insert_at:]
        write(path, text)
        return True

    body_close = "</body>"
    idx = text.rfind(body_close)
    if idx == -1:
        raise SystemExit("Could not find insertion point in index.html.")
    text = text[:idx] + new_tag + text[idx:]
    write(path, text)
    return True

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    index = root / "index.html"
    bridge = root / "src" / "central_step_state_bridge.js"

    write(bridge, BRIDGE_JS)
    changed_index = patch_index(index)

    write(root / "docs" / "B52_central_step_state_bridge.md", DOC_TEMPLATE.format(date=TODAY))

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B52 completed" not in done_text:
        done_text += f"- {TODAY}: Task B52 completed - added central step-state bridge.\n"
        write(done, done_text)

    print("B52 central step-state bridge added.")
    print("Changed/created:")
    if changed_index:
        print("  index.html")
    print("  src/central_step_state_bridge.js")
    print("  docs/B52_central_step_state_bridge.md")
    print("  tasks/done.md")
    print()
    print("Checks:")
    print('  Select-String -Path index.html -Pattern "central_step_state_bridge"')
    print('  Select-String -Path src\\central_step_state_bridge.js -Pattern "germany-context|__applyCentralMapState|data-global-state"')
    print()
    print("Then hard reload browser with Ctrl+F5.")

if __name__ == "__main__":
    main()
