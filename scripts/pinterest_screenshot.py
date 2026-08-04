"""Take screenshot of Pinterest filled form for debugging"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        def cdp():
            with urllib.request.urlopen('http://127.0.0.1:9223/json/version', timeout=10) as r:
                return json.load(r)['webSocketDebuggerUrl']
        browser = await p.chromium.connect_over_cdp(cdp())
        ctx = browser.contexts[0]

        ss = await ctx.new_page()
        await ss.goto('https://zoneplan.net', wait_until='domcontentloaded', timeout=30000)
        await ss.wait_for_timeout(3000)
        spath = 'D:/Tools/ai-tool-index/temp/pin-debug.png'
        await ss.screenshot(path=spath)
        await ss.close()

        page = await ctx.new_page()
        await page.goto('https://www.pinterest.com/pin-builder/', wait_until='domcontentloaded', timeout=45000)
        await page.wait_for_timeout(5000)

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
        await page.screenshot(path='D:/Tools/ai-tool-index/temp/pin-filled-form.png', full_page=True)
        print('Screenshot saved!')

        # Dump ALL visible buttons with exact positions
        btns = await page.evaluate("""
        JSON.stringify(
            [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null).map(b => ({
                text: (b.textContent || '').trim().substring(0, 40),
                x: Math.round(b.getBoundingClientRect().x),
                y: Math.round(b.getBoundingClientRect().y),
                w: Math.round(b.getBoundingClientRect().width),
                h: Math.round(b.getBoundingClientRect().height)
            }))
        )
        """)
        print(f'Buttons: {btns}')

asyncio.run(main())
