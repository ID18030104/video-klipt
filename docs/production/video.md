**Réponse courte : oui.** Une vidéo de 15 s finie, avec des images réelles en mouvement plus le texte et la marque exacts de Klipt, revient à **0,94 $** avec le meilleur montage testé, et à 1,47 $ avec Kling 3.0. Le rush seul coûte **0,27 $** (Hailuo 2.3, à partir de 3 images) ou **0,69 $** (Kling 3.0).

### 6.1 Protocole
- **Brief commun** : une boulangerie au levain lyonnaise (Maison Brune), un Reel 9:16 de 15 s en 3 plans.
  - Plan 1 : les mains qui grignent la miche à la lame, gros plan, farine en suspension.
  - Plan 2 : le four à bois, le boulanger sort les pains à la pelle.
  - Plan 3 : une cliente reçoit sa baguette au comptoir.
- Ce brief couvre les cas difficiles : mains, visages, feu et vapeur, lumière.
- **Consignes** : film chaud et réaliste, sans texte, logo ni filigrane. Le son est coupé quand c'est possible, car Klipt ajoute la musique au montage.
- **Six approches** au même prompt, via l'API Higgsfield :
  - cinq modèles en « texte → vidéo » d'un seul tenant ;
  - une chaîne « images → vidéo » : 3 images Marketing Studio (2k low), animées plan par plan par Hailuo 2.3, puis montées.
- **Prix** : le champ `usd` de l'endpoint d'estimation, qui est le montant réellement facturé, remise comprise. Le champ `discount` indique seulement l'économie réalisée.

### 6.2 Résultats (rush 15 s, 9:16)

| Modèle (endpoint) | Coût 15 s | Résolution | Temps de génération | Qualité observée |
|---|---|---|---|---|
| **Hailuo 2.3** à partir de 3 images Marketing Studio (`minimax/hailuo-2.3/standard/image-to-video`, 3 × 6 s coupés à 5 s) | **0,27 $** (images 3 × 0,019 $ + plans 3 × 0,07 $) | 768×1358 | ≈ 7–8 min (images puis plans, en parallèle) | **La plus authentique** : lumière de film, feu et vapeur crédibles, visages naturels, direction artistique contrôlée image par image. Petit défaut : une main de vendeuse qui disparaît. |
| **Kling 3.0 std** (`kling-video/v3.0/std/text-to-video`, `multi_shots`, son coupé) | **0,69 $** | 720×1280 | ≈ 3 min | Le plus fidèle au découpage demandé (3 plans nets aux bonnes durées), aucun texte parasite. Aspect un peu « banque d'images » (cliente en tailleur), geste de la lame étrange. |
| **PixVerse v6** (`pixverse/v6/text-to-video`, 720p, sans son) | 0,57 $ | 720×1280 | ≈ 3 min | Très belle lumière. La miche est tranchée au couteau au lieu d'être grignée, et une enseigne apparaît en miroir dans la vitrine. |
| **Wan 2.7** (`wan/v2.7/text-to-video`, 720p, son inclus) | 0,75 $ | 720×1280 | ≈ 18 min | Belles matières. Enseigne « LYON » illisible, scène de comptoir moins juste, génération lente. |
| **MiniMax H3** (`minimax/h3/text-to-video`, 2K, son inclus) | 1,37 $ | **1440×2560** | ≈ 13 min | Seul modèle en 2K natif, 3 plans propres. Geste au couteau, génération lente. |
| **Happy Horse** (`alibaba/happy-horse/text-to-video`, 720p, son inclus) | 1,47 $ | 720×1280 | ≈ 2 min | Le plus « cinéma » (four en briques, flammes), mais le texte de la vitrine est déformé. C'est le plus cher. |

**Non testés, pour raison de prix :**

| Modèle | Coût estimé pour 15 s | Tarification |
|---|---|---|
| Seedance 2.0 et 2.5 | ≈ 4,50 $ en 720p avant remise | au token |
| Cinema Studio 4.0 | ≈ 6,90 $ | au token |
| Kling 3.0 Turbo | 0,92 $ en 720p | — |
| Hailuo 2.3 en texte → vidéo | 0,14 $ les 10 s | format paysage uniquement |
| LTX 2.5 | 0,90–1,20 $ | 10 s au maximum |

Les images de comparaison sont dans `bench/results/video-models-compare.jpg`, et les rushs, planches et coûts dans `bench/video/`.

