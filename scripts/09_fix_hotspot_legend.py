#!/usr/bin/env python3
r"""
B6b-fix — Make the hotspot map legend visible and robust.

Run from repository root:

  python scripts\09_fix_hotspot_legend.py

Problem fixed:
The choropleth classes use SVG `fill`. The legend swatches are normal HTML <i>
elements, so they need `background`, not only `fill`.

No data changes.
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()

CSS_APPEND = r"""
/* B6b-fix: visible legend swatches for HTML legend items */
.hotspot-map-legend {
  padding: .75rem .85rem;
  border: 1px solid var(--line);
  border-radius: .85rem;
  background: rgba(255,255,255,.035);
}

.legend-item i.map-fill-1 { background: rgba(121,183,168,.22); }
.legend-item i.map-fill-2 { background: rgba(121,183,168,.38); }
.legend-item i.map-fill-3 { background: rgba(182,211,124,.50); }
.legend-item i.map-fill-4 { background: rgba(233,186,102,.68); }
.legend-item i.map-fill-5 { background: rgba(239,126,89,.82); }
.legend-item i.map-fill-no-data { background: rgba(255,255,255,.08); }

.legend-item i {
  flex: 0 0 auto;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.12);
}

.hotspot-toggle + .hotspot-map {
  margin-top: .25rem;
}
"""

NOTE = f"""# B6b-fix — Hotspot Legend Visibility

Date: {TODAY}

## Problem

The hotspot choropleth legend was present but visually weak/non-functional because the map color classes used SVG `fill`, while the legend swatches are normal HTML elements.

SVG paths respond to `fill`. HTML swatches need `background`.

## Change

Added explicit `background` colors for:

- `.legend-item i.map-fill-1`
- `.legend-item i.map-fill-2`
- `.legend-item i.map-fill-3`
- `.legend-item i.map-fill-4`
- `.legend-item i.map-fill-5`

Also added a subtle legend container background and border.

## Status

Visual fix only. No data-processing changes.
"""

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main():
    root = Path.cwd()
    styles = root / "src" / "styles.css"
    if not styles.exists():
        raise SystemExit("Run from repository root. src/styles.css not found.")

    css = read(styles)
    if "B6b-fix: visible legend swatches" not in css:
        write(styles, css + "\n" + CSS_APPEND)

    write(root / "docs" / "B6b_fix_hotspot_legend.md", NOTE)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B6b legend fix completed" not in done_text:
        done_text += f"- {TODAY}: Task B6b legend fix completed — made hotspot map legend swatches visible.\n"
        write(done, done_text)

    print("B6b legend fix applied.")
    print("Changed/created:")
    print("  src/styles.css")
    print("  docs/B6b_fix_hotspot_legend.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
