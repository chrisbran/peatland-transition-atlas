# B154 - Oberschwaben Flow Spacing Polish

Date: 2026-07-01

## Ziel

B154 glättet den Übergang zwischen drei inzwischen wichtigen Oberschwaben-Bausteinen:

1. statische Oberschwaben-Storykarte
2. interaktive Felt-Vertiefung
3. Flächenbilanz der Schnittmenge

Der Patch soll die Felt-Karte nicht wie eine Dopplung wirken lassen, sondern sie als
Vertiefung zwischen räumlicher Einordnung und quantitativer Bilanz lesbar machen.

## Umsetzung

- kleiner Übergangstext nach dem Felt-Block:
  - `Nach der räumlichen Vertiefung folgt die Bilanz...`
- sanftere vertikale Abstände zwischen Felt-Block und Flächenbilanz
- keine Änderung am Felt-iframe
- keine Änderung an Kartenlogik, Daten oder Quellen
- bestehende Oberschwaben-Karte bleibt erhalten

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/154_oberschwaben_flow_spacing_polish.py`
- `docs/B154_oberschwaben_flow_spacing_polish.md`
- `docs/B154_oberschwaben_flow_spacing_polish_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Übergang zwischen Felt-Karte und Flächenbilanz ist ruhiger.
- Felt-Block wirkt als Vertiefung, nicht als Dopplung.
- Flächenbilanz folgt logisch auf die interaktive Karte.
- Desktop iframe lädt weiterhin.
- Mobile Fallback bleibt unverändert.
