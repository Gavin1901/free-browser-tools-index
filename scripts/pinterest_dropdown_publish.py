"""Pinterest: click save dropdown arrow and select Publish Now"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        def cdp():
            with urllib.request.urlopen('http://127.0.0.1:9223/json/version', timeout=10) as r:
                return json.load(r)['webSocketDebuggerUrl']
        browser = await p.chromium.connect_over_cdp(cdp())
        ctx = browser.contexts[0]
        page = None

        # Find existing pin-builder page with filled form
        for pg in ctx.pages:
            if 'pin-builder' in pg.url:
                page = pg
                break

        if not page:
            # No existing page, the screenshot script closed it
            # Create new and fill
            page = await ctx.new_page()
            await page.goto('https://www.pinterest.com/pin-builder/', wait_until='domcontentloaded', timeout=45000)
            await page.wait_for_timeout(5000)

            ss = await ctx.new_page()
            await ss.goto('https://zoneplan.net', wait_until='domcontentloaded', timeout=30000)
            await ss.wait_for_timeout(3000)
            spath = 'D:/Tools/ai-tool-index/temp/pin-dd.png'
            await ss.screenshot(path=spath)
            await ss.close()

            fi = page.locator('input[type="file"]').first
            await fi.set_input_files(spath)
            await page.wait_for_timeout(6000)

            tid = await page.evaluate('document.querySelector("textarea[id*=\\"pin-draft-title\\"]")?.id || ""')
            if tid:
                await page.locator(f'#{tid}').click()
                await page.keyboard.type('Worldwide Meeting Planner - Free Tool', delay=5)

            lid = await page.evaluate('document.querySelector("textarea[id*=\\"pin-draft-link\\"]")?.id || ""')
            if lid:
                tf = page.locator(f'#{lid}')
                await tf.click()
                await tf.fill('')
                await page.keyboard.type('https://zoneplan.net', delay=5)

            await page.wait_for_timeout(2000)

        # Click the save button (x=315, y=535) slightly to the right to hit the dropdown arrow
        # The button is w=271, centered at ~x=450. Arrow is on the right edge ~x=580, y=553
        print(f'Current URL: {page.url}')

        # First, click the main button body to see if it just publishes
        await page.mouse.click(450, 553)
        await page.wait_for_timeout(3000)
        print(f'After main click: {page.url}')

        if '/pin/' in page.url:
            print(f'PUBLISHED! {page.url}')
            return

        # If not published, try clicking the right edge (dropdown arrow)
        await page.mouse.click(570, 553)
        await page.wait_for_timeout(3000)
        print(f'After dropdown click: {page.url}')

        # Check if a menu appeared
        menu = await page.evaluate("""
        JSON.stringify({
            bodyText: document.body.innerText.substring(0, 500),
            url: window.location.href
        })
        """)
        print(f'Menu state: {menu}')

        if '/pin/' in page.url:
            print(f'PUBLISHED! {page.url}')
            return

        # Try: look for "Publish now" or "立即发布" in any visible element and click it
        found = await page.evaluate("""
        (() => {
            const all = [...document.querySelectorAll('div, span, button, a, li')];
            for (const el of all) {
                const text = (el.textContent || '').trim();
                if ((text.includes('Publish') || text.includes('publish') || text.includes('now')) &&
                    el.offsetParent !== null && text.length < 30) {
                    el.click();
                    return 'clicked: ' + text;
                }
            }
            return 'not found';
        })()
        """)
        print(f'Publish text search: {found}')
        await page.wait_for_timeout(8000)
        print(f'Final: {page.url}')

asyncio.run(main())
