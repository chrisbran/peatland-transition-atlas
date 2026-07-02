# B169 - Live Sticky Zoom Integration Prototype

Date: 2026-07-01

## Ziel

B169 integriert die reparierte B167b-State-Matrix als Live-Prototyp in die öffentliche Hauptseite.

Wichtig: Der Prototyp-HTML-Block aus `docs/prototypes` wurde nicht kopiert.
Stattdessen ersetzt B169 die bestehende zentrale Kartenfolge durch eine kompakte Live-Komponente,
die die dunkle Kartenbühnen-Richtung beibehält.

## Neue Live-Stepfolge

| Nr. | State | Aussage | Basis | Overlay |
|---:|---|---|---|---|
| 1 | `global-peat` | Kleine Fläche, große Wirkung | `public/maps/global/global_gpm2_peat_extent.png` | `public/maps/global/global_country_borders.png` |
| 2 | `global-pressure-total` | Wo ist der gesamte Emissionsdruck hoch? | `public/maps/global/global_hotspots_total.png` | `public/maps/global/global_country_borders.png` |
| 3 | `global-pressure-density` | Wo ist der Druck pro Fläche besonders hoch? | `public/maps/global/global_hotspots_density.png` | `public/maps/global/global_country_borders.png` |
| 4 | `europe-bridge` | Aus Relevanz wird Planung | `public/maps/europe/europe_gpm2_peat_extent.png` | `public/maps/europe/europe_country_borders.png` |
| 5 | `germany-extent` | Die nationale Karte zeigt, wo genauer hingesehen werden muss | `public/maps/germany/germany_thuenen_moor_extent.png` | `public/maps/germany/germany_admin_context.png` |
| 6 | `germany-types` | Nicht jeder Moorboden stellt dieselbe Frage | `public/maps/germany/germany_thuenen_moor_types.png` | `public/maps/germany/germany_admin_context.png` |
| 7 | `baden-wuerttemberg` | Jetzt wird die Frage regional | `public/maps/bw/bw_bk50_moor_extent.png` | `public/maps/bw/bw_admin_context.png` |
| 8 | `oberschwaben-handoff` | Hier trifft Moorschutz auf Landwirtschaft | `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png` | `public/maps/oberschwaben/oberschwaben_admin_context.png` |

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `src/b169_live_sticky_zoom.js`
- `scripts/169_live_sticky_zoom_integration_prototype.py`
- `docs/B169_live_sticky_zoom_integration_prototype.md`
- `docs/B169_live_sticky_zoom_state_matrix.csv`
- `docs/B169_live_sticky_zoom_integration_prototype_audit.txt`
- `tasks/done.md`

## Nicht geändert

- keine Änderung an Felt
- keine Änderung an der Oberschwaben-Detailkarte
- keine Änderung an Flächenbilanz
- keine Änderung an Wertschöpfungs-Scorecard
- keine neuen Datenquellen
- keine raw GIS-Dateien

## Visuelle QA

Prüfen:

1. Desktop: Sticky-Zoom scrollt sauber.
2. Global: Total- und Density-Step sind unterscheidbar.
3. Europa: politische Grenzen helfen, ohne dominant zu werden.
4. Deutschland: Extent und Types sind klar getrennt.
5. Baden-Württemberg: BW-Layer erscheint als eigene Brücke.
6. Oberschwaben: kein Deutschland-Overlay.
7. Danach funktioniert die bestehende Oberschwaben-Section ohne Dopplungsgefühl.
8. Mobile: vertikale Sequenz bleibt lesbar.

## Entscheidung nach visueller QA

Falls acht Steps zu lang wirken:

- Variante A: `global-pressure-total` streichen, Density behalten.
- Variante B: `germany-types` streichen, Germany extent behalten.

Für den ersten Live-Test bleiben alle acht Steps aktiv.
