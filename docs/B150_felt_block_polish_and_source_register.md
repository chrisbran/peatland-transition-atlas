# B150 - Felt Block Polish and Source Register

Date: 2026-07-01

## Ziel

B150 macht den B149-Felt-Block sprachlich publikationstauglicher und ergänzt den zentralen
Quellennachweis um einen Eintrag zur interaktiven Oberschwaben-Karte.

## Umsetzung

- `Interaktiver Kartenpilot` wird zu `Interaktive Karte`
- öffentlicher Text entfernt interne Prototyp-Sprache
- Desktop-/Mobile-Logik bleibt unverändert
- iframe und Felt-Link bleiben aus B149 erhalten
- Quellen-/Methodenzeile im Kartenblock wird präzisiert
- zentraler Quellennachweis erhält einen Hinweis zu:
  - Felt
  - OpenStreetMap
  - FIONA 2024
  - BK50-Moor-/Feuchtbodenkontext
  - GISCO/NUTS-Landkreisgrenzen
  - mapshaper-Vereinfachung

## Nicht geändert

- kein Austausch der bestehenden Oberschwaben-Karte
- keine Änderung an Kartenlogik
- keine lokalen GeoJSON-/Shapefile-Dateien im Repo
- kein Entfernen des PNG-Fallbacks

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/150_felt_block_polish_and_source_register.py`
- `docs/B150_felt_block_polish_and_source_register.md`
- `docs/B150_felt_block_polish_and_source_register_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Felt-Block wirkt nicht mehr wie interner Prototyp.
- Desktop iframe lädt weiterhin.
- Mobile Fallback bleibt sichtbar unter 760 px.
- Zentraler Quellenblock enthält den Felt-/OSM-/mapshaper-Hinweis.
