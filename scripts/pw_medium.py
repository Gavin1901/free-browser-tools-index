import json, time
from playwright.sync_api import sync_playwright

TITLE = "0 Clicks, 1180 Impressions: An Invoice Generator SEO Lesson"
CONTENT = """After checking Google Search Console for InvoicePad (https://invoicepad.net), I found something surprising: 1,180 search impressions but zero clicks.

The free invoice generator works perfectly. You pick a template, fill in your details, and download a clean PDF. No sign-up, no watermark.

But here is the problem. People are not searching for "free invoice generator." They are searching for very specific templates:

- "web development invoice" — 88 impressions
- "handyman invoice template" — 33 impressions
- "makeup artist invoice template" — 27 impressions
- "SEO service invoice template" — 26 impressions
- "freelance writer invoice template" — 24 impressions

When someone searches "handyman invoice template," they want to see a handyman-specific preview with labor hours and materials pre-filled. The tool is right, but the landing page is wrong for that intent.

We are building dedicated landing pages for each profession. Same free tool, better search intent match.

Visit InvoicePad at https://invoicepad.net and generate a PDF invoice in under 60 seconds."""

print("Connecting to CDP 9223...")
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9223")
    contexts = browser.contexts
    print(f"Contexts: {len(contexts)}")
    
    context = contexts[0]
    pages = context.pages
    print(f"Pages: {len(pages)}")
    
    # Find or create a page for Medium
    medium_page = None
    for pg in pages:
        if "medium.com" in pg.url:
            medium_page = pg
            break
    
    if not medium_page:
        print("No Medium page, creating new...")
        medium_page = context.new_page()
    
    # Navigate to new story
    print("Navigating to Medium new-story...")
    medium_page.goto("https://medium.com/new-story", wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)
    
    # Check if on new-story page
    print(f"Current URL: {medium_page.url[:100]}")
    
    # Wait for editor to load
    try:
        medium_page.wait_for_selector('[contenteditable="true"]', timeout=15000)
        print("Editor loaded")
    except:
        print("Editor not found, taking screenshot...")
        medium_page.screenshot(path="D:/Tools/ai-tool-index/logs/2026-08-06-medium-playwright-debug.png")
    
    # Find editables
    editables = medium_page.query_selector_all('[contenteditable="true"]')
    print(f"Editables found: {len(editables)}")
    
    if len(editables) >= 1:
        # Click title area (first editable)
        print("Clicking title area...")
        editables[0].click()
        time.sleep(1)
        
        # Type title
        print("Typing title...")
        editables[0].fill("")
        time.sleep(0.5)
        editables[0].type(TITLE, delay=20)
        time.sleep(2)
        print(f"Title typed: {editables[0].text_content()[:60]}")
        
        # Click content area (second editable if exists, otherwise first)
        if len(editables) >= 2:
            content_el = editables[1]
        else:
            # Press Enter to go to content
            medium_page.keyboard.press("Enter")
            time.sleep(1)
            content_el = editables[0]
        
        print("Typing content...")
        content_el.click()
        time.sleep(1)
        content_el.type(CONTENT, delay=15)
        time.sleep(3)
        
        print(f"Content length: {len(content_el.text_content())}")
        
        # Check for Publish button
        time.sleep(3)
        pub_buttons = medium_page.query_selector_all('button')
        pub_btn = None
        for btn in pub_buttons:
            text = btn.text_content().strip()
            if text == 'Publish' and btn.is_visible():
                pub_btn = btn
                break
        
        if pub_btn:
            print("Clicking Publish...")
            pub_btn.click()
            time.sleep(3)
            
            # Check for confirmation dialog
            pub_buttons2 = medium_page.query_selector_all('button')
            for btn in pub_buttons2:
                text = btn.text_content().strip()
                if 'Publish' in text and btn.is_visible():
                    print(f"Second Publish button: {text}")
                    try:
                        btn.click()
                        time.sleep(5)
                    except:
                        pass
            
            # Screenshot and check URL
            medium_page.screenshot(path="D:/Tools/ai-tool-index/logs/2026-08-06-medium-playwright-final.png")
            print(f"Final URL: {medium_page.url}")
        else:
            print("Publish button not found!")
            medium_page.screenshot(path="D:/Tools/ai-tool-index/logs/2026-08-06-medium-playwright-nopub.png")
    
    browser.close()
    print("Done")