### 6.3 Vidéos finies : clip IA + couche Claude (« mode clip » du prompt hybride)
Un agent Sonnet 5.5 a reçu le rush et le brief client (nouveau « Pain du Plateau », 40 miches le samedi dès 7 h, adresse, horaires, compte Instagram). Il a :
- découpé le rush en images à 30 i/s (`tools/clip_frames.py`) ;
- ajouté un étalonnage commun, du grain et une poussée de caméra par plan ;
- posé un titre par plan, en Fraunces et Manrope ;
- ajouté des volets colorés sur les coupes ;
- terminé sur un carton de fin : logo, offre, appel à l'action, adresse, horaires, @compte.

Il n'a fait aucune génération supplémentaire.

| Pièce | Rush | Claude | **Total** | Temps agent | Remarques |
|---|---|---|---|---|---|
| **v02** (Hailuo, 3 images) | 0,27 $ | 0,68 $ (15 appels) | **0,94 $** | 17 min | La meilleure. L'accroche est lisible dès 0,4 s. Petits défauts : le « 40 » chevauche les mains, le sur-titre du plan 2 est posé sur le pain clair. |
| **v01** (Kling 3.0) | 0,69 $ | 0,78 $ (13 appels) | **1,47 $** | 16 min | Éditoriale et propre. Une image entièrement orange au pic du volet de transition, et quelques textes dans la zone basse de l'interface 9:16. |

Pour comparaison, le Studio optimisé sans vidéo IA (primeur, 9:16) coûte 1,26 $. L'hybride à partir d'une seule image animée coûte 0,83 $ pour 10 s, mais sans vrai mouvement.

### 6.4 Recommandation vidéo
**Mise à jour après les tests suivants : Kling 3.0 est le modèle retenu** (bon rendu, obéit au découpage, son natif, mode première et dernière image pour les logos). Hailuo reste l'option la moins chère.

1. **Par défaut : la chaîne « images → Hailuo 2.3 → couche Claude »**, environ **0,95 $ les 15 s finies**.
   - L'agent écrit d'abord le découpage (3 à 5 plans).
   - Il génère ensuite une image Marketing Studio par plan (0,02 $ chacune). On peut les valider avant d'animer, et y mettre la charte ou le produit en référence.
   - Chaque image est animée avec Hailuo (0,07 $ les 6 s).
   - La couche Claude ajoute le texte, la marque et le rythme.

   On contrôle chaque plan, on ne repaie que le plan raté, et c'est le rendu le plus crédible.
2. **Pour un rush d'un seul tenant, rapide : Kling 3.0 std en plusieurs plans, sans son** (0,69 $ les 15 s). C'est le plus obéissant sur le découpage et il n'ajoute pas de texte parasite.
3. **Pour une pièce vitrine en haute définition : MiniMax H3 2K** (1,37 $), seul modèle natif au-dessus de 1080p. Prévoir 10 à 15 min de génération.
4. **Toujours sans son** (moins cher, et la musique se choisit au montage). Interdire texte, logos et marques tierces dans le prompt, parce que les vitrines et enseignes sortent souvent en texte déformé. La couche Claude peut aussi masquer ces zones.
5. **Côté Claude**, les 0,68–0,78 $ de la couche peuvent baisser : effort `medium`, et moins de rendus intermédiaires (un rendu final de 15 s prend environ 10 min sur ce conteneur).
6. **Garde-fou** : un seul appel de génération par plan, pas de relance automatique, estimation gratuite avant chaque appel et réservation dans le registre de budget.

### 6.5 Kling : tous les prix vérifiés (devis Higgsfield, champ `usd`, 9:16)
**Kling** (modèle retenu) :

| Endpoint | Usage | 5 s | 15 s |
|---|---|---|---|
| `kling-video/v3.0/std/text-to-video` | texte → vidéo, jusqu'à 6 plans (`multi_shots`) | 0,35 $ avec son | **0,69 $ sans son / 1,04 $ avec son** |
| `kling-video/v3.0/pro/text-to-video` | même modèle, qualité « pro » | — | 0,92 $ sans son |
| `kling-video/v3.0-turbo/image-to-video` | image de départ → vidéo, 720p | 0,31 $ | 0,92 $ (1,16 $ en 1080p) |
| `kling-video/v3.0/4k/image-to-video` | image de départ et de fin, 4K | 1,16 $ | 3,47 $ |
| **`kling-video/o3/first-last-frame`** | **première et dernière image imposées** (Kling 3 « Omni ») | **0,56 $ std / 0,70 $ pro, avec son** | — |
| `kling-video/o3/image-reference` | images de référence | 0,23 $ | — |

**Le son natif Kling coûte +50 %** (0,69 → 1,04 $ pour 15 s). Il produit l'ambiance et les bruitages calés sur l'image, pas de la musique.

**Modèles plus haut de gamme**, non retenus pour le prix :

