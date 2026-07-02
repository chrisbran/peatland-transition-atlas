# B145 - Felt Pilot Build Sheet

Date: 2026-06-30

## Ziel

B145 beschreibt den manuellen Aufbau der Oberschwaben-Pilotkarte in Felt.
Es wird noch keine Karte in die öffentliche Seite eingebunden.

B145 setzt auf dem B143/B144-Pfad auf:

```text
ArcGIS -> EPSG:4326 -> GeoJSON -> mapshaper -> Felt -> iframe-Test
```

## Eingangsdaten

Erwartete lokale Pilotdatei:

```text
working/oberschwaben_felt_pilot/oberschwaben_schnittmenge_simpel.geojson
```

Diese Datei bleibt lokal und wird nicht committed.

Minimal erwartete Felder:

| Feld | Zweck |
|---|---|
| `klasse` | Styling und Filter |
| `flaeche_ha` | Tooltip |
| `landkreis` | Tooltip und Orientierung |
| `hinweis` | optionaler kurzer Kontext |

## Felt-Aufbau

### 1. Neue Karte

- neue Felt-Karte anlegen
- Pilotdatei `oberschwaben_schnittmenge_simpel.geojson` hochladen
- Kartenname intern:
  - `Oberschwaben Moor-/Feuchtbodenkontext Pilot`

### 2. Layer prüfen

Nach Upload prüfen:

- alle Klassen sichtbar
- Geometrien liegen in Baden-Württemberg/Oberschwaben
- keine verschobene Projektion
- Tooltip-Felder sind lesbar
- Schnittmenge ist vorhanden

### 3. Styling

Zentrales Designprinzip:

> Die Schnittmenge ist das Hauptsignal. Alle anderen Klassen sind Kontext.

Klassen sollten nach `klasse` gestylt werden.

Empfohlene Hierarchie:

1. Schnittmenge
2. Moor-/Feuchtbodenkontext
3. Grünland / Ackerland / Dauerkultur als Nutzungskontext

### 4. Direktannotation

Mindestens drei Annotationen setzen:

- `Schnittmenge = Prüfbedarf, nicht Eignung`
- Landkreisnamen:
  - Biberach
  - Ravensburg
  - Sigmaringen
  - Bodenseekreis
- ein kurzer Callout auf ein gut erkennbares Schnittmengen-Cluster:
  - `Hier überlagern sich Nutzung und Moor-/Feuchtbodenkontext`

Optional:

- dezenter Pfeil auf die stärkste Clusterzone
- Maßstabs-/Lesehinweis:
  - `BK50-Kontext, keine parzellenscharfe Eignung`

### 5. Tooltip

Tooltip nur mit diesen Feldern:

```text
klasse
flaeche_ha
landkreis
```

Optional:

```text
hinweis
```

Nicht zeigen:

- interne IDs
- technische Arbeitsfelder
- lange ArcGIS-Feldnamen
- Zwischenberechnungen

### 6. Share / Embed

Noch nicht direkt in `index.html` einfügen.

Zunächst nur:

- Sichtbarkeit prüfen
- Embed-Code kopieren
- in `docs/B145_felt_embed_candidate_template.txt` dokumentieren
- Datenschutz-/Lizenzfrage notieren
- mobile Darstellung manuell testen

## Erfolgskriterien

Der Pilot ist nur überzeugend, wenn:

- Schnittmenge sofort sichtbar ist
- Karte weniger nach GIS-Export aussieht
- direkte Labels einen Teil der Legende ersetzen
- Tooltip echte Zusatzinformation liefert
- mobile Darstellung nicht schlechter als die PNG-Version ist
- Ladezeit akzeptabel ist
- bestehende V2-Seite unangetastet bleibt

## Nicht-Ziele

B145 macht nicht:

- keine Änderung an `index.html`
- keine Änderung an `src/styles.css`
- kein Felt-iframe im Live-HTML
- keine MapLibre-Integration
- keine Datawrapper-Karte
- kein Commit von GeoJSON/GPKG/Shapefile
