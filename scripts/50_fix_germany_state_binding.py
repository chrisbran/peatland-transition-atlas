#!/usr/bin/env python3
r'''
50 - Fix Germany / Thuenen central-story state binding.

Problem fixed:
- Germany PNG layers were inserted into index.html but CSS/JS binding failed.
- Result: Germany layers remained visible across all states and overlaid Europe/global maps.

Run from repository root:
  python scripts\50_fix_germany_state_binding.py
'''

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()

GERMANY_META_ASSIGN = r'''
  // B19d/B50 Germany / Thuenen states
  Object.assign(STATE_META, {
    "germany-context": {
      mode: "Germany frame",
      title: "Germany is the national implementation frame.",
      legend: `
        <span><i class="legend-border"></i>Federal-state context</span>
      `,
      source: "Germany frame: NUTS 1 / federal-state context exported from GERMANY_FRAME_V1."
    },
    "germany-thuenen-extent": {
      mode: "Thuenen Kulisse",
      title: "The national peat and organic-soils Kulisse is spatially concentrated.",
      legend: `
        <span><i class="legend-thuenen-extent"></i>Thuenen peat / organic-soils Kulisse</span>
        <span><i class="legend-border"></i>Federal-state context</span>
      `,
      source: "Thuenen Kulisse rendered as national extent layer · Germany frame."
    },
    "germany-thuenen-types": {
      mode: "Moor and soil types",
      title: "Type differentiation matters for transition pathways.",
      legend: `
        <span><i class="legend-thuenen-hh"></i>Hochmoorboden</span>
        <span><i class="legend-thuenen-nh"></i>Niedermoorboden</span>
        <span><i class="legend-thuenen-mf"></i>Moorfolgeboden</span>
        <span><i class="legend-thuenen-tief-hh"></i>Tiefumbruchboden aus Hochmoor</span>
        <span><i class="legend-thuenen-tief-nh"></i>Tiefumbruchboden aus Niedermoor</span>
        <span><i class="legend-thuenen-flach-hh"></i>flach ueberdeckter Hochmoorboden</span>
        <span><i class="legend-thuenen-flach-nh"></i>flach ueberdeckter Niedermoorboden</span>
        <span><i class="legend-thuenen-maechtig-hh"></i>maechtig ueberdeckter Hochmoorboden</span>
        <span><i class="legend-thuenen-maechtig-nh"></i>maechtig ueberdeckter Niedermoorboden</span>
      `,
      source: "Thuenen Kulisse symbolized by KAT_LANG / moor and soil type."
    }
  });

'''

GERMANY_CSS = r'''
/* B50 fix Germany / Thuenen central-story layer binding */
.layer-germany-admin,
.layer-germany-thuenen-extent,
.layer-germany-thuenen-types {
  opacity: 0;
}

.central-map-story:not([data-state="germany-context"]):not([data-state="germany-thuenen-extent"]):not([data-state="germany-thuenen-types"]) .layer-germany-admin,
.central-map-story:not([data-state="germany-context"]):not([data-state="germany-thuenen-extent"]):not([data-state="germany-thuenen-types"]) .layer-germany-thuenen-extent,
.central-map-story:not([data-state="germany-context"]):not([data-state="germany-thuenen-extent"]):not([data-state="germany-thuenen-types"]) .layer-germany-thuenen-types {
  opacity: 0;
}

.central-map-story[data-state="germany-context"] .layer-gpm,
.central-map-story[data-state="germany-context"] .layer-total,
.central-map-story[data-state="germany-context"] .layer-density,
.central-map-story[data-state="germany-context"] .layer-borders,
.central-map-story[data-state="germany-context"] .layer-europe-peat,
.central-map-story[data-state="germany-context"] .layer-europe-borders,
.central-map-story[data-state="germany-context"] .layer-germany-thuenen-extent,
.central-map-story[data-state="germany-context"] .layer-germany-thuenen-types {
  opacity: 0;
}

.central-map-story[data-state="germany-context"] .layer-germany-admin {
  opacity: .96;
}

.central-map-story[data-state="germany-thuenen-extent"] .layer-gpm,
.central-map-story[data-state="germany-thuenen-extent"] .layer-total,
.central-map-story[data-state="germany-thuenen-extent"] .layer-density,
.central-map-story[data-state="germany-thuenen-extent"] .layer-borders,
.central-map-story[data-state="germany-thuenen-extent"] .layer-europe-peat,
.central-map-story[data-state="germany-thuenen-extent"] .layer-europe-borders,
.central-map-story[data-state="germany-thuenen-extent"] .layer-germany-thuenen-types {
  opacity: 0;
}

.central-map-story[data-state="germany-thuenen-extent"] .layer-germany-thuenen-extent {
  opacity: .98;
}

.central-map-story[data-state="germany-thuenen-extent"] .layer-germany-admin {
  opacity: .88;
}

.central-map-story[data-state="germany-thuenen-types"] .layer-gpm,
.central-map-story[data-state="germany-thuenen-types"] .layer-total,
.central-map-story[data-state="germany-thuenen-types"] .layer-density,
.central-map-story[data-state="germany-thuenen-types"] .layer-borders,
.central-map-story[data-state="germany-thuenen-types"] .layer-europe-peat,
.central-map-story[data-state="germany-thuenen-types"] .layer-europe-borders,
.central-map-story[data-state="germany-thuenen-types"] .layer-germany-thuenen-extent {
  opacity: 0;
}

.central-map-story[data-state="germany-thuenen-types"] .layer-germany-thuenen-types {
  opacity: .98;
}

.central-map-story[data-state="germany-thuenen-types"] .layer-germany-admin {
  opacity: .86;
}

.legend-thuenen-extent { background: #2F6B4F; }
.legend-thuenen-hh { background: #6E4B78; }
.legend-thuenen-mf { background: #8E7A4D; }
.legend-thuenen-nh { background: #2F6B4F; }
.legend-thuenen-tief-hh { background: #8A5A63; }
.legend-thuenen-tief-nh { background: #1F7A5C; }
.legend-thuenen-flach-hh { background: #9B7F8D; }
.legend-thuenen-flach-nh { background: #6F9A78; }
.legend-thuenen-maechtig-hh { background: #B08B6C; }
.legend-thuenen-maechtig-nh { background: #B7A15A; }
'''

