"""Pinterest: create pin from profile dropdown (different flow from pin-builder)"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

def cdp():
    with urllib.request.urlopen('http://127.0.0.1:9223/json/version', timeout=10) as r:
        return json.load(r)['webSocketDebuggerUrl']

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp())
        ctx = browser.contexts[0]

        # Try direct Pin creation URL
        page = await ctx.new_page()
        await page.goto('https://www.pinterest.com/pin-creation-tool/', wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(5000)
        print(f'Pin creation tool: {page.url}')
        body = await page.evaluate('document.body.innerText.substring(0, 300)')
        print(f'Body: {body}')

        # Also try the "create" endpoint
        page2 = await ctx.new_page()
        await page2.goto('https://www.pinterest.com/create/', wait_until='domcontentloaded', timeout=30000)
        await page2.wait_for_timeout(5000)
        print(f'\nCreate: {page2.url}')

        # Try going to the profile and using the create dropdown
        page3 = await ctx.new_page()
        await page3.goto('https://www.pinterest.com/lg695101011/', wait_until='domcontentloaded', timeout=30000)
        await page3.wait_for_timeout(5000)

        # Look for Create Pin button on profile
        create_btns = await page3.evaluate('''() => {
            const all = [...document.querySelectorAll('a, button, div[role="button"]')];
            const candidates = all.filter(el => {
                const text = (el.textContent || '').toLowerCase();
                return text.includes('create') || text.includes('pin') || el.getAttribute('aria-label')?.toLowerCase().includes('create');
            }).filter(el => el.offsetParent !== null);
            return JSON.stringify(candidates.map(c => ({
                tag: c.tagName,
                text: (c.textContent || '').trim().substring(0, 40),
                href: (c.href || '').substring(0, 60),
                aria: c.getAttribute('aria-label')?.substring(0, 40)
            })));
        }''')
        print(f'\nCreate buttons on profile: {create_btns}')

        # Try clicking the most likely create button
        await page3.evaluate('''() => {
            const all = [...document.querySelectorAll('a, button, div[role="button"]')];
            const btn = all.find(el => {
                const text = (el.textContent || '').toLowerCase();
                const aria = (el.getAttribute('aria-label') || '').toLowerCase();
                const href = (el.href || '');
                return text.includes('create pin') || aria.includes('create pin') ||
                       href.includes('/pin-creation-tool') || href.includes('/pin-builder');
            });
            if (btn) { btn.click(); return 'clicked'; }
            return 'not found';
        }''')
        await page3.wait_for_timeout(5000)
        print(f'After create click: {page3.url}')

        # Also try: use the "Save" button on zoneplan.net itself (like a user would)
        # Visit zoneplan.net and use Pinterest's browser save functionality
        page4 = await ctx.new_page()
        await page4.goto('https://zoneplan.net', wait_until='domcontentloaded', timeout=30000)
        await page4.wait_for_timeout(3000)

        # Check if Pinterest save extension is available
        pinterest_ext = await page4.evaluate('''() => {
            // Check for Pinterest's global objects
            return JSON.stringify({
                hasPinIt: typeof window.PinUtils !== 'undefined',
                hasParse: typeof window.parsePinIt !== 'undefined'
            });
        }''')
        print(f'\nPinterest extension on zoneplan: {pinterest_ext}')

        # As a last resort, try: post via Pinterest API endpoint
        # The v3 API endpoint for creating pins
        print('\n=== Summary ===')
        print('Pin creation tool: ' + ('WORKS' if 'pin-creation-tool' in page.url else 'redirected to pin-builder'))
        print('Create endpoint: ' + page2.url)

asyncio.run(main())
