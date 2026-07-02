# B143 - Map Upgrade Decision and Pilot Plan

Date: 2026-06-30

## Entscheidung

Die bestehende V2-Seite bleibt stabil. Die Karten werden nicht sofort vollständig auf einen neuen Stack umgestellt.

Stattdessen wird ein separater Pilot für die Oberschwaben-Karte vorbereitet:

> Erst die regionale Schluesselkarte auf ein hoeheres kartografisches Niveau bringen, dann entscheiden, ob der Ansatz in die Hauptseite uebernommen wird.

## Warum dieser Schritt jetzt sinnvoll ist

Die V2-Erzaehlung ist inzwischen deutlich staerker als die Kartenbasis. Scope, Wertschöpfung, Wasser/Governance, Methode und Konsequenz sind sichtbar verankert. Der groesste verbleibende Qualitaetssprung liegt nicht mehr in weiterem Text, sondern in der Kartenproduktion.

Die zentrale Review-Kritik betrifft vor allem:

- uneinheitliche Kartensprache
- blasse nationale und regionale Datenlayer
- zu starker GIS-/Export-Look
- zu wenig direkte Annotation
- eine Oberschwaben-Schnittmenge, die noch nicht stark genug als Hauptsignal erscheint

## Strategische Wahl

### Nicht jetzt

- kompletter Wechsel aller Karten auf MapLibre
- Austausch aller globalen/europaeischen/deutschen Karten
- tiefer Umbau der Sticky-Scroll-Logik
- Einbau externer Embeds ohne Pilot und Datenschutz-/Lizenzpruefung

### Jetzt als Pilot

- Oberschwaben-Karte neu aufbauen
- Daten aus ArcGIS sauber als GeoJSON vorbereiten
- mit mapshaper vereinfachen
- in Felt als hochwertige Vektorkarte gestalten
- Schnittmenge visuell privilegieren
- Hover/Tooltip und Direktannotation testen
- iframe-Prototyp separat bewerten
- bestehende PNG-/Sticky-Version als Fallback behalten

## Tool-Entscheidung

| Werkzeug | Rolle im Projekt | Bewertung |
|---|---|---|
| Felt | Pilot fuer Oberschwaben | wahrscheinlich bester pragmatischer Qualitaetssprung |
| mapshaper | Datenvorbereitung | sofort sinnvoll, unabhaengig vom Zieltool |
| Datawrapper | spaeter fuer Choroplethen | gut fuer Welt-/Laenderkarten, nicht erste Prioritaet |
| MapLibre GL JS | spaeter fuer Vollkontrolle | fachlich stark, aber mehr JavaScript-Engineering |
| PNG/WebP-Reexport | Fallback | stabil, falls Embed/Lizenz/Mobilverhalten nicht ueberzeugt |

## Pilot-Ziel

Eine neue Oberschwaben-Karte, die auf den ersten Blick zeigt:

> Die Schnittmenge aus landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext ist das Schluesselsignal.

Designprinzip:

- Schnittmenge als einzige satte, dominante Farbe
- Ackerland, Gruenland, Dauerkultur und Moor-/Feuchtbodenkontext gedämpft
- Landkreisnamen direkt in der Karte
- ein bis zwei direkte Labels statt Legendenlast
- Tooltip nur mit wenigen, lesbaren Feldern
- deutsche Quellen-/Methodenzeile unter dem Embed

## Datenvorbereitung

Zieldatei fuer den Pilot:

```text
oberschwaben_schnittmenge_simpel.geojson
```

Minimal benoetigte Attribute:

| Feld | Zweck |
|---|---|
| `klasse` | Styling nach Ackerland, Gruenland, Dauerkultur, Moor-/Feuchtbodenkontext, Schnittmenge |
| `flaeche_ha` | Tooltip / Plausibilisierung |
| `landkreis` | Tooltip / Orientierung |
| optional `hinweis` | kurze Leselogik fuer spezielle Klassen |

Technische Vorgaben:

- EPSG:4326 / WGS84
- GeoJSON, nicht Esri-JSON
- mapshaper-Vereinfachung mit Schutz kleiner Flaechen
- Zielgroesse moeglichst unter 2-3 MB
- keine raw GIS-Arbeitsdaten ins Repo committen

## Pilot-Gates

Der Pilot wird nur uebernommen, wenn alle Punkte erfuellt sind:

1. **Kartografischer Mehrwert:** Schnittmenge ist sofort erkennbar.
2. **Narrativer Mehrwert:** Annotationen erklaeren die These ohne Zusatzlegende.
3. **Performance:** Embed lädt schnell genug.
4. **Mobile:** Karte ist auf 390 px nutzbar oder es gibt einen stabilen Fallback.
5. **Datenschutz/Lizenz:** Felt/Embed-Nutzung ist fuer den geplanten oeffentlichen Kontext akzeptabel.
6. **Stabilitaet:** Bestehende V2-Story wird nicht beschädigt.
7. **Fallback:** Bisherige PNG-Karte kann jederzeit wieder aktiv werden.

## Umsetzungspfad

### B143

Dieses Decision Memo und die Pilot-Checkliste ins Repo aufnehmen.

### B144

Datenexport vorbereiten und dokumentieren:

- ArcGIS: Project nach EPSG:4326
- Attribute bereinigen
- GeoJSON exportieren
- mapshaper-Vereinfachung testen
- Dateigroesse dokumentieren

### B145

Felt-Prototyp manuell bauen:

- Layer hochladen
- Farben setzen
- Schnittmenge hervorheben
- Labels und Annotationen setzen
- Tooltip konfigurieren
- Embed-Link sichern

### B146

Lokale iframe-Testseite oder versteckter Testblock:

- Felt iframe als Prototyp einbinden
- bestehende PNG-Version unangetastet lassen
- Desktop/mobile Ladeverhalten pruefen

### B147

Entscheidung:

- Felt-Embed uebernehmen
- oder hochwertigen statischen Reexport erzeugen
- oder MapLibre als naechsten technischen Schritt planen

## Nicht-Ziele

B143 ist keine Kartenimplementation.

Nicht umgesetzt werden:

- keine iframe-Einbindung
- keine Felt-Karte im Live-HTML
- keine MapLibre-Abhaengigkeit
- keine Datawrapper-Karte
- keine Aenderung an `index.html`
- keine Aenderung an `src/styles.css`
- keine raw data im Repo

## Git-Hygiene

Weiterhin gilt:

```powershell
# nicht verwenden
git add .
```

Nur explizit stagen. Keine Raw-Daten, keine Shapefiles, keine GPKG/GDB, keine Arbeitsordner.
