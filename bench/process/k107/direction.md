# k107 — Maison Castel, Barbier · « Le cadran du rasage »

Deliverable: vidéo 1080 × 1920, **22,0 s**, 30 fps, sans son (Reels + TikTok, lu en muet). Langue : français.

---

## 1. Audience insight & message unique

**Qui scrolle :** hommes 25–55 ans de la Croix-Rousse. Ils se rasent seuls, vite, au rasoir 5 lames, le matin, avec le feu du rasoir en prime. Ils connaissent le barbier de nom, y vont pour la coupe, mais n'ont jamais « osé » le rasage — ils l'imaginent comme un truc de film.

**Insight :** le rasage chez soi est une corvée de 3 minutes ; le rasage à l'ancienne, c'est 40 minutes où l'on ne fait *rien* d'autre que se faire chouchouter. Ce qu'on vend, ce n'est pas une barbe nette, c'est du **temps pour soi**, rythmé par un vrai rituel.

**Le message unique :** *Le Rasage à l'ancienne : 40 minutes de rituel, 35 €, réservez en ligne.*

Registre : artisanal / old-school chaleureux, jamais hipster criard. Solide, lisible, un peu de laiton qui brille.

---

## 2. Concept — « Le cadran du rasage »

Un **cadran de 40 minutes** (comme une vieille horloge de salon, graduée de 0 à 40) sert de fil rouge. Le **coupe-chou**, qui s'ouvre en gros plan dans le hook, devient l'**aiguille-curseur** qui fait le tour du cadran : chaque quart de tour = une étape du rituel (serviette chaude, blaireau, coupe-chou, baume). Quand le cadran est complet, une « serviette chaude » crème monte et révèle le prix, puis une bande de **poteau de barbier** (rayures bordeaux / crème / laiton) balaie l'écran pour la carte de fin.

Pourquoi ça ne peut appartenir qu'à cette marque : le temps (40 min), l'objet signature (coupe-chou), le code visuel du métier (poteau rayé, plaque émaillée, laiton) et l'ancrage « depuis 2011 / Croix-Rousse ». On montre le soin *comme un rituel qui prend son temps*, ce qui est exactement l'argument.

---

## 3. Direction artistique

### Palette (5 couleurs, discipline stricte)
| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Dominante (fond) | Encre | `#17120F` | fond de toutes les scènes sauf le prix |
| Texte principal | Crème | `#EFE3CC` | titres, traits d'illustration, panneau « serviette » |
| Accent | Laiton | `#C0924A` | anneau de progression, chiffres, filets, italiques-clés |
| Secondaire | Bordeaux | `#7A1E22` | prix « 35 € », manche du rasoir, rayures du poteau |
| Ombre chaude | Noyer | `#3A2A20` | halo de lumière, ombres, graduations mineures |

Contrastes : crème/encre ≈ 15:1, laiton/encre ≈ 6,9:1, bordeaux/crème ≈ 8:1, encre/crème ≈ 15:1. Pas d'autre couleur. Aucun dégradé violet/bleu.

### Typographies (2 familles)
- **DM Serif Display** 400 + 400-italic (`@fontsource/dm-serif-display/index.css` et `/400-italic.css`) — titres, prix, nom de marque.
- **Barlow Condensed** 500, 600, 700 (`/500.css`, `/600.css`, `/700.css`) — surtitres en capitales espacées, infos pratiques, chiffres du cadran.

Échelle (canvas 1080 px de large) :
| Élément | Police | Taille | Interlettrage |
|---|---|---|---|
| Prix « 35 € » | DM Serif Display | 360 px | -0,02 em |
| Chiffre central « 40 » | DM Serif Display | 220 px | -0,02 em |
| Hook / titres | DM Serif Display (roman + italique) | 132–150 px | -0,01 em, interligne 1,0 |
| Titre d'étape | DM Serif Display | 116 px | -0,01 em |
| Sous-ligne d'étape | DM Serif Display italic | 52 px | 0 |
| Surtitres (NOUVEAU SOIN, 01 / 04…) | Barlow Condensed 600, capitales | 34 px | 0,28 em |
| Infos pratiques | Barlow Condensed 500 | 38 px | 0,04 em |
| URL | Barlow Condensed 700 | 64 px | 0,02 em |
| Chiffres du cadran | Barlow Condensed 500 | 30 px | 0,1 em |

