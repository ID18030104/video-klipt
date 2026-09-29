import math,re
IC='../../node_modules/lucide-static/icons/'
def icon(n,size,color):
    s=open(IC+n+'.svg').read()
    s=re.sub(r'<svg[^>]*>','<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'%(size,size,color),s,1)
    return re.sub(r'<!--.*?-->','',s,flags=re.S)
NB=' '
cx,cy,R=540,340,290
def pt(a,r):
    t=math.radians(a-90); return cx+r*math.cos(t), cy+r*math.sin(t)
def arc(a0,a1,r):
    x0,y0=pt(a0,r);x1,y1=pt(a1,r)
    return f"M{x0:.1f} {y0:.1f}A{r} {r} 0 {1 if a1-a0>180 else 0} 1 {x1:.1f} {y1:.1f}"
def ang(v): return -120+(v-1)*60
def gauge(v,label,ic,uid,ok=False):
    o=[]
    o.append(f'<svg class="gauge" viewBox="0 0 1080 700" width="1080" height="700">')
    o.append('<defs><linearGradient id="cu%s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F0B27E"/><stop offset=".45" stop-color="#C97B45"/><stop offset="1" stop-color="#7A3F1C"/></linearGradient>'%uid)
    o.append(f'<path id="lab{uid}" d="{arc(-95,95,232)}"/></defs>')
    o.append(f'<circle cx="{cx}" cy="{cy+8}" r="{R+30}" fill="#000" opacity=".28"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R+26}" fill="url(#cu{uid})"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R+6}" fill="#5E2F14"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#F1E8D6"/>')
    # colour band
    for a0,a1,c in [(-120,-30,'#6FBF8E'),(-30,60,'#E9B44C'),(60,120,'#E5482D')]:
        o.append(f'<path d="{arc(a0,a1,178)}" fill="none" stroke="{c}" stroke-width="22"/>')
    # ticks
    for i in range(0,49):
        a=-120+i*5; major=i%12==0
        x0,y0=pt(a,150 if major else 156); x1,y1=pt(a,190 if major else 178)
        o.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#0F2E2C" stroke-width="{5 if major else 2.5}"/>')
    for k in range(1,6):
        x,y=pt(ang(k),118)
        o.append(f'<text x="{x:.1f}" y="{y+16:.1f}" text-anchor="middle" class="num">{k}</text>')
    o.append(f'<text class="arclab" text-anchor="middle"><textPath href="#lab{uid}" startOffset="50%">{label}</textPath></text>')
    # icon
    o.append(f'<g transform="translate({cx-34},{cy+92})">{icon(ic,68,"#0F2E2C")}</g>'.replace('<svg','<svg',1))
    # needle
    a=ang(v); col='#0F2E2C'
    o.append(f'<g transform="rotate({a} {cx} {cy})"><polygon points="{cx-9},{cy+34} {cx+9},{cy+34} {cx+3},{cy-196} {cx-3},{cy-196}" fill="{"#1E7A4C" if ok else "#E5482D"}"/></g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="url(#cu{uid})" stroke="#5E2F14" stroke-width="4"/><circle cx="{cx}" cy="{cy}" r="8" fill="#5E2F14"/>')
    # glass glare
    o.append(f'<path d="{arc(-70,-20,R-8)}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="10" stroke-linecap="round"/>')
    # neck
    o.append(f'<rect x="{cx-44}" y="{cy+R+20}" width="88" height="{700-(cy+R+20)}" fill="url(#cuv{uid})"/>')
    o.append('</svg>')
    s=''.join(o)
    s=s.replace('</defs>',f'<linearGradient id="cuv{uid}" x1="0" x2="1"><stop offset="0" stop-color="#7A3F1C"/><stop offset=".3" stop-color="#F0B27E"/><stop offset=".6" stop-color="#C97B45"/><stop offset="1" stop-color="#6A3418"/></linearGradient></defs>',1)
    return s
words=["Il","vous","prévient","toujours","avant","de","lâcher."]
def tag(i):
    return '<div class="sent">'+' '.join(f'<span class="{"on" if j==i else ("past" if j<i else "")}">{w}</span>' for j,w in enumerate(words))+'</div>'
