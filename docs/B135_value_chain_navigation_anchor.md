# B135 - Value-Chain Navigation Anchor

Date: 2026-06-30

## Ziel

B135 macht die neue V2-Kernaussage zur Wertschöpfungskette navigierbar.
Die Engpass-/Scorecard-Section erhält einen stabilen Anker und die Hauptnavigation
einen Eintrag `Wertschöpfung`.

## Fachlicher Grund

Die V2-Erzählung verschiebt den Schwerpunkt von reiner Moor- und Nutzungskartierung
hin zur Frage, ob Verarbeitung, Abnahme, Standards und Mengen als Kette funktionieren.
Diese Stelle sollte daher direkt erreichbar sein.

## Umsetzung

- Zielanker `#wertschoepfung` an der B130/B130b-Wertschöpfungs-Scorecard
- neuer Navigationslink `Wertschöpfung`
- Einfügung vor `Prüfpfade`, falls möglich
- keine Änderung an Kartenlogik, Daten, Scorecard-Inhalt oder Matrix

## Hinweis zu B134

Der Audit vermerkt, ob noch B134-Marker im Arbeitsbaum sichtbar sind.
B134 sollte vor einem Commit verworfen sein, falls der mobile Matrix-Test nicht übernommen werden soll.

## Geänderte Dateien

- `index.html`
- `scripts/135_value_chain_navigation_anchor.py`
- `docs/B135_value_chain_navigation_anchor.md`
- `docs/B135_value_chain_navigation_anchor_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Navigation enthält `Wertschöpfung`.
- Klick auf `Wertschöpfung` springt zur Scorecard/Engpass-Section.
- Navigation bricht auf Desktop nicht unschön.
- B134 ist nicht versehentlich im Commit enthalten.
