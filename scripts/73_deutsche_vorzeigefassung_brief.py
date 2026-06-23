#!/usr/bin/env python3
"""
B73 - German presentation version brief

Purpose:
- Stop feature/cleanup drift and define the next communication target.
- Specify audience, tone, scope and design principles for a first German presentation version.
- Prepare the ground for text audit and controlled design dummy phase.
- No application files are changed.

Outputs:
- docs/B73_deutsche_vorzeigefassung_brief.md
- docs/B73_design_directions_brief.md
- tasks/done.md

Does NOT:
- modify index.html
- modify CSS
- alter maps/scripts/data
- delete or hide sections
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

BRIEF = DOCS / "B73_deutsche_vorzeigefassung_brief.md"
DESIGN = DOCS / "B73_design_directions_brief.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    today = date.today().isoformat()

    brief = f"""# B73 - Deutsche Vorzeigefassung: Kommunikationsbrief

Date: {today}

## 1. Ausgangspunkt

Der aktuelle Peatland Transition Atlas ist technisch und strukturell als MVP-Prototyp weit genug, um in eine erste vorzeigbare Kommunikationsfassung überführt zu werden.

Ab B73 gilt ein Wechsel der Arbeitslogik:

Nicht mehr: mehr Funktionen, mehr Layer, mehr Cleanup.  
Sondern: Verständlichkeit, Stringenz, professionelle Designsprache.

## 2. Zielgruppe

Primäre Zielgruppe der ersten deutschen Vorzeigefassung:

**wissenschaftlich informierte Praxisakteure**

Dazu gehören insbesondere:

- Projektpartnerinnen und Projektpartner,
- landwirtschaftliche und regionale Praxisakteure,
- Fachverwaltungen,
- Akteure aus Beratung, Planung und Umsetzung,
- wissenschaftsnahe Policy- und Förderumfelder.

Die Zielgruppe ist fachlich anschlussfähig, aber nicht bereit, sich durch eine technische Prototyp- oder Datenstruktur zu arbeiten. Die Seite muss führen.

## 3. Tonalität

Gewünschte Tonalität:

**narrativ vermittelnd**

Das bedeutet:

- die Seite erzählt eine klare Sachgeschichte,
- sie vermeidet interne Projektsprache,
- sie erklärt komplexe Zusammenhänge mit ruhiger Autorität,
- sie bleibt fachlich präzise,
- sie wirkt nicht werblich,
- sie wirkt nicht wie ein Dashboard-Handbuch.

## 4. Umfang

Gewünschter Umfang der ersten Vorzeigefassung:

**kurz und pointiert**

Die erste Fassung soll nicht vollständig sein. Sie soll verständlich, vorzeigbar und argumentativ geschlossen sein.

Priorität:

1. Kernargument schärfen.
2. Sichtbare Texte kürzen.
3. Meta- und Toolsprache entfernen.
4. Design konsolidieren.
5. Erst danach neue Inhalte oder Module ergänzen.

## 5. Zentrales Kommunikationsziel

Die Seite soll nicht den Atlas als Produkt erklären.

Sie soll eine komplexe Transformationsgeschichte anschaulich vermitteln:

**Moore sind räumlich ungleich verteilt, klima- und biodiversitätspolitisch relevant und in der Umsetzung stark vom regionalen Kontext abhängig. Daher braucht Moorschutz räumlich differenzierte Transformationspfade statt allgemeiner Pauschallösungen.**

Der Atlas ist nur das Medium.

## 6. Kernbotschaft der Präsentationsfassung

Eine vorläufige Kernbotschaft lautet:

> Moorschutz wird erst dann umsetzbar, wenn globale Klimarelevanz, nationale Planungskulissen, regionale Bodenkontexte und betriebliche Nutzungsperspektiven zusammen betrachtet werden.

Diese Aussage steuert die erste deutsche Fassung.

## 7. Sichtbare Zielstruktur

Die deutsche Vorzeigefassung sollte vorläufig diese Struktur haben:

1. Problemrahmen  
   Kleine Flächen, große Wirkung: Moore sind klima- und biodiversitätspolitisch hoch relevant.

2. Räumliche Einordnung  
   Wo liegen Moore, wo konzentriert sich Druck, und warum ist Maßstab entscheidend?

3. Umsetzungskulisse  
   Europa, Deutschland und Baden-Württemberg bilden unterschiedliche Ebenen der Umsetzung.

