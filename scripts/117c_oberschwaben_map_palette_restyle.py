#!/usr/bin/env python3
"""
B117c - Oberschwaben map palette restyle

Purpose
-------
Apply a controlled cartographic palette restyle to the Oberschwaben PNG layer
stack and synchronize the HTML/CSS legend swatches.

This follows B117b's palette probe. B117b showed that:
- the current agriculture PNG uses strong brown/green/purple source colours;
- moor context and intersection are both dark blue/petrol and therefore close;
- the HTML legend swatches are pastel and do not match the PNG colours well.

B117c changes only visual styling of already-derived public PNGs:
- no GIS/data processing
- no geometry changes
- no class/count/area changes
- no source swap
- no LGL reactivation

Changed:
- public/maps/oberschwaben/oberschwaben_agriculture.png
- public/maps/oberschwaben/oberschwaben_moor_context.png
- public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png
- src/styles.css
- docs/B117c_oberschwaben_map_palette_restyle.md
- docs/B117c_oberschwaben_map_palette_audit.txt
- docs/B117c_oberschwaben_recolor_counts.csv
- tasks/done.md

Not changed:
- data/*
- index.html, unless future manual edits are made
- public/maps/oberschwaben/oberschwaben_admin_context.png
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import binascii
import csv
import math
import re
import shutil
import struct
import sys
import zlib


ROOT = Path(__file__).resolve().parents[1]
MAP_DIR = ROOT / "public" / "maps" / "oberschwaben"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b117c_oberschwaben_palette_restyle"

REPORT = DOCS / "B117c_oberschwaben_map_palette_restyle.md"
AUDIT = DOCS / "B117c_oberschwaben_map_palette_audit.txt"
COUNTS_CSV = DOCS / "B117c_oberschwaben_recolor_counts.csv"

TODAY = date.today().isoformat()

TARGET = {
    "acker": "#C76E3F",
    "gruenland": "#5F8F4A",
    "dauerkultur": "#8C5A9E",
    "moor": "#4E7FA6",
    "intersection": "#043B36",
}

# Source anchors from B117b palette probe, used to classify agriculture PNG colours.
SOURCE_ANCHORS = {
    "acker": ["#732500", "#722600", "#712800", "#742300", "#563914", "#504010", "#504020", "#702000"],
    "gruenland": ["#00734D", "#00724C", "#00714F", "#007451", "#206040", "#206030", "#394D28", "#007050"],
    "dauerkultur": ["#B00080", "#A00080", "#A01060", "#B00090", "#802070", "#504070"],
}

FILES = {
    "agriculture": MAP_DIR / "oberschwaben_agriculture.png",
    "moor": MAP_DIR / "oberschwaben_moor_context.png",
    "intersection": MAP_DIR / "oberschwaben_agriculture_moor_intersection.png",
}


@dataclass
class PngImage:
    width: int
    height: int
    pixels: list[tuple[int, int, int, int]]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def parse_hex(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


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


def read_png(path: Path) -> PngImage:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")

    pos = 8
    width = height = None
    bit_depth = color_type = None
    idats: list[bytes] = []
    palette: list[tuple[int, int, int]] = []
    transparency: dict[int, int] = {}

    while pos < len(data):
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
            if bit_depth != 8:
                raise ValueError(f"unsupported bit depth {bit_depth}; expected 8")
            if compression != 0 or filter_method != 0 or interlace != 0:
                raise ValueError("unsupported PNG compression/filter/interlace mode")
        elif chunk_type == b"PLTE":
            palette = [tuple(chunk_data[i:i + 3]) for i in range(0, len(chunk_data), 3)]  # type: ignore[list-item]
        elif chunk_type == b"tRNS":
            transparency = {i: alpha for i, alpha in enumerate(chunk_data)}
        elif chunk_type == b"IDAT":
            idats.append(chunk_data)
        elif chunk_type == b"IEND":
            break

    if width is None or height is None or bit_depth is None or color_type is None:
        raise ValueError("missing IHDR")

    channels_by_type = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
    if color_type not in channels_by_type:
        raise ValueError(f"unsupported color type {color_type}")

    channels = channels_by_type[color_type]
    bpp = channels
    stride = width * channels
    raw = zlib.decompress(b"".join(idats))
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
                raise ValueError(f"unsupported filter {filter_type}")
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
                r, g, b = palette[idx] if idx < len(palette) else (0, 0, 0)
                a = transparency.get(idx, 255)
                pixels.append((r, g, b, a))
        elif color_type == 4:
            for i in range(0, len(row), 2):
                g, a = row[i], row[i + 1]
                pixels.append((g, g, g, a))
        elif color_type == 6:
            for i in range(0, len(row), 4):
                pixels.append((row[i], row[i + 1], row[i + 2], row[i + 3]))

    return PngImage(width=width, height=height, pixels=pixels)


def chunk(chunk_type: bytes, chunk_data: bytes) -> bytes:
    crc = binascii.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
    return struct.pack(">I", len(chunk_data)) + chunk_type + chunk_data + struct.pack(">I", crc)


def write_png_rgba(path: Path, img: PngImage) -> None:
    raw_rows = bytearray()
    i = 0
    for _y in range(img.height):
        raw_rows.append(0)  # no filter
        for _x in range(img.width):
            r, g, b, a = img.pixels[i]
            raw_rows.extend((r, g, b, a))
            i += 1

    ihdr = struct.pack(">IIBBBBB", img.width, img.height, 8, 6, 0, 0, 0)
    data = bytearray()
    data.extend(b"\x89PNG\r\n\x1a\n")
    data.extend(chunk(b"IHDR", ihdr))
    data.extend(chunk(b"IDAT", zlib.compress(bytes(raw_rows), level=9)))
    data.extend(chunk(b"IEND", b""))
    path.write_bytes(bytes(data))


def classify_agriculture(rgb: tuple[int, int, int]) -> str:
    best_cls = "gruenland"
    best_dist = float("inf")
    for cls, anchors in SOURCE_ANCHORS.items():
        for anchor in anchors:
            d = distance(rgb, parse_hex(anchor))
            if d < best_dist:
                best_dist = d
                best_cls = cls
    return best_cls


def recolor_agriculture(path: Path) -> dict[str, int]:
    img = read_png(path)
    counts = Counter()
    new_pixels = []
    target_rgb = {k: parse_hex(v) for k, v in TARGET.items()}

    for r, g, b, a in img.pixels:
        if a < 8:
            new_pixels.append((r, g, b, a))
            counts["transparent_or_near_transparent"] += 1
            continue
        cls = classify_agriculture((r, g, b))
        nr, ng, nb = target_rgb[cls]
        new_pixels.append((nr, ng, nb, a))
        counts[cls] += 1

    img.pixels = new_pixels
    write_png_rgba(path, img)
    return dict(counts)


def recolor_single_class(path: Path, cls: str) -> dict[str, int]:
    img = read_png(path)
    target = parse_hex(TARGET[cls])
    counts = Counter()
    new_pixels = []

    for r, g, b, a in img.pixels:
        if a < 8:
            new_pixels.append((r, g, b, a))
            counts["transparent_or_near_transparent"] += 1
            continue
        new_pixels.append((*target, a))
        counts[cls] += 1

    img.pixels = new_pixels
    write_png_rgba(path, img)
    return dict(counts)


def update_css() -> dict[str, int]:
    if not CSS.exists():
        return {"css_missing": 1}
    css = read_text(CSS)
    original = css

    replacements = {
        r"(\.moore-ob-swatch--acker\s*\{\s*background:\s*)#[0-9a-fA-F]{6}(\s*;\s*\})": rf"\g<1>{TARGET['acker']}\2",
        r"(\.moore-ob-swatch--gruenland\s*\{\s*background:\s*)#[0-9a-fA-F]{6}(\s*;\s*\})": rf"\g<1>{TARGET['gruenland']}\2",
        r"(\.moore-ob-swatch--dauerkultur\s*\{\s*background:\s*)#[0-9a-fA-F]{6}(\s*;\s*\})": rf"\g<1>{TARGET['dauerkultur']}\2",
        r"(\.moore-ob-swatch--moor\s*\{\s*background:\s*)#[0-9a-fA-F]{6}(\s*;\s*\})": rf"\g<1>{TARGET['moor']}\2",
        r"(\.moore-ob-swatch--intersection\s*\{\s*background:\s*)#[0-9a-fA-F]{6}(\s*;\s*\})": rf"\g<1>{TARGET['intersection']}\2",
    }

    counts = {}
    for pat, repl in replacements.items():
        css, n = re.subn(pat, repl, css)
        counts[pat] = n

    override = f"""
