#!/usr/bin/env python3
r'''
B19b — Bind Europe frame to central sticky story.

Run from repository root:
  python scripts\47_bind_europe_frame_to_central_story.py
'''

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()

EUROPE_LAYERS_HTML = '''
        <img class="central-map-layer layer-europe-peat" src="public/maps/europe/europe_gpm2_peat_extent.png" alt="">
        <img class="central-map-layer layer-europe-borders" src="public/maps/europe/europe_country_borders.png" alt="">
'''

EUROPE_STEPS_HTML = '''
    <article class="central-map-step" data-global-state="europe-borders">
      <span>05 · Europe frame</span>
      <h3>Europe needs its own regional map frame.</h3>
      <p>
        The story now changes scale. Country borders make the European frame readable before the peatland
        pattern is added back in.
      </p>
    </article>

    <article class="central-map-step" data-global-state="europe-peat">
      <span>06 · European peat context</span>
      <h3>European peatlands are spatially concentrated, not evenly spread.</h3>
      <p>
        The European frame shows peatland context with higher regional clarity. This sets up the next move:
        from continental structure to the national implementation layer in Germany.
      </p>
    </article>
'''

CSS = '''
/* B19b bind Europe frame to central sticky story */
.layer-europe-peat,
.layer-europe-borders {
  opacity: 0;
}

.central-map-story[data-state="europe-borders"] .layer-gpm,
.central-map-story[data-state="europe-borders"] .layer-total,
.central-map-story[data-state="europe-borders"] .layer-density,
.central-map-story[data-state="europe-borders"] .layer-borders {
  opacity: 0;
}

.central-map-story[data-state="europe-borders"] .layer-europe-peat {
  opacity: 0;
}

.central-map-story[data-state="europe-borders"] .layer-europe-borders {
  opacity: .96;
}

.central-map-story[data-state="europe-peat"] .layer-gpm,
.central-map-story[data-state="europe-peat"] .layer-total,
.central-map-story[data-state="europe-peat"] .layer-density,
.central-map-story[data-state="europe-peat"] .layer-borders {
  opacity: 0;
}

.central-map-story[data-state="europe-peat"] .layer-europe-peat {
  opacity: .98;
}

.central-map-story[data-state="europe-peat"] .layer-europe-borders {
  opacity: .96;
}
'''

DOC_TEMPLATE = '''# B19b — Bind Europe Frame to Central Sticky Story

Date: {date}

## Purpose

Bind the newly exported Europe frame into the existing central sticky map story.

## Input assets

Required files:

- `public/maps/europe/europe_country_borders.png`
- `public/maps/europe/europe_gpm2_peat_extent.png`

Both must be exported from the same Europe layout frame and must be exactly 1600 × 900 px.

## Added story states

1. `europe-borders`
   - hides global layers
   - shows the Europe country-boundary frame only

2. `europe-peat`
   - shows European peat extent
   - overlays Europe country borders

## Design decision

Europe is not treated as a zoomed-in global PNG. It is a separate regional frame, but it is displayed inside the same central sticky stage. This keeps the interface calm while allowing a better projection and higher regional clarity.

## Acceptance check

When scrolling through the central map story, the sequence should now read:

1. global peat extent
2. global total emissions
3. global emission density
4. interpretation
5. Europe borders
6. Europe peat extent
'''

TASK = '''# Task B19c — Prepare Germany Frame Workflow

## Goal

Prepare the Germany frame as the next scale level after Europe.

## Intended logic

1. Global: peat extent and emissions pressure.
2. Europe: continental peatland structure with country borders.
3. Germany: national organic-soils implementation layer.
4. Baden-Württemberg: regional soil-context / BK50-Moor frame.

## Work items

1. Create a Germany map/layout frame in ArcGIS Pro.
2. Use a suitable Germany projection / extent.
3. Export aligned PNG layers:
   - germany_country_or_state_context.png
   - germany_organic_soils.png
4. Ensure all Germany PNGs share the same pixel size and transparency.
5. Later bind Germany into the same central sticky stage.
'''

