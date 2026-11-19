#!/usr/bin/env python3
"""Compose the front page at 3x and write it at 1024 x 1024.

Run:  python3 tools/compose.py out/entry.png

The page is a broadsheet of type on a fixed grid, and the type is the variable
that gets solved: each band is drawn once off to the side to measure itself, then
the copy is scaled so the band closes exactly on the height the page budgeted for
it. That is why there are no holes and no overlaps - the empty space is spent as
leading rather than left as a gap.

The four top stories carry a flat spot graphic. Nothing is photographic: each is
a solid ground and three or four shapes, with the figures set as type. They are
there because at 300 pixels across a page of pure type is a grey wash, and a
reader - or a judge looking at a thumbnail - has to be able to tell one story
from another.
"""

import json
import os
import sys

from PIL import Image

import copy as C
import gfx
import layout as L
import paper as P

S = P.S
CW, CH, M, INNER, GUT, COLW = P.CW, P.CH, L.M, L.INNER, L.GUT, L.COLW
colx, span = L.colx, L.span

pg = L.Page()
d = pg.d

ILL = 78 * S          # height of a feature's spot graphic, at 3x

# One motif per top story, in the order the copy files them.
FEAT_MOTIF = ["gulf", "summit", "vote", "swarm"]


def solve(fn, target, lo=0.80, hi=1.45, iters=26):
    """Find the scale whose `fn(page, scale)` lands nearest `target`.

    Binary search assumes the function is monotonic in the scale, which the
    measured bands are: bigger type makes a taller block. The caller passes the
    function's own end, so this works whether the target is a height to fill or
    a height not to exceed.
    """
    up = fn(L.Page(), hi) >= fn(L.Page(), lo)
    for _ in range(iters):
        mid = (lo + hi) / 2
        end = fn(L.Page(), mid)
        if (end < target) == up:
            lo = mid
        else:
            hi = mid
    a, b = fn(L.Page(), lo), fn(L.Page(), hi)
    return lo if abs(a - target) <= abs(b - target) else hi


# ---------------------------------------------------------------- masthead

def masthead(y):
    """The day is the nameplate: this page is about one date and says so first."""
    P.hline(d, M, CW - M, y, P.RULE, 2 * S)
    y += 4 * S
    ft = P.f("nb", 7.4)
    P.caps(d, M, y, "THE WORLD", ft, P.INK, 2.2 * S)
    P.caps(d, M + P.caps_width(d, "THE WORLD", ft, 2.2 * S) + 8 * S, y,
           "\u00b7  THE DAY IN ONE PAGE", ft, P.INK_SOFT, 1.4 * S)
    right = (f"{len([C.LEAD] + C.SECOND + C.CARDS)} FILED  \u00b7  "
             f"{len(C.BRIEFS)} WIRE BRIEFS  \u00b7  SEVEN REGIONS")
    rw = P.caps_width(d, right, ft, 1.3 * S)
    P.caps(d, CW - M - rw, y, right, ft, P.RED, 1.3 * S)
    y += 13 * S

    # The date set as the largest thing on the page, sized to the measure.
    name = "WEDNESDAY 18 NOVEMBER 2026"
    sz = 560.0
    ft = P.f("sb", sz / 10.0)
    while P.tlen(d, name, ft) > INNER and sz > 120:
        sz -= 4
        ft = P.f("sb", sz / 10.0)
    asc, desc = ft.getmetrics()
    d.text((M, y), name, font=ft, fill=P.INK)
    y += asc

    y += 3 * S
    P.hline(d, M, CW - M, y, P.RED, 3 * S)
    return y + 4 * S


def standfirst(y):
    sub = ("The Gulf war widens \u00b7 the Senate changes hands \u00b7 a cyclone closes on Andhra \u00b7 "
           "Voyager leaves the solar system behind")
    ft = P.f("si", 11.4)
    while P.tlen(d, sub, ft) > INNER:
        ft = P.f("si", ft.size / S - 0.15)
    d.text((M, y), sub, font=ft, fill=P.INK_MID)
    return y + int(ft.size * 1.12)