/* B117c Oberschwaben palette synchronization */
.moore-ob-swatch--acker {{ background: {TARGET['acker']} !important; }}
.moore-ob-swatch--gruenland {{ background: {TARGET['gruenland']} !important; }}
.moore-ob-swatch--dauerkultur {{ background: {TARGET['dauerkultur']} !important; }}
.moore-ob-swatch--moor {{ background: {TARGET['moor']} !important; }}
.moore-ob-swatch--intersection {{ background: {TARGET['intersection']} !important; }}
.moore-ob-swatch--moor,
.moore-ob-swatch--intersection {{ box-shadow: 0 0 0 1px rgba(255,255,255,.42), 0 0 0 2px rgba(29,36,31,.22); }}
"""

    marker = "/* B117c Oberschwaben palette synchronization */"
    if marker not in css:
        css = css.rstrip() + "\n\n" + override.strip() + "\n"
        counts["override_appended"] = 1
    else:
        counts["override_appended"] = 0

    if css != original:
        write_text(CSS, css)
        counts["css_changed"] = 1
    else:
        counts["css_changed"] = 0

    return counts


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B117c - Oberschwaben map palette restyle"
    if marker in current:
        return
    entry = f"""
## B117c - Oberschwaben map palette restyle ({TODAY})

- Restyled already-derived Oberschwaben PNG layers to a clearer publication palette.
- Synchronized CSS legend swatches with the restyled PNG palette.
- Preserved geometry, alpha masks, source layers, FIONA/BK50/GISCO story logic and area values.
- Did not modify raw data or run GIS processing.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def write_counts(rows: list[dict[str, object]]) -> None:
    fields = ["file", "class", "count"]
    with COUNTS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_docs(rows: list[dict[str, object]], css_counts: dict[str, int], errors: list[str]) -> None:
    status = "OK" if not errors else "REVIEW REQUIRED"
    lines = [
        "# B117c – Oberschwaben Map Palette Restyle",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B117c synchronisiert die Oberschwaben-Kartenfarben und Legenden-Swatches mit einer klareren, publikationsfähigeren Palette.",
        "",
        "## Zielpalette",
        "",
        "| Klasse | Hex |",
        "|---|---|",
        f"| Ackerland | `{TARGET['acker']}` |",
        f"| Grünland | `{TARGET['gruenland']}` |",
        f"| Dauerkultur / Sondernutzung | `{TARGET['dauerkultur']}` |",
        f"| Moor-/Feuchtbodenkontext | `{TARGET['moor']}` |",
        f"| Schnittmenge | `{TARGET['intersection']}` |",
        "",
        "## Geänderte Karten",
        "",
        "- `public/maps/oberschwaben/oberschwaben_agriculture.png`",
        "- `public/maps/oberschwaben/oberschwaben_moor_context.png`",
        "- `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png`",
        "",
        "Nicht geändert:",
        "",
        "- `public/maps/oberschwaben/oberschwaben_admin_context.png`",
        "- `data/*`",
        "- FIONA/BK50/GISCO-Logik",
        "- Flächenwerte",
        "",
        "## Recolor counts",
        "",
        "| Datei | Klasse | Pixel |",
        "|---|---|---:|",
    ]
    for r in rows:
        lines.append(f"| `{r['file']}` | {r['class']} | {r['count']} |")

    lines.extend([
        "",
        "## CSS",
        "",
        f"- CSS changed: {css_counts.get('css_changed', 0)}",
        f"- Override appended: {css_counts.get('override_appended', 0)}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "python scripts\\117b_oberschwaben_png_palette_probe.py",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ])
    if errors:
        lines.extend(["## Errors", ""])
        for e in errors:
            lines.append(f"- {e}")

    write_text(REPORT, "\n".join(lines))

    audit = [
        "# B117c Oberschwaben palette audit",
        "",
        f"- Status: {status}",
        f"- Errors: {len(errors)}",
        f"- Recolor count rows: {len(rows)}",
        f"- CSS changed: {css_counts.get('css_changed', 0)}",
        "",
    ]
    if errors:
        audit.append("## Errors")
        for e in errors:
            audit.append(f"- {e}")
        audit.append("")
    audit.extend([
        "## Recommended checks",
        "",
        "```powershell",
        "Get-Content docs\\B117c_oberschwaben_map_palette_audit.txt",
        "Import-Csv docs\\B117c_oberschwaben_recolor_counts.csv -Delimiter ';' | Format-Table -Auto",
        "python scripts\\117b_oberschwaben_png_palette_probe.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "```",
        "",
    ])
    write_text(AUDIT, "\n".join(audit))


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    errors: list[str] = []
    rows: list[dict[str, object]] = []

    # Backups.
    for label, path in FILES.items():
        if not path.exists():
            errors.append(f"Missing {rel(path)}")
            continue
        backup = BACKUP_DIR / path.name
        if not backup.exists():
            shutil.copy2(path, backup)

    if CSS.exists():
        css_backup = BACKUP_DIR / "styles_before_b117c.css"
        if not css_backup.exists():
            shutil.copy2(CSS, css_backup)
    else:
        errors.append(f"Missing {rel(CSS)}")

    # Recolor maps.
    if not errors:
        try:
            counts = recolor_agriculture(FILES["agriculture"])
            for cls, count in counts.items():
                rows.append({"file": rel(FILES["agriculture"]), "class": cls, "count": count})
        except Exception as exc:
            errors.append(f"agriculture recolor failed: {exc}")

        try:
            counts = recolor_single_class(FILES["moor"], "moor")
            for cls, count in counts.items():
                rows.append({"file": rel(FILES["moor"]), "class": cls, "count": count})
        except Exception as exc:
            errors.append(f"moor recolor failed: {exc}")

        try:
            counts = recolor_single_class(FILES["intersection"], "intersection")
            for cls, count in counts.items():
                rows.append({"file": rel(FILES["intersection"]), "class": cls, "count": count})
        except Exception as exc:
            errors.append(f"intersection recolor failed: {exc}")

    css_counts = update_css() if CSS.exists() else {"css_changed": 0}

    write_counts(rows)
    write_docs(rows, css_counts, errors)
    update_done()

    print("B117c Oberschwaben map palette restyle complete.")
    print("Changed/created:")
    for p in [
        FILES["agriculture"], FILES["moor"], FILES["intersection"], CSS,
        REPORT, AUDIT, COUNTS_CSV, DONE
    ]:
        if p.exists():
            print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if not errors else 'REVIEW REQUIRED'}")
    print(f"Errors: {len(errors)}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B117c_oberschwaben_map_palette_audit.txt")
    print("  Import-Csv docs\\B117c_oberschwaben_recolor_counts.csv -Delimiter ';' | Format-Table -Auto")
    print("  python scripts\\117b_oberschwaben_png_palette_probe.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
