# Critique — k109 · Garnier & Fils — « 5 signes que votre chauffe-eau va lâcher »

**Verdict : 7/10.** Le registre est juste : artisan solide, bleu de travail, ocre, brique, Archivo Black. Le format « Ce que ça veut dire / Que faire » est vraiment utile et le conseil est concret. On sent la marque. Plusieurs défauts d'exécution empêchent encore de le publier sans retouche : un logo qui disparaît, des traits parasites dans les titres, une césure ratée sur la slide d'accroche, un tuyau qui coupe la lecture, et la continuité promise dans la direction, qui s'arrête à la slide 5.

## Corrections prioritaires

1. **Slide 06 : le logo est invisible.** Le symbole `#mark` (fond `#E8A33D`) est posé sur le fond ocre `#E8A33D` de la slide. On ne voit plus qu'un « U » flottant, sans cartouche. Il faut créer une variante `#mark-inv` (rect `fill="#14283F"`, trait `#E8A33D`) et l'utiliser dans le `.head` de `#s6`.

2. **Traits parasites dans tous les titres Archivo Black.** Des filets horizontaux de 1 px traversent les glyphes : « votre », « chauffe- » (s1), « tiède ou rousse » (s2), « de sécurité » (s4), « Diagnostic chauffe-eau » (s6). Ce sont des coutures de contours qui se chevauchent au rendu. Deux options : ajouter `.h1{-webkit-text-stroke:1px currentColor; paint-order:stroke fill}`, ou rendre avec `deviceScaleFactor:2` puis réduire à 1080×1350. Ensuite, vérifier au zoom 200 %.

3. **Slide 01 : la césure « chauffe- / eau » tue l'accroche.** Le mot-clé du carrousel est coupé en deux et le titre s'étale sur 5 lignes. Il faut passer le `h1` à `width:720px; font-size:104px` et entourer le mot de `<span style="white-space:nowrap">chauffe‑eau</span>` (avec un trait d'union insécable U+2011). Objectif : 4 lignes, soit « 5 signes que / votre chauffe‑eau / va lâcher ». Ajouter aussi un badge de preuve, prévu dans la direction mais absent : pastille brique « DEPUIS 1987 · NANTES » à `right:70px; top:190px`, en 30 px.

4. **Le tuyau de cuivre sépare le diagnostic de l'action (s2 à s5).** Il est à `top:1040px`, pile entre la carte « Ce que ça veut dire » et la carte « Que faire ». Il se lit comme une rupture, et il colle aux cartes : sur s4 (et s3), la carte `.why` finit vers y≈1030, soit **10 px** au-dessus du tuyau. Deux corrections :
   - descendre le tuyau à `top:1270px` (sous les cartes, au-dessus de la barre de progression) ;
   - remonter `.do` à `top:1060px`, pour que les deux cartes forment un bloc avec 30 px d'écart.

   À défaut, raccourcir le texte de s4 : « Goutte-à-goutte constant = **soupape entartrée** ou pression trop haute. » (sans « Risque réel. », qui crée la 3e ligne et la veuve « réel. »).

5. **La continuité s'arrête à la slide 5.** Le tuyau est absent de s6 et s7. Il faut le prolonger :
   - s6 : un tuyau à la même hauteur, qui passe *derrière* la carte navy (z-index inférieur) ;
   - s7 : un tuyau qui se termine par un coude ou un robinet cuivre à x≈900, pour clore le fil.

   Sur s1, le tuyau porte des raccords (`.pipe.j`) aux deux bords : retirer le raccord droit, sinon le tuyau semble fermé et ne se prolonge pas vers s2.

6. **Slide 05 : du vide et des veuves.** Les deux cartes (hauteur 540 px) ont environ 130 px de vide en bas, et la carte 04 finit sur la veuve « ans. ». Il faut descendre les cartes à `height:470px`, écrire « Durée de vie moyenne d’un ballon&nbsp;: 10&nbsp;à&nbsp;15&nbsp;ans. » (espaces insécables, dont celle avant « : » qui manque dans le HTML) et remonter `.why` à `top:680px`. Le libellé « Que faire » de cette slide utilise le style `.why` (label brique sur navy transparent), alors qu'ailleurs « Que faire » est la carte pleine. Renommer ce libellé « Comment vérifier » pour garder la grammaire des slides 2 à 4.

7. **Textes sous le minimum de 30 px.** Les libellés `.lab` font 26 px, le sous-titre du logo 22 px, « Glissez » 28 px et « RÉSERVEZ VOTRE DIAGNOSTIC À 49 € » (s7) 28 px. Il faut passer `.lab` à `30px` (letter-spacing `.12em`), la ligne CTA de s7 à `32px`, « Glissez » à `30px` et `.logo small` à `24px`. Il s'agit de la cible 35–70 ans sur mobile : c'est prioritaire.

8. **Slide 06 : rendre l'offre plus claire.** Le bloc navy laisse environ 260 px de vide à droite du « 49 € ».
   - Placer un tampon rond brique (diamètre 200 px, rotation −8°) à `right:60px; top:600px`, avec le texte « OFFERT si remplacement ». La ligne « Offert si remplacement » sous le prix devient alors « TTC · 45 min sur place ».
   - Ajouter le téléphone en pied de slide : `02 40 12 34 56` en Archivo Black 44 px à `top:1210px`. C'est souvent sur la slide d'offre que le lecteur décide.
   - Typographie : écrire « 7&nbsp;j/7 » (et non « 7j/7 ») sur s6 et s7.

## Points déjà solides (à garder)
- Le système « numéro géant ocre + picto + titre + 2 cartes » est clair et cohérent, et l'alternance crème/navy donne du rythme.
- La copie est concrète, en français parlé, sans jargon creux. « …et quoi faire avant la douche froide. » est une très bonne accroche secondaire.
- La barre de progression en bas fonctionne. La slide 7 contient toutes les preuves du brief (1987, 3 générations, 9 techniciens, 7 j/7).
