# B149 - Felt Desktop Embed / Mobile Fallback Prototype

Date: 2026-07-01

## Ziel

B149 setzt die in B148 dokumentierte Responsive-Strategie als kontrollierten Seiten-Prototyp um.

- Desktop/Tablet: Felt iframe wird angezeigt.
- Mobile unter 760 px: kein iframe, sondern kurzer Fallback-Block mit externem Felt-Link.
- Bestehende Kartenlogik und bestehende Assets bleiben erhalten.
- Keine lokalen GeoJSON/Shapefile-Daten werden ins Repo aufgenommen.

## Umsetzung

Der neue Abschnitt wird nach dem Oberschwaben-Kartenabschnitt eingefügt.

Titel:

```text
Die Schnittmenge wird als interaktive Karte lesbar
```

Mobile-Fallback:

```text
Interaktive Karte öffnen
```

## Technische Entscheidung

Der Felt-iframe wird aus `docs/B146_felt_embed_candidate.md` gelesen.
Breite/Höhe des iframe-Codes werden entfernt und über CSS gesteuert.

Breakpoint:

```css
@media (max-width: 760px)
```

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/149_felt_desktop_embed_mobile_fallback_prototype.py`
- `docs/B149_felt_desktop_embed_mobile_fallback_prototype.md`
- `docs/B149_felt_desktop_embed_mobile_fallback_prototype_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Desktop: Felt-Karte lädt und steht nach dem Oberschwaben-Abschnitt.
- Desktop: Annotation, Legende und Popup funktionieren.
- Mobile 390 px: iframe ist nicht sichtbar.
- Mobile: Fallback-Box mit Button ist sichtbar.
- Button öffnet die Felt-Karte in neuem Tab.
- Bestehende Oberschwaben-Karte ist nicht gelöscht.
