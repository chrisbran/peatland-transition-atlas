from pathlib import Path
from datetime import date

ROOT = Path(".")
SCRIPT = ROOT / "scripts" / "145_felt_pilot_build_sheet.py"
DOC = ROOT / "docs" / "B145_felt_pilot_build_sheet.md"
STYLE = ROOT / "docs" / "B145_felt_style_spec.md"
QA = ROOT / "docs" / "B145_felt_pilot_qa_checklist.md"
TEMPLATE = ROOT / "docs" / "B145_felt_embed_candidate_template.txt"
AUDIT = ROOT / "docs" / "B145_felt_pilot_build_sheet_audit.txt"
DONE = ROOT / "tasks" / "done.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done(done_text: str) -> str:
    line = f"- B145 Felt pilot build sheet: documented the manual Felt styling, annotation, tooltip and embed-candidate workflow for the Oberschwaben map pilot ({date.today().isoformat()})."
    if "B145 Felt pilot build sheet" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def build_doc(today: str) -> str:
    return f"""# B145 - Felt Pilot Build Sheet

Date: {today}

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
"""


def build_style(today: str) -> str:
    return f"""# B145 - Felt Style Specification

Date: {today}

## Designprinzip

Die Karte soll nicht wie ein GIS-Arbeitsstand wirken, sondern wie eine redaktionelle Karte.

Leitregel:

> Eine dominante Aussage, gedämpfter Kontext.

## Klassen und visuelle Rollen

| Klasse | Rolle | Füllung | Deckkraft | Kontur | Kommentar |
|---|---|---|---:|---|---|
| Schnittmenge | Hauptsignal | kräftiges Petrol / Dunkeltürkis | 85-95 % | dunkler Petrolton | einzige satte Farbe |
| Moor-/Feuchtbodenkontext | Bodenkontext | Blaugrau | 35-50 % | sehr schwach | Kontext, nicht Hauptsignal |
| Grünland | Nutzungskontext | gedämpftes Salbeigrün | 35-45 % | keine oder sehr schwach | nicht mit Schnittmenge konkurrieren |
| Ackerland | Nutzungskontext | warmes Ocker/Sand | 35-45 % | keine oder sehr schwach | ruhig halten |
| Dauerkultur | Nutzungskontext | gedämpftes Violett/Aubergine | 35-45 % | keine oder sehr schwach | kleinräumig interpretieren |

## Beispielpalette

Startwerte, in Felt visuell anpassen:

```text
Schnittmenge:            #087f7a
Moor-/Feuchtbodenkontext:#7f9aa3
Grünland:                #a8b97a
Ackerland:               #d6b36a
Dauerkultur:             #8f6b8f
Kontur dunkel:           #23443f
```

## Hintergrund

- möglichst reduzierter Basemap-Stil
- keine dominanten Straßen
- Gewässer und Orte nur, wenn sie Orientierung geben
- Landkreisgrenzen dezent
- Labels nicht flächendeckend, sondern gezielt

## Direkte Kartenlabels

Pflichtlabels:

```text
Schnittmenge = Prüfbedarf, nicht Eignung
Biberach
Ravensburg
Sigmaringen
Bodenseekreis
```

Optionaler Callout:

```text
Landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext überlagern sich hier.
```

## Legende

Legende möglichst kurz halten.

Priorität:

1. Schnittmenge
2. Moor-/Feuchtbodenkontext
3. Nutzungskontext

Wenn Felt eine vollständige Legende erzeugt, trotzdem direkt auf der Karte annotieren.
Die Legende darf nicht die zentrale Erklärung übernehmen.

## Tooltip-Text

Tooltip-Titel:

```text
{{klasse}}
```

Tooltip-Felder:

```text
Landkreis: {{landkreis}}
Fläche: {{flaeche_ha}} ha
```

Bei technischen Feldnamen in Felt manuell umbenennen oder ausblenden.
"""


