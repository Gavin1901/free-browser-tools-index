"""Scrape Google Search Console metrics for the 8 AI outbound sites via an existing Chrome CDP session.

Why this exists:
- The GSC UI text can be mojibake in this Windows automation environment.
- Older scripts used fragile Chinese regex and failed with `nothing to repeat`.
- This script uses stable URL routes and minimal label anchors, then records raw text for audit.

Requirements:
- GavinBuilds Chrome must be running on CDP port 9223.
- GSC account should be available at /u/1.
"""
import argparse
import asyncio
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright

SITES = [
    "iworkviewer.com",
    "livephotokit.com",
    "plantingcalendar.net",
    "freetdee.com",
    "babypercent.com",
    "invoicepad.net",
    "zoneplan.net",
    "pupvax.com",
]

# Mojibake-safe enough anchors seen in GSC Chinese UI under this environment.
ANCHORS = {
    "clicks": ["鎬荤偣", "点"],
    "impressions": ["鎬绘洕", "曝光"],
    "ctr": ["鐐瑰嚮鐜", "点击率", "CTR"],
    "position": ["鎺掑悕", "排名"],
}


def next_number_after_anchor(text: str, anchors: list[str], percent: bool = False):
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    for i, line in enumerate(lines):
        if any(a in line for a in anchors):
            window = lines[i + 1 : i + 8]
            for w in window:
                if percent:
                    m = re.search(r"-?\d+(?:\.\d+)?%", w)
                else:
                    m = re.search(r"-?\d+(?:\.\d+)?", w.replace(",", ""))
                if m:
                    val = m.group(0)
                    if percent:
                        return val
                    return float(val) if "." in val else int(val)
    return None


def parse_index_counts(text: str):
    # Examples observed after mojibake:
    # "32 涓綉椤垫湭缂栧叆绱㈠紩"
    # "8 涓綉椤靛凡缂栧叆绱㈠紩"
    not_indexed = None
    indexed = None
    for line in [x.strip() for x in text.splitlines() if x.strip()]:
        m = re.search(r"(\d+)", line)
        if not m:
            continue
        n = int(m.group(1))
        if "湭缂" in line or "未编" in line or ("未" in line and "索引" in line):
            not_indexed = n
        elif "凡缂" in line or "已编" in line or ("已" in line and "索引" in line):
            indexed = n
    return indexed, not_indexed


def parse_performance(text: str):
    return {
        "clicks": next_number_after_anchor(text, ANCHORS["clicks"]),
        "impressions": next_number_after_anchor(text, ANCHORS["impressions"]),
        "ctr": next_number_after_anchor(text, ANCHORS["ctr"], percent=True),
        "position": next_number_after_anchor(text, ANCHORS["position"]),
    }


async def fetch_text(page, url: str, wait_ms: int):
    await page.goto(url, wait_until="domcontentloaded", timeout=45_000)
    await page.wait_for_timeout(wait_ms)
    text = await page.locator("body").inner_text(timeout=10_000)
    return {"url": page.url, "title": await page.title(), "text": text}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    ap.add_argument("--port", default="9223")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--wait-ms", type=int, default=10000)
    args = ap.parse_args()

    base = Path(args.outdir)
    (base / "logs").mkdir(exist_ok=True)
    (base / "daily").mkdir(exist_ok=True)

    version = json.load(urllib.request.urlopen(f"http://127.0.0.1:{args.port}/json/version"))
    endpoint = version["webSocketDebuggerUrl"]

    results = []
    raw = []
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()
        for site in SITES:
            prop = f"sc-domain:{site}"
            perf_url = f"https://search.google.com/u/1/search-console/performance/search-analytics?resource_id={prop}&num_of_days=28"
            overview_url = f"https://search.google.com/u/1/search-console?resource_id={prop}"
            rec = {"site": site, "property": prop, "ok": False}
            try:
                perf = await fetch_text(page, perf_url, args.wait_ms)
                overview = await fetch_text(page, overview_url, args.wait_ms)
                metrics = parse_performance(perf["text"])
                indexed, not_indexed = parse_index_counts(overview["text"])
                rec.update(metrics)
                rec.update({
                    "indexed": indexed,
                    "not_indexed": not_indexed,
                    "performance_url": perf["url"],
                    "overview_url": overview["url"],
                    "performance_title": perf["title"],
                    "overview_title": overview["title"],
                    "ok": all(metrics.get(k) is not None for k in ["clicks", "impressions", "ctr", "position"]),
                    "index_ok": indexed is not None or not_indexed is not None,
                })
                raw.append({"site": site, "performance_text": perf["text"], "overview_text": overview["text"]})
            except Exception as e:
                rec.update({"error": str(e)})
            results.append(rec)
        await page.close()

    raw_path = base / "logs" / f"{args.date}-gsc-8sites-raw.json"
    json_path = base / "logs" / f"{args.date}-gsc-8sites-metrics.json"
    md_path = base / "daily" / f"{args.date}-gsc-8sites-metrics.md"
    raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [f"# {args.date} GSC 8-site metrics", "", "Source: Google Search Console /u/1 via GavinBuilds Chrome CDP 9223.", ""]
    lines.append("| Site | Clicks | Impressions | CTR | Avg position | Indexed | Not indexed | Status |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---|")
    for r in results:
        status = "PASS" if r.get("ok") else "PARTIAL"
        lines.append(
            f"| {r['site']} | {r.get('clicks')} | {r.get('impressions')} | {r.get('ctr')} | {r.get('position')} | {r.get('indexed')} | {r.get('not_indexed')} | {status} |"
        )
    lines += ["", "## Evidence", "", f"- JSON: logs/{args.date}-gsc-8sites-metrics.json", f"- Raw text: logs/{args.date}-gsc-8sites-raw.json"]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path), "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())


