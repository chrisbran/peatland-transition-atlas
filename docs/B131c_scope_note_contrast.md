# B131c - Scope Note Contrast

Date: 2026-06-30

## Ziel

B131c verbessert den Kontrast der kompakten Scope-Notiz aus B131b,
ohne sie wieder zu dominant werden zu lassen.

## Umsetzung

- stärkere Textkontraste für Label, Headline, Fließtext und Summary
- etwas kräftigere linke Akzentlinie
- sehr subtile helle Hinterlegung zur besseren Ablesbarkeit
- keine Änderung an HTML-Struktur oder Position

## Geänderte Dateien

- `src/styles.css`
- `scripts/131c_scope_note_contrast.py`
- `docs/B131c_scope_note_contrast.md`
- `docs/B131c_scope_note_contrast_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Scope-Notiz bleibt kompakt.
- Kontrast ist deutlich besser lesbar.
- Note wirkt weiterhin nicht wie ein dominanter Warnblock.
