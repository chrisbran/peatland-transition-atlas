# B164 - Premium Pacing Polish

Date: 2026-07-01

## Ziel

B164 schärft den Lesefluss nach B163. Es werden keine neuen Inhalte, Karten oder Grafiken ergänzt.
Stattdessen werden Titel, Leads und Übergänge knapper und stärker auf Feature-Rhythmus getrimmt.

## Prinzip

- kürzere Aussagen
- weniger Meta-Sprache
- mehr aktive Sätze
- keine fachlichen Grenzen entfernen
- keine Strukturänderung
- keine neue Section

## Ersetzungen

| ID | Treffer | Zweck |
|---|---:|---|
| `hero_subtitle` | 1 | sharpens the opening promise without adding detail |
| `hero_card_3_title` | 1 | more concrete and image-led than abstract transformation language |
| `hero_card_3_body` | 1 | shorter hero-card copy |
| `core_argument_heading` | 1 | turns the headline into a more memorable sentence |
| `core_argument_body` | 1 | removes stacked nouns in the early thesis paragraph |
| `regional_heading` | 1 | shorter regional section title |
| `regional_intro` | 1 | reduces a long question chain |
| `paths_heading` | 1 | more editorial and less administrative |
| `paths_lead` | 1 | shortens an explanatory lead |
| `oberschwaben_heading_punctuation` | 1 | clearer title rhythm |
| `felt_heading` | 1 | turns a functional label into an editorial transition |
| `felt_lead` | 1 | removes explanatory meta-language around the Felt block |
| `felt_to_balance_transition` | 1 | shorter transition after Felt |
| `area_balance_heading` | 1 | reduces caveat framing and improves section rhythm |
| `area_balance_body` | 1 | turns two defensive sentences into one active sentence |
| `negotiation_heading` | 1 | removes a repeated negative clause |
| `value_context_heading` | 1 | shorter and more active value-chain matrix heading |

## Grobe Wortzählung

Die folgende Zählung ist nur ein Indikator, weil sie HTML und technische Texte nicht perfekt trennt.

- vorher: 3001
- nachher: 2947
- Differenz: 54

## CSS

B164 ergänzt nur eine kleine Text-Rhythmus-Politur:

- `text-wrap: balance` für Überschriften, falls Browser es unterstützt
- `text-wrap: pretty` für Absätze/Listen, falls Browser es unterstützt

## QA

Nach dem Patch:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Hero bleibt stark
- zentrale Kartenstory bleibt unverändert
- Oberschwaben/Felt Übergang klingt kürzer
- Flächenbilanz startet direkter
- Scorecard bleibt unverändert zu B162c
