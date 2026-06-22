from pathlib import Path
from datetime import datetime
import re

ROOT = Path.cwd()

REQUIRED = [
    "index.html",
    "src/central_global_map_story.js",
    "src/central_layer_state_hardener.js",
    "src/central_step_state_bridge.js",
    "src/central_stage_label_fix.js",
    "src/styles.css",
    "public/maps/bw/bw_admin_context.png",
    "public/maps/bw/bw_bk50_moor_extent.png",
]

for rel in REQUIRED:
    p = ROOT / rel
    if not p.exists():
        raise FileNotFoundError(f"Missing required file: {rel}")

changed = []

def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

def write_if_changed(rel, old, new):
    if old != new:
        (ROOT / rel).write_text(new, encoding="utf-8")
        changed.append(rel)

# ---------------------------------------------------------------------
# index.html: ensure BW images and steps exist; do not duplicate.
# ---------------------------------------------------------------------
rel = "index.html"
txt = read(rel)
old = txt

if "layer-bw-bk50-extent" not in txt:
    anchor = '        <img class="central-map-layer layer-germany-thuenen-types" src="public/maps/germany/germany_thuenen_moor_types.png" alt="">'
    if anchor not in txt:
        raise RuntimeError("Could not find Germany image anchor in index.html")
    txt = txt.replace(anchor, anchor + '\n        <img class="central-map-layer layer-bw-bk50-extent" src="public/maps/bw/bw_bk50_moor_extent.png" alt="">\n        <img class="central-map-layer layer-bw-admin" src="public/maps/bw/bw_admin_context.png" alt="">', 1)

if 'data-global-state="bw-context"' not in txt:
    anchor = '    <article class="central-map-step" data-global-state="germany-thuenen-types">'
    pos = txt.find(anchor)
    if pos == -1:
        raise RuntimeError("Could not find germany-thuenen-types article")
    end = txt.find("    </article>", pos)
    if end == -1:
        raise RuntimeError("Could not find end of germany-thuenen-types article")
    end += len("    </article>")
    steps = '''

    <article class="central-map-step" data-global-state="bw-context">
      <span>10 · Baden-Württemberg frame</span>
      <h3>Baden-Württemberg narrows the national frame to a regional planning scale.</h3>
      <p>
        The story moves from the national Thuenen Kulisse to a federal-state frame. This scale is closer
        to implementation, but still needs regional soil evidence before transition pathways can be interpreted locally.
      </p>
    </article>

    <article class="central-map-step" data-global-state="bw-bk50-extent">
      <span>11 · BK50 peat and wetland soils</span>
      <h3>BK50 shows the regional peat and wetland soil context.</h3>
      <p>
        This first BW layer deliberately shows all mapped BK50 peat and wetland soil features as one extent.
        It does not yet classify agricultural use or rewetting suitability; that requires a later combination
        with land-use evidence.
      </p>
    </article>'''
    txt = txt[:end] + steps + txt[end:]

write_if_changed(rel, old, txt)

# ---------------------------------------------------------------------
# central_global_map_story.js: add BW metadata for the original controller.
# Robust insertion before function setState, without requiring exact whitespace.
# ---------------------------------------------------------------------
rel = "src/central_global_map_story.js"
txt = read(rel)
old = txt

if '"bw-context"' not in txt:
    m = re.search(r"\n\s*function\s+setState\s*\(", txt)
    if m:
        block = '''

  // B62 Baden-Württemberg / BK50 states
  Object.assign(STATE_META, {
    "bw-context": {
      mode: "Baden-Württemberg frame",
      title: "Baden-Württemberg brings the national implementation frame to a regional planning scale.",
      legend: `
        <span><i class="legend-border"></i>Regional frame</span>
      `,
      source: "BW frame: Baden-Württemberg regional context exported from the same 16:9 ArcGIS map frame."
    },
    "bw-bk50-extent": {
      mode: "BK50 peat and wetland soils",
      title: "BK50 shows where peat and wetland soil contexts occur at regional scale.",
      legend: `
        <span><i class="legend-peat"></i>BK50 peat / wetland soil context</span>
        <span><i class="legend-border"></i>Regional frame</span>
      `,
      source: "BK50 BW layer: peat and wetland soil context shown as a single extent layer; no land-use or suitability classification is implied."
    }
  });
'''
        txt = txt[:m.start()] + block + txt[m.start():]
    else:
        print("WARNING: Could not find setState function marker in central_global_map_story.js; skipping STATE_META extension. Bridge metadata will still handle BW text.")

