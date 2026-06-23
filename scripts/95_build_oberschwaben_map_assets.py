#!/usr/bin/env python3
"""
B95 - Build Oberschwaben map asset package

Purpose:
- Move from source-stack planning toward actual map-asset production.
- Prepare the Oberschwaben map-asset package, manifest, QA checks and export checklist.
- Scan the repository for likely source/input candidates, but do not use raw data automatically.
- Validate any already-exported Oberschwaben PNG assets if present.
- Create a B96 task for binding the map to the website after visual review.

Outputs:
- public/maps/oberschwaben/oberschwaben_map_sources.json
- docs/B95_build_oberschwaben_map_assets.md
- docs/B95_oberschwaben_asset_manifest.csv
- docs/B95_oberschwaben_source_candidate_scan.txt
- docs/B95_oberschwaben_png_asset_qa.md
- docs/B95_oberschwaben_manual_export_checklist.md
- tasks/B96_bind_oberschwaben_map_section.md
- tasks/done.md

Does NOT:
- modify index.html
- modify src/styles.css
- modify JavaScript
- create fake map images
- copy raw GIS data
- infer hectares or indicators without source data
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import csv
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

OBER_DIR = ROOT / "public" / "maps" / "oberschwaben"
SOURCES_JSON = OBER_DIR / "oberschwaben_map_sources.json"

REPORT = DOCS / "B95_build_oberschwaben_map_assets.md"
ASSET_MANIFEST = DOCS / "B95_oberschwaben_asset_manifest.csv"
SOURCE_SCAN = DOCS / "B95_oberschwaben_source_candidate_scan.txt"
PNG_QA = DOCS / "B95_oberschwaben_png_asset_qa.md"
EXPORT_CHECKLIST = DOCS / "B95_oberschwaben_manual_export_checklist.md"
TASK_B96 = TASKS / "B96_bind_oberschwaben_map_section.md"

EXPECTED_ASSETS = [
    {
        "file": "public/maps/oberschwaben/oberschwaben_implementation_context_composite.png",
        "role": "first visible composite",
        "required_for_b96": "yes",
        "expected_size": "1600x900",
        "description": "Composite map: four districts, agriculture, moor/soil context and intersection.",
    },
    {
        "file": "public/maps/oberschwaben/oberschwaben_admin_context.png",
        "role": "stack layer",
        "required_for_b96": "optional",
        "expected_size": "1600x900",
        "description": "Four-district admin context for transparent layer stack.",
    },
    {
        "file": "public/maps/oberschwaben/oberschwaben_agriculture.png",
        "role": "stack layer",
        "required_for_b96": "optional",
        "expected_size": "1600x900",
        "description": "Agricultural land-use context.",
    },
    {
        "file": "public/maps/oberschwaben/oberschwaben_moor_context.png",
        "role": "stack layer",
        "required_for_b96": "optional",
        "expected_size": "1600x900",
        "description": "Moor-/Feuchtbodenkontext.",
    },
    {
        "file": "public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png",
        "role": "stack layer",
        "required_for_b96": "optional",
        "expected_size": "1600x900",
        "description": "Schnittmenge: landwirtschaftliche Nutzung × Moor-/Feuchtbodenkontext.",
    },
    {
        "file": "public/maps/oberschwaben/oberschwaben_landuse_classes_on_moor.png",
        "role": "interpretation layer",
        "required_for_b96": "no",
        "expected_size": "1600x900",
        "description": "Optional use-class split within the intersection.",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def png_info(path: Path):
    try:
        data = path.read_bytes()
        if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
            return {"ok": False, "reason": "not a PNG"}
        # IHDR starts after signature and chunk length/type: offset 16
        width, height = struct.unpack(">II", data[16:24])
        bit_depth = data[24]
        color_type = data[25]
        color_name = {
            0: "grayscale",
            2: "truecolor RGB",
            3: "indexed",
            4: "grayscale+alpha",
            6: "truecolor RGBA",
        }.get(color_type, f"unknown({color_type})")
        return {
            "ok": True,
            "width": width,
            "height": height,
            "bit_depth": bit_depth,
            "color_type": color_type,
            "color_name": color_name,
            "has_alpha": color_type in {4, 6},
        }
    except Exception as exc:
        return {"ok": False, "reason": str(exc)}


def write_asset_manifest() -> None:
    fields = ["file", "exists", "role", "required_for_b96", "expected_size", "actual_size", "png_mode", "description"]
    with ASSET_MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for item in EXPECTED_ASSETS:
            path = ROOT / item["file"]
            info = png_info(path) if path.exists() else None
            if info and info.get("ok"):
                actual_size = f'{info["width"]}x{info["height"]}'
                png_mode = info["color_name"]
            elif path.exists():
                actual_size = "invalid"
                png_mode = info.get("reason", "unknown") if info else "unknown"
            else:
                actual_size = ""
                png_mode = ""
            row = {
                "file": item["file"],
                "exists": "yes" if path.exists() else "no",
                "role": item["role"],
                "required_for_b96": item["required_for_b96"],
                "expected_size": item["expected_size"],
                "actual_size": actual_size,
                "png_mode": png_mode,
                "description": item["description"],
            }
            writer.writerow(row)


def scan_source_candidates() -> list[str]:
    terms = [
        "oberschwaben",
        "ravensburg",
        "biberach",
        "sigmaringen",
        "bodensee",
        "bodenseekreis",
        "gemeinsamer",
        "antrag",
        "mlr",
        "lgrb",
        "bk50",
        "bk50moor",
        "geola",
        "moor",
        "moore",
        "feucht",
        "organic",
        "organic_soil",
        "landwirtschaft",
        "agriculture",
        "acker",
        "gruenland",
        "grünland",
        "dauerkultur",
        "bkg",
        "nuts",
        "admin",
    ]
    suffixes = {
        ".csv", ".geojson", ".json", ".gpkg", ".shp", ".dbf", ".prj", ".tif", ".tiff",
        ".xlsx", ".xls", ".png", ".md", ".txt"
    }
    skip_dirs = {".git", "__pycache__", ".venv", "node_modules"}
    hits = []
    for path in ROOT.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() not in suffixes:
            continue
        name = path.name.lower()
        pstr = rel(path).lower()
        score = sum(1 for t in terms if t in name or t in pstr)
        if score:
            hits.append((score, rel(path)))
    hits.sort(key=lambda x: (-x[0], x[1]))
    return [f"{score:02d}  {p}" for score, p in hits[:250]]


def write_sources_json(today: str) -> None:
    payload = {
        "created_by": "B95_build_oberschwaben_map_assets",
        "date": today,
        "status": "source anchors defined; actual map assets pending unless PNGs are present",
        "focus_area": ["Ravensburg", "Biberach", "Sigmaringen", "Bodenseekreis"],
        "method_boundary": (
            "Die Oberschwaben-Karten zeigen eine räumliche Einordnung der Überschneidung "
            "von landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext. Sie ersetzen "
            "keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche "
            "Betroffenheitsanalyse."
        ),
        "source_anchors": [
            {
                "layer": "agricultural land-use context",
                "reference": "Gemeinsamer Antrag Baden-Württemberg / MLR",
                "year": "2024",
                "status": "access and public-display rights open",
                "expected_classes": ["Ackerland", "Grünland", "Dauerkultur"],
            },
            {
                "layer": "moor/wetland/soil context",
                "reference": "Feuchtgebiete und Moore der Bodenkarte BW / GeoLa BK50MOOR / LGRB",
                "year": "2025",
                "status": "access and public-display rights open",
                "expected_label": "Moor-/Feuchtbodenkontext",
            },
            {
                "layer": "administrative base",
                "reference": "BKG or project-compatible public administrative boundaries",
                "year": "2026/reference year to be confirmed",
                "status": "source to be confirmed",
            },
        ],
        "expected_assets": EXPECTED_ASSETS,
        "do_not_use_labels": [
            "Eignungskarte",
            "Prioritätskarte",
            "Wiedervernässungspotenzial",
            "betroffene Betriebe",
            "Maßnahmenfläche",
            "SOLAMO-Ergebnis",
        ],
    }
    SOURCES_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    OBER_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    source_hits = scan_source_candidates()
    write(SOURCE_SCAN, "B95 source candidate scan\n\n" + "\n".join(source_hits) + "\n")

    write_sources_json(today)
    write_asset_manifest()

    qa_lines = [f"# B95 - Oberschwaben PNG Asset QA\n\nDate: {today}\n"]
    failures = []
    warnings = []
    for item in EXPECTED_ASSETS:
        path = ROOT / item["file"]
        qa_lines.append(f"## `{item['file']}`\n")
        if not path.exists():
            msg = "missing"
            if item["required_for_b96"] == "yes":
                warnings.append(f"{item['file']} missing; B96 should not bind visible map yet")
            qa_lines.append(f"- Status: **missing**\n- Role: {item['role']}\n- Required for B96: {item['required_for_b96']}\n")
            continue
        info = png_info(path)
        if not info.get("ok"):
            failures.append(f"{item['file']}: invalid PNG ({info.get('reason')})")
            qa_lines.append(f"- Status: **invalid PNG**\n- Reason: {info.get('reason')}\n")
            continue
        ok_size = (info["width"], info["height"]) == (1600, 900)
        if not ok_size:
            warnings.append(f"{item['file']}: expected 1600x900, got {info['width']}x{info['height']}")
        qa_lines.append(
            f"- Status: **present**\n"
            f"- Size: {info['width']} x {info['height']}\n"
            f"- Color: {info['color_name']}\n"
            f"- Alpha: {info['has_alpha']}\n"
            f"- Size check: {'OK' if ok_size else 'WARN'}\n"
        )

    result = "PASS" if not failures else "FAIL"
    if result == "PASS" and warnings:
        result = "PASS WITH WARNINGS"

    qa_lines.insert(1, f"## Result\n\n**{result}**\n\n")
    qa_lines.append("## Failures\n\n" + ("\n".join(f"- {f}" for f in failures) if failures else "- none") + "\n")
    qa_lines.append("## Warnings\n\n" + ("\n".join(f"- {w}" for w in warnings) if warnings else "- none") + "\n")
    write(PNG_QA, "\n".join(qa_lines))

    report = f"""# B95 - Build Oberschwaben Map Asset Package

