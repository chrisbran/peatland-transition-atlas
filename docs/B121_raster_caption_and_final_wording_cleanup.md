# B121 – Raster Caption and Final Wording Cleanup

Stand: 2026-06-26

Status: **REVIEW REQUIRED**

## Zweck

B121 bereinigt letzte HTML-Wording-Reste und erzeugt eine visuelle Prüfliste für Texte, die direkt in PNG-Karten eingebrannt sein können.

## Ergebnis

- HTML replacements applied: 2
- Map images listed for raster review: 15
- High-priority raster checks: 14
- Visible-text risk findings: 0
- Missing required findings: 1

## Applied replacements

| Pattern | Count |
|---|---:|
| `Arbeitsstand auf Basis kuratierter Literaturcodierung` | 1 |
| `Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen.` | 1 |

## Raster-caption review

Open `docs/B121_raster_caption_review.html` locally and inspect all HIGH/MEDIUM map images visually.

Terms that must not remain in raster images:

- `GLOBAL_FRAME_V1`
- `exported from`
- `ArcGIS`
- `same ArcGIS frame`
- `Peatland context`
- `Peat in soil mosaic`
- `Thuenen`
- `rendered as`
- `one-colour extent layer`
- `TOTAL EMISSIONS`
- `emissions_total_kt_co2e`

## Review commands

```powershell
Get-Content docs\B121_final_wording_audit.txt -Encoding UTF8
Start-Process docs\B121_raster_caption_review.html
Select-String -Encoding UTF8 -Path index.html -Pattern "GLOBAL_FRAME_V1","exported from","Peatland context","Nutzung / Produkt","Arbeitsstand","Methodischer Hinweis","Ã","�"
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```
