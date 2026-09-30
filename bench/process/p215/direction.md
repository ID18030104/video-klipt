# p215 — Cabinet dentaire Dr Amrani · « Le nuancier »

Reel / Story 9:16 · 1080 × 1920 · 30 fps · **durée 15,0 s** · Instagram + Facebook · copy en français.

---

## 1. Audience et message unique

**Qui scrolle :** 25–55 ans à Montpellier, actifs, parents, jeunes pros. Ils boivent du café, n'aiment pas le dentiste, repoussent le RDV parce qu'il faut appeler aux heures de bureau. Le blanchiment les tente mais ils l'imaginent long, douloureux, flou sur le prix.

**Insight :** « Je sais que mes dents ont jauni un peu, mais entre le téléphone qui sonne occupé et le prix que je ne connais pas, je ne franchis jamais le pas. »

**Le message unique (à retenir) :** *Un sourire plus lumineux en une séance, et le RDV se prend en 20 secondes, même à 23 h.*
Tout le film sert cette phrase : le nuancier qui s'éclaircit = le résultat ; l'interface de RDV = la facilité. Le prix (390 €) est affiché clairement : c'est de la transparence, pas de la promo.

**Registre :** soin rassurant, moderne, chaleureux. Surtout pas clinique : pas de bleu hôpital, pas de fauteuil, pas de fraise, pas de dent 3D anatomique, pas de blouse.

