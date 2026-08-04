import asyncio
from playwright.async_api import async_playwright

async def submit_directories():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=r"D:\ChromeProfiles\GavinBuilds",
            headless=False,
            channel="chrome"
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        # 1. ToolRadar submission
        print("=== ToolRadar ===")
        await page.goto("https://toolradar.com/vendors", timeout=15000)
        await page.wait_for_timeout(3000)
        await page.screenshot(path=r"D:\Tools\ai-tool-index\logs\2026-08-04-toolradar-landing.png")
        
        # Look for submit/list button
        btns = page.locator("a, button")
        count = await btns.count()
        for i in range(min(count, 30)):
            try:
                text = await btns.nth(i).text_content()
                href = await btns.nth(i).get_attribute("href")
                if text and ("list" in text.lower() or "submit" in text.lower() or "get listed" in text.lower() or "add" in text.lower()):
                    print(f"  Btn {i}: '{text.strip()}' -> {href}")
            except:
                pass
        
        # 2. LaunchTry submission
        print("\n=== LaunchTry ===")
        await page.goto("https://launchtry.com/startup-directories/submit-saas-startup", timeout=15000)
        await page.wait_for_timeout(3000)
        await page.screenshot(path=r"D:\Tools\ai-tool-index\logs\2026-08-04-launchtry.png")
        
        # Look for form
        inputs = page.locator("input, textarea")
        icount = await inputs.count()
        print(f"  Form inputs found: {icount}")
        for i in range(min(icount, 10)):
            try:
                name = await inputs.nth(i).get_attribute("name")
                placeholder = await inputs.nth(i).get_attribute("placeholder")
                print(f"  Input {i}: name={name}, placeholder={placeholder}")
            except:
                pass
        
        await browser.close()

asyncio.run(submit_directories())
