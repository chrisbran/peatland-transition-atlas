#!/usr/bin/env python3
"""
B113 - Public release notes and method documentation

Documentation-only patch:
- no index.html changes
- no CSS changes
- no map/data processing
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

RELEASE_NOTES = DOCS / "B113_public_release_notes.md"
METHOD_DOC = DOCS / "B113_method_documentation.md"
CHECKLIST = DOCS / "B113_release_checklist.md"
AUDIT = DOCS / "B113_public_release_audit.txt"

TODAY = date.today().isoformat()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


RELEASE_NOTES_TEXT = f"""# B113 – Public Release Notes

Stand: {TODAY}

## Current release position

The current public version is a **FIONA-based Oberschwaben story** embedded in the broader Moore / Peatland Transition Atlas narrative.

The project has returned to the FIONA/BK50/GISCO map stack after the temporary LGL source-swap branch was stopped. LGL work from B106–B109 is parked as a technical alternative and is **not** part of the active public story.

## Current public narrative

The atlas follows this sequence:

1. **Global peatland distribution** – peatlands are spatially uneven and globally relevant.
2. **Emission hotspots** – drained organic soils are not only a land-cover issue but a climate-emissions issue.
3. **Europe / Germany** – global patterns are translated into a regional policy and planning context.
4. **Baden-Württemberg / Oberschwaben** – a regional implementation frame is introduced.
5. **Land use × peat/wet-soil context** – the core Oberschwaben map sequence shows where agricultural use and BK50 Moor-/Feuchtbodenkontext overlap.
6. **Pathways and value chains** – the map is translated into questions about use, water level, farm logic, cooperation and value chains.

## Active public map stack

| Level | Main source basis | Current use |
|---|---|---|
| Global | Global Peatland Map 2.0 / Global Peatland Database | Global peatland context maps |
| Global emissions | FAOSTAT drained organic soils / derived hotspot data | Country hotspot ranking and emissions framing |
| Germany | Thünen organic-soils / peat-soils context | Germany organic soils / national context |
| Baden-Württemberg | BK50 / regional peat/wet-soil context | State-level transition into regional frame |
| Oberschwaben soil context | LGRB dBK50 / GeoLa BK50 | BK50 Moor-/Feuchtbodenkontext |
| Oberschwaben agricultural use | FIONA 2024 | Agricultural use layer and FIONA × BK50 intersection |
| Administrative context | GISCO NUTS 2024 / derived county frame | Biberach, Bodenseekreis, Ravensburg, Sigmaringen |

## Active Oberschwaben interpretation

The Oberschwaben map sequence should be read as a **spatial orientation and discussion layer**, not as a site-level intervention map.

The key public figure currently shown is:

```text
~19,900 ha agricultural use in BK50 Moor-/Feuchtbodenkontext
```

The public class split is shown as rounded orientation:

```text
~82 % Grünland
~16 % Ackerland
~2 % Stilllegung or unclear assignment separately reported
```

These values are rounded and should remain tied to the existing method note:

```text
Lesart: Die Werte geben räumliche Orientierung. Sie sind keine Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```

## What the current maps show

The maps show:

- where peatland / organic-soil / wet-soil contexts occur at different scales;
- how global emissions and peatland geography connect;
- how national and regional context layers narrow the question toward Baden-Württemberg and Oberschwaben;
- where agricultural land use overlaps with BK50 Moor-/Feuchtbodenkontext in the current Oberschwaben demonstration;
- which broad land-use classes dominate the overlap.

## What the current maps do not show

The maps do **not** show:

- parcel-level intervention recommendations;
- hydrological feasibility;
- water-management boundaries;
- ownership or farm-level affectedness;
- legal eligibility for funding;
- implementation priority;
- acceptance or governance readiness;
- detailed cost-benefit analysis;
- final suitability for rewetting or paludiculture.

This caveat should remain stable across further edits.

## Known caveats

### FIONA publication and derivative-use caveat

FIONA 2024 remains the active public-story layer for the Oberschwaben agricultural-use map and the BK50 intersection map. However, project documentation must continue to flag that **publication rights and derivative-use clarity for FIONA-based public outputs require explicit confirmation**.

Recommended internal note:

```text
FIONA-based layers are currently used as a demonstration and working state. Before broader public release, usage and publication rights for derived map products should be clarified with the responsible data owner/service provider.
```

### BK50 classification caveat

The BK50 layer used in the atlas is not the complete raw BK50 layer. It is an **own selection and aggregation of Moor-/Feuchtbodenkontext** from LGRB dBK50 / GeoLa BK50.

