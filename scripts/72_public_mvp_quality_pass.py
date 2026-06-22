#!/usr/bin/env python3
"""
B72 - Public MVP quality pass

Purpose:
- Freeze the current page as a reviewable MVP prototype.
- Run a stricter quality pass than B58 for the current MVP state.
- Explicitly check BW map PNGs, central 11-step story states, retired legacy sections,
  lower evidence grouping and broken local references.
- Do not change application behavior, CSS, map states, scripts, data files or assets.

Outputs:
- docs/B72_public_mvp_quality_pass.md
- docs/B72_public_mvp_quality_report.md
- tasks/done.md

Does NOT:
- delete files,
- hide sections,
- remove script tags,
- modify index.html,
- modify CSS,
- modify central story JS.
"""

from __future__ import annotations

import os
import re
import struct
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

REPORT = DOCS / "B72_public_mvp_quality_report.md"
DOC = DOCS / "B72_public_mvp_quality_pass.md"

REQUIRED_MAP_PNGS = [
    "public/maps/global/global_gpm2_peat_extent.png",
    "public/maps/global/global_hotspots_total.png",
    "public/maps/global/global_hotspots_density.png",
    "public/maps/global/global_country_borders.png",
    "public/maps/europe/europe_gpm2_peat_extent.png",
    "public/maps/europe/europe_country_borders.png",
    "public/maps/germany/germany_admin_context.png",
    "public/maps/germany/germany_thuenen_moor_extent.png",
    "public/maps/germany/germany_thuenen_moor_types.png",
    "public/maps/bw/bw_admin_context.png",
    "public/maps/bw/bw_bk50_moor_extent.png",
]

REQUIRED_CENTRAL_SCRIPTS = [
    "src/central_global_map_story.js",
    "src/central_layer_state_hardener.js",
    "src/central_step_state_bridge.js",
    "src/central_stage_label_fix.js",
]

ACTIVE_SCRIPT_REFS = [
    "src/app.js",
    "src/hotspots.js",
    "src/hotspot_base_layer.js",
    "src/central_global_map_story.js",
    "src/central_layer_state_hardener.js",
    "src/central_step_state_bridge.js",
    "src/central_stage_label_fix.js",
]

CENTRAL_STATES = [
    "extent",
    "total",
    "density",
    "compare",
    "europe-borders",
    "europe-peat",
    "germany-context",
    "germany-thuenen-extent",
    "germany-thuenen-types",
    "bw-context",
    "bw-bk50-extent",
]

RETIRED_SECTIONS = {
    "guidedStory": "B64",
    "story": "B69",
    "bwPeatLayer": "B71",
}

LOWER_GROUPS = [
    "interpretationIntro",
    "supportingEvidenceGroupIntro",
    "prototypeAppendixIntro",
]

FORBIDDEN_ACTIVE_SCRIPT_TAGS = [
    "src/scrolly_story.js",
    "src/scrolly_story_layers.js",
    "src/gpm2_context_images.js",
]

EXPECTED_BW_REFS = [
    "public/maps/bw/bw_admin_context.png",
    "public/maps/bw/bw_bk50_moor_extent.png",
]

RAW_DATA_WARNING_PREFIXES = [
    "?? data/external/",
    "?? data/metadata/",
]

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")

def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def git_status_short() -> str:
    try:
        return subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True, encoding="utf-8", errors="replace")
    except Exception as exc:
        return f"[git status unavailable: {exc}]"

