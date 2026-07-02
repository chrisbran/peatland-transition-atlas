# B159 - Editorial Elevation Audit

Date: 2026-07-01

## Ziel

B159 stoppt bewusst den reinen QA-/Patchmodus und bewertet die Seite als Editorial/Data-Feature.
Maßstab ist nicht nur fachliche Korrektheit, sondern Wirkung auf dem Niveau großer datenjournalistischer Features.

## Kurzurteil

> Aktueller Stand: starker fachlicher Demonstrator mit deutlich verbesserter Karte und klarer These.
> Noch nicht: radikal kuratiertes, visuell inszeniertes Premium-Feature.

Die Seite ist inzwischen fachlich belastbar, aber sie erklärt noch zu viel. Für ein stärkeres Editorial-Level braucht sie weniger sichtbare Absicherung, einen klareren visuellen Höhepunkt und eine stärkere Dramaturgie.

## Automatische Kennzahlen

- untersuchte Sections: 21
- grobe Wortzahl in Sections: 2868
- sichtbare Hinweis-/Warnwort-Treffer: 49
- mittlerer Editorial-Score: 6.2/10

## Fünf-Akt-Struktur

Die Seite sollte ab jetzt konsequent auf diese fünf Akte geschnitten werden:

1. **Moore sind klein, aber klimatisch groß.**
2. **Karten zeigen den Maßstabssprung von globaler Relevanz zu regionaler Planung.**
3. **In Oberschwaben trifft Moorbodenschutz auf reale Nutzung.**
4. **Aus Schnittmenge folgt Verhandlung: Wasser, Betriebe und Zuständigkeiten entscheiden.**
5. **Der Engpass liegt hinter dem Feld: Verarbeitung, Abnahme, Standards und Mengen.**

Alles, was diese Akte nicht stärkt, sollte gekürzt, in Methode/Quellen verschoben oder in eine stärkere Grafik übersetzt werden.

## Premium-Gap gegenüber NYT / ZEIT / Guardian

| Dimension | Aktueller Stand | Premium-Ziel |
|---|---|---|
| These | klar und fachlich belastbar | noch stärker als ein erinnerbarer Satz inszenieren |
| Karten | Felt ist echter Qualitätssprung | ein großer choreografierter Sticky-Zoom fehlt |
| Pacing | stabil, aber erklärend | 20–35 % weniger sichtbarer Text im Hauptfluss |
| Methodik | sehr transparent | weniger sichtbare Caveats, mehr Appendix/Details |
| Wertschöpfung | inhaltlich stark | visuell als Climax neu denken |
| Mobile | pragmatisch robust | kürzerer Lesefluss, weniger Boxen, klarere Bildmomente |

## Handlungskategorien

| Aktion | Anzahl |
|---|---:|
| `candidate_for_flagship_zoom` | 1 |
| `compress_caveats` | 1 |
| `keep_or_trim` | 2 |
| `keep_tighten_transition` | 1 |
| `move_to_appendix_or_keep_collapsed` | 5 |
| `rebuild_visual_climax` | 10 |
| `turn_into_visual_moment` | 1 |

## Story-Akte im aktuellen HTML

| Akt | Anzahl Sections |
|---|---:|
| A1 Hook / promise | 3 |
| A2 Why it matters / scale jump | 14 |
| A3 Regional concretisation | 2 |
| A5 Climax / bottleneck behind the field | 1 |
| Unclear / supporting | 1 |

## Prioritäre Eingriffe

| Nr. | Überschrift | Akt | Aktion | Begründung |
|---:|---|---|---|---|
| 1 | Moorbodenschutz braucht räumliche Orientierung | A1 Hook / promise | `rebuild_visual_climax` | The thesis is strong, but the visual language should become a memorable editorial graphic. |
| 3 | Fachlicher Demonstrator, keine Eignungskarte | A1 Hook / promise | `rebuild_visual_climax` | The thesis is strong, but the visual language should become a memorable editorial graphic. |
| 4 | Moorbodenschutz wird erst mit Boden, Nutzung und Wasserstand planbar | A1 Hook / promise | `rebuild_visual_climax` | The thesis is strong, but the visual language should become a memorable editorial graphic. |
| 6 | Moorbodenschutz beginnt als Klimathema – und wird vor Ort zur Nutzungsfrage | A2 Why it matters / scale jump | `rebuild_visual_climax` | The thesis is strong, but the visual language should become a memorable editorial graphic. |
| 9 | In Oberschwaben wird Moorbodenschutz zur konkreten Nutzungsfrage | A2 Why it matters / scale jump | `rebuild_visual_climax` | The thesis is strong, but the visual language should become a memorable editorial graphic. |
| 10 | Unterschiedliche Flächen brauchen unterschiedliche Transformationspfade | A2 Why it matters / scale jump | `rebuild_visual_climax` | The thesis is strong, but the visual language should become a memorable editorial graphic. |
| 11 | Die Karten zeigen Prüfbedarf, aber keine Flächeneignung | A3 Regional concretisation | `candidate_for_flagship_zoom` | This is where the premium sticky zoom should be earned. |
| 12 | Warum Oberschwaben? | A2 Why it matters / scale jump | `rebuild_visual_climax` | The thesis is strong, but the visual language should become a memorable editorial graphic. |
| 13 | Oberschwaben, wo Moorschutz auf Landwirtschaft trifft | A2 Why it matters / scale jump | `compress_caveats` | Too many caveats in the visible flow; move detail to method or collapse. |
| 16 | Aus der Schnittmenge folgt Verhandlung, keine Einheitslösung | A2 Why it matters / scale jump | `rebuild_visual_climax` | The thesis is strong, but the visual language should become a memorable editorial graphic. |
| 18 | Nutzungskontexte entscheiden, welche Wertschöpfungspfade plausibel sind | A2 Why it matters / scale jump | `rebuild_visual_climax` | The thesis is strong, but the visual language should become a memorable editorial graphic. |
| 19 | Wasser folgt Einzugsgebieten, nicht Eigentumsgrenzen | A2 Why it matters / scale jump | `turn_into_visual_moment` | Good concept, but should become a diagrammatic editorial beat. |
| 20 | Der Hebel verschiebt sich von der Fläche zur Kette | A5 Climax / bottleneck behind the field | `rebuild_visual_climax` | The thesis is strong, but the visual language should become a memorable editorial graphic. |

## Redaktionelle Leitentscheidung

Ab jetzt nicht mehr fragen: `Was können wir noch hinzufügen?`

Stattdessen fragen:

- Was ist der eine Satz, der hängen bleibt?
- Welche drei Bilder bleiben im Kopf?
- Welche Fachdetails gehören in Methode/Quellen statt in den Hauptfluss?
- Wo ist der stärkste Scrolly-Moment?
- Wo wird aus einer richtigen Aussage eine erinnerbare Szene?

## Empfehlung

Der nächste produktive Schritt ist kein Release-Audit, sondern ein **Narrative Cut Plan**:

```text
B160 Narrative Cut Plan
B161 Flagship Sticky Zoom Concept
B162 Value-Chain Visual Climax Redesign
B163 Main-Flow Caveat Reduction
```

## Dateien

- Section inventory: `docs/B159_editorial_section_inventory.csv`