write_if_changed(rel, old, txt)

# ---------------------------------------------------------------------
# central_layer_state_hardener.js: ensure BW selectors and states.
# This file is authoritative for layer opacity.
# ---------------------------------------------------------------------
rel = "src/central_layer_state_hardener.js"
txt = read(rel)
old = txt

if "bwAdmin" not in txt:
    # Insert into layerSelectors before its closing brace.
    m = re.search(r"(const\s+layerSelectors\s*=\s*\{)(.*?)(\n\s*\};)", txt, flags=re.S)
    if not m:
        raise RuntimeError("Could not find layerSelectors object in central_layer_state_hardener.js")
    body = m.group(2).rstrip()
    body = body.rstrip().rstrip(",") + ',\n    bwAdmin: ".layer-bw-admin",\n    bwExtent: ".layer-bw-bk50-extent"'
    txt = txt[:m.start()] + m.group(1) + body + m.group(3) + txt[m.end():]

if '"bw-context"' not in txt:
    m = re.search(r"(const\s+stateLayers\s*=\s*\{)(.*?)(\n\s*\};)", txt, flags=re.S)
    if not m:
        raise RuntimeError("Could not find stateLayers object in central_layer_state_hardener.js")
    body = m.group(2).rstrip()
    body = body.rstrip().rstrip(",") + ''',
    "bw-context": {
      bwAdmin: 0.96
    },
    "bw-bk50-extent": {
      bwExtent: 0.98,
      bwAdmin: 0.88
    }'''
    txt = txt[:m.start()] + m.group(1) + body + m.group(3) + txt[m.end():]

write_if_changed(rel, old, txt)

# ---------------------------------------------------------------------
# central_step_state_bridge.js: add BW metadata to bridge META.
# This is needed because the bridge actively drives inserted states.
# ---------------------------------------------------------------------
rel = "src/central_step_state_bridge.js"
txt = read(rel)
old = txt

if '"bw-context"' not in txt:
    fn = re.search(r"\n\s*function\s+updateMeta\s*\(", txt)
    if not fn:
        raise RuntimeError("Could not find updateMeta function in central_step_state_bridge.js")
    prefix = txt[:fn.start()]
    suffix = txt[fn.start():]
    close_pos = prefix.rfind("\n  };")
    close_len = len("\n  };")
    if close_pos == -1:
        close_pos = prefix.rfind("\n  }")
        close_len = len("\n  }")
    if close_pos == -1:
        raise RuntimeError("Could not find META object closing marker in central_step_state_bridge.js")
    bw_meta = ''',
    "bw-context": {
      mode: "Baden-Württemberg frame",
      title: "Baden-Württemberg narrows the national frame to a regional planning scale.",
      legend: `
        <span><i class="legend-border"></i>Regional frame</span>
      `,
      source: "BW frame: regional context exported from the same 16:9 ArcGIS map frame."
    },
    "bw-bk50-extent": {
      mode: "BK50 peat and wetland soils",
      title: "BK50 shows the regional peat and wetland soil context.",
      legend: `
        <span><i class="legend-peat"></i>BK50 peat / wetland soil context</span>
        <span><i class="legend-border"></i>Regional frame</span>
      `,
      source: "BK50 BW layer: peat and wetland soil context shown as a single extent layer; no land-use or suitability classification is implied."
    }'''
    txt = prefix[:close_pos] + bw_meta + prefix[close_pos:] + suffix

write_if_changed(rel, old, txt)

# ---------------------------------------------------------------------
# central_stage_label_fix.js: add labels and make known-label regex match BW.
# ---------------------------------------------------------------------
rel = "src/central_stage_label_fix.js"
txt = read(rel)
old = txt

if '"bw-context"' not in txt:
    needle = '    "germany-thuenen-types": "MOOR AND SOIL TYPES"'
    if needle not in txt:
        raise RuntimeError("Could not find germany-thuenen-types label in central_stage_label_fix.js")
    replacement = needle + ',\n    "bw-context": "BADEN-WÜRTTEMBERG FRAME",\n    "bw-bk50-extent": "BK50 PEAT / WETLAND SOILS"'
    txt = txt.replace(needle, replacement, 1)

