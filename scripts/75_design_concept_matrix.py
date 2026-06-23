#!/usr/bin/env python3
"""
B75 - Design concept matrix

Purpose:
- Convert the design discussion into an explicit decision framework.
- Define three controlled visual directions for the German presentation version.
- Translate the user's Design-Charta, brandt_theme and data-essay notes into website design criteria.
- Recommend a hybrid direction: fachlich hell + narrativ geführt + kartografisch diszipliniert.
- Do not modify application files.

Outputs:
- docs/B75_design_concept_matrix.md
- docs/B75_design_decision_scorecard.csv
- docs/B75_visual_language_principles.md
- tasks/done.md

Does NOT:
- modify index.html
- modify CSS
- create design dummies
- alter maps/scripts/data
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

MATRIX = DOCS / "B75_design_concept_matrix.md"
SCORECARD = DOCS / "B75_design_decision_scorecard.csv"
PRINCIPLES = DOCS / "B75_visual_language_principles.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_scorecard() -> None:
    rows = [
        {
            "criterion": "Story-Verständlichkeit",
            "weight": 5,
            "A_fachlich_hell": 5,
            "B_editorial_natur": 4,
            "C_kartografisch_analytisch": 3,
            "comment": "Die erste Vorzeigefassung muss führen, nicht explorativ überfordern.",
        },
        {
            "criterion": "Seriosität für Praxis/Fachverwaltung",
            "weight": 5,
            "A_fachlich_hell": 5,
            "B_editorial_natur": 3,
            "C_kartografisch_analytisch": 4,
            "comment": "A wirkt am anschlussfähigsten an Projekt-, Förder- und Verwaltungskontexte.",
        },
        {
            "criterion": "Narrative Vermittlung",
            "weight": 4,
            "A_fachlich_hell": 3,
            "B_editorial_natur": 5,
            "C_kartografisch_analytisch": 2,
            "comment": "B liefert Rhythmus, Atmosphäre und Einstieg; sollte dosiert in A integriert werden.",
        },
        {
            "criterion": "Kartenwirkung",
            "weight": 5,
            "A_fachlich_hell": 4,
            "B_editorial_natur": 3,
            "C_kartografisch_analytisch": 5,
            "comment": "C ist bei Label-, Quellen- und Legendenlogik stark; als Disziplin übernehmen.",
        },
        {
            "criterion": "Lesbarkeit deutscher Fachsprache",
            "weight": 5,
            "A_fachlich_hell": 5,
            "B_editorial_natur": 4,
            "C_kartografisch_analytisch": 3,
            "comment": "Längere deutsche Komposita und Fachbegriffe brauchen ruhige helle Typografie.",
        },
        {
            "criterion": "Reduktion visuellen Rauschens",
            "weight": 4,
            "A_fachlich_hell": 5,
            "B_editorial_natur": 3,
            "C_kartografisch_analytisch": 5,
            "comment": "A und C entsprechen Tufte/Schweizer Raster stärker als eine zu atmosphärische Variante.",
        },
        {
            "criterion": "Präsentationstauglichkeit",
            "weight": 4,
            "A_fachlich_hell": 5,
            "B_editorial_natur": 4,
            "C_kartografisch_analytisch": 3,
            "comment": "A funktioniert am robustesten in Jour fixe, Beamer, PDF-Screenshot und Gespräch.",
        },
        {
            "criterion": "Eigenständigkeit / Wiedererkennung",
            "weight": 3,
            "A_fachlich_hell": 3,
            "B_editorial_natur": 5,
            "C_kartografisch_analytisch": 3,
            "comment": "B ist stärker als Marke, aber darf die Sachautorität nicht schwächen.",
        },
    ]

    fieldnames = [
        "criterion", "weight", "A_fachlich_hell", "B_editorial_natur",
        "C_kartografisch_analytisch", "comment",
    ]

    with SCORECARD.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

        totals = {}
        for variant in ["A_fachlich_hell", "B_editorial_natur", "C_kartografisch_analytisch"]:
            totals[variant] = sum(int(r["weight"]) * int(r[variant]) for r in rows)

        writer.writerow({})
        writer.writerow({
            "criterion": "Weighted total",
            "weight": "",
            "A_fachlich_hell": totals["A_fachlich_hell"],
            "B_editorial_natur": totals["B_editorial_natur"],
            "C_kartografisch_analytisch": totals["C_kartografisch_analytisch"],
            "comment": "Scores are decision aids, not final design proof.",
        })


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    matrix = f"""# B75 - Design Concept Matrix