def png_header(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing"
    try:
        with path.open("rb") as f:
            sig = f.read(8)
            if sig != b"\x89PNG\r\n\x1a\n":
                return False, "not a PNG signature"
            length = struct.unpack(">I", f.read(4))[0]
            chunk_type = f.read(4)
            if chunk_type != b"IHDR" or length < 13:
                return False, "missing/invalid IHDR"
            data = f.read(13)
            width, height, bit_depth, color_type, compression, flt, interlace = struct.unpack(">IIBBBBB", data)
            color_name = {
                0: "grayscale",
                2: "RGB",
                3: "indexed",
                4: "grayscale+alpha",
                6: "RGBA",
            }.get(color_type, f"color_type={color_type}")
            ok = width == 1600 and height == 900 and bit_depth == 8 and color_type == 6
            return ok, f"PNG header {color_name} ({width}, {height}) bit_depth={bit_depth}"
    except Exception as exc:
        return False, f"PNG read error: {exc}"

def extract_local_refs(html: str) -> list[str]:
    refs = []
    # Include src and href references. Ignore fragment-only, http(s), mailto, tel and data URIs.
    for attr in ("src", "href"):
        for m in re.finditer(rf'\b{attr}\s*=\s*["\']([^"\']+)["\']', html, flags=re.IGNORECASE):
            val = m.group(1).strip()
            if not val or val.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")):
                continue
            # Strip query/hash.
            val = val.split("#", 1)[0].split("?", 1)[0]
            if val:
                refs.append(val)
    return sorted(set(refs))

def section_open_tag(html: str, section_id: str) -> str | None:
    m = re.search(
        rf'<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])[^>]*>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return m.group(0) if m else None

def script_refs(html: str) -> list[str]:
    return re.findall(r'<script[^>]*\bsrc=["\']([^"\']+)["\'][^>]*>', html, flags=re.IGNORECASE)

def add_result(results: list[tuple[str, str, str]], status: str, item: str, note: str) -> None:
    results.append((status, item, note))

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read(INDEX) if INDEX.exists() else ""
    css = read(CSS) if CSS.exists() else ""
    results: list[tuple[str, str, str]] = []
    warnings: list[str] = []
    failures: list[str] = []

    # 1. PNG checks
    for png in REQUIRED_MAP_PNGS:
        ok, msg = png_header(ROOT / png)
        if ok:
            add_result(results, "OK", png, msg)
        else:
            add_result(results, "FAIL", png, msg)
            failures.append(f"{png}: {msg}")

    # 2. Central scripts
    for s in REQUIRED_CENTRAL_SCRIPTS:
        if (ROOT / s).exists():
            add_result(results, "OK", s, "required central story script exists")
        else:
            add_result(results, "FAIL", s, "required central story script missing")
            failures.append(f"{s}: missing")

    # 3. Local reference check
    local_refs = extract_local_refs(html)
    broken = []
    for ref in local_refs:
        # External-looking protocol-relative URLs are not expected here but skip them.
        if ref.startswith("//"):
            continue
        p = ROOT / ref
        if not p.exists():
            broken.append(ref)
    if broken:
        for b in broken:
            add_result(results, "FAIL", b, "broken local reference in index.html")
        failures.extend([f"broken local reference: {b}" for b in broken])
    else:
        add_result(results, "OK", "index.html references", "no broken local src/href references detected")

    # 4. Central states
    for state in CENTRAL_STATES:
        in_index = f'data-global-state="{state}"' in html or f"data-global-state='{state}'" in html
        if in_index:
            add_result(results, "OK", f"central state {state}", "present in index.html")
        else:
            add_result(results, "FAIL", f"central state {state}", "missing in index.html")
            failures.append(f"central state missing: {state}")

    # 5. BW refs
    for ref in EXPECTED_BW_REFS:
        if ref in html:
            add_result(results, "OK", ref, "BW map PNG referenced by index.html")
        else:
            add_result(results, "FAIL", ref, "BW map PNG not referenced by index.html")
            failures.append(f"BW map reference missing: {ref}")

    # 6. Retired sections
    for section_id, expected_retire in RETIRED_SECTIONS.items():
        tag = section_open_tag(html, section_id)
        if not tag:
            add_result(results, "FAIL", f"#{section_id}", "section tag missing")
            failures.append(f"retired section tag missing: {section_id}")
            continue
        required_tokens = ["is-retired", "hidden", 'aria-hidden="true"', f'data-retired="{expected_retire}"', "display: none"]
        missing = [tok for tok in required_tokens if tok not in tag]
        if missing:
            add_result(results, "FAIL", f"#{section_id}", f"retirement markers missing: {missing}")
            failures.append(f"retired section {section_id} missing markers: {missing}")
        else:
            add_result(results, "OK", f"#{section_id}", f"retired/hidden with {expected_retire}")

    # 7. Lower grouping
    for section_id in LOWER_GROUPS:
        tag = section_open_tag(html, section_id)
        if tag:
            add_result(results, "OK", f"#{section_id}", "lower evidence grouping section present")
        else:
            add_result(results, "FAIL", f"#{section_id}", "lower evidence grouping section missing")
            failures.append(f"lower evidence grouping missing: {section_id}")

    # 8. Script tags
    scripts = script_refs(html)
    for s in ACTIVE_SCRIPT_REFS:
        if s in scripts:
            add_result(results, "OK", s, "active script tag present")
        else:
            add_result(results, "FAIL", s, "active script tag missing from index.html")
            failures.append(f"active script tag missing: {s}")

    for s in FORBIDDEN_ACTIVE_SCRIPT_TAGS:
        if s in scripts:
            add_result(results, "FAIL", s, "retired guidedStory script tag still active")
            failures.append(f"retired guidedStory script tag still active: {s}")
        else:
            add_result(results, "OK", s, "retired guidedStory script tag absent")

    # 9. CSS markers
    css_markers = [
        "B68 MVP storyline lock",
        "B68b compact storyline bridge",
        "B70 central story readability pass",
        "B71 lower evidence reframing",
    ]
    for marker in css_markers:
        if marker in css:
            add_result(results, "OK", f"CSS marker: {marker}", "present in src/styles.css")
        else:
            add_result(results, "WARN", f"CSS marker: {marker}", "not found in src/styles.css")
            warnings.append(f"CSS marker not found: {marker}")

    # 10. Git hygiene
    status = git_status_short()
    for prefix in RAW_DATA_WARNING_PREFIXES:
        if prefix in status:
            add_result(results, "WARN", prefix.strip(), "raw-data/GIS-like path visible in git status")
            warnings.append(f"{prefix.strip()} visible in git status")

    if failures:
        result_label = "FAIL"
    elif warnings:
        result_label = "PASS WITH WARNINGS"
    else:
        result_label = "PASS"

    result_lines = "\n".join(f"- {status_:4} `{item}` — {note}" for status_, item, note in results)

    report = f"""# B72 - Public MVP Quality Report

Date: {date.today().isoformat()}

## Result

**{result_label}**

## 1. Summary

B72 checks the current MVP page state after the story-flow and evidence-module restructuring.

It explicitly checks:

- global, Europe, Germany and BW PNG map assets,
- central story controller scripts,
- all 11 central sticky-map states,
- retired legacy sections,
- lower evidence grouping sections,
- active and retired script tags,
- local broken references,
- known raw-data/git hygiene warnings.

## 2. Check results

{result_lines}

## 3. Failures

{chr(10).join(f"- {f}" for f in failures) if failures else "- none"}

## 4. Warnings

{chr(10).join(f"- {w}" for w in warnings) if warnings else "- none"}

## 5. Manual public-site check

After committing and pushing B72, open:

```text
https://chrisbran.github.io/peatland-transition-atlas/?v=b72
```

Check manually:

1. No Six-part story visible.
2. No old guidedStory visible.
3. Main atlas story bridge visible.
4. Central 11-step map story works.
5. Interpretation / Supporting evidence / Prototype appendix grouping visible.
6. Old BW interactive prototype layer not visible.
7. No obvious public/local mismatch after hard refresh.

## 6. Git status at B72 runtime

```text
{status.strip()}
```
"""
    write(REPORT, report)

    doc = f"""# B72 - Public MVP Quality Pass

Date: {date.today().isoformat()}

## 1. Purpose

B72 freezes the current page as a reviewable MVP prototype and adds a stricter QA report for the current story architecture.

The MVP structure is:

1. Hero / problem statement.
2. Transition logic.
3. Main atlas story bridge.
4. Central PNG sticky-map story.
5. Interpretation.
6. Supporting evidence.
7. Prototype appendix.

## 2. Created files

- `docs/B72_public_mvp_quality_pass.md`
- `docs/B72_public_mvp_quality_report.md`

## 3. What B72 checks

B72 checks:

- BW PNGs in addition to global, Europe and Germany PNGs,
- all 11 central map states,
- retired legacy sections:
  - `#guidedStory`
  - `#story`
  - `#bwPeatLayer`
- lower evidence grouping:
  - `#interpretationIntro`
  - `#supportingEvidenceGroupIntro`
  - `#prototypeAppendixIntro`
- retired guidedStory scripts are no longer active,
- no broken local references in `index.html`.

## 4. What B72 does not do

B72 does not change application behavior. It does not:

- alter `index.html`,
- alter `src/styles.css`,
- alter central story JS,
- delete or move files,
- remove script tags,
- change map layers.

## 5. Current B72 result

`{result_label}`

See:

- `docs/B72_public_mvp_quality_report.md`

## 6. Next recommended step

Recommended B73:

`B73_mvp_copy_and_source_polish`

Scope:

- polish hero and section copy,
- check source wording,
- add a clear prototype/disclaimer sentence near the footer,
- no new functionality,
- no additional cleanup.
"""
    write(DOC, doc)

    done_entry = f"""
## B72 - Public MVP quality pass ({date.today().isoformat()})

- Created `docs/B72_public_mvp_quality_pass.md`.
- Created `docs/B72_public_mvp_quality_report.md`.
- Checked BW PNGs, central 11-step map states, retired legacy sections and lower evidence grouping.
- Did not change application behavior, CSS, scripts, data files, images or map assets.
- Result: {result_label}.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B72 - Public MVP quality pass" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B72 public MVP quality pass complete.")
    print(f"Result: {result_label}")
    if failures:
        print("Failures:")
        for f in failures:
            print(f"  - {f}")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")
    print("Changed/created:")
    print(f"  {rel(DOC)}")
    print(f"  {rel(REPORT)}")
    print(f"  {rel(DONE)}")

if __name__ == "__main__":
    main()
