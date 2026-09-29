# p216 — Studio Pilates Rive Gauche — « La ligne du midi »

Reel Instagram 1080 × 1920, **16,0 s**, 30 fps. Copy en français.

---

## 1. Audience & message

**Qui fait défiler ?** Cadres, profs, juristes, consultants de 28 à 55 ans qui travaillent dans le 7e ou autour (ministères, cabinets, Sciences Po, sièges de maisons). Le soir est pris (enfants, dîners, trajets), le matin est déjà serré. La pause déjeuner, elle, est souvent perdue : un sandwich devant l'écran et le dos qui se tasse. Ils ont tous déjà « voulu se mettre au Pilates » mais butent sur le créneau et sur la peur du cours collectif anonyme à 25 personnes.

**Insight :** « Ma pause déjeuner ne me fait pas de bien : elle me fait juste passer l'après-midi. »

**Le message unique :** *Votre pause du midi peut devenir 45 minutes de reformer, en groupe de 6 — et le premier cours coûte 25 €.*
(Tout le reste — petit groupe, reformer, Paris 7e — sert de preuve à ce message.)

**Registre :** premium doux, élégant, calme. Rive Gauche = raffinement discret, pas bling. Jamais « fitness » (pas de néon, pas de chrono agressif).

---

## 2. Concept — « La ligne du midi »

Une **seule ligne continue**, couleur argile, traverse toute la vidéo sans jamais disparaître. Comme la sangle d'un reformer ou une colonne vertébrale, elle **s'étire, se tend, se relâche** et se transforme à chaque temps :

1. elle s'étire horizontalement sous l'accroche (la pause qui « étire ») ;
2. elle s'enroule en **arc d'horloge de 12h15 à 13h** (45 minutes = 270° du cadran) ;
3. elle se déroule et devient la **sangle/ressort d'un reformer** dessiné au trait, qui respire avec le chariot ;
4. elle se retend et vient **souligner le prix, 25 €** ;
5. elle se courbe en **arche** : le logo, qui est à la fois un pont de Paris (la Rive Gauche) et la posture « shoulder bridge » du Pilates.

Pourquoi ça colle : le Pilates, c'est le contrôle et l'allongement ; une ligne qui s'allonge sans jamais casser raconte exactement ça, et le motif du pont ancre le studio dans son quartier. Le rythme est lent, fluide, respiré : l'inverse du midi pressé.

---

## 3. Direction artistique

### Palette (5 couleurs, discipline stricte)
| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Dominante (fond) | Lin | `#F3ECE2` | fond plein de toute la vidéo |
| Secondaire (formes) | Sable | `#E6D6C3` | grand blob organique |
| Secondaire (formes) | Sauge | `#B7C1AB` | blob moyen, pastilles des 6 places |
| Accent (rare) | Argile | `#C4836A` | LA ligne continue, uniquement elle + le point du logo |
| Texte | Encre expresso | `#2E2925` | tous les textes (contraste ≈ 13:1 sur Lin) |
| Texte accent | Argile foncée | `#9A5A43` | uniquement les mots en italique mis en valeur (« étirait », « pas plus. », « créneau ») — contraste ≈ 5,2:1 sur Lin |

Un 3e blob « blush » est la seule nuance supplémentaire tolérée : `#EBCDBD` à 70 % d'opacité.
Pas de noir pur, pas de blanc pur.

### Typographies (2 familles)
- **Cormorant Garamond** (`@fontsource/cormorant-garamond/300.css`, `300-italic.css`, `500.css`) — titres, chiffres, prix.
- **Manrope** (`@fontsource/manrope/500.css`, `600.css`) — étiquettes en capitales espacées, infos pratiques.

