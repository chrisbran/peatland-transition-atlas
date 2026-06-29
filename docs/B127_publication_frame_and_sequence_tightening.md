# B127 – Publication Frame and Sequence Tightening

Stand: 2026-06-29

Status: **OK**

## Ziel

B127 schärft den Veröffentlichungsrahmen und entfernt reine Grenz-/Rahmenkarten aus der zentralen Kartenfolge.

## Änderungen

- branding_hits: 3
- removed_boundary_steps: 2
- retitled_html_steps: 4
- retitled_js_titles: 2
- details_label_hits: 1
- footer_hits: 1
- css_hits: 1
- Missing required entries: 0
- Visible risk findings: 0
- Raw risk findings: 3
- Footer count: 1
- CSS marker count: 1

## Review commands

```powershell
Get-Content docs\B127_publication_frame_and_sequence_tightening_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path index.html,src\central_global_map_story.js,src\styles.css -Pattern "Moorbodenschutz","Details öffnen","Europa zeigt den größeren Bezugsraum","Deutschland grenzt den Prüfbedarf ein","Stand: Juni 2026","kompakt öffnen","data-global-state=`"europe-borders`"","data-global-state=`"germany-context`"","GLOBAL_FRAME_V1","Thuenen","Ã","�"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
