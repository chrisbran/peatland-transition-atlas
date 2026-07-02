# B177b - Remove Residual Felt Tokens

Date: 2026-07-02

## Ziel

B176 entfernte die öffentliche Felt/OpenStreetMap-Einbindung. B177 zeigte danach bereits:

```text
Active loaded external resources: 0
iframe in index: False
External map/tile resource references: 0
```

Der Audit fiel aber noch durch, weil ein alter Felt-Quellenblock beziehungsweise alte CSS-Marker als Texttoken im Quellcode verblieben.

B177b entfernt diese Reste.

## Änderungen

- alte HTML-Felt-Markerblöcke entfernt
- alter B150-Felt-Source-Register-Block entfernt, falls vorhanden
- alte B149/B150-Felt-CSS-Blöcke entfernt
- keine regionale Karte geändert
- kein B169/B170/B176-Inhalt geändert

## Token-Counts

| Datei | Token | Vorher | Nachher |
|---|---|---:|---:|
| `index.html` | felt | 1 | 0 |
| `index.html` | openstreetmap/osm | 0 | 0 |
| `index.html` | iframe | 0 | 0 |
| `src/styles.css` | felt | 49 | 5 |
| `src/styles.css` | openstreetmap/osm | 0 | 0 |
| `src/styles.css` | iframe | 0 | 0 |

## Akzeptanz

- `index.html` enthält kein Felt-Token mehr
- `index.html` enthält kein OpenStreetMap/OSM-Token mehr
- `index.html` enthält kein iframe mehr
- alte Felt-CSS-Regeln sind entfernt
- B177 External Request Audit kann erneut laufen
