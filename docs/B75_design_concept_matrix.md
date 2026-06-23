# B75 - Design Concept Matrix

Date: 2026-06-23

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
