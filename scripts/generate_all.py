import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for name in ['make_banner.py','make_info_card.py','render_heatmap_svg.py']:
    subprocess.run([sys.executable,str(R/'scripts'/name)],check=True)
if (R/'assets/source-prepped.png').exists(): subprocess.run([sys.executable,str(R/'scripts/make_ascii_svg.py')],check=True)
