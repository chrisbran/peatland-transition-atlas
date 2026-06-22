#!/usr/bin/env python3
"""
B71 - Reframe lower evidence modules

Purpose:
- Keep the central atlas story as the main narrative.
- Reframe the lower page as interpretation / supporting evidence / prototype appendix.
- Reversibly retire the old BW interactive GeoJSON layer from the visible page flow.
- Do not delete sections, scripts, data files, images, or map assets.

Changes:
- Add compact separators:
  - #interpretationIntro before #pathwayEvidenceMatrix
  - #supportingEvidenceGroupIntro before #hotspots
  - #prototypeAppendixIntro before #methodology
- Refresh #supportingEvidenceIntro text if it exists.
- Add data-evidence-tier attributes to lower modules.
- Retire #bwPeatLayer using HTML-level hiding:
  - class contains "is-retired"
  - hidden
  - aria-hidden="true"
  - data-retired="B71"
  - inline display:none
- Add CSS for lower evidence grouping.
- Create docs/B71_reframe_lower_evidence_modules.md.
- Update tasks/done.md.

Does NOT:
- remove script tags,
- delete bw_peat_layer.js,
- delete bw_bk50_moor_simplified.geojson,
- change central map story,
- change central map states,
- change map PNG assets.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

INTERPRETATION_INTRO = """
  <!-- B71 interpretation intro -->
  <section id="interpretationIntro" class="section lower-evidence-group lower-evidence-interpretation" data-story-role="lower-evidence-group" data-evidence-tier="interpretation">
    <div class="section-heading">
      <p class="eyebrow">Interpretation</p>
      <h2>What do the spatial patterns imply for transition pathways?</h2>
      <p>
        These modules translate the map story into pathway hypotheses: which forms of
        wet use, management change or policy support may fit different contexts.
      </p>
    </div>
  </section>
"""

SUPPORTING_INTRO = """
  <!-- B71 supporting evidence group intro -->
  <section id="supportingEvidenceGroupIntro" class="section lower-evidence-group lower-evidence-supporting" data-story-role="lower-evidence-group" data-evidence-tier="supporting-evidence">
    <div class="section-heading">
      <p class="eyebrow">Supporting evidence</p>
      <h2>Additional signals help test the atlas story.</h2>
      <p>
        Country hotspots, regional evidence and South Germany fit scores are exploratory
        checks. They support interpretation, but they are not the main storyline.
      </p>
    </div>
  </section>
"""

PROTOTYPE_INTRO = """
  <!-- B71 prototype appendix intro -->
  <section id="prototypeAppendixIntro" class="section lower-evidence-group lower-evidence-prototype" data-story-role="lower-evidence-group" data-evidence-tier="prototype-appendix">
    <div class="section-heading">
      <p class="eyebrow">Prototype appendix</p>
      <h2>Method, data and experimental layers.</h2>
      <p>
        This part documents the prototype status, source limitations and remaining
        experimental components. It is supporting material, not a finished decision tool.
      </p>
    </div>
  </section>
"""

SUPPORTING_EVIDENCE_REFRESH = """
  <!-- B68b / B71 compact supporting evidence bridge -->
  <section id="supportingEvidenceIntro" class="section evidence-explorer-intro evidence-explorer-bridge" data-story-role="supporting-evidence-intro">
    <div class="section-heading">
      <p class="eyebrow">After the main map</p>
      <h2>The rest of the page is an evidence explorer.</h2>
      <p>
        Use the following modules as interpretation and prototype support for the main
        atlas story, not as a second linear narrative.
      </p>
    </div>
  </section>
"""

CSS_BLOCK = """
/* B71 lower evidence reframing */
.lower-evidence-group {
  border-left: 2px solid rgba(209, 246, 168, 0.32);
  padding: clamp(0.75rem, 1.5vw, 1.1rem) 0 clamp(0.75rem, 1.5vw, 1.1rem) clamp(0.9rem, 1.8vw, 1.25rem);
  margin-block: clamp(1.2rem, 3vw, 2rem) clamp(0.4rem, 1vw, 0.8rem);
  background: linear-gradient(90deg, rgba(209, 246, 168, 0.055), transparent 72%);
}

.lower-evidence-group .section-heading {
  max-width: 780px;
}

.lower-evidence-group .section-heading h2 {
  font-size: clamp(1.05rem, 1.55vw, 1.32rem);
  margin-bottom: 0.35rem;
}

.lower-evidence-group .section-heading p {
  font-size: 0.9rem;
  line-height: 1.5;
}

