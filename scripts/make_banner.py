from pathlib import Path
import base64, json, html

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / "profile.json").read_text())
OUT = ROOT / "generated/banner.svg"
PHOTO = ROOT / "assets/profile.png"
t = C["theme"]
W, H = 960, 540
name = html.escape(C["name"])
headline = html.escape(C["headline"])
handle = html.escape(C["github_username"])
location = html.escape(C["location"])
experience = html.escape(C["experience"])
company = html.escape(C.get("company", ""))

if not PHOTO.exists():
    raise SystemExit("Missing assets/profile.png")

encoded = base64.b64encode(PHOTO.read_bytes()).decode()

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .handle {{ font: 600 13px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; letter-spacing: 3px; fill: #ffffff; }}
  .name {{ font: 700 46px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: #ffffff; }}
  .role {{ font: 600 18px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: #dbe7ff; }}
  .meta {{ font: 15px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: #d5dbe8; }}
  .rule {{ stroke: #ffffff; stroke-width: 2; stroke-linecap: round; animation: draw 1.2s ease forwards; }}
  @keyframes draw {{ from {{ stroke-dashoffset: 120; }} to {{ stroke-dashoffset: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .rule {{ animation: none; stroke-dashoffset: 0; }}
  }}
</style>
<defs>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <image href="data:image/png;base64,{encoded}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
</g>
<text x="40" y="214" class="handle">{handle}</text>
<line class="rule" x1="40" y1="228" x2="150" y2="228" stroke-dasharray="120" stroke-dashoffset="120"/>
<text x="40" y="278" class="name">{name}</text>
<text x="40" y="312" class="role">{headline}</text>
<text x="920" y="248" text-anchor="end" class="meta">{location}</text>
<text x="920" y="272" text-anchor="end" class="meta">{experience}</text>
<text x="920" y="296" text-anchor="end" class="meta">{company}</text>
</svg>
'''
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(svg)
print(f"Wrote {OUT}")
