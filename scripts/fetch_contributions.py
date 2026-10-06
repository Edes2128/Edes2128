from pathlib import Path
import json,os,re
from datetime import datetime,timezone
import requests
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; C=json.loads((ROOT/'profile.json').read_text()); USER=os.getenv('GITHUB_USERNAME') or C['github_username']; OUT=ROOT/'data/contributions.json'
if not USER or USER=='YOUR_GITHUB_USERNAME': raise SystemExit('Set github_username in profile.json or GITHUB_USERNAME.')
r=requests.get(f'https://github.com/users/{USER}/contributions',timeout=30,headers={'User-Agent':'animated-github-profile/1.0'}); r.raise_for_status(); soup=BeautifulSoup(r.text,'html.parser'); cells=soup.select('td.ContributionCalendar-day') or soup.select('[data-date][data-level]'); days=[]
for c in cells:
    date=c.get('data-date'); level=int(c.get('data-level') or 0); aria=c.get('aria-label',''); m=re.search(r'([\d,]+)\s+contribution',aria); count=int(m.group(1).replace(',','')) if m else int(c.get('data-count') or 0)
    if date: days.append({'date':date,'count':count,'level':level})
p={'username':USER,'generated_at':datetime.now(timezone.utc).isoformat(),'days':days[-371:]}; OUT.parent.mkdir(exist_ok=True); OUT.write_text(json.dumps(p,indent=2)); print(f'Fetched {len(days)} contribution days for {USER}')
