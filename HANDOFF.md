# Handoff: start here

Last updated **2026-11-18**. The site is live and finished; nothing was left half-done. The local
working copy was deleted after everything was pushed, so GitHub is the only copy.

## Pick up in five steps

1. `gh repo clone akarpo/mpsers` and `cd mpsers`.
2. Read `README.md` (layout, rules, corrections log, the dates when numbers change), then
   `docs/FIGURES.md` (every figure on the page with its source and page), then
   `docs/TSD-FINDINGS.md` (the Troy research notes).
3. `pip install playwright pymupdf` if they're missing, then `python -I tools/qa.py` to render the
   page at 1280/390 px in light and dark mode (screenshots land in `qa-out/`, which is git-ignored).
4. Edit `public/index.html` (and add the `docs/FIGURES.md` row first for any new number). Run
   `python -I tools/qa.py` again and look at the screenshots.
5. Commit and push to `main`. Cloudflare Pages deploys in about a minute. Confirm with
   `python -I tools/cloudflare.py status` (needs `CF_CRED_FILE`, see below) and
   `python -I tools/qa.py --live --links`.

## What the site says (as of 2026-11-18)

- **The claim:** the Governor's Nov. 17, 2026 release says MPSERS is "fully funded ahead of
  schedule." The page checks it claim by claim against the valuations, the ACFR, the SMIB
  presentation and the SEC 13F, and shows what the pooled fund holds (top 10 generated from the
  Q3 2026 13F by `tools/build_13f.py`).
- **The $3.2B** state payment is the floored UAAL payment set in law, not an overstatement (an
  early draft got this wrong; see `docs/FIGURES.md`).
- **Troy School District:** the UAAL ("debt") part of Troy's MPSERS bill is capped at 15.21% of
  payroll, about **$14.8M a year** on FY2026 payroll, and it ends at payoff *if* the state lets
  districts keep the savings. Troy's MPSERS cost after the state's offsetting payments **rose from
  22.0% to 23.1% of payroll (about $2.0M) from FY2025 to FY2026**, from MDE's State Aid Financial
  Status Reports (the "147a filing"). Offsets table is on the page under `#offsets`.
- **Questions:** "For the state" and "For Troy School District's business office", addressed to
  Dan Trudel, CPA, Assistant Superintendent for Business Services (name and title verified in his
  June 20, 2024 appointment and the FY2026 audit transmittal).

## History of the work (all on 2026-11-18)

Built the fact-check; moved from `mpsers.` to `tsd-mpsers.karpowitsch.org` at the owner's request;
added the Troy section and the questions for the business office; added the Troy share card
(`public/assets/share-troy.png`); found the Section 147a payments in MDE's status reports and
added the offsets table; corrected the Troy net-cost figure twice (both corrections are visible on
the page and in the README's corrections log); ran an independent fact-check of about 330 claims
and fixed the 18 items it found; added `tools/qa.py` and `tools/cloudflare.py` at hand-off.

## Open items and watch list

- **No answers yet** to the questions on the page. When the state or Troy answers, replace the
  question with the answer and a link, and add a `docs/FIGURES.md` row.
- **Dated updates:** the README's "When the numbers will change" table (SMIB meeting Dec. 16, 2026;
  Q4 2026 13F by mid-Feb. 2027; MPSERS FY2026 ACFR about Feb. 2027; the 9/30/2026 valuation about
  Mar. 2027; the FY2028 school aid budget; Troy's budget amendments and FY2027 audit).
- **Checked online only, no copy in `sources/`:** the MARSP "on track to pay off all pension debt by
  2035" quote (July 21, 2026), the Bridge Michigan headline, the SMIB Dec. 16, 2026 meeting date,
  and the 13F cover-page totals (966 securities, $22,595,236,086). Re-open those pages if any of
  them is questioned.
- **Still unclear:** whether "2030" in the release is the last payment or a valuation date (rates
  lag valuations by about three years; `docs/TSD-FINDINGS.md` works through both readings).
- **Not pulled:** 147a(1), 147a(2) and 147g amounts before FY2025. The same MDE archive goes back to
  2000 if a longer trend is wanted.
- **Not done, only offered:** a link between this site and the sibling site
  <https://tsd-section35.karpowitsch.org> (repo `akarpo/tsd-section35`).

## Pitfalls already hit (don't repeat them)

- **Which state payments reduce Troy's cost:** 147a(1), 147a(2), 147a(4), 147e and 27l(4) offset the
  district's cost. 147c(1)/(2) pass straight through to ORS. **147g passed through to employees**
  (Plante Moran FY2025 management letter, p. 10), so it is not an offset. Counting it caused the
  second correction. Get an independent check of any recalculation before publishing.
- **MDE status-report PDFs scramble their columns** in pdftotext. Render the page (PyMuPDF
  `get_pixmap`) and read the image before quoting an amount.
- The "budget books" in Troy board packets are **Oakland Schools'** budgets, not Troy's.
- **Everything in `public/` is deployed.** Keep scratch output elsewhere (a stray `links.txt` was
  published once). `qa-out/` is git-ignored for that reason.
- A changed share card needs a **new file name** (and updated `og:image`/`twitter:image`) or link
  previews keep the old one. `python -I tools/qa.py --card public/assets/<new-name>.png` renders it.
- **Never run `wrangler pages deploy`**; it shadows the Git-connected deployment.
- sec.gov refuses scripted requests that lack a contact User-Agent; `tools/qa.py` lists that link as
  "check in a browser" rather than sending anyone's contact details.
- If someone can't reach the site, check the spelling first (`tsd-mpsers`, not `tsd-mspers`).

## Credentials

Cloudflare API credentials are never in this repo. `tools/cloudflare.py` reads the text file named
by the `CF_CRED_FILE` environment variable (labeled lines "Cloudflare Pages/DNS token",
"Cloudflare account", "karpowitsch.org zone"). The site owner keeps that file. Never print or
commit its values. Day-to-day work doesn't need it: a push to `main` deploys.