4. Regionale Differenzierung  
   In Baden-Württemberg wird aus Moorbodenkontext eine konkrete Planungs- und Nutzungsfrage.

5. Transformationspfade  
   Wiedervernässung, angepasste Nutzung, Wertschöpfung und Förderinstrumente müssen zusammen gedacht werden.

6. Methodische Einordnung  
   Die Seite zeigt eine vermittlungsorientierte Strukturierung, keine fertige Eignungs- oder Prioritätskarte.

## 8. Terminologie-Regeln

### Vermeiden

- Atlas als Subjekt der Story
- Prototype als sichtbares Leitwort
- Module
- Storyline
- Dashboard
- Evidence group
- Appendix
- Tool erklärt sich selbst
- automatische Ableitung von Eignung aus BK50

### Bevorzugen

- Moorschutz
- Wiedervernässung
- regionale Umsetzung
- Bodenkontext
- Nutzungsperspektiven
- Transformationspfade
- Wertschöpfungsketten
- Förderinstrumente
- Planungskulisse
- Betroffenheit
- Einordnung / Interpretation / Orientierung

## 9. Methodische Grenzen

Die deutsche Vorzeigefassung muss fachlich vorsichtig bleiben.

Insbesondere:

- BK50 zeigt Boden- bzw. Moor-/Feuchtgebietskontext.
- BK50 ist keine Wiedervernässungs-Prioritätskarte.
- BK50 ist keine Flächeneignungskarte.
- Landwirtschaftliche Nutzung, betriebliche Betroffenheit und Umsetzbarkeit müssen separat analysiert werden.
- SOLAMO-BW kann diese sozio-ökonomische Umsetzungslogik ergänzen, sobald belastbare Aussagen und Daten vorliegen.
- LUBW/Moorschutzkonzeption liefert den offiziellen strategischen und planerischen Rahmen.

## 10. Rolle von SOLAMO-BW und LUBW

Für die deutsche Vorzeigefassung sollten SOLAMO-BW und LUBW nicht als separate Projektblöcke erscheinen, sondern als fachliche Verankerung der regionalen Umsetzungsebene.

### LUBW / Moorschutzkonzeption

Rolle:

- offizieller strategischer Rahmen,
- Moorschutzkonzeption,
- Moorkataster,
- Renaturierungs- und Priorisierungslogik,
- Förder- und Umsetzungsinstrumente.

### SOLAMO-BW

Rolle:

- sozio-ökonomische Konkretisierung,
- betriebliche Betroffenheit,
- Nutzungskonzepte,
- Wertschöpfungsketten,
- Workshops und Interviews,
- ökonomisch-ökologische Bewertung,
- Politikempfehlungen.

## 11. Nächste Arbeitsschritte

### B74 - Sichtbarer Textaudit

Ziel:

- alle sichtbaren Texte extrahieren,
- deutsch redigieren,
- interne Projektsprache markieren,
- Alternativformulierungen vorschlagen.

Output:

- `docs/B74_visible_text_audit_de.md`
- optional `docs/B74_visible_text_rewrite_table.csv`

### B75 - Design-Dummy-Phase

Ziel:

- drei kontrollierte visuelle Richtungen testen,
- nicht direkt die echte Website umbauen,
- Bewertung nach Verständlichkeit, Seriosität und Kartenwirkung.

### B76 - Deutsche Präsentationsfassung v0.1

Ziel:

- ausgewählte Textfassung und Designrichtung in die Seite überführen,
- auf Deutsch,
- kurz,
- vorzeigbar,
- fachlich vorsichtig.

## 12. Definition of Done für die deutsche Vorzeigefassung

Die erste Fassung ist ausreichend, wenn eine fachlich informierte Person in drei bis fünf Minuten versteht:

1. warum Moore relevant sind,
2. warum räumliche Differenzierung nötig ist,
3. warum Baden-Württemberg ein sinnvoller regionaler Fokus ist,
4. warum Wiedervernässung eine sozio-ökonomische Umsetzungsfrage ist,
5. welche Transformationspfade grundsätzlich betrachtet werden müssen,
6. wo die methodischen Grenzen der Darstellung liegen.
"""

    design = f"""# B73 - Design Directions Brief

Date: {today}

## 1. Designziel

Die visuelle Sprache muss professionell, ruhig und funktional sein.

