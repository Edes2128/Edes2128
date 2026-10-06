from pathlib import Path
import json, html

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / "profile.json").read_text())
OUT = ROOT / "generated/info-card.svg"
t = C["theme"]
W, H = 960, 132

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

about = "".join(
    f'<text x="36" y="{78 + i * 26}" class="about">{html.escape(line)}</text>'
    for i, line in enumerate(wrap(C.get("about", ""), 110))
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .bg {{ fill: {t["panel"]}; }}
  .frame {{ fill: none; stroke: #163056; }}
  .kicker {{ font: 600 11px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; letter-spacing: 1.8px; fill: {t["accent"]}; }}
  .about {{ font: 18px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: {t["text"]}; }}
</style>
<rect class="bg" width="100%" height="100%" rx="16"/>
<rect class="frame" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16"/>
<rect x="0" y="0" width="4" height="{H}" fill="{t["accent"]}"/>
<text x="36" y="42" class="kicker">NOW</text>
{about}
</svg>
'''
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(svg)
print(f"Wrote {OUT}")