if "BADEN|BK50" not in txt:
    txt = txt.replace(
        "(GLOBAL|EUROPE|EUROPEAN|GERMANY|THUENEN|MOOR AND\nSOIL|EMISSION)",
        "(GLOBAL|EUROPE|EUROPEAN|GERMANY|THUENEN|MOOR AND\nSOIL|EMISSION|BADEN|BK50)",
        1,
    )
    txt = txt.replace(
        "(GLOBAL|EUROPE|EUROPEAN|GERMANY|THUENEN|MOOR AND SOIL|EMISSION)",
        "(GLOBAL|EUROPE|EUROPEAN|GERMANY|THUENEN|MOOR AND SOIL|EMISSION|BADEN|BK50)",
        1,
    )

write_if_changed(rel, old, txt)

# ---------------------------------------------------------------------
# styles.css: minimal CSS fallback. The JS hardener remains authoritative.
# Add !important so B51 default fallbacks cannot keep BW invisible.
# ---------------------------------------------------------------------
rel = "src/styles.css"
txt = read(rel)
old = txt

if "B62 BW central-story layer binding" not in txt:
    block = '''

/* B62 BW central-story layer binding. JS hardener remains authoritative. */
.layer-bw-admin,
.layer-bw-bk50-extent {
  opacity: 0;
}

.layer-bw-bk50-extent {
  z-index: 1;
}

.layer-bw-admin {
  z-index: 2;
}

.central-map-story[data-state="bw-context"] .layer-bw-admin {
  opacity: .96 !important;
}

.central-map-story[data-state="bw-bk50-extent"] .layer-bw-bk50-extent {
  opacity: .98 !important;
}

.central-map-story[data-state="bw-bk50-extent"] .layer-bw-admin {
  opacity: .88 !important;
}
'''
    txt = txt.rstrip() + block + "\n"

write_if_changed(rel, old, txt)

# ---------------------------------------------------------------------
# docs / tasks
# ---------------------------------------------------------------------
doc_rel = "docs/B62_repair_bw_extent_state_binding.md"
doc_txt = f"""# B62 repair — BW extent state binding

Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Purpose

Repairs the partial B62 state where BW image tags and story steps existed in `index.html`,
but the opacity/state controllers did not yet know `bw-context` and `bw-bk50-extent`.

## Scope

- Registers BW layers in `central_layer_state_hardener.js`.
- Adds BW metadata to `central_step_state_bridge.js`.
- Adds BW chip labels to `central_stage_label_fix.js`.
- Adds minimal CSS fallback rules in `styles.css`.
- Optionally extends `central_global_map_story.js` metadata if its structure allows robust insertion.

## Interpretation constraint

The BW extent is only a BK50 peat / wetland soil context layer. It does not imply agricultural use or rewetting suitability.
"""
(ROOT / doc_rel).write_text(doc_txt, encoding="utf-8")
changed.append(doc_rel)

done_rel = "tasks/done.md"
done_path = ROOT / done_rel
done = done_path.read_text(encoding="utf-8") if done_path.exists() else ""
entry = "- B62 repair: Completed BW extent state binding across central map hardener, bridge, labels, and CSS.\n"
if "B62 repair:" not in done:
    done_path.write_text(done.rstrip() + "\n" + entry, encoding="utf-8")
    changed.append(done_rel)

print("B62 repair v2 completed.")
print("Changed/created:")
for rel in changed:
    print(f"  {rel}")

print("\nRun checks:")
print('  Select-String -Path src\\central_layer_state_hardener.js -Pattern "bwAdmin|bwExtent|bw-context|bw-bk50-extent" -Context 2,4')
print('  Select-String -Path src\\central_step_state_bridge.js -Pattern "bw-context|bw-bk50-extent" -Context 2,5')
print('  Select-String -Path src\\central_stage_label_fix.js -Pattern "bw-context|bw-bk50-extent|BADEN|BK50" -Context 2,4')
print('  Select-String -Path src\\styles.css -Pattern "B62 BW|layer-bw-admin|layer-bw-bk50-extent|bw-context|bw-bk50-extent" -Context 1,3')
print("  python scripts\\58_visual_qa_and_commit_check.py")