Date: {today}

## 1. Purpose

B95 prepares the asset package for the Oberschwaben implementation map.

It does not create fake map images and does not bind anything to the website.

## 2. Current result

PNG asset QA result:

**{result}**

This result may be `PASS WITH WARNINGS` if the composite map has not yet been exported. That is expected at this stage.

## 3. Main outputs

- `public/maps/oberschwaben/oberschwaben_map_sources.json`
- `docs/B95_oberschwaben_asset_manifest.csv`
- `docs/B95_oberschwaben_source_candidate_scan.txt`
- `docs/B95_oberschwaben_png_asset_qa.md`
- `docs/B95_oberschwaben_manual_export_checklist.md`
- `tasks/B96_bind_oberschwaben_map_section.md`

## 4. Source-anchor logic

B95 uses the B94 source anchors:

- Gemeinsamer Antrag Baden-Württemberg / MLR 2024 for agriculture,
- GeoLa BK50MOOR / LGRB 2025 for Moor-/Feuchtbodenkontext,
- BKG or compatible public administrative boundaries for county context.

## 5. First visible asset needed before website binding

```text
public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
```

Until this file exists and passes visual review, B96 should not bind the module into `index.html`.

## 6. Method boundary

The map package uses this boundary:

```text
Die Oberschwaben-Karten zeigen eine räumliche Einordnung der Überschneidung von landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```

