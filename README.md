# news-image-20261118-lucky-tapir-48

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/bongekanjing/news-image-20261118-lucky-tapir-48/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/bongekanjing/news-image-20261118-lucky-tapir-48/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One front page for Wednesday 18 November 2026, drawn as a broadsheet: a masthead
that is the date itself, a lead package on the Iranian drone salvo at Kuwait and
Bahrain, a rail of three second-billed stories, fourteen filed cards across seven
regions and eight fields, twenty-eight wire briefs, and a strip of the day's
figures. Every claim on the page is the one the named wire carried; nothing is
illustrated or invented.

The page is set entirely in type — flat fills, hairlines and letterforms, no
photographs and no gradients — so nothing can smear at the 1024 x 1024 the gate
accepts. It is composed at 3x and reduced once with Lanczos, which is what gives
the small type its clean edges.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## How the page is made

`tools/compose.py` solves the layout rather than guessing it: each band is drawn
off to the side to measure itself, then the copy is scaled so the band closes
exactly on the height the page budgeted for it, and the wire columns grow their
leading into whatever space is left. That is why there is no hole anywhere on the
sheet and no block ever overlaps its neighbour.

- `tools/paper.py` — the palette, the four faces, and the measuring helpers.
- `tools/layout.py` — the grid, the story card, the rule head.
- `tools/copy.py` — the day's copy, with the source for every story.
- `tools/check.py` — the defects a gate or a reader would catch: trim, blank bands,
  ink coverage.
- `tools/render.py`, `tools/map.py` — earlier passes, kept because the history of
  the page is the reason it is shaped this way.

To rebuild the image from the copy:

```sh
cd tools && python3 compose.py ../entry.png && python3 check.py ../entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