Aucun texte < 30 px.

### Langage graphique
- **Illustration au trait** crème, `stroke-width` 5 px, `stroke-linecap: round`, sans remplissage (sauf petits aplats laiton), style gravure simplifiée — dessinée au trait avec DrawSVG.
- **Le coupe-chou** (objet héros, SVG construit) : manche (« chasse ») en bordeaux `#7A1E22` avec liseré laiton 3 px et 2 goupilles laiton (cercles r=7) ; lame en crème avec dégradé linéaire crème → `#C9BBA2` et un filet de tranchant laiton 2 px ; talon/queue de lame cranté (3 petites encoches). Pivot = goupille du haut.
- **Le cadran** : cercle de graduation r = 270 px, centre (540, 720). 40 graduations : tous les 5 min graduation majeure (28 px, laiton, 3 px) ; les autres mineures (12 px, crème à 35 %, 2 px). Chiffres « 0 », « 10 », « 20 », « 30 » aux positions 12 h / 3 h / 6 h / 9 h, placés à r = 222 px, Barlow Condensed 500 30 px, crème 70 %. Anneau de progression laiton à r = 305 px, `stroke-width` 10, extrémités arrondies ; piste de fond du même anneau en Noyer `#3A2A20`. Découpage en 4 segments séparés par 3° de vide : 0→10 min (0°→90°), 10→20 (90°→180°), 20→35 (180°→315°), 35→40 (315°→360°). Départ à 12 h, sens horaire.
- **Bande « poteau de barbier »** : rayures diagonales à 35°, largeur 56 px, alternance bordeaux / crème / laiton / crème, bande de 240 px de haut.
- **Filets** : laiton 2 px, courts (120 px), centrés — ponctuation typographique de vieille enseigne.

### Textures
- **Grain** global : SVG `feTurbulence` (type fractalNoise, baseFrequency 0.85, numOctaves 2, seed fixe 7) en overlay `mix-blend-mode: overlay`, opacité 7 %, au-dessus de tout.
- **Lumière de miroir** : halo radial Noyer `#3A2A20` → transparent, centré (540, 700), rayon 900 px, sur le fond encre (comme la lampe au-dessus du fauteuil).
- **Vignette** : radial transparent → noir 45 % sur les bords.
- Sur le panneau crème du prix : un léger papier (même turbulence, 5 %) + 2 plis de serviette (bandes horizontales de 90 px, dégradé vertical crème → `#E2D4B9` → crème, opacité 60 %) aux y = 560 et y = 1380.

### Logo / marque
- **Badge émaillé ovale→rond** Ø 380 px : anneau extérieur laiton 6 px, anneau intérieur laiton 2 px (écart 14 px), fond intérieur bordeaux `#7A1E22`. Texte sur chemin circulaire (Barlow Condensed 600, 30 px, capitales, interlettrage 0,3 em, crème) : en haut « MAISON CASTEL », en bas « CROIX-ROUSSE · 2011 », séparés par deux petits losanges laiton à 3 h et 9 h. Au centre : le coupe-chou ouvert, en crème au trait, incliné à -30°.
- **Wordmark** : « Maison Castel » en DM Serif Display 120 px crème ; dessous « BARBIER · DEPUIS 2011 » Barlow Condensed 600 34 px laiton, interlettrage 0,32 em.
- Présence de marque dès le hook : petite signature « MAISON CASTEL — BARBIER » Barlow Condensed 600, 30 px, laiton, interlettrage 0,3 em, centrée à y = 260, visible de 0,0 à 16,2 s.

---

## 4. Copy finale (chaînes exactes)

Typographie : espace insécable fine (U+202F) avant `: ; ! ?` et dans les « » ; espace insécable (U+00A0) entre chiffre et unité (`35 €`, `40 min`, `9 h`) ; apostrophe typographique `’` partout.

