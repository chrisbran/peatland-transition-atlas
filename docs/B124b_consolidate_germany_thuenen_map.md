# B124b – Consolidate Germany Thünen Map

Stand: 2026-06-29

Status: **OK**

## Ziel

Die Deutschland/Thünen-Sequenz bleibt stabil, zeigt aber nicht mehr zwei kaum unterscheidbare Karten nacheinander.

## Änderungen

- JS state replacement hits: 1
- HTML step text replacement hits: 2
- `germany-thuenen-types` bleibt als State erhalten, nutzt aber dieselbe sichtbare Thünen-Kulisse wie `germany-thuenen-extent`.
- Keine Karten-, CSS- oder Datenänderung.

## Review commands

```powershell
Get-Content docs\B124b_consolidate_germany_thuenen_map_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path index.html,src\central_global_map_story.js -Pattern "germany-thuenen-types","layer-germany-thuenen-types","layer-germany-thuenen-extent","Für den Deutschland-Maßstab reicht eine Thünen-Karte","Thuenen","Ã","�"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
