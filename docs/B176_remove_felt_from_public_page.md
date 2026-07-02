# B176 - Remove Felt From Public Page

Date: 2026-07-02

## Ziel

B176 entfernt die externe Felt/OpenStreetMap-Einbindung aus der öffentlichen Seite.

Die regionale statische Oberschwaben-Karte bleibt unverändert. Entfernt wird nur der externe Kartenviewer-Pfad.

## Entscheidung

```text
Felt raus.
Regionale statische Karte bleibt.
Interaktivität wird nicht grundsätzlich verworfen, sondern nur die Drittanbieter-Abhängigkeit aus der öffentlichen V2 entfernt.
```

## Öffentlicher Ersatztext

```text
Kartografische Vertiefung

Die Detailkarte bleibt bewusst eine lokale, redaktionelle Grafik: Sie zeigt
die Schnittmenge aus heutiger Nutzung und Moor-/Feuchtbodenkontext, ohne beim
Seitenaufruf einen externen Kartendienst zu laden.
```

## Änderungen

- Felt-iframe entfernt
- Felt-Link entfernt, falls vorhanden
- Abschnitt `Interaktive Vertiefung` durch lokale `Kartografische Vertiefung` ersetzt
- Quellen-/Methodenverweis zu Felt/OpenStreetMap durch lokale Kartengrafik ersetzt
- CSS für den lokalen Ersatzabschnitt ergänzt

## Nicht geändert

- regionale statische Oberschwaben-Karte
- B169 Sticky-Zoom
- Flächenbilanz
- Wertschöpfungs-Scorecard
- Datenquellen
- raw GIS/Data

## Provider-Check

| Signal in `index.html` | Vorher | Nachher |
|---|---:|---:|
| `felt` | 30 | 5 |
| `openstreetmap` | 3 | 0 |
| `<iframe` | 1 | 0 |
| `felt.com` | 2 | 0 |

## Akzeptanz

- kein Felt-iframe mehr in `index.html`
- kein Felt-Link mehr in `index.html`
- keine OpenStreetMap-/Felt-Erwähnung als aktiver öffentlicher Dienst
- regionale statische Karte bleibt bestehen
- B103b PASS
- B58 PASS
