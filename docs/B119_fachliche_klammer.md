# B119 – Fachliche Klammer

Stand: 2026-06-26

## Zweck

B119 stärkt die fachliche Klammer der Seite, ohne sie zu einer Projektvorstellungsseite umzubauen.

## Eingebaut

- Wasserstand-/Treibhausgas-Mechanismus
- Oberschwaben als fachlich begründeter Fokusraum
- Transformationspfade als Prüfpfade aus Nutzungskontexten
- kompakte Quellenhinweise zu offiziellen und methodischen Grundlagen

## Actions

| Action | Status |
|---|---|
| `replace transformation heading` | `changed:Welche Nutzungen bei hohen Wasserständen tragfähig werden können` |
| `insert climate mechanism block before centralGlobalMapStory` | `inserted` |
| `insert Warum Oberschwaben block before Oberschwaben focus section` | `inserted` |
| `insert land-use-context transformation intro` | `inserted` |
| `append B119 CSS` | `inserted` |

## Review

```powershell
Get-Content docs\B119_fachliche_klammer_audit.txt
Select-String -Encoding UTF8 -Path index.html -Pattern "Warum Wasserstand","berechnet deshalb keine Treibhausgasminderung","Warum Oberschwaben","Prüfpfade","Ã","Evidence explorer"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