## 7. Candidate source scan

Candidate source-like files were scanned into:

- `docs/B95_oberschwaben_source_candidate_scan.txt`

This is a discovery aid only. It does not mean the files are approved inputs.

## 8. Next step

Export or create the first composite map asset manually or through a dedicated GIS workflow.

Then rerun B95 and proceed to B96 only after:

1. composite PNG exists,
2. source metadata are acceptable,
3. legend wording is approved,
4. visual review passes.
"""
    write(REPORT, report)

    checklist = f"""# B95 - Oberschwaben Manual Export Checklist

Date: {today}

## Goal

Create:

```text
public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
```

## Required visual content

- [ ] Landkreisrahmen: Ravensburg, Biberach, Sigmaringen, Bodenseekreis
- [ ] Agriculture layer: Ackerland / Grünland / Dauerkultur if available
- [ ] Moor-/Feuchtbodenkontext layer
- [ ] Intersection: Nutzung × Bodenkontext
- [ ] Compact legend
- [ ] Source note or source note documented in JSON

## Recommended title

```text
Oberschwaben: Nutzung × Moor-/Feuchtbodenkontext
```

or:

```text
Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird
```

## Required method wording

Do not put too much text inside the map. But the surrounding module or source metadata must state:

```text
Räumliche Einordnung, keine Eignungs- oder Prioritätskarte.
```

