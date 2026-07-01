# B156 - Visible `Umsetzung` Wording Polish

Date: 2026-07-01

## Ziel

B103b meldete sechs sichtbare Review-Kandidaten für wiederholte Verwendungen von `Umsetzung`.
B156 reduziert diese Wiederholung gezielt und ersetzt sie dort, wo präzisere Wörter fachlich besser passen.

## Prinzip

- keine Änderung an Karten, Daten, Quellen oder Struktur
- nur sichtbare Formulierungen im öffentlichen Seitenfluss
- keine versteckten/retired Abschnitte anfassen
- keine inhaltliche Abschwächung der V2-These

## Ersetzungen

| ID | Treffer | Neue Formulierung | Zweck |
|---|---:|---|---|
| `frame_mismatch_sentence` | 1 | In der Praxis entscheidet sich das Thema dort, wo Wasserstand, Nutzung, Eigentum, Betriebe und Wertschöpfungsketten zusammenkommen. | reduces repeated Umsetzung in the Frame-Mismatch paragraph |
| `frame_step_heading` | 1 | Lokale Ketten entscheiden | turns a topic label into a sharper statement title |
| `value_chain_scaling_sentence` | 1 | Kleinere Mengen, fehlende Skalierung oder unsichere Absatzwege begrenzen die Marktfähigkeit. | makes the value-chain bottleneck more specific |
| `water_governance_start_sentence` | 1 | Deshalb beginnt Abstimmung oft dort, wo Zuständigkeiten nicht deckungsgleich sind. | fits the water/governance argument more precisely |
| `water_governance_consequence_sentence` | 1 | Planung braucht zusätzlich lokale Wasserkenntnis, Abstimmung zwischen Eigentümern und Betrieben sowie tragfähige Bewirtschaftungs- und Verwertungspfade. | uses planning language in a planning/governance sentence |
| `consequence_sentence` | 1 | Für die Praxis reicht die Flächenperspektive aber nicht aus: | keeps the concluding sentence concrete and avoids repetition |

## Zählung

- `Umsetzung` in `index.html` vorher: 7
- `Umsetzung` in `index.html` nachher: 1

Die Zählung umfasst das gesamte HTML. Maßgeblich für die öffentliche Bewertung bleibt weiterhin `scripts/103b_corrected_visible_text_audit.py`.

## QA

Nach dem Patch:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```
