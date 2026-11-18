#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page.

Drawn entirely from geometric primitives so nothing can smear or garble:
flat fills, hairlines, and vector-ish spot graphics in a fixed palette.
The page is composed at 3x and downsampled once, which gives clean
antialiased type at the final 1024 x 1024 the gate accepts.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

S = 3                      # supersample factor
W = 1024                   # final width
H = 1024                   # final height
CW, CH = W * S, H * S
MARGIN = 18 * S

PAPER = (247, 243, 232)
PAPER_D = (238, 232, 216)
INK = (20, 17, 14)
INK_SOFT = (74, 66, 56)
RULE = (32, 28, 24)
RED = (166, 38, 30)
WHITE = (255, 255, 255)

REGION = {
    "EUROPE": (45, 95, 168),
    "MIDDLE EAST": (107, 125, 47),
    "ASIA": (176, 124, 26),
    "AFRICA": (192, 86, 42),
    "AMERICAS": (106, 63, 143),
    "OCEANIA": (31, 122, 114),
    "WORLD": (34, 49, 79),
}

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_B = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SERIF_R = os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
SANS_R = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def f(pt, kind="sans_b"):
    """A font at pt final-scale pixels (scaled to the supersampled canvas)."""
    path = {"serif_b": SERIF_B, "serif": SERIF_R, "sans_b": SANS_B, "sans": SANS_R}[kind]
    return font(path, max(1, int(round(pt * S))))


def tw(draw, text, ft):
    return draw.textlength(text, font=ft)


def wrap(draw, text, ft, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if tw(draw, trial, ft) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, ft, max_w, max_lines):
    """Wrap, and if it overruns the line budget, drop the tail with an ellipsis."""
    lines = wrap(draw, text, ft, max_w)
    if len(lines) <= max_lines:
        return lines
    kept = lines[:max_lines]
    last = kept[-1]
    while last and tw(draw, last + "\u2026", ft) > max_w:
        last = last[:-1]
    kept[-1] = last.rstrip(" ,;:") + "\u2026"
    return kept


def caps(draw, xy, text, ft, fill, spacing=1.0 * S):
    """Letter-spaced capitals, the page's navigational voice."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=ft, fill=fill)
        x += tw(draw, ch, ft) + spacing
    return x


def caps_width(draw, text, ft, spacing=1.0 * S):
    return sum(tw(draw, ch, ft) for ch in text) + spacing * max(0, len(text) - 1)


def rule(draw, x0, y0, x1, y1, fill=RULE, w=None):
    draw.line([(x0, y0), (x1, y1)], fill=fill, width=w or max(1, int(S * 0.8)))


def hair(draw, x0, y0, x1, y1, fill=(150, 141, 122)):
    draw.line([(x0, y0), (x1, y1)], fill=fill, width=max(1, int(S * 0.5)))
