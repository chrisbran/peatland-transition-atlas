#!/usr/bin/env python3
r"""
B7 — Prepare Phase B public release.

Run from repository root:

  python scripts\13_prepare_phase_B_release.py

Purpose:
- update README with Phase B hotspot layer,
- update CHANGELOG with v0.2.0 draft notes,
- create release notes and QA checklist,
- create next visual-refinement task for B8.

No data changes.
"""

from pathlib import Path
import datetime


TODAY = datetime.date.today().isoformat()

README_BLOCK = r"""
## Phase B — Country-level peatland hotspot layer

Phase B extends the atlas from a literature-driven transition prototype into a first data-backed hotspot atlas.

The current hotspot layer uses country-level drained organic soils data to show:

- total drained-organic-soils greenhouse-gas emissions,
- emissions density per hectare of drained organic soils,
- top hotspot countries by total emissions,
- top hotspot countries by emissions density,
- a lightweight country-level choropleth map,
- a toggle between total emissions and emissions density,
- linked ranking/map interaction.

Important interpretation boundary:

This layer is a national-level screening layer. It does not show local rewetting suitability, hydrological feasibility, farm-scale constraints, land tenure or policy readiness.

Key public data files:

- `public/data/country_hotspots.csv`
- `public/data/hotspot_countries_110m.geojson`
"""

CHANGELOG_BLOCK = f"""
## v0.2.0 — Country-level hotspot atlas draft ({TODAY})

### Added

- Country-level drained organic soils hotspot dataset.
- Public hotspot dataset for GitHub Pages.
- Natural Earth 110m country boundary join.
- Country-level choropleth map.
- Map metric toggle:
  - total emissions,
  - emissions density.
- Top-10 hotspot rankings by total emissions and emissions density.
- Ranking/map interaction with selected-country highlighting.
- Method notes for B2b–B6c.

### Known limitations

- The choropleth is national-level only.
- It is not a local rewetting suitability map.
- Some small territories are unmatched in the Natural Earth 110m join.
- The map uses a simple dependency-free SVG projection and is not yet cartographically refined.
- Highlight colors and map palette are intentionally provisional.

### Next

- B8 visual refinement:
  - softer highlight color,
  - clearer ocean/land contrast,
  - map projection/perspective review,
  - possible no-data and desert/background distinction.
"""

RELEASE_NOTES = f"""# Phase B Release Notes — v0.2.0 Draft

Date: {TODAY}

## Release title

`v0.2.0 — Country-level hotspot atlas draft`

## Summary

This release adds the first data-backed hotspot layer to the Peatland Transition Atlas. The prototype now moves beyond literature/evidence mapping and includes a country-level drained organic soils emissions layer.

## Main additions

- `country_hotspots.csv`: country-level hotspot dataset.
- `hotspot_countries_110m.geojson`: lightweight GeoJSON for web mapping.
- Hotspot metrics:
  - total emissions,
  - emissions density.
- Interactive hotspot section:
  - key metrics,
  - choropleth map,
  - ranking cards,
  - metric toggle,
  - linked ranking/map highlighting.

## Interpretation boundary

The hotspot layer is a national screening layer. It does not identify parcels, farms or local rewetting opportunities.

The map must not be interpreted as:

- local suitability,
- hydrological feasibility,
- investment readiness,
- farm-scale transition advice.

## Known limitations

- Some small territories remain unmatched in the boundary join.
- The map uses Natural Earth 110m geometry and a simple SVG projection.
- Colors and highlight states are provisional.
- Ranking-map interaction is functional but should be visually refined later.
- Country-name and M49 joins should be reviewed before scientific publication use.

## Suggested GitHub release description

```text
This release adds the first country-level drained organic soils hotspot layer to the Peatland Transition Atlas.

New features:
- public hotspot dataset,
- Natural Earth country boundary join,
- choropleth map,
- total-emissions vs emissions-density toggle,
- ranking/map interaction.

The hotspot layer is intended as a national screening layer. It is not a local rewetting suitability map.
```
"""

