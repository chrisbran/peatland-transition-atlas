#!/usr/bin/env python3
r"""
51 - Add hard central map layer controller.

Run from repository root:
  python scripts\51_add_hard_central_layer_controller.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()

HARDENER_JS = '/*\n * B51 hard central map layer controller.\n *\n * Purpose:\n * Keep central story map layers mutually exclusive and deterministic.\n * This intentionally runs after central_global_map_story.js.\n */\n(function () {\n  const story = document.querySelector(".central-map-story");\n  if (!story) return;\n\n  const layerSelectors = {\n    gpm: ".layer-gpm",\n    total: ".layer-total",\n    density: ".layer-density",\n    borders: ".layer-borders",\n    europePeat: ".layer-europe-peat",\n    europeBorders: ".layer-europe-borders",\n    germanyAdmin: ".layer-germany-admin",\n    germanyExtent: ".layer-germany-thuenen-extent",\n    germanyTypes: ".layer-germany-thuenen-types"\n  };\n\n  const aliases = {\n    "global-peat": "extent",\n    "global-extent": "extent",\n    "peat": "extent",\n    "gpm": "extent",\n    "global-total": "total",\n    "hotspots-total": "total",\n    "global-density": "density",\n    "hotspots-density": "density",\n    "global-compare": "compare"\n  };\n\n  const stateLayers = {\n    extent: {\n      gpm: 0.96,\n      borders: 0.72\n    },\n    total: {\n      gpm: 0.38,\n      total: 0.98,\n      borders: 0.66\n    },\n    density: {\n      gpm: 0.38,\n      density: 0.98,\n      borders: 0.66\n    },\n    compare: {\n      gpm: 0.38,\n      density: 0.98,\n      borders: 0.66\n    },\n    "europe-borders": {\n      europeBorders: 0.96\n    },\n    "europe-peat": {\n      europePeat: 0.98,\n      europeBorders: 0.96\n    },\n    "germany-context": {\n      germanyAdmin: 0.96\n    },\n    "germany-thuenen-extent": {\n      germanyExtent: 0.98,\n      germanyAdmin: 0.88\n    },\n    "germany-thuenen-types": {\n      germanyTypes: 0.98,\n      germanyAdmin: 0.86\n    }\n  };\n\n  function setOpacity(selector, value) {\n    document.querySelectorAll(selector).forEach((el) => {\n      el.style.setProperty("opacity", String(value), "important");\n    });\n  }\n\n  function applyState(rawState) {\n    const normalized = aliases[rawState] || rawState || "extent";\n    const visible = stateLayers[normalized] || stateLayers.extent;\n\n    Object.values(layerSelectors).forEach((selector) => {\n      setOpacity(selector, 0);\n    });\n\n    Object.entries(visible).forEach(([key, opacity]) => {\n      const selector = layerSelectors[key];\n      if (selector) setOpacity(selector, opacity);\n    });\n  }\n\n  function currentState() {\n    return story.getAttribute("data-state") || "extent";\n  }\n\n  const observer = new MutationObserver(() => applyState(currentState()));\n  observer.observe(story, { attributes: true, attributeFilter: ["data-state"] });\n\n  window.addEventListener("load", () => applyState(currentState()));\n  document.addEventListener("DOMContentLoaded", () => applyState(currentState()));\n\n  setTimeout(() => applyState(currentState()), 50);\n  setTimeout(() => applyState(currentState()), 300);\n\n  window.__applyCentralMapState = applyState;\n})();\n'
HARD_CSS = '\n/* B51 hard central map layer fallback. JS controller is authoritative. */\n.layer-germany-admin,\n.layer-germany-thuenen-extent,\n.layer-germany-thuenen-types {\n  opacity: 0 !important;\n}\n'
DOC_TEMPLATE = '# B51 - Hard Central Map Layer Controller\n\nDate: {date}\n\n## Issue\n\nGermany PNG layers were visible on Europe/global states. The previous script inserted HTML and attempted CSS/metadata binding, but the existing central story controller still allowed Germany layers to remain visible across states.\n\n## Fix\n\nThis patch adds `src/central_layer_state_hardener.js`, loaded after `src/central_global_map_story.js`.\n\nThe hardener:\n\n- observes `.central-map-story[data-state]`\n- force-hides all known central map layers\n- then explicitly shows only the layers belonging to the active state\n- applies opacity using `style.setProperty(..., "important")`\n\n## Supported states\n\n- `extent`\n- `total`\n- `density`\n- `compare`\n- `europe-borders`\n- `europe-peat`\n- `germany-context`\n- `germany-thuenen-extent`\n- `germany-thuenen-types`\n\n## Browser debug helper\n\nIn the browser console, a state can be forced manually:\n\n```javascript\nwindow.__applyCentralMapState("europe-peat")\nwindow.__applyCentralMapState("germany-thuenen-types")\n```\n\n## Acceptance check\n\n- Europe map states no longer show Germany overlays.\n- Germany states show only their intended layers.\n- Global states still work.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def patch_index(path: Path):
    text = read(path)
    if "src/central_layer_state_hardener.js" in text:
        return False

    new_tag = '  <script src="src/central_layer_state_hardener.js"></script>\n'
    central_tag = '<script src="src/central_global_map_story.js"></script>'
    idx = text.find(central_tag)
    if idx != -1:
        insert_at = idx + len(central_tag)
        text = text[:insert_at] + "\n" + new_tag.rstrip() + text[insert_at:]
        write(path, text)
        return True

    body_close = "</body>"
    idx = text.rfind(body_close)
    if idx == -1:
        raise SystemExit("Could not find central_global_map_story.js or </body> in index.html.")
    text = text[:idx] + new_tag + text[idx:]
    write(path, text)
    return True

def patch_css(path: Path):
    text = read(path)
    if "B51 hard central map layer fallback" in text:
        return False
    write(path, text.rstrip() + "\n" + HARD_CSS + "\n")
    return True

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    index = root / "index.html"
    styles = root / "src" / "styles.css"
    hardener = root / "src" / "central_layer_state_hardener.js"

    for p in [index, styles]:
        if not p.exists():
            raise SystemExit(f"Required file not found: {p}")

    write(hardener, HARDENER_JS)
    changed_index = patch_index(index)
    changed_css = patch_css(styles)

    write(root / "docs" / "B51_hard_central_map_layer_controller.md", DOC_TEMPLATE.format(date=TODAY))

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B51 completed" not in done_text:
        done_text += f"- {TODAY}: Task B51 completed - added hard central map layer controller.\n"
        write(done, done_text)

    print("B51 hard central map layer controller added.")
    print("Changed/created:")
    if changed_index:
        print("  index.html")
    print("  src/central_layer_state_hardener.js")
    if changed_css:
        print("  src/styles.css")
    print("  docs/B51_hard_central_map_layer_controller.md")
    print("  tasks/done.md")
    print()
    print("Checks:")
    print('  Select-String -Path index.html -Pattern "central_layer_state_hardener"')
    print('  Select-String -Path src\\central_layer_state_hardener.js -Pattern "germany-thuenen|europe-peat|setProperty"')
    print()
    print("Then hard reload browser with Ctrl+F5.")

if __name__ == "__main__":
    main()
