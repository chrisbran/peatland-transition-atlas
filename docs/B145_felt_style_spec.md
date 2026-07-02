# B145 - Felt Style Specification

Date: 2026-06-30

## Designprinzip

Die Karte soll nicht wie ein GIS-Arbeitsstand wirken, sondern wie eine redaktionelle Karte.

Leitregel:

> Eine dominante Aussage, gedämpfter Kontext.

## Klassen und visuelle Rollen

| Klasse | Rolle | Füllung | Deckkraft | Kontur | Kommentar |
|---|---|---|---:|---|---|
| Schnittmenge | Hauptsignal | kräftiges Petrol / Dunkeltürkis | 85-95 % | dunkler Petrolton | einzige satte Farbe |
| Moor-/Feuchtbodenkontext | Bodenkontext | Blaugrau | 35-50 % | sehr schwach | Kontext, nicht Hauptsignal |
| Grünland | Nutzungskontext | gedämpftes Salbeigrün | 35-45 % | keine oder sehr schwach | nicht mit Schnittmenge konkurrieren |
| Ackerland | Nutzungskontext | warmes Ocker/Sand | 35-45 % | keine oder sehr schwach | ruhig halten |
| Dauerkultur | Nutzungskontext | gedämpftes Violett/Aubergine | 35-45 % | keine oder sehr schwach | kleinräumig interpretieren |

## Beispielpalette

Startwerte, in Felt visuell anpassen:

```text
Schnittmenge:            #087f7a
Moor-/Feuchtbodenkontext:#7f9aa3
Grünland:                #a8b97a
Ackerland:               #d6b36a
Dauerkultur:             #8f6b8f
Kontur dunkel:           #23443f
```

## Hintergrund

- möglichst reduzierter Basemap-Stil
- keine dominanten Straßen
- Gewässer und Orte nur, wenn sie Orientierung geben
- Landkreisgrenzen dezent
- Labels nicht flächendeckend, sondern gezielt

## Direkte Kartenlabels

Pflichtlabels:

```text
Schnittmenge = Prüfbedarf, nicht Eignung
Biberach
Ravensburg
Sigmaringen
Bodenseekreis
```

Optionaler Callout:

```text
Landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext überlagern sich hier.
```

## Legende

Legende möglichst kurz halten.

Priorität:

1. Schnittmenge
2. Moor-/Feuchtbodenkontext
3. Nutzungskontext

Wenn Felt eine vollständige Legende erzeugt, trotzdem direkt auf der Karte annotieren.
Die Legende darf nicht die zentrale Erklärung übernehmen.

## Tooltip-Text

Tooltip-Titel:

```text
{klasse}
```

Tooltip-Felder:

```text
Landkreis: {landkreis}
Fläche: {flaeche_ha} ha
```

Bei technischen Feldnamen in Felt manuell umbenennen oder ausblenden.