Date: {today}

## 1. Zweck

B75 übersetzt die Design-Diskussion in ein explizites Entscheidungssystem.

Der nächste sichtbare Umbau der Website soll nicht geschmacklich oder zufällig erfolgen, sondern aus einem klaren Designziel abgeleitet werden:

**Ein heller, ruhiger, präziser Datenessay über räumlich differenzierten Moorschutz.**

## 2. Ausgangspunkte

Die deutsche Vorzeigefassung richtet sich an wissenschaftlich informierte Praxisakteure.

Die visuelle Sprache soll:

- narrativ führen,
- wissenschaftlich belastbar wirken,
- Karten und Daten in den Mittelpunkt stellen,
- interne Prototypen- und Toolsprache vermeiden,
- ruhig, reduziert und professionell sein.

## 3. Übernommene Designprinzipien

Aus der Design-Charta werden folgende Regeln direkt auf die Website übertragen:

1. Der Titel ist die Aussage, nicht das Thema.
2. Daten-Tinte maximieren, Dekoration vermeiden.
3. Eine Akzentfarbe trägt die Hauptaussage.
4. Direkte Beschriftung schlägt Legende.
5. Skalen und Vergleiche dürfen nicht übertreiben.
6. Wiederholung schlägt Komplexität.
7. Jede Grafik und Karte trägt ihre Herkunft.
8. Farben sind semantisch oder gar nicht.
9. Erst die Aussage, dann die Visualisierung.

Für diese Website heißt das:

- keine dekorativen Moor-Texturen,
- keine schweren Schatten,
- keine überflüssigen Cards,
- keine farbliche Vielfalt ohne Bedeutung,
- Quellenhinweise sichtbar, aber ruhig,
- deutsche Überschriften als Aussagen formulieren.

## 4. Designrichtung A - Fachlich hell / institutionell ruhig

### Kurzbeschreibung

Eine helle, sachliche Präsentationsfassung mit ruhiger Typografie, viel Weißraum, klaren Linien und Petrol als Hauptakzent.

### Wirkung

- glaubwürdig,
- anschlussfähig an Fachverwaltung, Projektpartner und Policy-Kontexte,
- robust für Jour fixe, Beamer, Screenshots und kurze Projektvorstellungen,
- nicht werblich,
- nicht experimentell.

### Gestaltungsmerkmale

- Hintergrund: warmes Hellgrau oder Papierweiß.
- Text: Ink `#1A1A1A`.
- Sekundärtext: Muted `#6E6E6E`.
- Linien/Raster: `#E9E9E7`.
- Akzent: Petrol `#1F4E5F`.
- Sparsame Ergänzungsfarben: Ocker, Salbei, Rost nur semantisch.
- Links ausgerichtete Titelblöcke.
- Karten in ruhiger, heller Bühne.
- Wenige, klar begründete Boxen.

### Passende deutsche Anmutung

- fachlich,
- ruhig,
- prüfbar,
- zugänglich,
- kein Kampagnenstil.

### Risiko

Kann trocken wirken, wenn narrative Übergänge fehlen.

### Einsatz

Geeignet als Basis der ersten deutschen Vorzeigefassung.

## 5. Designrichtung B - Editorial Natur / Datenessay

### Kurzbeschreibung

Eine etwas erzählerischere Fassung mit wärmeren Naturtönen, stärkerem Abschnittsrhythmus und optionaler dokumentarischer Bildsprache.

### Wirkung

- zugänglicher,
- stärker erzählerisch,
- näher am Datenessay-Format,
- emotionaler, ohne werblich sein zu müssen.

### Gestaltungsmerkmale

- Warmweiß, Torfbraun, Salbei, dezente Ockerakzente.
- Größere Abschnittsöffner.
- Mehr Luft um Kernzitate und Übergänge.
- Optional: dokumentarische Fotos als Einstieg oder Abschnittsanker.
- Karten bleiben jedoch dominant und sachlich.

