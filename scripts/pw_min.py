from playwright.sync_api import sync_playwright
import time

print("Starting...")
with sync_playwright() as p:
    print("Connecting...")
    browser = p.chromium.connect_over_cdp("http://localhost:9223")
    print(f"Connected. Contexts: {len(browser.contexts)}")
    ctx = browser.contexts[0]
    print(f"Pages: {len(ctx.pages)}")
    for pg in ctx.pages:
        print(f"  Page: {pg.url[:100]}")
    browser.close()
    print("Done")
