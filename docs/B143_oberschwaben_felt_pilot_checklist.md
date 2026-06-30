# B143 - Oberschwaben Felt Pilot Checklist

Date: 2026-06-30

## Ziel

Diese Checkliste fuehrt den Kartenpilot fuer Oberschwaben von ArcGIS ueber GeoJSON und mapshaper nach Felt.
Sie dient als Arbeitsliste, nicht als bereits umgesetzter Code.

## 1. Datenstruktur festlegen

Empfehlung:

- ein gemeinsamer Layer mit Feld `klasse`
- Werte:
  - `Ackerland`
  - `Gruenland`
  - `Dauerkultur`
  - `Moor-/Feuchtbodenkontext`
  - `Schnittmenge`

Alternativ kann die Schnittmenge als separater Layer bleiben, wenn sie aus dem Intersect bereits sauber getrennt vorliegt.

## 2. Projektion

In ArcGIS:

- Koordinatensystem prüfen
- falls EPSG:25832 oder anderes deutsches System: mit **Project** nach EPSG:4326 / WGS84 umprojizieren
- nicht `Define Projection` verwenden

## 3. Attribute bereinigen

Behalten:

- `klasse`
- `flaeche_ha`
- `landkreis`
- optional `hinweis`

Entfernen:

- interne IDs
- Arbeitsfelder
- Zwischenberechnungen
- lange technische Feldnamen

## 4. GeoJSON exportieren

In ArcGIS:

- `Features To JSON`
- Option `Output to GeoJSON` aktivieren
- Datei:
  - `oberschwaben_schnittmenge_4326.geojson`

## 5. mapshaper

In mapshaper:

- Datei importieren
- Simplify:
  - Visvalingam / weighted area
  - prevent shape removal aktivieren
  - 5-15 % testen
- Console:
  - `-clean`
- Export:
  - GeoJSON
  - Datei:
    - `oberschwaben_schnittmenge_simpel.geojson`

Ziel:

- moeglichst unter 2-3 MB
- kleine Schnittmengen-Cluster bleiben sichtbar

## 6. Felt-Gestaltung

Layer nach `klasse` stylen.

Startpalette:

| Klasse | Rolle | Styling |
|---|---|---|
| Ackerland | Kontext | warmes Ocker/Sand, gedämpft |
| Gruenland | Kontext | Salbeigrün, gedämpft |
| Dauerkultur | Kontext | Aubergine/Violett, gedämpft |
| Moor-/Feuchtbodenkontext | Kontext | Blaugrau, mittlere Deckkraft |
| Schnittmenge | Hauptsignal | kräftiges Petrol/Dunkeltürkis, hohe Deckkraft |

## 7. Annotationen

Direkt auf der Karte setzen:

- Landkreisnamen
- Label fuer groesstes Schnittmengen-Cluster
- kurzer Hinweis:
  - `Schnittmenge = Prüfbedarf, nicht Eignung`
- optional Pfeil/Callout zur dichtesten Clusterzone

## 8. Tooltip

Nur wenige Felder anzeigen:

- `klasse`
- `flaeche_ha`
- `landkreis`

Keine technischen Felder.

## 9. Embed-Test

- Felt-Karte auf oeffentlich / anyone with link stellen
- iframe-Code sichern
- noch nicht direkt in die Hauptseite committen
- zuerst lokale Testdatei oder separaten Prototyp verwenden

## 10. Entscheidung nach Test

Uebernehmen, wenn:

- Schnittmenge sofort sichtbar ist
- mobile Darstellung akzeptabel ist
- Ladezeit gut ist
- Datenschutz/Lizenz geklärt ist
- bestehende PNG-Version als Fallback erhalten bleibt
