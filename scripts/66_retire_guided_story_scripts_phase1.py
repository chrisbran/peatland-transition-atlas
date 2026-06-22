#!/usr/bin/env python3
"""
B66 - Retire guidedStory script tags phase 1

Purpose:
- After B64, #guidedStory is hidden/retired.
- B65 identified old guidedStory drivers as retire candidates.
- This patch removes their <script> tags from index.html only.
- It does NOT delete JS files, data files, image files, or map assets.

Targets removed from index.html:
- src/scrolly_story.js
- src/scrolly_story_layers.js
- src/gpm2_context_images.js

Outputs:
- index.html
- docs/B66_retire_guided_story_scripts_phase1.md
- tasks/done.md
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

TARGETS = [
    "src/scrolly_story.js",
    "src/scrolly_story_layers.js",
    "src/gpm2_context_images.js",
]

KEEP_SCRIPTS = [
    "src/app.js",
    "src/hotspots.js",
    "src/hotspot_base_layer.js",
    "src/bw_peat_layer.js",
    "src/central_global_map_story.js",
    "src/central_layer_state_hardener.js",
    "src/central_step_state_bridge.js",
    "src/central_stage_label_fix.js",
]

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")

def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def remove_script_tags(html: str) -> tuple[str, list[str], list[str]]:
    removed: list[str] = []
    missing: list[str] = []
    out = html

    for src in TARGETS:
        # Remove full script lines, preserving surrounding indentation/newlines.
        pattern = re.compile(
            rf"^[ \t]*<script\s+src=[\"']{re.escape(src)}[\"']\s*>\s*</script>[ \t]*\r?\n?",
            re.MULTILINE | re.IGNORECASE,
        )
        out2, n = pattern.subn("", out)
        if n:
            removed.append(src)
            out = out2
        else:
            missing.append(src)

    return out, removed, missing

def extract_script_srcs(html: str) -> list[str]:
    return re.findall(r'<script[^>]*\bsrc=["\']([^"\']+)["\'][^>]*>', html, flags=re.IGNORECASE)

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read(INDEX)

    if 'id="guidedStory"' not in html and "id='guidedStory'" not in html:
        raise RuntimeError("Could not find #guidedStory in index.html. Refusing to patch.")

    if "is-retired" not in html:
        raise RuntimeError(
            "#guidedStory does not appear to be retired/hidden. Run/verify B64 before B66."
        )

    new_html, removed, missing = remove_script_tags(html)

    if new_html != html:
        write(INDEX, new_html)

    final_scripts = extract_script_srcs(new_html)

    still_present = [src for src in TARGETS if src in final_scripts]
    if still_present:
        raise RuntimeError(f"Target script tags still present after patch: {still_present}")

    missing_keep = [src for src in KEEP_SCRIPTS if src not in final_scripts]
    if missing_keep:
        raise RuntimeError(f"Unexpected missing keep-script tags: {missing_keep}")

    doc = f"""# B66 - Retire guidedStory Script Tags Phase 1

Date: {date.today().isoformat()}

## 1. Purpose

B66 removes script tags for the old guided scroll story after B64 retired `#guidedStory` from the visible page flow and B65 classified the corresponding scripts as retire candidates.

This is a reversible cleanup step.

## 2. Changed files

- `index.html`
- `docs/B66_retire_guided_story_scripts_phase1.md`
- `tasks/done.md`

## 3. Removed from `index.html`

{chr(10).join(f"- `{src}`" for src in removed) if removed else "- none; all target script tags were already absent"}

## 4. Target scripts already absent

{chr(10).join(f"- `{src}`" for src in missing) if missing else "- none"}

## 5. Not deleted

The following files are not deleted by B66:

- `src/scrolly_story.js`
- `src/scrolly_story_layers.js`
- `src/gpm2_context_images.js`
- `public/data/germany_organic_soils_simplified.geojson`
- `public/data/bw_bk50_moor_simplified.geojson`
- `public/images/gpm2_global_context.png`
- `public/images/gpm2_europe_context.png`

## 6. Scripts intentionally kept

- `src/app.js`
- `src/hotspots.js`
- `src/hotspot_base_layer.js`
- `src/bw_peat_layer.js`
- `src/central_global_map_story.js`
- `src/central_layer_state_hardener.js`
- `src/central_step_state_bridge.js`
- `src/central_stage_label_fix.js`

## 7. Required visual QA

After B66, verify locally:

1. The retired `guidedStory` remains hidden.
2. The central PNG sticky story still works through all states.
3. The hotspot explorer still renders.
4. The evidence map still renders.
5. The pathway and South Germany fit sections still render.
6. The BW interactive layer still renders if retained.
7. There are no console errors caused by missing old guidedStory scripts.

## 8. Next step

Recommended B67:

`B67_legacy_asset_retirement_decision`

Scope:

- Decide whether to keep or retire `bwPeatLayer`.
- Decide whether old `public/images/gpm2_*` and old guidedStory GeoJSON-only dependencies should remain as archived assets or be removed from the public build.
- Update QA so BW PNGs and BW states are explicitly checked.
"""

    write(DOCS / "B66_retire_guided_story_scripts_phase1.md", doc)

    done_entry = f"""
## B66 - Retire guidedStory script tags phase 1 ({date.today().isoformat()})

- Removed old guidedStory script tags from `index.html`.
- Removed script tags only; no JS files, data files, images or map assets were deleted.
- Kept central PNG map story controller stack unchanged.
- Kept hotspot, evidence, pathway, fit and BW interactive modules loaded.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B66 - Retire guidedStory script tags phase 1" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B66 retired guidedStory script tags phase 1 complete.")
    print("Removed script tags:")
    for src in removed:
        print(f"  - {src}")
    if missing:
        print("Already absent:")
        for src in missing:
            print(f"  - {src}")
    print("Changed/created:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(DOCS / 'B66_retire_guided_story_scripts_phase1.md')}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
