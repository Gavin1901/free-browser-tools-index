import asyncio
import json
import sys
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


def endpoint():
    with urllib.request.urlopen("http://127.0.0.1:9223/json/version", timeout=10) as r:
        return json.load(r)["webSocketDebuggerUrl"]


async def main():
    sys.stdout.reconfigure(encoding="utf-8")
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint())
        context = browser.contexts[0]
        page = await context.new_page()
        for site in SITES:
            url = (
                "https://search.google.com/u/1/search-console/sitemaps"
                f"?resource_id=sc-domain:{site}"
            )
            rec = {"site": site, "url": url, "ok": False}
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=45_000)
                await page.wait_for_timeout(5_000)
                field = page.locator('input[aria-label="输入站点地图网址"]')
                if await field.count() != 1:
                    rec["error"] = "sitemap input not found"
                else:
                    await field.fill("sitemap.xml")
                    await page.get_by_text("提交", exact=True).click()
                    await page.wait_for_timeout(5_000)
                    text = await page.locator("body").inner_text()
                    rec["body_tail"] = text[-2500:]
                    rec["ok"] = (
                        "成功" in text
                        or "已成功提交站点地图" in text
                        or "站点地图已提交" in text
                    )
                    rec["visible_success"] = "成功" in text
                    rec["visible_sitemap"] = f"https://{site}/sitemap.xml" in text
            except Exception as e:
                rec["error"] = str(e)
            print(site, rec["ok"], rec.get("error", ""))
            results.append(rec)
        await page.close()
    date = datetime.now().strftime("%Y-%m-%d")
    path = Path(r"D:\Tools\ai-tool-index\logs") / f"{date}-gsc-sitemap-resubmission.json"
    path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    asyncio.run(main())
