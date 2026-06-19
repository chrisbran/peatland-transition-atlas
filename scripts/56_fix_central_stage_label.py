#!/usr/bin/env python3
r"""
56 - Fix central map stage label.

Run from repository root:
  python scripts\56_fix_central_stage_label.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()

LABEL_FIX_JS = '/*\n * B56 stage-label fix.\n *\n * Purpose:\n * Make the small map-stage chip follow the active central-map story state.\n * This fixes cases where the map image changes to Germany/Thuenen states but\n * the chip still reads "European peat context".\n */\n(function () {\n  const story = document.querySelector(".central-map-story");\n  if (!story) return;\n\n  const LABELS = {\n    extent: "GLOBAL PEAT CONTEXT",\n    total: "GLOBAL EMISSIONS PRESSURE",\n    density: "EMISSION DENSITY",\n    compare: "GLOBAL HOTSPOT INTERPRETATION",\n    "europe-borders": "EUROPE FRAME",\n    "europe-peat": "EUROPEAN PEAT CONTEXT",\n    "germany-context": "GERMANY FRAME",\n    "germany-thuenen-extent": "THUENEN KULISSE",\n    "germany-thuenen-types": "MOOR AND SOIL TYPES"\n  };\n\n  const ALIASES = {\n    "global-peat": "extent",\n    "global-extent": "extent",\n    "peat": "extent",\n    "gpm": "extent",\n    "global-total": "total",\n    "hotspots-total": "total",\n    "global-density": "density",\n    "hotspots-density": "density",\n    "global-compare": "compare"\n  };\n\n  const KNOWN_LABEL_PATTERN = /(GLOBAL|EUROPE|EUROPEAN|GERMANY|THUENEN|MOOR AND SOIL|EMISSION)/i;\n\n  function activeState() {\n    const raw = story.getAttribute("data-state") || "extent";\n    return ALIASES[raw] || raw;\n  }\n\n  function stageRoot() {\n    return (\n      story.querySelector(".central-map-stage") ||\n      story.querySelector(".central-map-visual") ||\n      story.querySelector(".central-map-card") ||\n      story.querySelector(".central-map-layer-stack") ||\n      story\n    );\n  }\n\n  function candidateElements(root) {\n    const selectors = [\n      "[data-central-map-mode]",\n      "[data-map-mode]",\n      ".central-map-mode",\n      ".central-map-kicker",\n      ".central-stage-mode",\n      ".map-mode",\n      ".map-chip",\n      ".map-kicker",\n      ".stage-chip",\n      ".map-pill",\n      ".central-map-pill"\n    ];\n\n    const set = new Set();\n    selectors.forEach((selector) => {\n      root.querySelectorAll(selector).forEach((el) => set.add(el));\n      story.querySelectorAll(selector).forEach((el) => set.add(el));\n    });\n\n    // Fallback: leaf elements in the map stage whose text looks like a stage chip.\n    root.querySelectorAll("span, p, div").forEach((el) => {\n      const text = (el.textContent || "").trim();\n      if (!text) return;\n      if (el.children.length > 0) return;\n      if (text.length > 42) return;\n      if (KNOWN_LABEL_PATTERN.test(text)) set.add(el);\n    });\n\n    return Array.from(set);\n  }\n\n  function applyLabel() {\n    const state = activeState();\n    const label = LABELS[state];\n    if (!label) return;\n\n    const root = stageRoot();\n    const candidates = candidateElements(root);\n\n    if (!candidates.length) return;\n\n    // Prefer elements that currently contain a known stage/context label.\n    const target =\n      candidates.find((el) => KNOWN_LABEL_PATTERN.test((el.textContent || "").trim())) ||\n      candidates[0];\n\n    target.textContent = label;\n  }\n\n  const observer = new MutationObserver(applyLabel);\n  observer.observe(story, { attributes: true, attributeFilter: ["data-state"] });\n\n  window.addEventListener("load", applyLabel);\n  document.addEventListener("DOMContentLoaded", applyLabel);\n  window.addEventListener("scroll", () => window.requestAnimationFrame(applyLabel), { passive: true });\n\n  setTimeout(applyLabel, 50);\n  setTimeout(applyLabel, 300);\n\n  window.__fixCentralStageLabel = applyLabel;\n})();\n'
DOC_TEMPLATE = '# B56 - Fix Central Map Stage Label\n\nDate: {date}\n\n## Issue\n\nAfter adding the Germany / Thuenen states, the small chip inside the central map stage could still read `EUROPEAN PEAT CONTEXT` while the Germany map and Germany text step were active.\n\n## Fix\n\nThis patch adds `src/central_stage_label_fix.js`, loaded after the central step bridge.\n\nThe script observes `.central-map-story[data-state]` and updates the small map-stage chip according to the active state.\n\n## Labels\n\n- `extent` -> `GLOBAL PEAT CONTEXT`\n- `total` -> `GLOBAL EMISSIONS PRESSURE`\n- `density` -> `EMISSION DENSITY`\n- `compare` -> `GLOBAL HOTSPOT INTERPRETATION`\n- `europe-borders` -> `EUROPE FRAME`\n- `europe-peat` -> `EUROPEAN PEAT CONTEXT`\n- `germany-context` -> `GERMANY FRAME`\n- `germany-thuenen-extent` -> `THUENEN KULISSE`\n- `germany-thuenen-types` -> `MOOR AND SOIL TYPES`\n\n## Acceptance check\n\nWhen scrolling into the Germany / Thuenen steps, the map-stage chip should no longer remain stuck on `EUROPEAN PEAT CONTEXT`.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def patch_index(path: Path):
    text = read(path)
    if "src/central_stage_label_fix.js" in text:
        return False

    new_tag = '  <script src="src/central_stage_label_fix.js"></script>\n'

    # Load after the bridge, because the bridge sets the active data-state.
    after = '<script src="src/central_step_state_bridge.js"></script>'
    idx = text.find(after)
    if idx != -1:
        insert_at = idx + len(after)
        write(path, text[:insert_at] + "\n" + new_tag.rstrip() + text[insert_at:])
        return True

    after = '<script src="src/central_layer_state_hardener.js"></script>'
    idx = text.find(after)
    if idx != -1:
        insert_at = idx + len(after)
        write(path, text[:insert_at] + "\n" + new_tag.rstrip() + text[insert_at:])
        return True

    body_close = "</body>"
    idx = text.rfind(body_close)
    if idx == -1:
        raise SystemExit("Could not find insertion point in index.html.")
    write(path, text[:idx] + new_tag + text[idx:])
    return True

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    index = root / "index.html"
    js = root / "src" / "central_stage_label_fix.js"

    write(js, LABEL_FIX_JS)
    changed_index = patch_index(index)

    write(root / "docs" / "B56_fix_central_map_stage_label.md", DOC_TEMPLATE.format(date=TODAY))

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B56 completed" not in done_text:
        done_text += f"- {TODAY}: Task B56 completed - fixed central map stage label for Germany / Thuenen states.\n"
        write(done, done_text)

    print("B56 central map stage label fix added.")
    print("Changed/created:")
    if changed_index:
        print("  index.html")
    print("  src/central_stage_label_fix.js")
    print("  docs/B56_fix_central_map_stage_label.md")
    print("  tasks/done.md")
    print()
    print("Checks:")
    print('  Select-String -Path index.html -Pattern "central_stage_label_fix"')
    print('  Select-String -Path src\\central_stage_label_fix.js -Pattern "GERMANY FRAME|THUENEN KULISSE|MOOR AND SOIL TYPES"')
    print()
    print("Then hard reload browser with Ctrl+F5.")

if __name__ == "__main__":
    main()
