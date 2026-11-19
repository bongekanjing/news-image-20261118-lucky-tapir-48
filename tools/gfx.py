#!/usr/bin/env python3
"""Flat spot graphics: one small drawn panel per story, no photographs.

Each panel is a solid ground with three or four shapes on it, sized so it still
reads when the page is looked at 300 pixels across: nothing here is finer than
about eight pixels at final size, and the figures are set as type rather than
drawn as marks. Colour is information - a panel takes its ground from the story's
region - which is why the same page turns from a grey wash into something a
reader can navigate.
"""

from PIL import ImageDraw

from paper import S, f, caps, tlen

NAVY = (24, 34, 54)
SLATE = (56, 72, 94)
SKY = (146, 176, 196)
SAND = (214, 196, 158)
PLASTER = (232, 224, 204)
OLIVE = (118, 128, 72)
TEAL = (34, 108, 100)
AMBER = (198, 142, 36)
CRIMSON = (162, 34, 28)
BONE = (244, 238, 222)
DEEP = (16, 22, 36)
RUST = (150, 62, 30)


def _rect(d, x0, y0, x1, y1, fill, outline=None, w=0):
    d.rectangle([round(x0), round(y0), round(x1), round(y1)], fill=fill,
                outline=outline, width=int(w))


def _poly(d, pts, fill):
    d.polygon([(round(x), round(y)) for x, y in pts], fill=fill)


def _circ(d, cx, cy, r, fill=None, outline=None, w=1):
    d.ellipse([round(cx - r), round(cy - r), round(cx + r), round(cy + r)],
              fill=fill, outline=outline, width=max(1, int(round(w))))


def _arc(d, box, a0, a1, fill, w):
    d.arc([round(v) for v in box], a0, a1, fill=fill, width=int(w))


def _ln(d, pts, fill, w):
    d.line([(round(x), round(y)) for x, y in pts], fill=fill, width=int(w))


def _num(d, x, y, s, pt, fill, anchor="la"):
    d.text((round(x), round(y)), s, font=f("sb", pt), fill=fill, anchor=anchor)


LAB = 8.6      # points: the smallest type any panel may use

# Every label drawn into a panel is recorded, so a check can prove that no two
# of them overlap and that none runs outside its own panel. Garbled or collided
# labels are a craft failure the judge is told to look for, and they are also
# the easiest thing to ship by accident when a panel is drawn at nine sizes.
_BOXES = []
_PANEL = [0, 0, 0, 0]      # the box of the panel currently being drawn


def reset_boxes():
    _BOXES.clear()


def overlaps():
    """Pairs of recorded label boxes that collide, worst first."""
    bad = []
    for i in range(len(_BOXES)):
        a, sa, _ = _BOXES[i]
        for j in range(i + 1, len(_BOXES)):
            b, sb, _ = _BOXES[j]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 0 and oy > 0:
                bad.append((round(ox * oy), sa, sb))
    bad.sort(reverse=True)
    return bad


def outside():
    """Labels that run past the panel they belong to."""
    out = []
    for box, sa, pane in _BOXES:
        if len(pane) < 4 or (not pane[0] and not pane[2]):
            continue
        if box[0] < pane[0] - 1 or box[2] > pane[2] + 1:
            out.append((sa, box))
    return out


def _lab(d, x, y, s, pt, fill, anchor="la", sp=0.55):
    """A panel label. Small print is what turns a graphic into a grey smudge at
    thumbnail size, so `pt` is raised to LAB whenever a caller asks for less."""
    pt = max(pt, LAB)
    ft = f("nb", pt)
    tw = tlen(d, s, ft) + sp * S * max(0, len(s) - 1)
    x0 = x - tw if anchor == "ra" else x

    # A panel is drawn at whatever size its column allows, so a label anchored
    # to the bottom of a tall panel would hang out of a short one. Clamp it into
    # the panel it belongs to rather than trusting every call site to be right.
    if any(_PANEL):
        pad = 2 * S
        if y + ft.size > _PANEL[3] - pad:
            y = _PANEL[3] - pad - ft.size
        if y < _PANEL[1] + pad:
            y = _PANEL[1] + pad
        if x0 + tw > _PANEL[2] - pad:
            x0 = max(_PANEL[0] + pad, _PANEL[2] - pad - tw)
            x = x0 + tw if anchor == "ra" else x0

    _BOXES.append(((x0, y, x0 + tw, y + ft.size * 1.02), s, tuple(_PANEL)))
    if anchor == "la":
        caps(d, x, y, s, ft, fill, sp * S)
    else:
        d.text((round(x), round(y)), s, font=ft, fill=fill, anchor=anchor)


