"""Click the Pinterest Save/Publish button by finding it via text content"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

def cdp_endpoint(port="9223"):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=10) as r:
        return json.load(r)["webSocketDebuggerUrl"]

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(cdp_endpoint("9223"))
        context = browser.contexts[0]

        # Close the menu page that might have opened
        for p in context.pages:
            url = p.url
            if 'pin-builder' not in url and 'pinterest' in url:
                await p.close()
                print(f"Closed: {url}")

        # Get the pin-builder page
        page = None
        for p in context.pages:
            if 'pin-builder' in p.url:
                page = p
                break

        if not page:
            page = await context.new_page()
            await page.goto("https://www.pinterest.com/pin-builder/", wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(5000)

        print(f"Page URL: {page.url}")

        # Verify content is filled
        title_check = await page.evaluate("""
        (() => {
            const titleEl = document.querySelector('textarea[id*="pin-draft-title"]');
            const linkEl = document.querySelector('textarea[id*="pin-draft-link"]');
            return JSON.stringify({
                title: titleEl?.value?.substring(0, 50),
                link: linkEl?.value?.substring(0, 50)
            });
        })()
        """)
        print(f"Content: {title_check}")

        # If no content, fill it
        if '"title":""' in title_check or '"title":null' in title_check:
            ss_path = "D:\\Tools\\ai-tool-index\\temp\\pin-zoneplan-v5.png"
            ss_page = await context.new_page()
            await ss_page.goto("https://zoneplan.net", wait_until="domcontentloaded", timeout=30000)
            await ss_page.wait_for_timeout(3000)
            await ss_page.screenshot(path=ss_path)
            await ss_page.close()

            file_input = page.locator('input[type="file"]').first
            await file_input.set_input_files(ss_path)
            await page.wait_for_timeout(6000)

            title_id = await page.evaluate('document.querySelector("textarea[id*=\"pin-draft-title\"]")?.id')
            if title_id:
                tf = page.locator(f'#{title_id}')
                await tf.click()
                await tf.fill("")
                await page.keyboard.type("Worldwide Meeting Planner - Find Fair Times Across 24 Time Zones", delay=5)
                await page.wait_for_timeout(1000)

            link_id = await page.evaluate('document.querySelector("textarea[id*=\"pin-draft-link\"]")?.id')
            if link_id:
                lf = page.locator(f'#{link_id}')
                await lf.click()
                await lf.fill("")
                await page.keyboard.type("https://zoneplan.net", delay=5)
                await page.wait_for_timeout(1000)

        # NOW: Find and click the actual Save button by scanning ALL buttons for specific Chinese text
        # The button text is "从网站收藏" (garbled as "����վ�ղ�" in our encoding)
        # Let's try clicking it by its position: at the bottom of the pin builder (y > 600)

        await page.evaluate("""
        (() => {
            const allButtons = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null);

            // Calculate center of each button and log
            const log = allButtons.map((b, i) => {
                const rect = b.getBoundingClientRect();
                const text = (b.textContent || '').trim();
                return `${i}: "${text}" at (${Math.round(rect.x)},${Math.round(rect.y)}) ${Math.round(rect.width)}x${Math.round(rect.height)}`;
            });

            // Find the button in the bottom area with significant width
            // The Save button is typically wide (200+px) and in the lower portion
            const candidates = allButtons.filter(b => {
                const rect = b.getBoundingClientRect();
                const text = b.textContent.trim();
                return rect.y > 500 && rect.width > 150 && text.length > 0;
            });

            if (candidates.length > 0) {
                candidates[0].click();
                console.log('Clicked button:', candidates[0].textContent.trim());
                console.log('Button log:', log.join('\\n'));
                return 'Clicked: ' + candidates[0].textContent.trim();
            }

            // Try ALL buttons in lower area
            for (const btn of allButtons.reverse()) {
                const rect = btn.getBoundingClientRect();
                if (rect.y > 400 && rect.width > 100) {
                    btn.click();
                    return 'Fallback click: ' + (btn.textContent?.trim() || 'no text');
                }
            }

            return 'No button found. Log:\\n' + log.join('\\n');
        })()
        """)

        await page.wait_for_timeout(10000)

        final_url = page.url
        print(f"After click URL: {final_url}")

        if '/pin/' in final_url:
            print(f"PIN PUBLISHED: {final_url}")
            # Verify link exists
            await page.wait_for_timeout(3000)
            links = await page.evaluate("""
            (() => {
                const zp = [...document.querySelectorAll('a')].filter(a => a.href && a.href.includes('zoneplan.net'));
                return JSON.stringify(zp.map(a => ({href: a.href, visible: a.offsetParent !== null})));
            })()
            """)
            print(f"ZonePlan links: {links}")
        else:
            # Check if draft was saved
            body = await page.evaluate("document.body.innerText")
            if 'Pin' in body and ('published' in body.lower() or 'saved' in body.lower() or 'created' in body.lower()):
                print("Pin appears to be saved/published")
            else:
                # One last attempt: try the button at exact coordinates
                print("Trying coordinate click...")
                await page.mouse.click(450, 660)  # Approximate position of Save button
                await page.wait_for_timeout(8000)
                print(f"After coordinate click: {page.url}")

asyncio.run(main())
