# B146 - Felt Pilot Candidate Documentation

Date: 2026-07-01

## Ziel

B146 dokumentiert den erfolgreichen Oberschwaben-Felt-Pilot als Integrationskandidaten.
Die oeffentliche Seite wird weiterhin nicht veraendert.

## Stand

Der Pilotpfad wurde erfolgreich getestet:

```text
ArcGIS -> GeoJSON -> mapshaper -> Felt
```

Ergebnis:

- Landkreis-GeoJSON erzeugt und in Felt geladen
- Schnittmengen-GeoJSON erzeugt, in mapshaper vereinfacht und in Felt geladen
- Schnittmenge ist visuell dominant
- Landkreisgrenzen und Landkreislabels geben Orientierung
- Popup funktioniert und zeigt nur relevante Felder
- Direktannotation ist gesetzt
- Share/View funktioniert
- Embed-Code ist verfuegbar
- Mobile View wurde geprueft und ist brauchbar

## Kartenkandidat

Arbeitstitel:

```text
Oberschwaben Moor-/Feuchtbodenkontext Pilot
```

Zentrale Aussage der Karte:

```text
Schnittmenge = Prüfbedarf, nicht Eignung
```

Interpretation:

Die Karte zeigt die Ueberlagerung aus landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext.
Sie ersetzt keine hydrologische Modellierung, keine Priorisierung und keine parzellenscharfe
Eignungsentscheidung.

## Lokale Pilotdaten

Lokal erzeugte Arbeitsdateien:

```text
working/oberschwaben_felt_pilot/oberschwaben_landkreise_4326.geojson
working/oberschwaben_felt_pilot/oberschwaben_schnittmenge_4326.geojson
working/oberschwaben_felt_pilot/oberschwaben_schnittmenge_simpel.geojson
```

Wichtig:

Diese Dateien bleiben lokal und werden nicht committed.

Die fuer Felt verwendete Schnittmengen-Datei ist:

```text
oberschwaben_schnittmenge_simpel.geojson
```

## Entscheidung

B146 ist noch kein Integrationspatch.

Noch nicht umgesetzt:

- kein iframe in `index.html`
- kein Ersatz der bestehenden PNG-/Sticky-Karte
- keine Aenderung an `src/styles.css`
- keine public map files im Repo
- keine MapLibre- oder Datawrapper-Integration

## Naechste Gate-Fragen vor B147

Vor einem aktiven Einbau in die Seite muessen diese Punkte dokumentiert sein:

1. Oeffnet der Share-Link in einem privaten Fenster ohne Login?
2. Ist der iframe-Code im Professional Trial auch fuer externe Webseiten nutzbar?
3. Bleibt die mobile Darstellung im eingebetteten Zustand brauchbar?
4. Ist ein externer Felt-Embed datenschutz-/rechtlich akzeptabel?
5. Gibt es eine stabile Fallback-Strategie, falls Felt spaeter nicht verfuegbar ist?
6. Bleibt die bestehende PNG-Karte als Rueckfalloption erhalten?

## Empfehlung fuer B147

B147 sollte nicht sofort die bestehende Karte ersetzen, sondern einen isolierten Prototyp bauen:

```text
docs/prototypes/oberschwaben_felt_embed_test.html
```

oder einen deaktivierten Testblock, der nicht in der Hauptnavigation sichtbar ist.

Erst nach diesem Integrationstest sollte entschieden werden, ob der Felt-Embed in `index.html`
die bestehende Oberschwaben-Karte ersetzt oder nur als optionaler externer Kartenlink angeboten wird.

## Hinweis zur B145-Vorlage

Die B145-Template-Datei ist vorhanden und kann als Quelle fuer Share-URL und iframe-Code genutzt werden.
