"""Publish Pinterest Pin via Playwright native keyboard on CDP Chrome"""
import argparse, asyncio, json, urllib.request, os
from playwright.async_api import async_playwright

SITES = [
    {
        "name": "ZonePlan",
        "title": "Worldwide Meeting Planner - Find Fair Times Across 24 Time Zones",
        "url": "https://zoneplan.net",
        "image": None  # Will use screenshot approach
    },
    {
        "name": "PupVax",
        "title": "Puppy Vaccination Schedule 2026 - Complete Timeline From 6 to 16 Weeks",
        "url": "https://pupvax.com",
        "image": None
    }
]

def cdp_endpoint(port="9223"):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=10) as r:
        return json.load(r)["webSocketDebuggerUrl"]

async def create_pin(playwright, browser, site):
    context = browser.contexts[0]
    page = await context.new_page()

    # Go to pin builder
    await page.goto("https://www.pinterest.com/pin-builder/", wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(5000)

    # Check if we're on the pin builder
    url = page.url
    print(f"  Pinterest URL: {url}")

    if "login" in url or "auth" in url:
        return {"status": "login_blocked", "site": site["name"]}

    # Pinterest pin builder flow:
    # 1. Upload image (click the upload area or use file input)
    # 2. Fill title/description
    # 3. Add destination link
    # 4. Click Save/Publish

    # Try to find the file input for image upload
    try:
        file_input = page.locator('input[type="file"]').first
        if await file_input.count() > 0:
            # We need an actual image file. Try to take a screenshot of the target site as the pin image
            screenshot_path = f"D:\\Tools\\ai-tool-index\\temp\\pin-{site['name'].lower()}.png"

            # Take a screenshot of the target site
            ss_page = await context.new_page()
            try:
                await ss_page.goto(site["url"], wait_until="domcontentloaded", timeout=30000)
                await ss_page.wait_for_timeout(3000)
                await ss_page.screenshot(path=screenshot_path, full_page=False)
                await ss_page.close()
            except:
                await ss_page.close()
                return {"status": "screenshot_failed", "site": site["name"]}

            if os.path.exists(screenshot_path):
                await file_input.set_input_files(screenshot_path)
                await page.wait_for_timeout(5000)
                print(f"  Image uploaded: {screenshot_path}")
            else:
                return {"status": "no_screenshot", "site": site["name"]}
    except Exception as e:
        print(f"  File input error: {e}")
        return {"status": "upload_error", "site": site["name"], "error": str(e)}

    # Fill title
    try:
        title_field = page.locator('[data-test-id="pin-title"], #storyboard-title, [aria-label*="title" i], [placeholder*="title" i]').first
        if await title_field.count() > 0:
            await title_field.click()
            await title_field.fill("")
            await page.keyboard.type(site["title"], delay=5)
            await page.wait_for_timeout(1000)
            print(f"  Title filled: {site['title'][:50]}")
    except Exception as e:
        print(f"  Title error: {e}")

    # Fill destination link
    try:
        link_field = page.locator('[data-test-id="pin-link"], #storyboard-link, [aria-label*="link" i], [placeholder*="link" i], [placeholder*="website" i]').first
        if await link_field.count() > 0:
            await link_field.click()
            await link_field.fill("")
            await page.keyboard.type(site["url"], delay=5)
            await page.wait_for_timeout(1000)
            print(f"  Link filled: {site['url']}")
    except Exception as e:
        print(f"  Link error: {e}")

    # Click Save/Publish button
    try:
        # Look for Save or Publish button
        save_btn = page.locator('button:has-text("Save"), button:has-text("Publish"), [data-test-id="board-dropdown-save-button"]').first
        if await save_btn.count() > 0:
            await save_btn.click()
            await page.wait_for_timeout(5000)
            print(f"  Save clicked")
    except Exception as e:
        print(f"  Save error: {e}")

    # After publishing, try to get the pin URL
    await page.wait_for_timeout(5000)
    final_url = page.url
    title = await page.title()

    # If we got redirected to the pin page, extract the URL
    pin_url = final_url if "pin" in final_url else None

    result = {
        "status": "published" if pin_url else "unknown",
        "site": site["name"],
        "pin_url": pin_url,
        "final_url": final_url,
        "title": title
    }

    await page.close()
    return result

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(cdp_endpoint("9223"))

        for site in SITES:
            print(f"\n=== Pinterest: {site['name']} ===")
            result = await create_pin(playwright, browser, site)
            print(json.dumps(result, indent=2))

asyncio.run(main())
