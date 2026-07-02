# B136b - Frame Bridge Alignment

Date: 2026-06-30

## Anlass

Die B136-Frame-Mismatch-Bridge stand im lokalen Screenshot zu dicht am linken Rand.
Ursache ist wahrscheinlich, dass der neue Bridge-Block zwar eine innere Maximalbreite hatte,
aber nicht ausreichend gegen den Viewport zentriert und gepolstert wurde.

## Umsetzung

- B136-CSS-Block ersetzt
- `.b136-frame-bridge .section-inner` erhält explizite Breite, horizontale Gutters und Zentrierung
- `.b136-frame-bridge__inner` wird ebenfalls zentriert
- keine Änderung an HTML, Text, Navigation, Kartenlogik oder Daten

## Geänderte Dateien

- `src/styles.css`
- `scripts/136b_frame_bridge_alignment.py`
- `docs/B136b_frame_bridge_alignment.md`
- `docs/B136b_frame_bridge_alignment_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Bridge steht nicht mehr am linken Rand.
- Bridge ist horizontal ähnlich eingebunden wie die übrigen Content-Blöcke.
- Desktop und mobile Ansicht behalten ausreichende Seitenabstände.
- Die drei Karten bleiben sauber nebeneinander bzw. mobil gestapelt.
