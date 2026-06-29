# B125b – Data Rights and Attribution Register

Stand: 2026-06-29

Status: **OK**

## Ziel

B125b ergänzt B125 um genaue Rechte-, Lizenz- und Quellenhinweise zu den verwendeten Datengrundlagen.

## Änderungen

- Rechteblock: `inserted_before_method_box`
- CSS: `inserted_or_replaced`
- Missing required entries: 0
- Visible risk findings: 0
- Rights section count: 1
- CSS marker count: 1

## Review commands

```powershell
Get-Content docs\B125b_data_rights_and_attribution_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path index.html -Pattern "Nutzungsrechte und Datenlizenzen","CC BY 4.0","Datenlizenz Deutschland","EuroGeographics","Regierungspräsidium Freiburg","keine Weiterlizenzierung","GLOBAL_FRAME_V1","Thuenen","Ã","�"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
