#!/usr/bin/env python3
r"""
B6a — Quick layout refinement after adding the hotspot choropleth.

Run from repository root:

  python scripts\07_refine_hotspot_layout.py

Purpose:
- make full-page screenshots cleaner by disabling the sticky header,
- give the hotspot section more breathing room,
- improve map/ranking layout on narrower screens,
- add a short QA note.

No external dependencies.
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()

CSS_APPEND = r"""
/* B6a layout refinement: hotspot section and full-page screenshot cleanup */

/*
The sticky header is useful during browsing, but it appears repeatedly in long
stitched screenshots and can overlap the hotspot section. For the portfolio
prototype we keep the header static.
*/
.site-header,
header.site-header {
  position: relative;
  top: auto;
  z-index: 20;
}

.hotspot-section {
  scroll-margin-top: 2rem;
}

.hotspot-section .section-heading {
  margin-bottom: 1.4rem;
}

.hotspot-layer {
  margin-top: 1.2rem;
}

.hotspot-map-card {
  margin-bottom: .4rem;
}

.hotspot-map {
  min-height: clamp(20rem, 46vw, 34rem);
}

.hotspot-map-details {
  line-height: 1.55;
}

.hotspot-caveat {
  line-height: 1.55;
}

@media (max-width: 760px) {
  .hotspot-grid {
    grid-template-columns: 1fr;
  }

  .hotspot-row-head {
    align-items: flex-start;
    flex-direction: column;
    gap: .25rem;
  }

  .hotspot-row-head span {
    white-space: normal;
  }

  .hotspot-map {
    min-height: 18rem;
  }

  .hotspot-map-legend {
    align-items: flex-start;
    flex-direction: column;
  }
}
"""

NOTE = f"""# B6a — Hotspot Layout Refinement

Date: {TODAY}

## Reason

After B5, the hotspot map loaded correctly, but the sticky header created a visual problem in long full-page screenshots. It appeared again inside the page and overlapped the hotspot section.

## Change

- Disabled sticky header behavior for this static portfolio prototype.
- Added spacing around the hotspot section.
- Improved responsive behavior for hotspot rankings and legend.
- Kept the dependency-free SVG map approach.

## Status

This is a visual/layout refinement only. It does not change the hotspot data or the choropleth join.

## Next possible refinement

- Add toggle: total emissions vs emissions density.
- Link map hover with ranking rows.
- Improve country tooltip.
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
    if "B6a layout refinement" not in css:
        write(styles, css + "\n" + CSS_APPEND)

    write(root / "docs" / "B6a_hotspot_layout_refinement.md", NOTE)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B6a completed" not in done_text:
        done_text += f"- {TODAY}: Task B6a completed — hotspot layout refined and sticky header disabled for cleaner screenshots.\n"
        write(done, done_text)

    print("B6a layout refinement applied.")
    print("Changed/created:")
    print("  src/styles.css")
    print("  docs/B6a_hotspot_layout_refinement.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
