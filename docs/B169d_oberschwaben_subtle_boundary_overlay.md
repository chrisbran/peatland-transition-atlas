# B169d - Oberschwaben Subtle Boundary Overlay

Date: 2026-07-01

## Ziel

B169c entfernte das Oberschwaben-Admin-Overlay, weil Landkreisnamen im Sticky-Zoom wie Artefakte wirkten.
Ganz ohne Grenzen fehlt aber räumliche Orientierung.

B169d stellt deshalb eine **subtile regionale Orientierungsebene** wieder her.

## Vorgehen

Der Patch sucht zuerst nach möglichst label-freien Oberschwaben-Grenzassets, zum Beispiel:

```text
oberschwaben_boundary_outline.png
oberschwaben_landkreis_boundaries.png
oberschwaben_admin_context_no_labels.png
```

Falls kein label-freies Asset vorhanden ist, nutzt er als Fallback:

```text
public/maps/oberschwaben/oberschwaben_admin_context.png
```

aber stark abgeschwächt.

## Gewähltes Overlay

```text
public/maps/oberschwaben/oberschwaben_admin_context.png
```

Modus:

```text
fallback_admin_context_softened
```

## CSS-Logik

Für Oberschwaben wird das Overlay separat markiert:

```html
data-b169-oberschwaben-boundary="true"
```

Bei Fallback auf `admin_context` zusätzlich:

```html
data-b169-soft-boundary="true"
```

Dadurch können Grenzen sichtbar bleiben, während Label-Artefakte möglichst wenig dominieren.

## Nicht geändert

- keine neue Statefolge
- keine neue Karte erzeugt
- keine Änderung an Felt
- keine Änderung an Oberschwaben-Detailkarte
- keine Änderung an Scorecard

## Bessere langfristige Lösung

Für den finalen Live-Zoom wäre ein echtes label-freies Boundary-Asset besser:

```text
public/maps/oberschwaben/oberschwaben_landkreis_boundaries.png
```

oder:

```text
public/maps/oberschwaben/oberschwaben_boundary_outline.png
```

Das sollte später aus ArcGIS/mapshaper exportiert werden, falls die abgeschwächte Admin-Kontext-Ebene noch zu unruhig wirkt.
