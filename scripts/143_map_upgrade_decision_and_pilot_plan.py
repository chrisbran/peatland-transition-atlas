from pathlib import Path
from datetime import date

ROOT = Path(".")
SCRIPT = ROOT / "scripts" / "143_map_upgrade_decision_and_pilot_plan.py"
DOC = ROOT / "docs" / "B143_map_upgrade_decision_and_pilot_plan.md"
AUDIT = ROOT / "docs" / "B143_map_upgrade_decision_and_pilot_plan_audit.txt"
CHECKLIST = ROOT / "docs" / "B143_oberschwaben_felt_pilot_checklist.md"
DONE = ROOT / "tasks" / "done.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done(done_text: str) -> str:
    line = f"- B143 map upgrade decision: documented a separate Oberschwaben map-quality pilot instead of replacing the current map stack immediately ({date.today().isoformat()})."
    if "B143 map upgrade decision" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def build_decision_doc(today: str) -> str:
    return f"""# B143 - Map Upgrade Decision and Pilot Plan

Date: {today}

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
"""


def build_checklist(today: str) -> str:
    return f"""# B143 - Oberschwaben Felt Pilot Checklist

Date: {today}

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
"""


def main() -> None:
    today = date.today().isoformat()

    write(DOC, build_decision_doc(today))
    write(CHECKLIST, build_checklist(today))

    audit_text = f"""# B143 map upgrade decision and pilot plan audit

Date: {today}

Result: DOCUMENTATION ONLY. No public page files changed.

Created/updated:

- docs/B143_map_upgrade_decision_and_pilot_plan.md
- docs/B143_oberschwaben_felt_pilot_checklist.md
- docs/B143_map_upgrade_decision_and_pilot_plan_audit.txt
- tasks/done.md

Decision:

- Do not replace the full map stack immediately.
- Prepare a separate Oberschwaben pilot using ArcGIS -> GeoJSON -> mapshaper -> Felt.
- Keep the current PNG/sticky map stack stable as fallback.
"""
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B143 map upgrade decision and pilot plan complete.")
    print("Documentation only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B143_map_upgrade_decision_and_pilot_plan.md")
    print("  docs/B143_oberschwaben_felt_pilot_checklist.md")
    print("  docs/B143_map_upgrade_decision_and_pilot_plan_audit.txt")
    print("  tasks/done.md")


if __name__ == "__main__":
    main()
