from pathlib import Path
import json, html

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / "profile.json").read_text())
OUT = ROOT / "generated/info-card.svg"
t = C["theme"]
W, H = 960, 248

def wrap(text, limit):
    lines, line = [], ""
    for word in text.split():
        trial = word if not line else f"{line} {word}"
        if len(trial) > limit and line:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines

def chips(items, x, y, max_w):
    nodes = []
    cx, cy = x, y
    for item in items:
        width = 22 + len(item) * 8.2
        if cx + width > x + max_w:
            cx = x
            cy += 34
        nodes.append(
            f'<rect x="{cx:.1f}" y="{cy}" width="{width:.1f}" height="26" rx="13" fill="#0c1830" stroke="#1d4ed8"/>'
            f'<text x="{cx + 12:.1f}" y="{cy + 17}" class="chip">{html.escape(item)}</text>'
        )
        cx += width + 8
    return "".join(nodes), cy

about = "".join(
    f'<text x="36" y="{68 + i * 22}" class="about">{html.escape(line)}</text>'
    for i, line in enumerate(wrap(C.get("about", ""), 62))
)
stack, _ = chips(C["stack"], 36, 132, 520)
projects = []
for i, project in enumerate(C["projects"][:3]):
    y = 78 + i * 48
    projects.append(
        f'<text x="620" y="{y}" class="project">{html.escape(project["name"])}</text>'
        f'<text x="620" y="{y + 18}" class="desc">{html.escape(project["description"])}</text>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .bg {{ fill: {t["panel"]}; }}
  .frame {{ fill: none; stroke: #163056; }}
  .kicker {{ font: 600 11px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; letter-spacing: 1.8px; fill: {t["accent"]}; }}
  .about {{ font: 16px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: {t["text"]}; }}
  .chip {{ font: 12px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: {t["bright"]}; }}
  .project {{ font: 600 15px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: {t["text"]}; }}
  .desc {{ font: 12px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: {t["muted"]}; }}
  .bar {{ transform-origin: 596px 36px; animation: grow 1s ease forwards; }}
  @keyframes grow {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
  @media (prefers-reduced-motion: reduce) {{ .bar {{ animation: none; }} }}
</style>
<rect class="bg" width="100%" height="100%" rx="16"/>
<rect class="frame" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16"/>
<rect x="0" y="0" width="4" height="{H}" fill="{t["accent"]}"/>
<text x="36" y="40" class="kicker">NOW</text>
{about}
<text x="36" y="122" class="kicker">STACK</text>
{stack}
<line class="bar" x1="596" y1="36" x2="596" y2="212" stroke="#163056"/>
<text x="620" y="40" class="kicker">SELECTED WORK</text>
{''.join(projects)}
</svg>
'''
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(svg)
print(f"Wrote {OUT}")