Échelle (canvas 1080 de large) :
| Niveau | Police | Taille / interlignage | Réglages |
|---|---|---|---|
| Prix | Cormorant 300 | 380 px / 0.9 | letter-spacing −0.02em, chiffres tabulaires non requis |
| Heure | Cormorant 300 | 170 px / 1.0 | letter-spacing −0.01em |
| Titre | Cormorant 300 (+ 300 italic) | 132–150 px / 1.0 | letter-spacing −0.015em |
| Sous-titre élégant | Cormorant 300 italic | 64 px / 1.15 | — |
| Texte info | Manrope 500 | 36 px / 1.35 | — |
| Étiquette | Manrope 600 | 30 px | MAJUSCULES, letter-spacing 0.24em |
Jamais de texte sous 30 px.

### Langage graphique
- **La ligne** : `stroke #C4836A`, épaisseur **6 px**, `stroke-linecap: round`, `stroke-linejoin: round`, pas de remplissage. Toujours un seul `<path>`.
- **Blobs organiques** en fond : 3 formes fermées, contours lisses générés par bruit simplex (voir §7), qui dérivent très lentement et changent de position à chaque temps. Aucune bordure. Légère ombre interne impossible → on reste en aplats doux ; la profondeur vient de leur superposition.
- **Trait fin** pour l'illustration du reformer : `stroke #2E2925`, 3 px, opacité 0.85, coins arrondis. Style dessin d'architecte, pas de remplissage sauf le chariot (Sable `#E6D6C3`).
- **Beaucoup de vide.** Alignement à gauche sur une marge de **90 px** pour les titres (sauf temps 2 et carte finale, centrés).
- **Texture** : grain `feTurbulence` (`type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7"`), désaturé, en overlay `mix-blend-mode: multiply`, **opacité 6 %**, statique sur toute la vidéo. Plus un vignettage très doux : radial-gradient transparent au centre → `rgba(46,41,37,0.06)` aux bords.

### Logo (à construire en SVG)
- **Symbole « Arche »** (viewBox 0 0 240 140) :
  - arche : `M 20 120 C 20 30, 220 30, 220 120` — stroke Argile `#C4836A`, 6 px, round cap ;
  - ligne d'eau/sol : `M 0 128 L 240 128` — stroke Encre `#2E2925`, 2 px, opacité 0.6 ;
  - point (la tête en posture de pont) : cercle `cx=8 cy=116 r=9`, rempli Argile.
  → On lit un pont sur la Seine et, en second regard, une silhouette en shoulder bridge.
- **Wordmark** sous le symbole, centré :
  - ligne 1 : « STUDIO PILATES » — Manrope 600, 28 px, letter-spacing 0.32em, Encre ;
  - ligne 2 : « Rive Gauche » — Cormorant 300 italic, 96 px, Encre, 14 px sous la ligne 1.
- Mini-version (en-tête persistante) : symbole 72 px de large + « Rive Gauche » Cormorant 300 italic 34 px à sa droite, placée **x 90, y 250** (haut de la zone sûre), opacité 0.9, visible de 0,4 s à 12,8 s. Présence de marque dès le début sans voler l'accroche.

---

## 4. Copy finale (chaînes exactes)

Espaces : `NNBSP` = espace fine insécable U+202F (avant `?` `!`), `NBSP` = espace insécable U+00A0 (avant `€`, entre chiffre et unité). Apostrophe typographique `’`.

| # | Chaîne | Notes |
|---|---|---|
| T1-a | `Et si votre pause` | |
| T1-b | `déjeuner` | |
| T1-c | `vous ` + *`étirait`* + `NNBSP?` | « étirait » en Cormorant 300 italic, Argile foncée |
| T2-label | `NOUVEAUX CRÉNEAUX DU MIDI` | accent sur le É capital obligatoire |
| T2-h1 | `12h15` | |
| T2-h2 | `13h` | |
| T2-sub | `45 minutes rien que pour vous.` | |
| T3-a | `À six,` | À capital accentué |
| T3-b | *`pas plus.`* | italic, Argile foncée |
| T3-sub | `Pilates sur reformer, en petit groupe.` | |
| T4-pre | `Votre 1<sup>er</sup> cours` | « er » en exposant (0.55em, décalé −0.45em) |
| T4-price | `25NBSP€` | |
| T4-label | `OFFRE DÉCOUVERTE` | dans une pastille contour |
| E-cta | `Réservez votre ` + *`créneau`* | italic Argile foncée sur « créneau » |
| E-info | `Paris 7e · Lien en bio` | « 7e » : le « e » en exposant (`7<sup>e</sup>`) ; point médian U+00B7 entouré d'espaces |
| E-handle | `@studiopilates.rivegauche` | |
| Logo | `STUDIO PILATES` / `Rive Gauche` | |

