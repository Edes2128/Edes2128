from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]; C=json.loads((ROOT/'profile.json').read_text()); D=ROOT/'data/contributions.json'; OUT=ROOT/'generated/contrib-heatmap.svg'; p=json.loads(D.read_text()); days=p.get('days',[])[-371:]
while len(days)<371: days.insert(0,{'date':'','count':0,'level':0})
t=C['theme']; W,H=860,230; left,top,cell,gap=32,58,12,3; colors=[t['grid'],t['accent2'],'#3fae68','#65d18b','#9ce8b4']; rs=[]
for i,d in enumerate(days):
    x=left+(i//7)*(cell+gap); y=top+(i%7)*(cell+gap); lv=max(0,min(4,int(d.get('level',0)))); rs.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{colors[lv]}" class="day" style="animation-delay:{i*.006:.3f}s"><title>{html.escape(d.get("date",""))}: {int(d.get("count",0))} contributions</title></rect>')
total=sum(int(d.get('count',0)) for d in days); active=sum(1 for d in days if int(d.get('count',0))>0)
legend=''.join(f'<rect x="{720+i*18}" y="184" width="12" height="12" rx="2" fill="{c}"/>' for i,c in enumerate(colors))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>.bg{{fill:{t['background']}}}.frame{{fill:none;stroke:{t['muted']};opacity:.55}}.title{{font:600 12px monospace;fill:{t['accent']}}}.meta{{font:10px monospace;fill:{t['muted']}}}.day{{opacity:0;animation:rise .45s ease-out forwards}}@keyframes rise{{0%{{opacity:0;transform:scale(.35)}}70%{{opacity:1;transform:scale(1.08)}}100%{{opacity:1;transform:scale(1)}}}}@media(prefers-reduced-motion:reduce){{.day{{animation:none;opacity:1}}}}</style><rect class="bg" width="100%" height="100%" rx="8"/><rect class="frame" x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8"/><text x="32" y="28" class="title">╭─ contribution activity</text><text x="32" y="43" class="meta">{html.escape(p.get('username',''))} · {total} contributions · {active} active days</text><g>{''.join(rs)}</g><text x="32" y="193" class="meta">less</text>{legend}<text x="805" y="193" class="meta">more</text></svg>'''
OUT.parent.mkdir(exist_ok=True); OUT.write_text(svg); print(f'Wrote {OUT}')
