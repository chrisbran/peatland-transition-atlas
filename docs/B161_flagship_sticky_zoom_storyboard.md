# B161 - Flagship Sticky Zoom Storyboard

Date: 2026-07-01

## Arbeitstitel

```text
Der Maßstab entscheidet
```

## Storyboard V1

| Step | Bühnenbild | Textfunktion | Sichtbarer Textvorschlag | Karten-/Grafiklogik |
|---:|---|---|---|---|
| 00 | Dunkle/ruhige Kartenbühne, globale Konturen | Einstieg | `Moorbodenschutz beginnt als Klimathema.` | Weltkarte sehr reduziert, noch ohne Detaildruck |
| 01 | Globale Moorverbreitung | Relevanz | `Kleine Fläche, große Wirkung.` | Global Peatland Map 2.0; Moore als konzentrierte Flächen |
| 02 | Hotspot-/Druckebene | Druck | `Der Druck ist räumlich ungleich verteilt.` | Hotspots total oder density; nur wenige visuelle Schwerpunkte |
| 03 | Europa/Deutschland rückt ins Bild | Maßstab | `Aus globaler Relevanz wird politische Planung.` | Europa-/Deutschland-Kontext, Grenzen sehr zurückhaltend |
| 04 | Deutschland organische Böden | nationale Kulisse | `Die nationale Karte zeigt, wo genauer hingesehen werden muss.` | Thünen-Kulisse organischer Böden |
| 05 | Baden-Württemberg / Süddeutschland | regionale Konkretisierung | `In Baden-Württemberg wird die Frage regional.` | BW/Region als Zielausschnitt; falls Asset fehlt, mit vorhandener Deutschlandkarte + Annotation |
| 06 | Oberschwaben als Fokus | Übergabe | `In Oberschwaben trifft Moorbodenschutz auf Nutzung.` | Übergang zur bestehenden Oberschwaben-Storykarte, nicht Felt |
| 07 | Textübergabe | Abschluss | `Jetzt beginnt die eigentliche Planungsfrage.` | Karte blendet in den regionalen Abschnitt aus |

## Premium-Redaktion

Der Abschnitt soll nicht erklären, dass es mehrere Datenquellen gibt.
Er soll zeigen, dass die gleiche Frage auf jedem Maßstab anders aussieht.

## Kürzungsziel gegenüber aktueller Kartenfolge

- bestehende mehrteilige Kartenliste um 30–50 % Text reduzieren
- Methodik in eine einzige Quellenzeile plus Methodenteil verschieben
- Step-Zahl ideal: 5–7, nicht 10+

## Starkes Schlussbild

Der letzte Step darf nicht nach Dateninventar aussehen.
Er muss als Übergabe funktionieren:

```text
Die Karte zeigt nicht die Lösung.
Sie zeigt, wo die Verhandlung beginnt.
```

## Offene Designentscheidung

Variante A: vorhandene PNG-Stages nutzen  
Schneller, robust, näher an aktuellem Code.

Variante B: neue statische Kartenexports bauen  
Visuell stärker, aber höherer Aufwand.

Variante C: MapLibre/Vektor später  
Nicht für diese Schleife. Zu groß, solange Story/Pacing noch offen sind.

## Empfehlung

Für V2: **Variante A+**.

Das heißt:

- vorhandene PNG-Stages nutzen
- Step-Texte radikal kürzen
- Labels/Annotationen neu setzen
- Übergang nach Oberschwaben stärker inszenieren
- später nur gezielt einzelne Karten neu exportieren, falls visuell nötig
