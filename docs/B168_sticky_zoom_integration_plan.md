# B168 - Sticky Zoom Integration Plan

Date: 2026-07-01

## Ziel

B168 plant die Integration des reparierten B167b-Sticky-Zooms in die bestehende Hauptseite.

Wichtig: B168 ist **kein** Seitenumbau. Der Patch dokumentiert, wie B169 später sauber integriert werden soll.

## Leitentscheidung

```text
Nicht den Prototyp-HTML-Block in die Hauptseite kopieren.
Die bestehende dunkle zentrale Kartenbühne behalten und mit der B167b-State-Logik verdichten.
```

Warum:

- die aktuelle Hauptseiten-Kartenstory ist technisch stabil
- die dunkle Bühne wirkt bereits hochwertig
- B165/B167b lösen die State- und Layerlogik
- die Integration soll bestehende Controller nutzen, nicht eine zweite Scrolly-Architektur einführen

## Zielsequenz

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

## Status

- Zielstates im B167b-Prototyp vorhanden: 8/8
- Zielstates oder Aliase in `index.html` vorhanden: 5/8
- Zielassets vorhanden: True

## Integrationsprinzip für B169

### 1. Bestehende zentrale Kartenstory verwenden

B169 soll die vorhandene zentrale Story verdichten:

```text
bestehender dunkler Scrolly → neue 8-Step-State-Matrix
```

Nicht:

```text
B165-Prototyp als neuen zweiten Sticky-Block einfügen
```

### 2. State-Aliase sauber auflösen

Einige alte States heißen anders:

| Zielstate | mögliche bestehende Aliase |
|---|---|
| `global-pressure-total` | `global-pressure` |
| `europe-bridge` | `europe-peat` |
| `germany-extent` | `germany-thuenen-extent` |
| `germany-types` | `germany-thuenen-types` |

B169 sollte entweder:

- alte Aliase beibehalten und sauber mappen, oder
- alles auf die neue State-Nomenklatur umstellen.

Empfehlung:

```text
Neue State-Namen verwenden, aber JS robust gegen alte Aliase halten.
```

### 3. Karte und Text gemeinsam kürzen

Die zentrale Kartenfolge soll nicht nur technisch neue States bekommen.
Sie soll editorial kürzer werden:

```text
aktuelle längere Kartenstory → 8 starke Steps
```

### 4. Oberschwaben bleibt Übergabe, nicht Ersatz

Der letzte Step `oberschwaben-handoff` ist nur die Brücke zur bestehenden regionalen Story.

Er darf nicht ersetzen:

- die statische Oberschwaben-Layerkarte
- den Felt-Block
- die Flächenbilanz

### 5. Mobile nicht überlasten

Desktop darf Sticky bleiben.
Mobile sollte eine einfache vertikale Sequenz bekommen oder die bestehende mobile Fallback-Logik behalten.

## B169-Gates

B169 darf erst umgesetzt werden, wenn diese Punkte akzeptiert sind:

1. 8 Steps sind rhythmisch noch tragbar.
2. Total- und Density-Karte bleiben beide, oder eine wird bewusst gestrichen.
3. BW-Step bleibt als eigene Brücke.
4. Oberschwaben-Step nutzt ausschließlich passende regionale Grenzen.
5. B58 bleibt PASS.
6. B103b zeigt keine sichtbaren Findings.

## Nicht-Ziele für B169

- kein Felt-Umbau
- keine neue Datenquelle
- keine MapLibre-Migration
- kein Löschen der regionalen Oberschwaben-Story
- keine Änderung an Wertschöpfungs-Scorecard
- kein `git add .`

## Dateien

- `docs/B168_live_sticky_zoom_state_plan.csv`
- `docs/B168_b169_implementation_brief.md`