The exact selection rule for included BK50 classes must be documented separately from the visual map.

### FAOSTAT caveat

FAOSTAT-derived hotspot layers require a reproducible method note:

- exact FAOSTAT domain/table;
- variables/items used;
- years used;
- GWP conversion, if applied;
- download/API date;
- any post-processing logic.

### Thünen caveat

The Germany map should cite the exact Thünen dataset or publication version used for the organic-soils context and should distinguish between:

- publication citation;
- geodata source/download;
- own cartographic conversion.

### Literature caveat

The international literature basis is currently documented as topic clusters. Full bibliographic references should be completed from the literature screening / OpenAlex export before a formal project report or manuscript-style documentation is finalized.

## Parked LGL branch

The LGL Landnutzung WFS branch from B106–B109 was technically tested but parked.

Reason:

- source access and licensing appeared more straightforward than FIONA;
- classification into broad public land-use groups was possible;
- the resulting cartographic layer was too fragmented for the current visual narrative without further generalization;
- the project decision was to stop the LGL map problem for now and continue with the restored FIONA-based public story.

LGL should remain documented as a tested alternative, not as an active public source.

## Current QA status

Current QA expectation:

```text
B103b visible text audit: no public-source changes
B58 visual QA: PASS
```

If B58 returns warnings again, inspect `git status --short` and ensure raw/working folders are not staged.

## Release decision

This version is suitable as a **project MVP / demonstration version** if presented with the caveats above.

For broader public release, the minimum additional steps are:

1. confirm FIONA derivative-publication permissions;
2. complete source register and method documentation;
3. document BK50 selection rules;
4. complete bibliography for all literature-derived claims;
5. perform browser/responsive QA.
"""


METHOD_DOC_TEXT = f"""# B113 – Method Documentation

Stand: {TODAY}

## Purpose

This document records the current method logic behind the public Moore / Peatland Transition Atlas state, with emphasis on the restored FIONA-based Oberschwaben map sequence.

It is intended for project documentation and release review. It is not a replacement for a full reproducibility package.

## Processing chain overview

### 1. Global and country context

**Input concepts**

- Global peatland distribution from Global Peatland Map 2.0 / Global Peatland Database.
- Country-level drained organic-soil emissions from FAOSTAT-derived data.

**Project use**

- Global spatial framing.
- Country hotspot and emissions framing.
- Narrative transition from global distribution to climate relevance.

**Method boundary**

The global maps support orientation and storytelling. They do not establish local intervention priorities.

### 2. Germany and Baden-Württemberg context

**Input concepts**

- Germany organic-soil / peat-soil context from Thünen-related sources.
- Baden-Württemberg BK50 / GeoLa-derived peat/wet-soil context.

**Project use**

- Translate global problem into German and regional planning context.
- Show that the question narrows from global hotspots to specific regional implementation contexts.

**Method boundary**

The Germany and Baden-Württemberg maps are context frames. They do not replace detailed soil, hydrology or land-use verification.

### 3. Oberschwaben spatial frame

Oberschwaben is represented through four counties:

- Biberach
- Bodenseekreis
- Ravensburg
- Sigmaringen

The current administrative frame is derived from GISCO NUTS 2024 / project-processed county geometry.

### 4. BK50 Moor-/Feuchtbodenkontext

**Input**

- LGRB dBK50 / GeoLa BK50 county-level vector data.
- Four relevant county downloads were identified for Biberach, Bodenseekreis, Ravensburg and Sigmaringen.

**Project-derived layers**

The local project contains derived layers corresponding to:

```text
bk50_moor_oberschwaben_raw
bk50_moor_oberschwaben_context
```

**Interpretation**

This is a BK50-derived **Moor-/Feuchtbodenkontext**, not a final hydrological planning or rewetting suitability layer.

**Documentation need**

The exact BK50 class-selection rule must be documented in a dedicated table:

```text
BK50 field / class / unit → include or exclude → reason
```

### 5. FIONA agricultural-use layer

**Input**

- FIONA 2024 / FIONA-Flächeninformation.
- Used as agricultural-use layer for the restored public Oberschwaben story.

**Project-derived layers**

The project used/created derived layers corresponding to:

```text
fiona_2024_oberschwaben_agri3
fiona_2024_oberschwaben_agri3_dissolved
agriculture_bk50_intersection_oberschwaben
agriculture_bk50_intersection_oberschwaben_dissolved
```

**Classification logic**

FIONA land-use classes were grouped into broad public classes:

