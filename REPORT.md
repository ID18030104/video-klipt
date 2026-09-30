# Klipt Lab — quel modèle, quel skill, quelle configuration ?

74 pièces (46 vidéos de 10 à 30 s, 28 carrousels, posts et stories) générées par des agents Claude pour 50 marques fictives (SaaS, PME, artisans, commerces de proximité, santé, culture, collectivités, luxe), en français et en anglais. Tout est rendu en code : HTML/CSS/SVG/canvas/three.js, capturé image par image par Chromium, encodé par ffmpeg. Aucune photo ni vidéo de banque d'images (réseau fermé, Higgsfield sans crédit).

Galerie interactive (vidéos, slides, notes, défauts, coûts) : https://claude.ai/artifact/Hsg5U2GQQHs7LmC6skCEQ2

## Protocole

- **8 configurations** : Sonnet 5.5 ou Opus 5.5, sans skill, avec `klipt-craft` (écrit pour ce test) ou avec `taste-express` (skill du dépôt), et deux pipelines multi-agents (directeur artistique Opus → exécutant Sonnet ; exécutant Sonnet → critique Opus → correction Sonnet).
- **Duels** : 3 briefs identiques (barbier Reel 9:16, SaaS vidéo LinkedIn 4:5, plombier carrousel 7 slides) × 8 configurations = 24 pièces, notées par un juge Opus et un juge Sonnet, puis classées par un juge-président Opus.
- **Production** : 50 briefs variés répartis en tourniquet (6 à 7 par configuration, mélange équilibré de formats et de langues), notés par un juge Sonnet.
- **Juges aveugles** : identifiants neutres, fichiers de travail (directions, critiques, design cards) retirés des dossiers avant notation, consigne de ne regarder que les rendus. 9 critères sur 10, pièce publiable telle quelle ou non, liste des défauts.
- **Coûts** : tokens relevés dans les transcripts (entrée, cache lu, cache écrit exacts ; sortie estimée par un modèle calibré sur les appels exacts de la session principale, ±15 %), valorisés au tarif API public (Opus 5.5 : 4 $/20 $ par million de tokens en entrée/sortie ; Sonnet 5.5 : 2 $/10 $ ; cache lu 0,20 $).
- **Temps** : horloge murale de chaque agent, attente de rendu comprise (4 CPU partagés entre 8 à 12 agents), donc gonflé.

## Résultats

| Config | Pièces | Note (juge Sonnet, 74 pièces) | Vidéo | Stills | Publiable | Banc: note 2 juges | Banc: rang | $/pièce | $/vidéo | min/pièce | tokens sortie | note/$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A — Sonnet seul | 9 | 6,33 | 5,80 | 7,00 | 22 % | 6,17 | 6,7 | 0,43 | 0,55 | 11 | 10,666 | 14,7 |
| B — Sonnet + klipt-craft | 9 | 6,44 | 6,00 | 7,00 | 22 % | 6,67 | 4,7 | 0,53 | 0,68 | 11 | 15,940 | 12,2 |
| C — Opus seul | 9 | 6,89 | 6,40 | 7,50 | 67 % | 7,00 | 2,7 | 1,38 | 1,46 | 15 | 22,473 | 5,0 |
| D — Opus + klipt-craft | 10 | 6,80 | 6,33 | 7,50 | 20 % | 6,83 | 2,3 | 1,11 | 1,28 | 12 | 21,417 | 6,1 |
| E — Opus DA → Sonnet | 10 | 6,60 | 6,33 | 7,00 | 30 % | 6,67 | 5,3 | 3,13 | 3,26 | 66 | 58,648 | 2,1 |
| F — Sonnet → critique Opus → Sonnet | 9 | 6,44 | 6,00 | 7,33 | 56 % | 6,50 | 4,3 | 1,73 | 1,95 | 42 | 30,598 | 3,7 |
| G — Opus + taste-express | 9 | 6,78 | 6,50 | 7,33 | 56 % | 6,50 | 2,7 | 3,00 | 3,63 | 43 | 31,108 | 2,3 |
| H — Sonnet + taste-express | 9 | 6,11 | 5,80 | 6,50 | 0 % | 6,50 | 7,3 | 0,80 | 0,92 | 23 | 17,147 | 7,6 |

