from pathlib import Path
import json, html
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / "profile.json").read_text())
payload = json.loads((ROOT / "data/contributions.json").read_text())
OUT = ROOT / "generated/contrib-heatmap.svg"
t = C["theme"]
days = payload.get("days", [])

W, H = 960, 214
cell, gap = 11, 3
left, top = 46, 58
step = cell + gap
colors = ["#10192c", "#1e4f96", "#2f6fe4", "#64b4ff", "#d7ecff"]

def placed(day):
    if "week" in day and "weekday" in day:
        return int(day["week"]), int(day["weekday"])
    return None

positioned = []
for i, day in enumerate(days):
    spot = placed(day)
    if spot is None:
        spot = (i // 7, i % 7)
    positioned.append((*spot, day))

weeks = max((week for week, _, _ in positioned), default=0) + 1
rects = []
for week, weekday, day in positioned:
    count = int(day.get("count", 0))
    level = int(day.get("level", 0)) if count > 0 else 0
    level = max(0, min(4, level))
    x = left + week * step
    y = top + weekday * step
    fill = colors[level]
    delay = week * 0.018
    klass = "day" if level else "empty"
    extra = ""
    if level == 4:
        extra = f'<rect x="{x-1}" y="{y-1}" width="{cell+2}" height="{cell+2}" rx="3" fill="{t["bright"]}" opacity="0.18" class="glow" style="animation-delay:{delay:.3f}s"/>'
    title = f'{html.escape(day.get("date", ""))}: {count} contribution{"s" if count != 1 else ""}'
    stroke = ' stroke="#1c3054" stroke-width="0.6"' if level == 0 else ""
    rects.append(
        extra
        + f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{fill}"{stroke} class="{klass}" style="animation-delay:{delay:.3f}s"><title>{title}</title></rect>'
    )

months = []
seen = set()
by_week = {}
for week, weekday, day in positioned:
    by_week.setdefault(week, []).append(day)
for week in range(weeks):
    dates = sorted(d.get("date", "") for d in by_week.get(week, []) if d.get("date"))
    if not dates:
        continue
    stamp = datetime.strptime(dates[0], "%Y-%m-%d")
    key = (stamp.year, stamp.month)
    if key in seen:
        continue
    # Label the first week that contains the 1st, otherwise the first week of that month.
    if any(datetime.strptime(d, "%Y-%m-%d").day <= 7 for d in dates):
        seen.add(key)
        months.append((week, stamp.strftime("%b")))

day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
labels = "".join(
    f'<text x="8" y="{top + weekday * step + 9}" class="tiny">{name}</text>'
    for weekday, name in day_labels
)
month_nodes = "".join(
    f'<text x="{left + week * step}" y="48" class="tiny">{html.escape(name)}</text>'
    for week, name in months
)

ordered = sorted(
    (datetime.strptime(d["date"], "%Y-%m-%d"), int(d.get("count", 0)))
    for _, _, d in positioned
    if d.get("date")
)
streak = best = 0
prev = None
for stamp, count in ordered:
    if count > 0 and (prev is None or stamp - prev == timedelta(days=1)):
        streak += 1
    elif count > 0:
        streak = 1
    else:
        streak = 0
    best = max(best, streak)
    prev = stamp
current = streak if ordered and ordered[-1][1] > 0 else 0

total = sum(count for _, count in ordered)
active = sum(1 for _, count in ordered if count > 0)
user = html.escape(payload.get("username") or C["github_username"])

legend = "".join(
    f'<rect x="{778 + i * 16}" y="188" width="11" height="11" rx="2.5" fill="{color}"/>'
    for i, color in enumerate(colors)
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .bg {{ fill: {t["background"]}; }}
  .frame {{ fill: none; stroke: #163056; }}
  .label {{ font: 600 11px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; letter-spacing: 1.8px; fill: {t["muted"]}; }}
  .stat {{ font: 700 22px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: {t["text"]}; }}
  .meta {{ font: 12px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: {t["muted"]}; }}
  .accent {{ fill: {t["accent"]}; }}
  .tiny {{ font: 10px ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif; fill: #5d6e8c; }}
  .day {{ opacity: 0; animation: rise .55s ease forwards; }}
  .glow {{ opacity: 0; animation: rise .55s ease forwards, pulse 2.8s ease-in-out infinite; }}
  .scan {{ fill: url(#scan); animation: sweep 7s linear infinite; }}
  @keyframes rise {{ to {{ opacity: 1; }} }}
  @keyframes pulse {{ 0%, 100% {{ opacity: .12; }} 50% {{ opacity: .38; }} }}
  @keyframes sweep {{ from {{ transform: translateX(-120px); }} to {{ transform: translateX({W}px); }} }}
  @media (prefers-reduced-motion: reduce) {{
    .day, .glow {{ animation: none; opacity: 1; }}
    .scan {{ display: none; }}
  }}
</style>
<defs>
  <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#4da3ff" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#4da3ff" stop-opacity="0.16"/>
    <stop offset="1" stop-color="#4da3ff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#4da3ff"/>
    <stop offset="1" stop-color="#4da3ff" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect class="bg" width="100%" height="100%" rx="16"/>
<rect x="0" y="0" width="3" height="{H}" fill="url(#edge)"/>
<rect class="frame" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16"/>
<text x="22" y="28" class="label">CONTRIBUTIONS</text>
<text x="168" y="30" class="stat">{total:,}</text>
<text x="248" y="28" class="meta">{user} · {active} active days · best streak {best} · current {current}</text>
{month_nodes}{labels}
<g>{''.join(rects)}</g>
<rect class="scan" x="0" y="{top - 4}" width="90" height="{7 * step}" rx="8"/>
<text x="748" y="198" class="tiny">less</text>
{legend}
<text x="864" y="198" class="tiny">more</text>
</svg>
'''
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(svg)
print(f"Wrote {OUT} ({total} contributions)")
