# B125c – Compact Source, Method and Rights

Stand: 2026-06-29

Status: **OK**

## Ziel

B125c fasst Quellen, Methodik und Nutzungsrechte in einen gemeinsamen, vollständig einklappbaren Abschnitt zusammen.

## Änderungen

- Register: `inserted_before_main_close`
- CSS: `inserted_or_replaced`
- Removed duplicate method-note fragments: 1
- Missing required entries: 0
- Visible risk findings: 0
- Source section count: 1
- Old rights section count: 0
- CSS marker count: 1
- Outer details count: 1
- Open attribute count: 0

## Review commands

```powershell
Get-Content docs\B125c_compact_source_method_rights_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path index.html -Pattern "Quellen, Methodik und Nutzungsrechte","Datengrundlagen, Rechte und Quellenvermerke","Nutzungsrechte und Datenlizenzen","Methodischer Hinweis:","CC BY 4.0","Datenlizenz Deutschland","EuroGeographics","Regierungspräsidium Freiburg","Thuenen","Ã","�"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