Note globale = juge Sonnet sur toutes les pièces de la configuration (comparable entre configurations). « Duels » = pièces du banc d'essai, deux juges. Coûts et temps : moyenne par pièce, toutes étapes comprises, hors 10 pièces reprises après le redémarrage du conteneur (coût partiel).

| Regroupement | Note moyenne | Coût / pièce |
|---|---|---|
| Sonnet 5.5 seul (A, B, H) | 6,30 | 0,59 $ |
| Opus 5.5 seul (C, D, G) | 6,82 | 1,73 $ |
| Pipelines Opus + Sonnet (E, F) | 6,53 | 2,67 $ |
| Sans skill (A, C) | 6,61 | 0,93 $ |
| klipt-craft (B, D) | 6,63 | 0,82 $ |
| taste-express (G, H) | 6,44 | 1,76 $ |

## Ce qu'on retient

1. **Opus 5.5 comme créatif donne la meilleure qualité** : +0,5 point sur 10 en moyenne face à Sonnet, surtout sur l'adéquation à la marque, la composition et le texte, pour environ 3 fois le prix. Opus seul (C) a la meilleure note (6,89) et le plus de pièces publiables telles quelles (67 %).
2. **Opus + klipt-craft (D)** coûte 20 % de moins qu'Opus seul (1,11 $ contre 1,38 $ par pièce) avec une note quasi identique et le meilleur rang en duel. C'est le meilleur compromis qualité-prix côté Opus.
3. **Sonnet seul (A)** reste imbattable en volume : 0,43 $ par pièce, 14,7 points par dollar. Ses images fixes sont bonnes (7/10), ses vidéos plus fragiles (5,8/10). klipt-craft améliore Sonnet de peu (B).
4. **taste-express** produit les concepts les plus originaux avec Opus (G : 7,3 en originalité, 1er du duel carrousel), mais coûte 3 $ par pièce. Avec Sonnet (H), c'est la pire configuration (6,1, aucune pièce publiable) : le processus créatif en 9 étapes est trop lourd pour Sonnet.
5. **Les pipelines multi-agents ne sont pas rentables** : E (directeur Opus → exécutant Sonnet) est le plus cher (3,13 $, 66 min) pour une qualité moyenne. F (critique puis correction) fait passer Sonnet de 22 % à 56 % de pièces publiables, mais pour 1,73 $, plus cher qu'Opus seul qui fait mieux.
6. **La vidéo est le point faible commun** (5,8 à 6,5/10 contre 7 à 7,5 pour les images fixes). Défauts récurrents relevés par les juges : première seconde vide ou statique, textes coupés par les masques d'apparition, images de transition vides, affiche prise en pleine transition, texte secondaire trop petit. Piste : un contrôle automatique des images clés (0,5 s, fin, affiche) avant livraison.
7. **Juges** : Opus et Sonnet s'écartent de 0,62 point en moyenne sur la même pièce ; un juge Sonnet coûte environ 0,11 $ contre 0,24 $ pour Opus.

## Budget

| Poste | Coût API |
|---|---|
| Production des 74 pièces | 105,68 $ |
| Notation (juges) | 14,88 $ |
| Orchestration (session principale) | 21,38 $ |
| Perdu au redémarrage du conteneur | 8,63 $ |
| **Total** | **150,58 $** |

## Structure du dépôt

- `pieces/<id>/` : une pièce = `index.html` (source), `video.mp4` + `poster.jpg` + `sheet.jpg` ou `slides/*.png`, `meta.json`.
- `bench/briefs/<id>.json` : le brief client de chaque pièce. `bench/process/<id>/` : directions artistiques, critiques, design cards.
- `bench/results/` : `assignments.json` (pièce → configuration), `judgments.json` (toutes les notes et défauts), `agent_costs.json` (tokens, coût et durée de chaque agent), `summary.json`.
- `bench/workflows/` : scripts de production et de notation.
- `tools/render.mjs` : moteur de rendu déterministe. `docs/RENDER_CONTRACT.md` : contrat pour écrire une pièce.
- `skills/klipt-craft/` : skill de production écrit pour ce test. `skills/taste-express/` : copie du skill utilisée pendant le test (avec `--no-sandbox` pour le conteneur, et la mémoire des pièces produites).
- `tools/metrics.py`, `bench_costs.py`, `collect_judgments.py`, `analyze.py`, `build_gallery.py` : mesure et analyse.

Rendre une pièce : `npm install` puis `node tools/render.mjs video pieces/<id>` (ou `stills`).
