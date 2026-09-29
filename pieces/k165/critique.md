# Critique k165 — Ledgerly « Relances intelligentes » (vidéo 1080×1350, 23 s)

**Verdict : 7/10.** Direction crème/encre/menthe crédible et propre à une fintech, bon arc narratif (facture impayée → IA qui choisit ton/créneau/canal → preuve → CTA), UI plausible. Mais pour un SaaS de **compta**, la facture du hook est fausse arithmétiquement, et plusieurs problèmes de timing/lisibilité empêchent la publication telle quelle.

## Corrections prioritaires

1. **Facture fausse (bloquant pour une fintech).** 9 200 + 1 800 = 11 000 € HT ; TVA 20 % = 2 200 €, donc TTC = 13 200 €, pas 1 400 € / 12 400 €. Un DAF le verra en 1 s. Fix : ligne TVA → `2 200 €`, total → `13 200 €`, et reporter `13 200 €` dans la carte Atelier Morel (#c1 `.am`) et dans `msg` du composeur e-mail. (Alternative pour garder 12 400 € TTC : lignes `8 500 €` + `1 833,33 €`… moins propre ; préférer 13 200 €.)

2. **Ligne « Relancer ? Quand ? Sur quel ton ? » visible dès 0 s et rognée.** À t = 0.5 s elle est déjà affichée, descendantes coupées (« Ouand », « quel ») et collée au bas de la facture qui monte (facture bas ≈ 1 200 px + rotation + scale 1.04 → ≈ 1 250 px ; texte à top 1 240). Fix : ajouter `gsap.set('#aq .ln>span',{yPercent:112})` avant la timeline (ou `immediateRender:true` explicite), remonter la facture `.inv{top:600px;height:540px}` et descendre `#aq` à `top:1256px`, en gardant ≥ 40 px d'air sous la facture même à scale 1.04.

3. **Le tampon IMPAYÉE masque les montants.** Il recouvre 9 200 € et 1 800 € (lecture impossible de « 1 800 € » à 3.5 s). Fix : le poser sur la zone vide à gauche du total : `.stamp{top:auto;bottom:40px;left:30px;right:auto;font-size:64px}`, ou en haut à droite sur l'en-tête (`top:-30px;right:-30px`). Les chiffres doivent rester lisibles.

4. **End card trop courte.** Tous les éléments ne sont en place qu'à 21.5 s (+0.6 s d'anim) → ~0.9 s de tenue complète, loin des 2.5 s exigés. Fix : allonger la durée à **24.5 s** (`duration:24.5` dans `KLIPT` + `tl.to({},{duration:.01},24.5)`), et resserrer les entrées : e1 19.6, e2 19.75, titres 19.9, e3 20.3, e4 20.5, e5 20.7 → tout lisible à 21.3 s, tenue ≈ 3.2 s. Supprimer le yoyo de #e3 ou le limiter à `scale:1.02`.

5. **Chiffres géants en JetBrains Mono : espaces béants.** « -38 % », « 11 j », « 12 400 € » affichent des trous d'une largeur de caractère (mono) — la preuve paraît cassée. Fix : pour `.num` et `.inv .tot b`, passer en `font-family:'Sora';font-weight:800;font-variant-numeric:tabular-nums` et utiliser U+202F entre nombre et unité (`'−'+v+' %'`, `v+' j'`, `13 200 €`). Remplacer le trait d'union par le vrai signe moins `−` (U+2212).

6. **Temps de lecture insuffisants en C et D.**
   - E-mail (22 mots) fini de taper à 13.7 s, wipe vers D à 14.95 s → 1.25 s pour lire (il en faut ~9 s ; au minimum que l'œil saisisse le ton). Fix : taper plus vite (`duration:1.4`, départ 11.3), démarrer le curseur de ton à 11.6 pour qu'il arrive sur Cordial *pendant* la frappe, et décaler le wipe D à **15.6 s** (grâce aux +1.5 s du point 4, décaler D et E de +0.6 s).
   - Note « DSO : délai moyen de paiement de vos clients. » apparaît à 18.4 s pour 0.75 s. Fix : la faire apparaître avec #d2 (17.3 s) pour ≥ 2.4 s de tenue.

7. **Pastilles IA qui débordent des cartes (scène B).** Les pills menthe dépassent le bord bas de chaque carte de ~8 px (visible à 9.5 s, la bordure passe à travers). Fix : `.cl{height:232px}` et tops `#c1 500 / #c2 752 / #c3 1004`, `#bnote top:1262px` ; ou réduire `.ai{padding:10px 18px;margin-top:14px}`.

8. **Finitions typo / détails.**
   - Espaces fines insécables (U+202F) avant `?` `!` dans « Relancer ? Quand ? Sur quel ton ? » et dans `msg` (« convient ? », « Merci ! ») ; `12 400 €` dans `msg` pour éviter une coupure « 12 / 400 € ».
   - Ligne de bas d'end card : le « · » final orphelin en fin de ligne 1. Fix : `width:940px` + remplacer par deux lignes explicites « Connecté à votre compta · relances e-mail et SMS » / « Tableau de bord de trésorerie », ou supprimer le dernier « · » au profit d'un `<br>`.
   - Curseur de ton : à 22 % le dégradé menthe→corail est compressé et la zone « Cordial » paraît corail. Fix : `.fill{background:var(--mint)}` (ou `background-size:936px 100%` pour figer le dégradé sur toute la piste).
   - Chip « Mar 9 h 12 » : le `scale:1.08` le fait déborder sur Lun/Mer (gap 14 px) — limiter à `1.04` ou ajouter un `box-shadow` plutôt qu'un scale.
