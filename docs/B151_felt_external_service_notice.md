# B151 - Felt External-Service Notice

Date: 2026-07-01

## Ziel

B151 ergänzt den neuen Felt-Kartenblock um einen kompakten Drittanbieter-Hinweis.
Der Felt-iframe ist ein externer Kartenservice; das soll im Seitenfluss transparent sein,
ohne den Kartenblock zu dominieren.

## Umsetzung

Unterhalb der Quellen-/Methodenzeile des Felt-Blocks wird ein kurzer Hinweis eingefügt:

- Felt wird als externer Kartendienst geladen
- OpenStreetMap-Hintergrunddaten werden genutzt
- beim Laden/Öffnen können Verbindungsdaten an externe Kartendienste übertragen werden
- die statische Kartenfassung bleibt als Fallback erhalten

## Nicht geändert

- keine Änderung am iframe-Code
- keine Änderung an Felt-Link oder Share-URL
- keine Änderung an Kartenlogik
- keine Änderung an lokalen GeoJSON-/Shapefile-Dateien
- kein Datenschutz-/Impressum-Ersatz

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/151_felt_external_service_notice.py`
- `docs/B151_felt_external_service_notice.md`
- `docs/B151_felt_external_service_notice_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Hinweis steht direkt unter dem Felt-Kartenblock.
- Hinweis ist lesbar, aber nicht dominant.
- Desktop-iframe lädt weiterhin.
- Mobile-Fallback bleibt unverändert.
