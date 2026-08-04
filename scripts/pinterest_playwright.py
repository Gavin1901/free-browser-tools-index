"""Pinterest pin via Playwright native keyboard (same approach that worked for Medium)"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

SITES = [
    {"name": "ZonePlan", "title": "Worldwide Meeting Planner - Find Fair Times Across 24 Time Zones", "url": "https://zoneplan.net"},
    {"name": "PupVax", "title": "Puppy Vaccination Schedule 2026 - Complete Timeline From 6 to 16 Weeks", "url": "https://pupvax.com"},
]

def cdp():
    with urllib.request.urlopen('http://127.0.0.1:9223/json/version', timeout=10) as r:
        return json.load(r)['webSocketDebuggerUrl']

async def do_pin(p, browser, site):
    ctx = browser.contexts[0]
    page = await ctx.new_page()

    await page.goto('https://www.pinterest.com/pin-builder/', wait_until='domcontentloaded', timeout=45000)
    await page.wait_for_timeout(5000)

    # 1. Screenshot target site
    ss = await ctx.new_page()
    ss_path = f'D:/Tools/ai-tool-index/temp/pin-{site["name"].lower()}-pw.png'
    await ss.goto(site['url'], wait_until='domcontentloaded', timeout=30000)
    await ss.wait_for_timeout(3000)
    await ss.screenshot(path=ss_path)
    await ss.close()

    # 2. Upload image
    fi = page.locator('input[type="file"]').first
    await fi.set_input_files(ss_path)
    await page.wait_for_timeout(6000)

    # 3. Fill title via Playwright keyboard (native events that trigger React state)
    title_id = await page.evaluate("document.querySelector('textarea[id*=\"pin-draft-title\"]')?.id || ''")
    if title_id:
        tf = page.locator(f'#{title_id}')
        await tf.click()
        await page.keyboard.type(site['title'], delay=5)
        await page.wait_for_timeout(1000)
        print(f'  Title: {(await tf.input_value())[:40]}')

    # 4. Find and fill link via Playwright keyboard
    link_id = await page.evaluate("document.querySelector('textarea[id*=\"pin-draft-link\"]')?.id || ''")
    if link_id:
        lf = page.locator(f'#{link_id}')
        await lf.click()
        await page.keyboard.type(site['url'], delay=5)
        await page.wait_for_timeout(1000)
        print(f'  Link: {await lf.input_value()}')

    # 5. Check if board is selected (should auto-select "Free Online Tools")
    # 6. Click Save/Publish - find the large bottom button
    await page.wait_for_timeout(2000)

    # Pinterest Save button: find wide button in bottom area
    save_clicked = await page.evaluate('''() => {
        const btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent);
        for (const b of btns.reverse()) {
            const r = b.getBoundingClientRect();
            if (r.width > 200 && r.y > 500 && r.height > 30) {
                b.click();
                return 'clicked: w=' + r.width + ' y=' + r.y + ' text=' + (b.textContent || '').trim();
            }
        }
        return 'no button found';
    }''')
    print(f'  Save: {save_clicked}')

    await page.wait_for_timeout(5000)

    # After clicking Save, Pinterest may show a preview modal with final "Publish" button
    # Check for dialog/modal and click final publish
    modal_state = await page.evaluate('''() => {
        const btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent);
        const dialog = document.querySelector('[role="dialog"]');
        return JSON.stringify({
            hasDialog: !!dialog,
            visibleButtons: btns.map(b => ({
                text: (b.textContent || '').trim().substring(0, 20),
                w: Math.round(b.getBoundingClientRect().width),
                y: Math.round(b.getBoundingClientRect().y)
            })).filter(b => b.text)
        });
    }''')
    print(f'  Modal: {modal_state}')

    # Try clicking final Publish button in modal
    await page.evaluate('''() => {
        const btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent);
        const publishBtns = btns.filter(b => {
            const t = (b.textContent || '').trim();
            return t === 'Publish' || t === 'Save' || t.includes('Publish') || t.includes('Save');
        });
        if (publishBtns.length > 0) {
            publishBtns[publishBtns.length - 1].click();
            return 'clicked final';
        }
        // Try any red/dark primary button
        for (const b of btns) {
            const style = window.getComputedStyle(b);
            if (style.backgroundColor && style.backgroundColor !== 'rgba(0, 0, 0, 0)' && b.getBoundingClientRect().width > 80) {
                b.click();
                return 'clicked colored: ' + (b.textContent || '').trim();
            }
        }
        return 'no final button';
    }''')
    await page.wait_for_timeout(10000)

    final_url = page.url
    print(f'  Final URL: {final_url}')

    if '/pin/' in final_url:
        pin_id = final_url.split('/pin/')[1].split('/')[0]
        # Verify link on pin page
        links = await page.evaluate(f"""
        JSON.stringify(
            [...document.querySelectorAll('a')]
                .filter(a => a.href && a.href.includes('{site["url"].replace("https://", "")}'))
                .map(a => ({{href: a.href, visible: a.offsetParent !== null}}))
        )
        """)
        print(f'  Target links: {links}')
        await page.close()
        return {'status': 'published', 'site': site['name'], 'pin_url': final_url, 'links_verified': len(json.loads(links)) > 0}
    else:
        await page.close()
        return {'status': 'not_published', 'site': site['name'], 'final_url': final_url}

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp())

        for site in SITES:
            print(f'\n=== {site["name"]} ===')
            result = await do_pin(p, browser, site)
            print(json.dumps(result, indent=2))

asyncio.run(main())
