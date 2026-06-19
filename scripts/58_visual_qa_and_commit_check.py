#!/usr/bin/env python3
r"""
58 - Visual QA and commit check.

Run from repository root:
  python scripts\58_visual_qa_and_commit_check.py

Purpose:
- Check required map PNGs exist and are RGBA 1600 x 900.
- Check script references in index.html are not broken.
- Check core central-story states exist.
- Warn about files that should not be committed.
- Write a QA report to docs/B58_visual_qa_and_commit_check.md.
"""

from pathlib import Path
from datetime import date
import re
import subprocess
import sys

TODAY = date.today().isoformat()

REQUIRED_MAP_IMAGES = [
    "public/maps/global/global_gpm2_peat_extent.png",
    "public/maps/global/global_hotspots_total.png",
    "public/maps/global/global_hotspots_density.png",
    "public/maps/global/global_country_borders.png",
    "public/maps/europe/europe_gpm2_peat_extent.png",
    "public/maps/europe/europe_country_borders.png",
    "public/maps/germany/germany_admin_context.png",
    "public/maps/germany/germany_thuenen_moor_extent.png",
    "public/maps/germany/germany_thuenen_moor_types.png",
]

REQUIRED_SCRIPT_FILES = [
    "src/central_global_map_story.js",
    "src/central_layer_state_hardener.js",
    "src/central_step_state_bridge.js",
    "src/central_stage_label_fix.js",
]

REQUIRED_STATES = [
    "europe-borders",
    "europe-peat",
    "germany-context",
    "germany-thuenen-extent",
    "germany-thuenen-types",
]

FORBIDDEN_PATTERNS = [
    "data/external/",
    ".tif",
    ".tiff",
    ".gdb",
    ".shp",
    ".shx",
    ".dbf",
    ".prj",
    ".cpg",
    ".lock",
]

UNWANTED_REFERENCES = [
    "germany_thuenen_legend_fix.js",
    "B53_germany_thuenen_distinction_and_legend_fix",
    "EUROPE_FRAME_V1.png",
]