.lower-evidence-interpretation {
  border-left-color: rgba(209, 246, 168, 0.42);
}

.lower-evidence-supporting {
  border-left-color: rgba(153, 210, 170, 0.34);
}

.lower-evidence-prototype {
  border-left-color: rgba(255, 215, 137, 0.34);
}
"""

TIER_ROLES = {
    "pathwayEvidenceMatrix": "interpretation",
    "pathways": "interpretation",
    "hotspots": "supporting-evidence",
    "map": "supporting-evidence",
    "fit": "supporting-evidence",
    "methodology": "prototype-appendix",
    "data": "prototype-appendix",
    "bwPeatLayer": "retired-experimental-layer",
}

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")

def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def find_section_open(html: str, section_id: str) -> re.Match[str] | None:
    return re.search(
        rf'<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])(?P<attrs>[^>]*)>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )

def replace_section(html: str, section_id: str, replacement: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf'\s*<!--\s*B(?:68|68b|71)[^>]*?-->\s*<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])[\s\S]*?</section>',
        re.IGNORECASE,
    )
    new_html, n = pattern.subn("\n" + replacement.rstrip(), html, count=1)
    if n:
        return new_html, True

    pattern = re.compile(
        rf'<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])[\s\S]*?</section>',
        re.IGNORECASE,
    )
    new_html, n = pattern.subn(replacement.strip(), html, count=1)
    return new_html, bool(n)

def insert_before_section(html: str, target_id: str, block: str, marker_id: str) -> str:
    if f'id="{marker_id}"' in html or f"id='{marker_id}'" in html:
        return html
    m = find_section_open(html, target_id)
    if not m:
        raise RuntimeError(f"Could not find target section #{target_id}.")
    return html[:m.start()] + block + "\n" + html[m.start():]

def upsert_attr(attrs: str, name: str, value: str | None = None) -> str:
    if value is None:
        if re.search(rf'\b{name}\b', attrs, flags=re.IGNORECASE):
            return attrs
        return attrs.rstrip() + f" {name}"

    pattern = re.compile(rf'\b{name}\s*=\s*["\'][^"\']*["\']', re.IGNORECASE)
    if pattern.search(attrs):
        return pattern.sub(f'{name}="{value}"', attrs)
    return attrs.rstrip() + f' {name}="{value}"'

def ensure_class(attrs: str, cls: str) -> str:
    m = re.search(r'\bclass\s*=\s*["\']([^"\']*)["\']', attrs, flags=re.IGNORECASE)
    if not m:
        return attrs.rstrip() + f' class="{cls}"'

    classes = m.group(1).split()
    if cls not in classes:
        classes.append(cls)

    new = f'class="{" ".join(classes)}"'
    return attrs[:m.start()] + new + attrs[m.end():]

def ensure_style_hidden(attrs: str) -> str:
    rule = "display: none !important;"
    m = re.search(r'\bstyle\s*=\s*["\']([^"\']*)["\']', attrs, flags=re.IGNORECASE)
    if not m:
        return attrs.rstrip() + f' style="{rule}"'

    style = m.group(1).strip()
    style_l = style.lower()
    if "display" not in style_l:
        style = style.rstrip(";") + "; " + rule
    elif "none" not in style_l:
        style = style.rstrip(";") + "; " + rule

    new = f'style="{style}"'
    return attrs[:m.start()] + new + attrs[m.end():]

def add_or_update_attr_on_section(html: str, section_id: str, name: str, value: str) -> str:
    m = find_section_open(html, section_id)
    if not m:
        return html
    tag = m.group(0)
    attrs = m.group("attrs")
    attrs = upsert_attr(attrs, name, value)
    new_tag = "<section" + attrs + ">"
    return html[:m.start()] + new_tag + html[m.end():]

def retire_bw_peat_layer(html: str) -> tuple[str, bool, str, str]:
    m = find_section_open(html, "bwPeatLayer")
    if not m:
        return html, False, "", ""

    old_tag = m.group(0)
    attrs = m.group("attrs")

    attrs = ensure_class(attrs, "is-retired")
    attrs = upsert_attr(attrs, "hidden", None)
    attrs = upsert_attr(attrs, "aria-hidden", "true")
    attrs = upsert_attr(attrs, "data-retired", "B71")
    attrs = upsert_attr(attrs, "data-story-role", "retired-experimental-regional-layer")
    attrs = upsert_attr(attrs, "data-evidence-tier", "retired-experimental-layer")
    attrs = ensure_style_hidden(attrs)

    new_tag = "<section" + attrs + ">"
    new_html = html[:m.start()] + new_tag + html[m.end():]
    return new_html, True, old_tag, new_tag

def patch_css(css: str) -> str:
    if "/* B71 lower evidence reframing */" in css:
        return css
    return css.rstrip() + "\n\n" + CSS_BLOCK.strip() + "\n"

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read(INDEX)

    required = ["pathwayEvidenceMatrix", "hotspots", "map", "pathways", "fit", "methodology", "data"]
    missing = [s for s in required if not find_section_open(html, s)]
    if missing:
        raise RuntimeError(f"Missing required lower sections: {missing}")

    # Refresh existing supporting evidence bridge from B68/B68b.
    if find_section_open(html, "supportingEvidenceIntro"):
        html, ok = replace_section(html, "supportingEvidenceIntro", SUPPORTING_EVIDENCE_REFRESH)
        if not ok:
            raise RuntimeError("Could not refresh #supportingEvidenceIntro.")

    html = insert_before_section(html, "pathwayEvidenceMatrix", INTERPRETATION_INTRO, "interpretationIntro")
    html = insert_before_section(html, "hotspots", SUPPORTING_INTRO, "supportingEvidenceGroupIntro")
    html = insert_before_section(html, "methodology", PROTOTYPE_INTRO, "prototypeAppendixIntro")

    for section_id, tier in TIER_ROLES.items():
        html = add_or_update_attr_on_section(html, section_id, "data-evidence-tier", tier)

    html, bw_retired, bw_old, bw_new = retire_bw_peat_layer(html)

    write(INDEX, html)

    css = read(CSS)
    write(CSS, patch_css(css))

    doc = f"""# B71 - Reframe Lower Evidence Modules

