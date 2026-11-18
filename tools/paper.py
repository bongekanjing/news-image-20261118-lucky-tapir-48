#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page.

Everything is drawn from flat fills, hairlines and type: no photographs, no
gradients, nothing that can smear at the final size. The page is composed at
3x and reduced once with Lanczos, which is what gives the small type its
clean edges at the 1024 x 1024 the gate accepts.

Geometry is fixed: the page is a broadsheet grid, four columns wide, with a
lead band, two card rows, and a foot carrying the wire briefs and the day's
figures. Each block measures its own text and reports an overflow instead of
running over its neighbour.
"""

import os
from PIL import Image, ImageDraw, ImageFont

S = 3
W = H = 1024
CW = CH = W * S

PAPER = (246, 242, 231)
INK = (22, 19, 16)
INK_MID = (62, 54, 45)
INK_SOFT = (104, 94, 80)
RULE = (30, 26, 22)
HAIR = (158, 148, 128)
RED = (162, 34, 28)
WHITE = (255, 255, 255)

REGION = {
    "EUROPE": (44, 92, 164),
    "MIDDLE EAST": (104, 122, 46),
    "ASIA": (172, 120, 24),
    "AFRICA": (190, 84, 40),
    "AMERICAS": (104, 60, 140),
    "OCEANIA": (28, 120, 112),
    "WORLD": (34, 48, 78),
}

FD = "/usr/share/fonts/truetype/liberation"
SERIF_B = FD + "/LiberationSerif-Bold.ttf"
SERIF_R = FD + "/LiberationSerif-Regular.ttf"
SERIF_I = FD + "/LiberationSerif-Italic.ttf"
SANS_B = FD + "/LiberationSans-Bold.ttf"
SANS_R = FD + "/LiberationSans-Regular.ttf"

_fc = {}
PATHS = {"sb": SERIF_B, "sr": SERIF_R, "si": SERIF_I, "nb": SANS_B, "nr": SANS_R}


def f(key, pt):
    px = max(1, int(round(pt * S)))
    k = (key, px)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(PATHS[key], px)
    return _fc[k]


def tlen(d, s, ft):
    return d.textlength(s, font=ft)


def wrap(d, s, ft, maxw):
    out, cur = [], ""
    for w in s.split():
        t = w if not cur else cur + " " + w
        if tlen(d, t, ft) <= maxw or not cur:
            cur = t
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def fit(d, s, ft, maxw, maxlines):
    lines = wrap(d, s, ft, maxw)
    if len(lines) <= maxlines:
        return lines, False
    keep = lines[:maxlines]
    last = keep[-1]
    while last and tlen(d, last + "\u2026", ft) > maxw:
        last = last[:-1]
    keep[-1] = last.rstrip(" ,;:-\u2014") + "\u2026"
    return keep, True


def caps_width(d, s, ft, sp):
    return sum(tlen(d, c, ft) for c in s) + sp * max(0, len(s) - 1)


def caps(d, x, y, s, ft, fill, sp):
    for c in s:
        d.text((x, y), c, font=ft, fill=fill)
        x += tlen(d, c, ft) + sp
    return x


def line(d, x0, y0, x1, y1, fill=RULE, w=1):
    d.line([(x0, y0), (x1, y1)], fill=fill, width=w)


def hline(d, x0, x1, y, fill=HAIR, w=1):
    line(d, x0, y, x1, y, fill, w)


def vline(d, x, y0, y1, fill=HAIR, w=1):
    line(d, x, y0, x, y1, fill, w)
