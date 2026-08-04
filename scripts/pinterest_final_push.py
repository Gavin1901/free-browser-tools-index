"""Pinterest: find and click final Publish button in modal after Save"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

def cdp():
    with urllib.request.urlopen('http://127.0.0.1:9223/json/version', timeout=10) as r:
        return json.load(r)['webSocketDebuggerUrl']

async def pin_one(browser, name, title, url, ss_path):
    ctx = browser.contexts[0]
    page = await ctx.new_page()

    await page.goto('https://www.pinterest.com/pin-builder/', wait_until='domcontentloaded', timeout=45000)
    await page.wait_for_timeout(5000)

    # Upload image
    fi = page.locator('input[type="file"]').first
    await fi.set_input_files(ss_path)
    await page.wait_for_timeout(6000)

    # Fill title
    tid = await page.evaluate("document.querySelector('textarea[id*=\"pin-draft-title\"]')?.id || ''")
    if tid:
        await page.locator(f'#{tid}').click()
        await page.keyboard.type(title, delay=5)
        await page.wait_for_timeout(1000)

    # Fill link
    lid = await page.evaluate("document.querySelector('textarea[id*=\"pin-draft-link\"]')?.id || ''")
    if lid:
        await page.locator(f'#{lid}').click()
        await page.keyboard.type(url, delay=5)
        await page.wait_for_timeout(1000)
        print(f'  Link: {(await page.locator(f"#{lid}").input_value())[:50]}')

    # Click the wide bottom Save button
    await page.evaluate('''() => {
        const btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent);
        for (const b of btns.reverse()) {
            const r = b.getBoundingClientRect();
            if (r.width > 200 && r.y > 400) { b.click(); return 'clicked'; }
        }
    }''')
    await page.wait_for_timeout(3000)

    # NOW: check if a modal/dialog appeared
    # Look for the final publish flow
    print(f'  After save click URL: {page.url}')

    # Check for dialog, overlay, or publish confirmation
    dialog_info = await page.evaluate('''() => {
        const dialogs = document.querySelectorAll('[role="dialog"], [role="alertdialog"], .modal, [class*="Modal"], [class*="overlay"]');
        const visibleDialogs = [...dialogs].filter(d => d.offsetParent !== null);
        return JSON.stringify({
            dialogCount: visibleDialogs.length,
            url: window.location.href,
            bodyText: document.body.innerText.substring(0, 400)
        });
    }''')
    print(f'  Dialog info: {dialog_info}')

    # If no dialog, look for ANY visible buttons in the lower area
    all_btns = await page.evaluate('''() => {
        const btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent);
        return JSON.stringify(btns.map(b => ({
            text: (b.textContent || '').trim().substring(0, 30),
            w: Math.round(b.getBoundingClientRect().width),
            y: Math.round(b.getBoundingClientRect().y)
        })).filter(b => b.text));
    }''')
    print(f'  All buttons: {all_btns}')

    # Try clicking buttons that might be publish confirmations
    for attempt in range(3):
        result = await page.evaluate('''() => {
            const btns = [...document.querySelectorAll('button, div[role="button"]')].filter(b => b.offsetParent);
            // Try: "Publish", "Save", "Done", "Create Pin", colored buttons
            for (const b of btns) {
                const text = (b.textContent || '').trim();
                const style = window.getComputedStyle(b);
                const bg = style.backgroundColor;
                const isColored = bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent';
                if ((text && text.length > 0 && text.length < 20 && b.getBoundingClientRect().width > 60) || isColored) {
                    b.click();
                    return 'clicked: ' + text;
                }
            }
            return 'no button';
        }''')
        await page.wait_for_timeout(5000)
        print(f'  Attempt {attempt+1}: {result}, URL: {page.url}')
        if '/pin/' in page.url:
            break

    print(f'  Final URL: {page.url}')
    success = '/pin/' in page.url
    if success:
        # Verify link
        links = await page.evaluate(f"""
        JSON.stringify([...document.querySelectorAll('a')].filter(a => a.href && a.href.includes('{url.replace("https://","")}')).map(a => ({{href: a.href, visible: a.offsetParent !== null}})))
        """)
        print(f'  Links: {links}')
    await page.close()
    return success

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp())

        # ZonePlan
        ss = await browser.contexts[0].new_page()
        await ss.goto('https://zoneplan.net', wait_until='domcontentloaded', timeout=30000)
        await ss.wait_for_timeout(3000)
        spath = 'D:/Tools/ai-tool-index/temp/pin-zp-final2.png'
        await ss.screenshot(path=spath)
        await ss.close()

        print('=== ZonePlan ===')
        ok = await pin_one(browser, 'ZonePlan',
            'Worldwide Meeting Planner - Find Fair Times Across 24 Time Zones',
            'https://zoneplan.net', spath)
        print(f'Result: {"PUBLISHED!" if ok else "not published"}')

        # PupVax
        ss2 = await browser.contexts[0].new_page()
        await ss2.goto('https://pupvax.com', wait_until='domcontentloaded', timeout=30000)
        await ss2.wait_for_timeout(3000)
        spath2 = 'D:/Tools/ai-tool-index/temp/pin-pv-final2.png'
        await ss2.screenshot(path=spath2)
        await ss2.close()

        print('\n=== PupVax ===')
        ok2 = await pin_one(browser, 'PupVax',
            'Puppy Vaccination Schedule - Complete Timeline from 6 to 16 Weeks',
            'https://pupvax.com', spath2)
        print(f'Result: {"PUBLISHED!" if ok2 else "not published"}')

asyncio.run(main())