QA_CHECKLIST = """# B7 — Phase B Release QA Checklist

## Before creating release v0.2.0

### Data

- [ ] `public/data/country_hotspots.csv` opens on GitHub Pages.
- [ ] `public/data/hotspot_countries_110m.geojson` opens on GitHub Pages.
- [ ] No raw data under `data/external/` are committed.
- [ ] Boundary join report is committed.
- [ ] Method notes B2b–B6c are committed.

### Interface

- [ ] Hotspot section loads after hard refresh.
- [ ] Total emissions map loads.
- [ ] Emissions density toggle works.
- [ ] Legend changes when the toggle changes.
- [ ] Ranking cards load.
- [ ] Ranking/map highlighting works.
- [ ] Caveat text is visible.

### Public interpretation

- [ ] README states that the layer is country-level only.
- [ ] Release notes state that the map is not local rewetting suitability.
- [ ] Known limitations are documented.

### GitHub

- [ ] All changes committed and pushed.
- [ ] GitHub Pages updated.
- [ ] Tag/release created as `v0.2.0`.
"""

B8_TASK = """# Task B8 — Visual and Cartographic Refinement

## Agent

Visualization Engineer Agent + QA Critic Agent

## Goal

Improve the visual quality of the hotspot map after the Phase B MVP is functional.

## Issues to review

- Highlight color is currently too bright/neon.
- Ocean and dark land/desert/background areas are not sufficiently distinguishable.
- The current equirectangular world map visually distorts high-latitude countries.
- Some small countries and fragmented archipelagos are hard to interact with.
- No-data and missing-geometries treatment should be clearer.

## Candidate improvements

- softer selected-country highlight color,
- separate ocean/background color,
- subtle base land fill for all countries,
- improved color ramp for total and density modes,
- optional Robinson/Natural Earth-style projection if implemented without heavy dependencies,
- fixed selected-country details panel instead of relying mainly on hover.

## Acceptance criteria

- map remains static and GitHub Pages compatible,
- no heavy framework is introduced,
- palette is readable but not visually aggressive,
- country-level caveat remains visible.
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def append_once(path: Path, marker: str, block: str):
    text = read(path) if path.exists() else ""
    if marker not in text:
        if text and not text.endswith("\n"):
            text += "\n"
        text += "\n" + block.strip() + "\n"
        write(path, text)


def prepend_changelog_once(path: Path, marker: str, block: str):
    text = read(path) if path.exists() else "# Changelog\n"
    if marker in text:
        return
    lines = text.splitlines()
    if lines and lines[0].lower().startswith("#"):
        new_text = lines[0] + "\n\n" + block.strip() + "\n\n" + "\n".join(lines[1:]).strip() + "\n"
    else:
        new_text = "# Changelog\n\n" + block.strip() + "\n\n" + text.strip() + "\n"
    write(path, new_text)


def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    append_once(root / "README.md", "Phase B — Country-level peatland hotspot layer", README_BLOCK)
    prepend_changelog_once(root / "CHANGELOG.md", "v0.2.0 — Country-level hotspot atlas draft", CHANGELOG_BLOCK)

    write(root / "docs" / "B7_phase_B_release_notes.md", RELEASE_NOTES)
    write(root / "tasks" / "phase_B_release_checklist.md", QA_CHECKLIST)
    write(root / "tasks" / "B8_visual_cartographic_refinement.md", B8_TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B7 completed" not in done_text:
        done_text += f"- {TODAY}: Task B7 completed — prepared Phase B release notes, README/CHANGELOG update and QA checklist.\n"
        write(done, done_text)

    print("B7 release prep applied.")
    print("Changed/created:")
    print("  README.md")
    print("  CHANGELOG.md")
    print("  docs/B7_phase_B_release_notes.md")
    print("  tasks/phase_B_release_checklist.md")
    print("  tasks/B8_visual_cartographic_refinement.md")
    print("  tasks/done.md")
    print()
    print("Next:")
    print("  Review live site and create GitHub release v0.2.0 if QA passes.")


if __name__ == "__main__":
    main()
