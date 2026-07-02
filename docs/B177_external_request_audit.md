# B177 - External Request / Third-Party Audit

Date: 2026-07-02

## Ziel

B177 prüft nach B176, ob die öffentliche Seite beim Seitenaufruf noch externe Kartenviewer, iframes, Tile-Dienste, CDNs oder andere Drittanbieter-Ressourcen lädt.

Passive Quellenlinks im Text sind nicht dasselbe wie aktive Drittanbieter-Ressourcen. Externe `a href`-Links werden inventarisiert, aber nicht als Seitenaufruf-Request gewertet.

## Ergebnis

```text
PASS
```

## Zentrale Checks

| Check | Ergebnis |
|---|---|
| B176 lokale Kartografie-Fassade vorhanden | `True` |
| `<iframe>` in `index.html` | `False` |
| Felt in `index.html` | `False` |
| OpenStreetMap/OSM in `index.html` | `False` |
| Aktive externe Page-Load-Ressourcen | `0` |
| Externe Map-/Tile-Ressourcen | `0` |

## Aktive externe Ressourcen

| Domain | Anzahl |
|---|---:|
| `www.w3.org` | 2 |

Details: `docs/B177_loaded_external_resources.csv`

## Passive externe Links

| Domain | Anzahl |
|---|---:|
| `430a.uni-hohenheim.de` | 1 |
| `atlas.thuenen.de` | 1 |
| `ec.europa.eu` | 1 |
| `fiona.landbw.de` | 1 |
| `lazbw.landwirtschaft-bw.de` | 1 |
| `ltz.landwirtschaft-bw.de` | 1 |
| `mlr.baden-wuerttemberg.de` | 2 |
| `www.bundesumweltministerium.de` | 1 |
| `www.fao.org` | 1 |
| `www.greifswaldmoor.de` | 1 |
| `www.ipcc-nggip.iges.or.jp` | 1 |
| `www.lgrb-bw.de` | 1 |
| `www.lubw.baden-wuerttemberg.de` | 1 |
| `www.moorwissen.de` | 1 |
| `www.umweltbundesamt.de` | 1 |

Details: `docs/B177_external_links_inventory.csv`

## Provider-Token-Scan

Details: `docs/B177_provider_token_scan.csv`

## Interpretation

- `PASS` bedeutet: Im statischen Quellcode sind keine aktiven externen Karten-/Tile-/iframe-Requests mehr erkennbar.
- Passive externe Quellenlinks bleiben als Quellenverweise erhalten.
- Dieser Audit ersetzt keine juristische Prüfung und keine Browser-Network-Analyse, reduziert aber die technische Drittanbieter-Angriffsfläche erheblich.

## Manuelle Browserprüfung

Im Browser DevTools öffnen:

```text
Network → Disable cache → Seite hart neu laden
```

Dann prüfen:

```text
felt
openstreetmap
tile
mapbox
maptiler
fonts.googleapis
fonts.gstatic
```

Erwartung: keine Treffer.