Date: {date.today().isoformat()}

## 1. Purpose

B71 makes the lower half of the page behave like an evidence explorer and prototype appendix rather than a second main storyline.

The central PNG sticky map story remains the main narrative.

## 2. Changed files

- `index.html`
- `src/styles.css`
- `docs/B71_reframe_lower_evidence_modules.md`
- `tasks/done.md`

## 3. New lower-page grouping

B71 adds three compact group separators:

1. `#interpretationIntro` before `#pathwayEvidenceMatrix`
2. `#supportingEvidenceGroupIntro` before `#hotspots`
3. `#prototypeAppendixIntro` before `#methodology`

## 4. Lower module tiers

- Interpretation:
  - `#pathwayEvidenceMatrix`
  - `#pathways`

- Supporting evidence:
  - `#hotspots`
  - `#map`
  - `#fit`

- Prototype appendix:
  - `#methodology`
  - `#data`

## 5. BW interactive layer decision

B71 reversibly retires `#bwPeatLayer` from the visible page flow.

Reason:

- The central BW/BK50 PNG story now carries the regional endpoint.
- The old BW GeoJSON layer is useful as an experimental prototype, but it weakens the current MVP narrative when shown as a full visible section.
- No files are deleted.

BW layer retired:

```text
{bw_retired}
```

Old opening tag:

```html
{bw_old}
```

New opening tag:

```html
{bw_new}
```

## 6. What B71 does not do

B71 does not:

- delete `#bwPeatLayer`,
- delete `src/bw_peat_layer.js`,
- remove the `src/bw_peat_layer.js` script tag,
- delete `public/data/bw_bk50_moor_simplified.geojson`,
- alter central map states,
- alter central map PNG assets,
- remove lower evidence modules.

## 7. Next recommended patch

Recommended B72:

`B72_public_mvp_quality_pass`

Scope:

- check the public GitHub Pages version,
- update QA to include BW PNGs and B69/B71 retired sections,
- optionally add a small "prototype status" note near the footer.
"""

    write(DOCS / "B71_reframe_lower_evidence_modules.md", doc)

    done_entry = f"""
## B71 - Reframe lower evidence modules ({date.today().isoformat()})

- Added lower-page grouping into interpretation, supporting evidence and prototype appendix.
- Refreshed the supporting-evidence bridge after the main map.
- Added `data-evidence-tier` attributes to lower modules.
- Reversibly retired the old `#bwPeatLayer` experimental GeoJSON section from the visible page flow.
- Did not delete sections, scripts, data files, images or map assets.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B71 - Reframe lower evidence modules" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B71 lower evidence reframing complete.")
    print(f"BW peat layer retired: {bw_retired}")
    print("Changed/created:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOCS / 'B71_reframe_lower_evidence_modules.md')}")
    print(f"  {rel(DONE)}")

if __name__ == "__main__":
    main()