| Modèle | Prix pour 15 s |
|---|---|
| Seedance 2.0 | ≈ 4,50 $ en 720p avant remise |
| Cinema Studio 4.0 | ≈ 6,90 $ en 720p |
| Seedance 2.5 | ≈ 6,90 $ en 720p |
| Wan 3.0 Prime 1080p | 2,94 $ |
| Happy Horse 1.1 1080p | 1,89 $ |

Veo 3.1, FLUX 3 Video, Grok Video et Gemini Omni existent dans l'application Higgsfield, mais pas via la clé API (réponse « model_not_found »).

### 6.6 Bien prompter Kling (`docs/KLING_PROMPTING.md`)
Ce qui a le plus amélioré les clips :
- **Une « bible de style » dans le `prompt` principal**, reprise par tous les plans :
  - support (film 35 mm ou rendu 3D studio) ;
  - palette nommée en couleurs précises ;
  - casting (âge, tenue, « pas de mannequins, pas de costumes ») ;
  - grammaire de caméra ;
  - son ;
  - interdits : texte, logos, enseignes, écrans lisibles.
- **Un plan = 5 éléments dans cet ordre** :
  1. cadrage ;
  2. sujet avec **une seule action physique simple** ;
  3. **un seul** mouvement de caméra ;
  4. la lumière ;
  5. la zone laissée vide pour le texte.

  Avec le son : 2 ou 3 sons concrets par plan.
- **`multi_shots` avec des durées par plan** (3 à 6 plans de 2 à 5 s). Les coupes tombent exactement aux durées demandées (v03 : coupes réelles à 3,0 ; 6,0 ; 9,3 et 12,9 s).
- **`cfg_scale` 0,6–0,7** pour suivre le découpage à la lettre.
- **À éviter**, parce que Kling les rate :
  - tout texte lisible (vitrines, écrans, enseignes) : il sort déformé ou en miroir ;
  - les gestes d'outil précis (grigner une miche est devenu « pousser la lame du doigt ») ;
  - les clichés de banque d'images (cliente en tailleur) ;
  - les mains en gros plan qui font un travail fin.
- **Ce qu'il fait très bien** : matières en macro (farine, vapeur, tissus, cheveux), lumière, mouvements de caméra lents, petits gestes humains naturels, 3D abstraite (verre, chrome, rubans de soie).

### 6.7 Film de présentation Klipt en clip + couche Claude (v03) : ce qu'il ne faut pas refaire
**Ce qui a été fait :**
- Kling 3.0 std, 15 s, 5 plans avec son (1,04 $) : boulangère, coiffeuse, panneaux 3D, fondateur sur un toit, faisceau de lumière.
- Un agent Sonnet a ajouté le texte en anglais, le logo, des volets de transition et une bande-son mixée (ambiance Kling, musique synthétisée, bruitages), pour 1,34 $.
- **Total : 2,38 $** de création.

**Verdict du client : raté.**
- Ce sont des plans sans rapport collés ensemble, avec du texte par-dessus. Ce n'est pas une présentation de Klipt, et ça ne montre rien du produit.
- Il portait en plus l'ancien logo inventé (§ 7.2).

**Leçons :**
1. Une vidéo de marque part d'**un concept visuel unique** (un univers, un objet, une transformation), pas d'une liste de métiers.
2. Si la demande est « du Kling », on livre du Kling. La couche Claude n'est qu'une option à proposer.
3. Le logo et les couleurs se vérifient sur le site du client avant de produire.

### 6.8 Génériques Klipt de début et de fin, 100 % Kling (j01)
**Demande :** deux vidéos de 5 s, un générique de début et un de fin à coller sur chaque vidéo Klipt. Kling uniquement, vrai logo, vraies couleurs, avec le son, au niveau d'un ident d'agence ou de chaîne.

**Méthode qui a marché :**
1. **Charte récupérée sur klipt-ai.com** : SVG officiel du symbole, CSS du site (couleurs, Bricolage Grotesque 700), capture du site pour l'ambiance (fond crème et halos aurore).
2. **Images clés exactes rendues en code** (`pieces/j01/frames/`, 1080×1920). Elles ne sont qu'une entrée de Kling, il n'y a aucune couche sur la vidéo :
   - fond crème avec halos, vide ;
   - logo centré (symbole et « Klipt ») ;
   - carte de fin : logo, « Agency quality. **Automatic.** » avec le dégradé du site, et klipt-ai.com ;
   - symbole seul, en grand.
