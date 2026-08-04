"""Publish ONE Pinterest Pin with explicit link - careful DOM targeting"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

SITE = {
    "name": "ZonePlan",
    "title": "Worldwide Meeting Planner - Find Fair Times Across 24 Time Zones",
    "url": "https://zoneplan.net",
    "desc": "Free worldwide meeting planner. Compare working hours across 24 time zones, handle DST, find overlapping slots. No sign-up required."
}

def cdp_endpoint(port="9223"):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=10) as r:
        return json.load(r)["webSocketDebuggerUrl"]

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(cdp_endpoint("9223"))
        context = browser.contexts[0]
        page = await context.new_page()

        # Go to pin builder
        await page.goto("https://www.pinterest.com/pin-builder/", wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(5000)

        print(f"URL: {page.url}")

        # Take screenshot of site for pin image
        ss_page = await context.new_page()
        ss_path = f"D:\\Tools\\ai-tool-index\\temp\\pin-{SITE['name'].lower()}-v2.png"
        await ss_page.goto(SITE["url"], wait_until="domcontentloaded", timeout=30000)
        await ss_page.wait_for_timeout(3000)
        await ss_page.screenshot(path=ss_path)
        await ss_page.close()
        print(f"Screenshot saved: {ss_path}")

        # Upload image
        file_input = page.locator('input[type="file"]')
        if await file_input.count() > 0:
            await file_input.first.set_input_files(ss_path)
            await page.wait_for_timeout(5000)
            print("Image uploaded")
        else:
            # Try drag-drop area
            print("No file input found, trying alternative...")
            body = await page.evaluate("document.body.innerText.substring(0, 500)")
            print(f"Page body: {body}")

        # Now try to find and fill the link field
        # Pinterest's pin builder has specific data-testid attributes
        await page.wait_for_timeout(3000)

        # Dump all visible inputs
        inputs = await page.evaluate("""
        (() => {
            const allInputs = [...document.querySelectorAll('input, textarea, [contenteditable="true"]')];
            return JSON.stringify(allInputs.filter(el => el.offsetParent !== null).map(el => ({
                tag: el.tagName,
                type: el.type || 'N/A',
                id: el.id,
                name: el.name,
                placeholder: el.placeholder,
                ariaLabel: el.getAttribute('aria-label'),
                dataTestId: el.getAttribute('data-test-id') || el.getAttribute('data-testid'),
                role: el.getAttribute('role'),
                contentEditable: el.getAttribute('contenteditable'),
                value: el.value?.substring(0, 30) || ''
            })));
        })()
        """)
        print(f"Visible inputs: {inputs}")

        # Try clicking the "Add link" or link area
        # Pinterest might have a separate "Add destination link" section
        await page.evaluate("""
        (() => {
            // Try clicking any element that mentions "link" or "website" or "destination"
            const allElements = [...document.querySelectorAll('*')];
            const linkElements = allElements.filter(el => {
                const text = (el.textContent || '').toLowerCase();
                return (text.includes('link') || text.includes('website') || text.includes('destination')) &&
                       el.offsetParent !== null &&
                       (el.tagName === 'BUTTON' || el.tagName === 'DIV' || el.tagName === 'SPAN');
            });
            if (linkElements.length > 0) {
                linkElements[0].click();
                return 'Clicked: ' + linkElements[0].textContent?.substring(0, 50);
            }
            return 'No link element found';
        })()
        """)

        await page.wait_for_timeout(2000)

        # Re-check inputs after clicking
        inputs2 = await page.evaluate("""
        (() => {
            const allInputs = [...document.querySelectorAll('input, textarea, [contenteditable="true"]')];
            return JSON.stringify(allInputs.filter(el => el.offsetParent !== null).map(el => ({
                tag: el.tagName,
                type: el.type || 'N/A',
                id: el.id,
                placeholder: el.placeholder,
                ariaLabel: el.getAttribute('aria-label'),
                value: el.value?.substring(0, 30) || ''
            })));
        })()
        """)
        print(f"Inputs after link click: {inputs2}")

        # Try to type the URL into any visible input that might be a link field
        typed = await page.evaluate(f"""
        (() => {{
            const inputs = [...document.querySelectorAll('input[type="text"], input:not([type]), textarea')]
                .filter(el => el.offsetParent !== null);
            for (const input of inputs) {{
                if (input.placeholder && (
                    input.placeholder.toLowerCase().includes('link') ||
                    input.placeholder.toLowerCase().includes('website') ||
                    input.placeholder.toLowerCase().includes('url') ||
                    input.placeholder.toLowerCase().includes('destination')
                )) {{
                    input.focus();
                    input.value = '{SITE['url']}';
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return 'Filled: ' + input.placeholder;
                }}
            }}
            // Fallback: try any text input
            for (const input of inputs) {{
                if (!input.value && input.type !== 'file' && input.type !== 'checkbox' && input.type !== 'radio') {{
                    input.focus();
                    input.value = '{SITE['url']}';
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return 'Filled fallback: ' + (input.placeholder || input.id || 'unnamed');
                }}
            }}
            return 'No fillable input found. Inputs: ' + inputs.map(i => i.placeholder || i.id || i.type).join(', ');
        }})()
        """)
        print(f"Type URL result: {typed}")

        # Click Save
        await page.wait_for_timeout(2000)
        save_clicked = await page.evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            const saveBtn = buttons.find(b => {
                const text = b.textContent.trim().toLowerCase();
                return text === 'save' || text.includes('publish') || text.includes('save from');
            });
            if (saveBtn) {
                saveBtn.click();
                return 'Clicked: ' + saveBtn.textContent.trim();
            }
            return 'No save button. All buttons: ' + buttons.filter(b => b.offsetParent !== null).map(b => b.textContent.trim()).join(', ');
        })()
        """)
        print(f"Save: {save_clicked}")

        await page.wait_for_timeout(8000)

        final_url = page.url
        print(f"Final URL: {final_url}")

        # Check if we got redirected to a pin
        if '/pin/' in final_url:
            print(f"PIN URL: {final_url}")

            # Verify link on the pin page
            links = await page.evaluate(f"""
            (() => {{
                const targetLinks = [...document.querySelectorAll('a')]
                    .filter(a => a.href && a.href.includes('{SITE['url'].replace('https://', '')}'));
                return JSON.stringify(targetLinks.map(a => ({{
                    href: a.href,
                    visible: a.offsetParent !== null,
                    text: a.textContent?.substring(0, 40)
                }})));
            }})()
            """)
            print(f"Target links on pin: {links}")

        await page.close()

asyncio.run(main())
