# B117c – Oberschwaben Map Palette Restyle

Stand: 2026-06-26

Status: **OK**

## Ziel

B117c synchronisiert die Oberschwaben-Kartenfarben und Legenden-Swatches mit einer klareren, publikationsfähigeren Palette.

## Zielpalette

| Klasse | Hex |
|---|---|
| Ackerland | `#C76E3F` |
| Grünland | `#5F8F4A` |
| Dauerkultur / Sondernutzung | `#8C5A9E` |
| Moor-/Feuchtbodenkontext | `#4E7FA6` |
| Schnittmenge | `#043B36` |

## Geänderte Karten

- `public/maps/oberschwaben/oberschwaben_agriculture.png`
- `public/maps/oberschwaben/oberschwaben_moor_context.png`
- `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png`

Nicht geändert:

- `public/maps/oberschwaben/oberschwaben_admin_context.png`
- `data/*`
- FIONA/BK50/GISCO-Logik
- Flächenwerte

## Recolor counts

| Datei | Klasse | Pixel |
|---|---|---:|
| `public/maps/oberschwaben/oberschwaben_agriculture.png` | transparent_or_near_transparent | 1103691 |
| `public/maps/oberschwaben/oberschwaben_agriculture.png` | acker | 151053 |
| `public/maps/oberschwaben/oberschwaben_agriculture.png` | gruenland | 169398 |
| `public/maps/oberschwaben/oberschwaben_agriculture.png` | dauerkultur | 15858 |
| `public/maps/oberschwaben/oberschwaben_moor_context.png` | transparent_or_near_transparent | 1386289 |
| `public/maps/oberschwaben/oberschwaben_moor_context.png` | moor | 53711 |
| `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png` | transparent_or_near_transparent | 1406320 |
| `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png` | intersection | 33680 |

## CSS

- CSS changed: 1
- Override appended: 1

## Review commands

```powershell
python scripts\117b_oberschwaben_png_palette_probe.py
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```