Relu : pas de faute, accords OK (« étirait » : conditionnel/imparfait après « si » ✔), « 1er » et « 7e » en abréviations correctes (jamais « 1ère », « 7ème »).

---

## 5. Storyboard (timecodes en secondes, 30 fps)

Zone sûre : textes clés entre **y 220 et y 1540**, marges latérales ≥ 70 px (on utilise 90 px).
Blobs (positions de leur centre, rayon moyen) donnés par temps ; entre deux temps ils glissent en 1,0 s `sine.inOut` centrés sur la transition.

### Temps 1 — Accroche « étirait » · 0,0 → 3,3 s
Blobs : Sable (820, 520, R 430) · Sauge (160, 1500, R 330) · Blush (980, 1320, R 240).
- **0,00** : le fond et les blobs sont déjà là, et la ligne est **déjà en train de se tracer** (8 % de sa longueur visible à la frame 0). Chemin : horizontale y = **1160**, de x 90 à x 990. `DrawSVG 8% → 100%` de 0,00 à 0,90 s, `power2.inOut`.
- **0,15 / 0,27 / 0,39** : T1-a, T1-b, T1-c montent derrière un masque (chaque ligne dans un conteneur `overflow:hidden`, translateY 105 % → 0), 0,8 s `expo.out`. Titre Cormorant 300 **138 px**, interlignage 1.0, aligné à gauche x 90, bloc de 3 lignes dont la ligne de base de T1-c est à **y 1080** (donc au-dessus de la ligne argile, 80 px d'air).
- **0,40** : mini-logo en haut à gauche, fondu + translateY 12 → 0 px, 0,6 s `power3.out`.
- **0,90 → 1,70** : « l'élastique pincé » : la ligne vibre verticalement en son milieu (courbe quadratique dont le point de contrôle central oscille : +22 px, −14, +8, −3, 0) — amortissement `elastic.out(1, 0.35)` feel ; en même temps, le mot **« étirait »** voit son `letter-spacing` passer de −0.015em à **0.07em** (1,0 → 2,0 s, `expo.out`) : le mot s'étire littéralement, le « ? » glisse vers la droite.
- **1,70 → 3,30** : tenue. Vie : le titre fait un scale 1 → 1.02 (origine gauche), blobs dérivent.
- **Transition 3,00 → 3,50** : T1 sort par le haut derrière ses masques (translateY 0 → −105 %, 0,4 s `power2.in`, stagger 0,06). Simultanément la ligne **se morphose (MorphSVG, 0,7 s de 3,05 à 3,75, `power3.inOut`) en arc d'horloge** du temps 2.

### Temps 2 — Le créneau · 3,3 → 6,5 s
Blobs : Sable (540, 960, R 470 — derrière le cadran) · Sauge (930, 380, R 260) · Blush (120, 1480, R 280).
Cadran : centre **(540, 930)**, rayon **340**.
- **Ligne** : arc de cercle de **3 h (angle 0°, point (880, 930)) à 12 h (point (540, 590)) dans le sens horaire**, soit 270° = les 45 minutes de 12h15 à 13h. Construire l'arc en 3 segments cubiques (pour un morph propre). Fin du morph à 3,75.
- **Graduations** : 12 petits traits Encre 2 px, longueur 18 px, à l'intérieur du cercle (rayon 310 → 292), opacité 0.35, apparaissent en rotation (stagger 0,03, fondu 0,3 s) à partir de 3,55.
- **Point de départ / arrivée** : un cercle plein Argile r 11 px posé à 3 h, puis un second à 12 h, pop scale 0 → 1 `back.out(2)` à 3,75 et 3,85.
- **3,55** : T2-label (Manrope 600 30 px, 0.24em, Encre) centré en **y 470**, révélé par masque vertical 0,6 s `expo.out`.
- **3,70** : T2-h1 « 12h15 » Cormorant 300 **170 px** centré, ligne de base y **900** ; **3,82** : un filet horizontal Encre 1,5 px, 120 px de large, centré à y 950, se trace depuis le centre (scaleX 0 → 1, 0,5 s) ; **3,90** : T2-h2 « 13h » 170 px, ligne de base y **1110**. Montées par masque, 0,8 s `expo.out`.
- **4,30** : T2-sub Cormorant 300 italic **64 px**, centré, ligne de base y **1400**, montée par masque.
- Pendant la tenue (4,3 → 6,1) : une **aiguille** fine (Encre 3 px, du centre vers le cercle, longueur 250 px) tourne lentement de 3 h vers 12 h (+270°) entre 3,8 et 6,2 s `sine.inOut`, derrière les chiffres (opacité 0.25). Elle rend le temps « vivant ».
- **Transition 6,15 → 6,90** : textes et graduations sortent (masques vers le haut / fondu 0,35 s `power2.in`), les deux points se rétractent ; l'arc **se déroule** (MorphSVG 0,75 s `power3.inOut`, 6,20 → 6,95) en sangle du reformer.

### Temps 3 — Reformer, à six · 6,5 → 9,8 s
Blobs : Sable (300, 1200, R 520) · Sauge (900, 1500, R 300) · Blush (880, 500, R 230).
- **Illustration reformer** (vue de profil, trait Encre 3 px, x 90 → 990, zone y 1060 → 1340), qui se dessine de 6,40 à 7,20 (DrawSVG, stagger 0,05 entre sous-tracés, `power2.out`) :
  - cadre / rail : rectangle arrondi (r 18) x 110–970, y 1230–1270 ;
  - 4 pieds : petits rectangles 40 × 50 à x 130, 330, 750, 930 sous le rail (y 1270–1320) ;
  - barre de pieds (footbar) à gauche : tube en U renversé montant de (150, 1230) à (150, 1110) puis (210, 1110) ;
  - **chariot** : rectangle arrondi (r 14) 260 × 46, rempli Sable `#E6D6C3`, trait Encre, position de repos x 380–640, y 1184–1230 ; appui-tête = petit coussin 70 × 24 à son extrémité droite ;
  - poulies/montants à droite : poteau vertical x 950, y 1230 → 1090, petite poulie cercle r 12 en haut.
  - **La ligne argile** = la sangle + ressort : elle part de la poulie (950, 1090), descend en diagonale vers l'arrière du chariot (640, 1200) — et entre le chariot et la barre de pieds, un ressort en zigzag (6 dents, hauteur 22 px) sous le rail relie x 210 au bord gauche du chariot. Les deux font partie du même path argile.
- **Respiration** 7,20 → 9,50 : le chariot glisse de +0 → −150 px vers la gauche puis revient (une « respiration » complète = 2,2 s, `sine.inOut`) ; le ressort zigzag se comprime puis s'étire en conséquence (recalculer les points du path à chaque frame depuis la position du chariot), la sangle suit l'extrémité du chariot. C'est le cœur « fluide » de la pièce.
- **6,70 / 6,82** : T3-a « À six, » et T3-b « pas plus. » (italic Argile foncée), Cormorant 300 **150 px**, aligné gauche x 90, lignes de base y **560** et **710**, montées par masque 0,8 s `expo.out`.
- **7,10** : **6 pastilles** (cercles Ø 26 px, contour Encre 2 px) en ligne, x 90 + i × 48, centre y 800 ; elles se remplissent de Sauge `#B7C1AB` une à une (stagger 0,10, scale 0.6 → 1 `back.out(2)`) de 7,10 à 7,70.
- **7,40** : T3-sub Manrope 500 **36 px** Encre, x 90, ligne de base y **900**, montée par masque 0,7 s.
- **Transition 9,45 → 10,15** : titre, sous-titre, pastilles sortent vers le haut (masques, `power2.in`, stagger 0,05) ; le reformer s'efface en « undraw » (DrawSVG 100 % → 0 %, 0,5 s, de droite à gauche) ; la ligne argile **se retend** : MorphSVG 0,7 s (9,50 → 10,20, `power3.inOut`) vers le soulignement ondulé du prix.

### Temps 4 — L'offre · 9,8 → 12,8 s
Blobs : Sable (540, 1000, R 500) · Sauge (130, 420, R 250) · Blush (950, 1450, R 300). Le Sable grossit légèrement (R 470 → 500) pendant la tenue : l'offre « respire ».
- **10,00** : T4-pre « Votre 1er cours » Cormorant 300 **96 px**, centré, ligne de base y **680**, masque 0,8 s `expo.out`.
- **10,15** : T4-price « 25 € » Cormorant 300 **380 px**, centré, ligne de base y **1080**. Entrée : masque vertical + letter-spacing 0.06em → −0.02em (1,0 s `expo.out`) — le prix « se resserre » et se pose.
- **Ligne** (fin du morph à 10,20) : soulignement organique sous le prix, de (250, 1150) à (830, 1150) avec une légère onde (cubique, points de contrôle (440, 1128) et (640, 1172)). À partir de 10,20, il « se tend » : l'onde s'aplatit à ±6 px (0,8 s `power2.out`).
- **10,70** : T4-label « OFFRE DÉCOUVERTE » Manrope 600 30 px 0.24em Encre, dans une pastille contour Encre 2 px (padding 18 / 34 px, rayon 999), centrée y **1290**. Apparition : le contour se trace (DrawSVG 0 → 100 %, 0,6 s) puis le texte fond + monte 10 px.
- Tenue 11,3 → 12,4 : scale global du groupe 1 → 1.025, lent.
- **Transition 12,40 → 13,10** : mini-logo du haut et textes sortent (masque vers le haut, 0,35 s `power2.in`, stagger 0,05) ; blobs se recentrent ; la ligne **se courbe en arche** (MorphSVG 12,45 → 13,15, `power3.inOut`) et vient se placer comme l'arche du logo final.

### Carte finale · 12,8 → 16,0 s (tenue lisible ≥ 2,9 s)
Blobs : Sable (540, 820, R 480) · Sauge (220, 1450, R 280) · Blush (880, 1400, R 260). Dérive quasi nulle.
- Symbole logo **600 px de large** (échelle 2.5 de la viewBox 240 × 140 → 600 × 350), centré, haut à y **470**. L'arche = la ligne argile (fin du morph 13,15). 13,10 : la ligne d'eau Encre se trace depuis le centre (scaleX 0 → 1, 0,6 s) ; 13,30 : le point (tête) pop `back.out(2)`.
- **13,35** : « STUDIO PILATES » Manrope 600 **32 px** 0.32em, centré, ligne de base y **900** ; **13,45** : « Rive Gauche » Cormorant 300 italic **120 px**, centré, ligne de base y **1030**. Masques, 0,8 s `expo.out`.
- **13,80** : E-cta « Réservez votre *créneau* » Cormorant 300 **72 px** centré, ligne de base y **1220** (« créneau » italic Argile foncée).
- **14,00** : E-info « Paris 7e · Lien en bio » Manrope 500 **36 px** Encre centré, ligne de base y **1320**.
- **14,10** : E-handle « @studiopilates.rivegauche » Manrope 500 **32 px**, Encre à 70 %, centré, ligne de base y **1390**.
- 14,6 → 16,0 : tout est posé. Seule vie : l'arche « respire » (point de contrôle haut ±4 px, sinusoïde lente de période 3 s) et le grain. **Pas de fondu au noir** à la fin : dernière frame = carte complète.

---

## 6. Notes de mouvement
- Personnalité : **lente, respirée, sans à-coups.** Entrées `expo.out` (0,7–0,9 s), sorties `power2.in` (0,35–0,4 s), morphs et déplacements `power3.inOut` / `sine.inOut`. Aucun `bounce`, aucune secousse. Seuls les petits points utilisent `back.out(2)`.
- Tout texte arrive **par masque** (monte depuis derrière son conteneur), jamais par simple fondu. Stagger 0,08–0,12 s entre lignes.
- **La ligne argile n'est jamais interrompue** : aucune frame sans elle (sauf avant 0 s). C'est la règle n°1 pour les deux développeurs.
- Rythme : accroche vive (tracé + vibration), temps 2 et 3 calmes et mécaniques-fluides, temps 4 posé, fin immobile. Aucune coupe franche : les 4 transitions passent par la ligne.
- Blobs : dérive continue (bruit simplex, amplitude ±18 px en position, ±4 % en rayon) — c'est la « vie » de fond pendant les tenues.

---

## 7. Pistes techniques
- **Stack** : un seul SVG plein cadre 1080 × 1920 (blobs + ligne + reformer + logo) sous des couches HTML pour les textes ; GSAP `timeline({paused:true})`, `render: t => tl.seek(t, false)` ; plugins **MorphSVGPlugin** et **DrawSVGPlugin**.
- **La ligne** : un unique `<path id="line">`. Préparer 5 formes cibles en paths cubiques (`#shape-h`, `#shape-clock`, `#shape-reformer`, `#shape-underline`, `#shape-arch`, invisibles) et morpher de l'un à l'autre. Pour l'état « respiration du reformer » et la vibration de l'accroche, **ne pas utiliser le morph** : dans `render(t)`, après `tl.seek`, si t est dans l'intervalle concerné, réécrire directement l'attribut `d` calculé depuis t (fonctions pures). Même principe pour la respiration de l'arche finale.
- **Blobs** : `simplex-noise` créé avec `KK.rng(216)` comme générateur ; 64 points par blob, rayon = R × (1 + 0.12 × noise3D(cos a, sin a, t × 0.15 + offset)), lissage Catmull-Rom → cubiques ; recalculés dans `render(t)` (déterministe). Positions/rayons par temps interpolés avec `sine.inOut` sur 1,0 s autour de chaque transition.
- **Grain** : `<filter>` feTurbulence + `feColorMatrix` saturate 0, appliqué à un `<rect>` plein cadre, opacité 0.06, `mix-blend-mode: multiply`. Statique.
- **Masques texte** : chaque ligne dans un `span` bloc `overflow:hidden` avec `padding-bottom: 0.12em` (pour ne pas couper les jambages de Cormorant italic) ; animer le `span` intérieur.
- **Letter-spacing animé** (« étirait », « 25 € ») : tween direct sur `letterSpacing` en `em`.
- **Polices** : attendre `document.fonts.ready` dans `KLIPT.ready` avant de construire les SplitText/mesures.
- Typographie : écrire les caractères U+202F / U+00A0 dans le HTML en `&#8239;` / `&nbsp;`.
- `meta.json` : techniques `["gsap", "morphsvg", "drawsvg", "svg-illustration", "simplex-noise"]`, fonts `["Cormorant Garamond", "Manrope"]`, palette `["#F3ECE2", "#E6D6C3", "#B7C1AB", "#C4836A", "#2E2925", "#9A5A43"]`, duration 16.
