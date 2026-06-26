# B117 – Oberschwaben Legend Colour Specification

Stand: 2026-06-26

## Zweck

Die aktuelle Oberschwaben-Legende ist fachlich richtig, aber die Klassen sind visuell zu ähnlich. B117 definiert deshalb eine klarere Zielpalette für den nächsten Kartenexport.

Wichtig: Die Farbänderung sollte **nicht nur in der HTML-Legende** erfolgen. Karte und Legende müssen zusammen angepasst werden, sonst entsteht ein Legenden-Karten-Mismatch.

## Zielpalette

| Klasse | Hex | Rolle | Hinweis |
|---|---|---|---|
| Ackerland | `#C76E3F` | warmer Braun-Orange-Ton für ackerbauliche Nutzung | klar von Grünland und Moor-/Feuchtbodenkontext getrennt |
| Grünland | `#5F8F4A` | mittleres Grün für Grünland | nicht zu hell; muss gegenüber Moor-Blau unterscheidbar bleiben |
| Dauerkultur / Sondernutzung | `#8C5A9E` | gedämpftes Violett für Sonder-/Dauerkultur | bewusst nicht grün/rosa, um kleine Klassen sichtbar zu halten |
| Moor-/Feuchtbodenkontext | `#4E7FA6` | Blau für Wasser-/Feuchtbodenkontext | semantisch mit Wasserstand/Feuchte gekoppelt |
| Schnittmenge | `#043B36` | dunkles Petrol als Kernaussage | höchster Kontrast; sollte in Karte und Legende dominant sein |

## Kartografische Regeln

1. Die Schnittmenge bleibt die visuell stärkste Klasse.
2. Moor-/Feuchtbodenkontext darf nicht mit Grünland verwechselt werden.
3. Ackerland und Dauerkultur müssen auch bei kleinen Flächen unterscheidbar bleiben.
4. Die Legende muss in Graustufen und bei Rot-Grün-Sehschwäche lesbar bleiben.
5. Quellen- und Caveat-Zeile bleiben unterhalb der Flächenbilanz, nicht als technische Karten-Caption.

## Prüfauftrag B117b

- Public PNGs aus der Oberschwaben-Karte mit Zielpalette neu exportieren.
- HTML-Legende und Kartenfarben abgleichen.
- Screenshot bei 1440 px und 1280 px prüfen.
- Danach B58 erneut laufen lassen.
