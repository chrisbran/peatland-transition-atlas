# B158 - Reduce Notice Density

Date: 2026-07-01

## Ziel

Nach B157 war die Seite fachlich sehr abgesichert, aber visuell zu stark von Hinweisen,
Lesarten und Warnboxen geprägt. B158 reduziert diese Hinweisdichte, ohne die fachlichen
Grenzen zu entfernen.

## Prinzip

- wichtige Einschränkungen bleiben erhalten
- weniger sichtbare Boxen im Lesefluss
- Detailmethodik wird aufklappbar
- Drittanbieter-Hinweis wird kurz und ruhig
- keine Änderung an Karten, Zahlen, Quellen oder Daten

## Änderungen

1. **Felt-Lesart-Box entfernt**
   - Die Aussage `Schnittmenge = Prüfbedarf, nicht Eignung` bleibt bereits in Karte,
     Quellenzeile, Mobile-Fallback und Methodik erhalten.
   - Die zusätzliche Box war redundant.

2. **Drittanbieter-Hinweis gekürzt**
   - vorher: längerer Warnhinweis unter dem Felt-Block
   - jetzt: kurze Fußnotenzeile mit Verweis auf den Quellen-/Methodenbereich

3. **Methodennotiz zur Hektarbilanz eingeklappt**
   - die methodische Absicherung bleibt verfügbar
   - sie dominiert aber nicht mehr direkt den Flächenbilanz-Abschnitt

## Nicht geändert

- `~19.900 ha`
- Felt-iframe
- Mobile-Fallback
- Quellenregister
- zentrale Methode
- statische Oberschwaben-Karte
- Datenbasis

## QA

Nach dem Patch:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Seite wirkt weniger von Warn-/Hinweisboxen überladen.
- Felt-Block bleibt verständlich.
- Hektarbilanz bleibt methodisch absicherbar.
- Keine Layoutverschiebung.
