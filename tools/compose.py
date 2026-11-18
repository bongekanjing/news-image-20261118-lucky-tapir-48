#!/usr/bin/env python3
"""Compose the front page at 3x and write it at 1024 x 1024.

Run:  python3 tools/compose.py out/entry.png

Nothing on this sheet is a picture. It is a page of type set on a fixed grid,
and the type is the variable that gets solved: each band is drawn once off to
the side to measure itself, then the copy is scaled so the band closes exactly
on the height the page has budgeted for it. That is why there are no holes and
no overlaps - the empty space is spent as leading rather than left as a gap.
"""

import os
import sys

from PIL import Image

import copy as C
import layout as L
import paper as P

S = P.S
CW, CH, M, INNER, GUT, COLW = P.CW, P.CH, L.M, L.INNER, L.GUT, L.COLW
colx, span = L.colx, L.span

pg = L.Page()
d = pg.d


def solve(draw, target, lo=0.80, hi=1.45, iters=22):
    """Find the scale at which `draw(page, scale)` ends nearest `target`."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        scratch = L.Page()
        end = draw(scratch, mid)
        if end < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


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

    # A red rule closes the nameplate and doubles as the section index's edge.
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


# ------------------------------------------------------------------- lead

def _lead_left(page, y, k, lw):
    """Headline, a two-column deck and three attributed fact columns."""
    dd = page.d
    tab_pt = 8.4
    tx, ph = L.tab(page, M, y, C.LEAD["region"], tab_pt)
    P.caps(dd, tx, y + int(tab_pt * S * 0.36), C.LEAD["desk"], P.f("nb", tab_pt),
           P.INK_SOFT, 0.7 * S)
    yy = y + ph + 4 * S

    hsize = 27.0 * k
    ft = P.f("sb", hsize)
    step = int(ft.size * 1.03)
    for ln in P.wrap(dd, C.LEAD["head"], ft, lw):
        dd.text((M, yy), ln, font=ft, fill=P.INK)
        yy += step
    yy += 5 * S

    deck_w = (lw - GUT) // 2
    dfs = P.f("sr", 9.4 * k)
    lines = P.wrap(dd, C.LEAD["deck"], dfs, deck_w)
    half = (len(lines) + 1) // 2
    dstep = int(dfs.size * 1.30)
    for c, chunk in enumerate([lines[:half], lines[half:]]):
        cx, cy = M + c * (deck_w + GUT), yy
        for ln in chunk:
            dd.text((cx, cy), ln, font=dfs, fill=P.INK_MID)
            cy += dstep
    yy += max(len(lines[:half]), len(lines[half:])) * dstep + 7 * S

    P.hline(dd, M, M + lw, yy, P.HAIR, 1 * S)
    yy += 5 * S
    fw = (lw - 2 * GUT) // 3
    ftp = P.f("nb", 6.7 * k)
    ftr = P.f("sr", 7.7 * k)
    top = yy
    deepest = 0
    for i, (place, text) in enumerate(C.LEAD["facts"]):
        fx = M + i * (fw + GUT)
        P.caps(dd, fx, top, place.upper(), ftp, P.RED, 0.7 * S)
        cy = top + int(ftp.size * 1.75)
        for ln in P.wrap(dd, text, ftr, fw):
            dd.text((fx, cy), ln, font=ftr, fill=P.INK_MID)
            cy += int(ftr.size * 1.28)
        deepest = max(deepest, cy)
    yy = deepest + 5 * S

    P.hline(dd, M, M + lw, yy, P.HAIR, 1 * S)
    P.caps(dd, M, yy + 4 * S, C.LEAD["src"].upper(), P.f("nb", 6.2), P.INK_SOFT, 0.55 * S)
    return yy + 4 * S + int(6.2 * S * 1.7)


def _rail(page, y, k):
    ry = y
    n = len(C.SECOND)
    for i, s in enumerate(C.SECOND):
        ry = L.card(page, colx(3), ry, COLW, s, hsize=13.0 * k, dsize=8.1 * k,
                    tab_pt=6.8, lh=1.05, rule_w=26)
        if i < n - 1:
            P.hline(page.d, colx(3), colx(3) + COLW, ry + 7 * S, P.HAIR, 1 * S)
            ry += 14 * S
    return ry


def lead_band(y, band_h):
    lw, rx = span(3), colx(3)
    target = y + band_h

    kl = solve(lambda p, k: _lead_left(p, y, k, lw), target)
    kr = solve(lambda p, k: _rail(p, y, k), target)

    _lead_left(pg, y, kl, lw)
    _rail(pg, y, kr)
    P.vline(d, M + lw + GUT // 2, y, target, P.HAIR, 1 * S)
    return target + 11 * S, kl, kr


# ------------------------------------------------------------------- cards

def card_rows(y, gap, k):
    """Three rows of four, then the tail cards running two columns each."""
    hs, ds = 14.4 * k, 9.0 * k
    row_h = max(L.card_h(COLW, c, hsize=hs, dsize=ds, tab_pt=7.0, lh=1.05)
                for c in C.CARDS[:12])
    for r in range(3):
        for c in range(4):
            L.card(pg, colx(c), y, COLW, C.CARDS[r * 4 + c], hsize=hs, dsize=ds,
                   tab_pt=7.0, lh=1.05, rule_w=26)
        P.hline(d, M, CW - M, y + row_h + gap // 2, P.HAIR, 1 * S)
        y += row_h + gap

    tail = C.CARDS[12:]
    if tail:
        w = span(2)
        th = max(L.card_h(w, c, hsize=(hs + 2.8), dsize=(ds + 0.6), tab_pt=7.0,
                          lh=1.05) for c in tail)
        for i, c in enumerate(tail):
            L.card(pg, M + i * (w + GUT), y, w, c, hsize=(hs + 2.8),
                   dsize=(ds + 0.6), tab_pt=7.0, lh=1.05, rule_w=40)
        y += th
    return y


# ------------------------------------------------------------------- foot

def _cards_probe(y, k):
    """Where `card_rows` would end, at scale k, without drawing anything."""
    hs, ds = 14.4 * k, 9.0 * k
    row_h = max(L.card_h(COLW, c, hsize=hs, dsize=ds, tab_pt=7.0, lh=1.05)
                for c in C.CARDS[:12])
    yy = y + 3 * (row_h + 11 * S)
    tail = C.CARDS[12:]
    if tail:
        yy += max(L.card_h(span(2), c, hsize=hs + 2.8, dsize=ds + 0.6,
                           tab_pt=7.0, lh=1.05) for c in tail)
    return yy


def briefs(y, bottom):
    y = L.rulehead(pg, M, y, INNER, "ALSO ON WEDNESDAY 18 NOVEMBER", P.RED, 8.2)
    per = (len(C.BRIEFS) + 3) // 4
    pt_p, pt_b = 7.3, 7.7
    inner = COLW - 6 * S

    natural = 0
    for c in range(4):
        yy = 0
        for place, what in C.BRIEFS[c * per:(c + 1) * per]:
            pw = P.tlen(d, place + " \u2014 ", P.f("nb", pt_p))
            yy += int(pt_b * S * 1.32) * max(1, len(P.wrap(d, what, P.f("sr", pt_b), inner - pw)))
            yy += int(pt_b * S * 1.05)
        natural = max(natural, yy)
    pad = max(0, int(((bottom - y) - natural) / max(1, per)) * 0.94)

    for c in range(4):
        x = colx(c)
        if c:
            P.vline(d, x - GUT // 2, y - 3 * S, bottom - 2 * S, P.HAIR, 1 * S)
        yy = y
        for place, what in C.BRIEFS[c * per:(c + 1) * per]:
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


def footer(y):
    note = ("Every story here happened, or was first reported, on Wednesday 18 November 2026. "
            "Figures are as the wires carried them; contested claims are attributed. "
            "Sources: AP, Reuters, AFP, Al Jazeera, BBC, NASA, IMD, ONS, Amnesty International.")
    ft = P.f("si", 6.8)
    yy = y
    for ln in P.wrap(d, note, ft, INNER):
        d.text((M, yy), ln, font=ft, fill=P.INK_SOFT)
        yy += int(6.8 * S * 1.32)
    return yy


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "out/entry.png"
    bottom = CH - M

    y = masthead(M)
    y = standfirst(y)
    y = index(y)

    # The foot is measured first and pinned; the lead band takes a fixed share
    # of what is left, and the cards take the rest.
    stats_h = int(16.5 * S * 1.24) + int(6.1 * S * 1.85) + 13 * S
    foot_h = stats_h + 6 * S + 2 * int(6.8 * S * 1.32) + 5 * S
    stats_top = bottom - foot_h

    band_h = int((stats_top - y) * 0.315)
    y, kl, kr = lead_band(y, band_h)

    # Solve the card block against the space between the lead and the wire.
    briefs_top = stats_top - 13 * S
    wire_h = L.rulehead_h(8.2) + int(196.0 * S) + 16 * S
    cards_target = briefs_top - wire_h - 16 * S
    kc = solve(lambda p, k: _cards_probe(y, k), cards_target, 0.82, 1.25)
    y = card_rows(y, 11 * S, kc)
    pg.scale["cards"] = kc

    P.hline(d, M, CW - M, y + 6 * S, P.RULE, 1 * S)
    briefs(y + 18 * S, briefs_top)
    P.hline(d, M, CW - M, stats_top - 9 * S, P.RULE, 2 * S)
    stats(stats_top, bottom)
    P.hline(d, M, CW - M, stats_top - int(16.5 * S * 1.24) - int(6.1 * S * 1.85) - 8 * S,
            P.HAIR, 1 * S)
    footer(stats_top - int(16.5 * S * 1.24) - int(6.1 * S * 1.85) - 2 * S)

    im = pg.im.resize((P.W, P.H), Image.LANCZOS)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    im.save(out, "PNG", optimize=True)
    print("wrote", out, im.size, os.path.getsize(out), "bytes")
    print("lead scale  L=%.3f  R=%.3f" % (kl, kr))
    if pg.warn:
        print("WARNINGS:", len(pg.warn))
        for w in pg.warn[:24]:
            print("  ", w)
    else:
        print("no warnings")


if __name__ == "__main__":
    main()
