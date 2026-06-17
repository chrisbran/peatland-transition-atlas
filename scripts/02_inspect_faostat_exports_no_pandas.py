#!/usr/bin/env python3
"""
Inspect FAOSTAT / KAPSARC CSV exports without pandas.

Usage:
  python scripts\02_inspect_faostat_exports_no_pandas.py --input data\external\faostat
  python scripts\02_inspect_faostat_exports_no_pandas.py --input data\external\faostat --max-values 30

This script is dependency-free: only Python standard library.
It scans .csv files and .zip files containing .csv files.
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
import zipfile
from collections import defaultdict
from pathlib import Path


LIKELY_FIELDS = [
    "Domain", "Domain Code", "Area", "Area Code", "Area Code (M49)",
    "Item", "Item Code", "Element", "Element Code", "Year", "Unit", "Value",
    "Flag", "Note", "Source"
]


def sniff_delimiter(sample: str) -> str:
    candidates = [",", ";", "\t", "|"]
    counts = {d: sample.count(d) for d in candidates}
    return max(counts, key=counts.get) if max(counts.values()) > 0 else ","


def open_text_from_path(path: Path):
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
        try:
            return io.StringIO(raw.decode(enc)), enc
        except UnicodeDecodeError:
            continue
    return io.StringIO(raw.decode("utf-8", errors="replace")), "utf-8-replace"


def iter_csv_sources(input_dir: Path):
    for path in sorted(input_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() == ".csv":
            text_io, enc = open_text_from_path(path)
            yield str(path), text_io, enc

        elif path.is_file() and path.suffix.lower() == ".zip":
            try:
                with zipfile.ZipFile(path) as z:
                    for name in z.namelist():
                        if name.lower().endswith(".csv"):
                            raw = z.read(name)
                            enc = None
                            for e in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
                                try:
                                    text = raw.decode(e)
                                    enc = e
                                    break
                                except UnicodeDecodeError:
                                    pass
                            if enc is None:
                                text = raw.decode("utf-8", errors="replace")
                                enc = "utf-8-replace"
                            yield f"{path}::{name}", io.StringIO(text), enc
            except zipfile.BadZipFile:
                print(f"[WARN] Not a valid ZIP: {path}", file=sys.stderr)


def inspect_csv(label: str, text_io, encoding: str, max_values: int):
    sample = text_io.read(4096)
    text_io.seek(0)
    delimiter = sniff_delimiter(sample)

    reader = csv.DictReader(text_io, delimiter=delimiter)
    if not reader.fieldnames:
        print(f"\n## {label}")
        print("Could not read header.")
        return

    fieldnames = [f.strip() if f else f for f in reader.fieldnames]
    reader.fieldnames = fieldnames

    uniques = defaultdict(set)
    row_count = 0

    for row in reader:
        row_count += 1
        for field in fieldnames:
            if field in LIKELY_FIELDS or any(key.lower() in field.lower() for key in ["domain", "area", "item", "element", "year", "unit", "value"]):
                val = (row.get(field) or "").strip()
                if val != "" and len(uniques[field]) < max_values:
                    uniques[field].add(val)

    print("\n" + "=" * 90)
    print(f"FILE: {label}")
    print(f"Encoding: {encoding} | Delimiter: {repr(delimiter)} | Rows: {row_count}")
    print("-" * 90)
    print("Columns:")
    for f in fieldnames:
        print(f"  - {f}")

    print("-" * 90)
    print("Selected unique values:")
    for field in fieldnames:
        vals = sorted(uniques.get(field, []))
        if vals:
            print(f"\n[{field}] ({len(vals)} shown)")
            for v in vals[:max_values]:
                print(f"  {v}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Folder containing FAOSTAT/KAPSARC CSV or ZIP exports.")
    parser.add_argument("--max-values", type=int, default=25, help="Max unique values shown per field.")
    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"Input folder not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    found = False
    for label, text_io, enc in iter_csv_sources(input_dir):
        found = True
        inspect_csv(label, text_io, enc, args.max_values)

    if not found:
        print(f"No CSV or ZIP-with-CSV files found in: {input_dir}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
