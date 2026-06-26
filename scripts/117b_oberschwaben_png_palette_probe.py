#!/usr/bin/env python3
"""
B117b - Oberschwaben PNG palette probe

Purpose
-------
Inspect the current Oberschwaben PNG map assets before changing legend colours.

This is a diagnostic-only step:
- reads PNG files with Python stdlib only (no Pillow dependency);
- reports dimensions, colour type, opaque-pixel counts and dominant colours;
- separates all dominant colours from more saturated candidate thematic colours;
- scans index.html and src/styles.css for visible HEX colour values;
- creates a basis for deciding whether the Oberschwaben maps need re-export or
  whether HTML/CSS legend changes are sufficient.

Changed:
- docs/B117b_oberschwaben_png_palette_probe.md
- docs/B117b_oberschwaben_png_color_summary.csv
- docs/B117b_oberschwaben_png_top_colors.csv
- docs/B117b_oberschwaben_html_css_color_scan.csv
- docs/B117b_oberschwaben_png_palette_audit.txt
- tasks/done.md

Not changed:
- index.html
- src/styles.css
- public/maps/*
- data/*
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import binascii
import csv
import math
import re
import struct
import sys
import zlib


ROOT = Path(__file__).resolve().parents[1]
MAP_DIR = ROOT / "public" / "maps" / "oberschwaben"
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REPORT = DOCS / "B117b_oberschwaben_png_palette_probe.md"
SUMMARY_CSV = DOCS / "B117b_oberschwaben_png_color_summary.csv"
TOP_COLORS_CSV = DOCS / "B117b_oberschwaben_png_top_colors.csv"
HTML_CSS_COLORS_CSV = DOCS / "B117b_oberschwaben_html_css_color_scan.csv"
AUDIT = DOCS / "B117b_oberschwaben_png_palette_audit.txt"

TODAY = date.today().isoformat()

PNG_FILES = [
    "oberschwaben_admin_context.png",
    "oberschwaben_agriculture.png",
    "oberschwaben_moor_context.png",
    "oberschwaben_agriculture_moor_intersection.png",
]

TARGET_PALETTE = {
    "Ackerland": "#C76E3F",
    "Grünland": "#5F8F4A",
    "Dauerkultur / Sondernutzung": "#8C5A9E",
    "Moor-/Feuchtbodenkontext": "#4E7FA6",
    "Schnittmenge": "#043B36",
}


@dataclass
class PngImage:
    width: int
    height: int
    color_type: int
    bit_depth: int
    pixels: list[tuple[int, int, int, int]]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def parse_png(path: Path) -> PngImage:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")

    pos = 8
    width = height = bit_depth = color_type = None
    idat_parts: list[bytes] = []
    palette: list[tuple[int, int, int]] = []
    transparency: dict[int, int] = {}

    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        chunk_data = data[pos + 8:pos + 8 + length]
        crc_read = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        crc_calc = binascii.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if crc_read != crc_calc:
            raise ValueError(f"CRC mismatch in {chunk_type!r}")
        pos += 12 + length

        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", chunk_data)
            if compression != 0 or filter_method != 0:
                raise ValueError("unsupported PNG compression/filter method")
            if interlace != 0:
                raise ValueError("interlaced PNG not supported by this lightweight reader")
            if bit_depth != 8:
                raise ValueError(f"unsupported bit depth {bit_depth}; expected 8")
        elif chunk_type == b"PLTE":
            palette = [
                tuple(chunk_data[i:i + 3])  # type: ignore[arg-type]
                for i in range(0, len(chunk_data), 3)
            ]
        elif chunk_type == b"tRNS":
            transparency = {i: alpha for i, alpha in enumerate(chunk_data)}
        elif chunk_type == b"IDAT":
            idat_parts.append(chunk_data)
        elif chunk_type == b"IEND":
            break

    if width is None or height is None or bit_depth is None or color_type is None:
        raise ValueError("missing IHDR")

    channels_by_type = {
        0: 1,  # grayscale
        2: 3,  # RGB
        3: 1,  # indexed
        4: 2,  # grayscale alpha
        6: 4,  # RGBA
    }
    if color_type not in channels_by_type:
        raise ValueError(f"unsupported color type {color_type}")

    channels = channels_by_type[color_type]
    bpp = channels
    stride = width * channels

    raw = zlib.decompress(b"".join(idat_parts))
    expected = height * (1 + stride)
    if len(raw) < expected:
        raise ValueError(f"decompressed stream shorter than expected: {len(raw)} < {expected}")

    rows: list[bytearray] = []
    offset = 0
    prev = bytearray(stride)

    for _y in range(height):
        filter_type = raw[offset]
        offset += 1
        scan = bytearray(raw[offset:offset + stride])
        offset += stride
        recon = bytearray(stride)

        for i in range(stride):
            left = recon[i - bpp] if i >= bpp else 0
            up = prev[i]
            up_left = prev[i - bpp] if i >= bpp else 0

            if filter_type == 0:
                val = scan[i]
            elif filter_type == 1:
                val = (scan[i] + left) & 0xFF
            elif filter_type == 2:
                val = (scan[i] + up) & 0xFF
            elif filter_type == 3:
                val = (scan[i] + ((left + up) // 2)) & 0xFF
            elif filter_type == 4:
                val = (scan[i] + paeth(left, up, up_left)) & 0xFF
            else:
                raise ValueError(f"unsupported PNG filter {filter_type}")

            recon[i] = val

        rows.append(recon)
        prev = recon

    pixels: list[tuple[int, int, int, int]] = []

    for row in rows:
        if color_type == 0:
            for i in range(0, len(row), 1):
                g = row[i]
                pixels.append((g, g, g, 255))
        elif color_type == 2:
            for i in range(0, len(row), 3):
                r, g, b = row[i], row[i + 1], row[i + 2]
                pixels.append((r, g, b, 255))
        elif color_type == 3:
            for i in range(0, len(row), 1):
                idx = row[i]
                if idx >= len(palette):
                    r, g, b = (0, 0, 0)
                else:
                    r, g, b = palette[idx]
                a = transparency.get(idx, 255)
                pixels.append((r, g, b, a))
        elif color_type == 4:
            for i in range(0, len(row), 2):
                g, a = row[i], row[i + 1]
                pixels.append((g, g, g, a))
        elif color_type == 6:
            for i in range(0, len(row), 4):
                r, g, b, a = row[i], row[i + 1], row[i + 2], row[i + 3]
                pixels.append((r, g, b, a))

    return PngImage(width=width, height=height, color_type=color_type, bit_depth=bit_depth, pixels=pixels)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def quantize_rgb(rgb: tuple[int, int, int], step: int = 16) -> tuple[int, int, int]:
    return tuple(max(0, min(255, int(round(v / step) * step))) for v in rgb)  # type: ignore[return-value]


def saturation_and_value(rgb: tuple[int, int, int]) -> tuple[float, float]:
    r, g, b = [v / 255.0 for v in rgb]
    mx = max(r, g, b)
    mn = min(r, g, b)
    sat = 0.0 if mx == 0 else (mx - mn) / mx
    return sat, mx


def color_distance(a: str, b: str) -> float:
    def parse(x: str) -> tuple[int, int, int]:
        x = x.strip().lstrip("#")
        return int(x[0:2], 16), int(x[2:4], 16), int(x[4:6], 16)
    ar, ag, ab = parse(a)
    br, bg, bb = parse(b)
    return math.sqrt((ar - br) ** 2 + (ag - bg) ** 2 + (ab - bb) ** 2)


def analyze_png(path: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    img = parse_png(path)
    opaque = [(r, g, b) for r, g, b, a in img.pixels if a >= 8]
    opaque_count = len(opaque)
    total_count = len(img.pixels)

    exact_counter = Counter(opaque)
    quant_counter = Counter(quantize_rgb(rgb, 16) for rgb in opaque)

    saturated = []
    for rgb in opaque:
        sat, val = saturation_and_value(rgb)
        # Keep potential thematic colours, not near black/white/gray background.
        if sat >= 0.18 and 0.12 <= val <= 0.95:
            saturated.append(quantize_rgb(rgb, 16))
    sat_counter = Counter(saturated)

    summary = {
        "file": path.name,
        "width": img.width,
        "height": img.height,
        "color_type": img.color_type,
        "bit_depth": img.bit_depth,
        "total_pixels": total_count,
        "opaque_pixels": opaque_count,
        "unique_exact_rgb": len(exact_counter),
        "unique_quantized_rgb": len(quant_counter),
        "saturated_candidate_pixels": len(saturated),
        "unique_saturated_quantized_rgb": len(sat_counter),
    }

    rows: list[dict[str, object]] = []

    for rank, (rgb, count) in enumerate(exact_counter.most_common(20), start=1):
        hx = rgb_to_hex(rgb)
        rows.append({
            "file": path.name,
            "group": "exact_top",
            "rank": rank,
            "hex": hx,
            "r": rgb[0],
            "g": rgb[1],
            "b": rgb[2],
            "count": count,
            "pct_opaque": round((count / opaque_count * 100) if opaque_count else 0, 4),
            "nearest_target_class": nearest_target(hx)[0],
            "nearest_target_distance": round(nearest_target(hx)[1], 2),
        })

    for rank, (rgb, count) in enumerate(quant_counter.most_common(30), start=1):
        hx = rgb_to_hex(rgb)
        rows.append({
            "file": path.name,
            "group": "quantized_top",
            "rank": rank,
            "hex": hx,
            "r": rgb[0],
            "g": rgb[1],
            "b": rgb[2],
            "count": count,
            "pct_opaque": round((count / opaque_count * 100) if opaque_count else 0, 4),
            "nearest_target_class": nearest_target(hx)[0],
            "nearest_target_distance": round(nearest_target(hx)[1], 2),
        })

    for rank, (rgb, count) in enumerate(sat_counter.most_common(30), start=1):
        hx = rgb_to_hex(rgb)
        rows.append({
            "file": path.name,
            "group": "saturated_candidate_quantized",
            "rank": rank,
            "hex": hx,
            "r": rgb[0],
            "g": rgb[1],
            "b": rgb[2],
            "count": count,
            "pct_opaque": round((count / opaque_count * 100) if opaque_count else 0, 4),
            "nearest_target_class": nearest_target(hx)[0],
            "nearest_target_distance": round(nearest_target(hx)[1], 2),
        })

    return summary, rows


def nearest_target(hex_color: str) -> tuple[str, float]:
    if not TARGET_PALETTE:
        return "", 0.0
    best_class = ""
    best_dist = 1e9
    for cls, target in TARGET_PALETTE.items():
        d = color_distance(hex_color, target)
        if d < best_dist:
            best_class = cls
            best_dist = d
    return best_class, best_dist


def scan_html_css_colors() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    pattern = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b")
    for path in [INDEX, CSS]:
        if not path.exists():
            continue
        text = read_text(path)
        for m in pattern.finditer(text):
            color = m.group(0)
            line_no = text.count("\n", 0, m.start()) + 1
            context_start = max(0, m.start() - 80)
            context_end = min(len(text), m.end() + 80)
            context = re.sub(r"\s+", " ", text[context_start:context_end]).strip()
            rows.append({
                "file": rel(path),
                "line": line_no,
                "hex": color.upper(),
                "nearest_target_class": nearest_target(color)[0],
                "nearest_target_distance": round(nearest_target(color)[1], 2),
                "context": context,
            })
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(summaries: list[dict[str, object]], top_rows: list[dict[str, object]], html_rows: list[dict[str, object]], errors: list[str]) -> None:
    status = "OK" if summaries and not errors else "REVIEW REQUIRED"

    lines = [
        "# B117b – Oberschwaben PNG Palette Probe",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Zweck",
        "",
        "B117b prüft die aktuellen Oberschwaben-PNGs, bevor Farben oder Legenden verändert werden. "
        "Die Analyse ändert keine Karten und keine Website-Dateien.",
        "",
        "## Geprüfte PNG-Dateien",
        "",
        "| Datei | Breite | Höhe | Farbtyp | Opaque Pixel | Exakte RGB-Farben | Sättigungs-Kandidaten |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for s in summaries:
        lines.append(
            f"| `{s['file']}` | {s['width']} | {s['height']} | {s['color_type']} | "
            f"{s['opaque_pixels']} | {s['unique_exact_rgb']} | {s['unique_saturated_quantized_rgb']} |"
        )

    lines.extend([
        "",
        "## Zielpalette aus B117",
        "",
        "| Klasse | Ziel-Hex |",
        "|---|---|",
    ])
    for cls, hx in TARGET_PALETTE.items():
        lines.append(f"| {cls} | `{hx}` |")

    lines.extend([
        "",
        "## Interpretation",
        "",
        "Die PNGs enthalten durch Antialiasing, Labels, Hintergrund und Transparenz viele Farbwerte. "
        "Deshalb erzeugt B117b drei Gruppen:",
        "",
        "- `exact_top`: häufigste exakte RGB-Werte;",
        "- `quantized_top`: auf 16er-Schritte gerundete dominante Farbbins;",
        "- `saturated_candidate_quantized`: stärker gesättigte Farbbins als Kandidaten für thematische Klassen.",
        "",
        "Für die Oberschwaben-Legende sind vor allem die `saturated_candidate_quantized`-Zeilen relevant.",
        "",
        "## Ergebnisdateien",
        "",
        f"- `{rel(SUMMARY_CSV)}`",
        f"- `{rel(TOP_COLORS_CSV)}`",
        f"- `{rel(HTML_CSS_COLORS_CSV)}`",
        f"- `{rel(AUDIT)}`",
        "",
        "## Empfehlung",
        "",
        "Nächster Schritt ist kein blindes HTML-Recoloring. Entscheide anhand der Palette-Probe, ob die Oberschwaben-Karten neu exportiert werden müssen. "
        "Wenn ja: Karte und Legende gemeinsam aktualisieren.",
        "",
    ])

    if errors:
        lines.extend(["## Fehler", ""])
        for e in errors:
            lines.append(f"- {e}")

    write_text(REPORT, "\n".join(lines))


def write_audit(summaries: list[dict[str, object]], errors: list[str]) -> None:
    status = "OK" if summaries and not errors else "REVIEW REQUIRED"
    lines = [
        "# B117b PNG palette audit",
        "",
        f"- Status: {status}",
        f"- PNG files expected: {len(PNG_FILES)}",
        f"- PNG files analysed: {len(summaries)}",
        f"- Errors: {len(errors)}",
        "",
    ]

    if errors:
        lines.append("## Errors")
        for e in errors:
            lines.append(f"- {e}")
        lines.append("")

    lines.extend([
        "## Recommended review commands",
        "",
        "```powershell",
        "Import-Csv docs\\B117b_oberschwaben_png_color_summary.csv -Delimiter ';' | Format-Table -Auto",
        "Import-Csv docs\\B117b_oberschwaben_png_top_colors.csv -Delimiter ';' | Where-Object {$_.group -eq 'saturated_candidate_quantized'} | Format-Table -Auto",
        "Import-Csv docs\\B117b_oberschwaben_html_css_color_scan.csv -Delimiter ';' | Format-Table -Auto",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "```",
        "",
    ])
    write_text(AUDIT, "\n".join(lines))


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B117b - Oberschwaben PNG palette probe"
    if marker in current:
        return
    entry = f"""
