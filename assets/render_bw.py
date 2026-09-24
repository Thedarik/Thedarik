#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
NY = "/System/Library/Fonts/NewYork.ttf"
NYI = "/System/Library/Fonts/NewYorkItalic.ttf"


def f(size, italic=False):
    return ImageFont.truetype(NYI if italic else NY, size)


w, h = 2400, 420
img = Image.new("RGB", (w, h), (0, 0, 0))
d = ImageDraw.Draw(img)
d.rectangle((24, 24, w - 24, h - 24), outline=(255, 255, 255), width=2)
d.text((80, 70), "SAMANDAR ESHPULATOV", font=f(64), fill=(255, 255, 255))
d.text((80, 170), "Flutter developer  ·  Tashkent", font=f(32, True), fill=(220, 220, 220))
d.text((80, 250), "Hazina   ·   EduFlix   ·   UzNext", font=f(28), fill=(255, 255, 255))
d.text((80, 320), "Available for freelance and full-time", font=f(24), fill=(180, 180, 180))
d.line((80, 300, 900, 300), fill=(255, 255, 255), width=1)
img.save(OUT / "hero.png", "PNG", optimize=True)
print("hero", OUT / "hero.png")