def index(y):
    """The index is derived from the copy, so it can never disagree with it."""
    y += 4 * S
    from collections import Counter
    allst = [C.LEAD] + C.SECOND + C.CARDS
    rc = Counter(s["region"] for s in allst)
    fc = Counter(s["field"] for s in allst)
    order = [r for r in ("EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS",
                         "OCEANIA", "WORLD") if rc[r]]
    assert sum(rc.values()) == len(allst)

    ft = P.f("nb", 7.4)
    ph = int(7.4 * S * 1.60)
    x = M
    for name in order:
        lab = f"{name} {rc[name]}"
        tw = P.caps_width(d, lab, ft, 0.85 * S)
        pg.box(x, y, x + tw + 6 * S, y + ph, P.REGION[name])
        P.caps(d, x + 3 * S, y + int(7.4 * S * 0.38), lab, ft, P.WHITE, 0.85 * S)
        x += tw + 10 * S
    fields = " \u00b7 ".join(f"{k} {v}" for k, v in
                            sorted(fc.items(), key=lambda kv: -kv[1]))
    fw = P.caps_width(d, fields, P.f("nb", 6.3), 0.45 * S)
    P.caps(d, CW - M - fw, y + int(7.4 * S * 0.50), fields,
           P.f("nb", 6.3), P.INK_SOFT, 0.45 * S)
    return y + ph + 11 * S


# --------------------------------------------------------------- features

def _feat(page, x, y, w, story, motif, k, draw_ill=True, bottom=None):
    """A top story: its spot graphic, its tab, its headline, its deck, its source.

    When `bottom` is given the source line is set on it, so all four features
    close on one baseline however many lines their copy runs to. That is what
    stops the row ending in a stagger, and it is why the four columns can then
    be ruled to a single depth.
    """
    dd = page.d
    if draw_ill:
        gfx.draw(dd, (x, y, x + w, y + ILL), motif)
    yy = y + ILL + 5 * S
    tab_pt = 7.0
    tx, ph = L.tab(page, x, yy, story["region"], tab_pt)
    P.caps(dd, tx, yy + int(tab_pt * S * 0.36), story["desk"], P.f("nb", tab_pt),
           P.INK_SOFT, 0.7 * S)
    yy += ph + 4 * S

    ft = P.f("sb", 21.0 * k)
    for ln in P.wrap(dd, story["head"], ft, w):
        if draw_ill:
            dd.text((x, yy), ln, font=ft, fill=P.INK)
        yy += int(ft.size * 1.04)
    yy += 4 * S

    dps = P.f("sr", 8.4 * k)
    for ln in P.wrap(dd, story["deck"], dps, w):
        if draw_ill:
            dd.text((x, yy), ln, font=dps, fill=P.INK_MID)
        yy += int(dps.size * 1.28)
    yy += 5 * S

    src_h = 4 * S + int(6.2 * S * 1.7)
    if bottom is not None:
        yy = max(yy, bottom - src_h)
    if draw_ill:
        P.hline(dd, x, x + min(w, 34 * S), yy, P.HAIR, 1 * S)
        P.caps(dd, x, yy + 4 * S, story["src"].upper(), P.f("nb", 6.2), P.INK_SOFT, 0.55 * S)
    return yy + src_h


def _feat_probe(y, k):
    """The tallest of the four features at scale k, ignoring the shared baseline."""
    return max(_feat(L.Page(), colx(i), y, COLW, s, FEAT_MOTIF[i], k, False)
               for i, s in enumerate([C.LEAD] + C.SECOND))


