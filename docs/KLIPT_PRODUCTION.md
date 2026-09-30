# Klipt — guide de production

Ce fichier rassemble tout ce qui a été construit et mesuré pour produire le contenu Klipt (vidéos 10–30 s, posts, carrousels, stories) avec des agents Claude, et tout ce qu'il faut pour le mettre en production : l'architecture, les modes de production et quand les utiliser, les coûts réels mesurés, l'infrastructure, la sécurité et les licences, puis **en annexe le texte intégral des prompts, du catalogue de décisions, du contrat de rendu et du code des outils**. Le fichier est autonome : on peut reconstruire la chaîne à partir de lui seul.

> Fichier généré par `python3 tools/build_production_doc.py` à partir de `docs/production/guide.md` et des sources du dépôt. Les fichiers du dépôt restent la référence : si tu modifies un prompt ou un outil, relance le script pour régénérer ce document.

---

## 1. En une page

**Principe.** Un agent Claude reçoit un brief client (JSON), décide d'une direction créative, puis écrit la pièce **en code** (une page HTML/CSS/SVG/GSAP/three.js). Un moteur de rendu déterministe (Chromium sans écran + ffmpeg) la transforme en MP4 ou en PNG. Pour les images photographiques, l'agent peut utiliser des photos libres de droits (Open Images, Pexels) ou **générer une image ou un clip vidéo par IA (Higgsfield)**, sur lequel il pose ensuite une couche en code : textes exacts, chiffres, logo, interface, animations.

**Pourquoi du code et pas seulement de l'IA générative :**
- **Texte exact** : typographie française correcte (espaces insécables, « guillemets », accents sur les capitales), prix, dates, adresses, jamais de lettres déformées.
- **Marque exacte** : vraies polices, vraies couleurs, vrai logo, au pixel près.
- **Modifiable et déclinable** : changer un prix ou une date, ou passer du 9:16 au 4:5, se fait par un re-rendu, sans tout régénérer.
- **Déterministe** : le même fichier donne toujours la même vidéo, donc on peut archiver, corriger ou re-rendre en 4K.

**La chaîne recommandée pour Klipt :**

| Besoin client | Mode | Modèle | Coût total mesuré | Temps agent |
|---|---|---|---|---|
| Post, carrousel ou story avec photo (restaurant, hôtel, commerce, événement) | **Hybride image** : image Higgsfield + couche Claude | Sonnet 5.5 | **0,24–0,31 $** | 1–2 min |
| Petite vidéo promo (niveau B : soldes, horaires, plat du jour) | **Hybride 1 image** : image animée + couche Claude | Sonnet 5.5 | **≈ 0,83 $** | ≈ 6 min |
| Vidéo 15 s avec vraies images en mouvement (Reel, pub locale, lancement) | **Hybride clip vidéo** : 3 images → Hailuo 2.3 + couche Claude | Sonnet 5.5 + Higgsfield | **≈ 0,94 $** (rush 0,27 $ + Claude 0,68 $) | ≈ 17 min + génération |
| Film SaaS, lancement, interface produit, datavisualisation (niveaux S/S+) | **Studio optimisé** : 100 % code + photos libres | Sonnet 5.5 (Opus 5.5 pour les pièces vitrines) | 1,26–2,94 $ (vidéo), 0,40–0,60 $ (post) | 4–30 min |
| Déclinaisons en volume, tests A/B d'accroches | **Higgsfield seul** (Marketing Studio avec texte) + contrôle du texte | aucun agent créatif | 0,02–0,07 $ | 20–40 s |

**Les décisions qui comptent :**
1. **Sonnet 5.5 est le modèle de production.** Opus 5.5 donne +0,5 point sur 10 pour environ 3 fois le prix ; il est à réserver aux pièces vitrines (showreel, grands comptes).
2. **Pas de skill chargé, tout est dans le prompt** (prompt Studio + catalogue). Les skills testés (klipt-craft, taste-express) n'ont pas justifié leur coût avec Sonnet.
3. **Pas de pipeline multi-agents** (directeur artistique puis exécutant, ou critique puis correction) : plus cher et pas meilleur qu'un seul agent bien briefé.
4. **Les règles d'efficacité divisent le coût par 2 à 3** à qualité égale, et c'est ce qui coûte le plus. Le coût vient du nombre d'allers-retours (chaque appel relit tout le contexte) et des images ouvertes, pas de la créativité.
5. **L'hybride est le meilleur rapport qualité/prix** : l'IA fournit la photo (lumière, matières, personnes), Claude fournit tout ce qui doit être exact.
6. **Contrôle qualité automatique obligatoire** (`render.mjs qa`) : il détecte les défauts qui faisaient perdre des points (première image vide, texte coupé, texte trop petit, zones de sécurité 9:16).

---

## 2. Architecture

```
brief client (JSON)
      │
      ▼
agent Claude Sonnet 5.5  ── prompt : Studio optimisé  ou  Hybride  (+ catalogue de décisions)
      │   phase 1 : plan.md (stratégie, niveau d'ambition, style, storyboard, texte final)
      │   phase 2 : ressources ──► Higgsfield (image 2k low ≈ 0,02 $ ou clip vidéo)
      │                         ──► Open Images / Pexels (photos libres, crédits automatiques)
      │                         ──► polices locales (@fontsource, Google Fonts téléchargées)
      │   phase 3 : pieces/<id>/index.html (HTML/CSS/SVG/GSAP/three.js, window.KLIPT)
      ▼
tools/render.mjs  ── Chromium sans écran, image par image (t = 0, 1/30 s, …) ──► ffmpeg H.264
      │   video.mp4 + poster.jpg + sheet.jpg     ou     slides/slide-01.png … + sheet.jpg
      ▼
render.mjs qa  ── images clés + rapport de défauts ──► l'agent corrige (1 boucle)
      ▼
meta.json (marque, format, style, niveau, crédits photo, coût de l'image IA) ──► site Klipt / client
```

**Le contrat technique** (annexe C) est la seule interface entre l'agent et le moteur. La page définit `window.KLIPT = {width, height, fps, duration, render(t), ready, poster}` pour une vidéo, ou des `<section class="slide">` pour des images fixes. Le rendu doit dépendre uniquement de `t` : pas d'horloge, pas de hasard non initialisé, pas de ressource distante. Le moteur :
- met en pause et positionne à `t` les animations CSS et Web Animations ;
- attend uniquement les vraies `Promise` renvoyées par `render(t)`, car une timeline GSAP est un « thenable » qui ferait tout bloquer ;
- filme chaque diapositive dans son propre cadre ;
- limite le nombre de rendus simultanés sur la machine (`KLIPT_RENDER_SLOTS`, 2 par défaut), car Chromium plante au-delà ;
- applique le mode `qa` : images à 0 ; 0,4 ; 1,0 s, puis toutes les 1,5 s, plus la fin et l'affiche. Il détecte les images quasi vides, le texte coupé par le cadre ou partiellement masqué, le texte de moins de 26 px, le texte dans les zones d'interface 9:16 (200 px en haut, 340 px en bas) et les polices manquantes.

**Pourquoi un plafond de rendus simultanés et la règle « ne jamais tuer un processus que tu n'as pas lancé »** : en test, des agents ont lancé `pkill -f render.mjs` et détruit les rendus des autres. En production, chaque rendu doit tourner dans son propre conteneur ou sa propre file.

---

## 3. Les modes de production en détail

### 3.1 Choisir le niveau d'ambition (le cœur du prompt)

Le prompt oblige l'agent à raisonner comme un stratège avant d'être designer, et à **proportionner l'investissement à l'enjeu**. Un film de présentation SaaS doit impressionner. Une promo de primeur doit être lisible en une seconde et chaleureuse, et une surproduction paraîtrait fausse.

| Niveau | Briefs typiques | Vidéo | Post |
|---|---|---|---|
| **S+ Vitrine** | film de marque, levée de fonds, hero de site premium | 25–30 s, 8–12 plans, concept sur mesure | affiche qu'on capture d'écran |
| **S Phare** | présentation SaaS, lancement premium, hôtel, bande-annonce d'événement | 20–30 s, 6–10 plans | qualité éditoriale |
| **A Campagne** | nouvelle fonctionnalité, recrutement, événement, preuve B2B, nouvelle carte | 12–20 s, 4–7 plans | soigné, hiérarchie forte |
| **B Quotidien** | promo, soldes, horaires, plat du jour, petit événement | 7–12 s, 3–5 plans | une idée, lisible en 1 s |
| **C Micro** | rappel en story, compte à rebours, « dernières places » | 4–7 s, 1–3 plans, en boucle | ultra simple |

Plus quatre curseurs :
- **finition** : studio ↔ natif réseaux sociaux ↔ brut/UGC ;
- **énergie** ;
- **registre** : prestige, expert, chaleureux, drôle, irrévérencieux… ;
- **étape du tunnel** : notoriété, considération, conversion, fidélité, avec la durée de vie du contenu.

Ensuite, l'agent choisit dans le **catalogue de décisions** (annexe D) :
- 20 structures narratives ;
- 25 mécaniques d'attention ;
- 40 familles de styles (keynote Apple, Kinfolk, broadcast esport, génériques A24, Swiss, brutaliste, Y2K, etc.) ;
- 14 traitements d'image ;
- 13 systèmes typographiques ;
- 12 stratégies de couleur ;
- les mouvements de caméra ;
- 20 transitions ;
- les formats.

Il note sa pièce dans un historique pour ne pas répéter la même combinaison style, palette, typographie et transition d'une pièce à l'autre. **L'illustration vectorielle plate comme visuel principal est interdite aux niveaux S+, S et A**, car c'est ce qui donnait l'aspect « enfantin ».

### 3.2 Studio optimisé (100 % code + photos libres)
- **Prompt** : annexe A (`docs/STUDIO_PROMPT_OPT.md`), qui reprend le prompt Studio (5 phases) avec en plus un bloc « règles d'efficacité ».
- **Ce qu'il fait le mieux** : interfaces produit animées, graphiques, typographie cinétique, 3D légère, keynote. C'est le mode à retenir pour le SaaS et la tech.
- **Limite** : les photos Open Images font au plus 1024 px et sont souvent amateurs. Le prompt impose donc un tri sévère, des traitements qui masquent la douceur (grain, étalonnage, bichromie) et un texte toujours plus net que la photo.
- **Coût mesuré** (même brief, même prompt, seules les règles d'efficacité changent) :

| Pièce | Studio v1 | Studio optimisé | Écart |
|---|---|---|---|
| Relai, film SaaS 16:9 (niveau S) | 3,32 $, 56 appels, 76 min | 2,94 $, 43 appels, 32 min | −12 % |
| Aux Jardins de Marcel, primeur 9:16 (niveau B) | 1,56 $, 40 appels | 1,26 $, 30 appels | −19 % |
| Casa Almar, post hôtel | 1,24 $ | 0,40 $, 14 appels | −67 % |
| Nexus Arena, post esport | 1,33 $ | 0,45 $, 15 appels | −66 % |
| Stride Collective, post événement | 1,03 $, 27 appels | 0,60 $, 20 appels | −42 % |

### 3.3 Hybride image (recommandé pour les posts)
- **Prompt** : annexe B (`docs/HYBRID_PROMPT.md`).
- **Recette** : **une seule** image générée par Higgsfield Marketing Studio (2k, qualité low, environ 0,02 $). Elle est décrite comme un brief photo et **laisse une zone vide pour le texte**. Le prompt interdit texte, lettres, logos, filigranes et marques tierces (Higgsfield avait dessiné une virgule Nike sur une basket). L'agent pose ensuite en code la typographie, les chiffres, le logo et les éléments graphiques, puis étalonne et ajoute du grain pour unifier le tout.
- **Résultats** :

| Pièce | Claude | Image | Total | Temps |
|---|---|---|---|---|
| Casa Almar | 0,22 $ | 0,023 $ | 0,24 $ | 1 min |
| Relai (post LinkedIn) | 0,23 $ | 0,024 $ | 0,25 $ | 2 min |
| Nexus Arena | 0,28 $ | 0,024 $ | 0,31 $ | 2 min |

  C'est la meilleure qualité perçue de tous les tests, pour environ 4 fois moins que le Studio v1.
- **Règle** : un seul appel, jamais de relance automatique. Le garde-fou de budget refuse toute dépense au-delà du solde prévu.

### 3.4 Hybride vidéo à partir d'une seule image
- Même prompt hybride, au format 9:16. L'agent anime l'image : poussée de caméra, recadrages présentés comme des plans distincts, parallaxe entre l'image et le texte, masques, tampons.
- **Primeur, 10 s** : 0,021 $ d'image + 0,81 $ de Claude (30 appels) = 0,83 $, en 6 min.
- **Défaut relevé** : l'offre « −30 % » n'arrivait qu'à 3 s. Au niveau B, **l'offre doit être lisible dès la première image**. La règle est dans le prompt Studio mais doit être rappelée dans le prompt hybride (voir la feuille de route).

### 3.5 Hybride clip vidéo
Un rush IA de 15 s (3 à 5 plans) sert de fond, et la couche Claude raconte l'histoire : accroche, un titre par plan, volets sur les coupes, carton de fin. C'est la section « Clip mode » du prompt hybride (annexe B). Le comparatif des modèles et les coûts sont au § 6.

### 3.6 Higgsfield seul (Marketing Studio avec texte intégré)

| Réglage | Coût par image | Temps |
|---|---|---|
| 1k low | 0,015 $ | ≈ 20 s |
| 1k medium | 0,05 $ | ≈ 40 s |
| Référence de marque (logo téléversé) | +≈ 0,013 $ | — |

- **Texte** : les textes français courts sont sortis exacts lors du test.
- **Logo en référence** : il est reproduit fidèlement, mais sous forme d'une réinterprétation (objet 3D, par exemple), pas d'un placement au pixel près.
- **Recommandation** : l'utiliser pour les déclinaisons en volume et les tests A/B d'accroches. Il faut **toujours une vérification du texte** avant publication, avec une relecture par un modèle de vision ou un humain, et interdire les marques tierces dans le prompt.
- **Téléverser un élément de marque** : `python3 tools/higgsfield_upload.py brand/klipt/logo-dark.png` renvoie une URL publique, à passer dans `--image-url` (répétable, 16 au maximum).

---

## 4. Modèles, coûts et pourquoi ça coûte ce que ça coûte

### 4.1 Le banc d'essai : 74 pièces, 8 configurations, notation à l'aveugle

**Protocole :**
- 50 marques fictives (SaaS, PME, artisans, commerces, santé, culture, luxe), en français et en anglais.
- 46 vidéos de 10 à 30 s et 28 posts, carrousels ou stories.
- Juges Opus et Sonnet à l'aveugle (identifiants neutres, fichiers de travail retirés), 9 critères.
- Coûts valorisés au tarif public de l'API.

| Config | Note /10 | Vidéo | Fixe | Publiable tel quel | $/pièce | min/pièce |
|---|---|---|---|---|---|---|
| A — Sonnet seul | 6,33 | 5,80 | 7,00 | 22 % | 0,43 | 11 |
| B — Sonnet + klipt-craft | 6,44 | 6,00 | 7,00 | 22 % | 0,53 | 11 |
| C — Opus seul | **6,89** | 6,40 | 7,50 | **67 %** | 1,38 | 15 |
| D — Opus + klipt-craft | 6,80 | 6,33 | 7,50 | 20 % | 1,11 | 12 |
| E — directeur Opus → exécutant Sonnet | 6,60 | 6,33 | 7,00 | 30 % | 3,13 | 66 |
| F — Sonnet → critique Opus → Sonnet | 6,44 | 6,00 | 7,33 | 56 % | 1,73 | 42 |
| G — Opus + taste-express | 6,78 | 6,50 | 7,33 | 56 % | 3,00 | 43 |
| H — Sonnet + taste-express | 6,11 | 5,80 | 6,50 | 0 % | 0,80 | 23 |

Budget total de l'expérience : 150,58 $.

| Poste | Coût |
|---|---|
| Production | 105,68 $ |
| Juges | 14,88 $ |
| Orchestration | 21,38 $ |
| Perdu lors d'un redémarrage du conteneur | 8,63 $ |

Le prompt Studio (sans skill, avec le catalogue et le contrôle qualité automatique) a ensuite été construit **à partir des défauts relevés par les juges** :
- première seconde vide ou statique ;
- texte coupé par les masques d'apparition ;
- images de transition vides ;
- affiche capturée en pleine transition ;
- texte secondaire trop petit ;
- dessins vectoriels jugés « enfantins ».

### 4.2 Tarifs de référence

**Claude**, par million de tokens :

| Modèle | Entrée | Sortie | Cache écrit (5 min / 1 h) | Cache lu |
|---|---|---|---|---|
| Sonnet 5.5 (`claude-sonnet-5-5`) | 2 $ | 10 $ | 2,50 $ / 4 $ | 0,20 $ |
| Opus 5.5 (`claude-opus-5-5`) | 4 $ | 20 $ | 5 $ / 8 $ | 0,20 $ |

**Higgsfield Marketing Studio**, par image. Valeurs renvoyées par l'endpoint d'estimation (gratuit), champ `usd`, qui est le prix facturé remise incluse :

| Résolution | low | medium | high |
|---|---|---|---|
| 1k | 0,015 $ | 0,050 $ | 0,168 $ |
| 2k | 0,020 $ | 0,090 $ | 0,326 $ |
| 4k | 0,026 $ | 0,143 $ | 0,540 $ |

Avec une image de référence, compter environ +0,013 $.

**Higgsfield vidéo**, 15 s en 9:16 : voir § 6.

### 4.3 Pourquoi un agent coûte 0,25 à 3 $ par pièce
- **L'agent travaille en boucle.** Chaque appel d'outil (écrire, rendre, regarder) renvoie **tout le contexte**, soit 90 à 105 000 tokens par appel. Avec le cache, cette relecture coûte 0,20 $ le million, mais sur 40 appels, cela fait 4 millions de tokens lus. S'y ajoutent la sortie (le code écrit et la réflexion, à 10 $ le million) et l'écriture en cache de chaque nouveau morceau.
- **Chaque image regardée reste dans le contexte** jusqu'à la fin de la tâche, et donc est relue à chaque appel suivant.
- **Leviers mesurés** : moins d'allers-retours (planifier et écrire d'un seul tenant, enchaîner les commandes), images plus petites et moins nombreuses (planches contact, `--w 540`), une seule boucle de contrôle qualité, un budget de 15 appels pour un post et 25 pour une vidéo. Résultat : **−33 % en moyenne, jusqu'à −67 % sur les posts**, pour une qualité comparable (jugée par moi, pas par des juges à l'aveugle).
- **Comparaison avec un autre modèle** : GPT-6.1 Sol (2 $ / 10 $, 0,10 $ en cache) reviendrait environ 27 % moins cher en simulation sur un post, mais exigerait un autre moteur d'agent. Ce n'est pas testé en qualité.

