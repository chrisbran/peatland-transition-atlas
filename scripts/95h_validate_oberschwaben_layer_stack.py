#!/usr/bin/env python3
"""
B95h - Validate Oberschwaben scrolly layer-stack assets

Context:
- B95 originally expected one composite PNG:
  public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
- The project decision changed: Oberschwaben should be implemented as a scrollable
  layer stack, consistent with the existing Global/Europe/Germany/BW map story.
- Therefore the required public assets are now separate, co-registered PNG layers.

Required layer-stack assets:
- public/maps/oberschwaben/oberschwaben_admin_context.png
- public/maps/oberschwaben/oberschwaben_agriculture.png
- public/maps/oberschwaben/oberschwaben_moor_context.png
- public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png

Optional:
- public/maps/oberschwaben/oberschwaben_landuse_classes_on_moor.png
- public/maps/oberschwaben/oberschwaben_implementation_context_composite.png

Outputs:
- docs/B95h_oberschwaben_layer_stack_qa.md
- docs/B95h_oberschwaben_layer_stack_manifest.csv
- tasks/B96_bind_oberschwaben_scrolly_layer_stack.md
- tasks/done.md

Does not modify:
- index.html
- src/styles.css
- JavaScript
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import csv
import struct


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REPORT = DOCS / "B95h_oberschwaben_layer_stack_qa.md"
MANIFEST = DOCS / "B95h_oberschwaben_layer_stack_manifest.csv"
TASK_B96 = TASKS / "B96_bind_oberschwaben_scrolly_layer_stack.md"

REQUIRED = [
    {
        "file": "public/maps/oberschwaben/oberschwaben_admin_context.png",
        "role": "admin context",
        "expected": "Landkreisgrenzen und Landkreisnamen; should normally be visible above thematic layers.",
        "alpha_recommended": "optional",
    },
    {
        "file": "public/maps/oberschwaben/oberschwaben_agriculture.png",
        "role": "agriculture layer",
        "expected": "FIONA 2024 Ackerland / Grünland / Dauerkultur; no admin labels baked in.",
        "alpha_recommended": "yes",
    },
    {
        "file": "public/maps/oberschwaben/oberschwaben_moor_context.png",
        "role": "moor/wetland soil context",
        "expected": "BK50 Moor-/Feuchtbodenkontext; no admin labels baked in.",
        "alpha_recommended": "yes",
    },
    {
        "file": "public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png",
        "role": "intersection layer",
        "expected": "Schnittmenge: Nutzung × Bodenkontext; no admin labels baked in.",
        "alpha_recommended": "yes",
    },
]

OPTIONAL = [
    {
        "file": "public/maps/oberschwaben/oberschwaben_landuse_classes_on_moor.png",
        "role": "optional interpretive layer",
        "expected": "Schnittmenge nach Ackerland / Grünland / Dauerkultur.",
        "alpha_recommended": "yes",
    },
    {
        "file": "public/maps/oberschwaben/oberschwaben_implementation_context_composite.png",
        "role": "optional composite fallback",
        "expected": "Static fallback/composite, not required for scrolly layer-stack.",
        "alpha_recommended": "no",
    },
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def png_info(path: Path) -> dict:
    try:
        data = path.read_bytes()
        if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
            return {"ok": False, "reason": "not a PNG"}

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
            "has_alpha_channel": color_type in {4, 6},
        }
    except Exception as exc:
        return {"ok": False, "reason": str(exc)}


def check_assets() -> tuple[str, list[str], list[str], list[dict]]:
    failures = []
    warnings = []
    rows = []
    sizes = []

    for required, item in [(True, a) for a in REQUIRED] + [(False, a) for a in OPTIONAL]:
        path = ROOT / item["file"]
        row = {
            "file": item["file"],
            "required": "yes" if required else "no",
            "exists": "no",
            "role": item["role"],
            "expected": item["expected"],
            "size": "",
            "png_mode": "",
            "alpha_channel": "",
            "alpha_recommended": item["alpha_recommended"],
            "status": "",
        }

        if not path.exists():
            row["status"] = "FAIL missing" if required else "optional missing"
            if required:
                failures.append(f"Missing required layer asset: `{item['file']}`")
            rows.append(row)
            continue

        row["exists"] = "yes"
        info = png_info(path)
        if not info.get("ok"):
            reason = info.get("reason", "unknown")
            row["status"] = f"invalid: {reason}"
            if required:
                failures.append(f"Invalid PNG: `{item['file']}` ({reason})")
            else:
                warnings.append(f"Optional PNG invalid: `{item['file']}` ({reason})")
            rows.append(row)
            continue

        size = (info["width"], info["height"])
        if required:
            sizes.append(size)

        row["size"] = f"{info['width']}x{info['height']}"
        row["png_mode"] = info["color_name"]
        row["alpha_channel"] = "yes" if info["has_alpha_channel"] else "no"
        row["status"] = "OK"

        if size != (1600, 900):
            msg = f"`{item['file']}` expected 1600x900, got {size[0]}x{size[1]}"
            if required:
                failures.append(msg)
                row["status"] = "FAIL size"
            else:
                warnings.append(msg)
                row["status"] = "WARN size"

        if item["alpha_recommended"] == "yes" and not info["has_alpha_channel"]:
            warnings.append(
                f"`{item['file']}` has no alpha channel. For a true web layer-stack, transparent thematic PNGs are strongly recommended."
            )

        rows.append(row)

    if len(set(sizes)) > 1:
        failures.append(f"Required layer PNGs are not co-registered by size: {sorted(set(sizes))}")

    result = "PASS" if not failures else "FAIL"
    if result == "PASS" and warnings:
        result = "PASS WITH WARNINGS"

    return result, failures, warnings, rows


def write_manifest(rows: list[dict]) -> None:
    fields = [
        "file",
        "required",
        "exists",
        "role",
        "expected",
        "size",
        "png_mode",
        "alpha_channel",
        "alpha_recommended",
        "status",
    ]
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    result, failures, warnings, rows = check_assets()
    write_manifest(rows)

    md = []
    md.append(f"# B95h - Oberschwaben Scrolly Layer-Stack QA\n\nDate: {today}\n")
    md.append("## Result\n")
    md.append(f"**{result}**\n")

    md.append("## Required layer-stack assets\n")
    for item in REQUIRED:
        md.append(f"- `{item['file']}` — {item['role']}: {item['expected']}")
    md.append("")

    md.append("## Optional assets\n")
    for item in OPTIONAL:
        md.append(f"- `{item['file']}` — {item['role']}: {item['expected']}")
    md.append("")

    md.append("## Failures\n")
    md.append("\n".join(f"- {f}" for f in failures) if failures else "- none")
    md.append("")

    md.append("## Warnings\n")
    md.append("\n".join(f"- {w}" for w in warnings) if warnings else "- none")
    md.append("")

    md.append("## Layer-stack interpretation\n")
    md.append(
        "The Oberschwaben module should be implemented as a scrollable layer stack, not as a static publication-style map. "
        "The admin context layer should remain visible above the thematic layers. The agriculture, moor-context and intersection layers "
        "should be faded in/out by scroll state."
    )
    md.append("")

    md.append("## Recommended state sequence\n")
    md.append("1. `region` — admin context only")
    md.append("2. `agriculture` — agriculture + admin")
    md.append("3. `moor-context` — agriculture + moor context + admin")
    md.append("4. `intersection` — intersection emphasized + context layers dimmed + admin")
    md.append("5. `method-boundary` — intersection remains visible; method boundary text visible")
    md.append("")

    md.append("## Manifest\n")
    md.append(f"- `{rel(MANIFEST)}`")

    write_text(REPORT, "\n".join(md) + "\n")

    b96 = f"""# B96 - Bind Oberschwaben Scrolly Layer Stack

