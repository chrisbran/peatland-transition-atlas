# B126 – Publication Wording Polish

Stand: 2026-06-29

Status: **REVIEW REQUIRED**

## Ziel

B126 schärft die öffentliche Fachkommunikation: weniger Projektlogik, mehr fachliche Aussage und Prüfbedarf.

## Änderungen

- nav_hits: 1
- generic_html_hits: 8
- generic_js_hits: 11
- central_index_step_hits: 14
- oberschwaben_step_hits: 4
- central_js_title_hits: 7
- flaechen_hits: 1
- Navigation OK: True
- Missing required entries: 0
- Visible risk findings: 1
- Raw risk findings: 1

## Review commands

```powershell
Get-Content docs\B126_publication_wording_polish_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path index.html,src\central_global_map_story.js -Pattern "Problem","Karten","Oberschwaben","Prüfpfade","Quellen","Fachliche Klammer","Lesart","Daten: ","Fachliche Grundlage:","Europa zeigt den größeren Bezugsraum","Deutschland grenzt den Prüfbedarf ein","Die nationale Kulisse ersetzt keine Standortprüfung","Werte gerundet. Werte gerundet","Ackerland ohne separat"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
