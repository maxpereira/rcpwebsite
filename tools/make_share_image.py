"""Make the image link previews show when a page is shared.

Crops a photo to 1200x630, the shape Facebook, iMessage, LinkedIn and Slack use,
and saves it as a JPEG. SRC can be the original or the largest WebP that
make_photos.py wrote. EXIF data is dropped, as in make_photos.py.

Some apps show only a square from the middle of the image, so pick a photo whose
subject sits near the center.

Needs: pip install pillow pillow-heif   (pillow-heif reads iPhone .heic files)

Usage:
  python3 tools/make_share_image.py SRC OUT_DIR NAME [FOCUS]

  SRC      e.g. images/events/2026-11/bike-repair-2400.webp
  OUT_DIR  e.g. images/events/2026-11
  NAME     same name as the web sizes: bike-repair -> bike-repair-share.jpg
  FOCUS    optional, which part of the height to keep: 0 = top, 0.5 = middle
           (default), 1 = bottom. Lower it if heads get cut off.
"""
import os
import sys

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()

src, out_dir, name = sys.argv[1:4]
focus = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5

im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
im = ImageOps.fit(im, (1200, 630), Image.LANCZOS, centering=(0.5, focus))

os.makedirs(out_dir, exist_ok=True)
out = f'{out_dir}/{name}-share.jpg'
im.save(out, quality=82, optimize=True, progressive=True)
print(out, im.size, os.path.getsize(out) // 1024, 'KB')