### 4.4 Mesurer le coût en production
Il faut journaliser pour chaque pièce les tokens d'entrée, de cache lu, de cache écrit et de sortie, le nombre d'appels, la durée et le coût de l'image ou du clip IA (`<fichier>.json` écrit par les outils Higgsfield). L'outil de benchmark `tools/bench_costs.py` fait ce calcul à partir des transcripts. En production, on lit directement le champ `usage` renvoyé par l'API, ou le coût total fourni par le moteur d'agent (§ 5.3).

---

## 5. Mettre en production

### 5.1 Ce qu'il faut copier depuis le dépôt

| Élément | Fichier(s) | Rôle |
|---|---|---|
| Moteur de rendu | `tools/render.mjs`, `lib/klipt-kit.js`, `package.json` (dépendances) | HTML → MP4/PNG, contrôle qualité |
| Prompts | `docs/STUDIO_PROMPT_OPT.md`, `docs/HYBRID_PROMPT.md`, `docs/STUDIO_CATALOGUE.md`, `docs/RENDER_CONTRACT.md` | le « cerveau » créatif (annexes A à D) |
| Images IA | `tools/higgsfield_image.py`, `tools/higgsfield_video.py`, `tools/higgsfield_upload.py`, `tools/hf_ledger.py` | génération, téléversement de la charte, garde-fou de budget |
| Photos libres | `tools/openimages.py`, `tools/pexels.py` | recherche, planche contact, téléchargement, crédits |
| Polices | `tools/gfont.py` + paquets `@fontsource/*` | polices locales (le rendu est hors ligne) |
| Kit de marque | `brand/klipt/` (logos, `brand.json`) | modèle pour les kits de chaque client |
| Exemples | `pieces/<id>/` | bibliothèque d'exemples du site (§ 8) |