## B117b - Oberschwaben PNG palette probe ({TODAY})

- Analysed current Oberschwaben PNG files with a stdlib-only PNG reader.
- Exported dominant exact, quantized and saturated candidate colours.
- Scanned index.html and src/styles.css for HEX colours near the B117 target palette.
- Did not modify maps, CSS, index.html or data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    summaries: list[dict[str, object]] = []
    top_rows: list[dict[str, object]] = []
    errors: list[str] = []

    if not MAP_DIR.exists():
        errors.append(f"Missing directory: {rel(MAP_DIR)}")
    else:
        for name in PNG_FILES:
            path = MAP_DIR / name
            if not path.exists():
                errors.append(f"Missing PNG: {rel(path)}")
                continue
            try:
                summary, rows = analyze_png(path)
                summaries.append(summary)
                top_rows.extend(rows)
            except Exception as exc:
                errors.append(f"{rel(path)}: {exc}")

    html_rows = scan_html_css_colors()

    write_csv(
        SUMMARY_CSV,
        summaries,
        [
            "file", "width", "height", "color_type", "bit_depth", "total_pixels",
            "opaque_pixels", "unique_exact_rgb", "unique_quantized_rgb",
            "saturated_candidate_pixels", "unique_saturated_quantized_rgb",
        ],
    )

    write_csv(
        TOP_COLORS_CSV,
        top_rows,
        [
            "file", "group", "rank", "hex", "r", "g", "b", "count", "pct_opaque",
            "nearest_target_class", "nearest_target_distance",
        ],
    )

    write_csv(
        HTML_CSS_COLORS_CSV,
        html_rows,
        ["file", "line", "hex", "nearest_target_class", "nearest_target_distance", "context"],
    )

    write_report(summaries, top_rows, html_rows, errors)
    write_audit(summaries, errors)
    update_done()

    print("B117b Oberschwaben PNG palette probe complete.")
    print("Changed/created:")
    for p in [REPORT, SUMMARY_CSV, TOP_COLORS_CSV, HTML_CSS_COLORS_CSV, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print(f"PNG files analysed: {len(summaries)}")
    print(f"Errors: {len(errors)}")
    print("")
    print("Review:")
    print("  Import-Csv docs\\B117b_oberschwaben_png_color_summary.csv -Delimiter ';' | Format-Table -Auto")
    print("  Import-Csv docs\\B117b_oberschwaben_png_top_colors.csv -Delimiter ';' | Where-Object {$_.group -eq 'saturated_candidate_quantized'} | Format-Table -Auto")
    print("  Get-Content docs\\B117b_oberschwaben_png_palette_audit.txt")


if __name__ == "__main__":
    main()
