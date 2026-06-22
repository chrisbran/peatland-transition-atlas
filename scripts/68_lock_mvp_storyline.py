#!/usr/bin/env python3
"""
B68 - Lock MVP storyline

Purpose:
- Shift the project back from technical cleanup to product/narrative clarity.
- Make the central PNG sticky map story explicitly the narrative spine.
- Mark lower modules as supporting evidence/explorer modules.
- Do not delete, hide, or remove any existing section, script, data file, image, or map asset.

Changes:
- Insert a compact MVP storyline lock section before #centralGlobalMapStory.
- Insert a compact supporting-evidence intro before #pathwayEvidenceMatrix.
- Add data-story-role attributes to key sections.
- Add small CSS styles for the new editorial framing blocks.
- Create docs/B68_lock_mvp_storyline.md.
- Update tasks/done.md.
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

MVP_SECTION = """
  <!-- B68 MVP storyline lock -->
  <section id="mvpStoryline" class="section mvp-storyline-lock" data-story-role="narrative-lock">
    <div class="section-heading">
      <p class="eyebrow">MVP storyline</p>
      <h2>One main argument: from peatland extent to transition pathways.</h2>
      <p>
        The atlas is structured as a scale transition. It starts with where peatlands are,
        adds where pressure accumulates, narrows to implementation contexts, and then
        asks which transition pathways become plausible.
      </p>
    </div>

    <div class="story-lock-chain" aria-label="Peatland Transition Atlas storyline">
      <span>Extent</span>
      <span>Pressure</span>
      <span>Implementation context</span>
      <span>Transition pathways</span>
    </div>

    <p class="story-lock-note">
      The sticky map below is the main atlas story. The following sections are supporting
      evidence and exploratory interpretation, not a second main storyline.
    </p>
  </section>
"""

EVIDENCE_SECTION = """
  <!-- B68 supporting evidence intro -->
  <section id="supportingEvidenceIntro" class="section evidence-explorer-intro" data-story-role="supporting-evidence-intro">
    <div class="section-heading">
      <p class="eyebrow">Supporting evidence</p>
      <h2>From spatial pressure to pathway interpretation.</h2>
      <p>
        The modules below are exploratory support layers: pathway evidence, country-level
        pressure signals, regional examples, South Germany fit and methods. They help test
        and interpret the main map story rather than replacing it.
      </p>
    </div>
  </section>
"""

CSS_BLOCK = """
/* B68 MVP storyline lock */
.mvp-storyline-lock,
.evidence-explorer-intro {
  border: 1px solid rgba(209, 246, 168, 0.16);
  background:
    radial-gradient(circle at 15% 10%, rgba(209, 246, 168, 0.08), transparent 34%),
    rgba(12, 26, 20, 0.72);
  border-radius: 18px;
  padding: clamp(1.1rem, 2vw, 1.8rem);
  margin-block: clamp(1.5rem, 4vw, 3rem);
}

.mvp-storyline-lock .section-heading,
.evidence-explorer-intro .section-heading {
  max-width: 820px;
}

.story-lock-chain {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.7rem;
  margin-top: 1.15rem;
}

.story-lock-chain span {
  border: 1px solid rgba(209, 246, 168, 0.2);
  border-radius: 999px;
  padding: 0.65rem 0.75rem;
  text-align: center;
  color: var(--accent);
  background: rgba(209, 246, 168, 0.055);
  font-size: 0.82rem;
  letter-spacing: 0.02em;
}

.story-lock-note {
  max-width: 820px;
  margin: 1.1rem 0 0;
  color: var(--muted);
  font-size: 0.94rem;
}