## Export settings

- [ ] PNG
- [ ] 1600 x 900 px
- [ ] same visual style as German presentation page
- [ ] no photo basemap
- [ ] no farm-level labels
- [ ] no parcel-owner/farm data
- [ ] no raw GIS files in `public/maps/oberschwaben/`

## Legend wording

Use:

```text
Landkreisrahmen
Ackerland
Grünland
Dauerkultur
Moor-/Feuchtbodenkontext
Schnittmenge: Nutzung × Bodenkontext
```

Avoid:

```text
Wiedervernässungspotenzial
Priorität
Eignung
betroffene Betriebe
Maßnahmenfläche
```

## After export

Run:

```powershell
python scripts\\95_build_oberschwaben_map_assets.py
```

Then inspect:

```powershell
Get-Content docs\\B95_oberschwaben_png_asset_qa.md
```
"""
    write(EXPORT_CHECKLIST, checklist)

    task_b96 = f"""# B96 - Bind Oberschwaben Map Section

Created from B95 on {today}

## Goal

Bind the Oberschwaben implementation map into the German presentation page.

## Do not start until

- [ ] `public/maps/oberschwaben/oberschwaben_implementation_context_composite.png` exists,
- [ ] B95 PNG QA accepts it,
- [ ] visual review is complete,
- [ ] source/legend wording is approved,
- [ ] method boundary is included.

## Expected section

Working section title:

```text
Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird
```

## Intended placement

After central map story and before current `Regionale Umsetzung` cards.

## Content

- short transition paragraph,
- composite map,
- three interpretation cards:
  - Karte zeigt Kontext
  - Daraus entsteht Betroffenheit
  - Daraus folgen Nutzungspfade
- method boundary sentence.

## Do not

- create another scrolly module yet,
- call the map an Eignungskarte,
- call the intersection Wiedervernässungspotenzial,
- imply farm-level affectedness,
- expose raw or restricted data.
"""
    write(TASK_B96, task_b96)

    done_entry = f"""
## B95 - Build Oberschwaben map asset package ({today})

- Created `public/maps/oberschwaben/oberschwaben_map_sources.json`.
- Created `docs/B95_build_oberschwaben_map_assets.md`.
- Created `docs/B95_oberschwaben_asset_manifest.csv`.
- Created `docs/B95_oberschwaben_source_candidate_scan.txt`.
- Created `docs/B95_oberschwaben_png_asset_qa.md`.
- Created `docs/B95_oberschwaben_manual_export_checklist.md`.
- Created `tasks/B96_bind_oberschwaben_map_section.md`.
- Prepared Oberschwaben map asset package and QA without creating fake map images.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B95 - Build Oberschwaben map asset package" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B95 Oberschwaben map asset package complete.")
    print(f"PNG QA result: {result}")
    if warnings:
        print("Warnings:")
        for w in warnings[:10]:
            print(f"  - {w}")
    if failures:
        print("Failures:")
        for f in failures:
            print(f"  - {f}")
    print("Changed/created:")
    for path in [SOURCES_JSON, REPORT, ASSET_MANIFEST, SOURCE_SCAN, PNG_QA, EXPORT_CHECKLIST, TASK_B96, DONE]:
        print(f"  {rel(path)}")


if __name__ == "__main__":
    main()
