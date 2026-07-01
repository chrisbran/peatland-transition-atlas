# B168 - B169 Implementation Brief

Date: 2026-07-01

## Ziel für B169

Die bestehende zentrale Kartenstory in der Hauptseite soll auf die B167b-Zielmatrix gebracht werden.

## Vorbereitende Analyse

### Index-Indikatoren

| Indikator | Wert |
|---|---:|
| `central_global_map_story` | True |
| `src/central_global_map_story.js` | True |
| `central_layer_state_hardener` | True |
| `central_step_state_bridge` | True |
| `central_stage_label_fix` | True |
| `data-state_count` | 11 |

### Gefundene Index-States / Aliase

```text
agriculture
baden-wuerttemberg
europe-peat
extent
germany-thuenen-extent
germany-thuenen-types
global-peat
intersection
method-boundary
moor-context
region
```

### B167b-Prototyp-States

```text
global-peat
global-pressure-total
global-pressure-density
europe-bridge
germany-extent
germany-types
baden-wuerttemberg
oberschwaben-handoff
```

## Empfohlene B169-Strategie

### Schritt 1: Backup vermeiden, aber Patch idempotent machen

B169 soll keine `_backup_before_*`-Ordner erzeugen.
Der Patch muss vorhandene B169-Blöcke entfernen/ersetzen können.

### Schritt 2: Zentrale Section finden

Suchanker:

```text
central_global_map_story
Moore sind räumlich konzentriert
data-state
global_gpm2_peat_extent
```

### Schritt 3: Step-Texte auf 8 Steps ersetzen

Neue Live-Texte:

| Nr. | Kicker | Titel |
|---:|---|---|
| 01 | Welt | Kleine Fläche, große Wirkung |
| 02 | Gesamt | Wo ist der gesamte Emissionsdruck hoch? |
| 03 | Intensität | Wo ist der Druck pro Fläche besonders hoch? |
| 04 | Europa | Aus Relevanz wird Planung |
| 05 | Deutschland | Die nationale Karte zeigt, wo genauer hingesehen werden muss |
| 06 | Bodenkontext | Nicht jeder Moorboden stellt dieselbe Frage |
| 07 | Baden-Württemberg | Jetzt wird die Frage regional |
| 08 | Oberschwaben | Hier trifft Moorschutz auf Landwirtschaft |

### Schritt 4: State-to-layer-Mapping in JS/CSS prüfen

B169 muss sicherstellen:

```text
global-peat              -> global_gpm2_peat_extent + global_country_borders
global-pressure-total    -> global_hotspots_total + global_country_borders
global-pressure-density  -> global_hotspots_density + global_country_borders
europe-bridge            -> europe_gpm2_peat_extent + europe_country_borders
germany-extent           -> germany_thuenen_moor_extent + germany_admin_context
germany-types            -> germany_thuenen_moor_types + germany_admin_context
baden-wuerttemberg       -> bw_bk50_moor_extent + bw_admin_context
oberschwaben-handoff     -> oberschwaben_agriculture_moor_intersection + oberschwaben_admin_context
```

### Schritt 5: QA

Nach B169:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Manuell:

- Desktop Scrolly komplett durchscrollen
- Mobile 390px prüfen
- Total/Density unterscheidbar
- BW-Step sichtbar
- Oberschwaben-Step nicht mit Deutschland-Grenzen
- Übergang zur bestehenden Oberschwaben-Section ohne Dopplung

## Entscheidungsfrage vor B169

Acht Steps sind fachlich sauber.
Falls es beim Scrollen zu lang wirkt, gibt es zwei Kürzungsvarianten:

### Variante A - Total streichen

```text
global-pressure-density bleibt
global-pressure-total entfällt
```

Vorteil: kürzer, stärker flächenbezogen.

### Variante B - Germany types streichen

```text
germany-extent bleibt
germany-types entfällt
```

Vorteil: Maßstabssprung bleibt erhalten, weniger nationale Detailtiefe.

## Empfehlung

Für den ersten Live-Integrationsprototyp: alle 8 Steps testen.
Danach auf 7 kürzen, falls der Rhythmus bricht.
