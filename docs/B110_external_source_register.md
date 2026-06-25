# B110 – Externe Quellen und Projektquellenregister

Stand: 2026-06-25

Dieses Register fasst die bisher im Moore-/Peatland-Transition-Atlas verwendeten, geprüften oder geparkten Quellen zusammen. Es ist eine erste umfassende Dokumentationsfassung; einzelne Literaturangaben und Abrufdaten müssen aus dem Literatur-/Downloadprotokoll noch ergänzt werden.

## Statuslogik

- **aktiv / öffentliche Story**: aktuell Teil der Karten- oder Textargumentation.
- **aktiv, aber Lizenz/Nutzung klären**: technisch genutzt, aber Publikations-/Ableitungsrechte sind offen.
- **geparkt / Fallback**: geprüft oder testweise verarbeitet, aber aktuell nicht Teil der öffentlichen Story.
- **bibliografisch unvollständig**: inhaltlich genutzt, aber DOI/Autor/Jahr müssen nachgetragen werden.

## Interne Projektquelle

| ID | Status | Quelle | Anbieter/Autor:innen | Verwendung | URL / lokaler Bezug | Risiko / offene Aktion |
|---|---|---|---|---|---|---|
| INT-001 | aktiv / Design | DESIGN_CHARTA.md | projektintern / user-provided | Gestaltungsprinzipien: Title carries statement, data ink, one accent color, semantic color, source on every graphic. | lokale Projektdatei | Als interne Designgrundlage markieren. |
| INT-002 | aktiv / Design | brandt_theme.md | projektintern / user-provided | Visueller Stil / Themenrahmen. | lokale Projektdatei | Als interne Quelle führen. |
| INT-003 | aktiv / Format | NOTIZ_Format_Datenessays.md | projektintern / user-provided | Formatmix aus Erzählung, Evidenz, Fotografie; Grenzen der Behauptbarkeit. | lokale Projektdatei | Als interne Quelle führen. |

## Karten/Geodaten

| ID | Status | Quelle | Anbieter/Autor:innen | Verwendung | URL / lokaler Bezug | Risiko / offene Aktion |
|---|---|---|---|---|---|---|
| MAP-001 | aktiv / öffentliche Story | Global Peatland Map 2.0 / Global Peatland Database | Greifswald Mire Centre / Global Peatland Database contributors | Globale Moorverbreitung und globale/Europa-Kontextkarten im Atlas. | https://greifswaldmoor.de/global-peatland-database-en.html | Quellenzeile mit Anbieter, Dataset-Name, Jahr/Version und Link ergänzen. |
| MAP-002 | aktiv / öffentliche Story | FAOSTAT drained organic soils / emissions from drained organic soils | FAO / FAOSTAT | Country hotspot layer: CO₂ + N₂O AR5 CO₂-equivalent emissions, emissions density, rankings. | https://www.fao.org/faostat/en/#data | Exakte FAOSTAT-Domain, Items, Jahre, GWP-Umrechnung und Abrufdatum ergänzen. |
| MAP-003 | aktiv / zentrale Deutschlandkarte | Aktualisierte Kulisse organischer Böden in Deutschland | Thünen-Institut; Wittnebel et al. | Deutschlandkarten: Thünen organic soils extent/types; nationale Einordnung organischer Böden. | https://literatur.thuenen.de/digbib_extern/dn066303.pdf | Exakten Geodaten-Downloadpfad oder Kontakt/Projektquelle nachtragen. |
| MAP-004 | aktiv / Oberschwaben BK50 | dBK50 / GeoLa BK50 – Bodenkarte Baden-Württemberg 1:50.000 | Regierungspräsidium Freiburg – LGRB | BK50 Moor-/Feuchtbodenkontext Oberschwaben; Schnittmenge mit landwirtschaftlicher Nutzung. | https://geoportal.lgrb-bw.de/produkt/dbk50 | Klassifikationsregel für Auswahl Moor-/Feuchtbodenkontext dokumentieren. |
| MAP-005 | aktiv, aber Lizenz/Nutzung klären | FIONA-Flächeninformation 2024 / WFS Flächeninformationen und Online-Antrag BW ab 2023 | MLR/LGL/LW-BW via OWSProxy / GDI-BW | Oberschwaben Landwirtschaftskarte und Schnittmenge Landwirtschaft × BK50; public story nach Rückkehr vor B105. | https://owsproxy.lgl-bw.de/owsproxy/wfs/WFS_LW-BW_FIONA_Flaecheninformation_ab2023?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities | Vor Veröffentlichung schriftlich klären oder Nutzung auf interne Demonstration begrenzen. |
| MAP-006 | aktiv / Verwaltungsgeometrien | GISCO NUTS 2024 | Eurostat / European Commission GISCO | NUTS-/Landkreis-/EU-Kontext, Oberschwaben-Landkreise, administrative Rahmen. | https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units/territorial-units-statistics | Exakte Datei/Scale/Format und Abrufdatum aus Workflow rekonstruieren. |

