# B167b - Restore BW Layer to Sticky Zoom

Date: 2026-07-01

## Ziel

B167 hatte den Sticky-Zoom-Prototyp grundsätzlich repariert, aber die frühere Baden-Württemberg-Ebene fehlte noch als eigene Maßstabsstufe.

B167b stellt diese Ebene im isolierten Prototyp wieder her:

```text
Deutschland → Baden-Württemberg → Oberschwaben
```

## Warum

Ohne BW-Step springt die Story zu schnell von Deutschland nach Oberschwaben.
Der BW-Layer ist die redaktionelle Brücke:

```text
nicht mehr nationale Kulisse,
noch nicht regionale Detailkarte.
```

## Änderung

Der Prototyp enthält jetzt einen zusätzlichen State:

```text
baden-wuerttemberg
```

mit:

```text
base:    public/maps/bw/bw_bk50_moor_extent.png
overlay: public/maps/bw/bw_admin_context.png
```

## Neue Stepfolge

| Nr. | State | Basis | Overlay |
|---:|---|---|---|
| 1 | `global-peat` | `public/maps/global/global_gpm2_peat_extent.png` | `public/maps/global/global_country_borders.png` |
| 2 | `global-pressure-total` | `public/maps/global/global_hotspots_total.png` | `public/maps/global/global_country_borders.png` |
| 3 | `global-pressure-density` | `public/maps/global/global_hotspots_density.png` | `public/maps/global/global_country_borders.png` |
| 4 | `europe-bridge` | `public/maps/europe/europe_gpm2_peat_extent.png` | `public/maps/europe/europe_country_borders.png` |
| 5 | `germany-extent` | `public/maps/germany/germany_thuenen_moor_extent.png` | `public/maps/germany/germany_admin_context.png` |
| 6 | `germany-types` | `public/maps/germany/germany_thuenen_moor_types.png` | `public/maps/germany/germany_admin_context.png` |
| 7 | `baden-wuerttemberg` | `public/maps/bw/bw_bk50_moor_extent.png` | `public/maps/bw/bw_admin_context.png` |
| 8 | `oberschwaben-handoff` | `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png` | `public/maps/oberschwaben/oberschwaben_admin_context.png` |

## Nicht geändert

- keine Änderung an `index.html`
- keine Änderung an `src/styles.css`
- keine Änderung an der öffentlichen Hauptseite
- keine neuen Kartenexports
- keine raw GIS-Dateien

## Visuelle Prüfung

Prüfen:

- BW-Step erscheint zwischen Deutschland und Oberschwaben.
- BW-Layer zeigt den BK50-Moor-/Feuchtbodenkontext.
- BW-Admin-Overlay passt räumlich.
- Oberschwaben-Step bleibt danach enger und regionaler.
- Acht Steps sind noch rhythmisch tragbar.