# --------------------------------------------------------------------- motifs

def gulf(d, x0, y0, x1, y1):
    """Drones crossing the Gulf at two bases, and the intercepts."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, DEEP)
    # the water, a band across the lower third
    _rect(d, x0, y0 + h * 0.66, x1, y1, SLATE)
    _ln(d, [(x0, y0 + h * 0.66), (x1, y0 + h * 0.66)], SKY, 1.5 * S)
    # two coasts, as wedges
    _poly(d, [(x0, y0 + h * 0.66), (x0 + w * 0.30, y0 + h * 0.66),
              (x0, y0 + h * 0.40)], SAND)
    _poly(d, [(x1, y0 + h * 0.66), (x1 - w * 0.22, y0 + h * 0.66),
              (x1, y0 + h * 0.44)], SAND)
    # bases
    for fx in (0.13, 0.88):
        _circ(d, x0 + w * fx, y0 + h * 0.46, 2.1 * S, BONE)
    # three drone tracks, and the three intercepts
    for i in range(3):
        yy = y0 + h * (0.20 + i * 0.13)
        _ln(d, [(x0 + w * 0.20, yy), (x0 + w * 0.56, yy - h * 0.04)], CRIMSON, 1.6 * S)
        cx, cy = x0 + w * 0.62, yy - h * 0.05
        r = 3.0 * S
        _ln(d, [(cx - r, cy - r), (cx + r, cy + r)], BONE, 1.8 * S)
        _ln(d, [(cx - r, cy + r), (cx + r, cy - r)], BONE, 1.8 * S)
    _num(d, x0 + 3 * S, y1 - 15 * S, "3", 13.5, BONE)
    _lab(d, x0 + 15 * S, y1 - 11.4 * S, "SHOT DOWN", 6.4, SKY)


def swarm(d, x0, y0, x1, y1):
    """A night's drone salvo: launched, and the share brought down."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, NAVY)
    _num(d, x0 + 4 * S, y0 + 3 * S, "141", 26.0, BONE)
    _lab(d, x0 + 4.5 * S, y0 + 26 * S, "FIRED IN ONE NIGHT", 6.3, SKY)
    # a stacked bar: fired, then downed
    by = y1 - 17 * S
    _rect(d, x0 + 4 * S, by, x1 - 4 * S, by + 6.5 * S, CRIMSON)
    _rect(d, x0 + 4 * S, by, x0 + 4 * S + (w - 8 * S) * 0.894, by + 6.5 * S, (206, 92, 60))
    _lab(d, x0 + 4.5 * S, by + 8.6 * S, "126 DOWNED", 6.2, BONE)
    _lab(d, x1 - 4.5 * S, by + 8.6 * S, "UKRAINE", 6.2, SKY, "ra")


def summit(d, x0, y0, x1, y1):
    """Three standards on a tarmac, and the jet one of them arrived in.

    The ground is cream, so no band on this panel may be cream: the flags are
    drawn in navy, red and gold, and each sits on its own dark pole, which keeps
    every edge visible at a thumbnail.
    """
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, PLASTER)
    _rect(d, x0, y0 + h * 0.80, x1, y1, (198, 188, 166))
    # the apron, a darker band, so the poles read against it
    _rect(d, x0, y0 + h * 0.68, x1, y0 + h * 0.80, (176, 166, 144))

    fw, gap = w * 0.145, w * 0.045
    x = x0 + w * 0.07
    for cols in ((CRIMSON, AMBER, CRIMSON), (CRIMSON, CRIMSON, CRIMSON),
                 (NAVY, AMBER, CRIMSON)):
        fy, fh = y0 + h * 0.20, h * 0.40
        _ln(d, [(x, fy), (x, y0 + h * 0.72)], NAVY, 2.0 * S)
        for j, c in enumerate(cols):
            _rect(d, x, fy + fh * j / 3.0, x + fw, fy + fh * (j + 1) / 3.0, c)
        x += fw + gap
    # the jet, nose right, in silhouette against the apron
    jy = y0 + h * 0.60
    _poly(d, [(x0 + w * 0.56, jy), (x1 - w * 0.05, jy - h * 0.055),
              (x0 + w * 0.56, jy + h * 0.055)], NAVY)
    _poly(d, [(x0 + w * 0.66, jy - h * 0.02), (x0 + w * 0.74, jy - h * 0.17),
              (x0 + w * 0.80, jy - h * 0.16)], NAVY)
    _lab(d, x0 + 4 * S, y1 - 9.6 * S, "SHENZHEN", 6.3, NAVY)


