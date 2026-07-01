# B152 - Oberschwaben/Felt Integration Consolidation

Date: 2026-07-01

## Ziel

B152 reduziert die Redundanz zwischen der bestehenden Oberschwaben-Karte und dem neuen
Felt-Block. Die Felt-Karte wird nicht mehr als weiterer Kartenabschnitt neben der alten Karte
gerahmt, sondern als interaktive Vertiefung der vorherigen statischen Story-Karte.

## Umsetzung

- Eyebrow: `Interaktive Vertiefung`
- neuer Titel:
  - `Die statische Karte zeigt die Lage – die interaktive Karte zeigt die Details`
- Text erklärt die Rollen:
  - vorherige Karte = Einordnung im Seitenfluss
  - Felt-Karte = interaktive Vertiefung
- zusätzliche Lesart-Box:
  - Schnittmenge = Prüfbedarf, nicht automatisch Eignung
  - konkrete Maßnahmen brauchen Wasserstand, Betrieb, Eigentum, Förderung und Wertschöpfung
- Desktop iframe bleibt erhalten
- Mobile Fallback bleibt erhalten
- Drittanbieter-Hinweis bleibt erhalten
- Quellen-/Methodenzeile bleibt erhalten
- lokale GeoJSON-/Shapefile-Dateien bleiben außerhalb des Repo

## Nicht geändert

- kein Entfernen der bestehenden Oberschwaben-Karte
- kein Entfernen des PNG-/Sticky-Fallbacks
- keine Änderung am Felt-iframe-Link
- keine Änderung an Kartenlogik oder Rohdaten

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/152_oberschwaben_felt_integration_consolidation.py`
- `docs/B152_oberschwaben_felt_integration_consolidation.md`
- `docs/B152_oberschwaben_felt_integration_consolidation_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Felt-Block wirkt als Vertiefung, nicht als Dopplung.
- Desktop iframe lädt weiterhin.
- Mobile Fallback bleibt sichtbar unter 760 px.
- Drittanbieter-Hinweis bleibt erhalten.
- Bestehende Oberschwaben-Karte bleibt unverändert vorhanden.
