import asyncio
from playwright.async_api import async_playwright

async def submit_toolradar():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=r"D:\ChromeProfiles\GavinBuilds",
            headless=False,
            channel="chrome"
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        await page.goto("https://toolradar.com/company/submit", timeout=15000)
        await page.wait_for_timeout(3000)
        
        # Find all form fields
        inputs = page.locator("input, textarea, select")
        count = await inputs.count()
        print(f"Form fields: {count}")
        
        for i in range(count):
            try:
                tag = await inputs.nth(i).evaluate("el => el.tagName")
                name = await inputs.nth(i).get_attribute("name")
                placeholder = await inputs.nth(i).get_attribute("placeholder")
                label = await inputs.nth(i).get_attribute("aria-label")
                req = await inputs.nth(i).get_attribute("required")
                print(f"  [{tag}] name={name} placeholder={placeholder} label={label} required={req}")
            except:
                pass
        
        await page.screenshot(path=r"D:\Tools\ai-tool-index\logs\2026-08-04-toolradar-form.png")
        
        # Try to fill if form is accessible
        name_input = page.locator('input[name*="name" i]').first
        url_input = page.locator('input[name*="url" i], input[name*="website" i]').first
        desc_input = page.locator('textarea[name*="desc" i], textarea[name*="about" i]').first
        
        name_count = await name_input.count()
        url_count = await url_input.count()
        print(f"Name input: {name_count}, URL input: {url_count}")
        
        if name_count > 0 and url_count > 0:
            await name_input.fill("ZonePlan - Worldwide Meeting Planner")
            await url_input.fill("https://zoneplan.net")
            print("Basic fields filled")
        
        await page.screenshot(path=r"D:\Tools\ai-tool-index\logs\2026-08-04-toolradar-filled.png")
        await browser.close()

asyncio.run(submit_toolradar())
