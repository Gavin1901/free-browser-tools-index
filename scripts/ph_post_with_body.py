"""Product Hunt: find rich text editor and fill body content"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

TITLE = "ZonePlan: Worldwide Meeting Planner Hit 258 Impressions for One Query"
BODY = """I built ZonePlan (zoneplan.net) as a free worldwide meeting planner. One query just crossed 258 Google impressions in 28 days.

The problem: worldwide meetings spanning Asia, Europe, and the Americas have conflicting DST transitions. ZonePlan shows a visual overlap grid of 24 hours across all selected time zones so you pick the one slot that works for everyone.

Current GSC data:
- 5 clicks, 4350 impressions in 28 days
- 30 pages indexed (up from 4 last week)
- Top query: meeting planner worldwide at 258 impressions, 0 clicks (still working on CTR)

Try it: https://zoneplan.net (free, no sign-up)

Would love feedback from anyone building SEO-first tools."""

def cdp():
    with urllib.request.urlopen('http://127.0.0.1:9223/json/version', timeout=10) as r:
        return json.load(r)['webSocketDebuggerUrl']

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp())
        ctx = browser.contexts[0]
        page = await ctx.new_page()

        await page.goto('https://www.producthunt.com/p/new?category=self-promotion', wait_until='domcontentloaded', timeout=45000)
        await page.wait_for_timeout(5000)
        print(f'URL: {page.url}')

        # Find ALL editable elements
        ed = await page.evaluate("""
        JSON.stringify(
            [...document.querySelectorAll('textarea, input, [contenteditable="true"], [role="textbox"]')]
                .filter(e => e.offsetParent !== null)
                .map(e => ({
                    tag: e.tagName,
                    type: e.type || 'N/A',
                    id: e.id,
                    name: e.name,
                    placeholder: (e.placeholder || '').substring(0, 40),
                    contentEditable: e.getAttribute('contenteditable'),
                    role: e.getAttribute('role'),
                    className: (e.className || '').substring(0, 50)
                }))
        )
        """)
        print(f'Editable elements: {ed}')

        # Fill title
        title_input = page.locator('input[name="title"]').first
        if await title_input.count() > 0:
            await title_input.click()
            await title_input.fill('')
            await page.keyboard.type(TITLE, delay=5)
            await page.wait_for_timeout(500)
            print(f'Title: {(await title_input.input_value())[:40]}')

        # Try to find and fill body via contenteditable or rich text editor
        # Product Hunt might use Trix, Quill, ProseMirror, or custom editor
        body_filled = False

        # Method 1: contenteditable div
        ce_div = page.locator('[contenteditable="true"]').first
        if await ce_div.count() > 0:
            await ce_div.click()
            await page.keyboard.type(BODY, delay=3)
            await page.wait_for_timeout(1000)
            text = await ce_div.inner_text()
            print(f'ContentEditable: {text[:50]}')
            body_filled = len(text) > 20

        # Method 2: role=textbox
        if not body_filled:
            tb = page.locator('[role="textbox"]').first
            if await tb.count() > 0:
                await tb.click()
                await page.keyboard.type(BODY, delay=3)
                await page.wait_for_timeout(1000)
                print(f'Role=textbox: {(await tb.inner_text())[:50]}')
                body_filled = True

        # Method 3: Look for any div that could be the editor
        if not body_filled:
            # Find all divs and try to type into the largest one
            div_info = await page.evaluate("""
            (() => {
                const divs = [...document.querySelectorAll('div')].filter(d => d.offsetParent && d.getBoundingClientRect().height > 100);
                return JSON.stringify(divs.map(d => ({
                    className: (d.className || '').substring(0, 60),
                    h: Math.round(d.getBoundingClientRect().height),
                    w: Math.round(d.getBoundingClientRect().width),
                    y: Math.round(d.getBoundingClientRect().y)
                })).slice(0, 10));
            })()
            """)
            print(f'Large divs: {div_info}')

            # Click the largest content area
            await page.evaluate("""
            (() => {
                const divs = [...document.querySelectorAll('div')].filter(d => d.offsetParent && d.getBoundingClientRect().height > 100 && d.getBoundingClientRect().y > 200);
                if (divs.length > 0) {
                    divs.sort((a,b) => b.getBoundingClientRect().height - a.getBoundingClientRect().height);
                    divs[0].click();
                }
            })()
            """)
            await page.wait_for_timeout(1000)
            await page.keyboard.type(BODY, delay=3)
            await page.wait_for_timeout(1000)
            body_filled = True
            print('Typed into large div')

        # Submit
        submit = page.locator('button[type="submit"]').first
        if await submit.count() > 0 and await submit.is_visible():
            await submit.click()
            print('Submit clicked')
            await page.wait_for_timeout(15000)

        final_url = page.url
        print(f'Final: {final_url}')

        if '/self-promotion/' in final_url and final_url != 'https://www.producthunt.com/p/self-promotion':
            print(f'POSTED: {final_url}')
            # Verify
            links = await page.evaluate("""
            JSON.stringify([...document.querySelectorAll('a')].filter(a => a.href && a.href.includes('zoneplan.net')).map(a => ({href: a.href, visible: a.offsetParent !== null})))
            """)
            print(f'Links: {links}')

asyncio.run(main())
