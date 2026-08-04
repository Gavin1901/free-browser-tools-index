"""Verify Product Hunt post content and links"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

def cdp():
    with urllib.request.urlopen('http://127.0.0.1:9223/json/version', timeout=10) as r:
        return json.load(r)['webSocketDebuggerUrl']

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp())
        ctx = browser.contexts[0]
        page = await ctx.new_page()

        url = 'https://www.producthunt.com/p/self-promotion/zoneplan-worldwide-meeting-planner-hit-258-impressions-for-one-query'
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(3000)
        print(f'URL: {page.url}')

        # Check HTTP status is good (not 404)
        if 'self-promotion' in page.url:
            # Find ZonePlan links
            links = await page.evaluate("""
            JSON.stringify(
                [...document.querySelectorAll('a')]
                    .filter(a => a.href && a.href.includes('zoneplan.net'))
                    .map(a => ({href: a.href, visible: a.offsetParent !== null, text: a.textContent?.substring(0, 30)}))
            )
            """)
            print(f'ZonePlan links: {links}')

            # Get page title
            title = await page.title()
            print(f'Title: {title}')

            body = await page.evaluate("document.body.innerText.substring(0, 300)")
            print(f'Body preview: {body}')
        else:
            print('Not a self-promotion page - may be 404 or redirect')

asyncio.run(main())
