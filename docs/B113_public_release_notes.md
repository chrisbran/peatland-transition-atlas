# B113 – Public Release Notes

Stand: 2026-06-25

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