@media (max-width: 760px) {
  .story-lock-chain {
    grid-template-columns: 1fr;
  }

  .story-lock-chain span {
    text-align: left;
  }
}
"""

SECTION_ROLES = {
    "story": "intro-overview",
    "transitionLogic": "conceptual-frame",
    "guidedStory": "retired-legacy-story",
    "layerProvenance": "layer-reading-note",
    "mvpStoryline": "narrative-lock",
    "centralGlobalMapStory": "main-atlas-story",
    "supportingEvidenceIntro": "supporting-evidence-intro",
    "pathwayEvidenceMatrix": "pathway-evidence",
    "hotspots": "evidence-explorer",
    "map": "regional-evidence",
    "pathways": "pathway-interpretation",
    "fit": "south-germany-fit",
    "methodology": "method-and-limits",
    "data": "prototype-data",
    "bwPeatLayer": "experimental-regional-layer",
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

def add_data_story_role(html: str, section_id: str, role: str) -> str:
    m = find_section_open(html, section_id)
    if not m:
        return html

    tag = m.group(0)
    if re.search(r'\bdata-story-role\s*=', tag, flags=re.IGNORECASE):
        new_tag = re.sub(
            r'\bdata-story-role\s*=\s*["\'][^"\']*["\']',
            f'data-story-role="{role}"',
            tag,
            flags=re.IGNORECASE,
        )
    else:
        new_tag = tag[:-1].rstrip() + f' data-story-role="{role}">'

    return html[:m.start()] + new_tag + html[m.end():]

def insert_before_section(html: str, target_id: str, block: str, marker_id: str) -> str:
    if f'id="{marker_id}"' in html or f"id='{marker_id}'" in html:
        return html
    m = find_section_open(html, target_id)
    if not m:
        raise RuntimeError(f'Could not find target section #{target_id}.')
    return html[:m.start()] + block + "\n" + html[m.start():]

def patch_css(css: str) -> str:
    if "/* B68 MVP storyline lock */" in css:
        return css
    return css.rstrip() + "\n\n" + CSS_BLOCK.strip() + "\n"

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read(INDEX)

    if not find_section_open(html, "centralGlobalMapStory"):
        raise RuntimeError("Missing #centralGlobalMapStory. Refusing B68 patch.")

    # Insert editorial framing blocks.
    html = insert_before_section(html, "centralGlobalMapStory", MVP_SECTION, "mvpStoryline")
    html = insert_before_section(html, "pathwayEvidenceMatrix", EVIDENCE_SECTION, "supportingEvidenceIntro")

    # Add/refresh story-role attributes.
    for section_id, role in SECTION_ROLES.items():
        html = add_data_story_role(html, section_id, role)

    write(INDEX, html)

    css = read(CSS)
    write(CSS, patch_css(css))

    doc = f"""# B68 - Lock MVP Storyline

Date: {date.today().isoformat()}

## 1. Purpose

B68 shifts the project from technical cleanup back to product clarity.

The current MVP is not a complete GIS dashboard. It is a narrative research and policy prototype that explains a single argument:

`Extent -> Pressure -> Implementation context -> Transition pathways`

## 2. Core product goal

The Peatland Transition Atlas should show how the peatland transition problem can be read across scales:

1. Global peatland extent.
2. Global pressure / hotspot signals.
3. European context.
4. Germany / Thuenen implementation context.
5. Baden-Wuerttemberg / BK50 regional soil context.
6. Transition pathway interpretation.

## 3. Changed files

- `index.html`
- `src/styles.css`
- `docs/B68_lock_mvp_storyline.md`
- `tasks/done.md`

## 4. What B68 adds

### `#mvpStoryline`

A compact editorial lock before the central sticky map story. It states that the sticky PNG map is the main atlas story.

### `#supportingEvidenceIntro`

A compact separator before the evidence/pathway modules. It states that the lower modules are support layers, not a second main storyline.

### `data-story-role`

B68 adds `data-story-role` attributes to major sections. These are not used for functionality yet; they document the intended role of each section and make later cleanup safer.

## 5. What B68 does not do

B68 does not:

- delete sections,
- hide sections,
- remove scripts,
- remove assets,
- change map states,
- alter the central PNG story controller stack,
- remove the BW interactive layer.

## 6. Next recommended patch

Recommended B69:

`B69_refine_central_story_readability`

Scope:

- tighten central map step wording,
- make each step's role explicit,
- reduce redundant or abstract text,
- leave data, scripts and map assets untouched.

## 7. Visual QA checklist

After B68:

1. The new MVP storyline block appears before the central sticky map story.
2. The central PNG map story still works through all states.
3. The supporting evidence intro appears before pathway/evidence modules.
4. Hotspot, evidence map, pathway, fit, methodology and data sections still render.
5. No legacy guided story is visible.
"""

    write(DOCS / "B68_lock_mvp_storyline.md", doc)

    done_entry = f"""
## B68 - Lock MVP storyline ({date.today().isoformat()})

- Added a compact MVP storyline lock before the central map story.
- Added a supporting-evidence intro before the lower explorer/pathway modules.
- Added `data-story-role` attributes to major page sections.
- Added small CSS styles for the new editorial framing blocks.
- Did not delete sections, scripts, data files, images or map assets.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B68 - Lock MVP storyline" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B68 MVP storyline lock complete.")
    print("Changed/created:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOCS / 'B68_lock_mvp_storyline.md')}")
    print(f"  {rel(DONE)}")

if __name__ == "__main__":
    main()