def build_qa(today: str) -> str:
    return f"""# B145 - Felt Pilot QA Checklist

Date: {today}

## 1. Daten-QA

- [ ] Karte liegt geografisch korrekt in Oberschwaben.
- [ ] Alle vier Landkreise sind erkennbar.
- [ ] `klasse` ist vorhanden.
- [ ] `flaeche_ha` ist vorhanden.
- [ ] `landkreis` ist vorhanden.
- [ ] Keine technischen Felder im Tooltip sichtbar.
- [ ] Kleine Schnittmengen-Cluster sind nicht durch Simplification verschwunden.

## 2. Kartografie-QA

- [ ] Schnittmenge ist das stärkste visuelle Signal.
- [ ] Kontextklassen sind gedämpft.
- [ ] Farben sind ausreichend unterscheidbar.
- [ ] Karte ist rotgrün-sicher genug.
- [ ] Landkreisnamen sind lesbar.
- [ ] Direktannotation erklärt die Schnittmenge.
- [ ] Karte wirkt nicht wie ein ArcGIS-Roh-Export.

## 3. Story-QA

- [ ] Karte unterstützt die Aussage `Prüfbedarf, nicht Eignung`.
- [ ] Karte erklärt die Überlagerung aus Nutzung und Moor-/Feuchtbodenkontext.
- [ ] Karte suggeriert keine Priorisierung.
- [ ] Karte suggeriert keine parzellenscharfe Eignung.
- [ ] Karte passt zur B138-Präzisierung.

## 4. Interaktions-QA

- [ ] Hover/Tooltip funktioniert am Desktop.
- [ ] Mobile Nutzung ist akzeptabel.
- [ ] Falls mobile Hover nicht sinnvoll ist: Karte bleibt auch ohne Tooltip verständlich.
- [ ] Embed lädt ohne Login.
- [ ] Embed lädt in normalem Browserfenster und privatem Fenster.

## 5. Performance-QA

- [ ] Karte lädt subjektiv schnell.
- [ ] Kein auffälliges Ruckeln.
- [ ] GeoJSON-Datei ist ausreichend vereinfacht.
- [ ] Felt-Embed blockiert nicht den restlichen Seitenaufbau.

## 6. Integrationsentscheidung

- [ ] Felt-Lizenz/Plan akzeptabel.
- [ ] Datenschutz/externes Embed akzeptabel.
- [ ] Bestehende PNG-Karte bleibt als Fallback erhalten.
- [ ] Kein aktiver Einbau in `index.html` ohne eigenen B146/B147-Patch.

## Entscheidung

```text
[ ] übernehmen als Embed-Pilot
[ ] besser als statischer Reexport verwenden
[ ] verwerfen und PNG-Version behalten
[ ] MapLibre-Minimaltest als Alternative starten
```
"""


def build_template(today: str) -> str:
    return f"""B145 Felt Embed Candidate Template
Date: {today}

Do not paste this into index.html yet.
Use this file only to document the candidate Felt pilot.

Felt map title:
<insert title>

Felt share URL:
<insert URL>

Felt iframe embed code:
<insert iframe code>

Visibility setting:
<public / anyone with link / other>

License / plan check:
<notes>

Privacy / external embed check:
<notes>

Desktop QA:
<notes>

Mobile QA:
<notes>

Decision:
<keep testing / integrate later / export static image / reject>
"""


def main() -> None:
    today = date.today().isoformat()

    write(DOC, build_doc(today))
    write(STYLE, build_style(today))
    write(QA, build_qa(today))
    write(TEMPLATE, build_template(today))

    audit_text = f"""# B145 Felt pilot build sheet audit

Date: {today}

Result: DOCUMENTATION ONLY. No public page files changed.

Created/updated:

- docs/B145_felt_pilot_build_sheet.md
- docs/B145_felt_style_spec.md
- docs/B145_felt_pilot_qa_checklist.md
- docs/B145_felt_embed_candidate_template.txt
- docs/B145_felt_pilot_build_sheet_audit.txt
- tasks/done.md

No Felt iframe was added to index.html.
No GeoJSON/GPKG/Shapefile files were created or staged.
"""
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B145 Felt pilot build sheet complete.")
    print("Documentation only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B145_felt_pilot_build_sheet.md")
    print("  docs/B145_felt_style_spec.md")
    print("  docs/B145_felt_pilot_qa_checklist.md")
    print("  docs/B145_felt_embed_candidate_template.txt")
    print("  docs/B145_felt_pilot_build_sheet_audit.txt")
    print("  tasks/done.md")


if __name__ == "__main__":
    main()
