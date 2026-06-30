# B138 - Soil Context Precision Note

Date: 2026-06-30

## Ziel

B138 schärft die fachliche Begrifflichkeit im Oberschwaben-Abschnitt.
Die regionale Karte soll nicht als parzellenscharfer Moorbodennachweis oder Eignungskarte
verstanden werden, sondern als BK50-basierte Moor-/Feuchtbodenkulisse für Prüfbedarf.

## Umsetzung

- kurze Note im Oberschwaben-Abschnitt
- Begriffsklärung: BK50-Moor- und Feuchtbodenkontext
- klare Abgrenzung: Orientierungskulisse, keine Flächeneignung
- zurückhaltendes Layout als kleine redaktionelle Notiz
- keine Änderung an Kartenlogik, Daten, Navigation, Scorecard oder Quellenblock

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/138_soil_context_precision_note.py`
- `docs/B138_soil_context_precision_note.md`
- `docs/B138_soil_context_precision_note_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Note erscheint im Oberschwaben-Abschnitt.
- Sie ist sichtbar, aber nicht dominant.
- Sie klärt den BK50-Moor-/Feuchtbodenkontext.
- Karten, Navigation, Scorecard und Quellenblock bleiben unverändert.