## Karten/Geodaten / Downloadlinks

| ID | Status | Quelle | Anbieter/Autor:innen | Verwendung | URL / lokaler Bezug | Risiko / offene Aktion |
|---|---|---|---|---|---|---|
| MAP-004a | aktiv / BK50 Rohdaten | dBK50 Biberach shp/gpkg | Regierungspräsidium Freiburg – LGRB | BK50-Rohdaten für Landkreis Biberach. | https://media.lgrb-bw.de/geoportal/data/dBK50/dBK50_426_BC_shp.zip ; https://media.lgrb-bw.de/geoportal/data/dBK50/dBK50_426_BC_gpkg.zip | Abrufdatum nachtragen. |
| MAP-004b | aktiv / BK50 Rohdaten | dBK50 Bodenseekreis shp/gpkg | Regierungspräsidium Freiburg – LGRB | BK50-Rohdaten für Bodenseekreis. | https://media.lgrb-bw.de/geoportal/data/dBK50/dBK50_435_FN_shp.zip ; https://media.lgrb-bw.de/geoportal/data/dBK50/dBK50_435_FN_gpkg.zip | Abrufdatum nachtragen. |
| MAP-004c | aktiv / BK50 Rohdaten | dBK50 Ravensburg shp/gpkg | Regierungspräsidium Freiburg – LGRB | BK50-Rohdaten für Landkreis Ravensburg. | https://media.lgrb-bw.de/geoportal/data/dBK50/dBK50_436_RV_shp.zip ; https://media.lgrb-bw.de/geoportal/data/dBK50/dBK50_436_RV_gpkg.zip | Abrufdatum nachtragen. |
| MAP-004d | aktiv / BK50 Rohdaten | dBK50 Sigmaringen shp/gpkg | Regierungspräsidium Freiburg – LGRB | BK50-Rohdaten für Landkreis Sigmaringen. | https://media.lgrb-bw.de/geoportal/data/dBK50/dBK50_437_SIG_shp.zip ; https://media.lgrb-bw.de/geoportal/data/dBK50/dBK50_437_SIG_gpkg.zip | Abrufdatum nachtragen. |

## Karten/Geodaten / geprüfte Alternative

| ID | Status | Quelle | Anbieter/Autor:innen | Verwendung | URL / lokaler Bezug | Risiko / offene Aktion |
|---|---|---|---|---|---|---|
| ALT-001 | geparkt nach Test | WFS LGL-BW Landnutzung | Landesamt für Geoinformation und Landentwicklung Baden-Württemberg (LGL) | B106-B108b FIONA-Ersatztest; nicht weiterverfolgt wegen Kartenfragmentierung/Designproblem. | https://owsproxy.lgl-bw.de/owsproxy/wfs/WFS_LGL-BW_Landnutzung?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities | Parken; nicht als aktive Quelle angeben, außer in Methodenhistorie. |
| ALT-002 | Fallback, nicht genutzt | LGL ATKIS Basis-DLM WFS | LGL Baden-Württemberg | Fallback-Quelle in B106, nicht produktiv verwendet. | https://owsproxy.lgl-bw.de/owsproxy/wfs/WFS_LGL-BW_ATKIS_Basis-DLM?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities | Nur als geprüfte Alternative dokumentieren. |
| ALT-003 | Fallback, nicht genutzt | BKG LBM-DE 2021 | Bundesamt für Kartographie und Geodäsie (BKG) | Fallback-Quelle in B106; nicht produktiv genutzt. | https://gdz.bkg.bund.de/index.php/default/digitales-landbedeckungsmodell-deutschland-stand-2021-lbm-de.html | Nur als geprüfte Alternative dokumentieren. |
| ALT-004 | Fallback, nicht genutzt | Copernicus HRL Grassland 2023 | Copernicus Land Monitoring Service | Nur als mögliche Fallback-/Kontextquelle in B106 geprüft. | https://land.copernicus.eu/en/products/high-resolution-layer-grasslands/grassland-2023-raster-10-m-100-m-europe-yearly | Als nicht verwendete Alternative markieren. |
| ALT-005 | Fallback, nicht genutzt | ESA WorldCover 2021 | ESA / Google Earth Engine catalogue | Nur als mögliche Fallback-/Kontextquelle in B106 geprüft. | https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200 | Als nicht verwendete Alternative markieren. |

