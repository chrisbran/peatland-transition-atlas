# B146 - Felt Pilot QA Record

Date: 2026-07-01

## QA-Status

| Punkt | Status | Notiz |
|---|---|---|
| Landkreis-Upload | bestanden | GeoJSON ca. 54 KB |
| Schnittmengen-Upload | bestanden | vereinfachtes GeoJSON ca. 3.37 MB |
| Projektion | bestanden | Felt zeigt Oberschwaben korrekt |
| Popup | bestanden | zeigt `klasse` und `flaeche_ha` |
| Annotation | bestanden | `Schnittmenge = Prüfbedarf, nicht Eignung` |
| Layernamen | bestanden | technische Namen reduziert |
| Mobile View | bestanden | laut manuellem Test brauchbar |
| Embed-Code | bestanden | verfügbar |
| Privates Fenster | offen | vor B147 testen/dokumentieren |
| Datenschutz/Lizenz | offen | vor Live-Einbau prüfen |
| Fallback | offen | PNG-/WebP-Fallback muss erhalten bleiben |

## Visuelle Bewertung

Der Felt-Pilot hebt die Oberschwaben-Karte sichtbar ueber den bisherigen GIS-/PNG-Look:

- scharfe Vektordarstellung
- dunkle Basemap passt zur Atlas-Aesthetik
- Schnittmenge ist direkt erkennbar
- Landkreisgrenzen geben Orientierung
- Popup ist aufgeraeumt
- Annotation erklaert die Karte im Kartenbild selbst

## Risiken

- externe Abhaengigkeit von Felt
- moegliche Plan-/Lizenzbindung nach Ablauf der Trial
- Datenschutz-/Drittanbieterfrage
- iframe-Verhalten im bestehenden Sticky-Layout noch ungeprueft
- mobile Embed-Hoehe und Legende koennen im Live-Layout anders wirken

## Gate fuer B147

B147 darf erst `index.html` beruehren, wenn mindestens ein isolierter iframe-Test bestaetigt:

- Embed laedt lokal
- Embed funktioniert in Firefox/Chrome
- Embed ist auf 390 px Breite brauchbar
- Fallback bleibt definierbar
