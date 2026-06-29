# B127b – Remove BW Boundary-only Step

Stand: 2026-06-29

Status: **OK**

## Ziel

B127b entfernt auch den reinen Baden-Württemberg-Grenzschritt aus der zentralen Kartenfolge.

## Änderungen

- removed_bw_boundary_step: 1
- retitled_html_step: 2
- retitled_js_state: 1
- Missing required entries: 0
- Visible risk findings: 0
- Raw risk findings: 0

## Review commands

```powershell
Get-Content docs\B127b_remove_bw_boundary_only_step_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path index.html,src\central_global_map_story.js -Pattern "Baden-Württemberg macht die Frage regional konkret","Hier wird sichtbar, wo Moor- und Feuchtbodenkontexte","data-global-state=`"bw-context`"","data-global-state=`"bw-bk50-extent`"","Der Bodenkontext zeigt","GLOBAL_FRAME_V1","Thuenen","Ã","�"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