```text
Grünland
Ackerland
Dauerkultur / Sondernutzung where applicable
Stilllegung or unclear assignment separately reported
```

**Documentation need**

A final method appendix should include:

- source field(s) used for classification;
- lookup table from original FIONA class to public class;
- handling of unclear/review classes;
- date/version of FIONA service/data;
- legal/publication-use clarification.

### 6. FIONA × BK50 intersection

**Purpose**

The intersection answers the regional orientation question:

```text
Where does agricultural use overlap with BK50 Moor-/Feuchtbodenkontext in Oberschwaben?
```

**Derived figure**

The current public value is rounded:

```text
~19,900 ha agricultural use in BK50 Moor-/Feuchtbodenkontext
```

**Class split**

```text
~82 % Grünland
~16 % Ackerland
~2 % Stilllegung or unclear assignment separately reported
```

These values are public-orientation numbers, not a regulatory area statement.

### 7. Cartographic treatment

The active Oberschwaben cartographic logic is:

```text
admin context
→ agricultural use
→ BK50 Moor-/Feuchtbodenkontext
→ agricultural use × BK50 intersection
```

Analytical layers and cartographic layers are not identical:

- analytical layers support area calculations and QA;
- dissolved/cartographic layers support readable web maps.

This distinction explains why earlier FIONA maps looked calmer than raw LGL test maps.

### 8. LGL replacement branch

**Status**

Parked.

**Reason**

LGL Landnutzung WFS was tested as a possible public-safe replacement for FIONA. It proved technically usable, but cartographic fragmentation was too high for the current public story without additional generalization.

**Implication**

LGL outputs should not be mixed into the active FIONA-based public page.

## Interpretation rules for public communication

Use formulations like:

```text
Die Karte zeigt räumliche Schnittmengen und Planungskontexte.
```

Avoid formulations like:

```text
Die Karte zeigt Wiedervernässungspotenzial.
Die Karte zeigt geeignete Flächen.
Die Karte priorisiert Maßnahmen.
Die Karte zeigt betroffene Betriebe.
```

## Minimum reproducibility package still needed

For a stronger release package, create or finalize:

1. **Source register**  
   `docs/B110_external_source_register.md`

2. **BK50 class-selection table**  
   original BK50 class → included/excluded → rationale

3. **FIONA classification table**  
   original FIONA use/class → public class → review flag

4. **FAOSTAT processing note**  
   source table, years, variables, GWP conversion

5. **Map asset manifest**  
   public PNG → source layers → export date → software → extent/projection

6. **Rights and caveats note**  
   FIONA derivative-use clarification, LGRB attribution, FAOSTAT attribution, GISCO attribution

## Suggested public source line

For the current public page:

```text
Datenbasis: Global Peatland Map 2.0; FAOSTAT drained organic soils; Thünen-Kulisse organischer Böden; Regierungspräsidium Freiburg – LGRB, dBK50 / GeoLa BK50; FIONA 2024; GISCO NUTS 2024; eigene Auswahl, Klassifikation, Verschneidung und kartografische Aufbereitung.
```

For Oberschwaben specifically:

```text
Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024; eigene Auswahl, Klassifikation und Verschneidung. Werte gerundet.
```

## Known release blockers

| Blocker | Severity | Action |
|---|---:|---|
| FIONA public derivative-use rights | high | clarify before broad public dissemination |
| BK50 inclusion rule missing as table | medium | document class selection |
| FAOSTAT reproducibility note incomplete | medium | add source/API/method note |
| Literature references incomplete | medium | complete DOI/author/year list |
| Responsive/browser QA pending | medium | run final visual QA |
"""


CHECKLIST_TEXT = f"""# B113 – Release Checklist

Stand: {TODAY}

## A. Current technical state

- [ ] `python scripts\\103b_corrected_visible_text_audit.py` runs without changing public source files.
- [ ] `python scripts\\58_visual_qa_and_commit_check.py` returns `RESULT: PASS`.
- [ ] `git status --short` contains no staged raw/working data.
- [ ] `index.html` contains no active `oberschwaben_lgl` reference.
- [ ] `index.html` contains no `Datenquelle in Umstellung`.
- [ ] `index.html` contains the current Oberschwaben source note: `FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024`.

## B. Public story checks

- [ ] Global peatland story is understandable without technical explanation.
- [ ] Hotspot/emissions framing does not overclaim precision.
- [ ] Germany/Baden-Württemberg transition is clear.
- [ ] Oberschwaben section clearly explains why this region is shown.
- [ ] Oberschwaben sequence shows: region → use → BK50 context → intersection.
- [ ] Flächenbilanz follows directly from the intersection.
- [ ] Value-chain/pathway section does not read as a finished recommendation catalogue.