Leitprinzip:

**Form follows function.**

Die Gestaltung darf nur existieren, wenn sie die komplexe Story verständlicher macht.

## 2. Bewertungsraster

Jede Designrichtung wird nach diesen Kriterien bewertet:

1. Verständlichkeit der Story
2. Seriosität
3. Lesbarkeit
4. Kartenwirkung
5. Anschlussfähigkeit an wissenschaftlich informierte Praxisakteure
6. Verträglichkeit mit deutscher Fachsprache
7. Präsentationstauglichkeit
8. Reduktion von visuellem Rauschen

## 3. Designrichtung A - Institutionell / fachlich ruhig

### Wirkung

- glaubwürdig
- verwaltungs- und förderfähig
- nah an LUBW / Ministerium / Projektkontext
- wenig Risiko

### Typografie

- klare, sehr gut lesbare Sans-Serif
- wenig dekorative Kontraste
- starke H1/H2-Hierarchie
- kompakte Fließtexte

### Farben

- dunkles Moorgrün oder helles Warmgrau als Grund
- gedämpftes Schilf-/Moosgrün als Akzent
- sehr zurückhaltende Signalfarben für Kartenlegenden

### Eignung

Sehr geeignet für erste Projektvorstellung, wenn Seriosität wichtiger ist als visuelle Eigenständigkeit.

## 4. Designrichtung B - Editorial / narrativ

### Wirkung

- hochwertiger
- stärker erzählerisch
- mehr Magazin-/Report-Charakter
- emotionaler, aber weiterhin sachlich

### Typografie

- ausdrucksstärkere Überschriften
- großzügigere Textführung
- klare Abschnittsdramaturgie
- starke Zwischenüberschriften

### Farben

- warme Naturtöne
- Moorgrün, Torfbraun, Wollgras-/Schilfakzent
- mehr atmosphärische Tiefe

### Eignung

Geeignet, wenn die Seite als Storytelling-Demo beeindrucken soll. Risiko: kann bei zu viel Atmosphäre weniger wissenschaftlich wirken.

## 5. Designrichtung C - Kartografisch / analytisch

### Wirkung

- daten- und raumorientiert
- nüchtern
- sehr präzise
- weniger emotional

### Typografie

- reduzierte Interface-Typografie
- klare Labels
- wenig Fließtext
- starke Karten- und Legendenlogik

### Farben

- dunkler neutraler Hintergrund
- kühle, analytische Akzente
- kartografisch kontrollierte Farbskalen

### Eignung

Geeignet, wenn die Seite als geodatenbasierter Analyseprototyp erscheinen soll. Risiko: kann für Praxisakteure zu technisch wirken.

## 6. Vorläufige Empfehlung

Für die erste deutsche Vorzeigefassung sollte Designrichtung A die Basis bilden, mit leichten Elementen aus B.

Also:

**Institutionell ruhig + narrativ geführt**

Nicht:

- zu dashboardartig,
- zu experimentell,
- zu stark akademisch,
- zu werblich.

## 7. Dummyphase

Die Dummyphase sollte nicht sofort die bestehende Website umbauen.

Empfohlene Outputs:

1. `design_dummies/design_a_institutionell.html`
2. `design_dummies/design_b_editorial.html`
3. `design_dummies/design_c_kartografisch.html`

Alle drei Dummies verwenden denselben deutschen Kerntext und dieselbe Inhaltsstruktur. Nur Typografie, Farbgebung, Abstände und Tonalität unterscheiden sich.

## 8. Entscheidungskriterium

Die beste Variante ist nicht die schönste.

Die beste Variante ist die, bei der eine fachlich informierte Person die Transformationslogik am schnellsten und sichersten versteht.
"""

    write(BRIEF, brief)
    write(DESIGN, design)

    done_entry = f"""
## B73 - German presentation version brief ({today})

- Defined target audience: scientifically informed practitioners.
- Defined tone: narrative and explanatory.
- Defined scope: short and pointed first German presentation version.
- Created `docs/B73_deutsche_vorzeigefassung_brief.md`.
- Created `docs/B73_design_directions_brief.md`.
- Did not modify application files, maps, scripts, data or styling.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B73 - German presentation version brief" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B73 German presentation version brief complete.")
    print("Changed/created:")
    print(f"  {rel(BRIEF)}")
    print(f"  {rel(DESIGN)}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
