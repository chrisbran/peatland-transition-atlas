# B136 - Frame Mismatch Bridge

Date: 2026-06-30

## Ziel

B136 verankert den zentralen V2-Erzählrahmen sichtbar:
Moorbodenschutz beginnt im Klimaframe, wird in der Umsetzung aber zur lokalen Frage von
Nutzung, Wasser, Eigentum, Betrieben und Wertschöpfung.

## Umsetzung

- neue kompakte Bridge-Section vor dem ersten Zoom-/Kartenblock
- drei Schritte: Klima, Raum, Umsetzung
- bewusst zurückhaltende Gestaltung mit Linien und kleinen Karten
- keine Änderung an Kartenlogik, Daten, Quellenblock oder Navigation

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/136_frame_mismatch_bridge.py`
- `docs/B136_frame_mismatch_bridge.md`
- `docs/B136_frame_mismatch_bridge_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Bridge steht vor dem ersten Zoom-/Kartenblock.
- Sie unterstützt die Story, ohne den Hero zu verdrängen.
- Drei Schritte sind auf Desktop nebeneinander und mobil gestapelt.
- Navigation und Scorecard bleiben unverändert.
