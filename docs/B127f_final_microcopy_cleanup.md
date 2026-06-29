# B127f – Final Microcopy Cleanup

Stand: 2026-06-29

Status: **OK**

## Ziel

B127f entfernt zwei letzte sichtbare redaktionelle Kleinigkeiten vor dem Commit.

## Änderungen

- methodische_lesart_replaced: 1
- standalone_werte_gerundet_removed: 1
- Missing required entries: 0
- Visible risk findings: 0

## Review commands

```powershell
Get-Content docs\B127f_final_microcopy_cleanup_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path index.html -Pattern "Methodische Hinweise","Methodische Lesart","Lesart","Werte gerundet. Werte gerundet","Werte gerundet.","Ã","�"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```
