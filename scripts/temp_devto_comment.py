import asyncio
from playwright.async_api import async_playwright

async def devto_comment():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=r"D:\ChromeProfiles\GavinBuilds",
            headless=False,
            channel="chrome"
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        # Go to the article
        await page.goto("https://dev.to/_d7eb1c1703182e3ce1782/best-free-developer-tools-2026-the-complete-curated-list-3i0l", timeout=15000)
        await page.wait_for_timeout(3000)
        
        # Find comment box
        comment_box = page.locator('[contenteditable="true"]').first
        if await comment_box.count() == 0:
            comment_box = page.locator('textarea#text-area').first
        if await comment_box.count() == 0:
            comment_box = page.locator('textarea').first
        
        cb_count = await comment_box.count()
        print(f"Comment box found: {cb_count}")
        
        if cb_count > 0:
            await comment_box.click()
            await page.wait_for_timeout(500)
            
            comment = """Great list! Two free tools I would add for remote dev teams:

**ZonePlan** (https://zoneplan.net) - Free worldwide meeting planner that handles DST automatically across 35+ cities. Way simpler than World Time Buddy for quick team scheduling. No sign-up needed.

**iWorkViewer** (https://iworkviewer.com) - Opens Apple Pages, Numbers and Keynote files right in the browser. Super useful when a client or designer sends you .pages or .keynote files and you are on Windows/Linux/Android. No upload, processes locally.

Both are completely free with no accounts required."""
            
            await page.keyboard.type(comment, delay=10)
            print("Comment typed")
            await page.wait_for_timeout(1000)
        
        await page.screenshot(path=r"D:\Tools\ai-tool-index\logs\2026-08-04-devto-comment.png")
        
        # Submit
        submit_btn = page.locator('button[type="submit"]').first
        if await submit_btn.count() > 0:
            await submit_btn.click()
            await page.wait_for_timeout(3000)
            print(f"Comment submitted! URL: {page.url}")
        
        await page.screenshot(path=r"D:\Tools\ai-tool-index\logs\2026-08-04-devto-comment-final.png")
        await browser.close()

asyncio.run(devto_comment())
