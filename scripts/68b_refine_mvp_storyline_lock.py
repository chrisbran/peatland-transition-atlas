#!/usr/bin/env python3
"""
B68b - Refine MVP storyline lock

Purpose:
- Keep the B68 narrative correction, but reduce visual weight.
- Convert the MVP storyline block from a large explanatory section into a compact bridge.
- Convert the supporting-evidence intro into a compact separator.
- Do not delete, hide, or remove any existing section, script, data file, image, or map asset.

Changes:
- Replace #mvpStoryline content with a shorter bridge.
- Replace #supportingEvidenceIntro content with a shorter bridge.
- Add compact CSS overrides for B68b.
- Create docs/B68b_refine_mvp_storyline_lock.md.
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

MVP_SECTION_COMPACT = """
  <!-- B68b compact MVP storyline bridge -->
  <section id="mvpStoryline" class="section mvp-storyline-lock mvp-storyline-bridge" data-story-role="narrative-lock">
    <div class="section-heading">
      <p class="eyebrow">Main atlas story</p>
      <h2>The map below is the core narrative.</h2>
      <p>
        It moves from global peatland extent and pressure to Germany,
        Baden-Wuerttemberg and pathway interpretation.
      </p>
    </div>

    <div class="story-lock-chain compact" aria-label="Peatland Transition Atlas storyline">
      <span>Extent</span>
      <span>Pressure</span>
      <span>Implementation</span>
      <span>Pathways</span>
    </div>

    <p class="story-lock-note">
      Everything after the map is supporting evidence and exploratory interpretation.
    </p>
  </section>
"""

EVIDENCE_SECTION_COMPACT = """
  <!-- B68b compact supporting evidence bridge -->
  <section id="supportingEvidenceIntro" class="section evidence-explorer-intro evidence-explorer-bridge" data-story-role="supporting-evidence-intro">
    <div class="section-heading">
      <p class="eyebrow">Evidence explorer</p>
      <h2>The following modules support the map story.</h2>
      <p>
        They add pathway evidence, country-level pressure signals, regional examples,
        South Germany fit and methodological context.
      </p>
    </div>
  </section>
"""

CSS_BLOCK = """
/* B68b compact storyline bridge */
.mvp-storyline-bridge,
.evidence-explorer-bridge {
  border-color: rgba(209, 246, 168, 0.12);
  background: rgba(12, 26, 20, 0.48);
  border-radius: 14px;
  padding: clamp(0.75rem, 1.4vw, 1.05rem);
  margin-block: clamp(0.85rem, 2.2vw, 1.55rem);
}

.mvp-storyline-bridge .section-heading,
.evidence-explorer-bridge .section-heading {
  max-width: 760px;
}

.mvp-storyline-bridge .section-heading h2,
.evidence-explorer-bridge .section-heading h2 {
  font-size: clamp(1.05rem, 1.6vw, 1.35rem);
  margin-bottom: 0.35rem;
}

.mvp-storyline-bridge .section-heading p,
.evidence-explorer-bridge .section-heading p {
  font-size: 0.9rem;
  line-height: 1.45;
}

.story-lock-chain.compact {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin-top: 0.75rem;
}

.story-lock-chain.compact span {
  flex: 0 1 auto;
  padding: 0.38rem 0.58rem;
  font-size: 0.72rem;
  text-align: left;
}

.mvp-storyline-bridge .story-lock-note {
  margin-top: 0.65rem;
  font-size: 0.82rem;
}
"""

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")

def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def replace_section(html: str, section_id: str, replacement: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf'\s*<!--\s*B68[^>]*?-->\s*<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])[\s\S]*?</section>',
        re.IGNORECASE,
    )
    new_html, n = pattern.subn("\n" + replacement.rstrip(), html, count=1)
    if n:
        return new_html, True

    # Fallback without comment marker.
    pattern = re.compile(
        rf'<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])[\s\S]*?</section>',
        re.IGNORECASE,
    )
    new_html, n = pattern.subn(replacement.strip(), html, count=1)
    return new_html, bool(n)

def patch_css(css: str) -> str:
    if "/* B68b compact storyline bridge */" in css:
        return css
    return css.rstrip() + "\n\n" + CSS_BLOCK.strip() + "\n"

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read(INDEX)

    if 'id="mvpStoryline"' not in html and "id='mvpStoryline'" not in html:
        raise RuntimeError("Missing #mvpStoryline. Run B68 before B68b.")
    if 'id="supportingEvidenceIntro"' not in html and "id='supportingEvidenceIntro'" not in html:
        raise RuntimeError("Missing #supportingEvidenceIntro. Run B68 before B68b.")

    html, ok1 = replace_section(html, "mvpStoryline", MVP_SECTION_COMPACT)
    html, ok2 = replace_section(html, "supportingEvidenceIntro", EVIDENCE_SECTION_COMPACT)

    if not ok1:
        raise RuntimeError("Could not replace #mvpStoryline.")
    if not ok2:
        raise RuntimeError("Could not replace #supportingEvidenceIntro.")

    write(INDEX, html)

    css = read(CSS)
    write(CSS, patch_css(css))

    doc = f"""# B68b - Refine MVP Storyline Lock

Date: {date.today().isoformat()}

## 1. Purpose

B68 added the correct narrative lock, but the first visual review showed that the block was too heavy.

B68b keeps the editorial intent but makes the intervention smaller:

- the central map is still identified as the main atlas story,
- the storyline chain remains visible,
- the supporting-evidence modules are still framed as support material,
- the page no longer adds another large explanatory block before the map.

## 2. Changed files

- `index.html`
- `src/styles.css`
- `docs/B68b_refine_mvp_storyline_lock.md`
- `tasks/done.md`

## 3. Design decision

The page already has enough explanation before the map. The narrative lock should behave like a bridge, not like a separate chapter.

Therefore B68b changes:

`MVP storyline section` -> `compact main atlas story bridge`

and:

`Supporting evidence section` -> `compact evidence explorer bridge`

## 4. What B68b does not do

B68b does not:

- delete sections,
- hide sections,
- remove scripts,
- remove assets,
- change central map states,
- change the BW/BK50 map layer stack,
- alter the lower evidence modules.

## 5. Next recommended patch

Recommended B69:

`B69_retire_or_merge_six_part_story`

Reason:

After B68b, the largest remaining redundancy is the old `#story` / "Six-part story" section above the transition logic. It should either be retired or merged into the conceptual framing.
"""

    write(DOCS / "B68b_refine_mvp_storyline_lock.md", doc)

    done_entry = f"""
## B68b - Refine MVP storyline lock ({date.today().isoformat()})

- Replaced the large B68 MVP storyline block with a compact main-atlas-story bridge.
- Replaced the large supporting-evidence intro with a compact evidence-explorer bridge.
- Added compact CSS overrides.
- Did not delete sections, scripts, data files, images or map assets.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B68b - Refine MVP storyline lock" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B68b refined MVP storyline lock complete.")
    print("Changed/created:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOCS / 'B68b_refine_mvp_storyline_lock.md')}")
    print(f"  {rel(DONE)}")

if __name__ == "__main__":
    main()