def read(path):
    return path.read_text(encoding="utf-8")

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def run_git(args):
    try:
        return subprocess.run(
            ["git"] + args,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except Exception as exc:
        return None

def png_header_check(path):
    """Return (status, detail) for PNG dimensions/RGBA using only stdlib."""
    try:
        with open(path, "rb") as f:
            sig = f.read(8)
            if sig != b"\x89PNG\r\n\x1a\n":
                return ("FAIL", "not a PNG file")
            length = int.from_bytes(f.read(4), "big")
            chunk_type = f.read(4)
            if chunk_type != b"IHDR" or length < 13:
                return ("FAIL", "PNG IHDR chunk not found")
            data = f.read(13)
            width = int.from_bytes(data[0:4], "big")
            height = int.from_bytes(data[4:8], "big")
            bit_depth = data[8]
            color_type = data[9]
            # PNG color type 6 = truecolor with alpha, equivalent to RGBA export.
            if (width, height) != (1600, 900):
                return ("FAIL", f"PNG header size=({width}, {height}), expected (1600, 900)")
            if color_type != 6:
                return ("FAIL", f"PNG header color_type={color_type}, expected 6/RGBA")
            return ("OK", f"PNG header RGBA ({width}, {height}) bit_depth={bit_depth}")
    except Exception as exc:
        return ("FAIL", f"Could not read PNG header: {exc}")

def image_check(path):
    """Check image dimensions and alpha; use Pillow if available, stdlib PNG check otherwise."""
    try:
        from PIL import Image
        try:
            with Image.open(path) as img:
                mode = img.mode
                size = img.size
                alpha = None
                if mode == "RGBA":
                    alpha = img.getchannel("A").getextrema()
                if size != (1600, 900):
                    return ("FAIL", f"{mode} {size}, expected (1600, 900)")
                if mode != "RGBA":
                    return ("FAIL", f"{mode} {size}, expected RGBA")
                return ("OK", f"{mode} {size} alpha={alpha}")
        except Exception as exc:
            return ("FAIL", f"Could not open image with Pillow: {exc}")
    except ImportError:
        return png_header_check(path)

def collect_index_refs(index_text):
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', index_text)
    images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', index_text)
    return scripts, images

def is_forbidden_path(path):
    p = path.replace("\\", "/")
    lower = p.lower()
    if lower.startswith("data/external/"):
        return True
    return any(lower.endswith(pattern) for pattern in FORBIDDEN_PATTERNS if pattern.startswith("."))

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    report_lines = []
    failures = []
    warnings = []

    report_lines.append(f"# B58 - Visual QA and Commit Check")
    report_lines.append("")
    report_lines.append(f"Date: {TODAY}")
    report_lines.append("")

    index_path = root / "index.html"
    index_text = read(index_path)

    # 1. Required map image checks
    report_lines.append("## 1. Required map PNGs")
    report_lines.append("")
    for rel in REQUIRED_MAP_IMAGES:
        path = root / rel
        if not path.exists():
            failures.append(f"Missing required map image: {rel}")
            report_lines.append(f"- FAIL `{rel}` — missing")
            continue
        status, detail = image_check(path)
        if status != "OK":
            failures.append(f"{rel}: {detail}")
        report_lines.append(f"- {status} `{rel}` — {detail}")
    report_lines.append("")

    # 2. Required script files
    report_lines.append("## 2. Required central-story scripts")
    report_lines.append("")
    for rel in REQUIRED_SCRIPT_FILES:
        path = root / rel
        if path.exists():
            report_lines.append(f"- OK `{rel}`")
        else:
            failures.append(f"Missing required script file: {rel}")
            report_lines.append(f"- FAIL `{rel}` — missing")
    report_lines.append("")

    # 3. Script/image references from index.html
    scripts, images = collect_index_refs(index_text)

    report_lines.append("## 3. index.html reference check")
    report_lines.append("")
    for src in scripts:
        if src.startswith(("http://", "https://", "//")):
            continue
        rel = src.split("?", 1)[0]
        if not (root / rel).exists():
            failures.append(f"Broken script reference in index.html: {src}")
            report_lines.append(f"- FAIL script `{src}` — file not found")
    for src in images:
        if src.startswith(("http://", "https://", "//")):
            continue
        rel = src.split("?", 1)[0]
        if not (root / rel).exists():
            failures.append(f"Broken image reference in index.html: {src}")
            report_lines.append(f"- FAIL image `{src}` — file not found")
    if not any(line.startswith("- FAIL") for line in report_lines[-(len(scripts)+len(images)+5):]):
        report_lines.append("- OK no broken local script/image references detected")
    report_lines.append("")

    # 4. Central story states
    report_lines.append("## 4. Central story states")
    report_lines.append("")
    for state in REQUIRED_STATES:
        in_index = f'data-global-state="{state}"' in index_text
        in_scripts = False
        for rel in ["src/central_step_state_bridge.js", "src/central_layer_state_hardener.js", "src/central_global_map_story.js"]:
            p = root / rel
            if p.exists() and state in read(p):
                in_scripts = True
                break
        if in_index and in_scripts:
            report_lines.append(f"- OK `{state}`")
        else:
            failures.append(f"State not fully wired: {state} (index={in_index}, scripts={in_scripts})")
            report_lines.append(f"- FAIL `{state}` — index={in_index}, scripts={in_scripts}")
    report_lines.append("")

    # 5. Unwanted references
    report_lines.append("## 5. Unwanted reference check")
    report_lines.append("")
    for token in UNWANTED_REFERENCES:
        found_in = []
        for rel in ["index.html", "src/styles.css", "src/central_step_state_bridge.js", "src/central_layer_state_hardener.js", "src/central_global_map_story.js"]:
            p = root / rel
            if p.exists() and token in read(p):
                found_in.append(rel)
        if found_in:
            warnings.append(f"Unwanted reference `{token}` found in {', '.join(found_in)}")
            report_lines.append(f"- WARN `{token}` found in {', '.join(found_in)}")
        else:
            report_lines.append(f"- OK `{token}` not found in active files")
    report_lines.append("")

    # 6. Git status warnings
    report_lines.append("## 6. Git status / commit hygiene")
    report_lines.append("")
    git = run_git(["status", "--short"])
    if git is None:
        warnings.append("Could not run git status.")
        report_lines.append("- WARN could not run `git status --short`")
    else:
        status_lines = [line.rstrip() for line in git.stdout.splitlines() if line.strip()]
        forbidden_status = []
        for line in status_lines:
            # status format e.g. " M index.html" or "?? data/external/"
            path = line[3:] if len(line) > 3 else line
            if is_forbidden_path(path):
                forbidden_status.append(line)
        if forbidden_status:
            warnings.append("Forbidden/raw-data-like files are visible in git status.")
            report_lines.append("- WARN raw-data/GIS-like files visible in git status:")
            for line in forbidden_status[:60]:
                report_lines.append(f"  - `{line}`")
            if len(forbidden_status) > 60:
                report_lines.append(f"  - ... {len(forbidden_status) - 60} more")
        else:
            report_lines.append("- OK no obvious raw-data/GIS files visible in git status")

        report_lines.append("")
        report_lines.append("### Current changed/untracked files")
        report_lines.append("")
        for line in status_lines[:160]:
            report_lines.append(f"- `{line}`")
        if len(status_lines) > 160:
            report_lines.append(f"- ... {len(status_lines) - 160} more")
    report_lines.append("")

    # 7. Suggested commit list
    report_lines.append("## 7. Suggested add list for this milestone")
    report_lines.append("")
    suggested = [
        "index.html",
        "src/styles.css",
        "src/central_global_map_story.js",
        "src/central_layer_state_hardener.js",
        "src/central_step_state_bridge.js",
        "src/central_stage_label_fix.js",
        "public/maps/germany/README.md",
        "public/maps/germany/germany_admin_context.png",
        "public/maps/germany/germany_thuenen_moor_extent.png",
        "public/maps/germany/germany_thuenen_moor_types.png",
        "scripts/48_prepare_germany_thuenen_frame_workflow.py",
        "scripts/50_fix_germany_state_binding.py",
        "scripts/51_add_hard_central_layer_controller.py",
        "scripts/52_add_central_step_state_bridge.py",
        "scripts/54_restore_original_thuenen_legend_colors.py",
        "scripts/55_fix_thuenen_legend_inline_swatches.py",
        "scripts/56_fix_central_stage_label.py",
        "scripts/57_refine_germany_thuenen_story_text.py",
        "docs/B19c_germany_thuenen_frame_workflow.md",
        "docs/B50_fix_germany_state_binding.md",
        "docs/B51_hard_central_map_layer_controller.md",
        "docs/B52_central_step_state_bridge.md",
        "docs/B54_restore_original_thuenen_legend_colors.md",
        "docs/B55_fix_thuenen_legend_inline_swatches.md",
        "docs/B56_fix_central_map_stage_label.md",
        "docs/B57_refine_germany_thuenen_story_text.md",
        "tasks/done.md",
    ]
    for rel in suggested:
        if (root / rel).exists():
            report_lines.append(f"- `{rel}`")
    report_lines.append("")

    if failures:
        report_lines.append("## Result")
        report_lines.append("")
        report_lines.append("FAIL — fix the issues below before committing.")
        report_lines.append("")
        for item in failures:
            report_lines.append(f"- {item}")
    elif warnings:
        report_lines.append("## Result")
        report_lines.append("")
        report_lines.append("PASS WITH WARNINGS — review warnings before committing.")
        report_lines.append("")
        for item in warnings:
            report_lines.append(f"- {item}")
    else:
        report_lines.append("## Result")
        report_lines.append("")
        report_lines.append("PASS — no blocking QA issues detected.")

    report = "\n".join(report_lines) + "\n"
    write(root / "docs" / "B58_visual_qa_and_commit_check.md", report)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B58 completed" not in done_text:
        done_text += f"- {TODAY}: Task B58 completed - ran visual QA and commit hygiene check.\n"
        write(done, done_text)

    print("B58 visual QA and commit check complete.")
    print("Report written to docs/B58_visual_qa_and_commit_check.md")
    print()
    if failures:
        print("RESULT: FAIL")
        for item in failures:
            print(" -", item)
        sys.exit(1)
    if warnings:
        print("RESULT: PASS WITH WARNINGS")
        for item in warnings:
            print(" -", item)
        sys.exit(0)
    print("RESULT: PASS")

if __name__ == "__main__":
    main()