3. **Kling O3 `first-last-frame`, mode pro, son activé, 5 s, 9:16.** L'image de début et l'image de fin sont imposées, Kling invente le mouvement entre les deux.
   - Le prompt décrit le style (ident premium, fond crème, halos, 3D brillante, pas de texte en plus), l'animation et le **design sonore** : souffle, montée, impact grave et note double sur le logo, sans voix ni musique.
   - Une phrase rappelle que la fin doit correspondre exactement à la dernière image.

**Résultats :** 4 génériques en 1080×1920, 24 i/s, avec son, générés en 2 à 5 min.

| Générique | Image de début → de fin | Animation |
|---|---|---|
| **intro-a** | fond vide → logo | trois rubans de soie indigo, violet et rouge s'enroulent et se replient en logo |
| **intro-b** | symbole géant → logo | le symbole devient du verre en 3D, pivote dans la lumière, rétrécit, « Klipt » se pose à côté |
| **outro-a** | fond vide → carte de fin | des cartes translucides (comme des posts) traversent l'écran, s'assemblent en logo, puis le slogan et l'URL apparaissent |
| **outro-b** | logo → carte de fin | le triangle pulse comme un bouton play qu'on presse, une onde lumineuse part, le slogan et l'URL apparaissent |

**Fidélité :** la dernière image de chaque vidéo, comparée à l'image clé, reproduit le logo, le slogan et l'URL quasiment au pixel près.

**Coût :**

| Poste | Coût |
|---|---|
| Création | 4 × 0,70 $ = **2,80 $**, soit **0,70 $ par générique** (0,56 $ en std) |
| Orchestration (session principale) | 6,09 $ (voir § 4.4) |

L'orchestration ne se repaie pas : le kit de marque et les images clés sont réutilisables, et un script ferait le reste.

**Limites :**
- **Son** : le niveau est bas (−20 à −25 dB en moyenne, crêtes entre −4 et −8 dB) et il n'a été vérifié qu'à la mesure, pas à l'écoute. Il faut l'écouter et, au besoin, le remonter au niveau des réseaux (−14 LUFS) sans toucher à l'image.
- **Image** : pendant l'animation, le mot « Klipt » apparaît lettre par lettre ou flou pendant une fraction de seconde (intro-b et outro-a vers 3,5 s). Il faut vérifier image par image qu'aucune lettre n'est déformée. Il est net sur la fin, imposée par l'image clé.

**Méthode réutilisable pour chaque client**, environ 0,70 $ par générique :
1. récupérer le logo et les couleurs du client sur son site ;
2. rendre 2 ou 3 images clés exactes ;
3. lancer Kling O3 en première et dernière image, avec le son.

### 6.9 Son
**Dans le moteur de rendu :**
- `KLIPT.audio` déclare des pistes : ambiance d'un clip, musique, bruitages, avec début, décalage, durée, gain et fondus.
- `render.mjs` les mixe et les limite dans le MP4.
- `node tools/render.mjs audio pieces/<id>` remixe le son en quelques secondes, sans refaire l'image.

**Bruitages** (`tools/sfx.py`), synthétisés, libres de droits et déterministes : whoosh, riser, impact, tick, pop, shimmer, glitch, et une musique de fond à tempo et ambiance choisis, avec une coupure optionnelle.

**Limites :**
- Ni Claude ni l'agent ne peuvent écouter : seuls les niveaux sont mesurés.
- La musique synthétisée est propre mais basique. Pour une vraie qualité, il faut une bibliothèque libre pour usage commercial ou la musique de la plateforme.
- Sur Instagram et TikTok, un compte professionnel n'a le droit qu'aux sons des bibliothèques commerciales de Meta et TikTok.

**Le son natif Kling** (+50 %) est le plus crédible pour l'ambiance d'une scène réelle ou d'un générique.

### 6.10 Montages réalisés pendant les tests
| Montage | Comment | Coût image | Note |
|---|---|---|---|
| Hailuo, 3 plans | 3 images Marketing Studio animées une par une (6 s), coupées à 5 s et mises bout à bout avec ffmpeg | 0,27 $ | rendu le plus authentique, base de v02 |
| v01 / v02 | rush Kling ou Hailuo découpé en images (`clip_frames.py`) + couche Claude (texte, volets, carton de fin) | 0,69 / 0,27 $ + Claude 0,78 / 0,68 $ | v02 = meilleure vidéo « commerce local » |
| v03 | rush Kling 5 plans avec son + couche Claude + mixage | 1,04 $ + 1,34 $ | raté : collage sans concept (§ 6.7) |
| j01 | Kling seul, images clés imposées | 0,70 $ par générique | génériques de début et de fin retenus |
| Comparatif | les 6 rushs côte à côte (`bench/results/video-models-compare.mp4`) | — | pour comparer les modèles d'un coup d'œil |
