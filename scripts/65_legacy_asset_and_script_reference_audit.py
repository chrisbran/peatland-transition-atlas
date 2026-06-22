#!/usr/bin/env python3
"""
B65 - Legacy asset and script reference audit

Purpose:
- Audit which sections, scripts and public assets are still active after B64.
- Identify likely keep / review / retire-later candidates.
- Do not delete or modify application code.
- Create documentation files only.

Outputs:
- docs/B65_legacy_asset_and_script_reference_audit.md
- docs/B65_reference_inventory.csv
- docs/B65_referenced_assets.txt
- updates tasks/done.md
"""

from __future__ import annotations

import csv
import re
import subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"

INDEX = ROOT / "index.html"
SRC_DIR = ROOT / "src"
PUBLIC_DIR = ROOT / "public"

OUT_MD = DOCS / "B65_legacy_asset_and_script_reference_audit.md"
OUT_CSV = DOCS / "B65_reference_inventory.csv"
OUT_ASSETS = DOCS / "B65_referenced_assets.txt"
DONE = TASKS / "done.md"

SECTION_RE = re.compile(r'<section[^>]*\bid=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
SCRIPT_RE = re.compile(r'<script[^>]*\bsrc=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
LINK_RE = re.compile(r'<link[^>]*\bhref=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
ASSET_RE = re.compile(
    r'(public/(?:data|maps|images)/[A-Za-z0-9_\-./ %]+?\.(?:png|geojson|json|csv|md))',
    re.IGNORECASE,
)

KNOWN_SECTION_INTENT = {
    "story": "Introductory story overview; candidate to compress or merge into transitionLogic.",
    "transitionLogic": "Conceptual chain: Extent -> Pressure -> Implementation -> Pathways.",
    "guidedStory": "Retired B64 section; old scroll-driven story system.",
    "layerProvenance": "Layer-reading note; keep but likely shorten/reposition.",
    "centralGlobalMapStory": "Main PNG-based atlas story; do not touch in cleanup.",
    "pathwayEvidenceMatrix": "Bridge from spatial pressure to transition pathways.",
    "hotspots": "Country-level pressure explorer; keep as evidence explorer.",
    "map": "Evidence nodes / region examples; keep if supporting evidence remains useful.",
    "pathways": "Transition pathway cards; keep but group with evidence/pathway interpretation.",
    "fit": "South Germany fit matrix; keep but strengthen relation to BW endpoint.",
    "methodology": "Method / limitations; keep.",
    "data": "Prototype datasets; keep.",
    "bwPeatLayer": "Old BW GeoJSON interactive layer; review after central BW PNG story is stable.",
}

SCRIPT_ROLE = {
    "src/app.js": "Evidence/pathways/fit/data app logic.",
    "src/hotspots.js": "Country hotspot table/map interaction.",
    "src/hotspot_base_layer.js": "Base country layer for hotspot map.",
    "src/bw_peat_layer.js": "Old interactive BW BK50 GeoJSON map section.",
    "src/scrolly_story.js": "Old guidedStory scroll-state driver.",
    "src/scrolly_story_layers.js": "Old guidedStory GeoJSON layer renderer.",
    "src/gpm2_context_images.js": "Old guidedStory image context renderer.",
    "src/central_global_map_story.js": "Main central PNG map story metadata/controller.",
    "src/central_layer_state_hardener.js": "Authoritative central PNG layer opacity controller.",
    "src/central_step_state_bridge.js": "Central story step-state bridge.",
    "src/central_stage_label_fix.js": "Central story label synchronizer.",
    "src/emissions_metric_scrolly.js": "Untracked/legacy emissions metric scrolly module; review.",
}

DO_NOT_TOUCH_PREFIXES = [
    "public/maps/global/",
    "public/maps/europe/",
    "public/maps/germany/",
    "public/maps/bw/",
]

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def git_status_short() -> str:
    try:
        return subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True, encoding="utf-8", errors="replace")
    except Exception as exc:
        return f"[git status unavailable: {exc}]"

def extract_sections(index_txt: str):
    items = []
    for m in SECTION_RE.finditer(index_txt):
        tag = m.group(0)
        sid = m.group(1)
        retired = "is-retired" in tag or 'aria-hidden="true"' in tag or "aria-hidden='true'" in tag
        items.append({"id": sid, "tag": tag, "retired": retired})
    return items

def extract_active_scripts(index_txt: str):
    return SCRIPT_RE.findall(index_txt)

def extract_links(index_txt: str):
    return LINK_RE.findall(index_txt)

def extract_assets_from_text(txt: str):
    return sorted(set(m.group(1).replace("\\", "/") for m in ASSET_RE.finditer(txt)))

def file_list(base: Path):
    if not base.exists():
        return []
    return sorted([p for p in base.rglob("*") if p.is_file()])

def classify_script(path: str, loaded: bool) -> tuple[str, str]:
    if path.startswith("src/central_"):
        return "KEEP", "Central PNG story controller stack; do not touch in B65/B66 cleanup."
    if path == "src/styles.css":
        return "KEEP", "Main stylesheet linked by index.html; do not delete during cleanup."
    if path in ("src/hotspots.js", "src/hotspot_base_layer.js"):
        return "KEEP", "Needed while #hotspots remains visible as evidence explorer."
    if path == "src/app.js":
        return "KEEP", "Needed while evidence/pathway/fit/data modules remain visible."
    if path == "src/bw_peat_layer.js":
        return "REVIEW", "Needed only if old #bwPeatLayer remains visible; central BW PNG story now covers main BW context."
    if path in ("src/scrolly_story.js", "src/scrolly_story_layers.js", "src/gpm2_context_images.js"):
        return "RETIRE CANDIDATE", "Likely tied to retired #guidedStory; verify no other section depends on it before removing script tags."
    if path == "src/emissions_metric_scrolly.js":
        return "REVIEW", "Untracked/legacy module not loaded by index unless added elsewhere; inspect before deleting."
    if loaded:
        return "REVIEW", "Loaded by index; role not classified."
    return "REVIEW", "Not loaded by index; inspect before deletion."

def classify_asset(path: str, referenced_by: list[str]) -> tuple[str, str]:
    for pref in DO_NOT_TOUCH_PREFIXES:
        if path.startswith(pref):
            return "KEEP", "Central/static map asset; do not touch during B65/B66."
    if path.startswith("public/data/"):
        if path.endswith("bw_bk50_moor_simplified.geojson"):
            return "REVIEW", "Used by old BW interactive layer and old guidedStory; central BW PNG story reduces need."
        if path.endswith("germany_organic_soils_simplified.geojson"):
            return "RETIRE CANDIDATE", "Appears tied to old guidedStory GeoJSON renderer; verify after script-tag audit."
        if any(path.endswith(x) for x in [
            "country_hotspots.csv",
            "hotspot_countries_110m.geojson",
            "world_countries_110m_base.geojson",
            "papers.json",
            "transition_pathways.json",
            "region_case_studies.geojson",
            "atlas_story_sections.json",
        ]):
            return "KEEP", "Still referenced by visible explorer/data modules."
        if path.endswith((".csv", ".json", ".geojson")):
            return "REVIEW", "Public data file; check whether it is linked as dataset, loaded by JS, or only legacy."
    if path.startswith("public/images/gpm2_"):
        return "RETIRE CANDIDATE", "Likely old guidedStory image context; central PNG map stack now uses public/maps."
    return "REVIEW", "Referenced asset with no specific classification."

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    index_txt = read_text(INDEX)
    sections = extract_sections(index_txt)
    active_scripts = extract_active_scripts(index_txt)
    active_links = extract_links(index_txt)

    code_files = [INDEX] + file_list(SRC_DIR)
    refs_by_asset: dict[str, list[str]] = defaultdict(list)

    for path in code_files:
        try:
            txt = read_text(path)
        except Exception:
            continue
        for asset in extract_assets_from_text(txt):
            refs_by_asset[asset].append(rel(path))

    public_files = [rel(p) for p in file_list(PUBLIC_DIR)]
    src_files = [rel(p) for p in file_list(SRC_DIR)]

    rows = []

    for s in sections:
        sid = s["id"]
        status = "RETIRE CANDIDATE" if s["retired"] and sid == "guidedStory" else "KEEP/REVIEW"
        if sid in ("centralGlobalMapStory", "transitionLogic", "pathwayEvidenceMatrix", "methodology", "data"):
            status = "KEEP"
        elif sid == "guidedStory":
            status = "RETIRE CANDIDATE" if s["retired"] else "REVIEW"
        elif sid in ("story", "layerProvenance", "bwPeatLayer"):
            status = "REVIEW"
        elif sid in ("hotspots", "map", "pathways", "fit"):
            status = "KEEP"
        rows.append({
            "type": "section",
            "path_or_id": sid,
            "status": status,
            "loaded_or_referenced": "retired" if s["retired"] else "visible/active",
            "references": "",
            "note": KNOWN_SECTION_INTENT.get(sid, ""),
        })

    loaded_set = set(active_scripts)
    for p in src_files:
        loaded_as_script = p in loaded_set
        loaded_as_link = p in active_links
        loaded = loaded_as_script or loaded_as_link
        status, note = classify_script(p, loaded)
        rows.append({
            "type": "stylesheet" if p == "src/styles.css" else "script",
            "path_or_id": p,
            "status": status,
            "loaded_or_referenced": "loaded in index" if loaded_as_script else ("loaded via stylesheet link" if loaded_as_link else "not loaded in index"),
            "references": "",
            "note": SCRIPT_ROLE.get(p, note),
        })

    for p in sorted(public_files):
        ref_by = sorted(set(refs_by_asset.get(p, [])))
        if ref_by:
            status, note = classify_asset(p, ref_by)
            ref_text = "; ".join(ref_by)
        else:
            status, note = "UNREFERENCED", "No reference found in index.html or src/*.js/css; do not delete until reviewed."
            ref_text = ""
        rows.append({
            "type": "asset",
            "path_or_id": p,
            "status": status,
            "loaded_or_referenced": "referenced" if ref_by else "not referenced",
            "references": ref_text,
            "note": note,
        })

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["type", "path_or_id", "status", "loaded_or_referenced", "references", "note"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with OUT_ASSETS.open("w", encoding="utf-8", newline="\n") as f:
        for asset, refs in sorted(refs_by_asset.items()):
            f.write(f"{asset}\n")
            for r in sorted(set(refs)):
                f.write(f"  - {r}\n")

    loaded_scripts_md = "\n".join(f"- `{s}` — {SCRIPT_ROLE.get(s, 'unclassified loaded script')}" for s in active_scripts)

    section_md = "\n".join(
        f"- `{s['id']}` — {'retired / hidden' if s['retired'] else 'visible'} — {KNOWN_SECTION_INTENT.get(s['id'], '')}"
        for s in sections
    )

    retire_scripts = [r for r in rows if r["type"] == "script" and r["status"] == "RETIRE CANDIDATE"]
    review_scripts = [r for r in rows if r["type"] == "script" and r["status"] == "REVIEW"]
    retire_assets = [r for r in rows if r["type"] == "asset" and r["status"] == "RETIRE CANDIDATE"]
    unref_assets = [r for r in rows if r["type"] == "asset" and r["status"] == "UNREFERENCED"]
    review_assets = [r for r in rows if r["type"] == "asset" and r["status"] == "REVIEW"]

    def item_list(items, limit=None):
        shown = items if limit is None else items[:limit]
        if not shown:
            return "- none"
        txt = "\n".join(f"- `{x['path_or_id']}` — {x['note']}" for x in shown)
        if limit is not None and len(items) > limit:
            txt += f"\n- ... {len(items) - limit} more in `{rel(OUT_CSV)}`"
        return txt

    md = f"""# B65 - Legacy Asset and Script Reference Audit

Date: {date.today().isoformat()}

## 1. Purpose

B65 audits legacy scripts, public data files, public images and public map assets after B64 story-flow cleanup.

This is an audit-only step. No application section, script tag, data file or asset is removed by this patch.

## 2. Current section inventory

{section_md}

## 3. Scripts loaded by `index.html`

{loaded_scripts_md}

## 4. Initial script classification

### Keep

- `src/app.js` — required while evidence/pathway/fit/data sections stay visible.
- `src/hotspots.js` — required while the country hotspot explorer stays visible.
- `src/hotspot_base_layer.js` — required by the country hotspot map base.
- `src/central_global_map_story.js`
- `src/central_layer_state_hardener.js`
- `src/central_step_state_bridge.js`
- `src/central_stage_label_fix.js`
- `src/styles.css` ? main stylesheet linked by `index.html`; keep.

### Review

{item_list(review_scripts)}

### Retire candidates

{item_list(retire_scripts)}

Interpretation: these scripts appear tied to the old guided scroll story that B64 has hidden. They should not be deleted yet. B66 should first remove their script tags only if local visual QA confirms no visible section depends on them.

## 5. Initial asset classification

### Retire candidates

{item_list(retire_assets)}

### Review

{item_list(review_assets, limit=20)}

### Unreferenced in active code scan

{item_list(unref_assets, limit=30)}

Unreferenced does not automatically mean safe to delete. Some files are linked only from documentation, generated for future use, or intentionally retained as provenance.

## 6. Do not touch in B66

Do not touch the central PNG story map stack:

- `public/maps/global/`
- `public/maps/europe/`
- `public/maps/germany/`
- `public/maps/bw/`

Do not touch the central story controller stack:

- `src/central_global_map_story.js`
- `src/central_layer_state_hardener.js`
- `src/central_step_state_bridge.js`
- `src/central_stage_label_fix.js`
- `src/styles.css` ? main stylesheet linked by `index.html`; keep.

## 7. Proposed B66 scope

Recommended B66 title:

`B66_retire_guided_story_scripts_phase1`

Recommended B66 scope:

1. Keep `guidedStory` hidden.
2. Remove script tags for old guided-story drivers only after confirming they are not needed:
   - `src/scrolly_story.js`
   - `src/scrolly_story_layers.js`
   - `src/gpm2_context_images.js`
3. Do not delete the JS files yet.
4. Do not delete GeoJSON or image assets yet.
5. Run local visual QA and confirm that:
   - central PNG story still works,
   - hotspot explorer still works,
   - evidence map still works,
   - pathway and South Germany fit sections still render.

## 8. Generated inventory files

- `{rel(OUT_CSV)}`
- `{rel(OUT_ASSETS)}`

## 9. Git hygiene note

`git status --short` at audit time:

```text
{git_status_short().strip()}
```
"""

    OUT_MD.write_text(md, encoding="utf-8", newline="\n")

    done_entry = f"""
## B65 - Legacy asset and script reference audit ({date.today().isoformat()})

- Created `docs/B65_legacy_asset_and_script_reference_audit.md`.
- Created `docs/B65_reference_inventory.csv`.
- Created `docs/B65_referenced_assets.txt`.
- Audited active sections, script tags and public asset references after B64.
- No application code, script tags, public data files or map assets were removed.
"""
    if DONE.exists():
        current = read_text(DONE)
    else:
        current = "# Done\n"
    if "## B65 - Legacy asset and script reference audit" not in current:
        DONE.write_text(current.rstrip() + "\n" + done_entry, encoding="utf-8", newline="\n")

    print("B65 legacy asset and script reference audit complete.")
    print("Changed/created:")
    print(f"  {rel(OUT_MD)}")
    print(f"  {rel(OUT_CSV)}")
    print(f"  {rel(OUT_ASSETS)}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
