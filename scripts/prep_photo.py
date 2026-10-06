from pathlib import Path
import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
if len(sys.argv) != 3:
    raise SystemExit('Usage: python scripts/prep_photo.py INPUT OUTPUT')
src,dst=map(Path,sys.argv[1:])
img=Image.open(src).convert('L'); img.thumbnail((1000,1000),Image.Resampling.LANCZOS)
img=ImageOps.autocontrast(img,cutoff=1); img=ImageEnhance.Contrast(img).enhance(1.35); img=ImageEnhance.Sharpness(img).enhance(1.2); img=img.filter(ImageFilter.GaussianBlur(.15))
dst.parent.mkdir(parents=True,exist_ok=True); img.save(dst); print(f'Wrote {dst}')
