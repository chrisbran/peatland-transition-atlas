#!/usr/bin/env python3
r"""
Rollback B18b3 CSS-only contrast patch.

This removes only the B18b3 appended CSS block and the B18b3/B18b4 docs/tasks created
by script 40. It keeps the central global map story itself.

Run from repository root:

  python scripts\41_rollback_b18b3_contrast_css.py
"""

from pathlib import Path
import re
import datetime

TODAY = datetime.date.today().isoformat()

START_MARKER = "/* B18b3 central global map contrast and palette refinement */"

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def remove_css_block(css: str) -> str:
    start = css.find(START_MARKER)
    if start == -1:
        return css

    # The B18b3 block was appended near the end. Remove from marker to end,
    # unless another later block marker exists after it.
    next_marker = css.find("\n/* B", start + len(START_MARKER))
    if next_marker == -1:
        return css[:start].rstrip() + "\n"
    return css[:start].rstrip() + "\n" + css[next_marker:].lstrip()

def remove_done_lines(text: str) -> str:
    lines = text.splitlines()
    filtered = [
        line for line in lines
        if "Task B18b3 completed" not in line
    ]
    return "\n".join(filtered).rstrip() + "\n"

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    styles = root / "src" / "styles.css"
    if styles.exists():
        old = read(styles)
        new = remove_css_block(old)
        if new != old:
            write(styles, new)
            print("Removed B18b3 CSS block from src/styles.css")
        else:
            print("B18b3 CSS marker not found in src/styles.css")

    # Remove generated B18b3 docs/tasks if present.
    for rel in [
        "docs/B18b3_central_global_map_contrast_refinement.md",
        "tasks/B18b4_arcgis_symbology_reexport_if_needed.md",
    ]:
        path = root / rel
        if path.exists():
            path.unlink()
            print(f"Removed {rel}")

    done = root / "tasks" / "done.md"
    if done.exists():
        old = read(done)
        new = remove_done_lines(old)
        if new != old:
            write(done, new)
            print("Removed B18b3 done.md entry")

    print()
    print("Rollback complete.")
    print("Now hard refresh the local site with Ctrl+F5.")
    print("If the map returns to the previous look, continue with ArcGIS re-export rather than CSS filters.")

if __name__ == "__main__":
    main()
