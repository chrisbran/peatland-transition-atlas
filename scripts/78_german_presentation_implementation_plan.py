#!/usr/bin/env python3
# B78 - German presentation implementation plan
#
# Purpose:
# - Plan the production implementation of the German presentation version.
# - Convert B73-B77 decisions into a concrete, reversible patch strategy.
# - Specify files, sections, text replacements, CSS direction, QA checks and rollback.
# - Do not modify production website files.

from __future__ import annotations

from datetime import date
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

PLAN = DOCS / "B78_german_presentation_implementation_plan.md"
COPY_TABLE = DOCS / "B78_german_presentation_copy_targets.csv"
PATCH_BRIEF = DOCS / "B78_patch_strategy.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_copy_table() -> None:
    rows = [
        {
            "area": "hero",
            "selector_or_context": "hero eyebrow / kicker",
            "current_problem": "Portfolio-/Prototype-Sprache; Englisch; selbstreferenziell",
            "target_de": "Moore · Klimaschutz · regionale Umsetzung",
            "priority": "high",
            "implementation_note": "Visible hero text ersetzen. Keine Erwähnung von Atlas, Prototype, MVP oder Portfolio.",
        },
        {
            "area": "hero",
            "selector_or_context": "main h1",
            "current_problem": "Peatland Transition Atlas als Produkt-/Tooltitel",
            "target_de": "Moorschutz braucht räumliche Orientierung",
            "priority": "high",
            "implementation_note": "H1 als Aussage setzen, nicht als Produktname.",
        },
        {
            "area": "hero",
            "selector_or_context": "lead paragraph",
            "current_problem": "Englisch; abstrakt; Tool-Perspektive",
            "target_de": "Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung.",
            "priority": "high",
            "implementation_note": "Kurz und pointiert. Keine Datenbehauptungen ohne Quelle im Hero.",
        },
        {
            "area": "navigation",
            "selector_or_context": "top nav links",
            "current_problem": "Story / Evidence Map / Pathways / Data = Englisch und Meta-Sprache",
            "target_de": "Problem | Kartenfolge | Umsetzung | Pfade | Methode",
            "priority": "high",
            "implementation_note": "Navigation an sichtbare deutsche Kurzfassung anpassen.",
        },
        {
            "area": "transition logic",
            "selector_or_context": "section kicker",
            "current_problem": "Atlas framing = Meta-Sprache",
            "target_de": "Kernargument",
            "priority": "high",
            "implementation_note": "Nur falls Section sichtbar bleibt. Alternativ mit Hero/Argumentblock verschmelzen.",
        },
        {
            "area": "transition logic",
            "selector_or_context": "section h2",
            "current_problem": "From peatland extent to transition priorities = Englisch; Priorität methodisch riskant",
            "target_de": "Aus Moorbodenkontext wird eine Umsetzungsfrage",
            "priority": "high",
            "implementation_note": "Keine Prioritätsbehauptung. Fokus auf Umsetzung.",
        },
        {
            "area": "transition logic",
            "selector_or_context": "section lead",
            "current_problem": "Prototype/atlas/workflow-Sprache",
            "target_de": "Moorschutz wird erst dann planbar, wenn räumliche Kulissen, regionale Nutzung, betriebliche Betroffenheit und mögliche Wertschöpfungsketten gemeinsam betrachtet werden.",
            "priority": "high",
            "implementation_note": "Als kurze argumentative Brücke.",
        },
        {
            "area": "central map story",
            "selector_or_context": "section kicker",
            "current_problem": "Main atlas story / central story = Tool-Sprache",
            "target_de": "Kartenfolge",
            "priority": "high",
            "implementation_note": "Kartenfolge statt Atlas/Story.",
        },
        {
            "area": "central map story",
            "selector_or_context": "section h2",
            "current_problem": "Englischer oder meta-orientierter Titel",
            "target_de": "Von globaler Relevanz zur regionalen Umsetzung",
            "priority": "high",
            "implementation_note": "Soll die Funktion der gesamten Sequenz erklären.",
        },
        {
            "area": "central map story",
            "selector_or_context": "section lead",
            "current_problem": "Zu lang / Englisch / Tool-Sprache",
            "target_de": "Die Kartenfolge verdichtet den Maßstab: von der weltweiten Moorverbreitung über Emissionsdruck und nationale Umsetzungskulissen bis zum Boden- und Feuchtgebietskontext in Baden-Württemberg.",
            "priority": "high",
            "implementation_note": "Kurz halten. Keine methodisch nicht gedeckte Priorisierung.",
        },
        {
            "area": "central step",
            "selector_or_context": "state extent",
            "current_problem": "Englisch",
            "target_de": "Wo liegen die Moore?",
            "priority": "high",
            "implementation_note": "Step h3 ersetzen. Step p kurz erklären.",
        },
        {
            "area": "central step",
            "selector_or_context": "state total",
            "current_problem": "Englisch / pressure abstrakt",
            "target_de": "Wo konzentriert sich der Emissionsdruck?",
            "priority": "high",
            "implementation_note": "Druck/Emission auf Deutsch fassen.",
        },
        {
            "area": "central step",
            "selector_or_context": "state density",
            "current_problem": "Englisch / pressure abstrakt",
            "target_de": "Wo ist der Druck besonders hoch?",
            "priority": "medium",
            "implementation_note": "Nur verwenden, wenn total/density getrennt sichtbar bleiben.",
        },
        {
            "area": "central step",
            "selector_or_context": "state compare",
            "current_problem": "Englisch",
            "target_de": "Größe und Intensität erzählen unterschiedliche Geschichten.",
            "priority": "medium",
            "implementation_note": "Langer Titel; ggf. kürzen zu: Größe und Intensität unterscheiden sich.",
        },
        {
            "area": "central step",
            "selector_or_context": "state europe-borders",
            "current_problem": "Englisch",
            "target_de": "Europa übersetzt Druck in Politik.",
            "priority": "medium",
            "implementation_note": "Etwas pointiert, ggf. sachlicher: Europa wird zur Umsetzungsebene.",
        },
        {
            "area": "central step",
            "selector_or_context": "state europe-peat",
            "current_problem": "Englisch",
            "target_de": "Moorvorkommen überschreiten Grenzen.",
            "priority": "medium",
            "implementation_note": "Kurz und sachlich.",
        },
        {
            "area": "central step",
            "selector_or_context": "state germany-context",
            "current_problem": "Englisch",
            "target_de": "Deutschland ist eine Umsetzungsebene.",
            "priority": "high",
            "implementation_note": "Gute Brücke zur nationalen Kulisse.",
        },
        {
            "area": "central step",
            "selector_or_context": "state germany-thuenen-extent",
            "current_problem": "Englisch",
            "target_de": "Die Thünen-Kulisse konkretisiert organische Böden.",
            "priority": "medium",
            "implementation_note": "Fachlich prüfen, ob organische Böden/Thünen exakt benannt werden.",
        },
        {
            "area": "central step",
            "selector_or_context": "state germany-thuenen-types",
            "current_problem": "Englisch",
            "target_de": "Bodenkontext prägt mögliche Nutzungspfade.",
            "priority": "medium",
            "implementation_note": "Keine Eignungsbehauptung.",
        },
        {
            "area": "central step",
            "selector_or_context": "state bw-context",
            "current_problem": "Englisch",
            "target_de": "Baden-Württemberg wird konkret.",
            "priority": "high",
            "implementation_note": "Als Übergang zur regionalen Ebene.",
        },
        {
            "area": "central step",
            "selector_or_context": "state bw-bk50-extent",
            "current_problem": "Englisch / wetland soil Kontext ggf. unscharf",
            "target_de": "BK50 zeigt Moor- und Feuchtbodenkontext.",
            "priority": "high",
            "implementation_note": "Immer mit Boundary: keine Eignung, keine Priorität.",
        },
        {
            "area": "regional implementation",
            "selector_or_context": "new or existing lower section",
            "current_problem": "SOLAMO/LUBW noch nicht sichtbar strukturiert",
            "target_de": "Oberschwaben zeigt die praktische Herausforderung",
            "priority": "high",
            "implementation_note": "Als kurze Brücke nach zentraler Karte; keine tiefe neue Datenlogik.",
        },
        {
            "area": "regional implementation cards",
            "selector_or_context": "three cards",
            "current_problem": "Evidence/Explorer-Sprache",
            "target_de": "Planungskulisse | Betriebliche Betroffenheit | Wertschöpfung",
            "priority": "high",
            "implementation_note": "LUBW/SOLAMO als fachliche Verankerung, nicht als Projektwerbung.",
        },
        {
            "area": "pathways",
            "selector_or_context": "pathway section",
            "current_problem": "Pathways Englisch / zu explorativ",
            "target_de": "Nicht jede Fläche braucht dieselbe Lösung",
            "priority": "high",
            "implementation_note": "Drei Pfade: schützen, wiedervernässen, Nutzung neu organisieren.",
        },
        {
            "area": "method",
            "selector_or_context": "method boundary",
            "current_problem": "Prototype appendix / Data-Sprache",
            "target_de": "Einordnung statt Eignungskarte",
            "priority": "high",
            "implementation_note": "Muss sichtbar bleiben. Schützt vor Überbehauptung.",
        },
    ]

    fields = ["area", "selector_or_context", "current_problem", "target_de", "priority", "implementation_note"]
    with COPY_TABLE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    plan = f"""# B78 - German Presentation Implementation Plan

Date: {today}

## 1. Purpose

B78 defines the implementation plan for the first German presentation version.

It does not implement the website. It translates the decisions from B73-B77 into a safe production patch strategy.

## 2. Strategic decision

The first German presentation version should be:

**Editorial Natur + fachliche Ruhe + kartografische Disziplin**

This means:

- B76_B_editorial_natur is the preferred visual base.
- A-style calm and presentation robustness must be preserved.
- C-style map/source/label discipline must be imported.
- The final page must feel like a warm but serious data essay.

## 3. Target audience and tone

Target group:

**wissenschaftlich informierte Praxisakteure**

Tone:

**narrativ vermittelnd**

Scope:

**kurz und pointiert**

The page should be understandable in a 3-5 minute project walkthrough.

## 4. Core communication goal

The page must not explain the Atlas as a product.

It must explain the subject:

**Moorschutz wird erst dann umsetzbar, wenn globale Klimarelevanz, nationale Planungskulissen, regionale Bodenkontexte und betriebliche Nutzungsperspektiven zusammen betrachtet werden.**

## 5. Production files likely to change in B79

B79 should likely change only:

- `index.html`
- `src/styles.css`
- `tasks/done.md`
- `docs/B79_german_presentation_version.md`
- `scripts/79_apply_german_presentation_version.py`

Possible but not preferred:

- `src/central_stage_label_fix.js` if stage labels need German replacement
- `src/central_step_state_bridge.js` only if metadata labels are visible and need German text

Files that should not be touched:

- map PNGs
- raw data
- GeoJSON
- central layer visibility logic
- central map state controller logic
- retired old scripts
- old data workflows

## 6. Sections in the German presentation version

The visible main flow should become:

1. Problem
2. Kernargument
3. Kartenfolge
4. Regionale Umsetzung
5. Transformationspfade
6. Methodische Grenze

Production mapping:

| Target section | Existing source | Action |
|---|---|---|
| Problem | Hero | Rewrite in German and restyle |
| Kernargument | transitionLogic or existing bridge | Keep/rewrite; reduce meta-language |
| Kartenfolge | centralGlobalMapStory | Keep functionality; rewrite visible text |
| Regionale Umsetzung | new compact section or existing lower intro | Add/convert; use LUBW/SOLAMO framing |
| Transformationspfade | pathways/pathway evidence area | Keep only compact first-level logic |
| Methodische Grenze | methodology/data/prototype appendix area | Keep as boundary, reduce prototype language |

## 7. Text replacement plan

The detailed copy target list is stored in:

- `docs/B78_german_presentation_copy_targets.csv`

High-level replacements:

- `Peatland Transition Atlas` -> `Moorschutz braucht räumliche Orientierung`
- `Portfolio prototype` / `MVP` -> remove
- `Story` -> `Kartenfolge` or `Problem`
- `Evidence Map` -> remove or `Einordnung`
- `Pathways` -> `Pfade`
- `South Germany Fit` -> remove or `Regionale Umsetzung`
- `Method` -> `Methode`
- `Data` -> avoid in main nav; if needed only in source/method area
- `Atlas framing` -> `Kernargument`
- `From peatland extent to transition priorities` -> `Aus Moorbodenkontext wird eine Umsetzungsfrage`
- `Main atlas story` -> `Kartenfolge`
- `Supporting evidence` -> `Einordnung und Vergleich`
- `Prototype appendix` -> `Methodische Grenze`

## 8. CSS implementation direction

The B79 CSS patch should not copy the B76 dummy blindly. It should apply the B-led visual direction to the current production structure.

Recommended CSS changes:

### Base

- page background: warm paper `#F5EFE6` or `#F7F2EA`
- text ink: `#221D18`
- muted text: `#776A5D`
- lines: `#DED4C7`
- primary accent: `#1F4E5F`

### Hero

- remove dark/tech impression
- strong left-aligned H1
- warm paper background
- no product/portfolio language
- three concise claim cards may remain if not too heavy

### Cards

- use subtle warm cards only for grouped arguments
- thin border
- low/no shadow except optional map frame
- avoid equal-weight card overload

### Central map stage

- preserve existing sticky map functionality
- warm surrounding design
- map frame clean and source-aware
- step cards readable
- reduce heavy glow/shadow/tech look
- keep map visually dominant

### Navigation

- German, short, low visual weight
- sticky okay
- no big UI emphasis

### Method boundary

- visible and quiet
- can use white/warm card block
- must clearly say: Einordnung statt Eignungskarte

## 9. Required method boundary text

This sentence must appear in the production version:

**Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.**

This protects the page from overstating BK50/Thünen/BW layer meaning.

## 10. SOLAMO/LUBW integration rule

SOLAMO-BW and LUBW should appear as contextual anchors, not as project promotion.

Use them to support:

- planning frame,
- farm affectedness,
- use concepts,
- value chains,
- policy instruments.

Do not overclaim SOLAMO results if results are not yet available.

## 11. Reversibility

B79 should be generated as a patch script and should:

- create documentation,
- update `tasks/done.md`,
- avoid deleting existing sections,
- prefer text replacement and CSS override,
- preserve retired sections as retired,
- make no raw-data changes.

If needed, use comments such as:

- `<!-- B79 German presentation version -->`
- `/* B79 German presentation design */`

## 12. QA after B79

After B79 implementation, run:

```powershell
python scripts\58_visual_qa_and_commit_check.py
python scripts\72_public_mvp_quality_pass.py
```

Then manually check:

1. no visible `prototype`, `MVP`, `portfolio`, `dashboard`, `appendix` in main flow,
2. page is German in the main visible presentation path,
3. central map still works,
4. BW states still work,
5. retired sections remain hidden,
6. method boundary is visible,
7. public page matches local after cache-busted URL.

## 13. Commit strategy for B79

Expected staged files for implementation:

```text
index.html
src/styles.css
docs/B79_german_presentation_version.md
scripts/79_apply_german_presentation_version.py
tasks/done.md
docs/B58_visual_qa_and_commit_check.md
docs/B72_public_mvp_quality_report.md
```

If central stage label JS is touched, stage it explicitly and document why.

Do not stage:

- `data/`
- old scripts
- old tasks
- raw GIS files
- unrelated README files

## 14. Acceptance criteria

The German presentation version is acceptable when:

1. the main page no longer looks like a technical prototype,
2. the visible main flow is German,
3. the hero states the substantive problem,
4. the map sequence remains the central argument,
5. LUBW/SOLAMO context supports regional implementation,
6. the design feels warm but professional,
7. method boundaries are explicit,
8. a project audience can follow the page in 3-5 minutes.
"""

    patch = f"""# B78 - Patch Strategy for B79

Date: {today}

## 1. Recommended B79 approach

B79 should be a single conservative patch:

`79_apply_german_presentation_version.py`

It should:

1. read `index.html`,
2. apply targeted text replacements,
3. inject or append B79 CSS overrides in `src/styles.css`,
4. add a short regional implementation block if needed,
5. create `docs/B79_german_presentation_version.md`,
6. update `tasks/done.md`.

## 2. Safer than manual editing

Manual editing is risky because:

- the page has multiple retired sections,
- central map state binding must stay intact,
- old scripts have been retired but not deleted,
- previous patches showed encoding risk with PowerShell.

Therefore B79 should write UTF-8 LF and avoid PowerShell `Set-Content`.

## 3. Text replacement strategy

Use precise replacements where possible.

Avoid broad regex replacements that might touch hidden/retired sections unless intended.

Priority order:

1. Hero and nav
2. Transition logic / argument block
3. Central map section headings and visible steps
4. Lower evidence headings
5. Method boundary
6. Source/caption cleanup

## 4. CSS strategy

Do not remove old CSS.

Append a clear B79 override block at the end:

```css
/* B79 German presentation version */
...
```

Benefits:

- reversible,
- low risk,
- easy diff,
- avoids breaking older layout.

## 5. What not to do in B79

Do not:

- delete sections,
- delete scripts,
- rewrite map JS,
- touch map PNGs,
- add new data,
- add external fonts,
- add decorative photos,
- create a new interaction model,
- change central map state names.

## 6. Rollback

If B79 looks wrong:

```powershell
git checkout -- index.html src/styles.css tasks/done.md
```

If docs/scripts are uncommitted:

```powershell
del docs\B79_german_presentation_version.md
del scripts\79_apply_german_presentation_version.py
```

If already committed:

```powershell
git revert <commit>
```

## 7. Next decision before B79

Before implementation, confirm:

- Should the production page be fully German, or only the main presentation path?
- Should old lower sections remain visible after the German short path, or be further reduced?
- Should the navigation link to data/source material remain, or only to method?
"""

    write(PLAN, plan)
    write(PATCH_BRIEF, patch)
    write_copy_table()

    done_entry = f"""
## B78 - German presentation implementation plan ({today})

- Created `docs/B78_german_presentation_implementation_plan.md`.
- Created `docs/B78_german_presentation_copy_targets.csv`.
- Created `docs/B78_patch_strategy.md`.
- Defined safe B79 production implementation strategy.
- Did not modify production website files, CSS, scripts, maps or data.
"""
    current = read(DONE) if DONE.exists() else "# Done
"
    if "## B78 - German presentation implementation plan" not in current:
        write(DONE, current.rstrip() + "
" + done_entry)

    print("B78 German presentation implementation plan complete.")
    print("Changed/created:")
    print(f"  {rel(PLAN)}")
    print(f"  {rel(COPY_TABLE)}")
    print(f"  {rel(PATCH_BRIEF)}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
