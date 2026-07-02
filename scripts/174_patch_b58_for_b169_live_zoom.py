from pathlib import Path
from datetime import date

ROOT = Path(".")
B58 = ROOT / "scripts" / "58_visual_qa_and_commit_check.py"
DOC = ROOT / "docs" / "B174_patch_b58_for_b169_live_zoom.md"
AUDIT = ROOT / "docs" / "B174_patch_b58_for_b169_live_zoom_audit.txt"
DONE = ROOT / "tasks" / "done.md"

NEW_B58 = 'from pathlib import Path\nfrom datetime import date\nimport re\nimport struct\nimport subprocess\n\nROOT = Path(".")\nREPORT = ROOT / "docs" / "B58_visual_qa_and_commit_check.md"\n\nBASE_REQUIRED_PNGS = [\n    "public/maps/global/global_gpm2_peat_extent.png",\n    "public/maps/global/global_hotspots_total.png",\n    "public/maps/global/global_hotspots_density.png",\n    "public/maps/global/global_country_borders.png",\n    "public/maps/europe/europe_gpm2_peat_extent.png",\n    "public/maps/europe/europe_country_borders.png",\n    "public/maps/germany/germany_admin_context.png",\n    "public/maps/germany/germany_thuenen_moor_extent.png",\n    "public/maps/germany/germany_thuenen_moor_types.png",\n]\n\nB169_REQUIRED_PNGS = [\n    "public/maps/bw/bw_bk50_moor_extent.png",\n    "public/maps/bw/bw_admin_context.png",\n    "public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png",\n]\n\nLEGACY_CENTRAL_SCRIPTS = [\n    "src/central_global_map_story.js",\n    "src/central_layer_state_hardener.js",\n    "src/central_step_state_bridge.js",\n    "src/central_stage_label_fix.js",\n]\n\nB169_SCRIPT = "src/b169_live_sticky_zoom.js"\n\nLEGACY_STATES = [\n    "global-peat",\n    "global-pressure",\n    "europe-peat",\n    "germany-thuenen-extent",\n    "germany-thuenen-types",\n]\n\nB169_STATES = [\n    "global-peat",\n    "global-pressure-total",\n    "global-pressure-density",\n    "europe-bridge",\n    "germany-extent",\n    "germany-types",\n    "baden-wuerttemberg",\n    "oberschwaben-handoff",\n]\n\nUNWANTED_REFS = [\n    "germany_thuenen_legend_fix.js",\n    "B53_germany_thuenen_distinction_and_legend_fix",\n    "EUROPE_FRAME_V1.png",\n]\n\nRAW_DATA_PATTERNS = [\n    r"(^|[\\\\/])working[\\\\/]",\n    r"(^|[\\\\/])data[\\\\/]working[\\\\/]",\n    r"(^|[\\\\/])data[\\\\/]external[\\\\/]",\n    r"(^|[\\\\/])sources[\\\\/]",\n    r"\\.gdb($|[\\\\/])",\n    r"\\.gpkg$",\n    r"\\.shp$",\n    r"\\.geojson$",\n]\n\n\ndef read_text(path: Path) -> str:\n    return path.read_text(encoding="utf-8") if path.exists() else ""\n\n\ndef png_info(path: Path) -> tuple[bool, str]:\n    if not path.exists():\n        return False, "missing"\n\n    try:\n        with path.open("rb") as f:\n            sig = f.read(8)\n            if sig != b"\\x89PNG\\r\\n\\x1a\\n":\n                return False, "not a PNG signature"\n\n            length = struct.unpack(">I", f.read(4))[0]\n            chunk = f.read(4)\n            if chunk != b"IHDR" or length != 13:\n                return False, "IHDR not found"\n\n            data = f.read(13)\n            width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", data)\n            color = {\n                0: "grayscale",\n                2: "RGB",\n                3: "indexed",\n                4: "grayscale+alpha",\n                6: "RGBA",\n            }.get(color_type, f"color_type={color_type}")\n\n            return True, f"PNG header {color} ({width}, {height}) bit_depth={bit_depth}"\n    except Exception as exc:\n        return False, f"read error: {exc}"\n\n\ndef local_refs_from_index(index: str) -> list[str]:\n    refs = []\n    for attr in ["src", "href"]:\n        for m in re.finditer(attr + r\'\\s*=\\s*"([^"]+)"\', index, flags=re.I):\n            refs.append(m.group(1))\n        for m in re.finditer(attr + r"\\s*=\\s*\'([^\']+)\'", index, flags=re.I):\n            refs.append(m.group(1))\n\n    local = []\n    for ref in refs:\n        if not ref:\n            continue\n        if ref.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")):\n            continue\n        if ref.startswith("//") or ref.startswith("javascript:"):\n            continue\n        clean = ref.split("#", 1)[0].split("?", 1)[0]\n        if clean:\n            local.append(clean)\n    return sorted(set(local))\n\n\ndef git_status() -> list[str]:\n    try:\n        out = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True, stderr=subprocess.STDOUT)\n        return [line.rstrip() for line in out.splitlines() if line.strip()]\n    except Exception as exc:\n        return [f"ERROR reading git status: {exc}"]\n\n\ndef is_staged(line: str) -> bool:\n    return len(line) >= 2 and line[0] not in (" ", "?")\n\n\ndef extract_path_from_status(line: str) -> str:\n    if len(line) <= 3:\n        return line.strip()\n    payload = line[3:].strip()\n    if " -> " in payload:\n        payload = payload.split(" -> ", 1)[1]\n    return payload.strip(\'"\')\n\n\ndef raw_data_staged(status_lines: list[str]) -> list[str]:\n    hits = []\n    for line in status_lines:\n        if not is_staged(line):\n            continue\n        path = extract_path_from_status(line).replace("\\\\", "/")\n        for pattern in RAW_DATA_PATTERNS:\n            if re.search(pattern, path, flags=re.I):\n                hits.append(line)\n                break\n    return hits\n\n\ndef main() -> None:\n    today = date.today().isoformat()\n    index = read_text(ROOT / "index.html")\n    b169_mode = "B169_LIVE_STICKY_ZOOM_START" in index or B169_SCRIPT in index\n\n    required_pngs = list(BASE_REQUIRED_PNGS)\n    if b169_mode:\n        required_pngs.extend(B169_REQUIRED_PNGS)\n\n    required_scripts = [B169_SCRIPT] if b169_mode else list(LEGACY_CENTRAL_SCRIPTS)\n    active_states = list(B169_STATES) if b169_mode else list(LEGACY_STATES)\n\n    script_texts = {rel: read_text(ROOT / rel) for rel in required_scripts}\n    all_active_script_text = "\\n".join(script_texts.values())\n\n    failures = []\n    report = []\n    report.append("# B58 - Visual QA and Commit Check\\n")\n    report.append(f"Date: {today}\\n")\n    report.append("## 0. Active map-story mode\\n")\n    report.append(f"- {\'OK\' if b169_mode else \'INFO\'} active mode: {\'B169 live sticky zoom\' if b169_mode else \'legacy central map story\'}")\n    if b169_mode:\n        report.append("- INFO legacy central map-story source files may still exist in `src/`, but they are not treated as active wiring unless referenced by `index.html`.\\n")\n    else:\n        report.append("")\n\n    report.append("## 1. Required map PNGs\\n")\n    for rel in required_pngs:\n        ok, info = png_info(ROOT / rel)\n        if ok:\n            report.append(f"- OK `{rel}` — {info}")\n        else:\n            report.append(f"- FAIL `{rel}` — {info}")\n            failures.append(f"Missing or invalid map PNG: {rel} ({info})")\n    report.append("")\n\n    report.append("## 2. Required map-story scripts\\n")\n    for rel in required_scripts:\n        exists = (ROOT / rel).exists()\n        if exists:\n            report.append(f"- OK `{rel}`")\n        else:\n            report.append(f"- FAIL `{rel}`")\n            failures.append(f"Missing required script: {rel}")\n\n    if b169_mode:\n        legacy_refs = [rel for rel in LEGACY_CENTRAL_SCRIPTS if rel in index]\n        if legacy_refs:\n            for rel in legacy_refs:\n                report.append(f"- FAIL legacy script still referenced in index: `{rel}`")\n                failures.append(f"Legacy central map-story script still referenced: {rel}")\n        else:\n            report.append("- OK no legacy central map-story scripts referenced by `index.html`")\n    report.append("")\n\n    report.append("## 3. index.html reference check\\n")\n    broken_refs = []\n    for ref in local_refs_from_index(index):\n        if ref.endswith("/"):\n            continue\n        path = ROOT / ref\n        if not path.exists():\n            broken_refs.append(ref)\n    if broken_refs:\n        for ref in broken_refs:\n            report.append(f"- FAIL broken local reference: `{ref}`")\n            failures.append(f"Broken local reference in index.html: {ref}")\n    else:\n        report.append("- OK no broken local script/image references detected")\n    report.append("")\n\n    report.append("## 4. Active map-story states\\n")\n    for state in active_states:\n        index_has = state in index\n        scripts_have = state in all_active_script_text if all_active_script_text else True\n        if index_has and scripts_have:\n            report.append(f"- OK `{state}` — index=True, scripts=True")\n        else:\n            report.append(f"- FAIL `{state}` — index={index_has}, scripts={scripts_have}")\n            failures.append(f"State not fully wired: {state} (index={index_has}, scripts={scripts_have})")\n    report.append("")\n\n    report.append("## 5. Unwanted reference check\\n")\n    active_text = index + "\\n" + all_active_script_text\n    for token in UNWANTED_REFS:\n        if token in active_text:\n            report.append(f"- FAIL `{token}` found in active files")\n            failures.append(f"Unwanted reference found: {token}")\n        else:\n            report.append(f"- OK `{token}` not found in active files")\n    report.append("")\n\n    report.append("## 6. Git status / commit hygiene\\n")\n    status = git_status()\n    raw_hits = raw_data_staged(status)\n    if raw_hits:\n        report.append("- FAIL staged raw-data/GIS-like files detected")\n        for line in raw_hits:\n            report.append(f"  - `{line}`")\n            failures.append(f"Staged raw-data/GIS file: {line}")\n    else:\n        report.append("- OK no obvious staged raw-data/GIS files visible in git status")\n\n    report.append("\\n### Current changed/untracked files\\n")\n    if status:\n        for line in status:\n            report.append(f"- `{line}`")\n    else:\n        report.append("- clean working tree")\n    report.append("")\n\n    report.append("## 7. Suggested add list for this milestone\\n")\n    suggested = [\n        "index.html",\n        "src/styles.css",\n        "src/b169_live_sticky_zoom.js",\n        "public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png",\n        "scripts/58_visual_qa_and_commit_check.py",\n        "tasks/done.md",\n    ]\n    for rel in suggested:\n        if (ROOT / rel).exists():\n            report.append(f"- `{rel}`")\n    report.append("")\n\n    report.append("## Result\\n")\n    if failures:\n        report.append("FAIL — fix the issues below before committing.\\n")\n        for failure in failures:\n            report.append(f"- {failure}")\n        result = "FAIL"\n    else:\n        report.append("PASS")\n        result = "PASS"\n\n    REPORT.parent.mkdir(parents=True, exist_ok=True)\n    REPORT.write_text("\\n".join(report) + "\\n", encoding="utf-8", newline="\\n")\n\n    print("B58 visual QA and commit check complete.")\n    print(f"Report written to {REPORT.as_posix()}")\n    print("")\n    print(f"RESULT: {result}")\n    for failure in failures:\n        print(f" - {failure}")\n\n\nif __name__ == "__main__":\n    main()\n'


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done(done_text: str, today: str) -> str:
    line = f"- B174 patch B58 for B169 live zoom: updated the visual QA script so the new B169 live sticky-zoom state matrix is treated as active and legacy central-map states no longer fail after replacement ({today})."
    if "B174 patch B58 for B169 live zoom" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not B58.exists():
        raise SystemExit("scripts/58_visual_qa_and_commit_check.py not found")

    old = read(B58)
    old_had_legacy_states = all(token in old for token in ["europe-peat", "germany-thuenen-extent", "germany-thuenen-types"])
    old_had_b169 = "B169_LIVE_STICKY_ZOOM_START" in old or "b169_live_sticky_zoom.js" in old

    write(B58, NEW_B58)

    doc = f"""# B174 - Patch B58 for B169 Live Zoom

Date: {today}

## Ziel

Nach B169 bis B172 ist die alte zentrale Kartenstory durch den neuen Live-Sticky-Zoom ersetzt.
B58 prüfte aber noch die alten zentralen States:

```text
europe-peat
germany-thuenen-extent
germany-thuenen-types
```

Diese States sind in `index.html` nach der B169-Integration bewusst nicht mehr aktiv.
Deshalb war der B58-FAIL ein veralteter QA-Check, kein aktueller Seitenfehler.

## Änderung

`scripts/58_visual_qa_and_commit_check.py` wurde aktualisiert.

Der neue B58 erkennt automatisch:

```text
B169 live sticky zoom
```

wenn in `index.html` einer dieser Marker vorhanden ist:

```text
B169_LIVE_STICKY_ZOOM_START
src/b169_live_sticky_zoom.js
```

Dann prüft B58 die aktive B169-State-Matrix:

```text
global-peat
global-pressure-total
global-pressure-density
europe-bridge
germany-extent
germany-types
baden-wuerttemberg
oberschwaben-handoff
```

und behandelt alte zentrale Map-Story-Scripts nur noch dann als aktiv, wenn sie weiterhin in `index.html` referenziert sind.

## Zusätzlich geprüft

Im B169-Modus prüft B58 jetzt auch:

```text
public/maps/bw/bw_bk50_moor_extent.png
public/maps/bw/bw_admin_context.png
public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png
```

## Nicht geändert

- keine öffentliche Seite
- keine CSS-Regeln
- keine Kartenassets
- keine Datenquellen
- keine raw GIS-Dateien

## Nächster Schritt

```powershell
python scripts\\58_visual_qa_and_commit_check.py
```

Erwartung:

```text
RESULT: PASS
```
"""
    write(DOC, doc)

    new = read(B58)
    audit = f"""# B174 patch B58 for B169 live zoom audit

Date: {today}

Old B58 contained legacy retired states: {old_had_legacy_states}
Old B58 already contained B169 detection: {old_had_b169}

Post-patch checks:
- B169 marker detection in B58: {'B169_LIVE_STICKY_ZOOM_START' in new}
- B169 script check in B58: {'b169_live_sticky_zoom.js' in new}
- B169 states in B58: {all(s in new for s in ['global-pressure-total', 'global-pressure-density', 'baden-wuerttemberg', 'oberschwaben-handoff'])}
- New Oberschwaben no-label map in B58: {'oberschwaben_landkreise_moor_nolabel.png' in new}

Result: PATCH WRITTEN. Rerun B58.
"""
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B174 patched B58 for B169 live zoom.")
    print("Changed:")
    print("  scripts/58_visual_qa_and_commit_check.py")
    print("Created/updated:")
    print("  docs/B174_patch_b58_for_b169_live_zoom.md")
    print("  docs/B174_patch_b58_for_b169_live_zoom_audit.txt")
    print("  tasks/done.md")
    print("Next: python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
