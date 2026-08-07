"""Publish Medium article via Playwright CDP - proven method from 08-06."""
from playwright.sync_api import sync_playwright
import time

TITLE = "Puppy Vaccination Schedule: What Every New Owner Misses"

BODY_PARAGRAPHS = [
    "I built PupVax.com, a free puppy vaccine schedule tracker. 839 Google impressions. 1 click. Zero clicks on the top 10 queries.",
    "The tool works. The content is accurate (AAHA 2026 guidelines, CDC deworming recommendations). But Google has not decided the site is an authority on dog health yet.",
    "",
    "## The 0-click problem",
    "Top query \"puppy vaccinations\" has 111 impressions and zero clicks at position 67.5 (page 7). Nobody scrolls to page 7. The tool needs external signals to move up.",
    "\"puppy vaccination schedule\" has 39 impressions, zero clicks. \"puppy vaccination schedule chart\" has 21 impressions, zero clicks. Combined, 91 impressions across vaccination schedule queries, all at positions where no one clicks.",
    "",
    "## What most owners do not know",
    "90% of puppies are born with roundworms. Deworming at 2 weeks is standard care, not optional. The immunity gap between weeks 8 and 16 means puppies are most vulnerable to parvovirus and distemper exactly when maternal antibodies are fading but still blocking vaccine response.",
    "This is why the vaccine schedule is a series, not a single shot. Not because one dose is not strong enough. Because we do not know exactly when maternal antibodies will clear enough for the puppy to respond.",
    "",
    "## The fix I am testing",
    "One variable change per observation window. For PupVax, I am adding authoritative citations (AAHA, WSAVA, CDC), creating a dedicated puppy vaccination schedule page, and publishing external backlinks from non-GitHub domains.",
    "Wait 7 to 14 days. Check GSC. If CTR moves, keep going. If not, pick the next variable.",
    "",
    "The tool is free, no sign-up, browser-based: pupvax.com",
    "Full GSC analysis and evidence log on GitHub: github.com/Gavin1901/free-browser-tools-index",
]

print("Connecting CDP for Medium...")
with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp("http://localhost:9223")
    ctx = browser.contexts[0]

    # Find or create a page for Medium
    page = None
    for p in ctx.pages:
        if "medium.com" in p.url:
            page = p
            print(f"Found existing Medium page: {p.url}")
            break

    if not page:
        page = ctx.new_page()

    # Go to Medium new story
    print("Navigating to Medium new story...")
    page.goto("https://medium.com/new-story", wait_until="networkidle", timeout=30000)
    time.sleep(4)
    print(f"URL: {page.url}")

    # Fill title using keyboard.type()
    try:
        title_area = page.locator('[data-testid="editorTitle"]').first
        if not title_area.is_visible(timeout=3000):
            title_area = page.locator('[contenteditable="true"]').first

        title_area.click()
        time.sleep(1)
        page.keyboard.type(TITLE, delay=15)
        print("Title typed")
        time.sleep(2)
    except Exception as e:
        print(f"Title error: {e}")

    # Type body paragraph by paragraph
    try:
        page.keyboard.press("Enter")
        time.sleep(1)

        for i, para in enumerate(BODY_PARAGRAPHS):
            if para == "":
                page.keyboard.press("Enter")
                time.sleep(0.3)
                continue

            if para.startswith("## "):
                page.keyboard.type(para, delay=5)
                page.keyboard.press("Enter")
                page.keyboard.press("Enter")
                time.sleep(0.5)
                continue

            if para.startswith("- "):
                page.keyboard.type(para, delay=5)
                page.keyboard.press("Enter")
                time.sleep(0.3)
                continue

            page.keyboard.type(para, delay=5)
            page.keyboard.press("Enter")
            page.keyboard.press("Enter")
            time.sleep(0.5)

            if (i+1) % 3 == 0:
                print(f"Paragraph {i+1}/{len(BODY_PARAGRAPHS)} done")

        print("All paragraphs typed")
    except Exception as e:
        print(f"Body error: {e}")

    time.sleep(3)

    # Click Publish (with secondary confirmation check)
    try:
        publish_btn = page.locator('button:has-text("Publish")').first
        if publish_btn.is_visible(timeout=3000):
            publish_btn.click()
            print("Clicked Publish")
            time.sleep(5)

            # Medium sometimes shows a second publish confirmation
            confirm_btn = page.locator('button:has-text("Publish")').first
            if confirm_btn.is_visible(timeout=2000):
                confirm_btn.click()
                print("Clicked confirm Publish")
                time.sleep(8)

            print(f"Final URL: {page.url}")

            # Get canonical
            try:
                canonical = page.locator('link[rel="canonical"]').get_attribute('href')
                print(f"Canonical: {canonical}")
            except Exception as e:
                print(f"Canonical error: {e}")
    except Exception as e:
        print(f"Publish error: {e}")

    browser.close()
    print("DONE")
