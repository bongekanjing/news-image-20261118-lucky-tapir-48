#!/usr/bin/env python3
"""Check a rendered page for the defects a gate or a reader would catch.

Detects: wrong size, ink at the trim, the largest blank horizontal band, the
widest blank column strip, and ink coverage. Prints one line per check so the
numbers, not an impression, decide whether the page is finished.

Pure Pillow: no numpy on this machine.
"""

import sys
from PIL import Image, ImageChops

PAPER = (246, 242, 231)


def load(path):
    return Image.open(path).convert("RGB")


def ink_mask(im):
    """1-bit mask of everything meaningfully darker than the paper."""
    bg = Image.new("RGB", im.size, PAPER)
    diff = ImageChops.difference(im, bg).convert("L")
    return diff.point(lambda v: 255 if v > 12 else 0, mode="L")


def runs(flags):
    out, start = [], None
    for i, v in enumerate(flags):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i - start))
            start = None
    if start is not None:
        out.append((start, len(flags) - start))
    return out


def main(path):
    im = load(path)
    w, h = im.size
    m = ink_mask(im)
    px = m.load()
    ok = True

    print(f"size {w}x{h}", "PASS" if (w, h) == (1024, 1024) else "FAIL")
    ok &= (w, h) == (1024, 1024)

    hist = m.histogram()
    ink = hist[255] if len(hist) > 255 else 0
    cov = ink / (w * h)
    print(f"ink coverage {cov*100:.2f}%", "PASS" if 0.10 < cov < 0.45 else "FAIL")
    ok &= 0.10 < cov < 0.45

    edge = 0
    for x in range(2):
        for y in range(h):
            edge += 1 if px[x, y] or px[w - 1 - x, y] else 0
    for y in range(2):
        for x in range(w):
            edge += 1 if px[x, y] or px[x, h - 1 - y] else 0
    print(f"ink within 2px of trim: {edge}", "PASS" if edge == 0 else "WARN")

    colink = [False] * w
    rowink = [False] * h
    for y in range(h):
        for x in range(w):
            if px[x, y]:
                rowink[y] = True
                colink[x] = True
    xs = [i for i, v in enumerate(colink) if v]
    ys = [i for i, v in enumerate(rowink) if v]
    print(f"ink box x {xs[0]}..{xs[-1]}  y {ys[0]}..{ys[-1]}",
          "PASS" if xs[0] >= 10 and xs[-1] <= w - 11 else "FAIL")
    ok &= xs[0] >= 10 and xs[-1] <= w - 11

    bands = [(s, n) for s, n in runs([not v for v in rowink]) if 2 < s < h - 2]
    big = sorted(bands, key=lambda t: -t[1])[:4]
    print("largest blank bands (y, px):", big)
    worst = big[0][1] if big else 0
    print("largest blank band", worst, "PASS" if worst <= 30 else "FAIL")
    ok &= worst <= 30

    gaps = [(s, n) for s, n in runs([not v for v in colink]) if 10 < s < w - 10]
    widest = max((n for _, n in gaps), default=0)
    print("widest blank column strip", widest,
          "PASS" if widest <= 26 else "WARN")

    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "out/entry.png"))