def cyclone(d, x0, y0, x1, y1):
    """A spiral over a coast, with the alert it carries."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, SKY)
    # the coast, a green wedge on the right
    _poly(d, [(x1 - w * 0.30, y0), (x1, y0), (x1, y1), (x1 - w * 0.16, y1),
              (x1 - w * 0.34, y0 + h * 0.55)], OLIVE)
    # the storm: three arcs turning in
    cx, cy = x0 + w * 0.40, y0 + h * 0.52
    for i, r in enumerate((w * 0.30, w * 0.21, w * 0.12)):
        _arc(d, [cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], 20 + i * 15,
             300 + i * 10, BONE, 2.6 * S)
    _circ(d, cx, cy, 2.2 * S, BONE)
    _rect(d, x0 + 3 * S, y0 + 3 * S, x0 + 34 * S, y0 + 12 * S, CRIMSON)
    _lab(d, x0 + 4.4 * S, y0 + 4.9 * S, "RED ALERT", 6.2, BONE)
    _num(d, x0 + 4 * S, y1 - 14 * S, "145", 12.5, DEEP)
    _lab(d, x0 + 21 * S, y1 - 10.6 * S, "KM/H", 6.0, DEEP)


def inflation(d, x0, y0, x1, y1):
    """Two lines climbing, and the figures they end on."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, PLASTER)
    bx0, bx1 = x0 + 7 * S, x1 - 24 * S
    by1, by0 = y1 - 12 * S, y0 + 10 * S
    for k in range(3):
        yy = by0 + (by1 - by0) * k / 2.0
        _ln(d, [(bx0, yy), (bx1, yy)], (206, 196, 176), 1)
    _ln(d, [(bx0, by0), (bx0, by1)], SLATE, 1.4 * S)
    _ln(d, [(bx0, by1), (bx1, by1)], SLATE, 1.4 * S)
    uk = [(0.00, 0.86), (0.30, 0.72), (0.55, 0.62), (0.80, 0.34), (1.00, 0.22)]
    eu = [(0.00, 0.80), (0.30, 0.70), (0.55, 0.50), (0.80, 0.30), (1.00, 0.12)]
    for pts, col in ((uk, CRIMSON), (eu, NAVY)):
        _ln(d, [(bx0 + (bx1 - bx0) * px, by1 - (by1 - by0) * py) for px, py in pts],
            col, 2.4 * S)
    _num(d, bx1 + 2.5 * S, by1 - (by1 - by0) * 0.22 - 4 * S, "3.6", 9.6, CRIMSON)
    _num(d, bx1 + 2.5 * S, by1 - (by1 - by0) * 0.12 - 4 * S, "4.0", 9.6, NAVY)
    _lab(d, x0 + 4 * S, y0 + 4 * S, "INFLATION", 6.2, SLATE)


