# B161 - Flagship Sticky Zoom Implementation Brief

Date: 2026-07-01

## Ziel des späteren Umsetzungspatches

Ein späterer Umsetzungspatch soll die vorhandene zentrale Kartenfolge zu einem Premium-Sticky-Zoom verdichten.

B161 selbst ändert die öffentliche Seite nicht.

## Wahrscheinliche Umsetzungsstrategie

### Phase 1: Inventarisieren und verdichten

- vorhandene `central_global_map_story`-Struktur prüfen
- aktuelle Steps und States auf 5–7 reduzieren
- keine neuen Datenquellen
- keine zusätzliche Kartenbibliothek

### Phase 2: Copy und Step-Logik

Zielstruktur:

```text
00 intro
01 global peat extent
02 global pressure/hotspot
03 europe/germany bridge
04 germany organic soils
05 Baden-Württemberg / regional focus
06 Oberschwaben handoff
```

### Phase 3: Bühnenbild

- Sticky-Stage bleibt groß
- Textspalte wird knapper
- Stage-Labels werden stärker statement-orientiert
- Quellenzeile wird ruhiger
- kein Methodenabschnitt mitten im Sticky

### Phase 4: Mobile

Mobile darf keine schwere Sticky-Mechanik erzwingen.

Mögliche Regel:

```css
@media (max-width: 760px) {
  /* Sticky aus, Kartenpanels sequenziell */
}
```

## Existing asset inventory

Die Datei `docs/B161_flagship_sticky_zoom_asset_inventory.csv` listet die verfügbaren Kartenassets.

Kurzstatus:

| Asset | Status |
|---|---:|
| `public/maps/global/global_gpm2_peat_extent.png` | vorhanden |
| `public/maps/global/global_hotspots_total.png` | vorhanden |
| `public/maps/global/global_hotspots_density.png` | vorhanden |
| `public/maps/global/global_country_borders.png` | vorhanden |
| `public/maps/europe/europe_gpm2_peat_extent.png` | vorhanden |
| `public/maps/europe/europe_country_borders.png` | vorhanden |
| `public/maps/germany/germany_admin_context.png` | vorhanden |
| `public/maps/germany/germany_thuenen_moor_extent.png` | vorhanden |
| `public/maps/germany/germany_thuenen_moor_types.png` | vorhanden |

## Optional gefundene regionale Asset-Verzeichnisse

### `public/maps/bw`

- gefundene Bilddateien: 2
- `public/maps/bw/bw_admin_context.png`
- `public/maps/bw/bw_bk50_moor_extent.png`

### `public/maps/oberschwaben`

- gefundene Bilddateien: 4
- `public/maps/oberschwaben/oberschwaben_admin_context.png`
- `public/maps/oberschwaben/oberschwaben_agriculture.png`
- `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png`
- `public/maps/oberschwaben/oberschwaben_moor_context.png`

### `public/maps/regional`

- gefundene Bilddateien: 0

## Technische Vorsicht

Nicht sofort `index.html` hart umbauen.

Empfohlene Reihenfolge:

```text
B161 Konzept
B162 Wertschöpfungs-Climax-Konzept
B163 Caveat-Reduction
B164 Premium-Pacing
B165 erst dann: Flagship-Zoom-Prototyp
```

Warum: Der Sticky-Zoom muss zur gekürzten Dramaturgie passen. Wenn wir ihn zu früh bauen,
zementieren wir eventuell die aktuelle Überfülle.

## QA-Anforderungen für späteren Umsetzungspatch

- B103b visible findings: 0
- B58 PASS
- Desktop: Sticky-Stage sauber
- Mobile: kein blockierendes Scrollytelling
- keine neuen raw GIS-Dateien
- kein `git add .`
