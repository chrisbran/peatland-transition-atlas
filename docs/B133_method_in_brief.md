# B133 - Method in Brief

Date: 2026-06-30

## Ziel

B133 ergänzt eine kompakte Methode-in-Kürze-Box im bestehenden Quellen-/Methodikbereich
und präzisiert die Projektnennung im Footer.

## Umsetzung

- neue Box `Methode in Kürze` vor `Methodische Hinweise`
- Anker `id="methode-in-kuerze"`
- kurze Beschreibung von Quellen, Datenständen, Verschneidungslogik und BK50-Generalisierung
- klare Abgrenzung: Orientierung, keine Flächeneignung oder Einzelfallentscheidung
- Footer präzisiert: eigenständiger fachlicher Demonstrator, kein offizielles Produkt

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/133_method_in_brief.py`
- `docs/B133_method_in_brief.md`
- `docs/B133_method_in_brief_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Quellenblock öffnen.
- `Methode in Kürze` steht vor `Methodische Hinweise`.
- Text ist kompakt und nicht zu technisch.
- Footer-Projektnennung ist präzisiert.
- Keine Layout-Verschiebung im Quellenblock.
