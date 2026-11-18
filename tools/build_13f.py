"""Build public/assets/smrs-13f-2026q3.csv from the SEC 13F information table.

Source: State of Michigan Retirement System, CIK 762152, 13F-HR for the quarter
ended 2026-09-30 (accession 0000762152-26-000017, filed 2026-10-27), saved in
sources/. Rows are combined by CUSIP + class, so a security reported across
several managers counts once.

Run from the repo root:  python -I tools/build_13f.py
"""
import csv
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "SEC-13F-2026Q3-InformationTable.xml"
PRIOR = ROOT / "sources" / "SEC-13F-2025Q3-InformationTable.xml"
OUT = ROOT / "public" / "assets" / "smrs-13f-2026q3.csv"


def load(path):
    root = ET.parse(path).getroot()
    ns = {"n": root.tag.split("}")[0].strip("{")}
    agg = defaultdict(lambda: {"value": 0.0, "shares": 0.0, "name": "", "cls": "", "type": ""})
    for it in root.findall("n:infoTable", ns):
        def g(tag):
            el = it.find("n:" + tag, ns)
            return (el.text or "").strip() if el is not None else ""
        key = (g("cusip"), g("titleOfClass"))
        a = agg[key]
        a["value"] += float(g("value") or 0)
        sh = it.find("n:shrsOrPrnAmt/n:sshPrnamt", ns)
        ty = it.find("n:shrsOrPrnAmt/n:sshPrnamtType", ns)
        a["shares"] += float(sh.text) if sh is not None else 0
        a["type"] = ty.text if ty is not None else ""
        a["name"], a["cls"] = g("nameOfIssuer"), g("titleOfClass")
    return agg


PAGE = ROOT / "public" / "index.html"
MARK_A, MARK_B = "/*TOP10:BEGIN*/", "/*TOP10:END*/"
MERGE_CLASSES = {"ALPHABET INC"}  # show share classes of these issuers as one holding
DISPLAY = {  # issuer (+ class) -> name shown on the page; a new top-10 entry must be named here
    ("NVIDIA CORPORATION", ""): "Nvidia",
    ("APPLE INC", ""): "Apple",
    ("ALPHABET INC", ""): ("Alphabet", "(A and C shares)"),
    ("MICROSOFT CORP", ""): "Microsoft",
    ("AMAZON COM INC", ""): "Amazon",
    ("BROADCOM INC", ""): "Broadcom",
    ("META PLATFORMS INC", ""): "Meta Platforms",
    ("ADVANCED MICRO DEVICES INC", ""): "Advanced Micro Devices",
    ("ISHARES TR", "MSCI USA MMENTM"): "iShares MSCI USA Momentum Factor ETF",
    ("MICRON TECHNOLOGY INC", ""): "Micron Technology",
}


def top10(cur, total):
    grouped = defaultdict(float)
    for (cusip, cls), a in cur.items():
        key = (a["name"], "") if a["name"] in MERGE_CLASSES else (a["name"], a["cls"])
        grouped[key] += a["value"]
    out = []
    for (name, cls), value in sorted(grouped.items(), key=lambda kv: -kv[1])[:10]:
        disp = DISPLAY.get((name, cls)) or DISPLAY.get((name, ""))
        if disp is None:
            raise SystemExit(f"No display name for top-10 holding {name!r} / {cls!r}: add it to DISPLAY")
        label, note = disp if isinstance(disp, tuple) else (disp, "")
        out.append({"name": label, "note": note, "v": round(value / 1e6, 1), "s": round(value / total * 100, 2)})
    return out


def patch_page(rows):
    js = "var top=[" + ",".join(
        "{name:%s,%sv:%.1f,s:%.2f}" % (repr(r["name"]), ("note:%s," % repr(r["note"])) if r["note"] else "", r["v"], r["s"])
        for r in rows) + "];"
    html = PAGE.read_text(encoding="utf-8")
    a, b = html.index(MARK_A) + len(MARK_A), html.index(MARK_B)
    PAGE.write_text(html[:a] + js + html[b:], encoding="utf-8", newline="\n")
    return js


def main():
    cur, prev = load(SRC), load(PRIOR)
    total = sum(a["value"] for a in cur.values())
    rows = sorted(cur.items(), key=lambda kv: -kv[1]["value"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "issuer", "class", "cusip", "value_usd", "shares_or_principal",
                    "type", "pct_of_13f_total", "shares_a_year_earlier"])
        for i, ((cusip, cls), a) in enumerate(rows, 1):
            p = prev.get((cusip, cls))
            w.writerow([i, a["name"], a["cls"], cusip, round(a["value"]), round(a["shares"]),
                        a["type"], f"{a['value'] / total * 100:.3f}",
                        round(p["shares"]) if p else ""])
    print(f"{len(rows)} securities, total ${total / 1e9:,.2f}B -> {OUT.relative_to(ROOT)}")
    print("page top-10 ->", patch_page(top10(cur, total)))
    for i, ((cusip, cls), a) in enumerate(rows[:15], 1):
        print(f"{i:2} {a['name'][:34]:34} {a['cls'][:22]:22} ${a['value'] / 1e6:8,.0f}M {a['value'] / total * 100:5.2f}%")


if __name__ == "__main__":
    sys.exit(main())
