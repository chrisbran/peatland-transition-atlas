# B125 – Source and Method Register

Stand: 2026-06-29

Status: **OK**

## Ziel

B125 ergänzt nach dem stabilisierten B124/B124b-Stand einen kompakten Quellen- und Methodikbereich.

## Änderungen

- Register: `inserted_before_main_close`
- CSS: `inserted_or_replaced`
- Visible risk findings: 0
- Missing required entries: 0
- Source section count: 1
- CSS marker count: 1
- href count in page: 29

## Review commands

```powershell
Get-Content docs\B125_source_and_method_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path index.html -Pattern "Quellen und Methodik","IPCC Wetlands Supplement","FAOSTAT","Thünen-Kulisse","FIONA Baden-Württemberg","SOLAMO-BW","keine hydrologische Modellierung","GLOBAL_FRAME_V1","Thuenen","Ã","�"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
