(function(){
gsap.registerPlugin(DrawSVGPlugin);
const NS='http://www.w3.org/2000/svg';
const $=id=>document.getElementById(id);
function el(tag,attrs,parent){const e=document.createElementNS(NS,tag);for(const k in attrs){if(k==='text')e.textContent=attrs[k];else e.setAttribute(k,attrs[k]);}if(parent)parent.appendChild(e);return e;}
const RED='#C24A2C';
const blue=$('blue'),paper=$('paper'),bandsvg=$('bandsvg');
const R=KK.rng(226);

/* ---------- shared defs ---------- */
function defs(svg,mode){
  const d=el('defs',{},svg);
  const gc=mode==='blue'?'#EDE6D6':'#221C17';
  const a1=mode==='blue'?.05:.04,a2=mode==='blue'?.09:.07;
  const p1=el('pattern',{id:'gm_'+mode,width:24,height:24,patternUnits:'userSpaceOnUse'},d);
  el('path',{d:'M24 0V24M0 24H24',stroke:gc,'stroke-opacity':a1,'stroke-width':1,fill:'none'},p1);
  const p2=el('pattern',{id:'gM_'+mode,width:120,height:120,patternUnits:'userSpaceOnUse'},d);
  el('path',{d:'M120 0V120M0 120H120',stroke:gc,'stroke-opacity':a2,'stroke-width':1,fill:'none'},p2);
  const h=el('pattern',{id:'hatch_'+mode,width:10,height:10,patternUnits:'userSpaceOnUse',patternTransform:'rotate(45)'},d);
  el('path',{d:'M0 0V10',stroke:gc,'stroke-width':1,'stroke-opacity':.8},h);
  const vg=el('radialGradient',{id:'vg_'+mode,cx:'50%',cy:'50%',r:'75%'},d);
  const vc=mode==='blue'?'#12263D':'#E4D8C2';
  el('stop',{offset:.55,'stop-color':vc,'stop-opacity':0},vg);
  el('stop',{offset:1,'stop-color':vc,'stop-opacity':mode==='blue'?.38:.30},vg);
  return d;
}
function base(svg,mode){
  el('rect',{width:1920,height:1080,fill:mode==='blue'?'#1B3553':'#F1EADC'},svg);
  el('rect',{width:1920,height:1080,fill:'url(#gm_'+mode+')'},svg);
  el('rect',{width:1920,height:1080,fill:'url(#gM_'+mode+')'},svg);
  el('rect',{width:1920,height:1080,fill:'url(#vg_'+mode+')'},svg);
}
function frame(svg){
  const g=el('g',{},svg);
  el('rect',{x:40,y:40,width:1840,height:1000,class:'frm'},g);
  const zw=1840/6;
  for(let i=0;i<6;i++)el('text',{x:40+zw*(i+.5),y:34+0,'text-anchor':'middle','font-size':18,opacity:.6,text:String(i+1),style:'font-size:18px'},g);
  const zh=1000/3;
  ['A','B','C'].forEach((c,i)=>el('text',{x:20,y:40+zh*(i+.5)+6,'text-anchor':'middle',opacity:.6,text:c,style:'font-size:18px'},g));
  for(let i=1;i<6;i++)el('line',{x1:40+zw*i,y1:40,x2:40+zw*i,y2:52,class:'fine'},g);
  for(let i=1;i<3;i++)el('line',{x1:40,y1:40+zh*i,x2:52,y2:40+zh*i,class:'fine'},g);
  return g;
}
function mark(parent,x,y,s,fill,stroke,cls){
  const g=el('g',{transform:`translate(${x},${y}) scale(${s/64})`,class:cls||''},parent);
  const sq=el('rect',{x:.75,y:.75,width:62.5,height:62.5,fill:'none',stroke:stroke,'stroke-width':1.5*64/s>3?1.5*64/s:1.5},g);
  const tail=el('path',{d:'M14 12H50L44 42H20Z',fill:fill,stroke:stroke,'stroke-width':1.2},g);
  const jl=el('line',{x1:.75,y1:44,x2:63.25,y2:44,stroke:stroke,'stroke-width':1},g);
  return {g,sq,tail,jl};
}

/* ---------- dimension helper ---------- */
function dim(parent,x1,y1,x2,y2,label,o){
  o=o||{};const col=o.col||'var(--line)';
  const g=el('g',{},parent);
  const vert=Math.abs(x1-x2)<.01;
  const exts=[];
  (o.ext||[]).forEach(e=>{exts.push(el('line',{x1:e[0],y1:e[1],x2:e[2],y2:e[3],stroke:col,'stroke-width':.75,fill:'none'},g));});
  const line=el('line',{x1,y1,x2,y2,stroke:col,'stroke-width':1.25},g);
  const ticks=[[x1,y1],[x2,y2]].map(p=>el('line',{x1:p[0]-6,y1:p[1]+6,x2:p[0]+6,y2:p[1]-6,stroke:col,'stroke-width':1.6},g));
  const tx=o.tx!==undefined?o.tx:(x1+x2)/2, ty=o.ty!==undefined?o.ty:(y1+y2)/2;
  const attrs={x:tx,y:ty,'text-anchor':o.anchor||'middle',class:o.key?'key':'dimt',style:'fill:'+col};
  if(o.rot)attrs.transform=`rotate(-90 ${tx} ${ty})`;
  const text=el('text',attrs,g);text.textContent=label;
  return {g,exts,line,ticks,text,label,x1,y1,x2,y2,start:o.start};
}

/* =========================================================
   BUILD LAYERS
========================================================= */
defs(blue,'blue');defs(paper,'paper');
base(blue,'blue');base(paper,'paper');

/* ---- BLUE: plan (camera group) ---- */
const camClipD=el('clipPath',{id:'camclip'},el('defs',{},blue));el('rect',{x:41,y:41,width:1838,height:998},camClipD);
const camW=el('g',{'clip-path':'url(#camclip)'},blue);
const cam=el('g',{id:'cam'},camW);
const P={};
// hatch ring
const ring=el('path',{d:'M976 176H1752V824H976Z M1000 200V800H1728V200Z','fill-rule':'evenodd',fill:'url(#hatch_blue)',opacity:1},cam);
P.ring=ring;
P.wallOut=el('path',{d:'M976 176H1752V824H976Z',class:'ln'},cam);
P.wallIn=el('path',{d:'M1000 200H1728V800H1000Z',class:'wall'},cam);
// window
P.winCut=el('rect',{x:1220,y:177,width:288,height:24,fill:'#1B3553'},cam);
P.win=el('g',{},cam);
[180,188,196].forEach(y=>el('line',{x1:1220,y1:y,x2:1508,y2:y,class:'fine'},P.win));
el('line',{x1:1220,y1:176,x2:1220,y2:200,class:'fine'},P.win);el('line',{x1:1508,y1:176,x2:1508,y2:200,class:'fine'},P.win);
// door
P.doorCut=el('rect',{x:1727,y:640,width:26,height:144,fill:'#1B3553'},cam);
P.door=el('g',{},cam);
el('line',{x1:1728,y1:640,x2:1752,y2:640,class:'fine'},P.door);el('line',{x1:1728,y1:784,x2:1752,y2:784,class:'fine'},P.door);
P.leaf=el('line',{x1:1728,y1:784,x2:1584,y2:784,class:'ln'},cam);
P.swing=el('path',{d:'M1584 784A144 144 0 0 1 1728 640',class:'hid'},cam);
// radiator
P.rad=el('g',{},cam);
el('rect',{x:1004,y:600,width:24,height:160,class:'ln'},P.rad);
for(let i=1;i<8;i++)el('line',{x1:1004,y1:600+i*20,x2:1028,y2:600+i*20,class:'fine'},P.rad);
// table + chairs
P.table=el('rect',{id:'planTable',x:1172,y:416,width:384,height:168,class:'ln'},cam);
P.tgrain=el('g',{opacity:.5},cam);
for(let i=1;i<6;i++)el('line',{x1:1180,y1:416+i*28,x2:1548,y2:416+i*28,stroke:'#EDE6D6','stroke-width':.6,'stroke-opacity':.5},P.tgrain);
P.chairs=[];
[1220,1316,1412,1508].forEach(cx=>{
  P.chairs.push(el('rect',{x:cx-36,y:340,width:72,height:64,rx:10,class:'hid'},cam));
  P.chairs.push(el('rect',{x:cx-36,y:596,width:72,height:64,rx:10,class:'hid'},cam));
});
P.tlabel=el('text',{x:1364,y:706,'text-anchor':'middle',class:'lab',text:'DINING TABLE — SEATS 8'},cam);
// dims
const D={};
D.len=dim(cam,1000,140,1728,140,'15′-2″',{ext:[[1000,172,1000,132],[1728,172,1728,132]],ty:128,start:'00′-0″'});
D.dep=dim(cam,940,200,940,800,'12′-6″',{ext:[[972,200,932,200],[972,800,932,800]],rot:1,tx:926,ty:500,start:'00′-0″'});
D.eL=dim(cam,1000,500,1172,500,'43″',{ty:490,tx:1086});
D.eR=dim(cam,1556,500,1728,500,'43″',{ty:490,tx:1642});
D.sT=dim(cam,1150,200,1150,416,'54″',{ext:[[1142,416,1168,416]],anchor:'start',tx:1164,ty:250});
D.sB=dim(cam,1150,584,1150,800,'54″',{ext:[[1142,584,1168,584]],anchor:'end',tx:1136,ty:700});
D.tl=dim(cam,1172,316,1556,316,'96″',{ext:[[1172,410,1172,308],[1556,410,1556,308]],ty:302,col:RED,key:1});
D.tw=dim(cam,1524,416,1524,584,'42″',{anchor:'end',tx:1510,ty:508});
P.clr=el('text',{x:1164,y:278,'text-anchor':'start',class:'lab',text:'CLEARANCE'},cam);
P.lWin=el('text',{x:1364,y:238,'text-anchor':'middle',class:'lab',text:'WINDOW'},cam);
P.lDoor=el('text',{x:1712,y:624,'text-anchor':'end',class:'lab',text:'DOOR'},cam);
P.lRad=el('text',{x:1004,y:786,class:'lab',text:'RADIATOR'},cam);
// cursor
P.cur=el('g',{opacity:0},cam);
el('line',{x1:-20,y1:0,x2:20,y2:0,class:'fine'},P.cur);el('line',{x1:0,y1:-20,x2:0,y2:20,class:'fine'},P.cur);
P.curc=el('circle',{cx:0,cy:0,r:10,class:'fine'},P.cur);

/* ---- elevation builder (both layers) ---- */
function buildElev(parent,mode){
  const E={g:el('g',{},parent)};
  const g=E.g;
  E.floor=el('line',{x1:940,y1:780,x2:1788,y2:780,class:'ln'},g);
  E.parts=el('g',{},g);
  E.slab=null;
  E.legL=el('rect',{x:1004,y:554,width:28,height:226,class:'ln'},E.parts);
  E.legR=el('rect',{x:1696,y:554,width:28,height:226,class:'ln'},E.parts);
  E.apron=el('rect',{x:1032,y:554,width:664,height:32,class:'ln'},E.parts);
  E.dims=el('g',{},g);
  E.d96=dim(E.dims,980,500,1748,500,'96″',{ext:[[980,534,980,492],[1748,534,1748,492]],ty:488});
  E.d30=dim(E.dims,1790,540,1790,780,'30″',{ext:[[1752,540,1796,540]],anchor:'start',tx:1802,ty:670});
  E.d134=dim(E.dims,946,540,946,554,'1¾″',{ext:[[976,540,938,540],[976,554,938,554]],anchor:'end',tx:924,ty:552});
  E.label=el('text',{x:1364,y:828,'text-anchor':'middle',class:'lab',text:'FRONT ELEVATION'},E.dims);
  return E;
}
const eB=buildElev(blue,'blue');
// slab (morph target) on blue, screen space
const slabB=el('rect',{id:'slabB',x:1172,y:416,width:384,height:168,class:'ln',opacity:0},blue);
// detail A
const det=el('g',{id:'det'},blue);
const dclip=el('clipPath',{id:'dclip'},el('defs',{},det));el('circle',{cx:1110,cy:330,r:110},dclip);
const dj=el('circle',{cx:1018,cy:575,r:56,class:'hid'},det);
const dlead=el('line',{x1:1037.7,y1:522.6,x2:1071.3,y2:433,class:'fine'},det);
const dc=el('circle',{cx:1110,cy:330,r:110,class:'ln'},det);
const dcont=el('g',{'clip-path':'url(#dclip)'},det);
el('rect',{x:1040,y:200,width:98,height:240,class:'ln'},dcont);
el('rect',{x:1138,y:274,width:120,height:112,class:'ln'},dcont);
el('rect',{x:1060,y:296,width:90,height:68,class:'hid'},dcont);
el('rect',{x:1064,y:300,width:74,height:60,class:'ln',opacity:.0},dcont);
el('circle',{cx:1094,cy:330,r:9,class:'ln'},dcont);
el('line',{x1:1094,y1:300,x2:1094,y2:360,class:'hid'},dcont);
el('path',{d:'M1138 286H1216M1138 374H1216',class:'fine'},dcont);
const dbub=el('g',{},det);
el('circle',{cx:1004,cy:196,r:22,class:'ln'},dbub);
el('text',{x:1004,y:206,'text-anchor':'middle',style:'font-size:28px',text:'A'},dbub);
const dcap=el('text',{x:1042,y:202,class:'lab',text:'DETAIL A — DRAWBORED MORTISE & TENON',style:'font-size:22px;letter-spacing:.04em'},det);
// crop caption: shorten spacing to fit
const capT=dcap;

blue.appendChild(frame(blue));
// title block (blue)
const tbB=el('g',{id:'tbB'},blue);
function titleBlock(parent){
  const g=el('g',{},parent);
  const rect=el('rect',{x:1476,y:924,width:364,height:116,class:'frm',fill:'none'},g);
  const div=el('line',{x1:1580,y1:924,x2:1580,y2:1040,class:'frm'},g);
  return {g,rect,div};
}
const tB=titleBlock(tbB);
const mkB=mark(tbB,1496,950,64,'#EDE6D6','#EDE6D6');
el('text',{x:1596,y:960,style:"font-family:'Fraunces',serif;font-weight:600;font-size:20px;letter-spacing:.1em",text:'VERNE WOODWORKS'},tbB);
el('text',{x:1596,y:992,style:'font-size:18px',text:'DWG VW-0226 · TABLE'},tbB);
el('text',{x:1596,y:1020,style:'font-size:18px',text:'1:24 · SHEET 01/01'},tbB);
// dashed-line fix for small caption: nothing

/* ---- PAPER ---- */
const paperBody=el('g',{id:'pbody'},paper);
const shadow=el('ellipse',{cx:1364,cy:784,rx:420,ry:14,fill:'#221C17',opacity:0,style:'filter:blur(14px)'},paperBody);
const tableP=el('g',{id:'tableP'},paperBody);
const pdefs=el('defs',{},paper);
const walP=el('pattern',{id:'walnut',x:980,y:540,width:768,height:240,patternUnits:'userSpaceOnUse'},pdefs);
const walI=el('image',{width:768,height:240,preserveAspectRatio:'none'},walP);
const oakP=el('pattern',{id:'oakv',x:980,y:540,width:768,height:240,patternUnits:'userSpaceOnUse'},pdefs);
const oakI=el('image',{width:768,height:240,preserveAspectRatio:'none'},oakP);
const oakHP=el('pattern',{id:'oakh',x:0,y:0,width:1320,height:60,patternUnits:'userSpaceOnUse'},pdefs);
const oakHI=el('image',{width:1320,height:60,preserveAspectRatio:'none'},oakHP);
const bandP=el('pattern',{id:'bandp',x:0,y:0,width:90,height:1280,patternUnits:'userSpaceOnUse',patternTransform:'translate(-90,-100)'},pdefs);
const bandI=el('image',{width:90,height:1280,preserveAspectRatio:'none'},bandP);
const tclip=el('clipPath',{id:'tclip'},pdefs);
el('rect',{x:980,y:540,width:768,height:14},tclip);el('rect',{x:1004,y:554,width:28,height:226},tclip);el('rect',{x:1696,y:554,width:28,height:226},tclip);el('rect',{x:1032,y:554,width:664,height:32},tclip);
const topg=el('linearGradient',{id:'topl',x1:0,y1:0,x2:0,y2:1},pdefs);
el('stop',{offset:0,'stop-color':'#fff','stop-opacity':.22},topg);el('stop',{offset:1,'stop-color':'#000','stop-opacity':.18},topg);
const sheng=el('linearGradient',{id:'sheen',x1:0,y1:0,x2:1,y2:0},pdefs);
el('stop',{offset:0,'stop-color':'#fff','stop-opacity':0},sheng);el('stop',{offset:.5,'stop-color':'#fff','stop-opacity':.16},sheng);el('stop',{offset:1,'stop-color':'#fff','stop-opacity':0},sheng);
// wood shapes
const woodParts=el('g',{},tableP);
el('rect',{x:1004,y:554,width:28,height:226,fill:'url(#oakv)'},woodParts);
el('rect',{x:1696,y:554,width:28,height:226,fill:'url(#oakv)'},woodParts);
el('rect',{x:1032,y:554,width:664,height:32,fill:'url(#walnut)'},woodParts);
el('rect',{x:980,y:540,width:768,height:14,fill:'url(#walnut)'},woodParts);
// lighting on wood
el('rect',{x:1004,y:554,width:28,height:226,fill:'#000',opacity:.12},woodParts);
el('rect',{x:1696,y:554,width:28,height:226,fill:'#000',opacity:.12},woodParts);
el('rect',{x:1032,y:554,width:664,height:32,fill:'url(#topl)',opacity:.7},woodParts);
el('rect',{x:980,y:540,width:768,height:14,fill:'url(#topl)'},woodParts);
el('line',{x1:980,y1:540.7,x2:1748,y2:540.7,stroke:'#fff','stroke-opacity':.4,'stroke-width':1},woodParts);
const patina=el('rect',{x:970,y:530,width:790,height:260,fill:'#7A4A26',opacity:0,'clip-path':'url(#tclip)'},tableP);
const sweep=el('rect',{x:800,y:530,width:220,height:260,fill:'url(#sheen)',opacity:1,'clip-path':'url(#tclip)'},tableP);
const eP=buildElev(tableP,'paper');
// slab outline in paper
const slabP=el('rect',{x:980,y:540,width:768,height:14,class:'ln'},eP.parts);
[eP.legL,eP.legR,eP.apron,slabP].forEach(e=>e.setAttribute('class','ln'));
eP.g.querySelector('line').setAttribute('opacity',1);
// move dims outside of tableP so scale works? keep inside (they fade before scaling)
// callouts
const cal=el('g',{id:'cal'},paperBody);
const CAL=[
 {dot:[1500,547],el:[1500,470],tx:1516,ty:478,t:'TOP: BLACK WALNUT, 8/4'},
 {dot:[1180,547],el:[1180,420],tx:1196,ty:428,t:'FINISH: HAND-RUBBED OIL'},
 {dot:[1006,700],el:[1006,850],tx:1022,ty:858,t:'BASE: WHITE OAK'}];
CAL.forEach(c=>{
  const g=el('g',{},cal);
  c.dotEl=el('circle',{cx:c.dot[0],cy:c.dot[1],r:3.5,fill:'var(--line)'},g);
  const horiz=c.el[1]<600?`M${c.dot[0]},${c.dot[1]}V${c.el[1]}H${c.tx-6}`:`M${c.dot[0]},${c.dot[1]}V${c.el[1]}H${c.tx-6}`;
  c.path=el('path',{d:horiz,class:'fine',stroke:'#221C17'},g);
  c.text=el('text',{x:c.tx,y:c.ty,style:'font-size:22px;letter-spacing:.04em',text:c.t},g);
  c.g=g;
});
// ruler
const ruler=el('g',{id:'ruler'},paperBody);
const rclip=el('clipPath',{id:'rclip'},pdefs);el('rect',{x:120,y:900,width:1320,height:60,rx:2},rclip);
const rbody=el('g',{},ruler);
el('rect',{x:120,y:900,width:1320,height:60,fill:'#C79A62'},rbody);
el('rect',{x:120,y:900,width:1320,height:60,fill:'url(#oakh)'},rbody);
el('rect',{x:120,y:900,width:1320,height:60,fill:'url(#topl)',opacity:.5},rbody);
const rticks=el('g',{'clip-path':'url(#rclip)'},ruler);
const rscroll=el('g',{},rticks);
const YR0=2026;
const RT={};
for(let i=-112;i<=125;i++){
  const x=1000+i*8;
  let h=12;if(i%5===0)h=20;if(i%25===0)h=32;
  el('line',{x1:x,y1:900,x2:x,y2:900+h,stroke:'#221C17','stroke-width':i%25===0?1.6:1},rscroll);
  if(i%25===0&&i>=0)el('text',{x:x,y:954,'text-anchor':'middle',style:'font-size:26px;fill:#221C17',text:String(YR0+i)},rscroll);
}
el('rect',{x:120,y:900,width:16,height:60,fill:'#B08A4E'},ruler);
el('rect',{x:1424,y:900,width:16,height:60,fill:'#B08A4E'},ruler);
el('rect',{x:120,y:900,width:1320,height:60,fill:'none',stroke:'#221C17','stroke-width':1.25,'stroke-opacity':.7},ruler);
const idx=el('line',{x1:1000,y1:892,x2:1000,y2:968,stroke:RED,'stroke-width':2.5},ruler);
paperBody.appendChild(ruler);
paper.appendChild(frame(paper));
// title block / end card (paper)
const tbP=el('g',{id:'tbP'},paper);
const tP=titleBlock(tbP);
const tbSmall=el('g',{},tbP);
const mkP=mark(tbSmall,1496,950,64,'#5A3825','#221C17');
el('text',{x:1596,y:960,style:"font-family:'Fraunces',serif;font-weight:600;font-size:20px;letter-spacing:.1em",text:'VERNE WOODWORKS'},tbSmall);
el('text',{x:1596,y:992,style:'font-size:18px',text:'DWG VW-0226 · TABLE'},tbSmall);
el('text',{x:1596,y:1020,style:'font-size:18px',text:'1:24 · SHEET 01/01'},tbSmall);
// end card content
const ec=el('g',{id:'ec'},tbP);
const ecMark=mark(ec,440,350,120,'#5A3825','#221C17');
const ecWord=el('g',{},ec);
const ecWText=el('text',{x:600,y:420,style:"font-family:'Fraunces',serif;font-weight:600;font-size:64px;letter-spacing:.12em"},ecWord);
ecWText.textContent='VERNE WOODWORKS';
const ecDesc=el('text',{x:600,y:480,style:"font-family:'Fraunces',serif;font-weight:400;font-size:38px"},ec);ecDesc.textContent='Bespoke furniture · Brooklyn, NY';
const ecRule=el('line',{x1:600,y1:530,x2:1480,y2:530,class:'fine'},ec);
const ecCta=el('text',{x:600,y:620,style:"font-family:'Fraunces',serif;font-weight:400;font-style:italic;font-size:56px"},ec);ecCta.textContent='Request a quote';
const ecUrl=el('text',{x:1480,y:620,'text-anchor':'end',style:'font-size:40px'},ec);ecUrl.textContent='vernewoodworks.com';
const ecUl=el('path',{d:'M1050 637C1140 633 1230 640 1320 636S1430 638 1482 634',fill:'none',stroke:RED,'stroke-width':2.5,'stroke-linecap':'round'},ec);
const ecCellRule=el('line',{x1:360,y1:710,x2:1560,y2:710,class:'frm'},ec);
const ecCellV2=el('line',{x1:1160,y1:710,x2:1160,y2:830,class:'frm'},ec);
const ecCells=el('g',{},ec);
[[384,'DRAWN BY: VERNE WOODWORKS'],[784,'FOR: YOUR ROOM'],[1184,'SHEET 01/01']].forEach(c=>el('text',{x:c[0],y:777,style:'font-size:20px;letter-spacing:.08em',text:c[1]},ecCells));

/* ---- band (shaving) ---- */
const band=el('g',{id:'band'},bandsvg);
const bd=el('defs',{},bandsvg);
const bsh=el('linearGradient',{id:'bsh',x1:0,y1:0,x2:1,y2:0},bd);
el('stop',{offset:0,'stop-color':'#221C17','stop-opacity':0},bsh);el('stop',{offset:1,'stop-color':'#221C17','stop-opacity':.22},bsh);
el('rect',{x:-150,y:-140,width:60,height:1360,fill:'url(#bsh)'},band);
const bandPat=bandP.cloneNode(true);bandPat.id='bandp2';bandPat.removeAttribute('patternTransform');bandPat.setAttribute('patternUnits','userSpaceOnUse');bandPat.setAttribute('x',-90);bandPat.setAttribute('y',-100);
bd.appendChild(bandPat);
el('path',{d:'M-90 -100H-8C16 300 16 800 -8 1180H-90Z',fill:'url(#bandp2)'},band);
el('path',{d:'M-90 -100H-8C16 300 16 800 -8 1180H-90Z',fill:'#C79A62',opacity:.25},band);
el('path',{d:'M-14 -100C10 300 10 800 -14 1180',fill:'none',stroke:'#DDB783','stroke-width':12,opacity:.9},band);
el('path',{d:'M-1 -100C21 300 21 800 -1 1180',fill:'none',stroke:'#221C17','stroke-width':1.5,opacity:.4},band);

/* ---------- textures ---------- */
function makeTex(w,h,vertical,pal,seed,noise2D,rays){
  const c=document.createElement('canvas');c.width=w;c.height=h;const x=c.getContext('2d');
  const img=x.createImageData(w,h);const rr=KK.rng(seed);
  const cols=pal.map(p=>[parseInt(p.slice(1,3),16),parseInt(p.slice(3,5),16),parseInt(p.slice(5,7),16)]);
  for(let j=0;j<h;j++)for(let i=0;i<w;i++){
    const a=vertical?j:i, b=vertical?i:j; // a along grain, b across
    const v=Math.sin((b*0.12+noise2D(a*0.0015,b*0.02)*6+noise2D(a*0.01,b*0.1)*0.6)*Math.PI);
    const t=(v+1)/2;
    let col;
    if(t<.5){const u=t*2;col=cols[0].map((c0,k)=>c0+(cols[1][k]-c0)*u);}else{const u=(t-.5)*2;col=cols[1].map((c0,k)=>c0+(cols[2][k]-c0)*u);}
    const n=(noise2D(i*.5+99,j*.5+7)*.5+.5);const f=.94+n*.1;
    const p=(j*w+i)*4;img.data[p]=col[0]*f;img.data[p+1]=col[1]*f;img.data[p+2]=col[2]*f;img.data[p+3]=255;
  }
  x.putImageData(img,0,0);
  // pores
  x.fillStyle='rgba(20,10,4,0.28)';
  for(let k=0;k<w*h*0.004;k++){const px=rr()*w,py=rr()*h;vertical?x.fillRect(px,py,1,4):x.fillRect(px,py,4,1);}
  if(rays){x.fillStyle='rgba(255,240,210,0.09)';for(let k=0;k<w*h*0.0015;k++){const px=rr()*w,py=rr()*h;vertical?x.fillRect(px,py,8,2):x.fillRect(px,py,2,8);}}
  return c.toDataURL();
}
function noiseFn(seed){
  // small seeded value-noise (deterministic)
  const r=KK.rng(seed);const N=256;const perm=[];for(let i=0;i<N;i++)perm.push(r());
  const g=(ix,iy)=>perm[(((ix*73856093)^(iy*19349663))>>>0)%N];
  const s=t=>t*t*(3-2*t);
  return (x,y)=>{const ix=Math.floor(x),iy=Math.floor(y),fx=s(x-ix),fy=s(y-iy);
    const a=g(ix,iy),b=g(ix+1,iy),c=g(ix,iy+1),d=g(ix+1,iy+1);
    return ((a+(b-a)*fx)+((c+(d-c)*fx)-(a+(b-a)*fx))*fy)*2-1;};
}
const texReady=(async()=>{
  let n2;
  try{const m=await import('../../node_modules/simplex-noise/dist/esm/simplex-noise.js');const sn=m.createNoise2D(KK.rng(226));n2=sn;}catch(e){n2=noiseFn(226);}
  const wal=makeTex(1536,480,false,['#3A2418','#5A3825','#7A5236'],11,n2,false);
  const oakV=makeTex(768,480,true,['#A97C48','#B98C56','#C79A62'],12,n2,true);
  const oakH=makeTex(1320,120,false,['#A97C48','#BC8F58','#D2A56C'],13,n2,true);
  const oakB=makeTex(180,1280,true,['#B58750','#C79A62','#D9B17A'],14,n2,true);
  [walI].forEach(i=>i.setAttribute('href',wal));
  oakI.setAttribute('href',oakV);oakHI.setAttribute('href',oakH);
  bandPat.querySelector('image')?0:0;
  const bi=el('image',{width:90,height:1280,preserveAspectRatio:'none',href:oakB},bandPat);
})();

/* =========================================================
   TEXT COLUMN
========================================================= */
const txt=$('txt');
const TX=[
 {id:'g0',k:'SHOP DRAWING — DINING ROOM, PARK SLOPE',l:['Before the wood,','the <i>drawing.</i>']},
 {id:'g1',k:'01 — MEASURED IN YOUR HOME',l:['Designed for','<i>your</i> room.']},
 {id:'g2',k:'02 — BUILT IN BROOKLYN',l:['Solid walnut.','Solid <i>oak.</i>'],sub:'No veneer. Joined by hand, one piece at a time.',ink:1},
 {id:'g3',k:'03 — MADE TO BE HANDED DOWN',l:['Built to last','<b>100</b> years.'],big:1,ink:1}];
const TXD={};
TX.forEach(g=>{
  const d=document.createElement('div');d.className='g'+(g.ink?' ink':'');d.id=g.id;
  d.innerHTML=`<div class="kick">${g.k}</div><div class="h1${g.big?' big':''}">${g.l.map(x=>`<div class="mask"><span>${x}</span></div>`).join('')}</div>${g.sub?`<div class="sub">${g.sub}</div>`:''}`;
  txt.appendChild(d);
  TXD[g.id]={kick:d.querySelector('.kick'),lines:[...d.querySelectorAll('.mask>span')],sub:d.querySelector('.sub'),final:g.k};
});

/* =========================================================
   TIMELINE
========================================================= */
const tl=gsap.timeline({paused:true});
const cam0={s:1,x:0};
const camP={s:1};
const wipe={X:-60};
const scr=[]; // scramble items
function scramble(elm,final,t0,dur,pool,start){scr.push({elm,final,t0,dur,pool:pool||'▮/0123456789',start:start===undefined?'':start});}

function maskIn(g,t0,stag){
  const d=TXD[g];
  tl.fromTo(d.lines,{yPercent:112},{yPercent:0,duration:.7,ease:'expo.out',stagger:stag||.12},t0);
}
function maskOut(g,t0){
  const d=TXD[g];
  tl.to(d.lines,{yPercent:-112,duration:.35,ease:'power2.in',stagger:.05},t0);
  tl.to(d.kick,{opacity:0,duration:.25,ease:'power2.in'},t0);
}
function kickIn(g,t0){
  const d=TXD[g];
  tl.fromTo(d.kick,{opacity:0,y:8},{opacity:1,y:0,duration:.5,ease:'power3.out'},t0);
}

// ---- Beat 0 ----
scramble(TXD.g0.kick,TXD.g0.final,0.0,0.5);
tl.fromTo(TXD.g0.kick,{opacity:0},{opacity:1,duration:.15},0);
tl.fromTo(TXD.g0.lines,{yPercent:112},{yPercent:0,duration:.8,ease:'expo.out',stagger:.12},0.1);
// walls
tl.fromTo(P.wallIn,{drawSVG:'0% 20%'},{drawSVG:'0% 100%',duration:1.4,ease:'power1.inOut'},0);
tl.fromTo(P.wallOut,{drawSVG:'0% 20%'},{drawSVG:'0% 100%',duration:1.4,ease:'power1.inOut'},0.1);
tl.fromTo(P.ring,{opacity:0},{opacity:1,duration:.6,ease:'power1.out'},.9);
tl.fromTo([P.winCut,P.win],{opacity:0},{opacity:1,duration:.3},1.0);
tl.fromTo(P.win.children,{drawSVG:'0%'},{drawSVG:'100%',duration:.5,stagger:.05,ease:'power2.inOut'},1.0);
tl.fromTo([P.doorCut,P.door],{opacity:0},{opacity:1,duration:.3},1.1);
tl.fromTo(P.leaf,{drawSVG:'0%'},{drawSVG:'100%',duration:.4,ease:'power2.out'},1.3);
tl.fromTo(P.swing,{opacity:0},{opacity:1,duration:.6,ease:'power2.inOut'},1.4);
function animDim(d,t0,o){
  o=o||{};const T=o.speed||1;
  d.exts.forEach(e=>tl.fromTo(e,{drawSVG:'0%'},{drawSVG:'100%',duration:.25*T,ease:'power2.out'},t0));
  tl.fromTo(d.line,{drawSVG:'50% 50%'},{drawSVG:'0% 100%',duration:.4*T,ease:'power2.inOut'},t0+.15*T);
  d.ticks.forEach((tk,i)=>{const cx=i?d.x2:d.x1,cy=i?d.y2:d.y1;tl.fromTo(tk,{scale:0,svgOrigin:`${cx} ${cy}`},{scale:1,svgOrigin:`${cx} ${cy}`,duration:.3,ease:'back.out(3)'},t0+.4*T+i*.04);});
  if(d.start){scramble(d.text,d.label,t0+.3*T,.5,'0123456789',d.start);tl.fromTo(d.text,{opacity:0},{opacity:1,duration:.1},t0+.3*T);}
  else tl.fromTo(d.text,{opacity:0,y:6},{opacity:1,y:0,duration:.3,ease:'power2.out'},t0+.45*T);
}
animDim(D.len,1.2);animDim(D.dep,1.45);
[[P.lWin,1.8],[P.lDoor,1.9],[P.lRad,2.0]].forEach(a=>tl.fromTo(a[0],{opacity:0,y:8},{opacity:1,y:0,duration:.4,ease:'power2.out'},a[1]));
tl.fromTo(P.rad.children,{drawSVG:'0%'},{drawSVG:'100%',duration:.5,stagger:.03,ease:'power2.inOut'},1.8);
tl.fromTo(P.table,{drawSVG:'0%'},{drawSVG:'100%',duration:.6,ease:'power2.inOut'},2.2);
tl.fromTo(P.tgrain,{opacity:0},{opacity:.5,duration:.4},2.6);
P.chairs.forEach((c,i)=>tl.fromTo(c,{opacity:0,y:8},{opacity:1,y:0,duration:.4,ease:'power2.out'},2.35+i*.05));
tl.fromTo(P.tlabel,{opacity:0,y:8},{opacity:1,y:0,duration:.4,ease:'power2.out'},2.6);
// camera drift + push
tl.to(camP,{s:1.02,duration:3.2,ease:'none'},0);
tl.to(camP,{s:1.3,duration:1,ease:'power3.inOut'},3.2);
tl.to(camP,{s:1,duration:.6,ease:'power3.inOut'},6.5);
maskOut('g0',3.2);
// ---- Beat 1 ----
kickIn('g1',3.6);maskIn('g1',3.6);
animDim(D.eL,4.0);animDim(D.eR,4.3);animDim(D.sT,4.6);animDim(D.sB,4.9);
tl.fromTo(P.clr,{opacity:0,y:6},{opacity:1,y:0,duration:.3},5.05);
animDim(D.tl,4.8);tl.fromTo(D.tl.line,{stroke:'#EDE6D6'},{stroke:RED,duration:.01},4.8);
animDim(D.tw,5.1,{speed:.9});
tl.fromTo(P.cur,{opacity:0,x:1172,y:416},{opacity:1,x:1172,y:416,duration:.2},5.6);
tl.to(P.cur,{x:1100,y:322,duration:.7,ease:'power2.inOut'},5.7);
tl.fromTo(P.curc,{scale:1,svgOrigin:'0 0'},{scale:1.4,svgOrigin:'0 0',duration:.15,yoyo:true,repeat:1,ease:'power1.inOut'},6.45);
tl.to(P.cur,{opacity:0,duration:.25},6.5);
maskOut('g1',6.6);
// ---- Transition 2 ----
const planFade=[P.ring,P.wallOut,P.wallIn,P.winCut,P.win,P.doorCut,P.door,P.leaf,P.swing,P.rad,P.tgrain,P.tlabel,P.clr,P.lWin,P.lDoor,P.lRad,...P.chairs,D.len.g,D.dep.g,D.eL.g,D.eR.g,D.sT.g,D.sB.g,D.tl.g,D.tw.g];
tl.to(planFade,{opacity:0,duration:.4,ease:'power2.in'},6.6);
tl.to(P.table,{opacity:0,duration:.01},7.0);
tl.fromTo(slabB,{opacity:0},{opacity:1,duration:.01,immediateRender:false},7.0);
tl.fromTo(slabB,{attr:{x:1172,y:416,width:384,height:168}},{attr:{x:980,y:540,width:768,height:14},duration:.55,ease:'power3.inOut',immediateRender:false},6.95);
// elevation build
tl.fromTo(eB.floor,{drawSVG:'0%'},{drawSVG:'100%',duration:.5,ease:'power2.inOut'},7.1);
[eB.legL,eB.legR,eB.apron].forEach((p,i)=>tl.fromTo(p,{drawSVG:'0%'},{drawSVG:'100%',duration:.45,ease:'power2.out'},7.3+i*.06));
animDim(eB.d96,7.4,{speed:.8});animDim(eB.d30,7.5,{speed:.8});animDim(eB.d134,7.55,{speed:.8});
tl.fromTo(eB.label,{opacity:0,y:6},{opacity:1,y:0,duration:.35},7.7);
// detail A
tl.fromTo(dj,{opacity:0},{opacity:1,duration:.35,ease:'power2.inOut'},7.7);
tl.fromTo(dlead,{drawSVG:'0%'},{drawSVG:'100%',duration:.25,ease:'power2.inOut'},7.9);
tl.fromTo(dc,{drawSVG:'0%'},{drawSVG:'100%',duration:.45,ease:'power2.inOut'},8.0);
tl.fromTo(dcont,{opacity:0},{opacity:1,duration:.3},8.1);
tl.fromTo([dbub,dcap],{opacity:0,y:6},{opacity:1,y:0,duration:.3},8.15);
// keep the sheet slightly alive
// ---- wipe ----
tl.to(wipe,{X:2080,duration:.9,ease:'power2.inOut'},8.4);
// paper: ghost outlines
const paperLines=[eP.legL,eP.legR,eP.apron,slabP,eP.floor];
tl.fromTo([eP.legL,eP.legR,eP.apron,slabP],{opacity:.6},{opacity:.25,duration:.9,ease:'none'},9.1);
tl.fromTo(shadow,{opacity:0},{opacity:.18,duration:.6},9.2);
tl.to(eP.dims,{opacity:0,duration:.3},9.6);
// ---- Beat 2 ----
kickIn('g2',9.0);maskIn('g2',9.0);
tl.fromTo(TXD.g2.sub,{opacity:0,y:10},{opacity:1,y:0,duration:.5,ease:'power3.out'},9.6);
CAL.forEach((c,i)=>{const t0=10.0+i*.25;
  tl.fromTo(c.dotEl,{scale:0,svgOrigin:c.dot.join(' ')},{scale:1,svgOrigin:c.dot.join(' '),duration:.25,ease:'back.out(3)'},t0);
  tl.fromTo(c.path,{drawSVG:'0%'},{drawSVG:'100%',duration:.4,ease:'power2.out'},t0+.1);
  tl.fromTo(c.text,{opacity:0,y:6},{opacity:1,y:0,duration:.3,ease:'power2.out'},t0+.4);
});
tl.fromTo(sweep,{attr:{x:900}},{attr:{x:1780},duration:3,ease:'none'},9.5);
// ---- Transition 4 ----
maskOut('g2',12.6);
tl.to(TXD.g2.sub,{opacity:0,duration:.3,ease:'power2.in'},12.6);
tl.to(cal,{opacity:0,duration:.3},12.6);
tl.to(tableP,{scale:.86,y:-30,svgOrigin:'1364 600',duration:.5,ease:'power3.inOut'},12.6);
tl.fromTo(ruler,{x:1400},{x:0,duration:.5,ease:'expo.out'},12.6);
tl.fromTo(ruler,{opacity:0},{opacity:1,duration:.01},12.6);
// ---- Beat 3 ----
kickIn('g3',13.0);maskIn('g3',13.0);
tl.fromTo(rscroll,{x:0},{x:-800,duration:2.4,ease:'power2.inOut'},13.2);
tl.to(patina,{opacity:.14,duration:2.4,ease:'none'},13.2);
tl.fromTo(idx,{scaleY:1,svgOrigin:'1000 930'},{scaleY:1.15,svgOrigin:'1000 930',duration:.15,yoyo:true,repeat:1,ease:'power2.inOut'},15.6);
// ---- Transition 5 ----
maskOut('g3',16.4);
tl.to([tableP,ruler,shadow],{opacity:0,y:'-=12',duration:.35,ease:'power2.in'},16.4);
tl.to(tbSmall,{opacity:0,duration:.2},16.4);
tl.to(tP.rect,{attr:{x:360,y:250,width:1200,height:580},duration:.7,ease:'power3.inOut'},16.5);
tl.to(tP.div,{attr:{x1:760,x2:760,y1:710,y2:830},duration:.7,ease:'power3.inOut'},16.5);
tl.fromTo(ecCellRule,{drawSVG:'0%'},{drawSVG:'100%',duration:.3,ease:'power2.out'},17.1);
tl.fromTo(ecCellV2,{drawSVG:'0%'},{drawSVG:'100%',duration:.3,ease:'power2.out'},17.1);
// end card items
tl.fromTo(ecMark.sq,{drawSVG:'0%'},{drawSVG:'100%',duration:.4,ease:'power2.inOut'},17.2);
tl.fromTo([ecMark.tail,ecMark.jl],{opacity:0},{opacity:1,duration:.3},17.5);
tl.fromTo(ecWText,{opacity:0,y:30},{opacity:1,y:0,duration:.6,ease:'expo.out'},17.35);
tl.fromTo(ecDesc,{opacity:0,y:14},{opacity:1,y:0,duration:.5,ease:'power3.out'},17.7);
tl.fromTo(ecRule,{drawSVG:'0%'},{drawSVG:'100%',duration:.4,ease:'power2.inOut'},17.9);
tl.fromTo([ecCta,ecUrl],{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'expo.out',stagger:.1},18.1);
tl.fromTo(ecUl,{drawSVG:'0%'},{drawSVG:'100%',duration:.5,ease:'power2.inOut'},18.6);
tl.fromTo(ecCells,{opacity:0},{opacity:1,duration:.4},18.3);
// hide end card elements until their times (initial state handled by fromTo immediateRender)
tl.set(ec,{visibility:'visible'},0);

// initial states for stuff shown only later
tl.set([eB.legL,eB.legR,eB.apron,eB.floor],{drawSVG:'0%'},0);
tl.set([eB.dims,eB.label,det],{opacity:0},0);
tl.set(eB.dims,{opacity:1},7.35);tl.set(det,{opacity:1},7.65);
tl.set(eB.dims,{opacity:0},0);

/* ---------- apply per-frame ---------- */
function applyState(t){
  // camera
  const s=camP.s,k=KK.clamp((s-1.02)/0.28);
  const ty=-30*k;
  cam.setAttribute('transform',`translate(1364,${500+ty}) scale(${s}) translate(-1364,-500)`);
  // wipe
  const X=wipe.X;
  paper.style.clipPath=`polygon(0px 0px,${X+38}px 0px,${X-38}px 1080px,0px 1080px)`;
  band.setAttribute('transform',`translate(${X},540) skewX(-4) translate(0,-540)`);
  bandsvg.style.display=(X<-100||X>2000)?'none':'block';
  // scrambles
  const fr=Math.floor(t*30);
  scr.forEach((it,n)=>{
    const p=KK.clamp((t-it.t0)/it.dur);
    let out;
    if(t<it.t0)out=it.start;
    else if(p>=1)out=it.final;
    else{
      const rr=KK.rng(fr*131+n*977+5);const nl=Math.floor(p*it.final.length);
      out='';for(let i=0;i<it.final.length;i++){const ch=it.final[i];
        if(i<nl||ch===' '||ch==='—'||ch===','||ch==='′'||ch==='″'||ch==='-'||ch==='.')out+=ch;else out+=it.pool[Math.floor(rr()*it.pool.length)];}
    }
    if(it.elm._last!==out){it.elm.textContent=out;it.elm._last=out;}
  });
  // detail A caption fades with wipe (paper never has it); slab in blue fades at wipe naturally
}
// dim elements inside eP already hidden at start of paper only matters after wipe
const ready=Promise.all([texReady,document.fonts.ready,
  document.fonts.load("400 40px Fraunces"),document.fonts.load("italic 400 40px Fraunces"),document.fonts.load("600 40px Fraunces"),
  document.fonts.load("500 20px 'IBM Plex Mono'")]).then(()=>{tl.seek(0,false);applyState(0);});
window.KLIPT={width:1920,height:1080,fps:30,duration:21,ready,
  render(t){tl.seek(t,false);applyState(t);}};
})();