## Politik/Projektkontext

| ID | Status | Quelle | Anbieter/Autor:innen | Verwendung | URL / lokaler Bezug | Risiko / offene Aktion |
|---|---|---|---|---|---|---|
| REG-001 | aktiv / Kontext | Moorschutzprogramm Baden-Württemberg | Land Baden-Württemberg / LUBW / Umweltministerium | Strategischer Rahmen: Schutz, Renaturierung, Monitoring, Förderung, regionale Planung. | https://pd.lubw.de/66926 | Exakte Version/Jahr des PDFs in Quellenblock angeben. |
| REG-002 | aktiv / Kontext | MLR Baden-Württemberg: Moore / Landwirtschaft im Klimawandel | Ministerium für Ernährung, Ländlichen Raum und Verbraucherschutz Baden-Württemberg | Kontextzahlen zu Moorflächen und landwirtschaftlicher Nutzung in BW; politischer Rahmen. | https://mlr.baden-wuerttemberg.de/de/unsere-themen/landwirtschaft/landwirtschaft-im-klimawandel/moore | Bei Nutzung von Zahlen im öffentlichen Text explizit zitieren. |

## Projektinformationen

| ID | Status | Quelle | Anbieter/Autor:innen | Verwendung | URL / lokaler Bezug | Risiko / offene Aktion |
|---|---|---|---|---|---|---|
| REG-003 | aktiv / Kontext | SOLAMO-BW Forschungsprojekt-Flyer | Universität Hohenheim / Projektpartner SOLAMO-BW | Regionale Projektlogik: Oberschwaben, Betroffenheit, Nutzungskonzepte, Interviews, Workshops, Wertschöpfungsketten. | lokal bereitgestellt: Flyer-SOLAMO-BW.pdf | Klärung, ob Flyer/Fakten öffentlich zitiert werden dürfen. |
| REG-004 | intern / Synthese | Moore_Primer.pdf | projektinterne Synthese im Chat/Arbeitsstand | Narrative Brücke: Wasserstand, Paludikulturtypen, Wertschöpfung, Moor-PV, Realismus-Formel. | lokal bereitgestellt: Moore_Primer.pdf | Nicht als Primärquelle zitieren; nur als interne Notiz führen. |

## Publikation/Faktenkontext

| ID | Status | Quelle | Anbieter/Autor:innen | Verwendung | URL / lokaler Bezug | Risiko / offene Aktion |
|---|---|---|---|---|---|---|
| PUB-003 | aktiv / Faktenkontext | UBA / deutsche Moorbodenemissionen | Umweltbundesamt | Primer: Emissionen aus Moorböden in Deutschland, Größenordnung ca. 50,8 Mio. t CO₂-Äq / ca. 7,5 % der Gesamtemissionen. | noch zu verifizieren | Exakten UBA-Link/Publikation nachtragen. |
| PUB-004 | aktiv / BW-Faktenkontext | Treibhausgasemissionen aus organischen Böden in Baden-Württemberg | HfWU / terra fusca / LUBW (laut Primer) | BW-Kontext zu THG-Kataster/organischen Böden, Modellierung und Szenarien. | noch zu verifizieren | Downloadlink/DOI/Jahr ergänzen. |

## Publikation/Literatur-Screening

