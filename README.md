# mpsers

**Live:** <https://tsd-mpsers.karpowitsch.org>

An independent, source-linked check of the Governor's Nov. 17, 2026 announcement that
Michigan's school pension (MPSERS) is "fully funded ahead of schedule." It goes claim by claim,
covers what the pooled State of Michigan Retirement Systems fund holds, and works out what payoff
would mean for Troy School District's budget, with questions for the state and for Troy's
business office.

**Picking this up in a new session? Start with [`HANDOFF.md`](HANDOFF.md)**: current state, open
items, and the mistakes not to repeat.

## Layout

| Path | What it is |
|---|---|
| `public/` | The site. This is the **only** folder Cloudflare Pages deploys (build output dir = `public`, no build command). |
| `public/index.html` | The single page: inline CSS and JS, no external libraries. |
| `public/404.html` | Not-found page. Without it, Pages answers every unknown path with the home page and a 200. |
| `public/_headers` | Security headers. The CSP allows Cloudflare Web Analytics, which the karpowitsch.org zone injects. |
| `public/assets/smrs-13f-2026q3.csv` | All 966 holdings from the Q3 2026 SEC 13F. Generated; don't edit. |
| `public/assets/share-troy.png` | Social share image, 1200×630, rendered from `tools/share-card.html`. |
| `sources/` | Copies of every statewide source document as downloaded on 2026-11-18. Not deployed. |
| `sources/troy/` | Troy School District audits, management letter, budget presentations and forecasts, plus Troy's pages from MDE's State Aid Financial Status Reports. Not deployed. |
| `tools/build_13f.py` | Rebuilds the CSV from `sources/` and rewrites the top-10 block in `index.html` between `/*TOP10:BEGIN*/` and `/*TOP10:END*/`. Run `python -I tools/build_13f.py`. |
| `tools/share-card.html` | Source of the share image. Render it with `python -I tools/qa.py --card public/assets/<new-name>.png`. |
| `tools/qa.py` | Renders the page at 1280/390 px, light and dark, into `qa-out/` (git-ignored) and checks overflow, console errors, anchors and heading order. `--live` checks the live site, its 404 page, share image and analytics; `--links` requests every external link. |
| `tools/cloudflare.py` | Cloudflare Pages status (`status`, `check`) and the one-time setup (`create`, `domain`). Reads credentials from the file named by `CF_CRED_FILE`; never prints them. |
| `HANDOFF.md` | Where things stand and how to pick the work back up. |
| `docs/FIGURES.md` | Every figure on the page, with its source document and page. Superseded figures stay listed and marked. |
| `docs/TSD-FINDINGS.md` | The full Troy research notes: by-year tables back to 2010, every quote, 36 cited board documents. |

## Rules for changes

- Every number on the page appears in `docs/FIGURES.md` with a source. Add the row before
  publishing a new figure.
- The top-10 holdings come from the 13F via the script. Never type them by hand: hand-typed values
  drifted from the filing on the first draft.
- Estimates and calculations are ours and stay labeled ("our calculation", "back-of-envelope").
- Quote whole clauses. A shortened quote must not drop a reason the source gives (see the
  $3,612,635 note, which first lost "actual attrition").
- When the page names a person, confirm the name and title in a primary source and cite it.
- Corrections stay visible: a dated note on the page, and a "Superseded" row in `docs/FIGURES.md`.
- After any edit, run `python -I tools/qa.py` (1280 px and 390 px, light and dark) and look at the
  screenshots for label collisions; the script catches heading order and horizontal overflow.
- If the share card changes, give the image a new file name so cached link previews refresh.

## Corrections

- **2026-11-18:** Troy's net MPSERS cost after state offsets was first shown as flat (27.24% →
  27.27% of payroll); it subtracted only some of the state's offsets. A first correction, using MDE's
  State Aid Financial Status Reports, showed 20.2% → 23.1% (+$3.7M) but counted Section 147g, which
  districts had to pass on to employees. Corrected again: 22.0% → 23.1%, about $2.0M more. The page
  carries a dated note.
- **2026-11-18, independent fact-check pass:** fixed a quote stitched from two paragraphs of the
  release; added the $300M/$200M/$425M extra deposits; "2038" is the funding-policy deadline, not
  "law"; returns trail peers over 3 years; "nearly half" includes hedge funds; PA 127's retiree-health
  changes stated exactly; Troy's $12M target is a proposal to the board; 2-year (not 3) timing shift;
  "$14.8M" in the Troy heading; market-value estimate "just under 89%".

## When the numbers will change

| Expected | What to update |
|---|---|
| SMIB meeting, Dec. 16, 2026 | Official FY2026 (to 9/30/2026) returns: the returns table and the "14%" claim card. |
| SEC 13F for Q4 2026 (due by mid-Feb. 2027) | Download the new information table into `sources/`, point `tools/build_13f.py` at it, rerun. |
| MPSERS valuation as of 9/30/2026 (about March 2027) | Funded ratio, UAAL, the funded-status chart, the computed FY2029 contribution. |
| MPSERS FY2026 ACFR (about Feb. 2027) | Funding-progress schedule, top holdings, net position. |
| State School Aid budget for FY2028 | Whether districts keep the UAAL savings; the 15.21% cap; 147a/147c/147g lines. |
| Troy budget amendments and the FY2027 audit | The Troy section's bill table, forecasts and fund balance. MDE status reports are at `https://mdoe.state.mi.us/samspublic/Home/StatusArchiveReport` (final report per year: `ALL<yy>11.pdf`; Troy is district 63150). |

## Hosting

Cloudflare Pages project `tsd-mpsers`, Git-connected to `akarpo/mpsers` (`main`), with the custom
domain `tsd-mpsers.karpowitsch.org` (proxied CNAME to `tsd-mpsers.pages.dev`). A push to `main`
deploys. Never run `wrangler pages deploy`: it creates a Direct Upload deployment that shadows the
Git one. After a push, `python -I tools/cloudflare.py status` shows whether the build succeeded and
`python -I tools/qa.py --live` checks the result.