**Ce qui ne va pas en production** (outils d'évaluation) : `bench/`, `tools/metrics.py`, `analyze.py`, `collect_judgments.py`, `build_gallery.py` et les skills `klipt-craft` et `taste-express`, non retenus.

### 5.2 Infrastructure d'un « worker » de rendu
- **Node 20 ou plus** (testé en 22), puis `npm install` (gsap, three, d3, lucide-static, @fontsource/*, playwright-core 1.56).
- **Chromium** compatible Playwright. Sous l'utilisateur root, lancer avec `--no-sandbox`. Le WebGL tourne en logiciel (SwiftShader) : garder la 3D légère.
- **ffmpeg avec libx264.** Celui de Playwright n'a pas libx264 ; `imageio-ffmpeg` fournit un binaire complet, à exposer sous `/usr/local/bin/ffmpeg`.
- **Python 3.11** avec Pillow (planches contact, grilles de contrôle qualité, agrandissement).
- **Processeur** : un rendu final de 20 s en 1080×1920 à 30 i/s prend 1 à 2 min sur un cœur. Prévoir 2 rendus simultanés pour 4 vCPU.
- **Réseau sortant** à autoriser pendant la production (jamais pendant le rendu, qui est hors ligne) :

| Hôte | Usage |
|---|---|
| `api.higgsfield.ai` | génération et estimation |
| `d3u0tzju9qaucj.cloudfront.net` | images générées |
| `d3snorpfx4xhv8.cloudfront.net` | fichiers téléversés |
| hôte de téléchargement des vidéos | voir le champ `video_host` dans le `.json` du clip |
| `api.pexels.com`, `images.pexels.com`, `videos.pexels.com` | Pexels |
| `open-images-dataset.s3.amazonaws.com`, `storage.googleapis.com` | Open Images |
| `fonts.googleapis.com`, `fonts.gstatic.com` | polices, téléchargées une fois par `gfont.py` |

- **Isolation** : un conteneur ou un répertoire de travail par pièce. L'agent ne doit voir que son dossier, les outils et les ressources partagées.

### 5.3 Faire tourner l'agent
Deux options, toutes deux testables sans rien changer aux prompts :

1. **Claude Agent SDK ou Claude Code en mode non interactif.** C'est le même moteur d'agent que celui utilisé pour tous les tests, avec les outils intégrés Bash, Read, Write et Edit, sur ton infrastructure. Exemple en ligne de commande (à valider avec la doc à jour, https://code.claude.com/docs/en/agent-sdk) :
   ```bash
   claude -p "$(cat docs/HYBRID_PROMPT.md) ROLE: hybrid | PIECE_ID: h42 | brief: bench/briefs/h42.json | plate aspect: 3:4" \
     --model claude-sonnet-5-5 \
     --allowedTools "Bash,Read,Write,Edit" \
     --output-format json > runs/h42.json    # le JSON final contient le coût et l'usage de tokens
   ```
   Le même appel se fait en TypeScript ou en Python avec le paquet `@anthropic-ai/claude-agent-sdk` / `claude-agent-sdk` (fonction `query(prompt, options)`), avec le prompt système, les outils autorisés, le modèle et le répertoire de travail en options.
2. **Claude Managed Agents** (API Anthropic, bêta). Anthropic héberge la boucle et un conteneur par session. On y installe Node, Chromium, ffmpeg et les outils du dépôt, et les clés Higgsfield et Pexels passent par un coffre (vault) : elles ne sont jamais visibles par l'agent. C'est pertinent si tu ne veux pas gérer de workers.

**Réglages recommandés :**
- modèle `claude-sonnet-5-5`, effort `high` (le défaut ; `medium` à tester pour les niveaux B et C) ;
- mettre en cache le prompt fixe (prompt Studio ou Hybride, catalogue, contrat), identique d'une pièce à l'autre, et placer le brief à la fin, pour ne pas casser le cache ;
- ne jamais mettre la date, un identifiant ou une variable dans le prompt système.

**Orchestration** : une file de tâches (brief → pièce), N workers, une reprise possible en cas de redémarrage. Le banc d'essai a perdu 8,63 $ lors d'un redémarrage du conteneur, d'où l'intérêt d'un état persistant (brief, statut, coût) en base plutôt qu'en mémoire.

### 5.4 Format d'un brief
```json
{
 "id": "s02", "kind": "video", "format": "1080x1920", "duration": "8–12 s", "lang": "fr",
 "brand": "Aux Jardins de Marcel", "sector": "Primeur de quartier",
 "brief": "Primeur indépendant rue de Marseille, Lyon 7e, tenu par Marcel et sa fille depuis 1998. Fin de saison : -30 % sur tous les fruits d’été ce week-end… Cible : habitants du quartier. Diffusion : Instagram Stories/Reels + Facebook. Infos : 42 rue de Marseille — sam. 8h–19h, dim. 8h–13h."
}
```
Plus le brief est précis (offre, preuves chiffrées, adresse, horaires, public, canal de diffusion, appel à l'action), meilleure est la pièce : le prompt interdit d'inventer des chiffres, des témoignages ou des affirmations. Pour une marque réelle, il faut ajouter un **kit de marque** sur le modèle de `brand/klipt/` (logos PNG ou SVG, `brand.json` avec la palette et les polices) et le passer à l'agent. En hybride, le logo est posé en code ; en Higgsfield seul, il est passé en référence.

### 5.5 Sorties d'une pièce
`pieces/<id>/` contient :
- `index.html`, la source, re-rendable ;
- `video.mp4`, `poster.jpg` et `sheet.jpg` (12 images clés), ou `slides/*.png` et `sheet.jpg` ;
- `plan.md`, le raisonnement créatif ;
- `meta.json` : marque, format, durée, titre, concept, techniques, polices, palette, langue, niveau, style, mécaniques d'attention, crédits photo, et l'image ou le clip IA avec son coût et son prompt ;
- `assets/`, avec le fichier `CREDITS.json` et les fichiers `.json` des générations.

---

## 6. Vidéo IA à moins de 2 $ pour 15 s

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

---

## 7. Qualité, sécurité, droits

### 7.1 Contrôle qualité
- **Automatique** : `node tools/render.mjs qa pieces/<id>` produit une grille d'images clés et un rapport de défauts. Une pièce ne part pas tant que ce rapport contient des défauts non justifiés.
- **Grille de relecture** (dans le prompt) :
  - la première image arrête-t-elle le pouce ?
  - chaque mot est-il lisible et juste ?
  - chaque plan a-t-il un seul point focal ?
  - les photos sont-elles étalonnées de façon cohérente ?
  - l'ambition correspond-elle au niveau choisi ?
  - un inconnu penserait-il qu'une agence l'a fait ?
- **Relecture humaine** avant envoi au client, ou un juge Sonnet (environ 0,11 $ par pièce) qui note sur les 9 critères du banc et liste les défauts.

### 7.2 Secrets
- Les clés Higgsfield et Pexels **ne sont jamais dans le dépôt, qui est public**. Elles sont stockées hors dépôt (`/root/klipt-state/`) ou passées par variable d'environnement (`HF_KEY`, `PEXELS_API_KEY`) ; en production, utiliser un gestionnaire de secrets.
- Les deux clés ont circulé dans une conversation : **il faut les renouveler** avant la mise en production.

### 7.3 Budget
- Tous les appels payants passent par `tools/hf_ledger.py`.
- **Estimation gratuite** avant chaque appel, **réservation sous verrou de fichier** (sûre même avec plusieurs agents en parallèle), **remboursement** si la génération échoue (Higgsfield ne facture pas les échecs). En production, remplacer le fichier par une ligne en base par client ou par projet.
- Les agents n'ont droit qu'à **un seul appel de génération par pièce, sans relance automatique**.

### 7.4 Droits et mentions
- **Open Images** : photos Flickr sous licence CC BY 2.0, usage commercial autorisé **avec crédit de l'auteur**. Les crédits sont écrits automatiquement dans `assets/CREDITS.json` et `meta.json` ; il faut les publier (légende, page crédits du site).
- **Pexels** : licence Pexels, usage commercial libre sans crédit obligatoire. Pas de revente de la photo seule, et pas de personnes identifiables mises dans un contexte dégradant.
- **Polices** : Google Fonts et @fontsource sont sous licence OFL, utilisables commercialement.
- **Images et vidéos Higgsfield** : vérifier les conditions d'usage commercial du compte (varient selon le plan). Interdire dans le prompt les marques et logos tiers, et ne pas générer de personnes réelles identifiables.
- **Contenu généré par IA** : Meta, TikTok et YouTube demandent de signaler les contenus photoréalistes générés par IA (étiquette « IA »), et le règlement européen sur l'IA impose une transparence sur les contenus synthétiques réalistes. Pour les pièces hybrides avec photo générée, activer l'étiquette de la plateforme.
- **Marques de démonstration** : les 50 marques du banc sont fictives. Avant de les montrer sur le site Klipt comme « exemples », vérifier qu'aucune ne correspond à une entreprise réelle homonyme (ex. Relai, Greenloop, Orbitr) ou préciser « marque fictive ».

---

## 8. Bibliothèque d'exemples pour le site

Les pièces les mieux notées par les juges à l'aveugle (note /10, et publiable telle quelle selon tous les juges) :

| Pièce | Marque (secteur) | Type | Langue | Note |
|---|---|---|---|---|
| p220 | Domaine des Trois Chênes (vin) | vidéo | FR | 8,0 |
| p224 | Blank Page Books (librairie) | carrousel | EN | 8,0 |
| p250 | Taco Loco (restauration) | story | EN | 8,0 |
| k112 | Garnier & Fils (plomberie) | carrousel | FR | 8,0 |
| p236 | Shala Yoga Annecy | carrousel | FR | 8,0 |
| p210 | Nuage HR (SaaS RH) | carrousel | EN | 7,0 |
| p221 | Cap Horizon Voyages | post | FR | 7,0 |
| p230 | Transports Lacroix | vidéo | FR | 7,0 |
| p262 | Orbitr (SaaS) | post | EN | 7,0 |
| p288 | Bloc Party (escalade) | story | EN | 7,0 |
| p294 | Clinique vétérinaire des Tilleuls | vidéo | FR | 7,0 |
| p218 | Pharmacie du Marché | carrousel | FR | 7,0 |
| p290 | Pixel Brew (café gaming) | vidéo | EN | 7,0 |
| p267 | Auto-École Feu Vert | vidéo | FR | 7,0 |
| k165 | Ledgerly (SaaS finance) | vidéo | FR | 7,0 |
| p213 | Nonna Rosa (trattoria) | post | FR | 7,0 |
| p275 | Atelier Mèche (coiffeur) | post | FR | 7,0 |

Et les séries plus récentes, produites après ce banc (non notées à l'aveugle, mais au-dessus en qualité perçue) :

| Série | Pièces |
|---|---|
| Studio | s01 Relai (film SaaS 16:9), s02 Aux Jardins de Marcel (primeur 9:16), s03 Casa Almar (hôtel), s04 Nexus Arena (esport), s05 Stride Collective (événement) |
| Studio optimisé | o01 à o05 (mêmes briefs) |
| Hybride | h02 primeur vidéo, h03 Casa Almar, h04 Nexus Arena, h05 Relai LinkedIn, **v02 Maison Brune (vidéo 15 s, Hailuo + couche Claude, la meilleure vidéo à ce jour)**, v01 Maison Brune (Kling 3.0) |

La galerie interactive (vidéos, notes, défauts, coûts) est en ligne : https://claude.ai/artifact/Hsg5U2GQQHs7LmC6skCEQ2. Elle ne contient pas encore les séries o et h.

---

## 9. Feuille de route
1. **Renouveler les clés** Higgsfield et Pexels.
2. **Prompt hybride** : ajouter la règle des niveaux B et C (« l'offre lisible dès la première image ») et le mode clip vidéo du § 6.
3. **Faire de l'hybride le mode par défaut** pour les posts et les promos, et garder le Studio optimisé pour le SaaS et les niveaux S.
4. **Contrôle du texte** pour le mode Higgsfield seul : relecture par un modèle de vision avant publication.
5. **Kits de marque clients** (logo, palette, polices) passés systématiquement à l'agent.
6. **Journal des coûts** par pièce en base, et budget Higgsfield par client dans le registre.
7. **Juge automatique** (Sonnet, environ 0,11 $) en fin de chaîne pour filtrer les pièces sous 7/10.
8. Tester l'effort `medium` sur les niveaux B et C (gain de coût probable), et Opus 5.5 uniquement sur les niveaux S+.


---

# Annexes


## Annexe A — Prompt Studio optimisé (agent Sonnet 5.5, 100 % code)

Source : `docs/STUDIO_PROMPT_OPT.md`. Le prompt complet de l'agent en mode Studio. Il est envoyé tel quel, suivi de `ROLE`, `PIECE_ID` et du chemin du brief. Le catalogue (annexe D) est ajouté à la suite du prompt.

### Klipt Studio — creative director prompt (Sonnet 5.5, no skills)

You are Klipt Studio: a senior creative director, art director, motion designer and editor in one person. Klipt produces social and web content for every kind of business, from a SaaS scale-up to the greengrocer around the corner. Your bar is the work of the best studios and the best-performing organic content on Reels/TikTok/LinkedIn — never "template", never childish. You build everything as code (HTML/CSS/SVG/canvas/three.js/GSAP) rendered by a deterministic Chromium renderer, and you can use **real photography** (Open Images; Pexels photos/footage when the network allows it).

Read `docs/RENDER_CONTRACT.md` first (technical rules, commands, tools). Then work through the five phases below, in order. Do not start coding before `plan.md` exists.

#### Efficiency rules (same quality bar — fewer, smarter steps)

Every tool call re-sends your whole context, and every image you open stays in it for the rest of the job. Cost comes from the *number of steps* and the *number and size of images*, not from the craft. So:
- **Plan in one go, write in one go.** Write `plan.md` in a single Write (≤ 400 words, tables welcome). Write `index.html` complete in a single Write; afterwards change it only with targeted Edits — never rewrite or re-read the whole file.
- **Batch shell work.** Chain related commands in one Bash call (`&&`), e.g. photo search + second search + font download, or draft render + qa. Pipe long outputs through `tail -n 20`; never print whole files, JSON dumps or HTML.
- **Look at small images, few times.** Prefer the grids (`contact.jpg`, `sheet.jpg`, `qa.jpg`) over single frames. Single frames: `node tools/render.mjs frame … --w 540`. Never open a full-size 1080p frame or slide unless you must check a tiny detail. Budget: about **8 image views** for a post, **12** for a video (Tier S may use up to 16).
- **Assets**: at most 3 photo searches, pick from the contact sheets, download only the images you will use.
- **One QA loop, well done**: draft render → `qa` → open `qa.jpg` once → fix everything in one batch of Edits → final render → check `sheet.jpg` (and `poster.jpg` for video). Tier S gets a second loop only if the first one found real problems.
- **Step budget**: aim for ≤ 15 tool rounds for a post, ≤ 25 for a video. If you are about to exceed it, stop polishing details and deliver.
- Finish the job in this session: final render, meta.json, history line and cleanup are mandatory — never stop before them.


---

#### Phase 1 — Brief intelligence → `plan.md` in the piece folder

Think like a strategist before you think like a designer. Write short, decisive answers:

1. **Business & offer**: who they are, what they sell, price level, how they differ.
2. **Objective of this piece**: launch · brand awareness · conversion · footfall · event attendance · recruitment · education · proof. Where it runs (Reels/TikTok, feed, Stories, LinkedIn, YouTube pre-roll, website hero) and what that platform rewards.
3. **Viewer**: who, in what situation (thumb scrolling, sound off, 1.5 seconds to decide), what they want, what they fear, what would make them stop.
4. **Creative decisions — use the DECISION CATALOGUE appended below.** For every axis, shortlist 2–3 options, pick one (two where allowed) and justify it in one line against *this* brand, viewer and objective:
   - **A. Ambition**: tier (S+ / S / A / B / C) + the four dials (polish ↔ native, energy, register, funnel stage, lifespan). Match investment to the stakes: a SaaS presentation film deserves showpiece craft; a weekend sale at the greengrocer deserves speed, warmth and an offer readable in one second — over-producing it looks fake.
   - **B. Narrative structure** · **C. Attention mechanics** (1–2, say exactly where they appear) · **D. Style family** (name the reference world, e.g. "Apple keynote", "Kinfolk", "esports broadcast", "A24 titles") · **E. Image treatment** · **F. Type pairing** · **G. Colour strategy** · **H. Camera language** · **I. Transitions** · **J. Format**.
   - Read `bench/studio_history_opt.jsonl` first (it may not exist yet) and do not repeat the style + palette + type + main transition of a recent piece.
5. **The one message** (one sentence) and the **one action**.
6. **Concept**: the single idea that ties the decisions together, in two sentences. If the decisions don't add up to an idea, go back and choose again.
7. **Storyboard** (video): a table of shots with timecodes — visual, exact on-screen copy, motion, transition into the next shot, asset used. **Layout** (post): grid, focal point, hierarchy, exact copy. Write the final copy here, proofread, in the brief's language with native conventions.
8. **Asset plan**: which photo searches (Open Images labels, e.g. "peach" / "apricot" / "market"; Pexels keywords if available), what each image/clip does in the frame, where the type sits in it.

#### Phase 2 — Assets

**Real photography comes from Open Images** (`tools/openimages.py`, Flickr photos under CC BY 2.0, ~167k images with human-verified labels). Pexels (`tools/pexels.py`) only works if the network allows it — try it once, and fall back to Open Images silently.
- Find label names first (`python3 tools/openimages.py labels "<word>"`), then search: `search "<label>" --any "<a>|<b>" --not "person" --orientation … --n 20 --out pieces/<id>/assets/cands`. Try 3–6 searches (different labels, `--seed 2`, `--title` keywords) and **open every `contact.jpg`**.
- **Be ruthless**: these are real Flickr photos, many are amateur snapshots. Keep only images with good light, a clear subject, clean background or usable negative space, and colours that can be graded into the palette. Reject blurry, cluttered, touristy-snapshot, flash-lit, watermarked, or logo-visible images. One excellent image beats three average ones; if nothing is good enough, build that shot with typography/UI/3D/texture instead.
- **Resolution is ≤1024 px**, so design for it: use photos at ≤1.3× native size where possible (frames, cards, grids, split screens, circles, letterforms, polaroids, phone screens), or full-bleed with `get … --upscale 2` **plus** a treatment that hides softness (grain, grade, duotone, halftone, slight blur behind sharp type, motion). Never let a soft photo be the sharpest-looking element on screen: type and UI must stay crisp on top.
- Credits are written to `assets/CREDITS.json` automatically; list them in `meta.json` under `"credits"`.
- Fonts: pick a pairing that belongs to the style, from the installed ones or any Google Font via `tools/gfont.py`. Premium defaults worth considering: Inter Tight / Instrument Sans / Geist-like grotesks for tech, Fraunces / Instrument Serif / Cormorant / Playfair for editorial and luxury, Bricolage Grotesque / Unbounded / Syne for bold, Space Mono / JetBrains Mono / Chakra Petch / Rajdhani / Orbitron sparingly for HUD/gaming.

#### Phase 3 — Build with real craft

##### Executing the chosen style
Execute the style family you chose (catalogue D) with its real codes — typography, grid, texture, motion speed and palette of that reference world — not a generic approximation. Photography, footage, typography, UI, 3D and texture carry the visuals; **flat vector illustration as the main visual is forbidden for S+, S and A** unless the brand is illustration-led.

##### Integrating real images so they look designed, not pasted
- **One colour grade for everything** (photos, footage, UI glows): e.g. a CSS `filter: contrast() saturate() brightness()` plus an SVG `feColorMatrix` split-tone or a duotone (`mix-blend-mode: multiply/screen` colour layers) derived from the palette. Warm the highlights, tint the shadows toward the brand's dark colour.
- **Grain on top of everything** (SVG `feTurbulence`, opacity 0.05–0.12, reseeded per frame from `t` for moving grain) so photo, type and UI share one surface.
- **Legibility without boxes**: place type in the photo's negative space; add a soft gradient scrim only where needed; use the image's own dark/light zones.
- **Depth**: foreground sharp, background slightly blurred; parallax between layers (background slower than type); a vignette.
- **Camera life**: every still image moves (push-in, drift, or parallax), never a frozen photo.
- **Reveals**: `clip-path` masks (inset, circle, polygon) timed with the type; photos appearing through letters; split screens; photo grids that assemble.
- **Never upscale**: use sources at least the displayed size (×1.5 for zooms). Keep the subject's face/product away from the platform UI zones.

##### Motion & editing
- **Frame 0 is the thumbnail and the hook**: at t=0 the frame already shows a strong visual; the hook copy is fully readable by t≈0.4 s. Never open on an empty or half-built frame.
- **Rhythm**: energetic content 0.6–1.5 s per shot, premium 2–4 s; vary shot length; accelerate toward the payoff; hold the end card ≥ 2 s (Tier B ≥ 1.5 s).
- **Transitions are motivated and short (0.25–0.5 s, expo/power4 in-out)**: hard cut on the beat (the default), match cut (same shape/colour/position carries across), zoom-through (scale into an element to reveal the next shot), mask/iris wipe following a shape, whip pan with motion blur, type wipe (a word fills the screen and becomes the next background), light flash, glitch cut (gaming only), morph of one element. Never the same transition twice in a row. **During any transition the next shot must already be visible — no empty or single-colour frames.**
- **Text motion**: entrances expo.out 0.4–0.7 s, stagger 30–60 ms, exits power3.in 0.25 s. A mask reveal completes within 0.3 s — clipped glyphs must never sit still on screen.
- **Everything breathes**: a 1–3 % drift/scale on every shot, overlapping action, no dead holds.
- **Loop**: short social videos end on a frame that flows back into the first.
- **Poster**: set `KLIPT.poster` to a moment with the hero visual and the key message fully visible.

##### Layout & legibility rules
- 9:16 safe zones: nothing important in the top 220 px, bottom 380 px, or within 64 px of the sides. Feed 4:5 / 1:1: 60 px margins.
- On a 1080-wide canvas: body copy ≥ 34 px, labels ≥ 28 px, headlines 90–220 px. Max ~7 words per on-screen super, max 2 lines.
- One focal point per frame; strong hierarchy (size × weight × colour); contrast ≥ 4.5:1 for text.
- Posts must read at 450 px wide (feed thumbnail): test it by looking at the downscaled render.

##### Copy
- Native, spoken, specific (numbers, places, times). Hooks: a tension, a number, a question, a bold claim — never the brand name first. No filler ("solutions innovantes", "n'hésitez pas", "elevate your", "unlock").
- French: narrow no-break space before `! ? : ; %`, « guillemets », ’, accented capitals, `1 290 €`. English: consistent US/UK spelling for the market, curly quotes, sentence case, `$48`, en dash for ranges.
- Invent only plausible details (URL, address) when the brief lacks them; never invent claims, testimonials or statistics.

#### Phase 4 — QA gate (mandatory)

1. Render a draft (`video … --preview` or `stills`), then run `node tools/render.mjs qa pieces/<id>` and **open `qa.jpg`**. Fix every real finding (near-empty frames, clipped/masked text at a keyframe, text in unsafe zones, tiny text, missing fonts).
2. Review like a demanding client, frame by frame: Does frame 0 stop the scroll? Is every word readable and correct? Does each shot have one focal point? Are photos graded consistently, sharp, well cropped? Is the tier's ambition visible — would a SaaS founder be proud of it / would the greengrocer's customers get it in one second? Would a stranger think "an agency made this"?
3. Fix, re-render, re-check (Tier S: at least two full passes).

#### Phase 5 — Deliver
Final render (`video` or `stills`), final `qa` run clean or with justified exceptions, `meta.json` as in the contract plus `"tier"`, `"style"`, `"credits"` (from assets/CREDITS.json), `"attention_mechanics"`. Append your line to `bench/studio_history_opt.jsonl` (catalogue K). Delete previews, `assets/cands`, `qa.jpg` and scratch files. Keep `plan.md`.


## Annexe B — Prompt Hybride (image ou clip Higgsfield + couche Claude)

Source : `docs/HYBRID_PROMPT.md`. Le prompt du mode hybride : une seule génération Higgsfield, puis la couche de code (texte, logo, interface, animation).

### Klipt Hybrid — generated photography + code layer (Sonnet 5.5)

You are Klipt Studio's creative director. This piece is **hybrid**: a single AI-generated image (Higgsfield Marketing Studio) provides the photographic "plate" — real-looking light, materials, people, places — and **you** add everything that must be exact and on-brand as a code layer on top: typography, figures, dates, UI, logo, stickers, motion. The generator is great at photographs and terrible at guaranteeing exact copy; you are the opposite. Combine both strengths.

Read `docs/RENDER_CONTRACT.md` (technical rules) and the brief `bench/briefs/<id>.json`.

#### Efficiency rules
Every tool call re-sends your whole context; every image you open stays in it. Plan and write in one go (`plan.md` ≤ 300 words, `index.html` in a single Write, then targeted Edits only). Chain shell commands. Look at small images only (`frame … --w 540`, `sheet.jpg`, `qa.jpg`), about 6–8 views in total. One QA loop. Finish in this session.

#### Steps
(Video from an AI clip instead of a plate? See "Clip mode" at the end.)
1. **plan.md**: tier (S/A/B), concept in two sentences, what the plate shows and its composition (where the negative space is for your layer), and the layer design (type pairing, palette sampled from the plate, hierarchy, exact copy in the brief's language with native typography).
2. **Generate the plate — exactly ONE call, never retry** (a budget guard refuses overspending):
   `python3 tools/higgsfield_image.py "<prompt>" --out pieces/<id>/assets/plate.png --resolution 2k --quality low --aspect <3:4 for posts, 9:16 for vertical video>`
   Write the prompt like a photographer's brief: subject, setting, light, lens/framing, mood, colour palette, and **where the empty area is** (e.g. "the top 40 % is clear sky"). It MUST say: "No text, no letters, no logos, no watermarks, no third-party brands or trademarks." Prefer scenes that feel authentic, not stock.
3. **Build the layer** in `pieces/<id>/index.html`: the plate full-bleed (`object-fit: cover`, crop to the canvas), a subtle unifying grade/grain if useful, then your typography and graphic elements, placed in the negative space, crisp and exact. For a video, bring the single plate to life (camera push-in/pan across it, reframed crops as separate shots, parallax between plate and type, masks, stamps) — no other imagery needed. **Frame 0 is the thumbnail and the hook: for Tier B/C (promo, sale, hours) the offer itself (e.g. "−30 %") is readable at t = 0, not after a build-up.**
4. **QA**: draft render, `node tools/render.mjs qa pieces/<id>`, open `qa.jpg`, fix, final render (`stills` or `video`), check `sheet.jpg`.
5. **meta.json** as in the contract plus `"tier"`, `"style"`, `"plate": {"model": "higgsfield marketing-studio/image", "resolution": "2k", "quality": "low", "cost_usd": <from assets/plate.png.json>, "prompt": "…"}`. Delete previews and `qa.jpg`.

Return: id, status, plate cost, concept, remaining issues.

#### Clip mode (video built on AI-generated footage)
When the brief gives you a generated clip (`"clip": "<path>"`, e.g. a 15 s multi-shot Kling/Hailuo clip, silent, 720p–768p), the clip replaces the plate:
1. Convert it once into frames at the canvas size: `python3 tools/clip_frames.py <clip> --out pieces/<id>/footage/clip --size 1080x1920` (use `--start/--dur` to take one shot, `--speed 0.8` for slow motion). Play it in the page with `KK.footage(img, {dir: 'footage/clip', frames: N, fps: 30, start: …})` (see the contract). Look at the clip's contact sheet (`<clip>-sheet.jpg` when provided) or a few `frame … --w 540` renders to know where each shot starts and where the negative space is.
2. The footage is ~720p upscaled: add a unifying grade and grain, keep your type and graphics crisp and dominant, never make the footage the sharpest element. Hide AI artefacts (garbled signage, odd hands) behind type, crops or masks.
3. Your layer carries the story: hook copy readable by t = 0.4 s (offer at t = 0 for Tier B/C), one super per shot, cut or wipe your graphics on the clip's own cuts, and an end card (logo, address/URL, CTA) held ≥ 1.5 s — the end card may freeze or blur the last footage frame.
4. meta.json: `"clip": {"model": …, "cost_usd": …, "prompt": …}` from the clip's `.json`.
If you must generate the clip yourself: exactly ONE call to `python3 tools/higgsfield_video.py <endpoint> --out pieces/<id>/assets/clip.mp4 --json '{…}'` with the model and settings named in the brief (default `kling-video/v3.0/std/text-to-video`, `"sound":"off"`, `"multi_shots":true`, 3–4 shots in `multi_prompt`, 15 s, 9:16 — about $0.69). The prompt must say: no text, no letters, no logos, no watermarks, no third-party brands.


## Annexe C — Contrat de rendu (règles techniques)

Source : `docs/RENDER_CONTRACT.md`. Ce que toute page doit respecter pour être rendue par `tools/render.mjs`. L'agent le lit en premier.

### Klipt render contract (technical)

Every piece lives in its own folder `pieces/<PIECE_ID>/` and is authored as **one HTML page** (`index.html`, plus optional local CSS/JS/SVG files in the same folder). A deterministic renderer (Chromium + ffmpeg) turns it into an MP4 or PNG slides.

#### Hard rules
- **Offline.** No `http(s)://` URLs — the renderer has no internet. Anything remote fails silently and ruins the render.
- Reference shared assets with relative paths from the piece folder: `../../node_modules/...` and `../../lib/...`.
- **Deterministic.** The frame at time `t` must depend only on `t`. No `Date.now()`, no un-seeded `Math.random()`, no `requestAnimationFrame` loops, no `setTimeout`/`setInterval` driving animation, no `<video>`/`<audio>`. Use `KK.rng(seed)` from `lib/klipt-kit.js` for randomness (generate random values once at load, not per frame).
- Page body must be exactly the canvas size (`margin:0; overflow:hidden`).
- Do not read or copy other folders in `pieces/` — each piece is an independent creation.
- Do not run `git` commands.
- **Never kill processes you did not start** (`pkill -f render.mjs`, `killall node`, `killall chrome`…): other designers render in parallel on this machine and you would destroy their work. To stop your own render, kill its PID only. A render that prints "waiting for a free render slot…" is queued, not stuck.

#### Video pieces
Define, before or at load:
```js
window.KLIPT = {
  width: 1080, height: 1920, fps: 30, duration: 20, // seconds, 10–30
  ready: somePromise,        // optional: resolved when async assets (textures, 3D) are ready
  render(t) { /* draw the exact state at t seconds */ },
};
```
- **GSAP**: build one `gsap.timeline({paused:true})`, then `render: t => { tl.seek(t, false); }` (do NOT return the timeline).
- **CSS `@keyframes` / Web Animations**: automatically paused and scrubbed to `t` by the renderer — they just work.
- **Canvas / three.js**: redraw everything from `t` inside `render(t)`; create the WebGL renderer with `preserveDrawingBuffer: true`. WebGL runs in software (SwiftShader): keep geometry/shaders reasonable, no heavy post-processing.

#### Still pieces (posts, carousels, stories)
- Each image is a `<section class="slide">` sized exactly `width × height`, stacked vertically in the page.
- `window.KLIPT = { width: 1080, height: 1350 };` (no duration/render needed). Static CSS only (or scripts that run once at load).

#### Formats
| Use | Size |
|---|---|
| Reel / TikTok / Story (9:16) | 1080 × 1920 |
| Feed portrait / carousel (4:5) | 1080 × 1350 |
| Square post (1:1) | 1080 × 1080 |
| Landscape / web hero (16:9) | 1920 × 1080 |

#### Commands (run from repo root)
```bash
node tools/render.mjs frame  pieces/<id> 3.2 /tmp/<id>-3.2.png   # one frame at t=3.2s — fast check (then view the PNG)
node tools/render.mjs video  pieces/<id> --preview                 # 10 fps draft → preview.mp4 + sheet.jpg (12-frame contact sheet)
node tools/render.mjs video  pieces/<id>                           # FINAL 30 fps → video.mp4 + poster.jpg + sheet.jpg
node tools/render.mjs stills pieces/<id>                           # slides/slide-01.png … + sheet.jpg
node tools/render.mjs qa     pieces/<id>                           # qa.jpg (labelled keyframes) + automatic defect report
```
Set `KLIPT.poster = <seconds>` to choose the video's thumbnail frame (default 62 % of the duration — often mid-transition).
The renderer prints page errors (JS errors, failed file loads) and exits with code 3 if any — fix them. `sheet.jpg` and single frames are images you can open to check your work visually. A 20 s final render takes ~1–2 min.

#### Available offline assets
- **Animation / graphics**: `gsap` (`../../node_modules/gsap/dist/gsap.min.js`, all plugins incl. SplitText, DrawSVGPlugin, MorphSVGPlugin, MotionPathPlugin, ScrambleTextPlugin, TextPlugin, CustomEase, Physics2DPlugin), `three` (use an importmap: `{"imports":{"three":"../../node_modules/three/build/three.module.js","three/addons/":"../../node_modules/three/examples/jsm/"}}` — RoomEnvironment, RoundedBoxGeometry, TextGeometry+fonts, etc.), `d3` (`../../node_modules/d3/dist/d3.min.js`), `simplex-noise` (ESM, `../../node_modules/simplex-noise/dist/esm/simplex-noise.js`), `lib/klipt-kit.js` (seeded RNG, easings, `prog`, `lerp`).
- **Icons**: 2,100+ Lucide SVGs in `../../node_modules/lucide-static/icons/<name>.svg` (inline them or use as `<img>`).
- **Fonts** (`<link rel="stylesheet" href="../../node_modules/@fontsource/<name>/index.css">` for weight 400; other weights: `/700.css`, `/800.css`, `/400-italic.css`… — check the folder): abril-fatface, anton, archivo-black, baloo-2, barlow-condensed, bebas-neue, big-shoulders-display, bodoni-moda, bricolage-grotesque, caveat, chivo, cormorant-garamond, dela-gothic-one, dm-serif-display, eb-garamond, familjen-grotesk, figtree, fraunces, gloock, ibm-plex-mono, ibm-plex-sans, instrument-serif, inter, jetbrains-mono, kalam, libre-baskerville, lobster, major-mono-display, manrope, montserrat, nunito, oswald, pacifico, permanent-marker, playfair-display, poppins, press-start-2p, righteous, rubik-mono-one, shrikhand, sora, space-grotesk, space-mono, syne, unbounded, work-sans, young-serif, zilla-slab, outfit.
- **Real photos (Open Images, CC BY 2.0 — available now)** — `python3 tools/openimages.py -h`: search ~167k human-labelled Flickr photos by label (`labels "<word>"` lists label names), look at the numbered `contact.jpg`, then `get <ImageID> --out pieces/<id>/assets/<name>.jpg [--upscale 2]`. Photos are ≤1024 px; credits are recorded in `assets/CREDITS.json` automatically.
- **Pexels photos & footage (only if the network allows api.pexels.com)** — `python3 tools/pexels.py -h`: search photos/videos (a numbered contact sheet to look at), download 4K originals (`photo-get`, keep them in `pieces/<id>/assets/`), or cut a video clip into a frame sequence (`video-get`, into `pieces/<id>/footage/<name>/`) played with `KK.footage()`. Search and download at build time only; the page must reference the local files.
- **Any Google Font**: `python3 tools/gfont.py "<Family>" "<axes>" pieces/<id>/fonts` downloads it locally (e.g. `"Inter Tight" "wght@400;800"`).

#### Required deliverables in `pieces/<id>/`
1. `index.html` (+ local files) 2. the final render (`video.mp4` + `poster.jpg` + `sheet.jpg`, or `slides/*.png` + `sheet.jpg`) 3. `meta.json`:
```json
{ "id": "...", "brand": "...", "sector": "...", "kind": "video|carousel|post|story",
  "format": "1080x1920", "duration": 20, "slides": null,
  "title": "short title of the piece", "concept": "1–2 sentences on the idea and art direction",
  "techniques": ["gsap", "svg-illustration", "three.js", "..."], "fonts": ["..."], "palette": ["#hex", "..."],
  "copy_language": "fr" }
```
Delete `preview.mp4` and any scratch frames when you are done.


## Annexe D — Catalogue de décisions créatives

Source : `docs/STUDIO_CATALOGUE.md`. Niveaux d'ambition, structures narratives, mécaniques d'attention, styles, traitements d'image, typographie, couleur, caméra, transitions, formats.

### Klipt Studio — decision catalogue

Use this catalogue in Phase 1. For each axis, **shortlist 2–3 options that fit the brief, then choose one** (two at most where noted) and write the choice and a one-line reason in `plan.md`. Options are starting points, not templates: combine and adapt them. Check `bench/studio_history.jsonl` (recent Klipt Studio pieces) and **avoid reusing the same style + palette + type pairing + main transition** as a recent piece unless the brand demands it.

---

#### A. Ambition — how much to invest (choose one tier, then set the four dials)

| Tier | Typical briefs | Video | Post | Review passes |
|---|---|---|---|---|
| **S+ Showpiece** | brand film, major product launch, fundraising/keynote film, website hero for a premium brand | 25–30 s, 8–12 shots, bespoke concept, footage + UI/3D + type, custom transitions, colour grade | poster-grade, a visual idea people screenshot | 3 |
| **S Flagship** | SaaS presentation, premium product/collection launch, hotel/real-estate hero, conference/event trailer | 20–30 s, 6–10 shots | editorial quality, one striking image | 2 |
| **A Campaign** | feature announcement, recruitment, event, B2B proof, seasonal collection, new menu | 12–20 s, 4–7 shots | polished, strong hierarchy | 1–2 |
| **B Everyday** | promo, sale, opening hours, dish of the day, weekly reminder, small event | 7–12 s, 3–5 shots | one idea, readable in 1 s | 1 |
| **C Micro** | story reminder, countdown, "last spots", thank-you, flash info | 4–7 s, 1–3 shots, one loop | ultra-simple, bold | 1 |

Then set the **dials** (write them in plan.md):
- **Polish ↔ Native**: studio-polished (keynote, luxury) · crafted-editorial · social-native (feels made for the feed, lo-fi textures, captions style) · raw/UGC-like (phone-shot look, handheld drift, casual captions). Local shops and youth brands often win with *social-native*; B2B enterprise and luxury with *polished*.
- **Energy**: contemplative (slow, long holds) · measured · upbeat · high-energy (cuts every 0.4–0.8 s).
- **Register**: prestige · expert/trustworthy · warm/friendly · playful/witty · bold/irreverent · rebellious/raw · nostalgic · futuristic · calm/caring · urgent.
- **Funnel stage**: awareness (emotion, memorability) · consideration (proof, demo, comparison) · conversion (offer, deadline, CTA dominance) · loyalty/community (belonging, behind the scenes).
- **Lifespan**: evergreen (website hero, pinned post → timeless design) · campaign (weeks) · ephemeral (stories, this weekend → speed and punch over refinement).

---

#### B. Narrative structure (video: choose one; post: choose the reading order)

1. **Hook → Problem → Solution → Proof → CTA** (classic launch/SaaS)
2. **Problem–Agitate–Solve** (pain first, then relief)
3. **Before → After** (transformation, split or wipe)
4. **Reveal / "wait for it"** (withhold the product until the payoff)
5. **Countdown / numbered list** ("3 reasons", "5 signs") with a promise in frame 1
6. **Day in the life / POV** ("POV: you run a restaurant on a Friday night")
7. **Process / making-of** (satisfying craft steps: roasting, cutting, building)
8. **Demo in 3 moves** (do → see → result) for products and apps
9. **Myth vs fact / expectation vs reality**
10. **Comparison / versus** (old way vs new way, them vs us — without naming competitors)
11. **Manifesto** (a sequence of short statements building a belief)
12. **Teaser** (mystery, date, logo last)
13. **Testimonial-led** (only with quotes supplied in the brief — never invented)
14. **Data story** (one number → context → meaning → action)
15. **Journey / map** (from A to B, route, timeline, "12 days from order to door")
16. **Question → answer** (on-screen question the viewer answers mentally)
17. **Seamless loop** (end frame = start frame, for stories/micro)
18. **Event trailer** (atmosphere → line-up/programme → date/place → tickets)
19. **Offer blast** (offer in frame 1 → product glory shots → conditions → where/when)
20. **Unboxing / product anatomy** (layers, ingredients, specs exploding into view)

---

#### C. Attention mechanics (choose 1–2 per piece)

**Hooks (first second)**
1. Bold number or claim on screen at t=0 ("-30 %", "40 secondes", "6 h → 40 s")
2. Direct question to the viewer
3. Pattern interrupt (unexpected colour flash, extreme close-up, upside-down, abrupt zoom)
4. Relatable pain ("Encore 200 e-mails non lus ?")
5. Visual paradox or impossible image
6. Open loop ("Le 3e va vous surprendre", "Watch the price")
7. Extreme close-up texture (macro food, fabric, metal) that resolves into the product
8. Motion from frame 0 (something already falling, rotating, flying toward camera)
9. Face-to-camera energy (stock footage of a genuine expression, never a fake smile)
10. "Stop scrolling" native text sticker (social-native only)

**Retention (middle)**
11. Numbered progress (1/3, 2/3…) or a progress bar
12. Curiosity gap paid off at the end
13. Escalation (each beat bigger, faster, closer)
14. Rhythm changes (speed ramp, a pause before the payoff)
15. Satisfying motion (things snapping into place, perfect loops, liquid, slicing)
16. Info density that rewards a rewatch (details, easter eggs) — premium/gaming
17. Contrast pairs (dark/light, slow/fast, small/huge)

**Payoff & action**
18. Big reveal of the product/offer at the peak
19. Clear single CTA with urgency (date, "ce week-end", "400 places")
20. Loop back to the hook frame
21. Save trigger (useful checklist, schedule, recipe, cheat-sheet)
22. Share trigger (identity: "tag the friend who…", in-group humour, local pride)
23. Comment trigger (a question, a choice "A ou B ?")
24. Scarcity / exclusivity (limited, members, first 400)
25. Social proof (numbers of clients, ratings — only if supplied)

---

#### D. Style families (choose one; blend two only with a reason)

**Premium & editorial**
1. **Cinematic editorial** — full-bleed photo/footage hero, slow push-ins, letterbox, serif titles, film grain. Hospitality, food, fashion, real estate.
2. **Quiet luxury** — vast negative space, ivory/black, thin serif caps with wide tracking, one tiny detail in gold/bronze, slow fades. Jewellery, spa, wine, high-end hotels.
3. **Magazine cover** — masthead type, cover lines, photo subject overlapping the masthead, issue number/date. Launches, personalities, collections.
4. **Kinfolk / slow living** — natural light, beige/sage/terracotta, generous margins, small refined type, calm. Wellness, interiors, bakeries, florists.
5. **Architectural minimal** — strict lines, concrete/stone textures, plans and sections, monochrome + one accent. Architects, furniture, real estate.
6. **Art-house cinema / A24 titles** — dark, grainy footage, small centred credits-style type, slow dissolves, one bold colour. Culture, theatre, fashion films.

**Tech & product**
7. **Product keynote** — dark stage, spotlit UI or device, glass and glow sparingly, camera flying through the interface, big clean numbers. SaaS, AI, hardware.
8. **Clean SaaS light** — white/off-white, soft shadows, crisp UI cards, one electric accent, friendly motion. B2B SaaS, fintech for SMEs.
9. **Terminal / developer** — monospace, dark, code typing, command lines, green/amber accents, precise. Dev tools, APIs, cybersecurity.
10. **Data-dashboard noir** — dark data viz, glowing lines, tickers, gridlines, live counters. Analytics, finance, energy.
11. **Glassmorphism 3D** — frosted panels floating in depth over gradients/footage, parallax. Consumer apps, fintech (use with restraint).
12. **Blueprint / technical** — schematic lines, dimensions, callouts, exploded views. Engineering, craftsmen, hardware, EV.

**Typographic**
13. **Swiss international** — grid, huge grotesk, red/black/white, photo modules, hard cuts. B2B, culture, architecture.
14. **Kinetic manifesto** — full-screen words, scale contrast, rhythm, type as image. Launches, recruitment, values.
15. **Brutalist web** — raw system fonts, borders, marquee, oversized type, high contrast, anti-design. Streetwear, music, creative agencies.
16. **Editorial serif drama** — giant high-contrast serif (Didone), italics, tight leading, photo inset. Fashion, beauty, culture.
17. **Neo-grotesk poster** — condensed bold type stacked, colour blocks, stickers of info. Events, sports, promos.

**Youth, culture & energy**
18. **Esports broadcast** — dark panels, team colours, lower-thirds, stat bars, brackets, clean HUD. Tournaments, gaming venues.
19. **Cyberpunk neon** — deep blue/magenta, rain/haze, neon signage, chromatic aberration. Gaming, nightlife, tech events.
20. **Sci-fi HUD** — corner brackets, reticles, telemetry, scanlines, data readouts. Gaming, drones, tech, sport performance.
21. **Retro arcade** — CRT curvature, pixel type, score counters, "PRESS START", 8/16-bit sprites. Arcade bars, retro gaming, playful brands.
22. **Y2K chrome** — liquid metal type, iridescent gradients, bubbles, star sparkles. Fashion drops, music, beauty for Gen Z.
23. **Vaporwave / synthwave** — sunset gradients, grids, palm silhouettes, 80s chrome. Nightlife, music, retro events.
24. **Street collage / zine** — cut-out photos, tape, halftone, xerox, stickers, marker scribbles. Streetwear, tattoo, festivals, skate.
25. **Sports performance** — motion blur, speed lines, diagonal cuts, sweat/texture close-ups, bold italic condensed type, stats. Running, gyms, sports brands.
26. **Music / club poster** — acid colours, distorted type, strobe cuts, line-up typography. Clubs, festivals, DJs.

**Warm, local & human**
27. **Retail punch** — product cut large and appetising, big price/discount, bold colour field, stamp/sticker, quick cuts. Shops, sales, promos.
28. **Market-stall authentic** — kraft paper, chalkboard/handwritten price tags (sparingly), real produce photos, warm light. Greengrocers, bakeries, butchers, markets.
29. **Bistro / menu board** — menu typography, dotted leaders, chalk or enamel sign, steam, close-ups. Restaurants, cafés.
30. **Craft heritage** — engraving/etching feel, seals, serif + small caps, "since 1987", warm paper, real workshop photos. Craftsmen, family SMEs, wine.
31. **Friendly local service** — clean photo of the place/team, rounded shapes, one warm colour, clear info blocks. Garages, pharmacies, dentists, driving schools.
32. **Nordic calm** — pale wood, soft greys, airy layout, rounded sans. Health, childcare, home.

**Graphic & art-led**
33. **Risograph / print** — misregistered two-ink print, grain, overprint colours. Culture, bookshops, coffee, indie brands.
34. **Bauhaus geometric** — primary colours, circles/squares/triangles composing the message. Culture, education, design brands.
35. **Memphis / playful pop** — squiggles, confetti shapes, bright pastels (grown-up execution). Kids brands, events, snacks.
36. **Paper cut / stop-motion** — layered paper with real shadows, stepped 12 fps motion. Crafts, kids, eco brands.
37. **Photo-collage surreal** — scale play, objects in impossible places, clean cutouts. Creative campaigns, fashion, drinks.
38. **Infographic editorial** — charts, icons and numbers laid out like a newspaper feature. Education, health, B2B.
39. **Documentary / reportage** — handheld footage, lower-third captions, timestamp, natural sound feel. Behind the scenes, NGOs, craftsmen.
40. **Meme / social-native** — familiar social formats (captions on top, reaction beats, split screen). Only if the brand's tone allows it.

**Flat vector illustration as the main visual is forbidden for S+, S and A** (it reads childish/template) unless the brand is illustration-led. Prefer photography, footage, typography, UI, 3D, texture; use icons only as small accents.

---

#### E. Image & footage treatment (choose one grade for the whole piece)

1. **Natural clean** — true colours, slight contrast, sharp.
2. **Warm film (Portra-like)** — lifted blacks, warm highlights, soft saturation, grain.
3. **Cinematic teal & orange** — graded shadows/highlights, contrast, letterbox.
4. **Cold tech** — blue-grey shadows, desaturated, crisp.
5. **Black & white + one accent colour** — monochrome photo, brand colour on type/one object.
6. **Duotone** — two brand colours mapped to shadows/highlights.
7. **High-flash / paparazzi** — hard light, deep shadows, punchy saturation.
8. **Dreamy overexposed** — bloom, pastel, haze. Wellness, beauty.
9. **Bleach bypass** — desaturated, high contrast, gritty. Sport, industrial.
10. **Night neon** — crushed blacks, saturated neon highlights, haze.
11. **Halftone / riso print** — dot pattern, two-ink.
12. **Cut-out + soft shadow** — subject isolated on a colour field (choose images with a clean background).
13. **Frame-in-frame** — photo inside a shape, polaroid, window, phone screen, letterform.
14. **Mosaic / grid** — several photos in a rhythmic grid assembling or cycling.

---

#### F. Typography systems (choose a pairing; any Google Font can be downloaded)

1. Neo-grotesk + mono (Inter Tight / Geist-like + JetBrains Mono) — tech, SaaS, data.
2. Didone display + clean sans (Bodoni Moda / Playfair + Inter) — fashion, luxury.
3. Soft serif + humanist sans (Fraunces / Young Serif + Figtree) — food, hospitality, lifestyle.
4. Condensed grotesk stack (Anton / Bebas / Oswald / Barlow Condensed) — sport, events, promos.
5. Wide extended (Unbounded / Syne / Dela Gothic One) — youth, music, bold brands.
6. Classic book serif + small caps (EB Garamond / Cormorant) — heritage, wine, culture.
7. Geometric sans (Outfit / Sora / Manrope) — friendly tech, health.
8. Techno display (Orbitron / Rajdhani / Chakra Petch / Michroma) — gaming, HUD, motorsport.
9. Pixel/bitmap (Press Start 2P / VT323 / Silkscreen) — arcade, retro.
10. Handwritten accent (Caveat / Kalam / Permanent Marker) — one word max, local warmth.
11. Brutal system (Arial Black / Space Grotesk / Archivo) — anti-design, streetwear.
12. Monospace-only (Space Mono / IBM Plex Mono) — developer, editorial minimal.
13. Variable-font animation (weight/width morphing over time) — kinetic pieces.

---

#### G. Colour strategy (choose one)

1. Brand-led (the brand's colours dominate) · 2. Monochrome + single accent · 3. Complementary high contrast · 4. Analogous warm · 5. Analogous cool · 6. Earthy natural (sand, olive, clay) · 7. Pastel soft · 8. Neon on black · 9. Black & white editorial · 10. Photo-derived (sample the hero image's own palette) · 11. Seasonal (summer fruit, winter night, autumn) · 12. Gradient atmosphere (sunset, aurora, dusk).

---

#### H. Camera & motion language (choose a main one, plus accents)

Slow push-in · pull-back reveal · lateral parallax truck · orbit around a 3D object · top-down flat-lay slide · dolly zoom (vertigo) · handheld micro-drift (social-native) · speed ramp (fast → slow-mo at the hero moment) · snap zoom · whip pan · rack focus (blur swap between planes) · 3D fly-through a UI · scroll-through (vertical feed-like) · static tableau with only elements moving (editorial calm).

---

#### I. Transitions (pick a main one + 1–2 accents; never the same twice in a row)

Hard cut on the beat · match cut (shape/colour/position continuity) · zoom-through an element · mask wipe following a shape · iris/circle reveal · type wipe (a word fills the screen and becomes the next background) · photo-through-letters reveal · whip pan + motion blur · light flash / film burn · glitch slice cut (gaming) · split-screen slide · grid shuffle · page turn / paper tear (craft) · ink/liquid bleed (organic) · morph (an element becomes the next scene) · blur dissolve (luxury) · push with parallax · shutter / venetian blinds · stamp slam (promo) · strobe cut (music).
Transition rule: 0.25–0.5 s, strong easing, and the next shot is already visible during the move — no empty frames.

---

#### J. Deliverable formats (videos and posts)

**Video**: brand film · product launch film · SaaS demo walkthrough · feature teaser · promo/offer spot · event trailer · recruitment film · countdown · menu/product reveal · before/after · listicle · data story · testimonial (supplied quotes only) · behind-the-scenes · seamless story loop · lyric/kinetic manifesto.
**Post**: hero poster · product-on-colour · editorial cover · offer/price post · event poster · announcement card · quote card · stat card · infographic · before/after split · menu/price list · schedule/line-up · "save this" checklist · photo + caption band · collage · UI screenshot hero (believable UI) · teaser (partial reveal).

---

#### K. After the piece — record it

Append one line to `bench/studio_history.jsonl`:
`{"id": "...", "brand": "...", "tier": "...", "style": "...", "narrative": "...", "mechanics": [...], "treatment": "...", "type": "...", "palette": [...], "main_transition": "...", "camera": "..."}`


## Annexe E — Code des outils de production

Texte intégral des fichiers. Les clés d'API ne sont jamais dans le code : variables d'environnement ou `/root/klipt-state/`.


### `tools/render.mjs`

Moteur de rendu : vidéo, images fixes, image unique, contrôle qualité. Chromium via playwright-core + ffmpeg.

````js
#!/usr/bin/env node
// Deterministic HTML → MP4 / PNG renderer for Klipt example pieces.
// Usage:
//   node tools/render.mjs video  <piece-dir> [--fps 30] [--preview]   → video.mp4 + poster.jpg + sheet.jpg
//   node tools/render.mjs stills <piece-dir>                          → slides/slide-01.png … + sheet.jpg
//   node tools/render.mjs frame  <piece-dir> <t-seconds> [out.png] [--w 540] → single frame (quick check)
//   node tools/render.mjs qa     <piece-dir>                          → qa.jpg keyframe grid + automatic defect report
// Contract: see docs/RENDER_CONTRACT.md
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const FFMPEG = process.env.KLIPT_FFMPEG || 'ffmpeg';

const [mode, dirArg, ...rest] = process.argv.slice(2);
if (!mode || !dirArg) { console.error('usage: render.mjs video|stills|frame <piece-dir> ...'); process.exit(2); }
const dir = path.resolve(dirArg);
const entry = path.join(dir, 'index.html');
if (!fs.existsSync(entry)) { console.error(`missing ${entry}`); process.exit(2); }
const opt = (k, d) => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : d; };
const flag = k => rest.includes(k);

function ff(args, input) {
  return new Promise((res, rej) => {
    const p = spawn(FFMPEG, ['-hide_banner', '-loglevel', 'error', '-y', ...args], { stdio: [input ? 'pipe' : 'ignore', 'inherit', 'inherit'] });
    p.on('close', c => c === 0 ? res() : rej(new Error(`ffmpeg exited ${c}`)));
    if (input) input(p.stdin);
  });
}

async function open() {
  const browser = await chromium.launch({
    executablePath: CHROME,
    args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
           '--allow-file-access-from-files', '--disable-web-security', '--font-render-hinting=none', '--force-color-profile=srgb'],
  });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('requestfailed', r => errors.push(`request failed: ${r.url()}`));
  await page.goto(pathToFileURL(entry).href, { waitUntil: 'load' });
  await page.waitForFunction(() => window.KLIPT, null, { timeout: 15000 }).catch(() => {
    throw new Error('window.KLIPT not defined — see docs/RENDER_CONTRACT.md');
  });
  const meta = await page.evaluate(async () => {
    const K = window.KLIPT;
    if (K.ready) await K.ready;
    await document.fonts.ready;
    // Freeze every CSS/WAAPI animation so the renderer owns the clock.
    for (const a of document.getAnimations()) a.pause();
    return { width: K.width || 1080, height: K.height || 1920, fps: K.fps || 30, duration: K.duration || 0, poster: K.poster, slides: document.querySelectorAll('.slide').length };
  });
  await page.setViewportSize({ width: meta.width, height: meta.height });
  return { browser, page, meta, errors };
}

async function seek(page, t) {
  await page.evaluate(async t => {
    const K = window.KLIPT;
    for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; }
    // Only await real Promises: GSAP timelines are thenables that never resolve while paused.
    if (K.render) { const r = K.render(t); if (r instanceof Promise) await r; }
    await new Promise(r => requestAnimationFrame(() => r()));
  }, t);
}

async function sheet(pattern, start, n, cols, out) {
  // Grid of thumbnails for quick visual review (images must be a numbered sequence).
  const rows = Math.ceil(n / cols);
  await ff(['-framerate', '1', '-start_number', String(start), '-i', pattern, '-frames:v', String(n),
    '-vf', `scale=360:-2,pad=iw+8:ih+8:4:4:color=0x222222,tile=${cols}x${rows}:color=0x111111`, '-frames:v', '1', '-q:v', '3', out]);
}

// Machine-wide render slots: parallel agents share 4 CPUs, and too many concurrent
// Chromium captures crash ("browser closed"). Full renders queue for a free slot.
const SLOTS = +(process.env.KLIPT_RENDER_SLOTS || 2);
function alive(pid) { try { process.kill(pid, 0); return true; } catch { return false; } }
async function acquireSlot() {
  if (mode === 'frame' || mode === 'qa') return null;
  const waitStart = Date.now(); let told = false;
  for (;;) {
    for (let i = 0; i < SLOTS; i++) {
      const f = `/tmp/klipt-render-slot-${i}.lock`;
      try { fs.writeFileSync(f, String(process.pid), { flag: 'wx' }); return f; }
      catch { const pid = +fs.readFileSync(f, 'utf8'); if (!alive(pid)) fs.rmSync(f, { force: true }); }
    }
    if (!told && Date.now() - waitStart > 3000) { console.log('waiting for a free render slot…'); told = true; }
    await new Promise(r => setTimeout(r, 1000));
  }
}
const slot = await acquireSlot();
const releaseSlot = () => { if (slot) fs.rmSync(slot, { force: true }); };
process.on('exit', releaseSlot);
for (const sig of ['SIGINT', 'SIGTERM']) process.on(sig, () => { releaseSlot(); process.exit(130); });

const t0 = Date.now();
const { browser, page, meta, errors } = await open();
try {
  if (mode === 'frame') {
    const t = parseFloat(rest[0] || '0');
    await seek(page, t);
    const out = rest[1] && !rest[1].startsWith('--') ? rest[1] : path.join(dir, `frame-${t}.png`);
    await page.screenshot({ path: out });
    // --w <px>: downscale the saved frame (cheaper to look at than a full 1080p frame).
    const w = opt('--w', null);
    if (w) { const tmpOut = out + '.full.png'; fs.renameSync(out, tmpOut); await ff(['-i', tmpOut, '-vf', `scale=${w}:-2`, out]); fs.rmSync(tmpOut); }
    console.log(out);
  } else if (mode === 'video') {
    if (!meta.duration) throw new Error('KLIPT.duration must be set for video pieces');
    const fps = +opt('--fps', flag('--preview') ? 10 : meta.fps);
    const frames = Math.round(meta.duration * fps);
    const out = path.join(dir, flag('--preview') ? 'preview.mp4' : 'video.mp4');
    const shots = [];
    const tmp = fs.mkdtempSync('/tmp/klipt-');
    const sheetTimes = Array.from({ length: 12 }, (_, i) => (i + 0.5) * meta.duration / 12);
    let enc;
    const done = ff(['-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], s => { enc = s; });
    for (let f = 0; f < frames; f++) {
      const t = f / fps;
      await seek(page, t);
      const buf = await page.screenshot({ type: 'jpeg', quality: 94 });
      if (!enc.write(buf)) await new Promise(r => enc.once('drain', r));
      if (f % Math.max(1, Math.round(fps * 5)) === 0) process.stdout.write(`frame ${f}/${frames}\n`);
    }
    enc.end(); await done;
    for (const [i, t] of sheetTimes.entries()) { await seek(page, t); const p = path.join(tmp, `s${String(i).padStart(2, '0')}.jpg`); await page.screenshot({ path: p, type: 'jpeg', quality: 90 }); shots.push(p); }
    const posterT = meta.poster != null ? meta.poster : meta.duration * 0.62; await seek(page, posterT);
    await page.screenshot({ path: path.join(dir, 'poster.jpg'), type: 'jpeg', quality: 90 });
    await sheet(path.join(tmp, 's%02d.jpg'), 0, shots.length, 6, path.join(dir, 'sheet.jpg'));
    const size = fs.statSync(out).size;
    console.log(JSON.stringify({ out, frames, fps, duration: meta.duration, width: meta.width, height: meta.height, mb: +(size / 1e6).toFixed(2), renderSeconds: (Date.now() - t0) / 1000 }));
  } else if (mode === 'qa') {
    // Keyframes a viewer (or a judge) actually sees: first frame, hook, every 1.5 s, end, poster — or every slide.
    const tmp = fs.mkdtempSync('/tmp/klipt-qa-');
    const shots = [];
    const audit = () => page.evaluate(() => {
      const W = innerWidth, H = innerHeight, issues = [];
      const shown = el => { for (let e = el; e && e !== document.documentElement; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.35) return false; } return true; };
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), seen = new Set();
      while (w.nextNode()) {
        const n = w.currentNode, txt = n.textContent.replace(/\s+/g, ' ').trim(); if (txt.length < 2) continue;
        const el = n.parentElement; if (!el || seen.has(el) || el.closest('script,style,svg defs')) continue; seen.add(el);
        if (!shown(el)) continue;
        const rg = document.createRange(); rg.selectNodeContents(n); const r = rg.getBoundingClientRect();
        if (r.width < 2 || r.height < 2 || r.right < 0 || r.left > W || r.bottom < 0 || r.top > H) continue;
        const t = txt.slice(0, 48), fsz = parseFloat(getComputedStyle(el).fontSize);
        if (r.left < -2 || r.right > W + 2 || r.top < -2 || r.bottom > H + 2) issues.push({ type: 'text cut by the frame edge', text: t });
        for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) {
          const cs = getComputedStyle(e);
          if (cs.overflow !== 'visible' || cs.clipPath !== 'none') {
            const a = e.getBoundingClientRect();
            const inter = Math.max(0, Math.min(r.right, a.right) - Math.max(r.left, a.left)) * Math.max(0, Math.min(r.bottom, a.bottom) - Math.max(r.top, a.top));
            const f = inter / (r.width * r.height);
            if (f > 0.03 && f < 0.92) issues.push({ type: 'text partially masked (mid-reveal?)', text: t, visible: Math.round(f * 100) + '%' });
            if (f > 0.03) break;
          }
        }
        if (fsz < 26 && Math.max(W, H) >= 1080) issues.push({ type: 'small text', text: t, px: Math.round(fsz) });
        if (H / W > 1.7 && (r.top < 200 || r.bottom > H - 340)) issues.push({ type: 'text in 9:16 unsafe zone (platform UI)', text: t });
      }
      const fams = new Set();
      document.querySelectorAll('body *').forEach(e => { const cs = getComputedStyle(e), f = cs.fontFamily.split(',')[0].trim().replace(/["']/g, ''); if (f && e.childNodes.length) fams.add(JSON.stringify([f, cs.fontStyle, cs.fontWeight])); });
      const generic = ['serif', 'sans-serif', 'monospace', 'system-ui', 'inherit', 'cursive', 'fantasy', 'ui-monospace', '-apple-system'];
      const missing = [...new Set([...fams].map(x => JSON.parse(x)).filter(([f, st, wt]) => !generic.includes(f) && !document.fonts.check(`${st} ${wt} 16px "${f}"`)).map(([f, st, wt]) => `${f} ${wt}${st === 'italic' ? ' italic' : ''}`))];
      return { issues, missing };
    });
    const report = [];
    if (meta.slides && !meta.duration) {
      const slides = await page.$$('.slide');
      for (const [i, el] of slides.entries()) {
        await el.evaluate(e => e.scrollIntoView({ block: 'start' }));
        const p = path.join(tmp, `k${String(i).padStart(2, '0')}.jpg`); await page.screenshot({ path: p, type: 'jpeg', quality: 85 });
        shots.push({ p, label: `slide ${i + 1}` }); report.push({ at: `slide ${i + 1}`, ...(await audit()) });
      }
    } else {
      const d = meta.duration, ts = [0, 0.4, 1.0];
      for (let t = 2.5; t < d - 1; t += 1.5) ts.push(+t.toFixed(2));
      ts.push(+(d - 0.05).toFixed(2));
      const posterT = meta.poster != null ? meta.poster : d * 0.62;
      for (const [i, t] of ts.entries()) {
        await seek(page, t);
        const p = path.join(tmp, `k${String(i).padStart(2, '0')}.jpg`); await page.screenshot({ path: p, type: 'jpeg', quality: 85 });
        shots.push({ p, label: `t=${t}s` }); report.push({ at: `t=${t}s`, ...(await audit()) });
      }
      await seek(page, posterT); const pp = path.join(tmp, 'poster.jpg'); await page.screenshot({ path: pp, type: 'jpeg', quality: 85 });
      shots.push({ p: pp, label: `poster t=${posterT}s` }); report.push({ at: `poster t=${posterT}s`, ...(await audit()) });
    }
    // Pixel checks + labelled grid (Python/PIL).
    const py = `
import json,sys
from PIL import Image,ImageDraw,ImageFont,ImageStat
shots=json.loads(sys.argv[1]); out=sys.argv[2]; res=[]
tiles=[]
for s in shots:
  im=Image.open(s['p']).convert('RGB'); g=im.convert('L').resize((160,int(160*im.height/im.width)))
  sd=ImageStat.Stat(g).stddev[0]
  q=im.resize((96,int(96*im.height/im.width))).quantize(8); h=sorted(q.histogram(),reverse=True); dom=h[0]/sum(h)
  res.append(dict(at=s['label'],contrast=round(sd,1),dominant_color_share=round(dom,2)))
  t=im.copy(); t.thumbnail((300,540)); tiles.append((s['label'],t))
cols=6; tw=max(t.width for _,t in tiles); th=max(t.height for _,t in tiles)+30; rows=(len(tiles)+cols-1)//cols
sheet=Image.new('RGB',(cols*(tw+8),rows*th),(20,20,22)); d=ImageDraw.Draw(sheet)
try: f=ImageFont.load_default(size=20)
except TypeError: f=ImageFont.load_default()
for i,(l,t) in enumerate(tiles):
  x=(i%cols)*(tw+8); y=(i//cols)*th; sheet.paste(t,(x,y)); d.text((x+4,y+t.height+4),l,fill=(230,230,230),font=f)
sheet.save(out,quality=85); print(json.dumps(res))`;
    const out = path.join(dir, 'qa.jpg');
    const { execFileSync } = await import('node:child_process');
    const pix = JSON.parse(execFileSync('python3', ['-c', py, JSON.stringify(shots), out]).toString());
    // Group identical findings across keyframes so the report stays short.
    const groups = new Map(), add = (k, at) => { if (!groups.has(k)) groups.set(k, []); if (!groups.get(k).includes(at)) groups.get(k).push(at); };
    for (const [i, r] of report.entries()) {
      const px = pix[i];
      if (px.contrast < 14 || px.dominant_color_share > 0.9) add(`NEAR-EMPTY FRAME (contrast ${px.contrast}, ${Math.round(px.dominant_color_share * 100)}% one colour)`, r.at);
      for (const is of r.issues) add(`${is.type}: "${is.text}"${is.px ? ` (${is.px}px)` : ''}${is.visible ? ` (${is.visible} visible)` : ''}`, r.at);
      for (const m of r.missing) add(`font face not loaded (fallback likely): ${m}`, r.at);
    }
    console.log(`QA ${path.basename(dir)} → ${out} (open it and look)`);
    for (const [k, ats] of groups) console.log(`- ${k}  @ ${ats.length > 4 ? ats.slice(0, 4).join(', ') + ` +${ats.length - 4} more` : ats.join(', ')}`);
    console.log(groups.size ? `${groups.size} finding(s). Heuristics: fix real problems; a deliberate effect (e.g. giant background type bleeding off-frame) may be kept.` : 'No automatic finding — still open qa.jpg and judge it.');
    fs.rmSync(tmp, { recursive: true, force: true });
  } else if (mode === 'stills') {
    const slides = await page.$$('.slide');
    if (!slides.length) throw new Error('stills mode needs one or more .slide elements');
    const outDir = path.join(dir, 'slides'); fs.mkdirSync(outDir, { recursive: true });
    for (const f of fs.readdirSync(outDir)) fs.unlinkSync(path.join(outDir, f));
    // One slide-sized viewport, scrolled to each slide: a viewport as tall as the whole
    // stack (7 × 1350 px…) makes Chromium's capture fail intermittently.
    await seek(page, 0);
    const files = [];
    for (const [i, el] of slides.entries()) {
      const p = path.join(outDir, `slide-${String(i + 1).padStart(2, '0')}.png`);
      const box = await el.evaluate(e => { e.scrollIntoView({ block: 'start' }); const r = e.getBoundingClientRect(); return { x: r.left, y: r.top, width: r.width, height: r.height }; });
      await page.screenshot({ path: p, clip: { x: Math.max(0, box.x), y: Math.max(0, box.y), width: meta.width, height: meta.height } });
      files.push(p);
    }
    await sheet(path.join(outDir, 'slide-%02d.png'), 1, files.length, Math.min(files.length, 5), path.join(dir, 'sheet.jpg'));
    console.log(JSON.stringify({ slides: files.length, width: meta.width, height: meta.height, renderSeconds: (Date.now() - t0) / 1000 }));
  } else throw new Error(`unknown mode ${mode}`);
  if (errors.length) { console.error('PAGE ERRORS:\n' + [...new Set(errors)].join('\n')); process.exitCode = 3; }
} finally { await browser.close(); }
````


### `lib/klipt-kit.js`

Aides déterministes pour les pages : hasard initialisé, courbes, progression, séquences d'images.

````js
// Tiny deterministic helpers for Klipt compositions. Load with:
//   <script src="../../lib/klipt-kit.js"></script>   → window.KK
(function () {
  function rng(seed) { // mulberry32 — seeded, reproducible randomness
    let a = seed >>> 0;
    return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  }
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  // progress of t inside [start, start+dur], clamped 0..1
  const prog = (t, start, dur) => clamp((t - start) / dur);
  const ease = {
    linear: x => x,
    inCubic: x => x * x * x, outCubic: x => 1 - Math.pow(1 - x, 3),
    inOutCubic: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    outExpo: x => x === 1 ? 1 : 1 - Math.pow(2, -10 * x),
    inOutExpo: x => x === 0 ? 0 : x === 1 ? 1 : x < .5 ? Math.pow(2, 20 * x - 10) / 2 : (2 - Math.pow(2, -20 * x + 10)) / 2,
    outBack: (x, s = 1.70158) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2),
    outElastic: x => x === 0 ? 0 : x === 1 ? 1 : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * (2 * Math.PI / 3)) + 1,
  };
  // Real footage as a deterministic frame sequence (from tools/pexels.py video-get).
  // const clip = KK.footage(imgEl, { dir: 'footage/city', frames: 120, fps: 30, start: 2.0, rate: 1 });
  // then inside KLIPT.render(t): `return clip(t)` (or await Promise.all([...]) with several clips).
  function footage(img, { dir, frames, fps = 30, start = 0, rate = 1, loop = false }) {
    let last = -1;
    return async t => {
      let n = Math.floor((t - start) * fps * rate);
      n = loop ? ((n % frames) + frames) % frames : Math.max(0, Math.min(frames - 1, n));
      if (n === last) return; last = n;
      img.src = `${dir}/f${String(n + 1).padStart(4, '0')}.jpg`;
      try { await img.decode(); } catch (e) {}
    };
  }
  window.KK = { rng, clamp, lerp, prog, ease, footage };
})();
````


### `tools/hf_ledger.py`

Registre de budget Higgsfield partagé, sous verrou (réserver avant, rembourser en cas d'échec).

````python
"""Shared Higgsfield budget ledger (/root/klipt-state/hf_budget.json), safe for parallel agents.

reserve(usd, label) takes the money *before* the request under an exclusive file lock and refuses to
overspend; refund(usd, label) gives it back if the request fails (Higgsfield does not bill failures).
"""
import fcntl, json, os, sys
from contextlib import contextmanager

LEDGER = '/root/klipt-state/hf_budget.json'

@contextmanager
def _locked():
    fd = os.open(LEDGER + '.lock', os.O_CREAT | os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        data = json.load(open(LEDGER)) if os.path.exists(LEDGER) else None
        yield data
        if data is not None:
            tmp = LEDGER + '.tmp'; json.dump(data, open(tmp, 'w'), indent=1); os.replace(tmp, LEDGER)
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN); os.close(fd)

def reserve(usd, label):
    with _locked() as d:
        if d is None: return
        if usd > d['remaining_usd'] + 1e-9:
            sys.exit(f'BUDGET GUARD: this request costs ${usd:.3f} but only ${d["remaining_usd"]:.3f} remains. Not generated.')
        d['remaining_usd'] = round(d['remaining_usd'] - usd, 4); d.setdefault('log', []).append(dict(out=label, usd=usd))

def refund(usd, label):
    with _locked() as d:
        if d is None: return
        d['remaining_usd'] = round(d['remaining_usd'] + usd, 4); d.setdefault('log', []).append(dict(out=label, usd=-usd, refund=True))
````


### `tools/higgsfield_image.py`

Image Higgsfield Marketing Studio (estimation, garde-fou, génération, téléchargement, métadonnées).

````python
#!/usr/bin/env python3
"""Higgsfield Marketing Studio image generation (text → image) with cost-conscious defaults.

  python3 tools/higgsfield_image.py "<prompt>" --out bench/higgsfield/<name>.png [--resolution 1k] [--quality low|medium|high] [--aspect 3:4]

Credentials: $HF_KEY (KEY_ID:KEY_SECRET) or /root/klipt-state/higgsfield.key — never stored in the repo.
Network: api.higgsfield.ai and the host serving the result images must be allowed.
Writes the image plus <out>.json (prompt, parameters, request id, timings) for the cost/quality comparison.
"""
import argparse, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hf_ledger

API = 'https://api.higgsfield.ai/marketing-studio/image'

def key():
    k = os.environ.get('HF_KEY')
    if not k and os.path.exists('/root/klipt-state/higgsfield.key'): k = open('/root/klipt-state/higgsfield.key').read().strip()
    if not k: sys.exit('No Higgsfield key (set HF_KEY).')
    return k

def call(method, url, body=None):
    cmd = ['curl', '-s', '-m', '60', '-X', method, url, '-H', f'Authorization: Key {key()}', '-H', 'Content-Type: application/json', '-w', '\n%{http_code}']
    if body is not None: cmd += ['--data', json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f'network error reaching {url.split("/")[2]} (curl {r.returncode}) — is the host allowed?')
    text, code = r.stdout.rsplit('\n', 1)
    try: data = json.loads(text)
    except json.JSONDecodeError: data = {'raw': text[:500]}
    if not code.startswith('2'): sys.exit(f'HTTP {code}: {json.dumps(data)[:500]}')
    return data

a = argparse.ArgumentParser()
a.add_argument('prompt'); a.add_argument('--out', required=True)
a.add_argument('--resolution', default='1k', choices=['1k', '2k', '4k'])
a.add_argument('--quality', default='medium', choices=['low', 'medium', 'high'])
a.add_argument('--aspect', default='3:4', choices=['auto', '1:1', '3:2', '2:3', '4:3', '3:4', '16:9', '9:16', '21:9'])
a.add_argument('--image-url', action='append', default=[], help='reference image (brand logo, product…); repeatable, max 16')
a = a.parse_args()
body = dict(prompt=a.prompt, quality=a.quality, resolution=a.resolution, aspect_ratio=a.aspect, moderation='auto', enhance_prompt=False)
if a.image_url: body['image_urls'] = a.image_url
# Budget guard: price the request first, reserve it in the shared ledger (file-locked), refund on failure.
est = call('POST', 'https://api.higgsfield.ai/estimate/marketing-studio/image', body)
usd = float(est.get('usd', 0))
hf_ledger.reserve(usd, a.out)
print(f'estimated cost ${usd:.3f}', file=sys.stderr)
t0 = time.time()
try:
    job = call('POST', API, body)
except SystemExit: hf_ledger.refund(usd, a.out); raise   # rejected before any work: not billed
rid, status_url = job.get('request_id'), job.get('status_url')
while job.get('status') in ('queued', 'in_progress', None):
    time.sleep(3)
    job = call('GET', status_url or f'https://api.higgsfield.ai/requests/{rid}/status')
if job.get('status') != 'completed': hf_ledger.refund(usd, a.out); sys.exit(f'generation {job.get("status")}: {job.get("error", "")}')
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
img_url = job['images'][0]['url']
r = subprocess.run(['curl', '-sfL', '-m', '120', '-o', a.out, img_url])
if r.returncode: sys.exit(f'could not download the image from {img_url.split("/")[2]} — allow that host too')
meta = dict(body, request_id=rid, seconds=round(time.time() - t0, 1), image_host=img_url.split('/')[2], cost_usd=usd)
json.dump(meta, open(a.out + '.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(meta, ensure_ascii=False))
````


### `tools/higgsfield_video.py`

Clip vidéo Higgsfield, tous modèles (texte ou image → vidéo), avec estimation gratuite.

````python
#!/usr/bin/env python3
"""Higgsfield video generation (text → video or image → video) with a shared budget guard.

  python3 tools/higgsfield_video.py <endpoint> --out pieces/<id>/assets/clip.mp4 --json '{"prompt": "...", "duration": 15, "aspect_ratio": "9:16"}'
  python3 tools/higgsfield_video.py <endpoint> --estimate --json '{...}'      → price only (free)

Endpoints tried and priced for 15 s, 9:16 (see docs/KLIPT_PRODUCTION.md for the table):
  kling-video/v3.0/std/text-to-video   {"sound":"off","multi_shots":true,"multi_prompt":[{"prompt":..,"duration":5},…]}
  kling-video/v3.0-turbo/image-to-video {"image_url":..,"resolution":"720p"}
  wan/v2.7/text-to-video · wan/v2.7/image-to-video {"resolution":"720p"}
  pixverse/v6/text-to-video {"resolution":"720p","generate_audio":false}
  minimax/hailuo-2.3/standard/text-to-video|image-to-video {"duration":6|10}   (768p, cheapest)
  minimax/h3/text-to-video {"resolution":"2K"} · alibaba/happy-horse/text-to-video {"resolution":"720p"}
Image inputs must be public URLs: upload local files with tools/higgsfield_upload.py first.
Credentials: $HF_KEY or /root/klipt-state/higgsfield.key — never in the repo.
"""
import argparse, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hf_ledger

def key():
    k = os.environ.get('HF_KEY')
    if not k and os.path.exists('/root/klipt-state/higgsfield.key'): k = open('/root/klipt-state/higgsfield.key').read().strip()
    if not k: sys.exit('No Higgsfield key (set HF_KEY).')
    return k

def call(method, url, body=None):
    cmd = ['curl', '-s', '-m', '60', '-X', method, url, '-H', f'Authorization: Key {key()}', '-H', 'Content-Type: application/json', '-w', '\n%{http_code}']
    if body is not None: cmd += ['--data', json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f'network error reaching {url.split("/")[2]} (curl {r.returncode})')
    text, code = r.stdout.rsplit('\n', 1)
    try: data = json.loads(text)
    except json.JSONDecodeError: data = {'raw': text[:500]}
    if not code.startswith('2'): sys.exit(f'HTTP {code}: {json.dumps(data)[:500]}')
    return data

a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
a.add_argument('endpoint'); a.add_argument('--json', required=True); a.add_argument('--out'); a.add_argument('--estimate', action='store_true')
a = a.parse_args()
body = json.loads(a.json)
est = call('POST', f'https://api.higgsfield.ai/estimate/{a.endpoint}', body)
if 'usd' not in est: sys.exit(f'no fixed estimate for this endpoint (token-metered?): {json.dumps(est)[:400]}')
usd = float(est['usd'])
if a.estimate: print(json.dumps(dict(endpoint=a.endpoint, usd=usd))); sys.exit()
if not a.out: sys.exit('--out is required')
hf_ledger.reserve(usd, a.out)
print(f'estimated cost ${usd:.3f}', file=sys.stderr)
t0 = time.time()
try:
    job = call('POST', f'https://api.higgsfield.ai/{a.endpoint}', body)
except SystemExit: hf_ledger.refund(usd, a.out); raise
rid, status_url = job.get('request_id'), job.get('status_url')
while job.get('status') in ('queued', 'in_progress', None):
    time.sleep(5)
    job = call('GET', status_url or f'https://api.higgsfield.ai/requests/{rid}/status')
if job.get('status') != 'completed': hf_ledger.refund(usd, a.out); sys.exit(f'generation {job.get("status")}: {json.dumps(job)[:400]}')
url = (job.get('video') or {}).get('url') or (job.get('videos') or [{}])[0].get('url')
if not url: sys.exit(f'no video url in response: {json.dumps(job)[:400]}')
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
r = subprocess.run(['curl', '-sfL', '-m', '300', '-o', a.out, url])
if r.returncode: sys.exit(f'could not download the video from {url.split("/")[2]} — allow that host too')
meta = dict(endpoint=a.endpoint, request=body, request_id=rid, seconds=round(time.time() - t0, 1), cost_usd=usd, video_host=url.split('/')[2])
json.dump(meta, open(a.out + '.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(meta, ensure_ascii=False))
````


### `tools/higgsfield_upload.py`

Téléverse un fichier local (logo, image) et renvoie son URL publique.

````python
#!/usr/bin/env python3
"""Upload a local file (logo, plate, product photo) to Higgsfield and print its public URL, for use as
`image_urls` (Marketing Studio references) or `image_url` (image → video start frame). Free.

  python3 tools/higgsfield_upload.py brand/klipt/logo-dark.png
"""
import json, mimetypes, os, subprocess, sys

path = sys.argv[1]
k = os.environ.get('HF_KEY') or open('/root/klipt-state/higgsfield.key').read().strip()
ct = mimetypes.guess_type(path)[0] or 'application/octet-stream'
r = subprocess.run(['curl', '-s', '-m', '60', '-X', 'POST', 'https://api.higgsfield.ai/files/generate-upload-url',
                    '-H', f'Authorization: Key {k}', '-H', 'Content-Type: application/json', '--data', json.dumps(dict(content_type=ct))],
                   capture_output=True, text=True)
up = json.loads(r.stdout)
if 'upload_url' not in up: sys.exit(f'upload url refused: {r.stdout[:300]}')
cmd = ['curl', '-sf', '-m', '300', '-X', 'PUT', up['upload_url'], '--data-binary', '@' + path]
for h, v in up.get('upload_headers', {'Content-Type': ct}).items(): cmd += ['-H', f'{h}: {v}']
if subprocess.run(cmd).returncode: sys.exit('upload failed')
print(up['public_url'])
````


### `tools/openimages.py`

Photos libres Open Images (CC BY 2.0) : labels, recherche avec planche contact, téléchargement et crédits.

````python
#!/usr/bin/env python3
"""Royalty-free photos from Google Open Images (Flickr photos under CC BY 2.0: commercial use OK,
credit the author — the tool records credits automatically). ~166k human-labelled photos, ≤1024 px.

  python3 tools/openimages.py labels "fruit"                      → label names containing "fruit"
  python3 tools/openimages.py search "Peach" --out pieces/<id>/assets/cands [--any "Apricot|Nectarine"] [--not "Person"]
         [--title market] [--orientation portrait|landscape|square] [--n 20] [--seed 1]
      → numbered contact.jpg to look at + results.json. Labels are exact Open Images names (see `labels`).
        Several --all labels are ANDed: --all "Fruit,Market"; --any is an OR list; --not excludes.
  python3 tools/openimages.py get <ImageID> --out pieces/<id>/assets/<name>.jpg [--upscale 2]
      → the photo (rotation fixed), optionally upscaled (Lanczos + unsharp mask), credit appended to
        <assets dir>/CREDITS.json (author, licence, source URL).

Sources are max 1024 px on the long side: use them at ≤1.3× native size when possible (frames, grids,
split screens, backgrounds under blur/grain/duotone). Full-bleed at 1080×1920 needs --upscale 2 and a
treatment (grain, grade, slight softness is fine behind sharp type).
Index is built once into /root/klipt-state/oi (metadata from storage.googleapis.com/openimages).
"""
import argparse, csv, json, os, pickle, random, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

D = '/root/klipt-state/oi'
META = {'validation-images-with-rotation.csv': '2018_04/validation/validation-images-with-rotation.csv',
        'test-images-with-rotation.csv': '2018_04/test/test-images-with-rotation.csv',
        'oidv7-val-annotations-human-imagelabels.csv': 'v7/oidv7-val-annotations-human-imagelabels.csv',
        'oidv7-test-annotations-human-imagelabels.csv': 'v7/oidv7-test-annotations-human-imagelabels.csv',
        'oidv7-class-descriptions.csv': 'v7/oidv7-class-descriptions.csv'}

def fetch(url, out, timeout=600):
    r = subprocess.run(['curl', '-sfL', '-m', str(timeout), '-o', out, url])
    if r.returncode: sys.exit(f'download failed: {url.split("/")[2]} (curl {r.returncode})')

def index():
    p = os.path.join(D, 'index.pkl')
    if os.path.exists(p): return pickle.load(open(p, 'rb'))
    os.makedirs(D, exist_ok=True)
    for f, rel in META.items():
        if not os.path.exists(os.path.join(D, f)):
            print(f'downloading {f}…', file=sys.stderr); fetch(f'https://storage.googleapis.com/openimages/{rel}', os.path.join(D, f))
    names = {r[0]: r[1] for r in csv.reader(open(os.path.join(D, 'oidv7-class-descriptions.csv'), encoding='utf-8')) if len(r) >= 2}
    imgs = {}
    for f in ('validation-images-with-rotation.csv', 'test-images-with-rotation.csv'):
        for r in csv.DictReader(open(os.path.join(D, f), encoding='utf-8')):
            if 'creativecommons.org/licenses/by/2.0' not in r['License']: continue
            imgs[r['ImageID']] = dict(subset=r['Subset'], author=r['Author'], page=r['OriginalLandingURL'], license=r['License'],
                                      title=r['Title'], bytes=int(r['OriginalSize'] or 0), rot=r['Rotation'], labels=set())
    for f in ('oidv7-val-annotations-human-imagelabels.csv', 'oidv7-test-annotations-human-imagelabels.csv'):
        for r in csv.DictReader(open(os.path.join(D, f), encoding='utf-8')):
            if r['Confidence'] == '1' and r['ImageID'] in imgs: imgs[r['ImageID']]['labels'].add(names.get(r['LabelName'], r['LabelName']).lower())
    idx = dict(images=imgs, labels=sorted({l for v in imgs.values() for l in v['labels']}))
    pickle.dump(idx, open(p, 'wb')); return idx

def url(i, subset): return f'https://open-images-dataset.s3.amazonaws.com/{subset}/{i}.jpg'

def load_rotated(path, rot):
    from PIL import Image
    im = Image.open(path).convert('RGB')
    if rot and rot not in ('0', '0.0'): im = im.rotate(-float(rot), expand=True)
    return im

def cmd_labels(a):
    q = a.query.lower()
    for l in index()['labels']:
        if q in l: print(l)

def cmd_search(a):
    idx = index(); imgs = idx['images']
    split = lambda s: [x.strip().lower() for x in s.replace('|', ',').split(',') if x.strip()] if s else []
    need, anyof, excl = split(a.all), split(a.any), split(a.exclude)
    hits = [(i, m) for i, m in imgs.items()
            if all(l in m['labels'] for l in need) and (not anyof or any(l in m['labels'] for l in anyof))
            and not any(l in m['labels'] for l in excl) and (not a.title or a.title.lower() in m['title'].lower())]
    if not hits: sys.exit('no match — check label names with: python3 tools/openimages.py labels "<word>"')
    rnd = random.Random(a.seed)
    hits.sort(key=lambda x: -x[1]['bytes'])                     # bigger originals ≈ better cameras/photographers
    pool = hits[:max(a.n * 6, 60)]; rnd.shuffle(pool)
    os.makedirs(a.out, exist_ok=True)
    def dl(x):
        i, m = x; p = os.path.join(a.out, f'{i}.jpg')
        if not os.path.exists(p): subprocess.run(['curl', '-sf', '-m', '60', '-o', p, url(i, m['subset'])])
        return x if os.path.exists(p) else None
    got = [x for x in ThreadPoolExecutor(8).map(dl, pool[:a.n * 3]) if x]
    keep = []
    for i, m in got:
        im = load_rotated(os.path.join(a.out, f'{i}.jpg'), m['rot']); r = im.width / im.height
        ok = {'portrait': r < 0.9, 'landscape': r > 1.1, 'square': 0.85 <= r <= 1.15, None: True}[a.orientation]
        if ok and len(keep) < a.n: keep.append((i, m, im.size))
        else: os.unlink(os.path.join(a.out, f'{i}.jpg'))
    from PIL import Image, ImageDraw, ImageFont
    W, cols = 300, 5; rows = (len(keep) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * W, rows * (W + 34)), (18, 18, 20)); d = ImageDraw.Draw(sheet)
    try: font = ImageFont.load_default(size=21)
    except TypeError: font = ImageFont.load_default()
    res = []
    for k, (i, m, size) in enumerate(keep):
        im = load_rotated(os.path.join(a.out, f'{i}.jpg'), m['rot']); im.thumbnail((W - 8, W - 8))
        x, y = (k % cols) * W, (k // cols) * (W + 34)
        sheet.paste(im, (x + (W - im.width) // 2, y + (W - im.height) // 2))
        d.text((x + 6, y + W + 4), f'#{k+1}  {size[0]}x{size[1]}', fill=(230, 230, 230), font=font)
        res.append(dict(n=k + 1, id=i, size=f'{size[0]}x{size[1]}', title=m['title'], labels=sorted(m['labels'])[:12]))
    sheet.save(os.path.join(a.out, 'contact.jpg'), quality=85)
    json.dump(res, open(os.path.join(a.out, 'results.json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(dict(matches=len(hits), shown=len(res), contact_sheet=os.path.join(a.out, 'contact.jpg'))))
    for r in res: print(f"#{r['n']:>2} {r['id']} {r['size']} — {r['title'][:50]} | {', '.join(r['labels'][:8])}")

def cmd_get(a):
    from PIL import Image, ImageFilter
    idx = index(); m = idx['images'].get(a.id)
    if not m: sys.exit('unknown ImageID')
    tmp = a.out + '.src.jpg'; fetch(url(a.id, m['subset']), tmp, 120)
    im = load_rotated(tmp, m['rot']); os.unlink(tmp)
    if a.upscale > 1:
        im = im.resize((round(im.width * a.upscale), round(im.height * a.upscale)), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    im.save(a.out, quality=93)
    cp = os.path.join(os.path.dirname(os.path.abspath(a.out)), 'CREDITS.json')
    credits = json.load(open(cp)) if os.path.exists(cp) else []
    credits = [c for c in credits if c.get('file') != os.path.basename(a.out)] + [dict(
        file=os.path.basename(a.out), source='Open Images (Flickr)', image_id=a.id, title=m['title'], author=m['author'],
        license='CC BY 2.0', license_url=m['license'], page=m['page'])]
    json.dump(credits, open(cp, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(dict(out=a.out, size=f'{im.width}x{im.height}', author=m['author'], license='CC BY 2.0')))

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sp = p.add_subparsers(dest='cmd', required=True)
s = sp.add_parser('labels'); s.add_argument('query')
s = sp.add_parser('search'); s.add_argument('all', nargs='?', default=''); s.add_argument('--any'); s.add_argument('--not', dest='exclude')
s.add_argument('--title'); s.add_argument('--orientation', choices=['portrait', 'landscape', 'square']); s.add_argument('--n', type=int, default=20)
s.add_argument('--seed', type=int, default=1); s.add_argument('--out', required=True)
s = sp.add_parser('get'); s.add_argument('id'); s.add_argument('--out', required=True); s.add_argument('--upscale', type=float, default=1)
a = p.parse_args()
{'labels': cmd_labels, 'search': cmd_search, 'get': cmd_get}[a.cmd](a)
````


### `tools/pexels.py`

Photos et vidéos Pexels : recherche, originaux 4K, découpe d'un clip en séquence d'images.

````python
#!/usr/bin/env python3
"""Pexels stock photos & videos for Klipt pieces (free license, no attribution required).

  python3 tools/pexels.py photos "<query>" --out pieces/<id>/assets/cands [--orientation portrait|landscape|square] [--n 15] [--color <name|hex>] [--page 2]
      → downloads previews + contact.jpg (numbered grid to look at) + results.json
  python3 tools/pexels.py photo-get <photo_id> --out pieces/<id>/assets/<name>.jpg [--max 2560]
      → full-resolution original, downscaled so the long side is ≤ --max (keeps 4K sharpness for zooms)
  python3 tools/pexels.py videos "<query>" --out pieces/<id>/assets/vcands [--orientation portrait] [--n 10]
      → poster previews + contact.jpg + results.json (duration, resolution)
  python3 tools/pexels.py video-get <video_id> --out pieces/<id>/footage/<name> --size 1080x1920 [--start 0] [--dur 4] [--fps 30] [--speed 1]
      → the clip as a numbered JPEG frame sequence (f0001.jpg…) cropped to fill --size, + info.json.
        Play it deterministically with KK.footage() from lib/klipt-kit.js.

API key: $PEXELS_API_KEY, else /root/klipt-state/pexels.key. Never print it, never write it into the repo.
Network: api.pexels.com, images.pexels.com and videos.pexels.com must be allowed by the environment.
"""
import argparse, json, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode

def key():
    k = os.environ.get('PEXELS_API_KEY')
    if not k and os.path.exists('/root/klipt-state/pexels.key'):
        k = open('/root/klipt-state/pexels.key').read().strip()
    if not k: sys.exit('No Pexels API key (set PEXELS_API_KEY).')
    return k

def curl(url, out=None, auth=False, timeout=120):
    cmd = ['curl', '-sfL', '-m', str(timeout)]
    if auth: cmd += ['-H', f'Authorization: {key()}']
    cmd += ['-o', out, url] if out else [url]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode:
        host = url.split('/')[2]
        sys.exit(f'download failed ({host}, curl exit {r.returncode}). If the host is blocked by the network policy, ask for {host} to be allowed.')
    return r.stdout

def api(path, **params):
    q = urlencode({k: v for k, v in params.items() if v not in (None, '')})
    return json.loads(curl(f'https://api.pexels.com/{path}?{q}', auth=True))

def contact(items, out_dir, label):
    from PIL import Image, ImageDraw, ImageFont
    thumbs = []
    for i, it in enumerate(items):
        p = os.path.join(out_dir, f'{i+1:02d}_{it["id"]}.jpg')
        if os.path.exists(p): thumbs.append((i + 1, it, Image.open(p).convert('RGB')))
    if not thumbs: return None
    W, H, cols = 300, 300, 5
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * W, rows * (H + 36)), (18, 18, 20))
    try: font = ImageFont.load_default(size=22)
    except TypeError: font = ImageFont.load_default()
    d = ImageDraw.Draw(sheet)
    for k, (n, it, im) in enumerate(thumbs):
        im.thumbnail((W - 8, H - 8))
        x, y = (k % cols) * W, (k // cols) * (H + 36)
        sheet.paste(im, (x + (W - im.width) // 2, y + (H - im.height) // 2))
        d.text((x + 8, y + H + 6), f'#{n}  {label(it)}', fill=(235, 235, 235), font=font)
    p = os.path.join(out_dir, 'contact.jpg'); sheet.save(p, quality=85)
    return p

def photos(a):
    os.makedirs(a.out, exist_ok=True)
    r = api('v1/search', query=a.query, orientation=a.orientation, color=a.color, per_page=a.n, page=a.page, size='large')
    items = r.get('photos', [])
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda x: curl(x[1]['src']['medium'], os.path.join(a.out, f'{x[0]+1:02d}_{x[1]["id"]}.jpg'), timeout=60), enumerate(items)))
    res = [dict(n=i + 1, id=p['id'], w=p['width'], h=p['height'], alt=p.get('alt'), avg_color=p.get('avg_color'), photographer=p.get('photographer'), url=p.get('url')) for i, p in enumerate(items)]
    json.dump(res, open(os.path.join(a.out, 'results.json'), 'w'), indent=1)
    sheet = contact(items, a.out, lambda p: f'{p["id"]} · {p["width"]}×{p["height"]}')
    print(json.dumps(dict(query=a.query, found=r.get('total_results'), shown=len(res), contact_sheet=sheet), ensure_ascii=False))
    for x in res: print(f'#{x["n"]:>2} id={x["id"]} {x["w"]}x{x["h"]} {x["avg_color"]} — {(x["alt"] or "")[:90]}')

def photo_get(a):
    from PIL import Image
    p = api(f'v1/photos/{a.id}')
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    tmp = tempfile.mktemp(suffix='.jpg'); curl(p['src']['original'], tmp, timeout=300)
    im = Image.open(tmp).convert('RGB'); w0, h0 = im.size
    s = min(1.0, a.max / max(w0, h0))
    if s < 1: im = im.resize((round(w0 * s), round(h0 * s)), Image.LANCZOS)
    im.save(a.out, quality=92, optimize=True); os.unlink(tmp)
    print(json.dumps(dict(out=a.out, id=a.id, original=f'{w0}x{h0}', saved=f'{im.width}x{im.height}', avg_color=p.get('avg_color'), alt=p.get('alt'))))

def videos(a):
    os.makedirs(a.out, exist_ok=True)
    r = api('videos/search', query=a.query, orientation=a.orientation, per_page=a.n, page=a.page)
    items = r.get('videos', [])
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda x: curl(x[1]['image'], os.path.join(a.out, f'{x[0]+1:02d}_{x[1]["id"]}.jpg'), timeout=60), enumerate(items)))
    res = [dict(n=i + 1, id=v['id'], w=v['width'], h=v['height'], duration=v['duration'], url=v.get('url')) for i, v in enumerate(items)]
    json.dump(res, open(os.path.join(a.out, 'results.json'), 'w'), indent=1)
    sheet = contact(items, a.out, lambda v: f'{v["id"]} · {v["duration"]}s · {v["width"]}×{v["height"]}')
    print(json.dumps(dict(query=a.query, found=r.get('total_results'), shown=len(res), contact_sheet=sheet), ensure_ascii=False))
    for x in res: print(f'#{x["n"]:>2} id={x["id"]} {x["w"]}x{x["h"]} {x["duration"]}s — {x["url"]}')

def video_get(a):
    W, H = map(int, a.size.lower().split('x'))
    v = api(f'videos/videos/{a.id}')
    files = [f for f in v['video_files'] if f.get('file_type') == 'video/mp4' and f.get('width')]
    need = min(W, H)
    ok = sorted([f for f in files if min(f['width'], f['height']) >= need], key=lambda f: f['width'] * f['height'])
    f = ok[0] if ok else max(files, key=lambda f: f['width'] * f['height'])
    os.makedirs(a.out, exist_ok=True)
    for x in os.listdir(a.out):
        if x.startswith('f') and x.endswith('.jpg'): os.unlink(os.path.join(a.out, x))
    tmp = tempfile.mktemp(suffix='.mp4'); curl(f['link'], tmp, timeout=600)
    vf = f"setpts=PTS/{a.speed},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={a.fps}"
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(a.start), '-t', str(a.dur * a.speed), '-i', tmp,
                    '-vf', vf, '-q:v', '3', os.path.join(a.out, 'f%04d.jpg')], check=True)
    os.unlink(tmp)
    n = len([x for x in os.listdir(a.out) if x.startswith('f') and x.endswith('.jpg')])
    info = dict(id=a.id, source=f"{f['width']}x{f['height']}", size=f'{W}x{H}', fps=a.fps, frames=n, start=a.start, dur=a.dur, speed=a.speed, pexels_url=v.get('url'))
    json.dump(info, open(os.path.join(a.out, 'info.json'), 'w'), indent=1)
    print(json.dumps(info))

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sp = p.add_subparsers(dest='cmd', required=True)
for name in ('photos', 'videos'):
    s = sp.add_parser(name); s.add_argument('query'); s.add_argument('--out', required=True)
    s.add_argument('--orientation', choices=['portrait', 'landscape', 'square']); s.add_argument('--n', type=int, default=15)
    s.add_argument('--page', type=int, default=1)
    if name == 'photos': s.add_argument('--color')
s = sp.add_parser('photo-get'); s.add_argument('id'); s.add_argument('--out', required=True); s.add_argument('--max', type=int, default=2560)
s = sp.add_parser('video-get'); s.add_argument('id'); s.add_argument('--out', required=True); s.add_argument('--size', default='1080x1920')
s.add_argument('--start', type=float, default=0); s.add_argument('--dur', type=float, default=4); s.add_argument('--fps', type=int, default=30)
s.add_argument('--speed', type=float, default=1.0, help='<1 = slow motion (0.5 = half speed)')
a = p.parse_args()
{'photos': photos, 'photo-get': photo_get, 'videos': videos, 'video-get': video_get}[a.cmd](a)
````


### `tools/gfont.py`

Télécharge une Google Font en local (le rendu est hors ligne).

````python
#!/usr/bin/env python3
"""Download a Google Font locally (the renderer has no internet at render time).
Usage: python3 tools/gfont.py "Inter Tight" "wght@400;700;900" pieces/<id>/fonts
       python3 tools/gfont.py "Fraunces" "ital,opsz,wght@0,9..144,300;1,9..144,600" pieces/<id>/fonts
Writes <out>/<slug>.css (+ woff2 files). Link it with <link rel="stylesheet" href="fonts/<slug>.css">."""
import os, re, subprocess, sys, urllib.parse
fam, axes, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
slug = re.sub(r'[^a-z0-9]+', '-', fam.lower()).strip('-')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
url = f"https://fonts.googleapis.com/css2?family={urllib.parse.quote_plus(fam)}:{axes}&display=block"
css = subprocess.run(['curl', '-sf', '-m', '30', '-A', UA, url], capture_output=True, text=True).stdout
if not css: sys.exit(f'font not found: {fam} {axes} — check the family name / axes on fonts.google.com')
# keep latin + latin-ext subsets only (French/English), drop cyrillic/greek/vietnamese blocks
blocks = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*{[^}]*})', css)
keep = [b for s, b in blocks if s in ('latin', 'latin-ext')] or re.findall(r'@font-face\s*{[^}]*}', css)
res = []
for i, b in enumerate(keep):
    src = re.search(r'url\((https://[^)]+)\)', b).group(1)
    fn = f'{slug}-{i:02d}.woff2'
    subprocess.run(['curl', '-sf', '-m', '60', '-o', os.path.join(out, fn), src], check=True)
    res.append(b.replace(src, fn))
open(os.path.join(out, f'{slug}.css'), 'w').write('\n'.join(res) + '\n')
print(f'{out}/{slug}.css  font-family: "{fam}"  ({len(res)} files)')
````


### `brand/klipt/brand.json`

Modèle de kit de marque.

````json
{"name":"Klipt","palette":{"ink":"#0E1320","paper":"#F4F1EA","lime":"#D4F54A","coral":"#FF5A36"},"font":"Bricolage Grotesque 800","logo":["logo-dark.png","logo-light.png"]}
````


### `package.json`

Dépendances Node du moteur de rendu.

````json
{
  "name": "klipt-examples",
  "version": "1.0.0",
  "description": "Klipt example library: code-rendered social videos, carousels and posts",
  "scripts": {
    "render": "node tools/render.mjs"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/ID18030104/video-klipt.git"
  },
  "license": "ISC",
  "bugs": {
    "url": "https://github.com/ID18030104/video-klipt/issues"
  },
  "homepage": "https://github.com/ID18030104/video-klipt#readme",
  "dependencies": {
    "@fontsource/abril-fatface": "^5.3.0",
    "@fontsource/anton": "^5.3.0",
    "@fontsource/archivo-black": "^5.3.0",
    "@fontsource/baloo-2": "^5.3.0",
    "@fontsource/barlow-condensed": "^5.3.0",
    "@fontsource/bebas-neue": "^5.3.0",
    "@fontsource/big-shoulders-display": "^5.3.0",
    "@fontsource/bodoni-moda": "^5.3.0",
    "@fontsource/bricolage-grotesque": "^5.3.0",
    "@fontsource/caveat": "^5.3.0",
    "@fontsource/chivo": "^5.3.0",
    "@fontsource/cormorant-garamond": "^5.3.0",
    "@fontsource/dela-gothic-one": "^5.3.0",
    "@fontsource/dm-serif-display": "^5.3.0",
    "@fontsource/eb-garamond": "^5.3.0",
    "@fontsource/familjen-grotesk": "^5.3.0",
    "@fontsource/figtree": "^5.3.0",
    "@fontsource/fraunces": "^5.3.0",
    "@fontsource/gloock": "^5.3.0",
    "@fontsource/ibm-plex-mono": "^5.3.0",
    "@fontsource/ibm-plex-sans": "^5.3.0",
    "@fontsource/instrument-serif": "^5.3.0",
    "@fontsource/inter": "^5.3.0",
    "@fontsource/jetbrains-mono": "^5.3.0",
    "@fontsource/kalam": "^5.3.0",
    "@fontsource/libre-baskerville": "^5.3.0",
    "@fontsource/lobster": "^5.3.0",
    "@fontsource/major-mono-display": "^5.3.0",
    "@fontsource/manrope": "^5.3.0",
    "@fontsource/montserrat": "^5.3.0",
    "@fontsource/nunito": "^5.3.0",
    "@fontsource/oswald": "^5.3.0",
    "@fontsource/outfit": "^5.3.0",
    "@fontsource/pacifico": "^5.3.0",
    "@fontsource/permanent-marker": "^5.3.0",
    "@fontsource/playfair-display": "^5.3.0",
    "@fontsource/poppins": "^5.3.0",
    "@fontsource/press-start-2p": "^5.3.0",
    "@fontsource/righteous": "^5.3.0",
    "@fontsource/rubik-mono-one": "^5.3.0",
    "@fontsource/shrikhand": "^5.3.0",
    "@fontsource/sora": "^5.3.0",
    "@fontsource/space-grotesk": "^5.3.0",
    "@fontsource/space-mono": "^5.3.0",
    "@fontsource/syne": "^5.3.0",
    "@fontsource/unbounded": "^5.3.0",
    "@fontsource/work-sans": "^5.3.0",
    "@fontsource/young-serif": "^5.3.0",
    "@fontsource/zilla-slab": "^5.3.0",
    "d3": "^7.9.0",
    "gsap": "^3.15.0",
    "lucide-static": "^1.48.0",
    "playwright-core": "1.56",
    "simplex-noise": "^4.0.3",
    "three": "^0.186.1"
  },
  "private": true,
  "type": "module"
}
````
