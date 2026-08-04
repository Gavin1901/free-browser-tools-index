"""Verify Pinterest pins via CDP - check destination links"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

PINS = [
    {"url": "https://www.pinterest.com/pin/1097893215437701412/", "expected": "zoneplan.net", "site": "ZonePlan"},
    {"url": "https://www.pinterest.com/pin/1097893215437701390/", "expected": "pupvax.com", "site": "PupVax"},
]

def cdp_endpoint(port="9223"):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=10) as r:
        return json.load(r)["webSocketDebuggerUrl"]

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(cdp_endpoint("9223"))
        context = browser.contexts[0]

        for pin in PINS:
            page = await context.new_page()
            await page.goto(pin["url"], wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)

            # Get all links on the pin page
            links = await page.evaluate(f"""
            (() => {{
                const allLinks = [...document.querySelectorAll('a')];
                const targetLinks = allLinks.filter(a =>
                    a.href && a.href.includes('{pin['expected']}')
                );
                return JSON.stringify(targetLinks.map(a => ({{
                    href: a.href,
                    text: a.textContent?.substring(0, 60),
                    visible: a.offsetParent !== null
                }})));
            }})()
            """)

            title = await page.title()
            url = page.url

            print(f"=== {pin['site']} ===")
            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"Target links: {links}")

            # HTTP status via evaluate
            http_ok = await page.evaluate("document.readyState === 'complete'")
            print(f"Page loaded: {http_ok}")

            await page.close()

asyncio.run(main())
