# B166 - Sticky Zoom Repair Recommendations

Date: 2026-07-01

## Reparaturziel

Der B165/B165b-Prototyp soll nicht verworfen werden. Er braucht eine saubere State-Matrix.

## Reparaturliste für B167

### A. Globale Druckkarten trennen

Aktuell:

```text
global-pressure -> global_hotspots_total.png
```

Neu:

```text
global-pressure-total   -> global_hotspots_total.png
global-pressure-density -> global_hotspots_density.png
```

Textvorschläge:

```text
02 / Gesamt
Wo ist der gesamte Emissionsdruck hoch?

03 / Intensität
Wo ist der Druck pro Fläche besonders hoch?
```

### B. Regionale Übergabe reparieren

Aktuell problematisch:

```text
regional-handoff base    = regional/Oberschwaben-or-BW asset
regional-handoff overlay = germany_admin_context.png
```

Neu:

```text
oberschwaben-handoff base    = regional/BW/Oberschwaben asset
oberschwaben-handoff overlay = matching regional boundary OR none
```

Falls kein regionales Boundary-Overlay existiert:

```text
Do not overlay germany_admin_context.
Use base image only and mark regional boundary export as open gate.
```

### C. Boundary-Pairing-Regel

| Basis-Scope | Erlaubtes Overlay |
|---|---|
| global | global_country_borders |
| europe | europe_country_borders |
| germany | germany_admin_context |
| bw | BW boundary / counties / embedded |
| oberschwaben | Oberschwaben counties / embedded |
| regional | matching regional boundary / embedded |

### D. Finale Stepfolge

```text
01 global-peat
02 global-pressure-total
03 global-pressure-density
04 europe-bridge
05 germany-extent
06 germany-types
07 oberschwaben-handoff
```

### E. Integrationsentscheidung

Erst nach B167 visuell prüfen:

- Ist sieben Steps zu lang?
- Sind Total und Density beide nötig?
- Falls ja: bleiben beide.
- Falls nein: Density ist wahrscheinlich redaktionell wichtiger als Total, weil sie den Flächendruck besser zeigt.
