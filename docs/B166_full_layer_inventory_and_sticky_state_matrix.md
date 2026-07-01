# B166 - Full Layer Inventory and Sticky State Matrix

Date: 2026-07-01

## Ziel

B166 erstellt eine vollständige Inventur der Kartenassets und eine saubere Zielmatrix für den Flagship-Sticky-Zoom.

Auslöser waren zwei Befunde aus der Prototypprüfung:

1. Im Oberschwaben-/Regional-Step wurde ein regionaler Moorlayer mit den politischen Grenzen der Deutschlandkarte kombiniert.
2. Die globale Karte zur Emissionsintensität pro Fläche ist vorhanden, aber im B165-Prototyp nicht eingebunden.

B166 ändert die öffentliche Seite nicht. Es ist ein Inventur- und Entscheidungsdokument für den nächsten Reparaturpatch.

## Ergebnis kurz

- inventarisierte Karten-/Bildassets: 17
- vorhandene Assets: 17
- fehlende erwartete Assets: 0
- regionale Basis-Kandidaten: 6
- regionale Boundary-Kandidaten: 2

## Globale Druckkarten

| Karte | Vorhanden | Aktuell im B165-Prototyp | Bewertung |
|---|---:|---:|---|
| `global_hotspots_total.png` | True | True | Gesamt-Emissionsdruck / absoluter Druck |
| `global_hotspots_density.png` | True | False | Emissionsintensität pro Fläche; muss als eigener Step ergänzt werden |

## State-Matrix Status

| Status | Anzahl |
|---|---:|
| `available_unused` | 1 |
| `ok_current` | 5 |
| `wrongly_paired` | 1 |

## Zielzustand für den Flagship-Sticky-Zoom

| Reihenfolge | State | Basisbild | Overlay | Aussage |
|---:|---|---|---|---|
| 1 | `global-peat` | `public/maps/global/global_gpm2_peat_extent.png` | `public/maps/global/global_country_borders.png` | Kleine Fläche, große Wirkung. |
| 2 | `global-pressure-total` | `public/maps/global/global_hotspots_total.png` | `public/maps/global/global_country_borders.png` | Wo ist der gesamte Emissionsdruck hoch? |
| 3 | `global-pressure-density` | `public/maps/global/global_hotspots_density.png` | `public/maps/global/global_country_borders.png` | Wo ist der Druck pro Fläche besonders intensiv? |
| 4 | `europe-bridge` | `public/maps/europe/europe_gpm2_peat_extent.png` | `public/maps/europe/europe_country_borders.png` | Aus globaler Relevanz wird politische Planung. |
| 5 | `germany-extent` | `public/maps/germany/germany_thuenen_moor_extent.png` | `public/maps/germany/germany_admin_context.png` | Die nationale Karte zeigt, wo genauer hingesehen werden muss. |
| 6 | `germany-types` | `public/maps/germany/germany_thuenen_moor_types.png` | `public/maps/germany/germany_admin_context.png` | Nicht jeder Moorboden stellt dieselbe Frage. |
| 7 | `oberschwaben-handoff` | `REGIONAL_ASSET_REQUIRED` | `MATCHING_REGIONAL_BOUNDARY_REQUIRED_OR_EMBEDDED` | Hier trifft Moorschutz auf Landwirtschaft. |

## Aktuelle Problemstellen

### 1. Globaler Druck muss in zwei Aussagen getrennt werden

Der Prototyp nutzt derzeit `global_hotspots_total.png` als Druckkarte.
Die vorhandene Intensitätskarte `global_hotspots_density.png` fehlt im Ablauf.

Empfohlene Trennung:

```text
global-pressure-total   = Wo ist der gesamte Emissionsdruck hoch?
global-pressure-density = Wo ist der Druck pro Fläche besonders intensiv?
```

Das ist editorial sinnvoll, weil Gesamtmenge und Intensität unterschiedliche Aussagen sind.

### 2. Regional-Handoff darf kein Deutschland-Overlay verwenden

Der letzte Step braucht eine passende regionale Kopplung:

```text
regional base    + regional boundaries
```

oder:

```text
regional base with boundaries already embedded + no additional overlay
```

Nicht verwenden:

```text
regional base + germany_admin_context
```

Das erzeugt die aktuell sichtbare Fehlkopplung.

## Regionale Kandidaten

### Basis-Kandidaten

- `public/maps/bw/bw_bk50_moor_extent.png`
- `public/maps/oberschwaben/oberschwaben_agriculture.png`
- `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png`
- `public/maps/oberschwaben/oberschwaben_moor_context.png`
- `public/maps/oberschwaben_lgl/oberschwaben_lgl_landuse.png`
- `public/maps/oberschwaben_lgl/oberschwaben_lgl_landuse_bk50_intersection.png`

### Boundary-Kandidaten

- `public/maps/bw/bw_admin_context.png`
- `public/maps/oberschwaben/oberschwaben_admin_context.png`

## Entscheidung für den nächsten Patch

Der nächste Patch sollte den B165-Prototyp reparieren:

```text
B167 Sticky Zoom State Repair
```

Pflichten für B167:

1. `global_hotspots_density.png` als eigenen Step ergänzen.
2. `global-pressure` in `global-pressure-total` umbenennen oder sauber auftrennen.
3. `regional-handoff` in `oberschwaben-handoff` umbenennen.
4. Deutschland-Overlay im Regional-Step entfernen.
5. Nur ein regional passendes Overlay verwenden, falls vorhanden.
6. Falls kein regionales Boundary-Overlay vorhanden ist: keine zusätzliche Grenze über den Regional-Step legen und Gate für neuen Regional-Export markieren.

## Dateien

- `docs/B166_map_asset_inventory.csv`
- `docs/B166_sticky_state_matrix.csv`
- `docs/B166_sticky_zoom_repair_recommendations.md`