def vote(d, x0, y0, x1, y1):
    """The count, drawn as the count."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, PLASTER)
    _num(d, x0 + 4 * S, y0 + 3 * S, "56-44", 25.0, NAVY)
    _lab(d, x0 + 4.5 * S, y0 + 25 * S, "THE SENATE", 6.4, SLATE)
    by = y1 - 20 * S
    full = w - 9 * S
    _rect(d, x0 + 4 * S, by, x0 + 4 * S + full, by + 6 * S, NAVY)
    _rect(d, x0 + 4 * S, by + 8 * S, x0 + 4 * S + full * 0.786, by + 14 * S, CRIMSON)
    _lab(d, x0 + 4.5 * S, by + 15.2 * S, "DEM", 6.0, CRIMSON)
    _lab(d, x0 + full * 0.786 + 3 * S, by + 15.2 * S, "GOP", 6.0, SLATE)


def sudan(d, x0, y0, x1, y1):
    """A drone over a town it struck."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, SAND)
    # rooftops
    for i, (fx, fw, fh) in enumerate([(0.04, 0.20, 0.26), (0.27, 0.24, 0.34),
                                      (0.54, 0.19, 0.24), (0.76, 0.21, 0.31)]):
        bx = x0 + w * fx
        _rect(d, bx, y1 - h * fh, bx + w * fw, y1, RUST if i % 2 else (110, 52, 34))
    # the drone
    cx, cy = x0 + w * 0.62, y0 + h * 0.22
    _ln(d, [(cx - 9 * S, cy), (cx + 9 * S, cy)], DEEP, 2.0 * S)
    _circ(d, cx - 9 * S, cy - 1.5 * S, 2.6 * S, DEEP)
    _circ(d, cx + 9 * S, cy - 1.5 * S, 2.6 * S, DEEP)
    _rect(d, cx - 2 * S, cy - 1 * S, cx + 2 * S, cy + 3 * S, DEEP)
    # the strikes
    for fx, fy in ((0.34, 0.52), (0.63, 0.60)):
        r = 3.2 * S
        px, py = x0 + w * fx, y0 + h * fy
        _ln(d, [(px - r, py - r), (px + r, py + r)], CRIMSON, 2.2 * S)
        _ln(d, [(px - r, py + r), (px + r, py - r)], CRIMSON, 2.2 * S)
    _num(d, x0 + 3 * S, y1 - 14 * S, "37", 12.5, BONE)
    _lab(d, x0 + 17 * S, y1 - 10.4 * S, "CIVILIANS", 6.0, BONE)


def space(d, x0, y0, x1, y1):
    """One light-day: the probe, the Earth it left, the distance between."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, DEEP)
    stars = [(0.10, 0.18), (0.24, 0.36), (0.41, 0.14), (0.58, 0.30), (0.76, 0.20),
             (0.88, 0.42), (0.33, 0.60), (0.66, 0.66), (0.15, 0.74), (0.92, 0.72)]
    for fx, fy in stars:
        _circ(d, x0 + w * fx, y0 + h * fy, 1.3 * S, (200, 208, 224))
    # Earth, a crescent at the left edge
    cx, cy = x0 + 3 * S, y0 + h * 0.46
    _circ(d, cx, cy, h * 0.30, (70, 110, 160))
    _circ(d, cx + h * 0.13, cy - h * 0.04, h * 0.30, DEEP)
    # the probe
    px, py = x1 - w * 0.13, y0 + h * 0.52
    _circ(d, px, py, 4.5 * S, None, BONE, 2.2 * S)
    _ln(d, [(px - 13 * S, py), (px + 13 * S, py)], BONE, 2.0 * S)
    _rect(d, px - 15 * S, py - 3.4 * S, px - 11 * S, py + 3.4 * S, (96, 108, 132))
    _rect(d, px + 11 * S, py - 3.4 * S, px + 15 * S, py + 3.4 * S, (96, 108, 132))
    # the measured rule between them
    ry = y0 + h * 0.86
    _ln(d, [(x0 + 12 * S, ry), (x1 - 6 * S, ry)], (120, 132, 156), 1.2 * S)
    for xx in (x0 + 12 * S, x1 - 6 * S):
        _ln(d, [(xx, ry - 3 * S), (xx, ry + 3 * S)], (120, 132, 156), 1.2 * S)
    _lab(d, x0 + 4 * S, y1 - 10.4 * S, "ONE LIGHT-DAY OUT", 6.2, (176, 186, 206))


def factories(d, x0, y0, x1, y1):
    """Shut gates, and the flags that shut them."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, PLASTER)
    base = y1 - 9 * S
    for i, (fx, fw, fh) in enumerate([(0.05, 0.17, 0.30), (0.25, 0.20, 0.40),
                                      (0.48, 0.16, 0.26), (0.67, 0.19, 0.36)]):
        bx = x0 + w * fx
        _rect(d, bx, base - h * fh, bx + w * fw, base, SLATE if i % 2 else (78, 92, 112))
        # saw-tooth roof
        for k in range(3):
            xa = bx + w * fw * k / 3.0
            _poly(d, [(xa, base - h * fh), (xa + w * fw / 3.0 * 0.55, base - h * fh - 5 * S),
                      (xa + w * fw / 3.0, base - h * fh)], SLATE)
    # the flags
    for fx in (0.16, 0.36, 0.58, 0.78):
        px = x0 + w * fx
        _ln(d, [(px, base - h * 0.44), (px, base - h * 0.62)], RUST, 1.4 * S)
        _poly(d, [(px, base - h * 0.62), (px + 7 * S, base - h * 0.57),
                  (px, base - h * 0.52)], CRIMSON)
    _rect(d, x0, base, x1, y1, (198, 188, 168))
    _num(d, x0 + 3 * S, y0 + 2 * S, "25", 13.5, CRIMSON)
    _lab(d, x0 + 13 * S, y0 + 8.4 * S, "SHUT", 6.2, SLATE)


