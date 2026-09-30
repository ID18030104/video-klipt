# p283 — Théâtre Lumen · « Les Heures Claires » — Direction artistique

**Livrable** : 1 story fixe (still), 1080 × 1920, une seule `<section class="slide">`.
Le brief ne donne ni durée ni nombre de slides : c'est **une image unique** (rendu `stills`), `window.KLIPT = { width: 1080, height: 1920 }`.

---

## 1. Insight & message unique

**Audience** : habitants de Poitiers et alentours, 25–65 ans, abonnés ou curieux du théâtre, étudiants (ville universitaire, prix d'entrée à 12 €). Ils voient la story entre deux autres, pouce en mouvement : ils ont 1,5 s pour capter *quoi, quand, combien*.

**Insight** : on ne va pas au théâtre pour « un spectacle », on y va pour **un soir précis**. Ce qui déclenche la réservation, c'est de voir la date et l'heure comme un rendez-vous.

**Message unique** : *« Les Heures Claires », 10 soirs seulement, du 12 au 21 novembre à 20 h 30.*

## 2. Concept — « L'horloge des soirs »

Le titre parle d'heures et de lumière ; le théâtre s'appelle Lumen. On fusionne les deux dans **une seule image forte** : un **disque de lumière chaude** (à la fois poursuite de scène, lune, soleil) qui est aussi **un cadran d'horloge**. Mais sur ce cadran, les heures sont **les dates des représentations** : 12 en haut (à la place du 12), puis 13, 14… jusqu'à 21 (à la place du 9). Les positions de 10 h et 11 h restent vides (deux petits points éteints) : la série s'arrête là.

Les aiguilles indiquent **8 h 30 → 20 h 30**, l'heure des séances. Le cadran *est* l'information : dates + horaire lus en un coup d'œil, sans texte.

Pourquoi c'est Lumen : un théâtre de 400 places, municipal/indépendant, exigeant mais chaleureux → registre **culturel premium, poétique, sobre**. Nuit d'encre, une seule source de lumière, typographie de caractère. Rien de « promo ».

## 3. Direction artistique

### Palette
| Rôle | Hex | Usage |
|---|---|---|
| Encre (dominant) | `#0D1222` | fond haut |
| Nuit bleue | `#161C38` | fond bas (dégradé) |
| Lumière crème | `#F6EAD0` | titre, textes principaux, cœur du disque |
| Or chaud (accent) | `#E6B45E` | label « NOUVELLE CRÉATION », CTA, fente du logo, point central |
| Bord du disque | `#EFCB84` | périphérie du dégradé du disque |
| Encre cadran | `#141A2E` | chiffres, graduations, aiguilles (sur le disque) |
| Gris lune (secondaire) | `#9AA0B8` | labels du bandeau d'infos, crédit |

Contraste : crème/encre ≈ 15:1 ; gris lune/encre ≈ 7:1 ; encre cadran/disque ≈ 13:1.

### Typographies (2 familles)
- **Cormorant Garamond** (`@fontsource/cormorant-garamond` : `500.css`, `500-italic.css`, `600.css`, `400-italic.css`) — titre, accroche, chiffres du cadran.
- **Manrope** (`@fontsource/manrope` : `500.css`, `600.css`, `700.css`) — logo, labels, infos pratiques, CTA. `font-variant-numeric: tabular-nums` sur les chiffres.

Échelle : 128 (titre) / 46 (chiffres cadran : 40 ; valeurs infos : 42) / 44 (accroche) / 34 (CTA) / 30 (labels, crédit, logo). Rien sous 30 px.

### Langage graphique
- Un seul foyer : le disque-cadran. Tout le reste est typographique, centré sur un axe vertical x = 540, marges 70 px.
- **Ondes de lumière** : 4 cercles concentriques fins autour du disque.
- **Faisceau** : un cône de lumière très discret descend du disque vers un « plateau » (ellipse lumineuse au sol, en bas de l'image) — rappel de la scène.
- Filets fins (1 px) pour le bandeau d'infos, comme une feuille de salle.

### Textures
- Grain SVG `feTurbulence` (`baseFrequency 0.85`, `numOctaves 2`, `stitchTiles stitch`) en overlay plein cadre, `mix-blend-mode: overlay`, opacité **0,07**.
- Un second grain plus fin sur le disque seul (opacité 0,10, `mix-blend-mode: multiply`) pour lui donner un aspect papier/lune, pas un aplat vectoriel.
- Vignettage : dégradé radial du bord `rgba(0,0,0,.35)` → transparent à 70 %.

### Logo Théâtre Lumen
Symbole : **cercle** de 48 px, contour crème 2,5 px, avec en son centre une **fente verticale** or `#E6B45E` (rectangle 6 × 30 px, coins arrondis 3 px) — une porte entrouverte / un rideau fendu de lumière. Wordmark à droite, espacement 18 px : « THÉÂTRE LUMEN » Manrope 700, 30 px, `letter-spacing: 0.24em`, crème. Lockup centré horizontalement.

---

## 4. Texte final (français, exact)

Utiliser des espaces insécables (`&nbsp;` / U+00A0) là où indiqué par `⍽`, l'apostrophe typographique `’`, les capitales accentuées.

| Élément | Texte exact |
|---|---|
| Logo | `THÉÂTRE LUMEN` |
| Label | `NOUVELLE CRÉATION` |
| Titre ligne 1 | `Les Heures` |
| Titre ligne 2 (italique) | `Claires` |
| Accroche | `Dix soirs où la nuit s’éclaire.` |
| Crédit | `Texte et mise en scène⍽: Clémence Arnaud` |
| Label infos 1 / valeur | `Novembre` / `12⍽–⍽21` (tiret demi-cadratin U+2013) |
| Label infos 2 / valeur | `Horaire` / `20⍽h⍽30` |
| Label infos 3 / valeur | `Tarifs` / `12 à 28⍽€` |
| CTA | `Réservez sur theatre-lumen.fr` |
| Pied (zone basse, décoratif) | `Poitiers · 400⍽places` |
| Chiffres du cadran | `12 13 14 15 16 17 18 19 20 21` |

(Clémence Arnaud est une metteuse en scène fictive, comme la pièce.)

---

## 5. Mise en page précise (1080 × 1920)

Zones sûres : rien d'important au-dessus de y = 220 ni sous y = 1540 ; marges latérales 70 px. Toutes les coordonnées = haut de la boîte, sauf mention.

**Fond** : `linear-gradient(180deg, #0D1222 0%, #0F1428 45%, #161C38 100%)` + vignettage + grain.

1. **Logo** — top 236, hauteur 48, centré.
2. **Halo** — gradient radial centré (540, 620) : `rgba(246,234,208,.30)` à r 240 → `rgba(230,180,94,.10)` à r 360 → 0 à r 540.
3. **Ondes** — cercles centrés (540, 620), stroke `#F6EAD0` 1 px, rayons / opacités : 262 / .16, 296 / .11, 340 / .07, 396 / .04.
4. **Faisceau** — trapèze SVG : sommet de largeur 300 px à y 780 (x 390–690), base de largeur 860 px à y 1760 (x 110–970), rempli d'un gradient vertical `rgba(246,234,208,.07)` → `rgba(246,234,208,0)` ; placé **derrière** tous les textes. Ellipse de plateau : centre (540, 1760), rayons 430 × 46, `rgba(230,180,94,.14)`, `filter: blur(18px)`.
5. **Disque-cadran** — centre (540, 620), r 220 (y 400–840).
   - Remplissage : radial `#FFF6E0` au centre → `#F6EAD0` à 60 % → `#EFCB84` à 100 %. Ombre externe douce `0 0 60px rgba(239,203,132,.45)`.
   - 60 graduations minutes : de r 204 à r 212, 1,5 px, `#141A2E` opacité .30. Graduations d'heures (12 positions) : r 196 → r 212, 3 px, opacité .75.
   - Chiffres (Cormorant Garamond 600, 40 px, `#141A2E`, centrés sur le point) à r 166, position k = 0…9 → angle θ = k × 30° dans le sens horaire depuis le haut (`x = 540 + 166·sin θ`, `y = 620 − 166·cos θ`) : 12 (0°), 13 (30°), 14 (60°), 15 (90°), 16 (120°), 17 (150°), 18 (180°), 19 (210°), 20 (240°), 21 (270°).
   - Positions 300° et 330° : petit point plein 8 px, `#141A2E` opacité .25 (pas de chiffre).
   - Aiguille des heures : longueur 112, largeur 10, bouts arrondis, `#141A2E`, angle **255°** (entre 20 et 21 → 20 h 30).
   - Aiguille des minutes : longueur 176, largeur 5, `#141A2E`, angle **180°** (vers 18 → « 30 »). Les deux dépassent de 22 px à l'arrière du centre.
   - Ombre portée des aiguilles : décalage (5, 7), `rgba(20,26,46,.20)`, flou 3 px — effet cadran solaire.
   - Moyeu : cercle 20 px `#141A2E`, point central 7 px `#E6B45E`.
   - Grain « papier » sur le disque (voir Textures).
6. **Label** — top 882, `NOUVELLE CRÉATION`, Manrope 600, 30 px, `letter-spacing: .32em`, `#E6B45E`, centré (compenser le tracking final avec `padding-left: .32em`).
7. **Titre** — Cormorant Garamond, 128 px, `line-height: .92`, `#F6EAD0`, centré, `letter-spacing: -0.01em`.
   - « Les Heures » : 500 romain, top 930.
   - « Claires » : 500 italique, ligne suivante (≈ top 1048). Fin du bloc ≈ 1166.
8. **Accroche** — top 1184, Cormorant Garamond 400 italique, 44 px, `#F6EAD0` opacité .92.
9. **Crédit** — top 1246, Manrope 500, 30 px, `#9AA0B8`.
10. **Bandeau d'infos** — filet haut à y 1306, filet bas à y 1450 (1 px, `rgba(246,234,208,.28)`, x 70–1010). Trois cellules égales (313 px) séparées par 2 filets verticaux (y 1330–1426, même couleur).
    - Label : top 1330, Manrope 500, 30 px, `#9AA0B8`.
    - Valeur : top 1374, Manrope 700, 42 px, `#F6EAD0`, `tabular-nums`.
11. **CTA** — top 1478, `Réservez sur theatre-lumen.fr`, Manrope 600, 34 px, `#E6B45E`, souligné par un filet or 2 px à 8 px sous la ligne de base, largeur = texte.
12. **Pied décoratif** (zone basse, sous le plateau lumineux) — top 1800, `Poitiers · 400 places`, Manrope 500, 30 px, `#9AA0B8` opacité .7, `letter-spacing: .08em`.

Hiérarchie de lecture : disque (dates + heure) → titre → bandeau infos → CTA.

---

## 6. Motion

Aucune : pièce fixe. (Si une version vidéo était demandée un jour : les aiguilles tournent de 12 h à 8 h 30 pendant que le disque s'allume, puis le texte monte par masques.)

## 7. Approche technique

- `index.html` unique, une `<section class="slide">` de 1080 × 1920, `body { margin:0; overflow:hidden; background:#0D1222 }`.
- Fonts via `<link rel="stylesheet" href="../../node_modules/@fontsource/...">` (fichiers listés §3) ; attendre `document.fonts.ready` n'est pas nécessaire pour un still mais conseillé si un script calcule des positions.
- Disque, ondes, faisceau, graduations, chiffres et aiguilles : **un seul SVG inline** 1080 × 1920 en arrière-plan (`position:absolute; inset:0`), chiffres en `<text text-anchor="middle" dominant-baseline="central">`. Générer graduations/chiffres par un petit script au chargement (déterministe) ou en dur.
- Textes HTML positionnés en absolu avec les `top` donnés, `width:100%; text-align:center`.
- Grain : `<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>` sur un `<rect>` plein cadre.
- Espaces insécables : `&nbsp;` dans le HTML.
- Rendu : `node tools/render.mjs stills pieces/p283` → `slides/slide-01.png` + `sheet.jpg`. Vérifier : chiffres du cadran lisibles et non tronqués, aiguille des heures bien entre 20 et 21, aucun texte clé sous y 1540.
- `meta.json` : kind `story`, format `1080x1920`, duration `null`, slides `1`, fonts `["Cormorant Garamond","Manrope"]`, palette `["#0D1222","#161C38","#F6EAD0","#E6B45E","#141A2E"]`, techniques `["svg-illustration","css-typography","svg-grain"]`, title « Les Heures Claires — story ».
