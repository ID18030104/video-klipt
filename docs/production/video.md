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
