#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Georgia.ttf"
# fallback
if not Path(BOLD).exists():
    BOLD = REG = "/System/Library/Fonts/NewYork.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# Wide but TALL so after GitHub shrinks it, body copy stays readable.
w, h = 1600, 720
img = Image.new("RGB", (w, h), (0, 0, 0))
d = ImageDraw.Draw(img)

# thick frame — visible at small size
d.rectangle((16, 16, w - 16, h - 16), outline=(255, 255, 255), width=8)
d.rectangle((28, 28, w - 28, h - 28), outline=(255, 255, 255), width=2)

white = (255, 255, 255)
name = font(BOLD, 86)
line2 = font(REG, 42)
line3 = font(BOLD, 40)
line4 = font(REG, 36)

# left-aligned block with generous size
x = 80
d.text((x, 90), "SAMANDAR ESHPULATOV", font=name, fill=white)
d.text((x, 210), "Flutter developer  |  Tashkent", font=line2, fill=white)
d.line((x, 280, 980, 280), fill=white, width=4)
d.text((x, 320), "Hazina   |   EduFlix   |   UzNext", font=line3, fill=white)
d.text((x, 400), "Available for freelance and full-time", font=line4, fill=white)
d.text((x, 520), "Play Market  ·  eduflix.uz  ·  uznext.uz", font=line4, fill=white)

img.save(OUT / "hero.png", "PNG", optimize=True)
print("hero", img.size, OUT / "hero.png")
