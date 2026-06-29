# B124 – Rebuild Central Scrolly Single Source

Stand: 2026-06-29

Status: **OK**

## Ziel

B124 ersetzt die fragile zentrale Kartensteuerung durch einen einzelnen Controller mit einer einzigen State-Tabelle.

## Architektur

- aktiv: `src/central_global_map_story.js`
- no-op: `src/central_layer_state_hardener.js`
- no-op: `src/central_step_state_bridge.js`
- no-op: `src/central_stage_label_fix.js`

## Audit summary

- Risk findings: 0
- Missing states: 0
- Missing public strings: 0
- Active helper observer/data-state hits: 0

## Review commands

```powershell
Get-Content docs\B124_central_scrolly_single_source_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path index.html,src\*.js,src\*.css -Pattern "GLOBAL_FRAME_V1","Country hotspot layer","Peatland context","Thuenen","ArcGIS","BW frame","Daten: FAOSTAT","Daten: GISCO","Daten: Thünen"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
