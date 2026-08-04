"""Check Pinterest pin state and try to complete publishing"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

def cdp_endpoint(port="9223"):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=10) as r:
        return json.load(r)["webSocketDebuggerUrl"]

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(cdp_endpoint("9223"))
        context = browser.contexts[0]

        # Check current pages
        for page in context.pages:
            print(f"Page: {page.url[:100]} | {await page.title()}")

        # Navigate to profile to check recent pins
        profile = await context.new_page()
        await profile.goto("https://www.pinterest.com/lg695101011/", wait_until="domcontentloaded", timeout=45000)
        await profile.wait_for_timeout(5000)

        # Check if we're on the profile or redirected
        print(f"Profile URL: {profile.url}")
        print(f"Profile title: {await profile.title()}")

        # Look for pins
        pins = await profile.evaluate("""
        (() => {
            const links = [...document.querySelectorAll('a')];
            const pinLinks = links.filter(a => a.href && a.href.includes('/pin/'));
            return JSON.stringify(pinLinks.slice(0, 10).map(a => ({
                href: a.href,
                text: (a.querySelector('img')?.alt || a.textContent)?.substring(0, 80)
            })));
        })()
        """)
        print(f"Recent pins: {pins}")

        # Go back to pin builder to see if there are unsaved drafts
        builder = await context.new_page()
        await builder.goto("https://www.pinterest.com/pin-builder/", wait_until="domcontentloaded", timeout=45000)
        await builder.wait_for_timeout(5000)

        # Check current state
        state = await builder.evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            const images = [...document.querySelectorAll('img')];
            const inputs = [...document.querySelectorAll('input')];
            return JSON.stringify({
                url: window.location.href,
                buttons: buttons.filter(b => b.offsetParent !== null).map(b => b.textContent.trim()).slice(0, 10),
                imageCount: images.length,
                inputNames: inputs.map(i => ({name: i.name, type: i.type, placeholder: i.placeholder}))
            });
        })()
        """)
        print(f"Builder state: {state}")

        # Try different approach: look for the pin-creation flow elements
        # Pinterest might have a modal/dialog flow
        flow = await builder.evaluate("""
        (() => {
            const allText = document.body.innerText.substring(0, 500);
            return allText;
        })()
        """)
        print(f"Page text preview: {flow[:300]}")

        await profile.close()

asyncio.run(main())
