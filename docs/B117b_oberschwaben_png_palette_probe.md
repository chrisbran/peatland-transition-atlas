# B117b – Oberschwaben PNG Palette Probe

Stand: 2026-06-26

Status: **OK**

## Zweck

B117b prüft die aktuellen Oberschwaben-PNGs, bevor Farben oder Legenden verändert werden. Die Analyse ändert keine Karten und keine Website-Dateien.

## Geprüfte PNG-Dateien

| Datei | Breite | Höhe | Farbtyp | Opaque Pixel | Exakte RGB-Farben | Sättigungs-Kandidaten |
|---|---:|---:|---:|---:|---:|---:|
| `oberschwaben_admin_context.png` | 1600 | 900 | 6 | 16164 | 177 | 0 |
| `oberschwaben_agriculture.png` | 1600 | 900 | 6 | 336309 | 45 | 26 |
| `oberschwaben_moor_context.png` | 1600 | 900 | 6 | 53711 | 4 | 2 |
| `oberschwaben_agriculture_moor_intersection.png` | 1600 | 900 | 6 | 33680 | 4 | 2 |

## Zielpalette aus B117

| Klasse | Ziel-Hex |
|---|---|
| Ackerland | `#C76E3F` |
| Grünland | `#5F8F4A` |
| Dauerkultur / Sondernutzung | `#8C5A9E` |
| Moor-/Feuchtbodenkontext | `#4E7FA6` |
| Schnittmenge | `#043B36` |

## Interpretation

Die PNGs enthalten durch Antialiasing, Labels, Hintergrund und Transparenz viele Farbwerte. Deshalb erzeugt B117b drei Gruppen:

- `exact_top`: häufigste exakte RGB-Werte;
- `quantized_top`: auf 16er-Schritte gerundete dominante Farbbins;
- `saturated_candidate_quantized`: stärker gesättigte Farbbins als Kandidaten für thematische Klassen.

Für die Oberschwaben-Legende sind vor allem die `saturated_candidate_quantized`-Zeilen relevant.

## Ergebnisdateien

- `docs/B117b_oberschwaben_png_color_summary.csv`
- `docs/B117b_oberschwaben_png_top_colors.csv`
- `docs/B117b_oberschwaben_html_css_color_scan.csv`
- `docs/B117b_oberschwaben_png_palette_audit.txt`

## Empfehlung

Nächster Schritt ist kein blindes HTML-Recoloring. Entscheide anhand der Palette-Probe, ob die Oberschwaben-Karten neu exportiert werden müssen. Wenn ja: Karte und Legende gemeinsam aktualisieren.