EUROPE_META = '''
    ,
    "europe-borders": {
      mode: "Europe frame",
      title: "Europe needs its own regional map frame.",
      legend: `
        <span><i class="legend-border"></i>European country borders</span>
      `,
      source: "Europe frame: GISCO country boundaries · exported from EUROPE_FRAME_V1."
    },
    "europe-peat": {
      mode: "European peat context",
      title: "European peatlands are spatially concentrated.",
      legend: `
        <span><i class="legend-peat"></i>Peatland context</span>
        <span><i class="legend-mosaic"></i>Peat in soil mosaic</span>
        <span><i class="legend-border"></i>Country frame</span>
      `,
      source: "GPM2 peatland context rendered in Europe frame · ETRS89 / LAEA Europe."
    }'''

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def find_closing_div(text: str, start_idx: int) -> int:
    pos = start_idx
    depth = 0
    while True:
        next_open = text.find("<div", pos)
        next_close = text.find("</div>", pos)
        if next_close == -1:
            return -1
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            if depth <= 0:
                return next_close
            pos = next_close + len("</div>")

def insert_europe_layers(html: str) -> str:
    if "public/maps/europe/europe_gpm2_peat_extent.png" in html:
        return html
    marker = '<div class="central-map-layer-stack">'
    start = html.find(marker)
    if start == -1:
        raise SystemExit("Could not find central-map-layer-stack in index.html.")
    close = find_closing_div(html, start)
    if close == -1:
        raise SystemExit("Could not find closing div for central-map-layer-stack.")
    return html[:close] + EUROPE_LAYERS_HTML + html[close:]

def insert_europe_steps(html: str) -> str:
    if 'data-global-state="europe-borders"' in html:
        return html
    marker = 'data-global-state="compare"'
    start = html.find(marker)
    if start != -1:
        end = html.find("</article>", start)
        if end != -1:
            end += len("</article>")
            return html[:end] + "\n" + EUROPE_STEPS_HTML + html[end:]
    steps_marker = '<div class="central-map-steps">'
    steps_start = html.find(steps_marker)
    if steps_start == -1:
        raise SystemExit("Could not find central-map-steps in index.html.")
    close = find_closing_div(html, steps_start)
    if close == -1:
        raise SystemExit("Could not find closing div for central-map-steps.")
    return html[:close] + EUROPE_STEPS_HTML + html[close:]

def patch_js(text: str) -> str:
    if '"europe-borders"' in text and '"europe-peat"' in text:
        return text
    marker = "\n  };\n\n  function setState"
    if marker not in text:
        raise SystemExit("Could not locate STATE_META closing in central_global_map_story.js.")
    return text.replace(marker, EUROPE_META + marker, 1)

def main():
    root = Path.cwd()
    index = root / "index.html"
    styles = root / "src" / "styles.css"
    js = root / "src" / "central_global_map_story.js"

    if not index.exists():
        raise SystemExit("Run from repository root. index.html not found.")
    if not styles.exists():
        raise SystemExit("src/styles.css not found.")
    if not js.exists():
        raise SystemExit("src/central_global_map_story.js not found. Run B18b-new first.")

    for rel in [
        "public/maps/europe/europe_country_borders.png",
        "public/maps/europe/europe_gpm2_peat_extent.png",
    ]:
        if not (root / rel).exists():
            raise SystemExit(f"Missing required Europe map asset: {rel}")

    html = read(index)
    html = insert_europe_layers(html)
    html = insert_europe_steps(html)
    write(index, html)

    write(js, patch_js(read(js)))

    css_text = read(styles)
    if "B19b bind Europe frame to central sticky story" not in css_text:
        write(styles, css_text.rstrip() + "\n" + CSS + "\n")

    write(root / "docs" / "B19b_bind_europe_frame_to_central_story.md", DOC_TEMPLATE.format(date=TODAY))
    write(root / "tasks" / "B19c_prepare_germany_frame_workflow.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B19b completed" not in done_text:
        done_text += f"- {TODAY}: Task B19b completed — bound Europe frame to central sticky story.\n"
        write(done, done_text)

    print("B19b Europe frame bound to central sticky story.")
    print("Changed/created:")
    print("  index.html")
    print("  src/central_global_map_story.js")
    print("  src/styles.css")
    print("  docs/B19b_bind_europe_frame_to_central_story.md")
    print("  tasks/B19c_prepare_germany_frame_workflow.md")
    print("  tasks/done.md")
    print()
    print('Check: Select-String -Path index.html -Pattern "europe-borders|europe-peat|europe_gpm2"')
    print("Local test: python -m http.server 8000")

if __name__ == "__main__":
    main()
