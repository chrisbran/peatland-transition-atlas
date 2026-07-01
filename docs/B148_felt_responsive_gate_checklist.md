# B148 - Felt Responsive Gate Checklist

Date: 2026-07-01

## Zweck

Diese Checkliste ist das Gate, bevor der Felt-Embed in die Hauptseite integriert wird.

## 1. Desktop Gate

- [ ] Embed laedt in lokalem Prototyp.
- [ ] Embed laedt im echten Seitenkontext.
- [ ] Karte zeigt Oberschwaben korrekt.
- [ ] Annotation sichtbar.
- [ ] Legende stoert nicht.
- [ ] Popup funktioniert.
- [ ] Karte wirkt sichtbar besser als PNG/GIS-Export.
- [ ] Ladezeit akzeptabel.

## 2. Tablet Gate

- [ ] Embed bleibt oberhalb ca. 760 px brauchbar.
- [ ] Legende verdeckt die Hauptaussage nicht.
- [ ] Karte kann gezoomt/panned werden.
- [ ] Annotation bleibt lesbar.

## 3. Mobile Gate

Mobile soll nicht zwingend den iframe zeigen.

- [ ] Unter 760 px wird ein Fallback angezeigt.
- [ ] Fallback erklaert die Karte knapp.
- [ ] Button "Interaktive Karte öffnen" ist sichtbar.
- [ ] Button oeffnet Felt in neuem Tab.
- [ ] Mobile Seite bleibt ruhig und lesbar.
- [ ] Kein horizontales Scrollen.
- [ ] Keine zu hohe iframe-Fläche im Scrollfluss.

## 4. Datenschutz / Lizenz

- [ ] Felt-Plan nach Trial geklaert.
- [ ] Embed-Nutzung im geplanten Kontext erlaubt.
- [ ] Externer Drittanbieter-Hinweis geklaert.
- [ ] Keine privaten oder nicht freigegebenen Daten im Felt-Projekt.
- [ ] Share-Link ist bewusst oeffentlich.

## 5. Fallback / Wiederherstellung

- [ ] Bestehende PNG-Karte bleibt verfuegbar.
- [ ] Integrationspatch ist reversibel.
- [ ] Kein Loeschen bestehender Kartenassets.
- [ ] Keine raw GIS-Dateien im Repo.
- [ ] Nur explizite Dateien stagen, kein `git add .`.

## Gate-Entscheidung

```text
[ ] Desktop-Embed + Mobile-Fallback in B149 testen
[ ] nur externer Link, kein Embed
[ ] statischen hochwertigen Export bevorzugen
[ ] Felt-Pilot verwerfen
```
