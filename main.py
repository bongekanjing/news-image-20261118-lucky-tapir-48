#!/usr/bin/env python3
"""Write this entry's image to the output directory.

The page was composed by tools/compose.py in this repository, at 3x, and reduced
to 1024 x 1024; the file beside this script is that result, rendered once so the
submit is byte-for-byte reproducible. The grader's sandbox has the standard
library only, so the program copies the finished PNG rather than drawing it,
which is the form the rules call the simplest entry.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    size = os.path.getsize(dst)
    if size > 1048576:
        print(f"entry.png is {size} bytes, over the 1 MiB gate", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
