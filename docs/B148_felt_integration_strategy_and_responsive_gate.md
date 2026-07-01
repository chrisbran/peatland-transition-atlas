# B148 - Felt Integration Strategy and Responsive Gate

Date: 2026-07-01

## Ziel

B148 dokumentiert die Integrationsentscheidung fuer den Felt-Kartenpilot nach dem isolierten
B147-Test. Es wird weiterhin nichts in die oeffentliche Hauptseite eingebaut.

## Ausgangslage

Der Oberschwaben-Felt-Pilot ist technisch und visuell erfolgreich:

- Felt-Upload funktioniert
- vereinfachte Schnittmenge laedt
- Landkreisgrenzen und Labels funktionieren
- Popup zeigt nur sinnvolle Felder
- Direktannotation ist sichtbar
- iframe ist verfuegbar
- isolierter Prototyp laedt lokal

Der lokale B147-Test zeigt aber auch:

- Desktop und Tablet sind geeignet
- Mobile 390 px funktioniert technisch, ist aber nicht ideal als alleinige Kartenloesung
- Legende/Layerbox und Popup/Context-Menue nehmen mobil viel Platz ein
- die Karte bleibt nutzbar, aber nicht so ruhig und kontrolliert wie ein redaktioneller Mobile-Block

## Entscheidung

Felt wird nicht als 1:1-Ersatz fuer alle Viewports integriert.

Stattdessen gilt fuer eine spaetere Live-Integration:

```text
Desktop / Tablet:
Felt-Embed als interaktive Oberschwaben-Karte

Mobile:
statischer Preview- oder Fallback-Block
+ Button "Interaktive Karte öffnen"
```

Die bestehende PNG-/Sticky-Karte bleibt zunaechst als Rueckfalloption erhalten.

## Warum diese Strategie

Der Felt-Embed hebt die Karte auf Desktop sichtbar auf ein hoeheres Niveau.
Auf Mobile ist die externe Kartenoberflaeche aber schwerer kontrollierbar als eigenes HTML/CSS.
Eine responsive Gate-Strategie verhindert, dass ein fachlich starker Desktop-Pilot die mobile
Lesbarkeit der Seite verschlechtert.

## Integrationsprinzip fuer B149/B150

Eine spaetere Integration darf `index.html` erst beruehren, wenn diese Strategie eingehalten wird:

1. Felt-Embed nicht global einsetzen, sondern nur in der Oberschwaben-Section.
2. Embed nur oberhalb eines Breakpoints sichtbar machen.
3. Unterhalb des Breakpoints Mobile-Fallback zeigen.
4. Fallback enthaelt Kurztext, Screenshot/Preview oder bestehende Karte plus externen Link.
5. Bestehende PNG-Karte bleibt als Rueckfall im Code oder als dokumentierte Wiederherstellungsoption verfuegbar.
6. Keine lokalen GeoJSON/Shapefile-Dateien ins Repo committen.
7. Datenschutz-/Drittanbieter-Hinweis vor Live-Publikation klaeren.

## Empfohlener Breakpoint

Startwert:

```css
@media (max-width: 760px) {
  /* Mobile-Fallback statt iframe */
}
```

Begruendung:

- 390 px-Test zeigt technische Nutzbarkeit, aber eingeschraenkte Lesbarkeit
- Tablet/Desktop profitieren vom interaktiven iframe
- 760 px trennt Smartphone und kleine Tablets pragmatisch

Der Breakpoint kann im Integrationstest angepasst werden.

## Mobile-Fallback-Varianten

Priorisiert:

### Variante A - Statisches Preview + externer Link

- kleines statisches Kartenbild oder bestehender Screenshot
- kurzer Text: "Interaktive Karte in neuem Tab öffnen"
- Button zum Felt-Link
- robusteste Mobile-Loesung

### Variante B - bestehende PNG-Karte mobil behalten

- kein neuer Screenshot noetig
- bestehendes Kartenbild bleibt mobil stabil
- Felt nur als Desktop-Upgrade

### Variante C - iframe auch mobil, aber collapsible

- technisch moeglich
- nicht empfohlen als Standard
- nur wenn mobile Nutzbarkeit nach weiterem Test deutlich besser wird

## Empfehlung

B149 sollte ein Integrationskonzept oder Prototyp sein, nicht sofort der finale Ersatz:

```text
B149_felt_desktop_embed_mobile_fallback_prototype
```

Ziel von B149:

- ein isolierter oder deaktivierter Abschnitt testet die echte Einbettung in die Seitenumgebung
- Desktop zeigt iframe
- Mobile zeigt Fallback
- bestehende Karte bleibt wiederherstellbar

## Noch offene Gates

Vor einem Live-Merge in die oeffentliche Seite:

- [ ] Share-Link im privaten Fenster ohne Login getestet
- [ ] iframe im echten Seitenkontext getestet
- [ ] 390 px Mobile-Fallback getestet
- [ ] Datenschutz-/Drittanbieter-Hinweis geklaert
- [ ] Felt-Plan/Lizenz nach Trial geklaert
- [ ] Fallback zur bestehenden PNG-Karte dokumentiert
- [ ] QA B103b und B58 bestehen

## Nicht-Ziele von B148

B148 macht nicht:

- keine Aenderung an `index.html`
- keine Aenderung an `src/styles.css`
- kein iframe in der Live-Seite
- keine public GeoJSON-Dateien
- kein MapLibre-Code
- kein Datawrapper-Embed