DOC_TEMPLATE = '''# B50 - Fix Germany / Thuenen State Binding

Date: {date}

## Issue

Script 49 inserted Germany layers and steps into `index.html`, but the JavaScript metadata patch did not apply because the expected `STATE_META` closing marker was different in the current file.

This caused the Germany PNG layers to appear across other map states and overlay the Europe/global map.

## Fix

- Add robust CSS rules that hide Germany layers by default.
- Add Germany-specific show/hide rules for:
  - `germany-context`
  - `germany-thuenen-extent`
  - `germany-thuenen-types`
- Inject Germany state metadata into `src/central_global_map_story.js` via `Object.assign(STATE_META, ...)` before `function setState`.

## Acceptance check

- Europe steps no longer show Germany overlays.
- Germany steps correctly update the map title, legend, source text and layer stack.
- No duplicate Germany HTML blocks are created.
'''

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def patch_css(path: Path):
    text = read(path)
    if "B50 fix Germany / Thuenen central-story layer binding" not in text:
        write(path, text.rstrip() + "\n" + GERMANY_CSS + "\n")
        return True
    return False

def patch_js(path: Path):
    text = read(path)
    if "B19d/B50 Germany / Thuenen states" in text:
        return False
    if "STATE_META" not in text:
        raise SystemExit("Could not find STATE_META in src/central_global_map_story.js.")
    marker = "function setState"
    idx = text.find(marker)
    if idx == -1:
        raise SystemExit("Could not find function setState in src/central_global_map_story.js.")
    write(path, text[:idx] + GERMANY_META_ASSIGN + text[idx:])
    return True

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    styles = root / "src" / "styles.css"
    js = root / "src" / "central_global_map_story.js"
    index = root / "index.html"

    for p in [styles, js, index]:
        if not p.exists():
            raise SystemExit(f"Required file not found: {p}")

    index_text = read(index)
    missing = []
    for token in [
        "germany_admin_context.png",
        "germany_thuenen_moor_extent.png",
        "germany_thuenen_moor_types.png",
        'data-global-state="germany-context"',
        'data-global-state="germany-thuenen-extent"',
        'data-global-state="germany-thuenen-types"',
    ]:
        if token not in index_text:
            missing.append(token)

    if missing:
        raise SystemExit("Missing Germany HTML tokens in index.html: " + ", ".join(missing))

    changed_css = patch_css(styles)
    changed_js = patch_js(js)

    write(root / "docs" / "B50_fix_germany_state_binding.md", DOC_TEMPLATE.format(date=TODAY))

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B50 completed" not in done_text:
        done_text += f"- {TODAY}: Task B50 completed - fixed Germany / Thuenen central-story state binding.\n"
        write(done, done_text)

    print("B50 Germany state binding fix complete.")
    print("Changed:")
    if changed_css:
        print("  src/styles.css")
    if changed_js:
        print("  src/central_global_map_story.js")
    print("  docs/B50_fix_germany_state_binding.md")
    print("  tasks/done.md")
    print()
    print("Now hard reload local page with Ctrl+F5.")
    print('Check: Select-String -Path src\\central_global_map_story.js -Pattern "germany-context|B19d/B50"')
    print('Check: Select-String -Path src\\styles.css -Pattern "B50 fix Germany"')

if __name__ == "__main__":
    main()
