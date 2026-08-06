import time
from playwright.sync_api import sync_playwright

SHORT = "GSC analysis for InvoicePad: 1180 impressions, zero clicks. The free invoice generator works but search intent is misaligned. People search for profession-specific templates. Fix coming: dedicated landing pages. https://invoicepad.net"

print("Connect...")
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9223")
    context = browser.contexts[0]
    pages = context.pages
    
    # Find Medium page
    pg = None
    for pge in pages:
        if "medium.com" in pge.url:
            pg = pge
            break
    if not pg:
        pg = pages[0]
    
    print(f"URL: {pg.url[:80]}")
    
    # Navigate to fresh new-story
    pg.goto("https://medium.com/new-story", timeout=20000)
    time.sleep(4)
    
    # Wait for editor
    try:
        pg.wait_for_selector('[contenteditable="true"]', timeout=10000)
    except:
        print("No editor")
        browser.close()
        exit()
    
    editables = pg.query_selector_all('[contenteditable="true"]')
    print(f"Editables: {len(editables)}")
    
    # Title: use fill (not type to save time)
    title_el = editables[0]
    title_el.click()
    time.sleep(1)
    # Clear first
    pg.keyboard.press("Control+a")
    pg.keyboard.press("Backspace")
    time.sleep(0.5)
    # Type title with keyboard for draft detection
    pg.keyboard.type("InvoicePad SEO: 0 Clicks on 1180 Impressions", delay=10)
    time.sleep(2)
    
    # Content: click into it and type short text
    content_el = editables[1] if len(editables) >= 2 else editables[0]
    if len(editables) >= 2:
        content_el.click()
    else:
        pg.keyboard.press("Enter")
        time.sleep(1)
    
    time.sleep(1)
    # Type the short text via keyboard
    pg.keyboard.type(SHORT, delay=5)
    time.sleep(3)
    
    print(f"Content typed: {len(content_el.text_content())} chars")
    
    # Check for publish availability
    popover = pg.query_selector('.popover-description')
    if popover:
        print(f"Popover: {popover.text_content()[:80]}")
    
    # Try publish
    pub_btns = pg.query_selector_all('button')
    for btn in pub_btns:
        if btn.text_content().strip() == 'Publish' and btn.is_visible():
            print("Clicking Publish...")
            btn.click()
            time.sleep(4)
            break
    
    # Check result
    print(f"URL: {pg.url}")
    pg.screenshot(path="D:/Tools/ai-tool-index/logs/2026-08-06-medium-pw-fast.png")
    browser.close()
    print("Done")
