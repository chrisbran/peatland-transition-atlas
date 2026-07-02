from pathlib import Path
from datetime import date
import re
import struct
import subprocess

ROOT = Path(".")
REPORT = ROOT / "docs" / "B58_visual_qa_and_commit_check.md"

BASE_REQUIRED_PNGS = [
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

B169_REQUIRED_PNGS = [
    "public/maps/bw/bw_bk50_moor_extent.png",
    "public/maps/bw/bw_admin_context.png",
    "public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png",
]

LEGACY_CENTRAL_SCRIPTS = [
    "src/central_global_map_story.js",
    "src/central_layer_state_hardener.js",
    "src/central_step_state_bridge.js",
    "src/central_stage_label_fix.js",
]

B169_SCRIPT = "src/b169_live_sticky_zoom.js"

LEGACY_STATES = [
    "global-peat",
    "global-pressure",
    "europe-peat",
    "germany-thuenen-extent",
    "germany-thuenen-types",
]

B169_STATES = [
    "global-peat",
    "global-pressure-total",
    "global-pressure-density",
    "europe-bridge",
    "germany-extent",
    "germany-types",
    "baden-wuerttemberg",
    "oberschwaben-handoff",
]

UNWANTED_REFS = [
    "germany_thuenen_legend_fix.js",
    "B53_germany_thuenen_distinction_and_legend_fix",
    "EUROPE_FRAME_V1.png",
]

RAW_DATA_PATTERNS = [
    r"(^|[\\/])working[\\/]",
    r"(^|[\\/])data[\\/]working[\\/]",
    r"(^|[\\/])data[\\/]external[\\/]",
    r"(^|[\\/])sources[\\/]",
    r"\.gdb($|[\\/])",
    r"\.gpkg$",
    r"\.shp$",
    r"\.geojson$",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def png_info(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing"

    try:
        with path.open("rb") as f:
            sig = f.read(8)
            if sig != b"\x89PNG\r\n\x1a\n":
                return False, "not a PNG signature"

            length = struct.unpack(">I", f.read(4))[0]
            chunk = f.read(4)
            if chunk != b"IHDR" or length != 13:
                return False, "IHDR not found"

            data = f.read(13)
            width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", data)
            color = {
                0: "grayscale",
                2: "RGB",
                3: "indexed",
                4: "grayscale+alpha",
                6: "RGBA",
            }.get(color_type, f"color_type={color_type}")

            return True, f"PNG header {color} ({width}, {height}) bit_depth={bit_depth}"
    except Exception as exc:
        return False, f"read error: {exc}"


def local_refs_from_index(index: str) -> list[str]:
    refs = []
    for attr in ["src", "href"]:
        for m in re.finditer(attr + r'\s*=\s*"([^"]+)"', index, flags=re.I):
            refs.append(m.group(1))
        for m in re.finditer(attr + r"\s*=\s*'([^']+)'", index, flags=re.I):
            refs.append(m.group(1))

    local = []
    for ref in refs:
        if not ref:
            continue
        if ref.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")):
            continue
        if ref.startswith("//") or ref.startswith("javascript:"):
            continue
        clean = ref.split("#", 1)[0].split("?", 1)[0]
        if clean:
            local.append(clean)
    return sorted(set(local))


def git_status() -> list[str]:
    try:
        out = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True, stderr=subprocess.STDOUT)
        return [line.rstrip() for line in out.splitlines() if line.strip()]
    except Exception as exc:
        return [f"ERROR reading git status: {exc}"]


def is_staged(line: str) -> bool:
    return len(line) >= 2 and line[0] not in (" ", "?")


def extract_path_from_status(line: str) -> str:
    if len(line) <= 3:
        return line.strip()
    payload = line[3:].strip()
    if " -> " in payload:
        payload = payload.split(" -> ", 1)[1]
    return payload.strip('"')


def raw_data_staged(status_lines: list[str]) -> list[str]:
    hits = []
    for line in status_lines:
        if not is_staged(line):
            continue
        path = extract_path_from_status(line).replace("\\", "/")
        for pattern in RAW_DATA_PATTERNS:
            if re.search(pattern, path, flags=re.I):
                hits.append(line)
                break
    return hits


def main() -> None:
    today = date.today().isoformat()
    index = read_text(ROOT / "index.html")
    b169_mode = "B169_LIVE_STICKY_ZOOM_START" in index or B169_SCRIPT in index

    required_pngs = list(BASE_REQUIRED_PNGS)
    if b169_mode:
        required_pngs.extend(B169_REQUIRED_PNGS)

    required_scripts = [B169_SCRIPT] if b169_mode else list(LEGACY_CENTRAL_SCRIPTS)
    active_states = list(B169_STATES) if b169_mode else list(LEGACY_STATES)

    script_texts = {rel: read_text(ROOT / rel) for rel in required_scripts}
    all_active_script_text = "\n".join(script_texts.values())

    failures = []
    report = []
    report.append("# B58 - Visual QA and Commit Check\n")
    report.append(f"Date: {today}\n")
    report.append("## 0. Active map-story mode\n")
    report.append(f"- {'OK' if b169_mode else 'INFO'} active mode: {'B169 live sticky zoom' if b169_mode else 'legacy central map story'}")
    if b169_mode:
        report.append("- INFO legacy central map-story source files may still exist in `src/`, but they are not treated as active wiring unless referenced by `index.html`.\n")
    else:
        report.append("")

    report.append("## 1. Required map PNGs\n")
    for rel in required_pngs:
        ok, info = png_info(ROOT / rel)
        if ok:
            report.append(f"- OK `{rel}` — {info}")
        else:
            report.append(f"- FAIL `{rel}` — {info}")
            failures.append(f"Missing or invalid map PNG: {rel} ({info})")
    report.append("")

    report.append("## 2. Required map-story scripts\n")
    for rel in required_scripts:
        exists = (ROOT / rel).exists()
        if exists:
            report.append(f"- OK `{rel}`")
        else:
            report.append(f"- FAIL `{rel}`")
            failures.append(f"Missing required script: {rel}")

    if b169_mode:
        legacy_refs = [rel for rel in LEGACY_CENTRAL_SCRIPTS if rel in index]
        if legacy_refs:
            for rel in legacy_refs:
                report.append(f"- FAIL legacy script still referenced in index: `{rel}`")
                failures.append(f"Legacy central map-story script still referenced: {rel}")
        else:
            report.append("- OK no legacy central map-story scripts referenced by `index.html`")
    report.append("")

    report.append("## 3. index.html reference check\n")
    broken_refs = []
    for ref in local_refs_from_index(index):
        if ref.endswith("/"):
            continue
        path = ROOT / ref
        if not path.exists():
            broken_refs.append(ref)
    if broken_refs:
        for ref in broken_refs:
            report.append(f"- FAIL broken local reference: `{ref}`")
            failures.append(f"Broken local reference in index.html: {ref}")
    else:
        report.append("- OK no broken local script/image references detected")
    report.append("")

    report.append("## 4. Active map-story states\n")
    for state in active_states:
        index_has = state in index
        scripts_have = state in all_active_script_text if all_active_script_text else True
        if index_has and scripts_have:
            report.append(f"- OK `{state}` — index=True, scripts=True")
        else:
            report.append(f"- FAIL `{state}` — index={index_has}, scripts={scripts_have}")
            failures.append(f"State not fully wired: {state} (index={index_has}, scripts={scripts_have})")
    report.append("")

    report.append("## 5. Unwanted reference check\n")
    active_text = index + "\n" + all_active_script_text
    for token in UNWANTED_REFS:
        if token in active_text:
            report.append(f"- FAIL `{token}` found in active files")
            failures.append(f"Unwanted reference found: {token}")
        else:
            report.append(f"- OK `{token}` not found in active files")
    report.append("")

    report.append("## 6. Git status / commit hygiene\n")
    status = git_status()
    raw_hits = raw_data_staged(status)
    if raw_hits:
        report.append("- FAIL staged raw-data/GIS-like files detected")
        for line in raw_hits:
            report.append(f"  - `{line}`")
            failures.append(f"Staged raw-data/GIS file: {line}")
    else:
        report.append("- OK no obvious staged raw-data/GIS files visible in git status")

    report.append("\n### Current changed/untracked files\n")
    if status:
        for line in status:
            report.append(f"- `{line}`")
    else:
        report.append("- clean working tree")
    report.append("")

    report.append("## 7. Suggested add list for this milestone\n")
    suggested = [
        "index.html",
        "src/styles.css",
        "src/b169_live_sticky_zoom.js",
        "public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png",
        "scripts/58_visual_qa_and_commit_check.py",
        "tasks/done.md",
    ]
    for rel in suggested:
        if (ROOT / rel).exists():
            report.append(f"- `{rel}`")
    report.append("")

    report.append("## Result\n")
    if failures:
        report.append("FAIL — fix the issues below before committing.\n")
        for failure in failures:
            report.append(f"- {failure}")
        result = "FAIL"
    else:
        report.append("PASS")
        result = "PASS"

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8", newline="\n")

    print("B58 visual QA and commit check complete.")
    print(f"Report written to {REPORT.as_posix()}")
    print("")
    print(f"RESULT: {result}")
    for failure in failures:
        print(f" - {failure}")


if __name__ == "__main__":
    main()
