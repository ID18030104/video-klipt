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

@@VIDEO_SECTION@@

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
