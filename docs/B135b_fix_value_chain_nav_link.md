# B135b - Fix Value-Chain Navigation Link

Date: 2026-06-30

## Anlass

B135 konnte den Zielanker setzen, hat den Navigationslink aber nicht sichtbar ergänzt.
Ursache: Die Prüfung auf `Wertschöpfung` war zu breit und konnte Treffer im Seiteninhalt
statt nur in der Navigation als vorhandenen Link interpretieren.

## Umsetzung

- prüft nur den tatsächlichen `<nav>`-Block
- ergänzt `Wertschöpfung` als Link zu `#wertschoepfung`
- Einfügung vor `Prüfpfade`, Fallback vor `Quellen`
- stellt sicher, dass der Zielanker `#wertschoepfung` vorhanden ist
- keine Änderung an Scorecard-Inhalt, Kartenlogik, Daten oder CSS

## Geänderte Dateien

- `index.html`
- `scripts/135b_fix_value_chain_nav_link.py`
- `docs/B135b_fix_value_chain_nav_link.md`
- `docs/B135b_fix_value_chain_nav_link_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Hauptnavigation enthält `Wertschöpfung`.
- Klick auf `Wertschöpfung` springt zur Scorecard/Engpass-Section.
- Navigation bricht auf Desktop nicht unschön.
