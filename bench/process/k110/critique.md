# Critique — k110 · Maison Castel — Rasage à l'ancienne (1080×1920, 22 s)

**Verdict : 7/10.** La direction est juste et propre à la marque : noir/crème/laiton/bordeaux, Gloock, poteau de barbier animé, trois étapes numérotées comme un ticket de salon, prix en très grand. Le français est propre (espaces insécables avant « ? » et dans « 35 € », apostrophes typographiques). Cinq problèmes empêchent une publication sans retouche : le tampon « 2025 » est périmé, l'accroche disparaît avant d'avoir été lue, le brun du blaireau chevauche le « 02 », le laiton sur bordeaux manque de contraste, et la moitié basse de chaque scène est vide.

## Corrections par priorité

1. **Le tampon « NOUVEAU 2025 » est faux (nous sommes en 2026) et vieillira mal.** Dans `#stamp`, remplacez `2025` par `2026`, ou mieux, retirez l'année : `<div class="caps">Nouveau</div><div class="serif" style="font-size:52px">soin</div>`, ou « Nouveau · 35 € ». Un exemple de la bibliothèque ne doit pas porter de date.

2. **L'accroche n'est pas assez longtemps à l'écran.** La question fait 12 mots, soit au moins 5,6 s de lecture selon la règle (0,4 s par mot + 0,8 s). Sa dernière ligne n'est entièrement arrivée qu'à ~1,5 s et la scène coupe à 3,4 s, ce qui ne laisse que ~1,9 s pour lire. Deux corrections :
   - Raccourcir le texte à 7 mots : « Votre dernier *vrai* rasage, c'était quand ? », sur 3 lignes.
   - Passer la S1 à 0–4,2 s, puis décaler les scènes suivantes : S2 4,2–7,6, S3 7,6–10,4, S4 10,4–13,2, S5 13,2–16, S6 16–18,6. On garde DUR = 22.
   - Accélérer le stagger du masque de 0.16 à 0.1 pour que tout soit en place avant 1,1 s.

3. **Le blaireau chevauche le « 02 » (S4, t ≈ 11,5 s).** Les bulles de mousse du `#brushG` débordent en y < 0 du viewBox. Elles recouvrent le chiffre détouré en haut à gauche (x 100–310, y 270–420). Corrections :
   - Descendre `.ill` du blaireau : `#brush{top:560px;left:180px}`.
   - Ou bien réduire l'illustration : `transform: scale(.85)` sur `#brushG`, avec `transformOrigin:'200px 150px'`.
   - Vérifier ensuite qu'il reste au moins 40 px entre la mousse et le haut du « 02 ».
   - Même contrôle pour la vapeur de la serviette (S3), qui monte jusqu'à y ≈ 470 et reste pour l'instant juste sous le « 01 ».

4. **Contraste insuffisant du laiton sur bordeaux (S2).** « LE SOIN SIGNATURE » en #b98b3e sur #8c2a22 donne un contraste d'environ 2:1, donc illisible sur téléphone. Passez `#s2k` en `color:var(--cream)` (contraste d'environ 8:1). Ou gardez le laiton mais posez-le sur une pastille `background:var(--ink);padding:10px 18px`. Dans la même scène, `#s2 .serif` dérive jusqu'à x = −24 : « Le rasage » finit alors à 76 px du bord et se décale de la colonne de 100 px. Limitez la dérive à `x:-8`, ou appliquez-la à tout le bloc (kicker + titre + filet + sous-titre).

5. **Les 600 à 800 px du bas sont vides sur 5 scènes sur 7.** Sur S2 (y > 1350), S3/S4/S5 (y > 1470), S6 (y > 1300) et S7 (y > 1320), le bas de l'écran est un aplat vide. La zone sûre descend jusqu'à y = 1540 : il faut l'occuper. Propositions :
   - S2 : ajouter `« 40 min · 35 € »` en 44 px à top 1400.
   - S3/S4/S5 : poser le titre à `top:1260` et le sous-titre à `top:1420` en 48 px, puis ajouter une ligne en 30 px caps laiton à top 1500 : « 10 min », « 10 min », « 20 min » (la durée de chaque geste).
   - S6 : faire entrer le sous-titre « Un vrai moment pour vous. », qui n'apparaît pas sur la planche. Vérifiez que `#p3` hérite bien d'Oswald et d'une couleur lisible, et placez-le à top 1240 avec `color:var(--ink)`.
   - S7 : descendre l'adresse à top 1260 et ajouter en dessous un rappel « RDV en ligne en 30 s » en 30 px laiton, pour que le carton de fin occupe 270 → 1450.

6. **La sortie de S6 cache le prix trop tôt.** Le « 35 € » apparaît à 16,25 s et « 40 minutes » à 16,9 s, puis le balayage démarre à 18,3 s : il ne reste que ~1,4 s de lecture pleine pour l'information clé du brief. Passez S6 à 16 → 19,2 s et S7 à 19,2 → 22 s. Le carton de fin tient alors 2,8 s, ce qui respecte encore le minimum de 2,5 s, et le prix gagne 0,6 s.

7. **Trois familles de caractères, alors que le guide en autorise deux.** Gloock, Instrument Serif italique et Oswald sont utilisés ensemble. L'italique d'Instrument Serif (« vraiment rasé », « à l'ancienne », « 40 ») est le meilleur accent de la pièce : gardez-le. Mais Gloock et Instrument Serif sont deux serifs proches, donc la hiérarchie flotte. Deux options :
   - Remplacer les titres Gloock par Instrument Serif en romain.
   - Ou assumer Gloock et faire les accents en Gloock avec `font-style:italic`, puis retirer `instrument-serif/400-italic.css`.

8. **Le carton de fin est trop sage pour un Reel.** La CTA ne bouge presque pas (`scale 1.015`). Pour une marque de quartier, un rappel concret convertit mieux. Ajoutez sous la carte un « bouton » visuel `Prendre RDV →` en crème sur bordeaux, 40 px, à top 1110, animé en `x:[0,8,0]` en boucle de 1,2 s à partir de 20,2 s. Autre point : le monogramme « MC » coupe presque le cercle intérieur (r 70). Réduisez `font-size` de 62 à 54, ou montez `y` de 106 à 104, pour garder de l'air.

## Ce qui fonctionne (à garder)
- Le poteau de barbier qui tourne en continu sur le bord gauche : identitaire et vivant, il donne un fil rouge à toute la vidéo.
- La typographie du prix (« 35 € » en 400 px sur fond laiton) : une vraie preuve lisible au premier coup d'œil.
- L'illustration du coupe-chou avec le reflet sur la lame, et les balayages bordeaux avec leur filet laiton entre les scènes.
- Le français est correct : espaces insécables, ’, « Mar.–sam. », aucune coquille repérée.
