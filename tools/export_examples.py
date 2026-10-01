#!/usr/bin/env python3
"""Export the validated pieces (jingles, videos, posts) into a folder with index.html, infos.txt and photo credits, ready to upload as Klipt examples. Edit SEL and OUT below."""
import json, os, glob, re, shutil, subprocess, unicodedata, html
ROOT='/home/user/video-klipt'; OUT='/tmp/claude-0/-home-user-video-klipt/b3448e48-88a3-5a07-a3bb-7a2c31472416/scratchpad/klipt-exemples'
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
scores={}
for it in json.load(open(f'{ROOT}/bench/results/judgments.json'))['scores']: scores.setdefault(it['id'],[]).append(it['overall'])
GROUPS=[
 ('1-generiques-klipt', 'Génériques Klipt (vrai logo, 100 % Kling, avec son)', ['j01']),
 ('2-videos', 'Vidéos', []), ('3-posts-carrousels-stories', 'Posts, carrousels et stories', []),
]
SEL=['s01','s02','v02','v01','h02','p220','p230','p267','p294','k165','p290',
     's03','h03','s04','h04','s05','h05','k112','p224','p236','p250','p207','p210','p213','p218','p221','p261','p262','p273','p275','p283','p288']
def slug(t):
    t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',t).strip('-')[:40]
def ff(*a): subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*a],check=True)
items=[]
# jingles
jd=f'{OUT}/1-generiques-klipt'; os.makedirs(jd)
for k,lab in [('intro-a','Générique de début A — rubans de soie'),('intro-b','Générique de début B — symbole en verre 3D'),('outro-a','Générique de fin A — cartes qui s’assemblent'),('outro-b','Générique de fin B — pulsation play')]:
    shutil.copy(f'{ROOT}/pieces/j01/{k}.mp4',f'{jd}/klipt-{k}.mp4')
    ff('-sseof','-0.1','-i',f'{ROOT}/pieces/j01/{k}.mp4','-frames:v','1','-vf','scale=360:-2',f'{jd}/klipt-{k}-apercu.jpg')
    items.append(dict(group='1-generiques-klipt',title=lab,brand='Klipt',kind='générique 5 s',fmt='1080x1920',lang='—',files=[f'1-generiques-klipt/klipt-{k}.mp4'],thumb=f'1-generiques-klipt/klipt-{k}-apercu.jpg',note='Kling O3 (première / dernière image), son natif. Coût 0,70 $.'))
for pid in SEL:
    d=f'{ROOT}/pieces/{pid}'; m=json.load(open(f'{d}/meta.json'))
    vid=os.path.exists(f'{d}/video.mp4'); g='2-videos' if vid else '3-posts-carrousels-stories'
    lang=m.get('copy_language') or m.get('lang') or ''
    name=f"{slug(m.get('brand',pid))}-{slug(m.get('kind','') )}-{lang}-{pid}"
    pd=f'{OUT}/{g}/{name}'; os.makedirs(pd)
    files=[]
    if vid:
        has_a='Audio:' in subprocess.run(['ffmpeg','-hide_banner','-i',f'{d}/video.mp4'],capture_output=True,text=True).stderr
        ff('-i',f'{d}/video.mp4','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p',*(['-c:a','aac','-b:a','192k'] if has_a else ['-an']),'-movflags','+faststart',f'{pd}/video.mp4')
        shutil.copy(f'{d}/poster.jpg',f'{pd}/miniature.jpg'); files=[f'{g}/{name}/video.mp4']; thumb=f'{g}/{name}/miniature.jpg'
    else:
        sl=sorted(glob.glob(f'{d}/slides/*.png'))
        for i,s in enumerate(sl,1): shutil.copy(s,f'{pd}/slide-{i:02d}.png'); files.append(f'{g}/{name}/slide-{i:02d}.png')
        ff('-i',sl[0],'-vf','scale=360:-2','-q:v','4',f'{pd}/apercu.jpg'); thumb=f'{g}/{name}/apercu.jpg'
    cr=m.get('credits') or []
    if not cr and os.path.exists(f'{d}/assets/CREDITS.json'): cr=json.load(open(f'{d}/assets/CREDITS.json'))
    lines=[f"Marque (fictive) : {m.get('brand')}", f"Secteur : {m.get('sector','')}", f"Type : {m.get('kind')} · format {m.get('format')} · langue {lang}" + (f" · {m.get('duration')} s" if vid else f" · {len(files)} image(s)"),
           f"Titre : {m.get('title','')}", f"Concept : {m.get('concept','')}"]
    if pid in scores: lines.append(f"Note des juges à l'aveugle : {sum(scores[pid])/len(scores[pid]):.1f}/10, publiable tel quel")
    if m.get('plate') or m.get('clip'): lines.append('Image ou vidéo de fond générée par IA (Higgsfield) : activer l’étiquette « contenu IA » de la plateforme.')
    if cr:
        lines.append('\nCRÉDITS PHOTO À AFFICHER (licence CC BY 2.0, obligatoire) :')
        for c in cr:
            if isinstance(c,dict) and c.get('author'): lines.append(f"- Photo : {c.get('author')} — {c.get('title','')} — {c.get('page','')} — CC BY 2.0")
            elif isinstance(c,str): lines.append(f'- {c}')
    open(f'{pd}/infos.txt','w').write('\n'.join(lines)+'\n')
    items.append(dict(group=g,title=m.get('title',''),brand=m.get('brand'),kind=m.get('kind'),fmt=m.get('format'),lang=lang,files=files,thumb=thumb,
                      note=(f"Note juges {sum(scores[pid])/len(scores[pid]):.1f}/10" if pid in scores else '')+(' · crédits photo dans infos.txt' if cr else ''),folder=f'{g}/{name}'))
