from pathlib import Path
import json,html
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; C=json.loads((ROOT/'profile.json').read_text()); SRC=ROOT/'assets/source-prepped.png'; OUT=ROOT/'generated/ascii-portrait.svg'
if not SRC.exists(): raise SystemExit('Missing assets/source-prepped.png. Run prep_photo.py first.')
chars=' .:-=+*#%@'; cols=82; fs=7; lh=10; pad=18
im=Image.open(SRC).convert('L'); rows=max(24,int(cols*(im.height/im.width)*.52)); im=im.resize((cols,rows)); lines=[]
for y in range(rows):
    s=''.join(chars[max(0,min(len(chars)-1,int((255-im.getpixel((x,y)))/256*len(chars))))] for x in range(cols)); lines.append(s.rstrip())
t=C['theme']; W=cols*fs+pad*2; H=rows*lh+pad*2+30
nodes=[]
for i,line in enumerate(lines):
    nodes.append(f'<text x="{pad}" y="{pad+22+i*lh}" class="ascii" style="animation-delay:{i*.018:.3f}s">{html.escape(line)}</text>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>.bg{{fill:{t["background"]}}}.frame{{fill:none;stroke:{t["muted"]};opacity:.55}}.title{{font:600 11px monospace;fill:{t["accent"]}}}.ascii{{font:7px monospace;fill:{t["accent"]};opacity:0;animation:appear .42s ease-out forwards}}@keyframes appear{{0%{{opacity:0;transform:translateX(-3px)}}100%{{opacity:1;transform:translateX(0)}}}}@media(prefers-reduced-motion:reduce){{.ascii{{animation:none;opacity:1}}}}</style><rect class="bg" width="100%" height="100%" rx="8"/><rect class="frame" x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8"/><text x="{pad}" y="16" class="title">./portrait — terminal render</text>{''.join(nodes)}</svg>'''
OUT.parent.mkdir(exist_ok=True); OUT.write_text(svg); print(f'Wrote {OUT}')
