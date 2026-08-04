"""Pinterest Pin - fill correct fields by ID pattern"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

SITE = {
    "name": "ZonePlan",
    "title": "Worldwide Meeting Planner - Find Fair Times Across 24 Time Zones",
    "url": "https://zoneplan.net",
}

def cdp_endpoint(port="9223"):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=10) as r:
        return json.load(r)["webSocketDebuggerUrl"]

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(cdp_endpoint("9223"))
        context = browser.contexts[0]
        page = await context.new_page()

        await page.goto("https://www.pinterest.com/pin-builder/", wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(5000)

        # Upload screenshot
        ss_page = await context.new_page()
        ss_path = f"D:\\Tools\\ai-tool-index\\temp\\pin-{SITE['name'].lower()}-v3.png"
        await ss_page.goto(SITE["url"], wait_until="domcontentloaded", timeout=30000)
        await ss_page.wait_for_timeout(3000)
        await ss_page.screenshot(path=ss_path)
        await ss_page.close()

        file_input = page.locator('input[type="file"]').first
        await file_input.set_input_files(ss_path)
        await page.wait_for_timeout(6000)
        print("1. Image uploaded")

        # Fill TITLE field by ID pattern
        title_id = await page.evaluate("""
        (() => {
            const el = document.querySelector('textarea[id*="pin-draft-title"]');
            return el ? el.id : null;
        })()
        """)
        print(f"2. Title field ID: {title_id}")

        if title_id:
            title_field = page.locator(f'#{title_id}')
            await title_field.click()
            await title_field.fill("")
            await page.keyboard.type(SITE["title"], delay=5)
            await page.wait_for_timeout(1000)
            print(f"   Title filled: {SITE['title'][:50]}")

        # Fill LINK field by ID pattern
        link_id = await page.evaluate("""
        (() => {
            const el = document.querySelector('textarea[id*="pin-draft-link"]');
            return el ? el.id : null;
        })()
        """)
        print(f"3. Link field ID: {link_id}")

        if link_id:
            link_field = page.locator(f'#{link_id}')
            await link_field.click()
            await link_field.fill("")
            await page.keyboard.type(SITE["url"], delay=5)
            await page.wait_for_timeout(1000)
            print(f"   Link filled: {SITE['url']}")

            # Verify
            val = await link_field.input_value()
            print(f"   Link value verified: {val}")

        # Select board (required before publish)
        board_id = await page.evaluate("""
        (() => {
            const boardDiv = document.querySelector('[aria-label*="Free Online Tools"], [role="combobox"]');
            if (boardDiv) boardDiv.click();
            return boardDiv ? 'clicked' : 'no board selector';
        })()
        """)
        print(f"4. Board selector: {board_id}")
        await page.wait_for_timeout(1000)

        # Uncheck AI disclosure if checked
        await page.evaluate("""
        (() => {
            const checkboxes = [...document.querySelectorAll('input[type="checkbox"]')];
            checkboxes.forEach(cb => {
                if (cb.checked && (cb.id.includes('ai') || cb.id.includes('synthetic'))) {
                    cb.click();
                }
            });
        })()
        """)

        # Click "从网站收藏" or "Save" button
        # The publish button may vary - try multiple selectors
        publish_result = await page.evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            // Try specific publish-related buttons
            for (const btn of buttons) {
                const text = btn.textContent.trim();
                if (text && (text.includes('发布') || text.includes('保存') || text === 'Save' || text.includes('Publish'))) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return 'Clicked: ' + text;
                    }
                }
            }
            // Fallback: click the rightmost visible button in the top-right area
            for (const btn of buttons.reverse()) {
                if (btn.offsetParent !== null) {
                    btn.click();
                    return 'Clicked fallback: ' + btn.textContent.trim();
                }
            }
            return 'No clickable button';
        })()
        """)
        print(f"5. Publish click: {publish_result}")

        await page.wait_for_timeout(10000)

        final_url = page.url
        print(f"6. Final URL: {final_url}")

        if '/pin/' in final_url:
            # Verify link
            pin_id = final_url.split('/pin/')[1].split('/')[0]
            print(f"   PIN ID: {pin_id}")

            # Navigate to the pin page cleanly
            await page.goto(final_url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)

            links = await page.evaluate(f"""
            (() => {{
                const targetLinks = [...document.querySelectorAll('a')]
                    .filter(a => a.href && a.href.includes('zoneplan.net'));
                return JSON.stringify(targetLinks.map(a => ({{
                    href: a.href,
                    visible: a.offsetParent !== null
                }})));
            }})()
            """)
            print(f"   Target links: {links}")
            print(f"7. DONE - Pin URL: {final_url}")
        else:
            # Check if pin was saved as draft or needs more steps
            body = await page.evaluate("document.body.innerText.substring(0, 300)")
            print(f"   Page text: {body}")

asyncio.run(main())
