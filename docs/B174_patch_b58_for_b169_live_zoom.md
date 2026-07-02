# B174 - Patch B58 for B169 Live Zoom

Date: 2026-07-02

## Ziel

Nach B169 bis B172 ist die alte zentrale Kartenstory durch den neuen Live-Sticky-Zoom ersetzt.
B58 prüfte aber noch die alten zentralen States:

```text
europe-peat
germany-thuenen-extent
germany-thuenen-types
```

Diese States sind in `index.html` nach der B169-Integration bewusst nicht mehr aktiv.
Deshalb war der B58-FAIL ein veralteter QA-Check, kein aktueller Seitenfehler.

## Änderung

`scripts/58_visual_qa_and_commit_check.py` wurde aktualisiert.

Der neue B58 erkennt automatisch:

```text
B169 live sticky zoom
```

wenn in `index.html` einer dieser Marker vorhanden ist:

```text
B169_LIVE_STICKY_ZOOM_START
src/b169_live_sticky_zoom.js
```

Dann prüft B58 die aktive B169-State-Matrix:

```text
global-peat
global-pressure-total
global-pressure-density
europe-bridge
germany-extent
germany-types
baden-wuerttemberg
oberschwaben-handoff
```

und behandelt alte zentrale Map-Story-Scripts nur noch dann als aktiv, wenn sie weiterhin in `index.html` referenziert sind.

## Zusätzlich geprüft

Im B169-Modus prüft B58 jetzt auch:

```text
public/maps/bw/bw_bk50_moor_extent.png
public/maps/bw/bw_admin_context.png
public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png
```

## Nicht geändert

- keine öffentliche Seite
- keine CSS-Regeln
- keine Kartenassets
- keine Datenquellen
- keine raw GIS-Dateien

## Nächster Schritt

```powershell
python scripts\58_visual_qa_and_commit_check.py
```

Erwartung:

```text
RESULT: PASS
```
