#!/usr/bin/env python3
"""Assemble docs/KLIPT_PRODUCTION.md: the production guide (docs/production/guide.md + video section)
followed by the full text of the prompts, the catalogue, the render contract and the production tools.
Re-run after changing any of them:  python3 tools/build_production_doc.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()

def demote(md, by=2):
    out, fence = [], False
    for line in md.splitlines():
        if line.lstrip().startswith('```'): fence = not fence
        if not fence and re.match(r'^#{1,4} ', line): line = '#' * by + line
        out.append(line)
    return '\n'.join(out)

PROMPTS = [
    ('A', 'Prompt Studio optimisé (agent Sonnet 5.5, 100 % code)', 'docs/STUDIO_PROMPT_OPT.md',
     "Le prompt complet de l'agent en mode Studio. Il est envoyé tel quel, suivi de `ROLE`, `PIECE_ID` et du chemin du brief. Le catalogue (annexe D) est ajouté à la suite du prompt."),
    ('B', 'Prompt Hybride (image ou clip Higgsfield + couche Claude)', 'docs/HYBRID_PROMPT.md',
     "Le prompt du mode hybride : une seule génération Higgsfield, puis la couche de code (texte, logo, interface, animation)."),
    ('C', 'Contrat de rendu (règles techniques)', 'docs/RENDER_CONTRACT.md',
     "Ce que toute page doit respecter pour être rendue par `tools/render.mjs`. L'agent le lit en premier."),
    ('D', 'Catalogue de décisions créatives', 'docs/STUDIO_CATALOGUE.md',
     "Niveaux d'ambition, structures narratives, mécaniques d'attention, styles, traitements d'image, typographie, couleur, caméra, transitions, formats."),
]
CODE = [
    ('tools/render.mjs', 'js', 'Moteur de rendu : vidéo, images fixes, image unique, contrôle qualité. Chromium via playwright-core + ffmpeg.'),
    ('lib/klipt-kit.js', 'js', 'Aides déterministes pour les pages : hasard initialisé, courbes, progression, séquences d\'images.'),
    ('tools/hf_ledger.py', 'python', 'Registre de budget Higgsfield partagé, sous verrou (réserver avant, rembourser en cas d\'échec).'),
    ('tools/higgsfield_image.py', 'python', 'Image Higgsfield Marketing Studio (estimation, garde-fou, génération, téléchargement, métadonnées).'),
    ('tools/higgsfield_video.py', 'python', 'Clip vidéo Higgsfield, tous modèles (texte ou image → vidéo), avec estimation gratuite.'),
    ('tools/higgsfield_upload.py', 'python', 'Téléverse un fichier local (logo, image) et renvoie son URL publique.'),
    ('tools/openimages.py', 'python', 'Photos libres Open Images (CC BY 2.0) : labels, recherche avec planche contact, téléchargement et crédits.'),
    ('tools/pexels.py', 'python', 'Photos et vidéos Pexels : recherche, originaux 4K, découpe d\'un clip en séquence d\'images.'),
    ('tools/gfont.py', 'python', 'Télécharge une Google Font en local (le rendu est hors ligne).'),
    ('brand/klipt/brand.json', 'json', 'Modèle de kit de marque.'),
    ('package.json', 'json', 'Dépendances Node du moteur de rendu.'),
]

guide = rd('docs/production/guide.md').replace('@@VIDEO_SECTION@@', rd('docs/production/video.md').strip())
parts = [guide, '\n---\n\n# Annexes\n']
for letter, title, path, note in PROMPTS:
    parts.append(f'\n## Annexe {letter} — {title}\n\nSource : `{path}`. {note}\n\n' + demote(rd(path).strip()) + '\n')
parts.append('\n## Annexe E — Code des outils de production\n\nTexte intégral des fichiers. Les clés d\'API ne sont jamais dans le code : variables d\'environnement ou `/root/klipt-state/`.\n')
for path, lang, note in CODE:
    parts.append(f'\n### `{path}`\n\n{note}\n\n````{lang}\n{rd(path).rstrip()}\n````\n')
out = os.path.join(ROOT, 'docs/KLIPT_PRODUCTION.md')
open(out, 'w', encoding='utf-8').write('\n'.join(parts))
print(out, round(os.path.getsize(out) / 1024), 'KB')