# --- card motifs -----------------------------------------------------------
# The cards carry the same idea at half the size: one ground, three shapes, one
# figure, at most two words. Each is drawn to read as a coloured patch first and
# a diagram second, which is what survives a look at 300 pixels across.

def truce(d, x0, y0, x1, y1):
    """Two sides, and the line between them that is holding by a thread."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, NAVY)
    _rect(d, x0, y0 + h * 0.30, x0 + w * 0.30, y1 - h * 0.16, SLATE)
    _rect(d, x1 - w * 0.30, y0 + h * 0.30, x1, y1 - h * 0.16, SLATE)
    yy = y0 + h * 0.56
    x = x0 + w * 0.34
    while x < x1 - w * 0.32:
        _ln(d, [(x, yy), (x + 5 * S, yy)], CRIMSON, 2.2 * S)
        x += 9 * S
    _circ(d, x0 + w * 0.17, y0 + h * 0.42, 2.6 * S, BONE)
    _circ(d, x1 - w * 0.17, y0 + h * 0.42, 2.6 * S, BONE)
    _lab(d, x0 + 4 * S, y1 - 13 * S, "TRUCE AT RISK", 8.6, BONE)


def raid(d, x0, y0, x1, y1):
    """A compound under a crosshair, struck from the air."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, SAND)
    _rect(d, x0, y1 - h * 0.26, x1, y1, RUST)
    for fx, fw, fh in ((0.06, 0.18, 0.22), (0.30, 0.22, 0.30), (0.60, 0.17, 0.20),
                       (0.82, 0.14, 0.26)):
        bx = x0 + w * fx
        _rect(d, bx, y1 - h * 0.26 - h * fh, bx + w * fw, y1 - h * 0.26, (110, 52, 34))
    cx, cy = x0 + w * 0.44, y0 + h * 0.28
    _circ(d, cx, cy, h * 0.22, None, CRIMSON, 2.4 * S)
    _ln(d, [(cx - h * 0.30, cy), (cx + h * 0.30, cy)], CRIMSON, 2.2 * S)
    _ln(d, [(cx, cy - h * 0.30), (cx, cy + h * 0.30)], CRIMSON, 2.2 * S)
    _lab(d, x0 + 4 * S, y0 + 4 * S, "AIR RAID", 8.6, DEEP)


def border(d, x0, y0, x1, y1):
    """Two armies, one line, nothing between them."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, PLASTER)
    _rect(d, x0, y0 + h * 0.62, x1, y1, (206, 196, 174))
    _rect(d, x0 + w * 0.48, y0, x0 + w * 0.52, y1, SLATE)
    for i in range(4):
        yy = y0 + h * (0.66 + i * 0.07)
        _ln(d, [(x0 + 4 * S, yy), (x0 + w * 0.30, yy)], OLIVE, 3.0 * S)
        _ln(d, [(x0 + w * 0.70, yy), (x1 - 4 * S, yy)], RUST, 3.0 * S)
    _lab(d, x0 + 4 * S, y0 + 3 * S, "1,000 KM", 8.6, SLATE)
    _lab(d, x0 + 4 * S, y1 - 13 * S, "BORDER", 8.6, SLATE)


def stamp(d, x0, y0, x1, y1):
    """A passport page, and the stamp that voids it."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, BONE)
    _rect(d, x0, y0, x1, y0 + h * 0.16, NAVY)
    _lab(d, x0 + 4 * S, y0 + 3 * S, "SANCTIONS", 8.6, BONE)
    for i in range(3):
        yy = y0 + h * (0.30 + i * 0.10)
        _ln(d, [(x0 + 4 * S, yy), (x0 + w * 0.44, yy)], (196, 186, 164), 2.4 * S)
    cx, cy = x0 + w * 0.68, y0 + h * 0.58
    _circ(d, cx, cy, h * 0.20, None, CRIMSON, 3.0 * S)
    _ln(d, [(cx - h * 0.14, cy - h * 0.14), (cx + h * 0.14, cy + h * 0.14)], CRIMSON, 3.0 * S)
    _lab(d, x0 + 4 * S, y1 - 13 * S, "BANNED", 8.6, CRIMSON)