**Signature (haut d'écran, 0–16,2 s)**
- `MAISON CASTEL — BARBIER`

**Scène 1 — Hook**
- Ligne 1 : `On a ressorti`
- Ligne 2 (italique, laiton) : `le coupe-chou.`

**Scène 2 — Titre**
- Centre du cadran : `40` + dessous `MIN`
- Surtitre : `NOUVEAU SOIN`
- Titre ligne 1 : `Le Rasage`
- Titre ligne 2 (italique, laiton) : `à l’ancienne`

**Scène 3 — Les 4 étapes**
| # | Surtitre (Barlow, laiton) | Titre (DM Serif, crème) | Sous-ligne (DM Serif italic, crème 80 %) |
|---|---|---|---|
| 1 | `01 / 04 · 10 MIN` | `Serviette chaude` | `Pour ouvrir la peau.` |
| 2 | `02 / 04 · 10 MIN` | `Blaireau` | `Mousse montée à la main.` |
| 3 | `03 / 04 · 15 MIN` | `Coupe-chou` | `Au plus près, sans irriter.` |
| 4 | `04 / 04 · 5 MIN` | `Baume` | `Et vous repartez neuf.` |

(10 + 10 + 15 + 5 = 40 min, cohérent avec le cadran.)

**Scène 4 — Prix (panneau crème)**
- Surtitre : `LE RASAGE À L’ANCIENNE`
- Prix : `35 €` (bordeaux)
- Durée : `40 min` (italique, encre)
- Liste (Barlow 500, 38 px, 2 lignes) : `Serviette chaude · Blaireau` / `Coupe-chou · Baume`

**Scène 5 — Carte de fin**
- Badge (textes sur cercle) : `MAISON CASTEL` / `CROIX-ROUSSE · 2011`
- Wordmark : `Maison Castel`
- Sous-wordmark : `BARBIER · DEPUIS 2011`
- CTA : `Réservez votre fauteuil`
- URL : `maisoncastel.fr`
- Adresse : `12 rue d’Austerlitz · Lyon 4e`
- Horaires : `Du mardi au samedi · 9 h – 19 h`

Relecture faite : pas de majuscule accentuée manquante (« À » dans le surtitre du prix), « coupe-chou » avec trait d'union, « Lyon 4e » (4e sans exposant forcé ; si possible `4<sup>e</sup>` à 0,6 em).

---

## 5. Storyboard (22,0 s)

Zones sûres : aucun texte clé au-dessus de y = 220 ni sous y = 1540, marges latérales ≥ 90 px. Toute la mise en page est centrée horizontalement (x = 540).

### Scène 1 — Hook « On a ressorti le coupe-chou. » · 0,00 → 3,00 s
- **Frame 0** (déjà en mouvement) : fond encre + halo + grain. Coupe-chou géant centré, pivot à (540, 640), manche à la verticale vers le bas (longueur 520 px), lame **déjà entrouverte à 25°**. Signature en haut visible.
- 0,00 → 1,10 : la lame pivote de 25° à 185° (ouverte, pointant vers le haut-droite), `back.out(1.2)`. Ensemble du rasoir : rotation globale de -8° → 0°, scale 1,06 → 1.
- 1,15 → 1,55 : **reflet** : une bande crème 30 % oblique (largeur 60 px, flou 6 px), masquée par la forme de la lame, traverse la lame de gauche à droite, `power2.inOut`.
- 0,25 s : « On a ressorti » (132 px, crème, y ≈ 1150) monte depuis un masque, mot par mot, stagger 0,08, 0,6 s, `expo.out`.
- 0,55 s : « le coupe-chou. » (150 px, italique laiton, y ≈ 1300) idem.
- Pendant le hold (1,6 → 2,8) : scale lente du rasoir 1 → 1,03 ; halo respire (opacité 0,85 → 1).

**Transition 1 → 2 (2,75 → 3,45 s) — match cut rasoir → aiguille :**
- 2,75 → 3,05 : textes sortent vers le haut dans leurs masques, `power2.in`, 0,3 s, stagger 0,05.
- 2,85 → 3,45 : le rasoir se replie à ~120°, réduit à scale 0,22 et vole (MotionPath, courbe) jusqu'au point 12 h de l'anneau (540, 415), en s'orientant tangent à l'anneau (lame vers la droite = sens horaire). `power3.inOut`.
- 3,00 → 3,90 : le cercle de graduation se dessine dans le sens horaire (DrawSVG 0 → 100 %), les graduations apparaissent en stagger 0,012 s (scaleY 0 → 1 depuis l'extérieur) ; piste Noyer de l'anneau dessinée en même temps ; chiffres 0/10/20/30 en fondu 0,3 s à la fin.

### Scène 2 — Titre « Le Rasage à l’ancienne » · 3,45 → 5,40 s
- 3,50 : « 40 » (220 px) apparaît au centre du cadran (scale 0,85 → 1 + opacité, 0,5 s, `expo.out`), « MIN » (Barlow 600, 40 px, laiton, 0,3 em) dessous.
- Sous le cadran : « NOUVEAU SOIN » (y ≈ 1110) à 3,55 ; « Le Rasage » (120 px, y ≈ 1200) à 3,65 ; « à l’ancienne » (120 px italique laiton, y ≈ 1325) à 3,75 — montées masquées, 0,6 s, `expo.out`.
- 5,10 → 5,40 : sortie — titre monte dans ses masques (`power2.in`) ; « 40 / MIN » scale 1 → 0,8 + opacité 0.

### Scène 3 — Le rituel en 4 étapes · 5,40 → 16,20 s (4 × 2,70 s)
Mise en page fixe pour les 4 étapes :
- Cadran en haut (centre 540, 720).
- **Illustration** au centre du cadran, dans un carré de 300 × 300 px centré sur (540, 720).
- Surtitre y ≈ 1110, titre y ≈ 1215 (116 px), sous-ligne y ≈ 1330 (52 px).

Pour chaque étape *n* démarrant à T :
- T + 0,00 → 1,60 : l'anneau laiton se remplit sur son segment, le coupe-chou-curseur glisse le long de l'anneau (toujours tangent), `power2.inOut`. Le segment rempli reste allumé ensuite.
- T + 0,05 → 0,85 : illustration dessinée au trait (DrawSVG 0 → 100 %, stagger 0,06 entre les tracés), `power2.out`.
- T + 0,10 surtitre / T + 0,20 titre / T + 0,32 sous-ligne : montées masquées 0,55 s `expo.out` (titre par mot, stagger 0,06).
- Hold vivant jusqu'à T + 2,40 (voir illustrations).
- T + 2,40 → 2,70 : textes sortent vers le haut (`power2.in`, 0,3 s) ; illustration scale 1 → 0,9 + opacité 0 (0,25 s). L'entrée suivante chevauche de 0,05 s.

Étapes :
1. **5,40 s — Serviette chaude** (segment 0°→90°). Illustration : serviette roulée vue de profil (rectangle arrondi 220 × 90 avec spirale à droite), 3 volutes de vapeur au-dessus (chemins en S, 110 px de haut). Hold : les volutes ondulent (translation X = 6·sin(2π·0,8·t + phase), opacité 0,5 ↔ 0,9) et montent de 10 px en boucle déterministe.
2. **8,10 s — Blaireau** (segment 90°→180°). Illustration : blaireau (manche galbé + dôme de poils avec 5 petits traits internes), à côté un bol. Hold : 6 bulles (cercles r 6–14 px, trait crème) sortent du bol et grossissent/disparaissent en boucle (positions via `KK.rng(11)` générées au chargement).
3. **10,80 s — Coupe-chou** (segment 180°→315°, le plus long : 1,6 s aussi, donc un peu plus rapide visuellement). Illustration : profil de mâchoire/joue simplifié (1 tracé : oreille → joue → menton), recouvert d'un contour de mousse « nuageux » (festons). Hold : de 11,5 à 12,6 s, un masque linéaire balaie de gauche à droite et **efface la mousse** en révélant une ligne de joue nette ; un petit trait laiton suit le front de balayage (le passage de lame).
4. **13,50 s — Baume** (segment 315°→360°). Illustration : flacon d'apothicaire (corps arrondi, bouchon, étiquette rectangulaire avec un « C » en DM Serif 60 px à l'intérieur). Hold : 2 gouttes laiton tombent en alternance (y +40 px, opacité 1 → 0, boucle 0,9 s).

**Transition 3 → 4 (16,00 → 16,80 s) — « la serviette chaude » :**
- 16,00 → 16,25 : l'anneau complet fait une **pulsation** : `stroke-width` 10 → 20 → 12 et un halo laiton (drop-shadow 0 0 24px `#C0924A`) s'allume puis retombe. Le curseur-rasoir arrive à 12 h pile.
- 16,20 → 16,80 : un **panneau crème** monte du bas (translateY 1920 → 0), `expo.inOut`, avec un bord supérieur légèrement ondulé (bord en SVG, amplitude 14 px) et une ombre portée noyer vers le haut — comme une serviette qu'on déplie. Il couvre tout l'écran (cadran et signature disparaissent dessous).

### Scène 4 — Le prix · 16,80 → 18,80 s
Sur fond crème (papier + 2 plis). Cadre de plaque émaillée : double filet encre inséré à 90 px des bords latéraux, de y = 330 à y = 1500 (extérieur 3 px, intérieur 1 px à 14 px d'écart), coins coupés à 45° (24 px).
- 16,60 → 17,10 : les filets du cadre se dessinent (DrawSVG, depuis le centre haut vers les deux côtés).
- 16,75 : « LE RASAGE À L’ANCIENNE » (Barlow 600, 38 px, encre, 0,28 em) y ≈ 460, montée masquée.
- 16,85 : **« 35 € »** (360 px, bordeaux) centré y ≈ 820 : effet tampon — scale 1,18 → 1, opacité 0 → 1, 0,45 s `back.out(1.6)`, léger flou 8 px → 0.
- 17,05 : filet laiton 120 px sous le prix (y ≈ 1030) se déploie depuis le centre.
- 17,10 : « 40 min » (DM Serif italic 90 px, encre) y ≈ 1130.
- 17,25 : liste sur 2 lignes (Barlow 500, 38 px, encre 80 %) y ≈ 1290 et 1345, stagger 0,08.
- Hold jusqu'à 18,60 : tout le contenu scale 1 → 1,02.

**Transition 4 → 5 (18,55 → 19,25 s) — bande du poteau de barbier :**
- Une bande rayée (240 px de haut, rayures diagonales 35°, 56 px, bordeaux / crème / laiton / crème) traverse l'écran de haut en bas (y -240 → 1920), `power2.inOut`, 0,7 s. Les rayures défilent aussi latéralement dans la bande (translateX 0 → 224 px) comme un poteau qui tourne.
- Au-dessus de la bande : panneau crème ; en dessous (déjà passé) : carte de fin sur encre. Réalisation : clip-path `inset()` du panneau crème synchronisé sur le bord bas de la bande.

### Scène 5 — Carte de fin · 18,80 → 22,00 s (hold lisible ≥ 2,5 s)
Fond encre + halo + grain.
- 19,00 : **badge** Ø 380 px centré en (540, 560) : anneaux laiton dessinés (DrawSVG, 0,6 s), fond bordeaux en scale 0,9 → 1, textes circulaires en fondu, coupe-chou central dessiné au trait. Hold : le texte circulaire tourne lentement de 0° → 10° jusqu'à 22 s (linéaire, seule dérive continue autorisée).
- 19,30 : « Maison Castel » (120 px, crème) y ≈ 870, montée masquée par mot.
- 19,42 : « BARBIER · DEPUIS 2011 » (34 px laiton) y ≈ 960.
- 19,50 : filet laiton 120 px y ≈ 1030.
- 19,60 : « Réservez votre fauteuil » (DM Serif italic 64 px, crème) y ≈ 1120.
- 19,72 : « maisoncastel.fr » (Barlow 700, 64 px, laiton) y ≈ 1210 dans un cadre rectangulaire laiton 2 px (padding 18 × 40 px) ; à 20,4 s un petit reflet crème 25 % traverse le cadre une fois.
- 19,85 : « 12 rue d’Austerlitz · Lyon 4e » (Barlow 500, 38 px, crème 85 %) y ≈ 1340.
- 19,95 : « Du mardi au samedi · 9 h – 19 h » (Barlow 500, 38 px, crème 85 %) y ≈ 1400.
- 20,00 → 22,00 : hold. Groupe complet scale 1 → 1,025 (`none` ease sur la durée), grain, rotation du badge. Rien ne sort : la dernière frame est la carte complète (elle sert de poster).

---

## 6. Notes de motion

- Personnalité : **posée, précise, artisanale** — comme un geste de barbier : un départ net, puis de la lenteur. Entrées `expo.out` / `power3.out`, sorties `power2.in` (courtes, 0,25–0,3 s), déplacements `power2.inOut` / `power3.inOut`. Seules exceptions linéaires : rotation du badge, dérive de scale, défilement des rayures.
- Rythme : rapide (hook 3 s) – rapide (titre 2 s) – régulier (4 × 2,7 s, métronome du cadran) – impact (prix « tampon ») – calme (fin 3,2 s).
- Les textes n'apparaissent **jamais** en simple fondu : toujours des montées depuis un masque (`overflow:hidden` sur la ligne, `yPercent 110 → 0`).
- Le coupe-chou est l'élément continu du film : de 0 à 16,2 s il est toujours à l'écran (héros, puis curseur). Ne jamais le faire disparaître/réapparaître.
- Pendant les holds, toujours un micro-mouvement (vapeur, bulles, mousse, gouttes, respiration du halo).

---

## 7. Approche technique

- Un seul `index.html` ; tout en **SVG inline** (viewBox 0 0 1080 1920) pour le cadran, le rasoir, les illustrations, le badge, la bande rayée (`<pattern>` rayé avec `patternTransform="rotate(35)"`), + HTML pour les textes.
- GSAP (`../../node_modules/gsap/dist/gsap.min.js`) + `DrawSVGPlugin`, `MotionPathPlugin`, `SplitText` (masques ligne/mot). Une seule `gsap.timeline({paused:true})` ; `window.KLIPT = { width:1080, height:1920, fps:30, duration:22, ready: document.fonts.ready, render: t => { tl.seek(t, false); } }`.
- Micro-mouvements continus (vapeur, bulles, gouttes, respiration) : les calculer dans `render(t)` après le `seek`, à partir de `t` uniquement (sin/cos), ou les placer dans la timeline avec des `repeat` finis. Positions aléatoires via `KK.rng(seed)` (`../../lib/klipt-kit.js`) générées une fois au chargement.
- Curseur-rasoir le long de l'anneau : plus simple que MotionPath — dans `render(t)`, calculer l'angle θ(t) (piloté par un objet proxy `{deg}` tweené dans la timeline) puis `x = 540 + 305·sin θ`, `y = 720 − 305·cos θ`, `rotate(θ)`. L'arc laiton : `stroke-dasharray` / `stroke-dashoffset` du cercle r = 305 (circonférence ≈ 1916 px) avec `rotate(-90deg)` pour partir de 12 h ; les 4 segments sont 4 cercles distincts avec leur propre dasharray pour gérer les écarts de 3°.
- Effacement de la mousse (étape 3) : `<mask>` avec un `<rect>` dont `x` est tweené.
- Panneau « serviette » : `<div>` crème plein écran avec `transform: translateY()` et un SVG de bord ondulé en haut ; transition vers la fin via `clip-path: inset(Ypx 0 0 0)` synchronisé à la position de la bande rayée.
- Grain : un `<svg>` plein écran avec `feTurbulence` statique (seed 7), `pointer-events:none`, opacité 0,07, `mix-blend-mode: overlay`.
- Polices : charger `@fontsource/dm-serif-display/index.css`, `/400-italic.css`, `@fontsource/barlow-condensed/500.css`, `/600.css`, `/700.css` ; attendre `document.fonts.ready` avant `SplitText`.
- Vérifications recommandées : frames à 0,5 / 2,0 / 3,3 / 4,5 / 7,5 / 12,0 / 17,8 / 21,5 s.

### meta.json attendu
```json
{ "id": "k107", "brand": "Maison Castel — Barbier", "sector": "Barbier / coiffeur de quartier",
  "kind": "video", "format": "1080x1920", "duration": 22, "slides": null,
  "title": "Le cadran du rasage à l’ancienne",
  "concept": "Le coupe-chou s’ouvre puis devient l’aiguille d’un cadran de 40 minutes qui égrène les 4 gestes du rituel, avant un prix façon plaque émaillée et une carte de fin balayée par un poteau de barbier. Encre, crème, laiton, bordeaux.",
  "techniques": ["gsap", "svg-illustration", "drawsvg", "splittext", "masks", "svg-grain"],
  "fonts": ["DM Serif Display", "Barlow Condensed"],
  "palette": ["#17120F", "#EFE3CC", "#C0924A", "#7A1E22", "#3A2A20"],
  "copy_language": "fr" }
```
