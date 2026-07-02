from pathlib import Path
from datetime import date

ROOT = Path(".")
SCRIPT = ROOT / "scripts" / "146_felt_pilot_candidate_documentation.py"
DOC = ROOT / "docs" / "B146_felt_pilot_candidate_documentation.md"
EMBED = ROOT / "docs" / "B146_felt_embed_candidate.md"
QA = ROOT / "docs" / "B146_felt_pilot_qa_record.md"
AUDIT = ROOT / "docs" / "B146_felt_pilot_candidate_documentation_audit.txt"
DONE = ROOT / "tasks" / "done.md"

B145_TEMPLATE = ROOT / "docs" / "B145_felt_embed_candidate_template.txt"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done(done_text: str) -> str:
    line = f"- B146 Felt pilot candidate documentation: documented the successful Felt pilot, embed availability, mobile check and integration gates ({date.today().isoformat()})."
    if "B146 Felt pilot candidate documentation" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def build_doc(today: str, has_b145_template: bool) -> str:
    template_note = (
        "Die B145-Template-Datei ist vorhanden und kann als Quelle fuer Share-URL und iframe-Code genutzt werden."
        if has_b145_template else
        "Die B145-Template-Datei wurde nicht gefunden; Share-URL und iframe-Code bitte direkt in `docs/B146_felt_embed_candidate.md` eintragen."
    )

    return f"""# B146 - Felt Pilot Candidate Documentation

Date: {today}

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

{template_note}
"""


def build_embed(today: str, b145_text: str) -> str:
    carried = ""
    if b145_text:
        carried = "\n## Aus B145-Template uebernommener Arbeitsstand\n\n```text\n" + b145_text.strip() + "\n```\n"

    return f"""# B146 - Felt Embed Candidate

Date: {today}

## Zweck

Diese Datei dokumentiert den Felt-Kandidaten fuer den Oberschwaben-Kartenpilot.
Der iframe-Code wird hier nur dokumentiert und noch nicht in `index.html` eingebaut.

## Felt map title

```text
Oberschwaben Moor-/Feuchtbodenkontext Pilot
```

## Felt share URL

```text
<PASTE FELT SHARE URL HERE>
```

## Felt iframe embed code

```html
<!-- PASTE FELT IFRAME CODE HERE -->
```

## Visibility setting

```text
Anyone with the link can view
```

## Plan / license status

```text
Professional Trial, 7 Tage.
Embed-Code ist verfuegbar.
Vor Live-Einbau: Nutzungs-/Lizenzbedingungen pruefen.
```

## Privacy / external service status

```text
Externer Felt-Embed.
Vor Live-Einbau: Datenschutz-/Cookie-/Drittanbieter-Hinweis klaeren.
```

## Desktop QA

```text
Bestanden: Karte lädt, Schnittmenge sichtbar, Annotation sichtbar, Popup funktioniert.
```

## Mobile QA

```text
Bestanden laut manuellem Test: Mobile View ist brauchbar.
```

## Current decision

```text
Keep testing. Noch kein Einbau in index.html.
```
{carried}
"""


def build_qa(today: str) -> str:
    return f"""# B146 - Felt Pilot QA Record

Date: {today}

## QA-Status

| Punkt | Status | Notiz |
|---|---|---|
| Landkreis-Upload | bestanden | GeoJSON ca. 54 KB |
| Schnittmengen-Upload | bestanden | vereinfachtes GeoJSON ca. 3.37 MB |
| Projektion | bestanden | Felt zeigt Oberschwaben korrekt |
| Popup | bestanden | zeigt `klasse` und `flaeche_ha` |
| Annotation | bestanden | `Schnittmenge = Prüfbedarf, nicht Eignung` |
| Layernamen | bestanden | technische Namen reduziert |
| Mobile View | bestanden | laut manuellem Test brauchbar |
| Embed-Code | bestanden | verfügbar |
| Privates Fenster | offen | vor B147 testen/dokumentieren |
| Datenschutz/Lizenz | offen | vor Live-Einbau prüfen |
| Fallback | offen | PNG-/WebP-Fallback muss erhalten bleiben |

## Visuelle Bewertung

Der Felt-Pilot hebt die Oberschwaben-Karte sichtbar ueber den bisherigen GIS-/PNG-Look:

- scharfe Vektordarstellung
- dunkle Basemap passt zur Atlas-Aesthetik
- Schnittmenge ist direkt erkennbar
- Landkreisgrenzen geben Orientierung
- Popup ist aufgeraeumt
- Annotation erklaert die Karte im Kartenbild selbst

## Risiken

- externe Abhaengigkeit von Felt
- moegliche Plan-/Lizenzbindung nach Ablauf der Trial
- Datenschutz-/Drittanbieterfrage
- iframe-Verhalten im bestehenden Sticky-Layout noch ungeprueft
- mobile Embed-Hoehe und Legende koennen im Live-Layout anders wirken

## Gate fuer B147

B147 darf erst `index.html` beruehren, wenn mindestens ein isolierter iframe-Test bestaetigt:

- Embed laedt lokal
- Embed funktioniert in Firefox/Chrome
- Embed ist auf 390 px Breite brauchbar
- Fallback bleibt definierbar
"""


def main() -> None:
    today = date.today().isoformat()

    b145_text = read(B145_TEMPLATE) if B145_TEMPLATE.exists() else ""
    has_b145 = B145_TEMPLATE.exists()

    write(DOC, build_doc(today, has_b145))
    write(EMBED, build_embed(today, b145_text))
    write(QA, build_qa(today))

    audit_text = f"""# B146 Felt pilot candidate documentation audit

Date: {today}

Result: DOCUMENTATION ONLY. No public page files changed.

Created/updated:

- docs/B146_felt_pilot_candidate_documentation.md
- docs/B146_felt_embed_candidate.md
- docs/B146_felt_pilot_qa_record.md
- docs/B146_felt_pilot_candidate_documentation_audit.txt
- tasks/done.md

B145 template found: {has_b145}

No iframe was added to index.html.
No CSS was changed.
No local GeoJSON/Shapefile/GPKG files were staged or referenced for commit.
"""
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B146 Felt pilot candidate documentation complete.")
    print("Documentation only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B146_felt_pilot_candidate_documentation.md")
    print("  docs/B146_felt_embed_candidate.md")
    print("  docs/B146_felt_pilot_qa_record.md")
    print("  docs/B146_felt_pilot_candidate_documentation_audit.txt")
    print("  tasks/done.md")


if __name__ == "__main__":
    main()
