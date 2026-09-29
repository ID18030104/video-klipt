import re
s=open('index.src.html').read()
base='/home/user/video-klipt/node_modules/lucide-static/icons/'
for k,f in [('coins','coins'),('gamepad','gamepad-2'),('orbit','orbit'),('beer','beer')]:
    svg=open(base+f+'.svg').read()
    svg=re.sub(r'<!--.*?-->','',svg,flags=re.S)
    svg=re.sub(r'\s+(width|height)="24"','',svg)
    s=s.replace('{{%s}}'%k,svg)
open('index.html','w').write(s)
