# B153 - Map Role and Redundancy Audit

Date: 2026-07-01

## Ziel

B153 prüft nach der Felt-Integration, welche Karten- und Grafikblöcke welche Rolle im Storyboard haben.
Der Patch verändert die öffentliche Seite nicht. Er dient als redaktionelles Audit, bevor weitere Kartenblöcke umgebaut werden.

## Ergebnis

- untersuchte Sections: 21
- Sections mit besonderer Relevanz für Oberschwaben/Felt: 6
- B149/Felt-Block im HTML erkannt: ja
- B152-Rahmung `Interaktive Vertiefung` erkannt: ja

## Rollen-Zählung

| Rolle | Anzahl |
|---|---:|
| `felt_interactive_deepening` | 2 |
| `frame_mismatch` | 12 |
| `global_context` | 6 |
| `method_sources` | 6 |
| `regional_static_story` | 5 |
| `value_chain` | 13 |
| `water_governance` | 17 |

## Relevante Karten-/Redundanzstellen

| Nr. | Überschrift | Rolle | Audit-Notiz |
|---:|---|---|---|
| 13 | Oberschwaben, wo Moorschutz auf Landwirtschaft trifft | frame_mismatch; regional_static_story; water_governance | behalten: Einordnung im Lesefluss; nicht durch Felt ersetzen, solange Sticky/Story-Kontext gebraucht wird |
| 14 | Die statische Karte zeigt die Lage – die interaktive Karte zeigt die Details | frame_mismatch; regional_static_story; felt_interactive_deepening; value_chain; water_governance; method_sources | potenzielle Dopplung: statische Story-Karte und interaktive Vertiefung im selben Abschnitt genau prüfen |
| 15 | Die Schnittmenge macht den Prüfbedarf sichtbar, nicht die Lösung | regional_static_story; method_sources | behalten: Einordnung im Lesefluss; nicht durch Felt ersetzen, solange Sticky/Story-Kontext gebraucht wird |
| 16 | Aus der Schnittmenge folgt Verhandlung, keine Einheitslösung | regional_static_story; value_chain; water_governance | behalten: Einordnung im Lesefluss; nicht durch Felt ersetzen, solange Sticky/Story-Kontext gebraucht wird |
| 18 | Nutzungskontexte entscheiden, welche Wertschöpfungspfade plausibel sind | regional_static_story; value_chain; water_governance | behalten: Einordnung im Lesefluss; nicht durch Felt ersetzen, solange Sticky/Story-Kontext gebraucht wird |
| 21 | Grundlagen | global_context; frame_mismatch; felt_interactive_deepening; value_chain; water_governance; method_sources | behalten: interaktive Vertiefung; klar als Detailschicht rahmen, nicht als zweite Hauptkarte |

## Redaktionelle Entscheidung nach B152

Die bestehende Oberschwaben-Karte und die Felt-Karte sollten nicht gegeneinander ausgespielt werden.

- **Statische Oberschwaben-Karte:** bleibt Story- und Orientierungskarte im Lesefluss.
- **Felt-Karte:** bleibt interaktive Vertiefung für Details, Popup und Vektorqualität.
- **Mobile:** Felt bleibt optional über externen Link; die Story darf nicht vom iframe abhängig werden.

## Empfohlene nächste Schritte

1. Keine weitere neue Karte hinzufügen, bevor die Rollen konsolidiert sind.
2. In B154 nur Abstände/Übergänge zwischen statischer Karte und Felt-Vertiefung feinjustieren, falls visuell nötig.
3. In B155 Veröffentlichungsgates aktualisieren: Felt-Lizenz, Datenschutz, Hohenheim/SOLAMO-BW-Freigabe, 19.900-ha-Methodennotiz.
4. Den großen Sticky-Zoom erst später als eigenen Strang behandeln.

## Dateien

- CSV-Inventar: `docs/B153_map_role_inventory.csv`