# index.html
names={'1-generiques-klipt':'Génériques Klipt','2-videos':'Vidéos','3-posts-carrousels-stories':'Posts, carrousels et stories'}
cards={k:[] for k in names}
for it in items:
    media=f'<video src="{it["files"][0]}" poster="{it["thumb"]}" controls preload="none"></video>' if it['files'][0].endswith('.mp4') else f'<a href="{it["files"][0]}"><img src="{it["thumb"]}" loading="lazy"></a>'
    more='' if len(it['files'])<2 else ' · '+' '.join(f'<a href="{f}">{i+1}</a>' for i,f in enumerate(it['files']))
    cards[it['group']].append(f'<article>{media}<h3>{html.escape(it["brand"] or "")}</h3><p>{html.escape(it["title"] or "")}</p><p class=m>{html.escape(str(it["kind"]))} · {it["fmt"]} · {it["lang"]}{more}</p><p class=m>{html.escape(it["note"])}</p></article>')
page=['<!doctype html><html lang=fr><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Exemples Klipt</title><style>body{margin:0;font:15px/1.45 system-ui,sans-serif;background:#FAF7F3;color:#211C2E;padding:32px}h1{font-size:28px}h2{margin-top:40px}section{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:20px}article{background:#fff;border:1px solid #ece7f1;border-radius:14px;padding:10px}video,img{width:100%;border-radius:8px;background:#000;display:block}h3{margin:8px 0 2px;font-size:15px}p{margin:2px 0}.m{color:#5C566E;font-size:13px}</style>',
      '<h1>Exemples Klipt</h1><p>Contenus validés, prêts à publier comme exemples. Les marques clientes sont fictives. Crédits photo et mentions dans le fichier <b>infos.txt</b> de chaque dossier.</p>']
for k,v in names.items(): page.append(f'<h2>{v} ({len(cards[k])})</h2><section>{"".join(cards[k])}</section>')
open(f'{OUT}/index.html','w').write(''.join(page))
open(f'{OUT}/LISEZ-MOI.txt','w').write("""EXEMPLES KLIPT — contenus validés
Ouvrir index.html dans un navigateur pour tout voir.

1-generiques-klipt : génériques de début et de fin (vrai logo Klipt, 100 % Kling, avec son, 1080x1920, 5 s).
2-videos : vidéos (MP4 H.264), avec une miniature.
3-posts-carrousels-stories : images PNG prêtes à publier (slide-01, slide-02… dans l'ordre du carrousel).

Sélection : pièces notées publiables telles quelles par les juges à l'aveugle (note ≥ 7/10), séries Studio et Hybride,
vidéos Maison Brune et génériques Klipt. Exclues : le film v03 (raté), les tests Higgsfield avec l'ancien logo inventé.

À savoir avant de publier :
- Les marques sont fictives (créées pour les tests). Vérifier qu'aucune ne correspond à une entreprise réelle homonyme
  (ex. Relai, Greenloop, Orbitr) ou préciser « marque fictive / exemple ».
- Photos Open Images (licence CC BY 2.0) : le crédit de l'auteur est obligatoire, voir infos.txt du dossier concerné.
- Fonds générés par IA (Higgsfield / Kling) : activer l'étiquette « contenu IA » de la plateforme.
- La plupart des vidéos sont muettes (ajouter la musique dans l'app) ; les génériques ont leur son.
""")
print(len(items))