slides=[
 dict(v=5,label="5 SIGNES À LIRE",ic="thermometer",kind="cover",
  h=f"5 signes que votre chauffe&#8209;eau va <em>lâcher</em>",
  b="Et quoi faire avant la panne. Glissez pour lire l’aiguille."),
 dict(v=1,label="SIGNE 1 SUR 5",ic="thermometer",n="01",h="Eau tiède ou rouillée",
  b="L’eau chaude tiédit vite, ou sort teintée de rouille : la cuve ou la résistance fatiguent.",a="Faites contrôler la cuve et la résistance."),
 dict(v=2,label="SIGNE 2 SUR 5",ic="volume-2",n="02",h="Des bruits dans la cuve",
  b="Claquements, grondements, sifflements : c’est souvent le tartre qui s’accumule au fond.",a="Faites-le vérifier avant que ça empire."),
 dict(v=3,label="SIGNE 3 SUR 5",ic="droplet",n="03",h="Le groupe de sécurité goutte",
  b="Une fuite au groupe de sécurité qui ne s’arrête pas.",a="Ne le bouchez jamais. Appelez un plombier.",drip=True),
 dict(v=4,label="SIGNE 4 SUR 5",ic="calendar-clock",n="04",h="Plus de 10 ans d’âge",
  b="Passé dix ans, un chauffe-eau est en fin de course, même s’il marche encore.",a="Faites-le contrôler et préparez son remplacement."),
 dict(v=5,label="SIGNE 5 SUR 5",ic="trending-up",n="05",h="La facture qui grimpe",
  b="Vous consommez pareil, mais la facture monte : l’appareil chauffe moins bien.",a="Demandez un diagnostic."),
 dict(v=1,label="DIAGNOSTIC 49" +NB+ "€",ic="wrench",kind="offer",ok=True,
  h="Diagnostic chauffe&#8209;eau<br><span class='price'>49"+NB+"€</span>",
  b="Offert si vous remplacez votre chauffe-eau avec nous. Dépannage 7j/7.",
  c="02 40 12 34 56", w="garnier-plomberie.fr", f="Nantes depuis 1987 · 3 générations · 9 techniciens · dépannage 7j/7"),
]
def pipe(drip):
    d=''
    if drip: d='<svg class="drip" width="60" height="90" viewBox="0 0 60 90"><path d="M30 6C30 6 8 38 8 58a22 22 0 0 0 44 0C52 38 30 6 30 6Z" fill="#7FC4E8"/><path d="M20 58a10 10 0 0 0 8 10" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/></svg>'
    return f'''<div class="pipe"></div><div class="fl fl-l"></div><div class="fl fl-r"></div><div class="tee"></div>{d}'''
out=[]
for i,s in enumerate(slides):
    kind=s.get('kind','')
    g=gauge(s['v'],s['label'],s['ic'],str(i),s.get('ok',False))
    body=''
    if kind=='cover':
        body=f'<h1 class="cover">{s["h"]}</h1><p class="sub">{s["b"]}</p>'
    elif kind=='offer':
        body=f'<h2 class="offer">{s["h"]}</h2><p class="b">{s["b"]}</p><div class="contact"><span class="tel">{s["c"]}</span><span class="web">{s["w"]}</span></div>'
    else:
        body=f'<h2><span class="n">{s["n"]}</span>{s["h"]}</h2><p class="b">{s["b"]}</p><p class="a"><b>Que faire</b> {s["a"]}</p>'
    out.append(f'''<section class="slide {kind}"><div class="grain"></div><div class="brand"><span>GARNIER &amp; FILS</span><span>{"NANTES DEPUIS 1987 · 3 GÉNÉRATIONS" if kind=="offer" else "PLOMBERIE CHAUFFAGE · NANTES"}</span></div>{g}{pipe(s.get("drip"))}<div class="txt">{body}</div>{tag(i)}<div class="cnt">{i+1}/7</div></section>''')
html=open('tpl.html').read().replace('%%SLIDES%%','\n'.join(out))
open('index.html','w').write(html)
