# B155 - Publication Gate Register

Date: 2026-07-01

## Ziel

B155 bündelt nach der Felt-Integration die verbleibenden Veröffentlichungsgates.
Der Patch verändert die öffentliche Seite nicht. Er dokumentiert, was vor einer finalen V2-Veröffentlichung fachlich, rechtlich und prozessual noch zu prüfen ist.

## Kurzfazit

Die fachliche Story ist nach B152/B154 deutlich stabiler: Scope, Methodik, Oberschwaben-Rahmung, Felt-Vertiefung und Wertschöpfungsthese sind gesetzt.
Offen sind vor allem Veröffentlichungssicherheit, nicht Story-Substanz.

## Gate-Übersicht

| Gate | Status | Nächste Aktion |
|---|---|---|
| Scope / Nicht-Eignungskarte | inhaltlich gesetzt | Nur noch auf Konsistenz achten; keine neuen decision-tool Formulierungen einführen. |
| Methode / Quellen | weitgehend gesetzt | Final gegen Datenherkunft und Rundungslogik lesen. |
| 19.900-ha-Zahl | sichtbar, methodisch noch final zu bestätigen | Finale Methodennotiz ergänzen: Rundung, Geometrievereinfachung nicht für Flächenbilanz, FIONA/BK50/GISCO-Versionen. |
| Felt / Drittanbieter | technisch und textlich vorbereitet | Felt-Plan/Lizenz nach Trial und Datenschutztext rechtlich/praktisch klären. |
| Mobile / Responsive Felt | gesetzt | Vor Veröffentlichung einmal 390 px und Tablet prüfen; iframe darf mobil nicht dominieren. |
| Hohenheim / SOLAMO-BW Kontext | Hinweis vorhanden, Freigabe offen | Freigabe/Disclaimer intern klären; ggf. präzisere Formulierung mit Projektleitung abstimmen. |
| Impressum / Datenschutz | Text/Linkwörter vorhanden, Zielseiten prüfen | Prüfen, ob echte Zielseiten/Links vorhanden sind und ob Felt dort erwähnt werden muss. |
| Git-/Datenhygiene | laufend | Weiterhin nur explizite Dateien stagen; kein git add .; working/ und raw GIS nicht committen. |

## Priorität vor Veröffentlichung

### Muss vor Live-Freigabe geklärt sein

1. **Impressum/Datenschutz:** echte Zielseiten oder verlässliche Links, inklusive Drittanbieter-/Felt-Hinweis.
2. **Felt-Lizenz/Plan:** Klären, ob Embed nach Trial stabil und zulässig bleibt.
3. **Hohenheim/SOLAMO-BW-Disclaimer:** Formulierung intern freigeben lassen.
4. **19.900-ha-Methodennotiz:** Rundung und Datenstand final absichern.

### Sollte vor finaler Version geprüft werden

1. Mobile 390 px und Tablet mit echtem Felt-Embed testen.
2. Letzter sichtbarer Wording-Pass auf Wiederholungen von `Umsetzung`.
3. Quellenregister gegen finale sichtbare Aussagen lesen.
4. Git-Status vor Commit auf raw GIS/GeoJSON prüfen.

## Aktuelle automatische Indikatoren aus index.html

| Indikator | Erkannt |
|---|---:|
| `scope_box` | True |
| `no_suitability_language` | True |
| `method_short` | True |
| `central_sources` | True |
| `felt_notice` | True |
| `felt_source_register` | True |
| `osm_notice` | True |
| `fiona_bk50_gisco` | True |
| `area_19900` | True |
| `solamo_disclaimer` | True |
| `impressum_privacy_words` | True |
| `b152_felt_framing` | True |

## Entscheidung

Bis zur Klärung der Veröffentlichungsgates bleibt der Felt-Block ein integrierter, aber reversibel gehaltener Kartenbaustein.
Die bestehende statische Oberschwaben-Karte bleibt als Story- und Fallback-Komponente erhalten.

## Dateien

- CSV-Register: `docs/B155_publication_gate_register.csv`
