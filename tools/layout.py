#!/usr/bin/env python3
"""Layout primitives: the grid, a measured story card, a rule head.

Every block can be measured before it is drawn (`measure_card`), so the
composer can solve heights against the page instead of guessing them. A block
that does not fit its allowance reports a warning rather than overlapping the
one below it.
"""

from PIL import Image, ImageDraw

from paper import (S, CW, CH, PAPER, INK, INK_MID, INK_SOFT, RULE, HAIR,
                   RED, WHITE, REGION, f, tlen, wrap, fit, caps, caps_width,
                   hline, vline)

M = 17 * S
INNER = CW - 2 * M
GUT = 9 * S
COLS = 4
COLW = (INNER - GUT * (COLS - 1)) // COLS

_PROBE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def colx(i):
    return M + i * (COLW + GUT)


def span(n):
    """Width of n columns plus the gutters between them."""
    return COLW * n + GUT * (n - 1)


class Page:
    """An RGB canvas plus the two text habits the page needs everywhere."""

    def __init__(self):
        self.im = Image.new("RGB", (CW, CH), PAPER)
        self.d = ImageDraw.Draw(self.im)
        self.warn = []
        self.scale = {}

    def text(self, x, y, s, key, pt, fill=INK, maxw=None, maxlines=1, lh=1.14):
        ft = f(key, pt)
        lines, over = ([s], False) if maxw is None else fit(self.d, s, ft, maxw, maxlines)
        if over:
            self.warn.append(("clipped", s[:44]))
        step = int(ft.size * lh)
        for ln in lines:
            self.d.text((x, y), ln, font=ft, fill=fill)
            y += step
        return y

    def para(self, x, y, s, key, pt, fill=INK_MID, maxw=COLW, lh=1.30):
        ft = f(key, pt)
        step = int(ft.size * lh)
        for ln in wrap(self.d, s, ft, maxw):
            self.d.text((x, y), ln, font=ft, fill=fill)
            y += step
        return y

    def box(self, x0, y0, x1, y1, fill):
        self.d.rectangle([x0, y0, x1, y1], fill=fill)


def tab(pg, x, y, region, pt=7.2):
    col = REGION[region]
    ft = f("nb", pt)
    tw = caps_width(pg.d, region, ft, 0.7 * S)
    ph = int(pt * S * 1.55)
    pg.box(x, y, x + tw + 5 * S, y + ph, col)
    caps(pg.d, x + 2.5 * S, y + int(pt * S * 0.36), region, ft, WHITE, 0.7 * S)
    return x + tw + 7 * S, ph


def card(pg, x, y, w, story, hsize=14.0, dsize=9.0, tab_pt=7.0, lh=1.06,
         rule_w=None, src_pt=6.6):
    """Draw one story block at (x, y), w wide. Returns the y it ended at."""
    tx, ph = tab(pg, x, y, story["region"], tab_pt)
    caps(pg.d, tx, y + int(tab_pt * S * 0.36), story["desk"], f("nb", tab_pt),
         INK_SOFT, 0.7 * S)
    yy = y + ph + 3 * S
    yy = pg.text(x, yy, story["head"], "sb", hsize, INK, w, 4, lh=lh)
    if story.get("deck"):
        yy = pg.para(x, yy + 3 * S, story["deck"], "sr", dsize, INK_MID, w, 1.28)
    if story.get("src"):
        hline(pg.d, x, x + min(w, (rule_w or 40) * S), yy + 4 * S, HAIR, 1)
        caps(pg.d, x, yy + 6 * S, story["src"].upper(), f("nb", src_pt), INK_SOFT, 0.55 * S)
        yy += 6 * S + int(src_pt * S * 1.7)
    return yy


def card_h(w, story, **kw):
    """The height `card` will occupy, without drawing it."""
    hsize = kw.get("hsize", 14.0)
    dsize = kw.get("dsize", 9.0)
    tab_pt = kw.get("tab_pt", 7.0)
    lh = kw.get("lh", 1.06)
    src_pt = kw.get("src_pt", 6.6)
    h = int(tab_pt * S * 1.55) + 3 * S
    ft = f("sb", hsize)
    h += len(wrap(_PROBE, story["head"], ft, w)) * int(ft.size * lh)
    if story.get("deck"):
        fd = f("sr", dsize)
        h += 3 * S + len(wrap(_PROBE, story["deck"], fd, w)) * int(fd.size * 1.28)
    if story.get("src"):
        h += 4 * S + 6 * S + int(src_pt * S * 1.7)
    return h


def tab_head(pg, x, y, w, story, hsize=29.0, tab_pt=8.4, lh=1.02):
    """A lead-size headline with its tab: no deck, measured by the caller."""
    tx, ph = tab(pg, x, y, story["region"], tab_pt)
    caps(pg.d, tx, y + int(tab_pt * S * 0.36), story["desk"], f("nb", tab_pt),
         INK_SOFT, 0.7 * S)
    yy = y + ph + 4 * S
    yy = pg.text(x, yy, story["head"], "sb", hsize, INK, w, 4, lh=lh)
    return yy


def tab_head_h(w, story, hsize=29.0, tab_pt=8.4, lh=1.02):
    h = int(tab_pt * S * 1.55) + 4 * S
    ft = f("sb", hsize)
    h += len(wrap(_PROBE, story["head"], ft, w)) * int(ft.size * lh)
    return h


def rulehead_h(pt=7.6, tail=5 * S):
    """Height of `rulehead`: its label line, the rule, and the gap under it."""
    return int(pt * S * 1.6) + tail


def rulehead(pg, x, y, w, label, col=RED, pt=7.6, track=1.0 * S):
    caps(pg.d, x, y, label, f("nb", pt), col, track)
    base = y + int(pt * S * 1.6)
    hline(pg.d, x, x + w, base, RULE, 1 * S)
    return base + 5 * S
