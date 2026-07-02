# B140 - Unified Source Lines

Date: 2026-06-30

## Ziel

B140 vereinheitlicht kompakte Quellen-/Methodikzeilen unter zentralen Karten-, Grafik-
und Erzählblöcken. Damit wird der V2-Standard `Quellzeile + Methode-Link unter jeder Grafik`
schrittweise umgesetzt, ohne Kartenlogik oder Daten anzufassen.

## Umsetzung

- B130b-Quellenbox erhält einen Link auf `Methode in Kürze`
- kompakte Quellen-/Methodikzeilen für:
  - Frame-Mismatch-Bridge
  - globalen Karten-/Kontextblock
  - regionalen Oberschwaben-/Schnittmengenblock
  - Wasser-und-Governance-Block
  - Konsequenz-Kicker
- CSS für ein einheitliches, zurückhaltendes Erscheinungsbild
- keine Änderung an Kartenlogik, Daten, Navigation oder Scorecard-Struktur

## Hinweise

Die Zeilen sind bewusst kurz und verweisen auf den zentralen Methodenanker `#methode-in-kuerze`.
Sie ersetzen nicht den zentralen Quellen- und Rechtenachweis, sondern machen die Herkunft und
Einordnung direkt im Lesefluss sichtbar.

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/140_unified_source_lines.py`
- `docs/B140_unified_source_lines.md`
- `docs/B140_unified_source_lines_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- kompakte Quell-/Methodenzeilen erscheinen unter den relevanten Blöcken
- Methode-Links springen zu `Methode in Kürze`
- Zeilen wirken zurückhaltend und nicht wie zusätzliche Absätze
- keine doppelten B140-Quellzeilen nach erneutem Ausführen
- Karten, Scorecard, Navigation und Quellenblock bleiben unverändert