def verdict(d, x0, y0, x1, y1):
    """The bars, and the months added behind them."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, SLATE)
    for i in range(5):
        bx = x0 + w * (0.10 + i * 0.17)
        _rect(d, bx, y0 + h * 0.16, bx + 4.5 * S, y1 - h * 0.10, DEEP)
    _num(d, x0 + 4 * S, y1 - 22 * S, "17", 15.0, BONE)
    _lab(d, x0 + 20 * S, y1 - 13 * S, "MONTHS", 8.6, BONE)


def globe(d, x0, y0, x1, y1):
    """The planet as a target, and the year the gavel falls."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, TEAL)
    cx, cy, r = x0 + w * 0.40, y0 + h * 0.48, h * 0.27
    _circ(d, cx, cy, r, None, BONE, 2.6 * S)
    _ln(d, [(cx - r, cy), (cx + r, cy)], BONE, 2.0 * S)
    _arc(d, [cx - r * 0.55, cy - r, cx + r * 0.55, cy + r], 0, 360, BONE, 2.0 * S)
    _num(d, x1 - 30 * S, y0 + 4 * S, "31", 17.0, BONE)
    _lab(d, x0 + 4 * S, y1 - 13 * S, "FOSSIL", 8.6, BONE)
    _lab(d, x0 + 4 * S + 34 * S, y1 - 13 * S, "PHASE-OUT", 8.6, BONE)


def podium(d, x0, y0, x1, y1):
    """A lectern with nobody behind it."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, PLASTER)
    _rect(d, x0, y1 - h * 0.12, x1, y1, (206, 196, 174))
    _poly(d, [(x0 + w * 0.30, y0 + h * 0.34), (x0 + w * 0.70, y0 + h * 0.34),
              (x0 + w * 0.78, y1 - h * 0.12), (x0 + w * 0.22, y1 - h * 0.12)], NAVY)
    _ln(d, [(x0 + w * 0.50, y0 + h * 0.34), (x0 + w * 0.50, y0 + h * 0.20)], DEEP, 2.4 * S)
    _circ(d, x0 + w * 0.50, y0 + h * 0.17, 3.0 * S, DEEP)
    _lab(d, x0 + 4 * S, y0 + 3 * S, "RESIGNS", 8.6, CRIMSON)


def atoll(d, x0, y0, x1, y1):
    """A ring of islands, and the flag that still flies over them."""
    w, h = x1 - x0, y1 - y0
    _rect(d, x0, y0, x1, y1, SKY)
    _rect(d, x0, y0 + h * 0.52, x1, y1, (86, 132, 156))
    cx, cy = x0 + w * 0.44, y0 + h * 0.54
    for i in range(7):
        a = -0.4 + i * 0.55
        import math
        px = cx + math.cos(a) * w * 0.26
        py = cy + math.sin(a) * h * 0.20
        _circ(d, px, py, 2.6 * S, OLIVE)
    _ln(d, [(x1 - 26 * S, y0 + 6 * S), (x1 - 26 * S, y0 + h * 0.42)], DEEP, 1.8 * S)
    _rect(d, x1 - 26 * S, y0 + 6 * S, x1 - 8 * S, y0 + 15 * S, CRIMSON)
    _lab(d, x0 + 4 * S, y1 - 13 * S, "CHAGOS", 8.6, BONE)


MOTIFS = {
    "gulf": gulf, "swarm": swarm, "summit": summit, "cyclone": cyclone,
    "inflation": inflation, "vote": vote, "sudan": sudan, "space": space,
    "factories": factories, "truce": truce, "raid": raid, "border": border,
    "stamp": stamp, "verdict": verdict, "globe": globe, "podium": podium,
    "atoll": atoll,
}


def draw(d, box, key):
    """Draw motif `key` into box=(x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    fn = MOTIFS.get(key)
    if fn is None:
        _rect(d, x0, y0, x1, y1, SLATE)
        return
    _PANEL[:] = [x0, y0, x1, y1]
    fn(d, x0, y0, x1, y1)
    d.rectangle([round(x0), round(y0), round(x1), round(y1)], outline=(30, 26, 22), width=1 * S)
