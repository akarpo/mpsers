# mpsers

**Live:** <https://mpsers.karpowitsch.org>

An independent, source-linked check of the Governor's Nov. 17, 2026 announcement that
Michigan's school pension (MPSERS) is "fully funded ahead of schedule." It goes claim by claim
and also covers what the pooled State of Michigan Retirement Systems fund holds.

## Layout

| Path | What it is |
|---|---|
| `public/` | The site. This is the **only** folder Cloudflare Pages deploys (build output dir = `public`, no build command). |
| `public/index.html` | The single page: inline CSS and JS, no external libraries. |
| `public/assets/smrs-13f-2026q3.csv` | All 966 holdings from the Q3 2026 SEC 13F. Generated; don't edit. |
| `public/assets/share.png` | Social share image, 1200×630. |
| `sources/` | Copies of every source document as downloaded on 2026-11-18. Not deployed. |
| `tools/build_13f.py` | Rebuilds the CSV from `sources/` and rewrites the top-10 block in `index.html` between `/*TOP10:BEGIN*/` and `/*TOP10:END*/`. |
| `docs/FIGURES.md` | Every figure on the page, with its source document and page. |

## Rules for changes

- Every number on the page appears in `docs/FIGURES.md` with a source. Add the row before
  publishing a new figure.
- The top-10 holdings come from the 13F via `python -I tools/build_13f.py`. Never type them by
  hand: hand-typed values drifted from the filing on the first draft.
- Estimates are ours and must stay labeled as estimates (the "back-of-envelope" block).
- After any edit, render the page at 1280 px and 390 px, in light and dark mode, and check it for
  label collisions and horizontal overflow.

## Hosting

Cloudflare Pages project `mpsers`, Git-connected to `akarpo/mpsers` (`main`), with the custom
domain `mpsers.karpowitsch.org`. A push to `main` deploys.