**Déontologie (important, santé en France) :** ton informatif, sans superlatif ni promesse chiffrée de résultat (« jusqu'à X teintes » interdit), pas de « promo », pas d'urgence commerciale. La mention « Après bilan avec votre dentiste » figure à l'écran. Le prix est présenté comme une information.

---

## 2. Concept — « Le nuancier »

Chaque dentiste utilise un **teintier** : une rangée de petites languettes de couleur ivoire, du plus jaune au plus clair. C'est l'objet le plus reconnaissable et le plus doux du métier, sans rien de médical qui fasse peur. On en fait le héros graphique :

1. Un **sourire stylisé** (un arc souple de six « dents-pastilles » arrondies) apparaît, légèrement ambré.
2. Les pastilles se détachent et se rangent en **nuancier** : six languettes, de l'ambre au blanc nacré. Une lumière passe dessus, elles s'éclaircissent l'une après l'autre : c'est le blanchiment, raconté par la couleur.
3. La languette la plus claire se transforme (morph) en **bouton de créneau** dans une **interface de prise de RDV** : on réserve jeudi 18 h 30, à 23 h 12 le soir.
4. End card : le sourire revient, lumineux, et devient le logo.

**Pourquoi c'est ce cabinet :** un objet de métier réel (crédibilité), traité en formes rondes et couleurs chaudes (le « pas clinique » du brief), et un fil continu (pastille → languette → bouton → logo) qui relie les deux nouveautés en une seule histoire.

---

## 3. Direction artistique

### Palette (5 couleurs + dégradé du nuancier)
| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Fond dominant | Ivoire perle | `#FBF6EE` | fond de toutes les scènes |
| Texte / structure | Encre lagon | `#0F3D3E` | tous les textes, boutons pleins, contours du téléphone |
| Secondaire | Menthe douce | `#CFE8DF` | grandes formes douces de fond, cartes, créneaux disponibles |
| Accent (rare) | Corail pêche | `#FF8C69` | uniquement : le point du prix, la pastille « Réservé », le trait sous l'URL. Jamais du texte sur corail blanc. |
| Texte secondaire | Lagon doux | `#44706E` | sous-titres, mentions (contraste ≥ 4,5:1 sur ivoire, vérifié) |

**Nuancier (6 languettes, de gauche à droite, état « avant ») :** `#D9B98A`, `#E2C79E`, `#E9D4B2`, `#EFDFC5`, `#F4E9D8`, `#F8F1E6`.
**État « après » (fin du balayage), toutes les languettes glissent vers :** `#F3E6D2`, `#F6ECDD`, `#F8F1E6`, `#FAF5EC`, `#FCF9F3`, `#FFFFFF`.
Dents du sourire : « avant » `#E6CFA6`, « après » `#FFFDF8` avec liseré `#0F3D3E` à 10 % d'opacité (2 px) pour qu'elles restent visibles sur ivoire.

### Typographies (2 familles)
- **Fraunces** (poids 400 et 600, + 400 italic) — titres. Serif douce et ronde, chaleureuse, jamais institutionnelle.
- **Figtree** (500, 600, 700) — UI, infos, mentions. Très lisible, arrondie.

Échelle (canvas 1080 de large) :
| Niveau | Police | Taille / interligne | Approche |
|---|---|---|---|
| H1 accroche | Fraunces 600 | 112 px / 1,0 | -1,5 % |
| H1 italique (mot clé) | Fraunces 400 italic | 112 px | -1 % |
| H2 | Fraunces 600 | 84 px / 1,05 | -1 % |
| Prix | Fraunces 600 | 150 px | -2 % |
| Info / corps | Figtree 600 | 44 px / 1,25 | 0 |
| UI téléphone | Figtree 500/700 | 30–40 px | 0 |
| Mentions | Figtree 500 | 30 px | +1 % |
| Étiquettes nuancier | Figtree 700 | 30 px, capitales | +8 % |

Charger : `../../node_modules/@fontsource/fraunces/400.css`, `/600.css`, `/400-italic.css` ; `../../node_modules/@fontsource/figtree/500.css`, `/600.css`, `/700.css`. Attendre `document.fonts.ready` dans `KLIPT.ready`.

### Langage graphique
- **Tout est rond** : rayons généreux (languettes : rayon 36 px en haut, 14 px en bas ; cartes : 44 px ; boutons : pilule complète). Aucun angle vif, aucun trait fin agressif.
- **Formes douces de fond** : 2 grandes « bulles » organiques (blobs SVG, menthe `#CFE8DF`, opacité 55 %) qui dérivent lentement pendant tout le film (±30 px, ±2°), une en haut à droite, une en bas à gauche. Elles sont le « vivant » permanent.
- **Lumière** : un reflet (dégradé linéaire blanc 0 → 70 % → 0, incliné à 20°, largeur 160 px) qui balaie le nuancier puis, plus tard, le logo. C'est le geste « éclat ».
- **Ombres** : très douces, teintées lagon : `0 24px 60px rgba(15,61,62,0.12)`. Jamais de noir.
- **Icônes** : Lucide, trait 2,5 px, couleur Encre lagon : `calendar-check`, `clock`, `sparkles` (une seule fois), `map-pin`, `check`, `chevron-left`, `chevron-right`. Pas d'emoji.

### Textures
- Grain `feTurbulence` (baseFrequency 0.85, numOctaves 2) en overlay plein cadre, opacité **5 %**, mode `multiply`, statique.
- Vignette très légère : dégradé radial ivoire → `#F3EADB` sur les bords (15 %).

### Logo (à construire en SVG, identique partout)
- **Symbole** : un **sourire-dent** — une forme de dent simplifiée (deux lobes arrondis en haut, deux racines courtes et rondes en bas, style « pastille »), 96 × 104 px, remplissage Encre lagon ; à l'intérieur, un arc de sourire évidé (épaisseur 8 px, couleur Ivoire) qui traverse la couronne. Un petit éclat 4 branches corail `#FF8C69` (12 px) en haut à droite.
- **Wordmark** : « Dr Amrani » en Fraunces 600, 72 px, Encre lagon. Dessous : « CABINET DENTAIRE · MONTPELLIER » en Figtree 700, 26 px, capitales, approche +12 %, Lagon doux.
- Disposition : symbole à gauche, wordmark à droite, gap 28 px. Version compacte (symbole seul, 56 px) en coin haut-gauche des scènes 2 et 3 (x 70, y 240).

---

## 4. Copy finale (chaînes exactes)

Espaces : « ⍽ » ci-dessous = espace insécable fine U+202F (avant `?` `!` `:` `;`, dans les nombres). Utiliser `&#8239;` en HTML. Espace insécable U+00A0 entre nombre et unité (`390&nbsp;€`, `1&nbsp;séance`, `24&nbsp;h`). Apostrophe typographique `’`.

**Scène 1 — accroche**
- L1 : `Café, thé,`
- L2 : `le temps qui passe…`
- L3 (italique) : `et votre sourire⍽?`

**Scène 2 — blanchiment**
- Étiquette haute : `NOUVEAU AU CABINET`
- H2 : `Le blanchiment` / `en cabinet.`
- Étiquettes sous le nuancier (gauche et droite) : `AVANT` ... `APRÈS`
- Info ligne 1 : `1 séance`
- Info ligne 2 : `390 €`   (le « € » en Fraunces 600, 150 px ; un point corail de 18 px devant le prix)
- Mention : `Après bilan avec votre dentiste.`

**Scène 3 — RDV en ligne**
- H2 : `Réservez` / `quand vous voulez.`
- Écran téléphone :
  - Barre d’état : `23:12`
  - En-tête : `Dr Amrani` (Figtree 700, 40 px) + sous-titre `Prendre rendez-vous` (Figtree 500, 30 px)
  - Motif sélectionné (carte) : `Blanchiment · 1 h 30`
  - Mois : `Octobre 2026`
  - En-têtes de jours : `L M M J V S D`
  - Créneaux (pilules) après sélection du 15 : `17:00` `17:45` `18:30` `19:15`
  - Bouton : `Confirmer`
  - Confirmation : `Rendez-vous confirmé` / `Jeudi 15 octobre · 18:30`
- Badge sous le téléphone : `En ligne 24⍽h/24, 7⍽j/7`

**Scène 4 — end card**
- Logo complet (voir §3).
- Ligne 1 (Fraunces 600, 84 px) : `Un sourire` / `plus lumineux.`
- CTA (bouton pilule plein Encre lagon, texte Ivoire, Figtree 700, 42 px) : `Prendre RDV en ligne`
- URL (Figtree 600, 40 px) : `dr-amrani-dentiste.fr`
- Contact (Figtree 500, 32 px, Lagon doux) : `04 67 58 21 40 · Montpellier` (espaces insécables dans le numéro)
- Mention (Figtree 500, 30 px, Lagon doux) : `3 praticiens · Blanchiment après bilan`

Relu : accents (« APRÈS », « confirmé », « réservez »), pas de majuscule accentuée manquante, apostrophes courbes, ellipse `…` (U+2026, un seul caractère), ponctuation double précédée d’une fine insécable.

---

## 5. Storyboard (15,0 s)

Zones sûres : aucun texte clé au-dessus de y = 220 ni en dessous de y = 1540 ; marges latérales 70 px (texte aligné à gauche sur x = 90 sauf mention contraire).

### Scène 1 — Accroche « Café, thé… » · 0,00 → 3,40 s
Composition : fond ivoire, blobs menthe déjà présents (ils dérivent dès la frame 0). Texte aligné à gauche, x = 90, bloc commençant y = 330. Le **sourire stylisé** centré, x = 540, y = 1180, largeur 760 px.

Sourire : six dents-pastilles (rectangles arrondis, 96 × 128 px, rayon 44 px) posées le long d’un arc (courbe quadratique : points 190,1080 → 540,1260 → 890,1080 ; les dents suivent la tangente, rotation ±14° aux extrémités), sous une lèvre supérieure = trait Encre lagon 10 px, extrémités arrondies, courbe parallèle 40 px au-dessus. Couleur des dents : `#E6CFA6`.

- **0,00–0,60** : le trait de lèvre se dessine du centre vers les deux bords (DrawSVG 50 %→0–100 %, `power3.out`). Les dents « poussent » de scale 0 → 1 depuis leur base, stagger 0,05 s du centre vers l’extérieur, `back.out(1.6)`. Mouvement dès la frame 0 (la lèvre est à 8 % à t = 0).
- **0,15** : L1 `Café, thé,` monte de derrière un masque (yPercent 110 → 0, 0,6 s, `expo.out`), mots en stagger 0,08 s.
- **0,90** : L2 `le temps qui passe…` idem. Pendant L1–L2, les dents se teintent légèrement plus ambré (`#E6CFA6` → `#DDBF8F`, 1,4 s, `sine.inOut`) : on « vit » la patine.
- **1,90** : L3 italique `et votre sourire ?` entre, puis léger rebond d’échelle du mot « sourire » (1 → 1,04 → 1, 0,5 s).
- **1,90–3,20** : hold lisible. Le sourire respire (scaleY 1 → 1,02, sinusoïdal, période 2 s).
- **Transition 3,00 → 3,40** : le texte sort vers le haut (yPercent 0 → -110, stagger 0,04, `power2.in`). Simultanément, les six dents **se détachent de l’arc** et se déplacent (MotionPath / tween x,y,rotation, `power3.inOut`, 0,8 s, stagger 0,04 de gauche à droite) vers leurs positions de nuancier (scène 2). La lèvre se rétracte (DrawSVG 100 % → 0, depuis les bords vers le centre).

### Scène 2 — Le nuancier qui s’éclaircit · 3,40 → 7,60 s
Composition :
- Logo compact coin haut-gauche (x 70, y 240), fade + y 12 → 0 à 3,40.
- Étiquette `NOUVEAU AU CABINET` y = 380, Figtree 700 30 px, Lagon doux, avec pastille `sparkles` 32 px à gauche.
- H2 `Le blanchiment` / `en cabinet.` y = 440, Fraunces 600 84 px.
- **Nuancier** centré horizontalement, y = 760 à 1160 : six languettes 128 × 380 px (rayon 36 en haut, 14 en bas), gap 20 px (largeur totale 888 px, x de 96 à 984). Chacune porte en bas une petite étiquette Figtree 700 26 px Encre lagon à 60 % (codes décoratifs : `A3`, `A2`, `B2`, `A1`, `B1`, `0M1`). Ombre douce. Un fin rail Encre lagon à 15 % relie leurs têtes (comme un vrai teintier). Sous le rail, à gauche `AVANT`, à droite `APRÈS` (Figtree 700 30 px, +8 %), y = 1200.
- Bloc info y = 1270 à 1520 : `1 séance` (Figtree 600, 48 px) au-dessus, puis le prix `● 390 €` (point corail 18 px, Fraunces 600 150 px). À droite du prix, aligné en bas, la mention `Après bilan avec votre dentiste.` sur deux lignes (Figtree 500, 30 px, Lagon doux, largeur 360 px) — ou sous le prix si ça ne tient pas, y ≤ 1540.

Timing :
- **3,40–4,20** : les dents arrivent et se déforment en languettes (MorphSVG pastille → languette, 0,5 s), en prenant les six couleurs « avant ». H2 monte par masque à 3,50 (lignes stagger 0,1). Étiquette à 3,45.
- **4,30–5,90** : **le balayage de lumière** traverse le nuancier de gauche à droite (x -200 → 1280, 1,6 s, `power1.inOut`). Au passage du reflet, chaque languette glisse vers sa couleur « après » (tween couleur 0,5 s, déclenché à 4,40 + i × 0,22 s). Un micro-rebond de chaque languette (y -10 → 0, `back.out`) accompagne le changement. `AVANT`/`APRÈS` apparaissent à 4,30 (fade 0,3 s).
- **5,10** : `1 séance` entre (masque). **5,35** : le prix : point corail pop (scale 0 → 1, `back.out(3)`), puis `390 €` monte par masque, chiffres en stagger 0,05. **5,70** : mention fade-in (opacité 0 → 1, 0,4 s).
- **5,90–7,20** : hold. Vivant : les languettes flottent individuellement (y ±4 px, sinus déphasés), blobs dérivent.
- **Transition 7,20 → 7,60 (morph continu)** : tout le texte sort par masque vers le haut (`power2.in`, 0,3 s) ; les languettes 1 à 5 glissent vers le bas hors cadre en stagger (y +900, `power3.in`). **La 6e languette (la blanche)** reste, grandit et se transforme (MorphSVG / animation de width, height, border-radius, 0,5 s, `power3.inOut`) **en écran de téléphone** : 700 × 1240 px, rayon 72 px, centré x = 540, y = 360 → 1600 (le haut de l’écran démarre sous la zone sûre ; la partie basse du téléphone peut toucher la zone plateforme, elle ne porte pas d’info critique). Un cadre Encre lagon de 14 px se dessine autour.

### Scène 3 — La prise de RDV · 7,60 → 11,60 s
Composition : H2 `Réservez` / `quand vous voulez.` NE PEUT PAS aller au-dessus du téléphone faute de place → **le téléphone se décale** : à 7,60–8,00 il se réduit à 620 × 1100 px et descend à y = 560 → 1660 (centré x = 540). H2 en haut, y = 260 → 520, aligné à gauche x = 90, Fraunces 600 84 px (Réservez) + Fraunces 400 italic 84 px (quand vous voulez.). Le bas du téléphone passe sous 1540 : la **zone utile de l’écran** (créneaux, bouton) reste entre y 620 et 1500.

Contenu de l’écran (fond `#FFFFFF`, padding 40 px) :
- Barre d’état : `23:12` à gauche (Figtree 700 28 px), icônes batterie/réseau simples à droite. Placer l’heure bien visible : c’est la preuve « même le soir ».
- En-tête : cercle 64 px Menthe avec le symbole-dent + `Dr Amrani` / `Prendre rendez-vous`.
- Carte motif (fond Menthe douce, rayon 28) : icône `sparkles` + `Blanchiment · 1 h 30`, coche `check` à droite.
- Calendrier `Octobre 2026` avec chevrons ; grille 7 colonnes L M M J V S D. **Octobre 2026 commence un jeudi** : première ligne vide L, M, M puis 1 (J), 2, 3, 4. Afficher les jours 1 à 25 (4 lignes pleines ; tronquer après le 25 si nécessaire, puis dégradé blanc). Jours disponibles en menthe (13, 14, 15, 16, 20, 21, 22), passés/indisponibles en Lagon doux 40 %.
- Rangée de créneaux (pilules contour Encre lagon 2 px, 132 × 64 px) : `17:00` `17:45` `18:30` `19:15`.
- Bouton plein Encre lagon, largeur 100 %, 96 px de haut : `Confirmer` (Ivoire, Figtree 700 38 px).

Un **curseur-doigt** (cercle 56 px, Encre lagon 25 %, halo qui pulse au tap) pilote l’UI.

Timing :
- **7,60–8,10** : réduction/placement du téléphone, contenu de l’écran apparaît par blocs (stagger 0,06, y 20 → 0, fade). H2 masque à 7,75.
- **8,30** : le doigt entre depuis le bas-droite (`power3.out`), **8,60** tap sur le **15** : cercle Encre lagon plein derrière le chiffre (scale 0 → 1, `back.out(2)`), chiffre passe en Ivoire. Ripple menthe.
- **8,80** : la rangée de créneaux s’ouvre (height 0 → 64, créneaux stagger 0,05).
- **9,20** : tap sur `18:30` → la pilule se remplit Encre lagon, texte Ivoire.
- **9,60** : tap sur `Confirmer` (bouton scale 0,96 → 1).
- **9,80–10,30** : **écran de confirmation** : un panneau Menthe douce monte depuis le bas de l’écran (rayon 44 en haut, `expo.out`, 0,5 s) avec un cercle corail 120 px contenant l’icône `check` Ivoire (trait dessiné DrawSVG 0,35 s), puis `Rendez-vous confirmé` (Figtree 700 44 px) et `Jeudi 15 octobre · 18:30` (Figtree 500 34 px).
- **10,30** : badge (placé au-dessus du téléphone, car le dessous est hors zone sûre) : pilule Menthe douce avec icône `clock` + `En ligne 24 h/24, 7 j/7` (Figtree 700 36 px) glisse sous le H2 à y = 540 et le téléphone descend doucement de 40 px pour lui laisser la place (tween `power2.inOut`).
- **10,30–11,20** : hold. Le téléphone flotte (y ±6 px, rotation ±0,6°).
- **Transition 11,20 → 11,60 (zoom-through)** : caméra « entre » dans le cercle corail de confirmation : toute la scène (conteneur) scale 1 → 6 centrée sur le cercle, `power3.in`, pendant qu’un disque Ivoire perle grandit depuis ce centre et recouvre l’écran (clip-path circle 0 → 150 %). Le fond de l’end card est ce disque.

### Scène 4 — End card · 11,60 → 15,00 s (tenue ≥ 3 s)
Composition, centrée horizontalement :
- **Sourire lumineux** y = 380 → 560 : reprise du sourire de la scène 1, largeur 600 px, dents `#FFFDF8` avec liseré, lèvre Encre lagon.
- Titre y = 640 : `Un sourire` / `plus lumineux.` Fraunces 600 84 px, centré (« lumineux. » en Fraunces 400 italic).
- Logo complet y = 900 → 1020, centré.
- Bouton CTA y = 1110, pilule 700 × 120 px, Encre lagon, texte `Prendre RDV en ligne` Ivoire Figtree 700 42 px, icône `calendar-check` 44 px à gauche.
- URL y = 1280 : `dr-amrani-dentiste.fr`, Figtree 600 40 px, Encre lagon, soulignée d’un trait corail 6 px arrondi.
- Contact y = 1360 : `04 67 58 21 40 · Montpellier` (icône `map-pin` 30 px avant « Montpellier »).
- Mention y = 1430 : `3 praticiens · Blanchiment après bilan`, Figtree 500 30 px, Lagon doux.

Timing :
- **11,60–12,20** : le sourire se redessine (lèvre DrawSVG depuis le centre, dents scale 0 → 1 stagger 0,04, déjà blanches). **11,80** titre par masque (lignes stagger 0,1). 
- **12,10** : le reflet lumineux traverse le sourire (x -200 → 1280, 0,7 s) ; éclat corail 4 branches pop au coin de la dent centrale (scale 0 → 1 → 0,8, rotation 0 → 45°).
- **12,20** : logo (symbole scale 0,8 → 1 `back.out`, wordmark masque). **12,45** bouton (y 30 → 0, fade, `expo.out`). **12,65** URL + trait corail qui se dessine de gauche à droite (0,4 s). **12,80** contact et mention (fade, stagger 0,08).
- **13,00–15,00** : **hold calme**. Seuls vivants : dérive des blobs, respiration du bouton (scale 1 → 1,02 → 1, période 1,6 s, `sine.inOut`), grain. Pas de fondu de fin : la dernière frame est l’end card complète (sert de poster).

---

## 6. Notes de mouvement

- Personnalité : **douce et précise**. Entrées `expo.out` / `power3.out` 0,5–0,7 s ; sorties `power2.in` 0,3 s ; déplacements `power3.inOut`. Rebonds `back.out(1.6)` réservés aux objets ronds (dents, languettes, points), jamais au texte.
- Texte toujours révélé par **masque** (conteneur `overflow:hidden`, ligne yPercent 110 → 0), jamais par simple fondu.
- **Fil continu** obligatoire : dents → languettes → languette blanche → téléphone → cercle de confirmation → end card. Pas de coupe sèche, pas de fondu au noir.
- Rythme : scène 1 posée (lecture), scène 2 le « wow » couleur, scène 3 rapide et précise (taps toutes les 0,3–0,6 s), scène 4 calme.
- Temps de lecture vérifiés : accroche 9 mots lisibles de ~0,9 à 3,0 s ; scène 2 : H2 + prix visibles 5,7 → 7,2 s ; confirmation 10,3 → 11,2 s ; end card 3,4 s.
- Toujours quelque chose de vivant : blobs (dérive sinusoïdale continue, seule animation linéaire/sinus autorisée), flottement des objets pendant les holds, grain statique.

---

## 7. Approche technique

- **Une page, GSAP** : `gsap.timeline({paused:true})`, `KLIPT = {width:1080, height:1920, fps:30, duration:15, ready, render: t => { tl.seek(t,false); }}`. Plugins : DrawSVGPlugin, MorphSVGPlugin, MotionPathPlugin (dents vers nuancier ; un simple tween x/y/rotation avec `power3.inOut` est acceptable), CustomEase si besoin.
- **Oscillations continues** (blobs, flottements, respiration) : ne pas les mettre en `repeat:-1` dans la timeline ; les calculer dans `render(t)` après le seek (`Math.sin(t*…)` appliqué via `gsap.set` sur un wrapper parent distinct de l’élément animé par la timeline, pour ne pas écraser les tweens).
- **Sourire et nuancier en SVG** (un seul `<svg>` 1080 × 1920 en couche de fond, viewBox identique aux pixels). Les dents sont des `<rect rx>` dans des `<g>` (transform pour position/rotation) ; pour la déformation dent → languette, animer `width`, `height`, `rx` des rects plutôt que de morpher des paths (plus simple, déterministe). La languette → téléphone : passer à un `<div>` HTML superposé exactement aux mêmes coordonnées au moment 7,20 (swap invisible), puis animer ce div (width/height/border-radius/top/left) — l’UI du téléphone est en HTML/CSS dedans.
- **Couleurs du nuancier** : tweener `fill` directement (GSAP interpole les hex).
- **Reflet** : `<rect>` avec `linearGradient` blanc, `mix-blend-mode: screen` ou simple opacité 0,7, clippé par un `<clipPath>` qui contient les six languettes (le reflet n’apparaît que sur elles).
- **Grain** : `<svg>` plein cadre avec `<filter><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7"/><feColorMatrix type="saturate" values="0"/></filter>`, opacité 0,05, `mix-blend-mode:multiply`, `pointer-events:none`, au-dessus de tout.
- **Transition zoom-through** : scale du conteneur scène 3 avec `transformOrigin` sur le centre du cercle corail + `clip-path: circle(r at x y)` sur le conteneur end card animé de 0 % à 150 %.
- **Icônes Lucide** : inliner le SVG (copier le contenu de `../../node_modules/lucide-static/icons/<nom>.svg`), `stroke="#0F3D3E"`, `stroke-width="2.5"`.
- Texte : respecter les insécables (`&#8239;` avant `?`, `&nbsp;` dans `390&nbsp;€`, `24&#8239;h/24`, `04&nbsp;67&nbsp;58&nbsp;21&nbsp;40`). Aucune coupure de ligne automatique non prévue : lignes explicitement séparées en `<span class="line">`.
- Pas de `Math.random` ; si besoin, `KK.rng(215)`.
- Vérifier frames clés : 0,5 / 2,5 / 4,0 / 5,2 / 6,5 / 7,4 / 9,0 / 10,6 / 11,4 / 14,5 s.
- `meta.json` : title « Le nuancier — blanchiment & RDV en ligne », techniques `["gsap","svg-illustration","morph","ui-mockup","drawsvg"]`, fonts `["Fraunces","Figtree"]`, palette `["#FBF6EE","#0F3D3E","#CFE8DF","#FF8C69","#44706E"]`.
