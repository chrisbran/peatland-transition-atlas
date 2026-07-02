from pathlib import Path
from datetime import date

ROOT = Path(".")
SCRIPT = ROOT / "scripts" / "148_felt_integration_strategy_and_responsive_gate.py"
DOC = ROOT / "docs" / "B148_felt_integration_strategy_and_responsive_gate.md"
CHECKLIST = ROOT / "docs" / "B148_felt_responsive_gate_checklist.md"
FALLBACK = ROOT / "docs" / "B148_mobile_fallback_options.md"
AUDIT = ROOT / "docs" / "B148_felt_integration_strategy_and_responsive_gate_audit.txt"
DONE = ROOT / "tasks" / "done.md"

B146 = ROOT / "docs" / "B146_felt_pilot_qa_record.md"
B147 = ROOT / "docs" / "B147_felt_embed_isolated_prototype.md"
B147_AUDIT = ROOT / "docs" / "B147_felt_embed_isolated_prototype_audit.txt"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done(done_text: str) -> str:
    line = f"- B148 Felt integration strategy and responsive gate: documented desktop-embed/mobile-fallback strategy before any live integration ({date.today().isoformat()})."
    if "B148 Felt integration strategy and responsive gate" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def build_doc(today: str) -> str:
    return f"""# B148 - Felt Integration Strategy and Responsive Gate

Date: {today}

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
@media (max-width: 760px) {{
  /* Mobile-Fallback statt iframe */
}}
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
"""


def build_checklist(today: str) -> str:
    return f"""# B148 - Felt Responsive Gate Checklist

Date: {today}

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
"""


def build_fallback(today: str) -> str:
    return f"""# B148 - Mobile Fallback Options for Felt Map

Date: {today}

## Problem

Der Felt-Embed funktioniert mobil technisch, aber die Felt-eigene UI nimmt auf 390 px viel Raum ein.
Legende, Popup und Kontextmenue koennen die Karte ueberlagern.

## Ziel

Mobile soll die Story nicht bremsen.
Die interaktive Karte darf optional sein, aber die Kernaussage muss ohne Interaktion sichtbar bleiben.

## Variante A - Statisches Preview plus Button

Empfohlen.

Inhalt:

```text
Schnittmenge aus landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext.
Die interaktive Karte öffnet in einem neuen Tab.
```

Button:

```text
Interaktive Karte öffnen
```

Vorteile:

- ruhig
- schnell
- barriereärmer
- keine iframe-UI-Probleme
- kontrollierbarer Scrollfluss

Nachteile:

- kein direktes Mobile-Embed

## Variante B - bestehende PNG-Karte mobil behalten

Inhalt:

- bisherige statische Karte bleibt auf Mobile
- Felt wird nur Desktop/Tablet gezeigt
- externer Felt-Link optional darunter

Vorteile:

- kein neuer Screenshot noetig
- sehr reversibel
- geringstes Risiko

Nachteile:

- Mobile bekommt nicht den vollen Qualitaetssprung

## Variante C - iframe mobil einklappbar

Inhalt:

- Button "Interaktive Karte anzeigen"
- iframe erst nach Klick

Vorteile:

- Mobile kann interaktiv bleiben
- initialer Scrollfluss ruhiger

Nachteile:

- mehr JS/State
- externe UI bleibt klein
- hoeherer Testaufwand

## Empfehlung fuer B149

Mit Variante B oder A starten:

```text
Desktop/Tablet: Felt iframe
Mobile: statischer Fallback + externer Felt-Link
```

Falls spaeter ein hochwertiger statischer Kartenexport aus Felt moeglich ist, wird Variante A bevorzugt.
Bis dahin ist Variante B der pragmatischste Weg.
"""


def main() -> None:
    today = date.today().isoformat()

    b146_exists = B146.exists()
    b147_exists = B147.exists()
    b147_audit_exists = B147_AUDIT.exists()

    write(DOC, build_doc(today))
    write(CHECKLIST, build_checklist(today))
    write(FALLBACK, build_fallback(today))

    audit_text = f"""# B148 Felt integration strategy and responsive gate audit

Date: {today}

Result: DOCUMENTATION ONLY. No public page files changed.

Input docs detected:

- docs/B146_felt_pilot_qa_record.md: {b146_exists}
- docs/B147_felt_embed_isolated_prototype.md: {b147_exists}
- docs/B147_felt_embed_isolated_prototype_audit.txt: {b147_audit_exists}

Created/updated:

- docs/B148_felt_integration_strategy_and_responsive_gate.md
- docs/B148_felt_responsive_gate_checklist.md
- docs/B148_mobile_fallback_options.md
- docs/B148_felt_integration_strategy_and_responsive_gate_audit.txt
- tasks/done.md

Decision documented:

- Desktop/tablet: Felt embed candidate.
- Mobile: fallback or preview + external link.
- No live integration yet.

No iframe was added to index.html.
No CSS was changed.
No local GeoJSON/Shapefile/GPKG files were staged or referenced for commit.
"""
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B148 Felt integration strategy and responsive gate complete.")
    print("Documentation only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B148_felt_integration_strategy_and_responsive_gate.md")
    print("  docs/B148_felt_responsive_gate_checklist.md")
    print("  docs/B148_mobile_fallback_options.md")
    print("  docs/B148_felt_integration_strategy_and_responsive_gate_audit.txt")
    print("  tasks/done.md")


if __name__ == "__main__":
    main()