### Passende deutsche Anmutung

- vermittelnd,
- essayistisch,
- anschaulich,
- menschlicher.

### Risiko

Kann zu magazinig oder atmosphärisch werden, wenn Fotos, Texturen oder warme Farben zu stark eingesetzt werden.

### Einsatz

Geeignet als Inspirationsquelle für Rhythmus, nicht als reine Basis.

## 6. Designrichtung C - Kartografisch analytisch

### Kurzbeschreibung

Eine stark reduzierte, daten- und kartenorientierte Fassung mit minimaler UI und maximaler Präzision.

### Wirkung

- analytisch,
- geodatenbasiert,
- präzise,
- methodisch streng.

### Gestaltungsmerkmale

- sehr wenig Fließtext,
- starke Kartenbühne,
- direkte Labels,
- Quellenzeilen,
- kleine Multiples und klare Vergleichsraster,
- reduzierte Farbpalette.

### Passende deutsche Anmutung

- kontrolliert,
- sachlich,
- technisch kompetent.

### Risiko

Kann zu kühl, zu dashboardartig oder zu wenig narrativ wirken.

### Einsatz

Geeignet als Regelwerk für Karten- und Labeldisziplin.

## 7. Entscheidungsmatrix

Die detaillierte Bewertungsmatrix steht in:

- `docs/B75_design_decision_scorecard.csv`

Vorläufiges Ergebnis:

**A ist die Basis. B liefert Erzählrhythmus. C liefert kartografische Disziplin.**

## 8. Empfohlene Richtung

Die erste deutsche Vorzeigefassung sollte kein reines A, B oder C sein.

Empfohlen wird:

**A + dosierte B-Elemente + C-Regeln**

Oder präzise:

> Fachlich hell, narrativ geführt, kartografisch diszipliniert.

## 9. Konkrete visuelle Zielparameter

### Hintergrund

- `#F8F7F3` oder `#F7F6F2`
- keine dunkle Default-Fläche für die Gesamtseite

### Text

- primär `#1A1A1A`
- sekundär `#6E6E6E`

### Akzent

- Petrol `#1F4E5F`
- nur eine dominante Akzentfarbe pro Abschnitt

### Semantik

- Petrol: Fokus / räumliche Orientierung / Hauptaussage
- Ocker: Politik / Instrumente / Umsetzung
- Salbei: Nutzung / Landschaft / Landwirtschaft
- Rost: Risiko / Emissionsdruck / Konflikt
- Grau: Kontext / Hintergrund

### Typografie

- Inter / Segoe UI / Helvetica / Arial
- keine Serifenschrift in Version 0.1
- linksbündige Titel
- kurze deutsche Überschriften

### Kartenbühne

- heller Hintergrund
- keine schweren Schatten
- dezente Kontur oder Rasterlinie
- Quellenzeile unten links
- Labels direkt, wo möglich

## 10. Anti-Patterns

Nicht verwenden:

- Moor-Texturen als Hintergrund
- dekorative Icons
- große Naturfoto-Hintergründe ohne Funktion
- NGO-Kampagnenästhetik
- Climate-emergency-Farbdramaturgie
- zu viele Cards
- zentrierte Plakattitel
- viele Akzentfarben gleichzeitig
- unklare Legenden
- sichtbare Begriffe wie Prototype, Dashboard, Module, Appendix

## 11. Nächster Schritt

B76 sollte drei statische Design-Dummies erzeugen.

Wichtig:

- alle drei nutzen denselben deutschen Kerntext,
- alle drei sind statische HTML-Dateien,
- keine echte Website wird verändert,
- keine produktiven Styles werden überschrieben.

Vorgeschlagene Dateien:

- `design_dummies/B76_A_fachlich_hell.html`
- `design_dummies/B76_B_editorial_natur.html`
- `design_dummies/B76_C_kartografisch_analytisch.html`

Danach kann entschieden werden, welche Richtung in die echte Seite übertragen wird.
"""
    write(MATRIX, matrix)

    principles = f"""# B75 - Visual Language Principles

