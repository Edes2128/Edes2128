from pathlib import Path
import json, os, re
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / "profile.json").read_text())
USER = os.getenv("GITHUB_USERNAME") or C["github_username"]
OUT = ROOT / "data/contributions.json"

if not USER or USER == "YOUR_GITHUB_USERNAME":
    raise SystemExit("Set github_username in profile.json or GITHUB_USERNAME.")

r = requests.get(
    f"https://github.com/users/{USER}/contributions",
    timeout=30,
    headers={"User-Agent": "Mozilla/5.0 (compatible; animated-github-profile/1.0)"},
)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

tips = {}
for tip in soup.select("tool-tip"):
    target = tip.get("for")
    if target:
        tips[target] = tip.get_text(" ", strip=True)

table = soup.select_one("table.ContributionCalendar-grid")
rows = table.select("tbody tr") if table else []
days = []
for weekday, tr in enumerate(rows):
    for week, cell in enumerate(tr.select("td.ContributionCalendar-day")):
        date = cell.get("data-date")
        if not date:
            continue
        text = tips.get(cell.get("id"), "") or cell.get("aria-label", "")
        if re.search(r"no contribution", text, re.I):
            count = 0
        else:
            match = re.search(r"([\d,]+)\s+contribution", text, re.I)
            count = int(match.group(1).replace(",", "")) if match else int(cell.get("data-count") or 0)
        level = int(cell.get("data-level") or 0)
        if count <= 0:
            count = 0
            level = 0
        days.append({"date": date, "count": count, "level": max(0, min(4, level)), "week": week, "weekday": weekday})

days.sort(key=lambda d: (d["week"], d["weekday"]))
previous = json.loads(OUT.read_text()) if OUT.exists() else {}
if previous.get("username") == USER and previous.get("days") == days:
    print(f"Contribution data unchanged for {USER}; left {OUT.name} as-is")
    raise SystemExit(0)
payload = {
    "username": USER,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "days": days,
}
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(payload, indent=2) + "\n")
total = sum(d["count"] for d in days)
print(f"Fetched {len(days)} contribution days for {USER} ({total} contributions)")
