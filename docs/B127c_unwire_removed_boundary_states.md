# B127c – Unwire Removed Boundary States

Stand: 2026-06-29

Status: **OK**

## Ziel

B127c entfernt nach der Straffung der Kartenfolge die nicht mehr sichtbaren Grenz-States auch aus dem zentralen JS-Controller.

## Änderungen

- removed_index_articles: 0
- removed_js_state_objects: 0
- removed_loose_js_mentions: 0
- Missing required entries: 0
- Raw risk findings: 0
- Visible risk findings: 0

## Review commands

```powershell
Get-Content docs\B127c_unwire_removed_boundary_states_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path index.html,src\central_global_map_story.js -Pattern "europe-borders","germany-context","bw-context","europe-peat","germany-thuenen-extent","bw-bk50-extent","GLOBAL_FRAME_V1","Thuenen","Ã","�"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
