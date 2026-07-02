# B160 - Narrative Cut Plan

Date: 2026-07-01

## Ziel

B160 übersetzt den B159-Editorial-Audit in einen konkreten Schnittplan.
Der Patch verändert die öffentliche Seite nicht. Er entscheidet, welche Inhalte im Hauptfluss bleiben, welche gekürzt, verschoben oder visuell neu gebaut werden sollen.

## Leitentscheidung

> Nicht mehr vollständiger werden. Schärfer werden.

Die V2 soll auf eine klare fünfaktige Dramaturgie geschnitten werden. Methodische Absicherung bleibt erhalten, aber weniger davon darf den Lesefluss dominieren.

## Fünf Akte

| Akt | Aussage | Funktion | Behalten | Kürzen/Verschieben |
|---|---|---|---|---|
| A1 | Moore sind klein, aber klimatisch groß. | Hook, Relevanz, Versprechen der Seite. | Hero, eine starke These, ein kurzer Scope-Hinweis. | lange Vorbemerkungen, wiederholte Demonstrator-/Nicht-Eignungshinweise. |
| A2 | Karten zeigen den Maßstabssprung. | Globaler Kontext wird zu regionaler Planungsfrage. | ein choreografierter Kartenmoment global → Deutschland/BW → Oberschwaben. | zu viele einzelne Zwischenkarten oder erklärende Kartenlisten. |
| A3 | In Oberschwaben trifft Moorbodenschutz auf reale Nutzung. | Der abstrakte Moorschutz wird konkret. | statische Story-Karte, Felt-Vertiefung, Flächenbilanz. | Dopplungen zwischen statischer Karte, Felt und Bilanz. |
| A4 | Aus Schnittmenge folgt Verhandlung. | Wasser, Betriebe, Zuständigkeiten und Pfade erklären, warum Karte nicht Lösung ist. | ein starker Governance-/Transformationsmoment. | lange Pfadbeschreibungen, wenn sie nicht visuell tragen. |
| A5 | Der Engpass liegt hinter dem Feld. | Climax: nicht das nasse Bewirtschaften allein limitiert, sondern die Kette danach. | eine erinnerbare Wertschöpfungsgrafik + kurzer Kicker. | Scorecard-/Matrix-Dopplungen, Quellenblöcke im Hauptfluss. |

## Automatische Schnittbilanz

- Datenquelle: B159 CSV
- Sections im Plan: 21
- grobe Wortzahl: 2868
- geschätztes Kürzungspotenzial im Hauptfluss: ca. 34.7 %

Das Ziel aus B159 war 20–35 % weniger sichtbarer Erklärtext. Dieser Plan liegt bewusst in diesem Korridor, ohne Fachgrenzen zu löschen.

## Entscheidungstypen

| Entscheidung | Anzahl |
|---|---:|
| `compress` | 2 |
| `keep` | 3 |
| `keep/tighten` | 3 |
| `move/collapse` | 1 |
| `rebuild` | 10 |
| `visualise` | 2 |

## Wichtigste redaktionelle Eingriffe

### 1. Scope und Caveats konsolidieren

Ein starker Scope-Hinweis am Anfang bleibt. Wiederholte Nicht-Eignungskarten-, Priorisierungs- und Modellierungswarnungen werden im Hauptfluss reduziert und in Methode/Quellen konzentriert.

### 2. Kartenfolge als Flagship-Zoom neu denken

Die existierende globale Kartenfolge ist fachlich nützlich, aber editorial noch zu listenartig. B161 soll daraus einen einzigen großen Sticky-Moment konzipieren:

```text
global → Europa/Deutschland → Baden-Württemberg → Oberschwaben
```

### 3. Oberschwaben bleibt der Beleg

Statische Karte, Felt-Vertiefung und Flächenbilanz bleiben, aber mit klarer Rollenverteilung:

- statische Karte: Lage und Layerlogik
- Felt: Details und Interaktion
- Bilanz: quantitative Verdichtung

### 4. Governance als visuelles Zwischenbild

`Wasser folgt Einzugsgebieten, nicht Eigentumsgrenzen` ist stark, sollte aber weniger wie ein Fachabschnitt und stärker wie ein Diagramm wirken.

### 5. Wertschöpfung als Climax neu bauen

Der wichtigste Premium-Gap liegt hier. Der bestehende Scorecard-/Matrix-Ansatz ist korrekt, aber noch nicht ikonisch.

Leitmotiv für B162:

```text
Das Feld funktioniert. Die Kette dahinter reißt.
```

## Abschnittsmatrix

Siehe `docs/B160_section_cut_matrix.csv`.

## Nächste Patches

```text
B161 Flagship Sticky Zoom Concept
B162 Value-Chain Visual Climax Redesign
B163 Main-Flow Caveat Reduction
B164 Premium Pacing Polish
```
