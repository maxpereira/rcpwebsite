"""Make web-sized copies of an event photo.

Writes WebP files at 640/1024/1600/2400px wide (only sizes up to the original's
width, plus the original width itself when it's under 2400) and one 1024px JPEG
fallback. EXIF data, including GPS location from phones, is dropped: Pillow only
writes EXIF when asked to.

Needs: pip install pillow pillow-heif   (pillow-heif reads iPhone .heic files)

Usage:
  python3 tools/make_photos.py SRC OUT_DIR NAME [CROP]

  SRC      original photo (.heic, .jpg, .png)
  OUT_DIR  e.g. images/events/2026-11
  NAME     kebab-case description, e.g. bike-repair -> bike-repair-1024.webp ...
  CROP     optional x0,y0,x1,y1 as fractions of the image, e.g. 0,0.1,1,0.9
"""
import os
import sys

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()

src, out_dir, name = sys.argv[1:4]
crop = sys.argv[4] if len(sys.argv) > 4 else None

im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
if crop:
    x0, y0, x1, y1 = map(float, crop.split(','))
    W, H = im.size
    im = im.crop((round(x0 * W), round(y0 * H), round(x1 * W), round(y1 * H)))

os.makedirs(out_dir, exist_ok=True)
widths = [w for w in (640, 1024, 1600, 2400) if w <= im.width]
if im.width < 2400 and im.width not in widths:
    widths.append(im.width)  # keep the full resolution of smaller originals

for w in widths:
    r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    r.save(f'{out_dir}/{name}-{w}.webp', quality=78, method=6)
    if w == 1024 or (w == widths[-1] and 1024 not in widths):
        r.save(f'{out_dir}/{name}-{w}.jpg', quality=80, optimize=True, progressive=True)
    print(f'{name}-{w}', r.size, os.path.getsize(f'{out_dir}/{name}-{w}.webp') // 1024, 'KB')
