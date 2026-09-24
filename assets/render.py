#!/usr/bin/env python3
"""Render the vault-pass profile art as GitHub-safe PNGs."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent
INK = (7, 6, 5)
GOLD = (201, 161, 90)
GOLD_LT = (246, 226, 176)
GOLD_DK = (140, 106, 47)
CREAM = (232, 213, 163)
PAPER = (243, 230, 208)

NEWYORK = "/System/Library/Fonts/NewYork.ttf"
NEWYORK_I = "/System/Library/Fonts/NewYorkItalic.ttf"
PALATINO = "/System/Library/Fonts/Palatino.ttc"


def font(size: int, italic: bool = False) -> ImageFont.FreeTypeFont:
    path = NEWYORK_I if italic else NEWYORK
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(PALATINO, size)


def grain(img: Image.Image, amount: int = 16) -> Image.Image:
    rng = random.Random(7)
    noise = Image.new("L", img.size, 0)
    px = noise.load()
    w, h = img.size
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            v = rng.randint(0, amount)
            px[x, y] = v
    noise = noise.filter(ImageFilter.GaussianBlur(0.6))
    overlay = Image.new("RGB", img.size, (20, 16, 10))
    return Image.composite(overlay, img, noise.point(lambda p: min(40, p)))


def frame(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], width: int = 2) -> None:
    x0, y0, x1, y1 = box
    draw.rectangle(box, outline=GOLD, width=width)
    t = 22
    draw.line((x0, y0 + t, x0, y0, x0 + t, y0), fill=GOLD_LT, width=3)
    draw.line((x1, y0 + t, x1, y0, x1 - t, y0), fill=GOLD_LT, width=3)
    draw.line((x0, y1 - t, x0, y1, x0 + t, y1), fill=GOLD_LT, width=3)
    draw.line((x1, y1 - t, x1, y1, x1 - t, y1), fill=GOLD_LT, width=3)


def text_spaced(draw, xy, text, fnt, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def vault_dial(base: Image.Image, cx: int, cy: int, r: int) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for rad, w, dash in (
        (r, 2, None),
        (int(r * 0.84), 3, None),
        (int(r * 0.68), 2, 8),
        (int(r * 0.48), 4, None),
    ):
        bbox = (cx - rad, cy - rad, cx + rad, cy + rad)
        if dash:
            # dashed ring via many short arcs
            for i in range(0, 360, 14):
                d.arc(bbox, start=i, end=i + 7, fill=(*GOLD, 200), width=w)
        else:
            d.ellipse(bbox, outline=(*GOLD, 210), width=w)
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x0 = cx + int(math.cos(a) * (r - 8))
        y0 = cy + int(math.sin(a) * (r - 8))
        x1 = cx + int(math.cos(a) * r)
        y1 = cy + int(math.sin(a) * r)
        d.line((x0, y0, x1, y1), fill=(*GOLD_LT, 180), width=2)
    d.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=(26, 20, 12, 255), outline=(*GOLD, 255), width=2)
    d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=(*GOLD_LT, 255))
    base.alpha_composite(overlay)


def hero() -> None:
    w, h = 2400, 920
    img = Image.new("RGB", (w, h), INK)
    # spotlight
    spot = Image.new("RGB", (w, h), INK)
    sd = ImageDraw.Draw(spot)
    sd.ellipse((1400, 80, 2300, 980), fill=(42, 32, 16))
    spot = spot.filter(ImageFilter.GaussianBlur(80))
    img = Image.blend(img, spot, 0.55)
    img = grain(img, 18)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)
    frame(d, (36, 36, w - 36, h - 36), 2)
    d.rectangle((48, 48, w - 48, h - 48), outline=(201, 161, 90, 70), width=1)

    # vertical serial
    v = "N 0 4 0 . 3"
    vy = 200
    for ch in v:
        d.text((70, vy), ch, font=font(16), fill=GOLD)
        vy += 22

    text_spaced(d, (130, 88), "PASS  SE-07     TASHKENT", font(22), GOLD, tracking=4)
    text_spaced(d, (130, 250), "FLUTTER DEVELOPER", font(26), GOLD, tracking=8)
    text_spaced(d, (124, 330), "SAMANDAR", font(92), CREAM, tracking=8)
    text_spaced(d, (126, 448), "ESHPULATOV", font(92), GOLD_LT, tracking=12)
    d.text((130, 568), "Ships products. Not demos.", font=font(28, italic=True), fill=GOLD)

    vault_dial(img, 1960, 400, 240)

    # magnetic stripe
    d.rectangle((48, 740, w - 48, h - 48), fill=(18, 14, 10, 255))
    d.line((48, 740, w - 48, 740), fill=GOLD, width=1)
    text_spaced(d, (130, 772), "HAZINA     EDUFLIX     UZNEXT", font(26), GOLD_LT, tracking=3)
    d.text((130, 828), "play market   ·   eduflix.uz   ·   uznext.uz", font=font(22), fill=GOLD)
    d.text((w - 80, 804), "open to work", font=font(22), fill=GOLD_LT, anchor="rm")
    d.text((w - 80, 838), "tashkent", font=font(20), fill=GOLD, anchor="rm")

    img.convert("RGB").save(OUT / "hero.png", "PNG", optimize=True)


def card(name: str, code: str, kicker: str, line1: str, line2: str, footer: str, filename: str, motif: str) -> None:
    w, h = 1140, 690
    img = Image.new("RGB", (w, h), INK)
    spot = Image.new("RGB", (w, h), INK)
    sd = ImageDraw.Draw(spot)
    sd.ellipse((600, -80, 1300, 500), fill=(40, 30, 16))
    img = Image.blend(img, spot.filter(ImageFilter.GaussianBlur(60)), 0.5)
    img = grain(img, 14).convert("RGBA")
    d = ImageDraw.Draw(img)
    frame(d, (24, 24, w - 24, h - 24), 2)
    text_spaced(d, (64, 64), code, font(22), GOLD, tracking=4)
    d.text((64, 150), name, font=font(72), fill=GOLD_LT)
    d.text((64, 240), kicker, font=font(24), fill=GOLD)
    d.text((64, 360), line1, font=font(28, italic=True), fill=CREAM)
    d.text((64, 410), line2, font=font(28, italic=True), fill=CREAM)
    text_spaced(d, (64, 580), footer, font(22), GOLD, tracking=3)

    if motif == "chip":
        x, y = 900, 80
        d.rounded_rectangle((x, y, x + 132, y + 100), radius=10, outline=GOLD, width=3)
        for i in range(1, 4):
            d.line((x + i * 33, y, x + i * 33, y + 100), fill=GOLD, width=1)
        d.line((x, y + 33, x + 132, y + 33), fill=GOLD, width=1)
        d.line((x, y + 66, x + 132, y + 66), fill=GOLD, width=1)
        cx, cy, r = 966, 430, 70
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD, width=2)
        d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=GOLD_LT)
    elif motif == "grid":
        x, y = 900, 80
        for i in range(2):
            for j in range(2):
                box = (x + i * 64, y + j * 64, x + 52 + i * 64, y + 52 + j * 64)
                if i == 1 and j == 1:
                    d.rectangle(box, fill=(201, 161, 90, 70), outline=GOLD, width=2)
                else:
                    d.rectangle(box, outline=GOLD, width=2)
    else:
        cx, cy = 966, 150
        d.polygon([(cx, cy - 70), (cx + 70, cy), (cx, cy + 70), (cx - 70, cy)], outline=GOLD)
        d.polygon([(cx, cy - 36), (cx + 36, cy), (cx, cy + 36), (cx - 36, cy)], fill=(201, 161, 90, 50), outline=GOLD)

    img.convert("RGB").save(OUT / filename, "PNG", optimize=True)


def plate() -> None:
    w, h = 2400, 440
    img = Image.new("RGB", (w, h), INK)
    img = grain(img, 12).convert("RGBA")
    d = ImageDraw.Draw(img)
    frame(d, (36, 36, w - 36, h - 36), 2)
    text_spaced(d, (80, 70), "THE BENCH", font(22), GOLD, tracking=6)
    cols = [
        (80, "MOBILE", "Flutter  ·  Dart", "Riverpod · Provider · BLoC · GoRouter"),
        (860, "SHIP", "REST  ·  Firebase", "Maps · QR · OTP · Push · l10n"),
        (1640, "ALSO", "Python  ·  Vite", "UZ · RU · EN · Tashkent office"),
    ]
    for x, a, b, c in cols:
        d.text((x, 160), a, font=font(22), fill=GOLD)
        d.text((x, 210), b, font=font(40), fill=GOLD_LT)
        d.text((x, 280), c, font=font(24), fill=CREAM)
    d.line((800, 80, 800, 360), fill=GOLD, width=1)
    d.line((1580, 80, 1580, 360), fill=GOLD, width=1)
    img.convert("RGB").save(OUT / "plate-stack.png", "PNG", optimize=True)


def footer() -> None:
    w, h = 2400, 280
    img = Image.new("RGB", (w, h), INK)
    img = grain(img, 10).convert("RGBA")
    d = ImageDraw.Draw(img)
    frame(d, (36, 36, w - 36, h - 36), 2)
    d.text((w // 2, 88), "OPEN THE PASS", font=font(20), fill=GOLD, anchor="mm")
    d.text((w // 2, 150), "TELEGRAM   ·   LINKEDIN   ·   UPWORK", font=font(34), fill=GOLD_LT, anchor="mm")
    d.text((w // 2, 208), "t.me/thedarik   ·   not a template", font=font(20, italic=True), fill=GOLD_DK, anchor="mm")
    img.convert("RGB").save(OUT / "footer-stamp.png", "PNG", optimize=True)


if __name__ == "__main__":
    hero()
    card(
        "Hazina",
        "01  ·  LIVE",
        "Loyalty  ·  Flutter  ·  Play Market",
        "Phone login. Customer QR.",
        "Bonuses, map, push.",
        "uz.hazina.app",
        "pass-hazina.png",
        "chip",
    )
    card(
        "EduFlix",
        "02  ·  LIVE",
        "CRM  ·  Web + mobile",
        "Education-center product.",
        "Students, courses, admin.",
        "eduflix.uz",
        "pass-eduflix.png",
        "grid",
    )
    card(
        "UzNext",
        "03  ·  STUDIO",
        "Web  ·  products  ·  studio",
        "Sites and product work",
        "under one mark.",
        "uznext.uz",
        "pass-uznext.png",
        "diamond",
    )
    plate()
    footer()
    print("ok", list(OUT.glob("*.png")))
