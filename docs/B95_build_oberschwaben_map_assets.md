# B95 - Build Oberschwaben Map Asset Package

Date: 2026-06-23

## 1. Purpose

B95 prepares the asset package for the Oberschwaben implementation map.

It does not create fake map images and does not bind anything to the website.

## 2. Current result

PNG asset QA result:

**PASS WITH WARNINGS**

This result may be `PASS WITH WARNINGS` if the composite map has not yet been exported. That is expected at this stage.

## 3. Main outputs

- `public/maps/oberschwaben/oberschwaben_map_sources.json`
- `docs/B95_oberschwaben_asset_manifest.csv`
- `docs/B95_oberschwaben_source_candidate_scan.txt`
- `docs/B95_oberschwaben_png_asset_qa.md`
- `docs/B95_oberschwaben_manual_export_checklist.md`
- `tasks/B96_bind_oberschwaben_map_section.md`

## 4. Source-anchor logic

B95 uses the B94 source anchors:

- Gemeinsamer Antrag Baden-Württemberg / MLR 2024 for agriculture,
- GeoLa BK50MOOR / LGRB 2025 for Moor-/Feuchtbodenkontext,
- BKG or compatible public administrative boundaries for county context.

## 5. First visible asset needed before website binding

```text
public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
```

Until this file exists and passes visual review, B96 should not bind the module into `index.html`.

## 6. Method boundary

The map package uses this boundary:

```text
Die Oberschwaben-Karten zeigen eine räumliche Einordnung der Überschneidung von landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```

## 7. Candidate source scan

Candidate source-like files were scanned into:

- `docs/B95_oberschwaben_source_candidate_scan.txt`

This is a discovery aid only. It does not mean the files are approved inputs.

## 8. Next step

Export or create the first composite map asset manually or through a dedicated GIS workflow.

Then rerun B95 and proceed to B96 only after:

1. composite PNG exists,
2. source metadata are acceptable,
3. legend wording is approved,
4. visual review passes.