| ID | Status | Quelle | Anbieter/Autor:innen | Verwendung | URL / lokaler Bezug | Risiko / offene Aktion |
|---|---|---|---|---|---|---|
| LIT-001 | genutzt / Literaturgrundlage, bibliografisch unvollständig | Internationale Synthesen zu Landwirtschaft auf nassen/entwässerten Mooren | mehrere Autorenteams | Einleitung, Problemrahmen, globale Relevanz, Nutzungspfade. | DOIs/Links aus Literatur-Screening nachtragen | Aus Literaturdatenbank/OpenAlex-Export DOI, Autor, Jahr, Journal ergänzen. |
| LIT-002 | genutzt / Literaturgrundlage, bibliografisch unvollständig | Hydrologie / Wasserstand / Tragfähigkeit / Drainage | mehrere Autorenteams | Diskussion zu Wasserstand, Drainage, Verkehrbarkeit, load-bearing, shallow drainage, adjustable drainage. | DOIs/Links aus Literatur-Screening nachtragen | Bibliografische Normalisierung erforderlich. |
| LIT-003 | genutzt / Literaturgrundlage, bibliografisch unvollständig | Paludikultur / Biomasse / Produkt- und Wertschöpfungspfade | mehrere Autorenteams | Wertschöpfungsmatrix: Nassgrünland, Nassweide, Schilf/Rohrkolben/Seggen, Sphagnum, Moor-PV. | DOIs/Links aus Literatur-Screening nachtragen | DOI/Autor/Jahr für reed utilisation, reed canary grass LCA, Common Reed for Thatching, Sphagnum, Moor-PV ergänzen. |
| LIT-004 | genutzt / Literaturgrundlage, bibliografisch unvollständig | Adoption / Governance / Farmer motivations and barriers | mehrere Autorenteams | Pfad 4 Kooperation; Akzeptanz, Förderinstrumente, Koordination, Governance-Risiken. | DOIs/Links aus Literatur-Screening nachtragen | Bibliografische Normalisierung erforderlich. |

## Publikation/Methodenrahmen

| ID | Status | Quelle | Anbieter/Autor:innen | Verwendung | URL / lokaler Bezug | Risiko / offene Aktion |
|---|---|---|---|---|---|---|
| PUB-001 | aktiv / Methoden-/Faktenkontext | IPCC 2013 Wetlands Supplement | IPCC | Methodischer Hintergrund zu Drainage/Rewetting, Emissionsberichterstattung und Moor-/Wetland-Kategorien. | https://www.ipcc-nggip.iges.or.jp/public/wetlands/ | Kapitel/Abschnitt nachtragen, falls im finalen Text konkrete Methodenbehauptungen stehen. |
| PUB-002 | aktiv / Methoden-/Faktenkontext | FAOSTAT / FAO drained organic soils methods and data notes | FAO / Conchedda et al. / Tubiello et al. | Emissions-/Hotspot-Interpretation zu drained organic soils. | https://www.fao.org/statistics/highlights-archive/highlights-detail/drained-organic-soils-%281990-2019%29/en | Genaue FAOSTAT-Domain und Datum der Abfrage dokumentieren. |

## Recherche-/Metadaten-Tool

| ID | Status | Quelle | Anbieter/Autor:innen | Verwendung | URL / lokaler Bezug | Risiko / offene Aktion |
|---|---|---|---|---|---|---|
| TOOL-001 | genutzt | OpenAlex | OpenAlex | Literatur-Screening und Sammlung potenzieller Publikationen. | https://openalex.org/ | Exportdateien/Query-Parameter nachtragen, falls vorhanden. |

## Noch zu ergänzen / offene Punkte

1. **FIONA**: schriftliche Klärung der Publikations-/Ableitungsrechte oder klare Kennzeichnung als interne Demonstrations-/Arbeitsquelle.
2. **BK50**: konkrete Klassifikationsregel dokumentieren, welche BK50-Einheiten als Moor-/Feuchtbodenkontext ausgewählt wurden.
3. **FAOSTAT**: exakte Domains, Items, Jahr, GWP-Umrechnung, Abfragedatum und Skript/Downloadpfad nachtragen.
4. **Thünen-Kulisse**: exakten Geodaten-Downloadpfad/Version ergänzen, nicht nur Publikations-PDF.
5. **Literatur**: DOI/Autor/Jahr/Journal aus OpenAlex-/Literatur-Screening-Export ergänzen.
6. **Country/admin boundaries**: für globale Karten prüfen, ob Natural Earth, GISCO, ArcGIS Basemap oder andere Admin-Layer verwendet wurden.
7. **Projektinterne PDFs**: SOLAMO-BW-Flyer und Moore_Primer als interne/Projektquellen markieren; nicht als Primärliteratur behandeln.

## Empfohlene Quellenzeile für die aktuelle FIONA-basierte Oberschwaben-Version

> Daten: Global Peatland Map 2.0; Thünen-Kulisse organischer Böden; Regierungspräsidium Freiburg – LGRB, dBK50 / GeoLa BK50; FIONA-Flächeninformation 2024; GISCO NUTS 2024; LUBW/Moorschutzprogramm Baden-Württemberg; SOLAMO-BW-Projektinformationen. Eigene Auswahl, Klassifikation, Verschneidung und kartografische Aufbereitung. Hinweis: FIONA-basierte Ableitungen stehen unter Vorbehalt der abschließenden Nutzungs-/Publikationsklärung.
