# B97g - Clean Remaining Public Copy Red Flags

Date: 2026-06-24

## Result

B97g applied a conservative second editorial cleanup pass to `index.html`.

## Changed files

- `index.html`
- `docs/B97g_clean_remaining_public_copy_red_flags.md`
- `docs/B97g_public_readiness_red_flag_scan_classified.txt`
- `tasks/done.md`

## Replacements applied

- `From national emission hotspots to real peatland landscapes` -> `Von Emissions-Hotspots zu realen Moorlandschaften`: 1
- `A peat/organic-soils map is not a rewetting suitability map` -> `Eine Moor-/organische-Böden-Karte ist keine Wiedervernässungs-Eignungskarte`: 1
- `Use the following modules as interpretation and prototype support for the main` -> `Die folgenden Module ordnen die Hauptkarte ein und ergänzen die Argumentation der Seite`: 1
- `to evidence-informed transition pathways. The matrix is not a prescription; it is a prototype logic for` -> `zu evidenzgestützten Transformationspfaden. Die Matrix ist keine Vorgabe; sie ist eine Arbeitslogik für`: 1
- `<strong>Prototype rule:</strong>` -> `<strong>Arbeitsregel:</strong>`: 1
- `<p class="eyebrow">Phase B hotspot layer</p>` -> `<p class="eyebrow">Optionale Hotspot-Vertiefung</p>`: 1
- `Prototype based on curated literature coding. Scores are qualitative and evidence-map points are approximate visual anchors.` -> `Arbeitsstand auf Basis kuratierter Literaturcodierung. Die Bewertungen sind qualitativ; Evidenzpunkte sind ungefähre visuelle Anker.`: 1

## Residual scan summary

- visible-review: 1
- hidden-retired: 8
- script-false-positive: 1
- scan file: `docs/B97g_public_readiness_red_flag_scan_classified.txt`

## Editorial decisions

- Removed remaining high-confidence visible English/prototype wording.
- Did not touch hidden retired prototype appendix sections.
- Did not touch JavaScript false positives such as `Array.prototype`.
- Did not move Transformationspfade. That remains planned for B99 after B98 quantitative QA.

## Next recommended steps

1. Inspect the classified scan.
2. If visible-review count is zero or acceptable, commit B97f/B97g.
3. Continue with B98: Oberschwaben intersection area and classification QA.
