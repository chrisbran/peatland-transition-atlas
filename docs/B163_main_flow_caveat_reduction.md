# B163 - Main-Flow Caveat Reduction

Date: 2026-07-01

## Ziel

B163 reduziert wiederholte sichtbare Caveats im Hauptfluss, ohne fachliche Grenzen zu löschen.

Nach B158 und B162c ist die Seite ruhiger, aber in den regionalen Abschnitten erscheinen noch mehrfach ähnliche Warnformeln:

```text
keine Eignungskarte
keine Priorisierung
keine betriebliche Betroffenheitsanalyse
Orientierung
Prüfbedarf
```

Diese Aussagen bleiben fachlich wichtig. Für Premium-Pacing sollen sie aber nicht ständig als Bremsklotz im Lesefluss stehen.

## Prinzip

- Scope-Box am Anfang bleibt erhalten.
- Methode/Quellen bleiben der Ort für Detailgrenzen.
- Regionale Kartenabschnitte behalten ihre Aussagegrenzen, aber in knapperer Form.
- Keine neue Fachbehauptung.
- Keine Änderung an Karten, Felt, Scorecard, Matrixstruktur oder Daten.

## Ersetzungen

| ID | Treffer | Zweck |
|---|---:|---|
| `oberschwaben_step_label` | 1 | turns a warning label into a quieter map-reading label |
| `oberschwaben_step_title` | 1 | keeps the limitation but removes repetitive negative phrasing |
| `oberschwaben_step_body` | 1 | keeps the meaning with one positive sentence and one concise boundary |
| `felt_source_line` | 1 | moves repeated caveat wording into the method link |
| `area_balance_note` | 1 | reduces a repeated warning block in the area-balance section |
| `area_balance_source_line` | 1 | keeps data/source line but removes repeated no-suitability phrasing |
| `transform_paths_work_rule` | 1 | turns another caveat repetition into the section's positive argument |
| `matrix_footer` | 1 | keeps the methodological boundary in less repetitive wording |

## Caveat-Term-Zählung in `index.html`

| Begriff | Vorher | Nachher |
|---|---:|---:|
| keine Eignungskarte | 4 | 3 |
| keine Priorisierung | 6 | 3 |
| keine hydrologische Modellierung | 3 | 3 |
| keine betriebliche Betroffenheitsanalyse | 3 | 0 |
| keine Flächeneignung | 3 | 1 |
| keine Standortempfehlung | 1 | 0 |
| Prüfbedarf | 7 | 7 |
| Orientierung | 15 | 12 |
| Hinweis | 7 | 7 |

Gesamt:

- vorher: 49
- nachher: 36

Die Zählung ist nur ein grober Indikator. Entscheidend bleibt die sichtbare Lesbarkeit im Hauptfluss.

## QA

Nach dem Patch:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- regionale Kartenabschnitte wirken weniger defensiv
- Scope bleibt fachlich klar
- Flächenbilanz bleibt methodisch abgesichert
- keine Layoutänderung
