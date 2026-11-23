#!/usr/bin/env python3
"""Build the GTA 6 meme for the make.fun bounty gta6-meme-x-01.

Wanted-star parody, Vice City vibe: the real make.fun ghost logo,
front and centre under five gold wanted stars, on a sunset gradient.
Output: meme.png, 1024x1024. Deterministic (fixed seed, no network
at build time beyond the already-downloaded ghost-mark.png).
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
GHOST_SRC = "ghost-mark.png"
OUT = "meme.png"

# Sunset gradient stops: (position 0..1, RGB)
STOPS = [
    (0.00, (42, 10, 74)),     # deep purple night sky
    (0.35, (179, 18, 127)),   # magenta
    (0.65, (255, 107, 53)),   # orange
    (1.00, (255, 201, 60)),   # golden horizon
]

GOLD = (255, 215, 0)
GOLD_DARK = (218, 165, 32)
WHITE = (255, 255, 255)
BLACK = (20, 8, 28)
SUN_CREAM = (255, 243, 176)


def gradient_color(y):
    """Colour of the vertical sunset gradient at row y."""
    t = y / (H - 1)
    for i in range(len(STOPS) - 1):
        t0, c0 = STOPS[i]
        t1, c1 = STOPS[i + 1]
        if t0 <= t <= t1:
            f = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
            return tuple(int(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
    return STOPS[-1][1]


def star_points(cx, cy, r_outer, r_inner, points=5, rot=-90):
    """Polygon points for a star centred at (cx, cy)."""
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(rot + i * 180.0 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_star(draw, cx, cy, r_outer, fill=GOLD, outline=BLACK, width=5):
    r_inner = r_outer * 0.42
    draw.polygon(star_points(cx, cy, r_outer, r_inner),
                 fill=fill, outline=outline, width=width)


def draw_spaced(draw, cx, y, text, font, fill, stroke_fill, stroke_width,
                spacing=10):
    """Draw text centred on cx with extra space between letters."""
    widths = []
    total = 0
    for ch in text:
        w = draw.textlength(ch, font=font)
        widths.append(w)
        total += w
    total += spacing * (len(text) - 1)
    x = cx - total / 2.0
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill,
                  stroke_width=stroke_width, stroke_fill=stroke_fill)
        x += w + spacing
    return total


def main():
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        c = gradient_color(y)
        for x in range(W):
            px[x, y] = c
    draw = ImageDraw.Draw(img, "RGBA")

    # Faint stars in the upper sky.
    rng = random.Random(20261123)
    for _ in range(70):
        x = rng.randint(10, W - 10)
        y = rng.randint(10, 300)
        r = rng.choice([1, 1, 2, 2, 3])
        a = rng.randint(90, 200)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))

    # Giant sunset sun behind the ghost, with slats across its lower half.
    sun_cx, sun_cy, sun_r = W // 2, 545, 265
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r,
                  sun_cx + sun_r, sun_cy + sun_r], fill=SUN_CREAM)
    bar_y = sun_cy + 10
    bar_h = 7
    gap = 13
    while bar_y < sun_cy + sun_r:
        half = int(math.sqrt(max(0, sun_r * sun_r - (bar_y - sun_cy) ** 2)))
        c = gradient_color(bar_y)
        draw.rectangle([sun_cx - half, bar_y, sun_cx + half, bar_y + bar_h],
                       fill=c)
        bar_y += bar_h + gap
        bar_h += 3
        gap += 4

    # "WANTED" big at the top, GTA poster style.
    font_wanted = ImageFont.truetype(BOLD, 128)
    draw_spaced(draw, W // 2, 28, "WANTED", font_wanted,
                fill=WHITE, stroke_fill=BLACK, stroke_width=7, spacing=14)

    # Five gold wanted stars in a row above the ghost.
    star_y = 215
    star_r = 44
    gap_x = 108
    start_x = W // 2 - 2 * gap_x
    for i in range(5):
        draw_star(draw, start_x + i * gap_x, star_y, star_r)

    # The real make.fun ghost, front and centre.
    ghost = Image.open(GHOST_SRC).convert("RGBA")
    ghost = ghost.resize((420, 420), Image.LANCZOS)
    img.paste(ghost, ((W - 420) // 2, 282), ghost)
    draw = ImageDraw.Draw(img, "RGBA")

    # "make.fun" large and clearly readable at the bottom.
    font_brand = ImageFont.truetype(BOLD, 118)
    draw_spaced(draw, W // 2, 812, "make.fun", font_brand,
                fill=WHITE, stroke_fill=BLACK, stroke_width=7, spacing=4)

    img.save(OUT, "PNG")
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
