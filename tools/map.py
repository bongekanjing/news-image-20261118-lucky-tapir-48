#!/usr/bin/env python3
"""A schematic locator panel, drawn from flat polygons and hairlines.

This is a diagram, not a picture: the Gulf is a flat tint, the coasts are
single-weight lines, the three places named in the lead are dots with labels.
Nothing here is photographic, so nothing can smear at 1024 px.

Coordinates are geographic (lon, lat) and projected linearly into the panel,
which is all a locator needs. The panel says so.
"""

from PIL import ImageDraw

from paper import (S, INK, INK_MID, INK_SOFT, RULE, HAIR, RED, WHITE, PAPER,
                   f, tlen, caps, caps_width, wrap, hline, vline)

LON0, LON1 = 46.6, 57.4
LAT0, LAT1 = 23.6, 30.4

WATER = (214, 222, 218)
LAND = (239, 234, 221)

# The Iranian shore, then round Musandam and back along Arabia.
GULF = [
    (48.7, 30.05), (49.4, 29.75), (50.1, 29.35), (50.85, 28.95), (51.4, 28.55),
    (52.2, 28.15), (53.0, 27.75), (53.9, 27.35), (54.7, 27.0), (55.4, 26.75),
    (56.0, 26.85), (56.45, 27.15), (56.7, 27.0), (56.6, 26.55), (56.35, 26.0),
    (56.05, 25.65), (55.35, 25.25), (54.5, 24.75), (53.6, 24.35), (52.6, 24.3),
    (51.85, 24.5), (51.35, 25.15), (51.15, 25.9), (50.85, 26.15), (50.4, 26.3),
    (49.9, 26.9), (49.5, 27.5), (49.05, 28.15), (48.55, 28.75), (48.15, 29.3),
    (47.95, 29.75), (48.05, 30.15), (48.35, 30.3),
]

QATAR = [
    (51.62, 24.55), (51.4, 25.2), (51.22, 25.85), (50.98, 26.15), (50.78, 25.95),
    (50.82, 25.4), (51.02, 24.95), (51.3, 24.6),
]

PLACES = [
    ("QESHM", 55.92, 26.90, "strike", "US strike, Tue"),
    ("SHEIKH ISA", 50.58, 26.05, "base", "Bahrain"),
    ("ALI AL SALEM", 47.53, 29.35, "base", "Kuwait"),
]


def draw(d, x0, y0, x1, y1, caption="LOCATOR \u00b7 SCHEMATIC \u00b7 NOT TO SCALE"):
    w, h = x1 - x0, y1 - y0

    def P(lon, lat):
        return (x0 + (lon - LON0) / (LON1 - LON0) * w,
                y0 + (LAT1 - lat) / (LAT1 - LAT0) * h)

    d.rectangle([x0, y0, x1, y1], fill=LAND, outline=HAIR, width=1 * S)
    d.polygon([P(a, b) for a, b in GULF], fill=WATER, outline=HAIR)
    d.polygon([P(a, b) for a, b in QATAR], fill=LAND, outline=HAIR)

    # The two capitals of the exchange, joined by the salvo's path.
    q = P(55.92, 26.90)
    for lon, lat, lab in [(47.53, 29.35, ""), (50.58, 26.05, "")]:
        t = P(lon, lat)
        d.line([q, t], fill=RED, width=1 * S)
        # a short tick at the midpoint, so the line reads as a bearing not a border
        mx, my = (q[0] + t[0]) / 2, (q[1] + t[1]) / 2
        d.ellipse([mx - 1.6 * S, my - 1.6 * S, mx + 1.6 * S, my + 1.6 * S], fill=RED)

    for name, lon, lat, kind, sub in PLACES:
        px, py = P(lon, lat)
        r = 3.0 * S
        if kind == "strike":
            d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=PAPER, width=1 * S)
            tx, ty = px - r * 1.4, py - 15 * S
        else:
            d.ellipse([px - r, py - r, px + r, py + r], fill=INK, outline=PAPER, width=1 * S)
            tx, ty = px - r * 1.4, py + 7 * S
        ft = f("nb", 6.4)
        lab = name
        lw = caps_width(d, lab, ft, 0.55 * S)
        tx = min(max(tx, x0 + 3 * S), x1 - lw - 3 * S)
        caps(d, tx, ty, lab, ft, INK if kind == "base" else RED, 0.55 * S)
        st = f("si", 6.4)
        caps(d, tx, ty + int(6.4 * S * 1.5), sub.upper(), f("nb", 5.2), INK_SOFT, 0.5 * S)

    # Panel furniture.
    ft = f("nb", 5.4)
    caps(d, x0 + 5 * S, y0 + 4 * S, caption, ft, INK_SOFT, 0.6 * S)
    caps(d, x0 + 5 * S, y1 - int(6.0 * S * 1.8), "GULF \u00b7 18 NOV 2026", ft, INK_SOFT, 0.6 * S)
    return y1
