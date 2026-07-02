# B171 - Prune Obsolete Central Map Scripts

Date: 2026-07-01

## Ziel

Nach B169 bis B170 ist die zentrale Kartenfolge durch den neuen Live-Sticky-Zoom ersetzt.
Alte Script-Referenzen der vorherigen zentralen Kartenstory sollen nicht weiter auf der Live-Seite laufen.

B171 entfernt deshalb nur alte Script-Tags in `index.html`, die eindeutig zur vorherigen zentralen Map-Story gehören.

## Sicherheitsregel

B171 läuft nur, wenn der B169-Live-Sticky-Zoom bereits vorhanden ist:

```text
<!-- B169_LIVE_STICKY_ZOOM_START -->
```

Der neue Controller bleibt erhalten:

```text
src/b169_live_sticky_zoom.js
```

## Entfernte Script-Referenzen

| Script | Grund |
|---|---|
| `src/central_global_map_story.js` | obsolete central map story script after B169 live sticky zoom |
| `src/central_layer_state_hardener.js` | obsolete central map story script after B169 live sticky zoom |
| `src/central_step_state_bridge.js` | obsolete central map story script after B169 live sticky zoom |
| `src/central_stage_label_fix.js` | obsolete central map story script after B169 live sticky zoom |

## Behaltene Script-Referenzen

| Script |
|---|
| `src/app.js` |
| `src/hotspots.js` |
| `src/hotspot_base_layer.js` |
| `src/bw_peat_layer.js` |
| `src/b169_live_sticky_zoom.js` |

## Nicht geändert

- keine Kartenassets
- keine CSS-Regeln
- keine B169/B170-Texte
- keine Felt-Integration
- keine Datenquellen
- keine raw GIS-Dateien

## QA

Nach dem Patch:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Sticky-Zoom funktioniert weiterhin.
- Alle acht Steps wechseln Karte und Label.
- Oberschwaben-Step nutzt weiterhin die No-Label-Karte.
- Keine Console-Fehler zu fehlenden alten Map-Story-Funktionen.