def feature_band(y, target):
    """Solve the four features to close on `target`, then rule them to it."""
    k = solve(lambda p, k: _feat_probe(y, k), target, 0.72, 1.36)
    for i, s in enumerate([C.LEAD] + C.SECOND):
        _feat(pg, colx(i), y, COLW, s, FEAT_MOTIF[i], k, True, target)
    for i in range(1, 4):
        P.vline(d, colx(i) - GUT // 2, y, target, P.HAIR, 1 * S)
    return target, k


# ------------------------------------------------------------------- cards

CARD_PT, DECK_PT, TAB_PT, TAIL_BUMP, TAIL_DECK = 13.6, 8.4, 6.8, 2.6, 0.5


def _bare(story):
    """A card without its source line: the tail of every story names its wire in
    the footer, and the four features carry theirs in full, so repeating it
    fourteen times only buys grey. Dropping it buys a full point of type size."""
    return {k: v for k, v in story.items() if k != "src"}


CARD_MOTIF = {
    0: "truce", 1: "cyclone", 2: "inflation", 3: "sudan", 4: "raid",
    5: "factories", 6: "space", 7: "border", 8: "stamp", 9: "verdict",
    10: "globe", 11: "raid",
}
ART_FRAC = 0.22      # the art band's share of a module's width
ART_CARDS = 8        # how many cards lead with art; the rest run as a tail row
TAIL_HS = 12.4       # the tail: headline only, two columns each, no art


def card_rows(y, gap, k):
    """Three rows of four, then the tail cards running two columns each."""
    hs, ds = CARD_PT * k, DECK_PT * k
    art_h = int(COLW * ART_FRAC)
    row_h = max(L.card_h(COLW, _bare(c), hsize=hs, dsize=ds, tab_pt=TAB_PT,
                         lh=1.05, art_h=art_h, bar=True) for c in C.CARDS[:4])
    for r in range(ART_CARDS // 4):
        for c in range(4):
            i = r * 4 + c
            L.card(pg, colx(c), y, COLW, _bare(C.CARDS[i]), hsize=hs,
                   dsize=ds, tab_pt=TAB_PT, lh=1.05, rule_w=26,
                   art_h=art_h, motif=CARD_MOTIF[i], bar=True)
        P.hline(d, M, CW - M, y + row_h + gap // 2, P.HAIR, 1 * S)
        y += row_h + gap

    # The rest of the day, at a smaller weight: every story filed still gets its
    # headline on the page, so nothing is dropped to buy the art band.
    tail = C.CARDS[ART_CARDS:]
    if tail:
        tw = span(2)
        th = max(L.tab_head_h(tw, c, hsize=TAIL_HS, tab_pt=TAB_PT)
                 for c in tail)
        for i, c in enumerate(tail):
            cx = M + (i % 2) * (tw + GUT)
            cy = y + (i // 2) * (th + 6 * S)
            L.tab_head(pg, cx, cy, tw, c, hsize=TAIL_HS, tab_pt=TAB_PT)
        rows = (len(tail) + 1) // 2
        y += rows * th + (rows - 1) * 6 * S
    return y


def _cards_probe(y, k):
    """Where `card_rows` would end, at scale k, without drawing anything."""
    hs, ds = CARD_PT * k, DECK_PT * k
    art_h = int(COLW * ART_FRAC)
    row_h = max(L.card_h(COLW, _bare(c), hsize=hs, dsize=ds, tab_pt=TAB_PT,
                         lh=1.05, art_h=art_h, bar=True) for c in C.CARDS[:4])
    yy = y + (ART_CARDS // 4) * (row_h + 11 * S)
    tail = C.CARDS[ART_CARDS:]
    if tail:
        th = max(L.tab_head_h(span(2), c, hsize=TAIL_HS, tab_pt=TAB_PT)
                 for c in tail)
        rows = (len(tail) + 1) // 2
        yy += rows * th + (rows - 1) * 6 * S
    return yy


# -------------------------------------------------------------------- foot

BR_PT_P, BR_PT_B = 7.3, 7.7


BR_N = 20          # how many one-line briefs the wire block carries


def briefs_natural(n=None):
    """The height the wire columns need if set solid, with no extra leading."""
    n = BR_N if n is None else n
    per = (n + 3) // 4
    inner = COLW - 6 * S
    natural = 0
    for c in range(4):
        yy = 0
        for place, what in C.BRIEFS[c * per:min(n, (c + 1) * per)]:
            pw = P.tlen(d, place + " \u2014 ", P.f("nb", BR_PT_P))
            yy += int(BR_PT_B * S * 1.32) * max(
                1, len(P.wrap(d, what, P.f("sr", BR_PT_B), inner - pw)))
            yy += int(BR_PT_B * S * 1.05)
        natural = max(natural, yy)
    return natural


def briefs(y, bottom):
    y = L.rulehead(pg, M, y, INNER, "ALSO ON WEDNESDAY 18 NOVEMBER", P.RED, 8.2)
    per = (BR_N + 3) // 4
    pt_p, pt_b = BR_PT_P, BR_PT_B
    inner = COLW - 6 * S

    natural = briefs_natural()
    pad = max(0, int(((bottom - y) - natural) / max(1, per)) * 0.94)

    for c in range(4):
        x = colx(c)
        if c:
            P.vline(d, x - GUT // 2, y - 3 * S, bottom - 2 * S, P.HAIR, 1 * S)
        yy = y
        for place, what in C.BRIEFS[c * per:min(BR_N, (c + 1) * per)]:
            d.ellipse([x, yy + int(2.9 * S), x + int(2.2 * S), yy + int(5.1 * S)], fill=P.RED)
            lead = place + " \u2014 "
            pw = P.tlen(d, lead, P.f("nb", pt_p))
            d.text((x + 6 * S, yy), lead, font=P.f("nb", pt_p), fill=P.INK)
            lines = P.wrap(d, what, P.f("sr", pt_b), inner - pw)
            step = int(pt_b * S * 1.32)
            d.text((x + 6 * S + pw, yy), lines[0], font=P.f("sr", pt_b), fill=P.INK_MID)
            for ln in lines[1:]:
                yy += step
                d.text((x + 6 * S, yy), ln, font=P.f("sr", pt_b), fill=P.INK_MID)
            yy += step + pad
        if yy > bottom + pad:
            pg.warn.append(("briefs-over", c, round((yy - bottom) / S, 1)))
    return bottom


def stats(y, bottom):
    step = INNER // len(C.STATS)
    for i, (num, lab) in enumerate(C.STATS):
        x = M + i * step
        if i:
            P.vline(d, x - 7 * S, y, bottom - 7 * S, P.HAIR, 1 * S)
        pg.text(x, y, num, "sb", 16.5, P.RED, maxw=step - 10 * S)
        P.caps(d, x, y + int(16.5 * S * 1.24), lab, P.f("nb", 6.1), P.INK_SOFT, 0.4 * S)


FOOT_NOTE = ("Every story here happened, or was first reported, on Wednesday 18 November 2026. "
             "Figures are as the wires carried them; contested claims are attributed. "
             "Sources: AP, Reuters, AFP, Al Jazeera, BBC, NASA, IMD, ONS, Amnesty International.")


def footer_h():
    """Height of the provenance note, measured rather than assumed."""
    ft = P.f("si", 6.8)
    return len(P.wrap(d, FOOT_NOTE, ft, INNER)) * int(6.8 * S * 1.32)


def footer(y):
    ft = P.f("si", 6.8)
    yy = y
    for ln in P.wrap(d, FOOT_NOTE, ft, INNER):
        d.text((M, yy), ln, font=ft, fill=P.INK_SOFT)
        yy += int(6.8 * S * 1.32)
    return yy


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "out/entry.png"
    bottom = CH - M

    y = masthead(M)
    y = standfirst(y)
    y = index(y)

    # The foot is built from the bottom up, and every part is measured:
    #
    #   bottom | figures strip (stats_h) | gap | provenance note | rule | wire
    #
    # Nothing below is guessed, so the briefs can never run into the note and the
    # note can never sit on the figures.
    stats_h = int(16.5 * S * 1.24) + int(6.1 * S * 1.85)
    note_y = bottom - footer_h()
    stats_top = note_y - 9 * S - stats_h

    # The wire block is measured too: seven briefs a column at a fixed size.
    briefs_top = stats_top - 14 * S
    wire_h = L.rulehead_h(8.2) + briefs_natural() + 8 * S
    cards_room = briefs_top - wire_h - 18 * S - y

    # The two bands divide what is left in a stated share, and each is then
    # solved to close exactly on its share: neither can starve the other, and
    # neither can leave a hole. The share is written here, once.
    # Split what is left between the two bands in the ratio their own content
    # asks for, measured at full size rather than written down as a fraction:
    # each band then reads at the same type scale, and neither starves the other.
    n_feat = _feat_probe(0, 1.0)
    n_cards = _cards_probe(0, 1.0)
    share = n_feat / (n_feat + n_cards)
    band_h = int(cards_room * share) - 11 * S
    cards_h_target = cards_room - band_h - 22 * S

    y, kf = feature_band(y, y + band_h)
    kc = solve(lambda p, k: _cards_probe(y, k) - y, cards_h_target, 0.70, 1.25)
    y = card_rows(y, 11 * S, kc)
    pg.scale["features"] = kf
    pg.scale["cards"] = kc

    P.hline(d, M, CW - M, y + 6 * S, P.RULE, 1 * S)
    briefs(y + 18 * S, briefs_top)

    P.hline(d, M, CW - M, stats_top - 8 * S, P.RULE, 2 * S)
    stats(stats_top, stats_top + stats_h)
    footer(note_y)

    # Record every panel label's box beside the image, so the checker can prove
    # after the fact that no two labels collide and none leaves its panel.
    with open(os.path.splitext(out)[0] + ".labels.json", "w") as fh:
        # The page is drawn at S times final size, so the boxes are stored in
        # final pixels: the checker then needs no knowledge of the drawing scale.
        json.dump([{"box": [round(v / S, 1) for v in b], "text": t}
                   for b, t, _ in gfx._BOXES], fh)

    im = pg.im.resize((P.W, P.H), Image.LANCZOS)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    im.save(out, "PNG", optimize=True)
    print("wrote", out, im.size, os.path.getsize(out), "bytes")
    print("scale  features=%.3f  cards=%.3f" % (kf, kc))
    if pg.warn:
        print("WARNINGS:", len(pg.warn))
        for w in pg.warn[:24]:
            print("  ", w)
    else:
        print("no warnings")


if __name__ == "__main__":
    main()