Date: {today}

## 1. Leitsatz

**Form follows function.**

Die Gestaltung dient nur einem Zweck: Die komplexe Story räumlich differenzierten Moorschutzes schneller, sicherer und fachlich korrekter verständlich zu machen.

## 2. Produktkategorie

Die Seite ist kein Dashboard, keine Kampagnenseite und kein klassischer Projektbericht.

Sie ist ein:

**Datenessay zur regionalen Umsetzung von Moorschutz.**

## 3. Dramaturgie

Die Struktur folgt dem Martini-Glas-Prinzip:

1. Geführter Einstieg  
   Problem, Maßstab, Kartenfolge.

2. Kontrollierte Öffnung  
   Transformationspfade, regionale Einordnung, Quellen und Methode.

Damit ist die obere Hälfte stärker geführt als die untere.

## 4. Layout

- linksbündig,
- klare Raster,
- wenige Breiten,
- keine dekorativen Trennflächen,
- Textspalten begrenzen,
- Karten bewusst größer als Begleittext,
- keine gleichwertige Überfülle von Boxen.

## 5. Typografie

- eine Schriftfamilie,
- klare Größenhierarchie,
- deutsche Komposita brauchen Luft,
- keine zentrierten Hero-Blöcke,
- keine verspielten Headlines.

## 6. Farbe

Farben müssen Bedeutung tragen.

- Petrol: Hauptfokus
- Rost: Risiko / Emissionsdruck
- Ocker: Instrumente / Politik
- Salbei: Nutzung / Landschaft
- Grau: Kontext

Wenn Farbe keine Bedeutung trägt, wird sie entfernt.

## 7. Karten

Karten sind Belege, nicht Dekoration.

Jede zentrale Karte braucht:

- klare Aussage,
- ruhigen Rahmen,
- kurze Legende oder direkte Labels,
- Quellenzeile,
- methodische Grenze, wenn nötig.

## 8. Text

Sichtbarer Text folgt diesen Regeln:

- Aussage vor Thema.
- Kurz vor vollständig.
- Deutsch vor internem Englisch.
- Sache vor Tool.
- Grenze vor Überbehauptung.

Beispiel:

Nicht:

`Peatland Transition Atlas`

Sondern:

`Moorschutz braucht räumliche Orientierung`

Nicht:

`Supporting evidence explorer`

Sondern:

`Einordnung und Vergleich`

## 9. Bilder

Fotografie kann später eine starke Rolle spielen, aber nur wenn sie dokumentarisch und ortsbezogen ist.

Nicht verwenden:

- generische Moorbilder,
- dekorative Hero-Fotos,
- Stock-Ästhetik,
- atmosphärische Bilder ohne analytische Funktion.

Ein gutes Foto müsste zeigen:

- einen Ort,
- eine Nutzung,
- einen Konflikt,
- eine Person,
- eine konkrete Umsetzungssituation.

## 10. Qualitätsprüfung

Ein Designentwurf ist nur dann gut, wenn er diese Fragen besteht:

1. Versteht man die Hauptaussage in 30 Sekunden?
2. Kann man die Kartenfolge ohne Erklärung nachvollziehen?
3. Wirkt die Seite fachlich glaubwürdig?
4. Sind alle Farben semantisch begründet?
5. Sind Quellen und Grenzen sichtbar?
6. Verschwindet das Tool hinter der Sache?
"""
    write(PRINCIPLES, principles)

    write_scorecard()

    done_entry = f"""
## B75 - Design concept matrix ({today})

- Defined three controlled design directions for the German presentation version.
- Recommended hybrid direction: fachlich hell, narrativ geführt, kartografisch diszipliniert.
- Created `docs/B75_design_concept_matrix.md`.
- Created `docs/B75_design_decision_scorecard.csv`.
- Created `docs/B75_visual_language_principles.md`.
- Did not modify application files, maps, scripts, data or CSS.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B75 - Design concept matrix" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B75 design concept matrix complete.")
    print("Changed/created:")
    print(f"  {rel(MATRIX)}")
    print(f"  {rel(SCORECARD)}")
    print(f"  {rel(PRINCIPLES)}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
