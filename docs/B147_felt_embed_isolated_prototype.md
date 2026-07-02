# B147 - Felt Embed Isolated Prototype

Date: 2026-07-01

## Ziel

B147 erstellt einen isolierten iframe-Prototyp fuer den Felt-Kartenkandidaten.
Die Hauptseite wird weiterhin nicht veraendert.

## Erzeugte Prototype-Datei

```text
docs/prototypes/oberschwaben_felt_embed_test.html
```

Diese Datei dient nur zum lokalen Testen:

- Desktop
- mobile Breiten
- iframe-Ladeverhalten
- Popup/Interaktion
- Legende/Annotation
- visuelle Hoehe im Browser

## Status

| Punkt | Status |
|---|---|
| iframe aus B146 erkannt | ja |
| Share-URL erkannt | ja |
| public `index.html` geaendert | nein |
| `src/styles.css` geaendert | nein |
| lokale GeoJSON/Shapefiles committed | nein |

## Share-URL

```text
https://felt.com/map/Oberschwaben-Moor-Feuchtbodenkontext-Pilot-VaKZdOYFRw9B2SzH1sdk39AD?share=1&loc=47.9524,9.489,10z
```

## Testanleitung

Lokal Server starten:

```powershell
python -m http.server 8000
```

Dann im Browser:

```text
http://localhost:8000/docs/prototypes/oberschwaben_felt_embed_test.html
```

Responsive Test:

```text
390 px Breite
```

## Entscheidung

B147 ist noch keine Live-Integration.
Wenn der isolierte Prototyp bestanden ist, kann B148 als eigentlicher Integrationsentscheid folgen:

- entweder Felt-Embed in die Oberschwaben-Section integrieren
- oder Felt nur als externer Link anbieten
- oder hochwertigen statischen Export/PNG-Fallback verwenden
