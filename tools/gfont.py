#!/usr/bin/env python3
"""Download a Google Font locally (the renderer has no internet at render time).
Usage: python3 tools/gfont.py "Inter Tight" "wght@400;700;900" pieces/<id>/fonts
       python3 tools/gfont.py "Fraunces" "ital,opsz,wght@0,9..144,300;1,9..144,600" pieces/<id>/fonts
Writes <out>/<slug>.css (+ woff2 files). Link it with <link rel="stylesheet" href="fonts/<slug>.css">."""
import os, re, subprocess, sys, urllib.parse
fam, axes, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
slug = re.sub(r'[^a-z0-9]+', '-', fam.lower()).strip('-')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
url = f"https://fonts.googleapis.com/css2?family={urllib.parse.quote_plus(fam)}:{axes}&display=block"
css = subprocess.run(['curl', '-sf', '-m', '30', '-A', UA, url], capture_output=True, text=True).stdout
if not css: sys.exit(f'font not found: {fam} {axes} — check the family name / axes on fonts.google.com')
# keep latin + latin-ext subsets only (French/English), drop cyrillic/greek/vietnamese blocks
blocks = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*{[^}]*})', css)
keep = [b for s, b in blocks if s in ('latin', 'latin-ext')] or re.findall(r'@font-face\s*{[^}]*}', css)
res = []
for i, b in enumerate(keep):
    src = re.search(r'url\((https://[^)]+)\)', b).group(1)
    fn = f'{slug}-{i:02d}.woff2'
    subprocess.run(['curl', '-sf', '-m', '60', '-o', os.path.join(out, fn), src], check=True)
    res.append(b.replace(src, fn))
open(os.path.join(out, f'{slug}.css'), 'w').write('\n'.join(res) + '\n')
print(f'{out}/{slug}.css  font-family: "{fam}"  ({len(res)} files)')