Created from B95h on {today}

## Goal

Implement an Oberschwaben scrollable layer-stack module in the German presentation page.

## Required assets

- `public/maps/oberschwaben/oberschwaben_admin_context.png`
- `public/maps/oberschwaben/oberschwaben_agriculture.png`
- `public/maps/oberschwaben/oberschwaben_moor_context.png`
- `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png`

## Section concept

Working title:

```text
Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird
```

## State sequence

1. Region: Landkreisrahmen + Namen.
2. Landwirtschaft: Ackerland, Grünland, Dauerkultur.
3. Bodenkontext: BK50 Moor-/Feuchtbodenkontext.
4. Schnittmenge: Nutzung × Bodenkontext.
5. Methodische Grenze: räumliche Einordnung, keine Eignungs- oder Prioritätskarte.

## Implementation requirements

- Use a sticky map stage with stacked PNG layers.
- Keep `oberschwaben_admin_context.png` on top in all states.
- Do not use the static composite map as the primary module.
- Do not call the intersection Wiedervernässungspotenzial.
- Do not imply farm-level affectedness.
- Keep the method boundary visible.

## Method boundary text

```text
Die Karte zeigt eine räumliche Einordnung der Überschneidung von landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext. Sie ersetzt keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```
"""
    write_text(TASK_B96, b96)

    done_entry = f"""
## B95h - Validate Oberschwaben scrolly layer-stack assets ({today})

- Validated Oberschwaben scrolly layer-stack PNG assets.
- Created `docs/B95h_oberschwaben_layer_stack_qa.md`.
- Created `docs/B95h_oberschwaben_layer_stack_manifest.csv`.
- Created `tasks/B96_bind_oberschwaben_scrolly_layer_stack.md`.
- Updated the Oberschwaben implementation direction from static composite map to scrollable layer stack.
"""
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    if "## B95h - Validate Oberschwaben scrolly layer-stack assets" not in current:
        write_text(DONE, current.rstrip() + "\n" + done_entry)

    print("B95h Oberschwaben scrolly layer-stack QA complete.")
    print(f"Result: {result}")
    if failures:
        print("Failures:")
        for f in failures:
            print(f"  - {f}")
    if warnings:
        print("Warnings:")
        for w in warnings[:20]:
            print(f"  - {w}")
    print("Changed/created:")
    for p in [REPORT, MANIFEST, TASK_B96, DONE]:
        print(f"  {rel(p)}")


if __name__ == "__main__":
    main()
