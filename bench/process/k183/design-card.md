# k183 · Garnier & Fils · carrousel « 5 signes chauffe-eau »

## 1. Fragments
- cumulus au fond du cellier / garage, qu’on ne regarde jamais
- groupe de sécurité : la molette, l’entonnoir, la goutte
- anode magnésium rongée, eau qui sort couleur thé
- tartre au fond de la cuve : « ça claque », « ça siffle », « ça crépite »
- douche tiède à 7 h du matin
- plaque signalétique, date de fabrication, > 10 ans
- facture d’électricité qui grimpe sans changer d’usage
- Nantes, eau calcaire, propriétaires 35–70 ans
- 1987, trois générations, le père qui montre au fils
- 9 techniciens, dépannage 7j/7
- 49 € diagnostic, offert si remplacement
- ennemi : la cuve qui lâche un dimanche et inonde le cellier
Truth : un chauffe-eau prévient avant de lâcher, par cinq signes précis qu’on peut repérer soi-même, si on sait où regarder sur l’appareil.

## 2. Autopilot (zone to leave)
Bleu plombier + orange, icônes de goutte et clé à molette, photo de technicien souriant, cartes numérotées 1-5 en sans-serif gras, checklist verte.
Recent: Ledgerly vending machine / karaoke (Bricolage, JetBrains Mono, dark), Pécule receipts, printer test page, espresso (Young Serif, Archivo, Martian Mono).

## 3. Draw 20260929-210102-753e
Operators: Use the format · Mistake · Repeat. Domains: compass rose, encyclopedia plate, dungeon map, trophy engraving. Constraint: one single object centred in emptiness. Mechanic: a list that builds itself slide by slide.

## 4. Concepts (T/Su/St/C/F/Fr)
1. Planche d’encyclopédie : le chauffe-eau gravé en coupe comme une planche de Diderot, chaque slide agrandit une « Fig. » à la loupe, la légende se remplit slide après slide (encyclopedia plate × list builds × format) — 5/4/4/5/4/5 = 27
2. Carte de donjon : le cellier en plan de donjon, 5 pièges à repérer (dungeon map × mistake) — 3/5/4/3/3/5 = 23
3. Rose des vents des pannes : 5 branches = 5 signes (compass rose × repeat) — 2/4/3/3/4/4 = 20
4. La goutte répétée : une goutte répétée jusqu’à former une flaque qui dessine le chiffre 49 (repeat × mistake) — 3/4/4/3/3/4 = 21
5. Trophée gravé « 10 ans de bons et loyaux services » : l’âge comme retraite (trophy engraving) — 3/4/3/3/4/4 = 21
6. Objet seul dans le vide : chauffe-eau seul au centre, chaque slide il se dégrade un peu plus (constraint × sequence) — 4/3/4/4/3/4 = 22
7. Relevé de facture qui monte, colonne par colonne (autopilot-adjacent) — 3/2/3/4/5/2 = 19
8. Carnet d’entretien du grand-père, 1987, annoté par trois générations (intuition) — 4/3/3/3/3/4 = 20
Choice: 1. It tells people exactly where to look on their own appliance, which is the brief’s promise, and the plate grammar (Fig., légende, planche) turns « 5 signes » into a reference document worth saving.

## 6. Language
- Composition: cover = one object centred in emptiness on the plate, callouts 1-5. Sign slides = detail enlargement convention: small full figure left with a marker ring, leader lines to a large circular enlargement right. Text below like a plate caption. Foot: the legend that fills itself (done / current / to come).
- Type: the engraver and the encyclopedist speak: Cormorant Garamond 600/700 (display, italics for Fig.), EB Garamond 500 (body 30-36px), tracked caps for running heads.
- Colour: the plate’s own world: rag paper #EFE6D3, sepia ink #2A2019, hand-coloured washes (water #A9C2C4, warm top #E3BE97), and rust #A2381F, the colour of the failure itself (anode, drips), used only for what goes wrong and the offer.
- Material: engraved hatching (SVG line patterns), stippled insulation, double-rule plate frame, kit paper fibre, guilloche medallion for the 49 € seal.
- Constants: Garnier & Fils, Plomberie Chauffage, phone, site.

## 7. Bold move
The whole carousel is one engraved plate: no photo, no icon, no blue, and each sign is literally a magnified figure of the same drawing. The cover is almost empty paper with a single cut-open water heater.

## Tokens
--paper #EFE6D3 · --ink #2A2019 · --ink-2 #5A4A3A · --rust #A2381F · --water #A9C2C4 · --warm #E3BE97 · fonts Cormorant Garamond, EB Garamond (local @fontsource)

## 8. Critique (first render) and fixes
- Art director: the Fig. 2 and Fig. 5 enlargements were muddled (wrong crop, anode stealing Fig. 5), and the guilloche was clipped square behind the price. Fixed: new crops (tank floor with scale and noise marks; hairpin bends with crust), guilloche kept inside its bounds, a paper disc behind the price.
- Stranger in the feed: the cover reads (title + one object); the offer's old-style figures made « 49 € » and the phone look off. Fixed: lining figures for the price and phone.
- AI detector: capture tearing and slides bleeding into each other gave it away. Fixed: the plate is rasterised once (3x) and reused as a bitmap, and title orphans were broken by hand.