## C. Method and source checks

- [ ] Source register exists and is up to date.
- [ ] BK50 selection rule is documented.
- [ ] FIONA classification table is documented.
- [ ] FAOSTAT processing note is documented.
- [ ] Thünen geodata source/version is documented.
- [ ] Literature references have DOI/author/year/journal.
- [ ] LGRB attribution text is included in source register.
- [ ] GISCO attribution is included in source register.
- [ ] FIONA rights/publication status is explicitly marked.

## D. Caveat checks

- [ ] Page does not claim suitability.
- [ ] Page does not claim prioritization.
- [ ] Page does not imply farm-level affectedness.
- [ ] Page does not imply legal eligibility.
- [ ] Page does not claim hydrological feasibility.
- [ ] Page frames maps as orientation and discussion layers.

## E. Visual QA

- [ ] Desktop scroll tested at 1440px width.
- [ ] Desktop scroll tested at 1280px width.
- [ ] Tablet-ish width around 1024px checked.
- [ ] Mobile fallback checked.
- [ ] No sticky heading is clipped.
- [ ] Step cards are readable.
- [ ] Source notes do not dominate the visual flow.
- [ ] Oberschwaben maps remain visually stable through scroll.

## F. Release decision

Recommended release status:

```text
Suitable for internal/project demonstration after B113.
Suitable for broader public release only after FIONA rights clarification and source/method appendix completion.
```
"""


def audit_text(index_text: str) -> str:
    required = [
        "~19.900 ha",
        "FIONA 2024",
        "BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024",
        "eigene Auswahl, Klassifikation und Verschneidung",
        "oberschwaben_agriculture.png",
        "oberschwaben_agriculture_moor_intersection.png",
    ]
    forbidden = [
        "Datenquelle in Umstellung",
        "oberschwaben_lgl",
        "B98c",
        "Flächen-QA",
    ]

    ok_required = True
    ok_forbidden = True

    lines = [
        "# B113 public release audit",
        "",
        f"Date: {TODAY}",
        "",
        "## Required public-state patterns",
        "",
    ]

    for p in required:
        c = index_text.count(p)
        if c < 1:
            ok_required = False
        lines.append(f"- {p}: {c}")

    lines.extend(["", "## Forbidden / parked public-state patterns", ""])
    for p in forbidden:
        c = index_text.count(p)
        if c != 0:
            ok_forbidden = False
        lines.append(f"- {p}: {c}")

    source_register_exists = (DOCS / "B110_external_source_register.md").exists()
    source_register_csv_exists = (DOCS / "B110_external_source_register.csv").exists()

    lines.extend([
        "",
        "## Source register files",
        "",
        f"- docs/B110_external_source_register.md: {'OK' if source_register_exists else 'MISSING'}",
        f"- docs/B110_external_source_register.csv: {'OK' if source_register_csv_exists else 'MISSING'}",
        "",
        "## B113 outputs",
        "",
        f"- {rel(RELEASE_NOTES)}",
        f"- {rel(METHOD_DOC)}",
        f"- {rel(CHECKLIST)}",
        "",
    ])

    status = "OK" if ok_required and ok_forbidden else "REVIEW REQUIRED"
    lines.insert(2, f"Status: **{status}**")
    lines.insert(3, "")

    return "\n".join(lines)


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B113 - Public release notes and method documentation"
    if marker in current:
        return
    entry = f"""
## B113 - Public release notes and method documentation ({TODAY})

- Created public release notes for the restored FIONA-based atlas state.
- Created method documentation for map sources, derived layers, interpretation rules and caveats.
- Created release checklist for source, method, caveat and visual QA.
- Did not modify website, CSS, maps or data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    index_text = read_text(INDEX)

    write_text(RELEASE_NOTES, RELEASE_NOTES_TEXT)
    write_text(METHOD_DOC, METHOD_DOC_TEXT)
    write_text(CHECKLIST, CHECKLIST_TEXT)
    write_text(AUDIT, audit_text(index_text))
    update_done()

    print("B113 public release notes and method documentation complete.")
    print("Changed/created:")
    for p in [RELEASE_NOTES, METHOD_DOC, CHECKLIST, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B113_public_release_audit.txt")
    print("  Get-Content docs\\B113_release_checklist.md")
    print("")
    print("No website, CSS, map or data files were modified.")


if __name__ == "__main__":
    main()
