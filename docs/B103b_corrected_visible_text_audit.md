# B103b - Corrected Visible Text Audit

Date: 2026-06-25

## Result

B103b reran the public text audit with proper inherited hidden/retired-state handling.
No source file was modified.

## Why this was needed

B103 could leak nested text from hidden or retired sections into the visible extract.
B103b separates actual visible text from hidden/retired archive text.

## Created files

- `docs/B103b_corrected_visible_text_audit.md`
- `docs/B103b_visible_text_extract_corrected.txt`
- `docs/B103b_hidden_retired_text_extract.txt`
- `docs/B103b_visible_findings.csv`
- `docs/B103b_hidden_findings.csv`
- `docs/B103b_wording_frequency.csv`

## Corrected visible frequency check

| Pattern group | Count |
|---|---:|
| Umsetzung* | 0 |
| Transform* | 6 |
| Wertschöpfung* | 7 |
| wird zu/zur/zum/eine | 0 |
| übersetz* | 0 |
| Suchkulisse/Gesprächskulisse | 0 |
| prototype/explorer | 0 |
| English cue words | 0 |

## Visible findings summary

| Category | Severity | Count |
|---|---|---:|
| none | none | 0 |

## Hidden/retired findings summary

| Category | Severity | Count |
|---|---|---:|
| language-mix | review | 3 |
| prototype/english | review | 12 |

## Interpretation

- Act only on `B103b_visible_findings.csv` for public wording.
- Use `B103b_hidden_findings.csv` only to decide whether hidden archive sections should remain in the repository.
- Do not remove central map stacks, Oberschwaben layer-stack assets or raw GIS/data folders in a wording pass.

## First visible review candidates

No findings.

## First hidden/retired review candidates

### 1. prototype/english / review: `Prototype`

Context: isting South German dairy and forage systems Bubble size: qualitative GHG mitigation potential Colour: adoption / market barrier Prototype appendix Methode, data and experimental layers. This part documents the prototype status, source limitations and remaining exper

Recommendation: Review if this is truly visible public copy. Remove/translate if visible.

### 2. prototype/english / review: `prototype`

Context: n potential Colour: adoption / market barrier Prototype appendix Methode, data and experimental layers. This part documents the prototype status, source limitations and remaining experimental components. It is supporting material, not a finished decision tool. Method

Recommendation: Review if this is truly visible public copy. Remove/translate if visible.

### 3. prototype/english / review: `prototype`

Context: ining experimental components. It is supporting material, not a finished decision tool. Methode and uncertainty How to read this prototype This Atlas is a literature-driven prototype. It is designed to make evidence, assumptions and transition hypotheses visible, not

Recommendation: Review if this is truly visible public copy. Remove/translate if visible.

### 4. prototype/english / review: `prototype`

Context: ng material, not a finished decision tool. Methode and uncertainty How to read this prototype This Atlas is a literature-driven prototype. It is designed to make evidence, assumptions and transition hypotheses visible, not to replace local hydrological-economic model

Recommendation: Review if this is truly visible public copy. Remove/translate if visible.

### 5. prototype/english / review: `prototype`

Context: contain copyrighted PDFs, confidential project data, licence-unclear raw rasters or unpublished partner data. Data model Current prototype datasets country_hotspots.csv papers.csv transition_pathways.csv region_case_studies.geojson atlas_story_sections.json Regional

Recommendation: Review if this is truly visible public copy. Remove/translate if visible.

### 6. prototype/english / review: `prototype`

Context: ist.toggle('is-active', step.getAttribute('data-state') === state); }); } sections.forEach(function (section) { var steps = Array.prototype.slice.call(section.querySelectorAll('[data-ob-step]')); if (!steps.length) return; setState(section, steps[0].getAttribute('data-

Recommendation: Review if this is truly visible public copy. Remove/translate if visible.

### 7. prototype/english / review: `explorer`

Context: ory Geführte Kartenstory Von Emissions-Hotspots zu realen Moorlandschaften This guided view is the bridge between the existing explorer layers. It turns the atlas into a scroll-driven narrative: country emissions first, then peat/organic-soil extent, and finally th

Recommendation: Review if this is an old explorer/prototype remnant.

### 8. prototype/english / review: `explorer`

Context: untries report large drained-organic-soils emissions? This is a national accounting layer, not a local peatland map. Open hotspot explorer 2 Then reveal the actual peat/organic-soil context Emissions are reported nationally, but transition happens in real landscape

Recommendation: Review if this is an old explorer/prototype remnant.

### 9. prototype/english / review: `evidence explorer`

Context: s Everything after the map is supporting evidence and exploratory interpretation. After the main map The rest of the page is an evidence explorer. Die folgenden Module ordnen die Hauptkarte ein und ergänzen die Argumentation der Seite atlas story, not as a second linear narr

Recommendation: Review if this is an old explorer/prototype remnant.

### 10. prototype/english / review: `Evidence explorer`

Context: it scores are exploratory checks. They support interpretation, but they are not the main storyline. Optionale Hotspot-Vertiefung Evidence explorer: where are drained organic soil emissions concentrated? A first country-level hotspot layer based on FAO/FAOSTAT-derived drained

Recommendation: Review if this is an old explorer/prototype remnant.

### 11. prototype/english / review: `Evidence explorer`

Context: gs. Hotspot classes are exploratory and will be replaced by a geographic choropleth in the next step. International evidence map Evidence explorer: cases and transition evidence Points are approximate visual anchors for study regions, policy nodes and review clusters. They a

Recommendation: Review if this is an old explorer/prototype remnant.

### 12. prototype/english / review: `How to read this prototype`

Context: itations and remaining experimental components. It is supporting material, not a finished decision tool. Methode and uncertainty How to read this prototype This Atlas is a literature-driven prototype. It is designed to make evidence, assumptions and transition hypotheses visible, not

Recommendation: Remove from public version if visible.

### 13. language-mix / review: `Why this layer matters`

Context: actually located within Baden-Württemberg? BK50-Moor features Classes Source area sum Loading Baden-Württemberg BK50-Moor layer… Why this layer matters From national hotspots to real landscapes This regional layer is a first spatial bridge from national drained-organic-soils emi

Recommendation: Review map/body label language. Body copy should be German.

### 14. language-mix / review: `From national`

Context: Baden-Württemberg? BK50-Moor features Classes Source area sum Loading Baden-Württemberg BK50-Moor layer… Why this layer matters From national hotspots to real landscapes This regional layer is a first spatial bridge from national drained-organic-soils emissions to the a

Recommendation: Review map/body label language. Body copy should be German.

### 15. language-mix / review: `from national`

Context: K50-Moor layer… Why this layer matters From national hotspots to real landscapes This regional layer is a first spatial bridge from national drained-organic-soils emissions to the actual distribution of moor and organic-soil contexts in Baden-Württemberg. Interpretation

Recommendation: Review map/body label language. Body copy should be German.


## Next step

If visible prototype/English findings remain, B104 should remove or translate only those specific public sections.
If B103b shows that prototype/explorer text is hidden, B104 should focus on typos and wording polish instead.
