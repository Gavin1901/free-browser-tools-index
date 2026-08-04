"""Complete existing Pinterest draft - click the right publish button"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

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

        # Check if there's a draft
        has_draft = await page.evaluate("""
        (() => {
            const body = document.body.innerText;
            return body.includes('草稿') || body.includes('Draft') || body.includes('draft');
        })()
        """)
        print(f"Has draft: {has_draft}")

        if not has_draft:
            print("No draft found, creating new...")
            # Fill everything again quick
            ss_page = await context.new_page()
            ss_path = "D:\\Tools\\ai-tool-index\\temp\\pin-zoneplan-v4.png"
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

            # Confirm link value
            link_val = await page.locator(f'#{link_id}').input_value()
            print(f"Link value: {link_val}")

        # Now the key step: find ALL buttons and their text, click the right one
        buttons = await page.evaluate("""
        (() => {
            const allButtons = [...document.querySelectorAll('button, [role="button"]')];
            return JSON.stringify(allButtons.map((b, i) => ({
                index: i,
                text: b.textContent?.trim()?.substring(0, 30),
                visible: b.offsetParent !== null,
                enabled: !b.disabled,
                rect: b.getBoundingClientRect()
            })).filter(b => b.visible));
        })()
        """)
        print(f"Visible buttons: {buttons}")

        # Pinterest has a specific publish flow:
        # The main blue/dark button in the top right - try clicking it
        # Or the button that says "Save" / "Publish" / "Review" in some form
        clicked = await page.evaluate("""
        (() => {
            const allButtons = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null);

            // Pinterest "Save" button is typically a dark button with specific styles
            // Try to find by position (top right) or by being the primary action button
            for (const btn of allButtons) {
                const rect = btn.getBoundingClientRect();
                const text = (btn.textContent || '').trim();

                // Skip tiny or empty buttons
                if (rect.width < 40 && rect.height < 40) continue;

                // The primary publish button is typically the rightmost button
                // in the header area (y < 100) or a prominent button at the bottom
                if (text && text.length > 1 && text.length < 20) {
                    console.log('Trying button: ' + text + ' at (' + rect.x + ',' + rect.y + ')');
                }
            }

            // Strategy: find the most likely "Save/Publish" button by position
            // Pinterest's save button is usually at the top right, dark colored
            const candidates = allButtons.filter(b => {
                const rect = b.getBoundingClientRect();
                return rect.y < 80 && rect.x > 600; // top right area
            });

            if (candidates.length > 0) {
                // Click the rightmost one
                candidates.sort((a, b) => b.getBoundingClientRect().x - a.getBoundingClientRect().x);
                candidates[0].click();
                return 'Clicked top-right button: ' + (candidates[0].textContent?.trim() || 'no text');
            }

            // Alternative: find by background color (dark button)
            for (const btn of allButtons) {
                const style = window.getComputedStyle(btn);
                const bg = style.backgroundColor;
                if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
                    const text = btn.textContent.trim();
                    if (text && text.length > 0 && text.length < 15) {
                        btn.click();
                        return 'Clicked colored button: ' + text + ' bg=' + bg;
                    }
                }
            }

            return 'No publish button identified';
        })()
        """)
        print(f"Click result: {clicked}")

        await page.wait_for_timeout(10000)

        final_url = page.url
        print(f"Final URL: {final_url}")

        if '/pin/' in final_url:
            print(f"SUCCESS: {final_url}")
        else:
            # One more attempt - click "以后发布" which might be "Publish now" with a dropdown
            body_text = await page.evaluate("document.body.innerText.substring(0, 500)")
            print(f"Page text: {body_text}")

            # Try clicking elements near "Publish" text
            await page.evaluate("""
            (() => {
                const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
                let node;
                while (node = walker.nextNode()) {
                    const text = node.textContent.trim();
                    if (text === 'Publish' || text === 'Save' || text.includes('Publish') || text.includes('Save')) {
                        const clickable = node.parentElement;
                        if (clickable) {
                            clickable.click();
                            return;
                        }
                    }
                }
            })()
            """)
            await page.wait_for_timeout(6000)
            print(f"After text search: {page.url}")

asyncio.run(main())
