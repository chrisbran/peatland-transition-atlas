# B167 - Sticky Zoom State Repair

Date: 2026-07-01

## Ziel

B167 repariert den isolierten B165/B165b-Sticky-Zoom-Prototyp nach der B166-Inventur.

B166 hatte zwei konkrete Probleme markiert:

1. Die vorhandene globale Emissionsintensitätskarte `global_hotspots_density.png` fehlte im Prototyp.
2. Der regionale Oberschwaben-Step war falsch gekoppelt: regionale Basiskarte plus Deutschland-Admin-Overlay.

## Änderungen

### 1. Globaler Druck getrennt

Alt:

```text
global-pressure -> global_hotspots_total.png
```

Neu:

```text
global-pressure-total   -> global_hotspots_total.png
global-pressure-density -> global_hotspots_density.png
```

Damit unterscheidet der Prototyp jetzt zwischen:

- absolutem Gesamt-Emissionsdruck
- Emissionsintensität pro Fläche

### 2. Regional-Step repariert

Alt:

```text
regional-handoff base    = regionales Oberschwaben-Asset
regional-handoff overlay = germany_admin_context.png
```

Neu:

```text
oberschwaben-handoff base    = regionales Oberschwaben-Asset
oberschwaben-handoff overlay = passendes regionales Overlay, falls vorhanden
```

Die Deutschland-Grenzen werden im Regional-Step nicht mehr als Overlay verwendet.

### 3. Prototyp neu geschrieben

Der isolierte Prototyp bleibt:

```text
docs/prototypes/B165_flagship_sticky_zoom_prototype.html
```

Die Hauptseite bleibt unverändert.

## Finale Stepfolge im Prototyp

| Nr. | State | Basis | Overlay |
|---:|---|---|---|
| 1 | `global-peat` | `public/maps/global/global_gpm2_peat_extent.png` | `public/maps/global/global_country_borders.png` |
| 2 | `global-pressure-total` | `public/maps/global/global_hotspots_total.png` | `public/maps/global/global_country_borders.png` |
| 3 | `global-pressure-density` | `public/maps/global/global_hotspots_density.png` | `public/maps/global/global_country_borders.png` |
| 4 | `europe-bridge` | `public/maps/europe/europe_gpm2_peat_extent.png` | `public/maps/europe/europe_country_borders.png` |
| 5 | `germany-extent` | `public/maps/germany/germany_thuenen_moor_extent.png` | `public/maps/germany/germany_admin_context.png` |
| 6 | `germany-types` | `public/maps/germany/germany_thuenen_moor_types.png` | `public/maps/germany/germany_admin_context.png` |
| 7 | `oberschwaben-handoff` | `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png` | `public/maps/oberschwaben/oberschwaben_admin_context.png` |

## Nicht geändert

- keine Änderung an `index.html`
- keine Änderung an `src/styles.css`
- keine Änderung an der öffentlichen Hauptseite
- keine neuen Kartenexports
- keine raw GIS-Dateien

## Visuelle Prüfung

Nach B167 prüfen:

- Total- und Density-Step sind beide sichtbar und unterscheidbar.
- Der Oberschwaben-Step zeigt keine Deutschland-Grenzen mehr als falsches Overlay.
- Regionale Grenzen, falls eingeblendet, passen zur regionalen Karte.
- Sieben Steps sind noch rhythmisch tragbar.
- Falls sieben Steps zu lang wirken: Total oder Density redaktionell priorisieren.
