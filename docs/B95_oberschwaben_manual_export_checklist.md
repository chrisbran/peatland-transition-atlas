# B95 - Oberschwaben Manual Export Checklist

Date: 2026-06-23

## Goal

Create:

```text
public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
```

## Required visual content

- [ ] Landkreisrahmen: Ravensburg, Biberach, Sigmaringen, Bodenseekreis
- [ ] Agriculture layer: Ackerland / Grünland / Dauerkultur if available
- [ ] Moor-/Feuchtbodenkontext layer
- [ ] Intersection: Nutzung × Bodenkontext
- [ ] Compact legend
- [ ] Source note or source note documented in JSON

## Recommended title

```text
Oberschwaben: Nutzung × Moor-/Feuchtbodenkontext
```

or:

```text
Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird
```

## Required method wording

Do not put too much text inside the map. But the surrounding module or source metadata must state:

```text
Räumliche Einordnung, keine Eignungs- oder Prioritätskarte.
```

## Export settings

- [ ] PNG
- [ ] 1600 x 900 px
- [ ] same visual style as German presentation page
- [ ] no photo basemap
- [ ] no farm-level labels
- [ ] no parcel-owner/farm data
- [ ] no raw GIS files in `public/maps/oberschwaben/`

## Legend wording

Use:

```text
Landkreisrahmen
Ackerland
Grünland
Dauerkultur
Moor-/Feuchtbodenkontext
Schnittmenge: Nutzung × Bodenkontext
```

Avoid:

```text
Wiedervernässungspotenzial
Priorität
Eignung
betroffene Betriebe
Maßnahmenfläche
```

## After export

Run:

```powershell
python scripts\95_build_oberschwaben_map_assets.py
```

Then inspect:

```powershell
Get-Content docs\B95_oberschwaben_png_asset_qa.md
```
