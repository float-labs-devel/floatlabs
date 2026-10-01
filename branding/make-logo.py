#!/usr/bin/env python3
"""Generate the Float Labs logo and favicon.

Same shape language as the floatblue mark (blue disc, white stylised wave) but
three waves instead of two: one per image, Floatblue, Kifloat and CoreFloat.

Each wave is an annular sector whose stroke tapers to a point, so the polygon is
simple and never self-intersects.
"""
import math
import os

from PIL import Image, ImageDraw

OUT = os.path.dirname(os.path.abspath(__file__))

BG_TOP = (60, 140, 255)
BG_BOTTOM = (14, 48, 122)
WHITE = (255, 255, 255)


def disc(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    grad = Image.new("RGB", (1, size))
    px = grad.load()
    for y in range(size):
        t = y / (size - 1)
        px[0, y] = tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM))
    grad = grad.resize((size, size))

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    img.paste(grad, (0, 0), mask)
    return img


def wave(draw, cx, cy, r, thick, a0, a1):
    """One tapering wave crest: an arc whose stroke thins to nothing at both ends."""
    steps = 120
    outer, inner = [], []
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(a0 + (a1 - a0) * t)
        # fat in the middle of the crest, thin at the tips
        w = thick * (math.sin(math.pi * t) ** 0.85)
        outer.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        inner.append((cx + (r - w) * math.cos(ang), cy + (r - w) * math.sin(ang)))
    draw.polygon(outer + inner[::-1], fill=WHITE)


def build(size, path):
    img = disc(size)
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # three crests, smallest at the top so the stack reads as rising
    wave(d, size * 0.50, size * 0.78, size * 0.44, size * 0.125, 202, 338)
    wave(d, size * 0.50, size * 0.52, size * 0.44, size * 0.115, 202, 338)
    wave(d, size * 0.50, size * 0.28, size * 0.44, size * 0.105, 202, 338)

    mask = img.getchannel("A")
    img.paste(layer, (0, 0), Image.composite(layer.getchannel("A"), Image.new("L", (size, size), 0), mask))
    img.save(path)
    print(path, img.size)


build(512, os.path.join(OUT, "floatlabs-logo.png"))
build(192, os.path.join(OUT, "floatos-logo.png"))
build(64, os.path.join(OUT, "favicon.png"))