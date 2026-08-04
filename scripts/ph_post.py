"""Post to Product Hunt Self-Promotion via Playwright CDP"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

TITLE = "ZonePlan: Worldwide Meeting Planner Hit 258 Impressions for One Query"
BODY = """I built ZonePlan (zoneplan.net) as a free worldwide meeting planner. One query just crossed 258 Google impressions in 28 days.

The problem: worldwide meetings spanning Asia+Europe+Americas have conflicting DST transitions. ZonePlan shows a visual overlap grid of 24 hours across all selected time zones.

GSC data: 4350 impressions, 5 clicks, 30 indexed (up from 4 last week). Top query "meeting planner worldwide" at 258 impressions.

Try it: https://zoneplan.net (free, no sign-up, no installation)

Would love feedback from anyone building SEO-first tools."""

def cdp():
    with urllib.request.urlopen('http://127.0.0.1:9223/json/version', timeout=10) as r:
        return json.load(r)['webSocketDebuggerUrl']

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp())
        ctx = browser.contexts[0]
        page = await ctx.new_page()

        # Directly go to new thread with self-promotion category
        await page.goto('https://www.producthunt.com/p/new?category=self-promotion', wait_until='domcontentloaded', timeout=45000)
        await page.wait_for_timeout(5000)
        print(f'URL: {page.url}')

        # Check what's on the page
        body_text_preview = await page.evaluate("document.body.innerText.substring(0, 200)")
        print(f'Body: {body_text_preview}')

        # Look for title input
        title_el = page.locator('input[name="title"], input[placeholder*="title" i], #thread_title, [data-test="thread-title"]').first
        body_el = page.locator('textarea[name="body"], textarea[placeholder*="text" i], #thread_body, [data-test="thread-body"]').first

        title_count = await title_el.count()
        body_count = await body_el.count()
        print(f'Title fields: {title_count}, Body fields: {body_count}')

        if title_count > 0:
            await title_el.click()
            await page.keyboard.type(TITLE, delay=5)
            await page.wait_for_timeout(1000)
            print('Title typed')

        if body_count > 0:
            await body_el.click()
            await page.keyboard.type(BODY, delay=3)
            await page.wait_for_timeout(1000)
            print('Body typed')

        # Look for submit button
        submit = page.locator('button[type="submit"], button:has-text("Submit"), button:has-text("Post"), button:has-text("Create thread"), button:has-text("Publish")').first
        if await submit.count() > 0 and await submit.is_visible():
            await submit.click()
            print(f'Submit clicked: {await submit.text_content()}')
            await page.wait_for_timeout(10000)

        final_url = page.url
        print(f'Final URL: {final_url}')

        if 'self-promotion' in final_url and final_url != 'https://www.producthunt.com/p/self-promotion':
            print(f'POSTED! URL: {final_url}')
        else:
            print(f'Page body: {await page.evaluate("document.body.innerText.substring(0, 200)")}')

asyncio.run(main())
