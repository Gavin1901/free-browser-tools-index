"""Publish Medium article via Playwright CDP with native keyboard typing."""
from playwright.sync_api import sync_playwright
import time

TITLE = "What I Learned Running Isolated SEO Experiments on 8 Free Browser Tools"

BODY_PARAGRAPHS = [
    "I built 8 free browser tools over the past few months. An iWork file viewer, a live photo converter, a planting calendar, a TDEE calculator, a baby growth tracker, an invoice generator, a meeting planner, and a puppy vaccine scheduler.",
    "They all live on their own domains. They all use Next.js and Cloudflare Pages. They all have proper sitemaps, schema markup, and IndexNow submission.",
    "What I did not have was a clear SEO growth methodology. So I built one.",
    "",
    "## The One-Variable Rule",
    "The biggest mistake I made early on was changing too many things at once. New page titles, new meta descriptions, new content, new backlinks, all in the same week. When something moved in GSC, I had no idea what caused it.",
    "Now each station gets exactly one SEO variable change per observation window. Title. Or description. Or page consolidation. Or authority signals. One thing. Then I wait 7 to 14 days.",
    "",
    "## Three experiments that taught me the most",
    "",
    "### 1. ZonePlan — 6 pages into 1",
    "We had six planner pages competing for the same search intent. 4,670 impressions. 5 clicks. 0.1% CTR.",
    "We merged all six into one comprehensive global-meeting-planner page: expanded from 45 to 230 lines, set canonicals, added 301 redirects, redesigned the homepage CTA.",
    "Observation window: 7 days. We are watching CTR, average position for \"meeting planner worldwide\" (265 impressions, 0 clicks), and index coverage.",
    "",
    "### 2. InvoicePad — title from noun to verb",
    "The title was \"Invoice Templates for Freelancers.\" Changed to \"Free Invoice Generator — Create and Download PDF Invoices Instantly.\"",
    "Why: 1,160 impressions and zero clicks. The old title described a catalog. The new title describes a tool that does something.",
    "Observation window: 7 days. Watching for any click from those 1,160 monthly impressions.",
    "",
    "### 3. PupVax — adding veterinary authority",
    "A puppy vaccine scheduler needs trust. We added AAHA, AVMA, and CDC citations, an amber medical disclaimer card, and changed the title to include \"2026 AAHA Guidelines.\"",
    "108 impressions on \"puppy vaccinations\" with zero clicks. The theory: users see the result, do not recognize the brand, and skip it. Authority signals might change that.",
    "",
    "## What I would do differently",
    "1. Build fewer pages, make each one stronger. We started with 745 URLs across 8 sites. Most get zero traffic. The ones that get impressions need better on-page signals, not more sibling pages.",
    "2. Separate page count from domain diversity. We published dozens of GitHub Gists and Issues. Great for getting content indexed. Terrible for building referring domain diversity. Dev.to, Medium, Pinterest, Quora each count as one domain. So do ten GitHub Gists.",
    "3. Start with the query, not the page. Every new page should answer a query that already has impressions in GSC. If the query is not there, the page is premature.",
    "",
    "## The tools",
    "All 8 tools are free, no sign-up, browser-based:",
    "- iworkviewer.com — open Apple iWork files online",
    "- livephotokit.com — HEIC and Live Photo converter",
    "- plantingcalendar.net — USDA zone planting calendar",
    "- freetdee.com — TDEE and macro calculator",
    "- babypercent.com — baby growth percentile calculator",
    "- invoicepad.net — free invoice generator",
    "- zoneplan.net — worldwide meeting planner",
    "- pupvax.com — puppy vaccine scheduler",
    "",
    "If you are running SEO experiments on your own projects, I would love to hear what variables you are testing and how long your observation windows are."
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

    # Fill title using keyboard.type() — proven method
    try:
        # Click on the title area - Medium uses contenteditable
        title_area = page.locator('[data-testid="editorTitle"]').first
        if not title_area.is_visible(timeout=3000):
            # Fallback: first contenteditable
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
        # Press Enter after title to start body
        page.keyboard.press("Enter")
        time.sleep(1)

        for i, para in enumerate(BODY_PARAGRAPHS):
            if para == "":
                # Empty paragraph = newline for spacing
                page.keyboard.press("Enter")
                time.sleep(0.3)
                continue

            if para.startswith("## "):
                # Heading - select heading style via keyboard shortcut
                page.keyboard.type(para, delay=5)
                page.keyboard.press("Enter")
                page.keyboard.press("Enter")
                time.sleep(0.5)
                continue

            if para.startswith("- "):
                # List item
                page.keyboard.type(para, delay=5)
                page.keyboard.press("Enter")
                time.sleep(0.3)
                continue

            # Normal paragraph
            page.keyboard.type(para, delay=5)
            page.keyboard.press("Enter")
            page.keyboard.press("Enter")
            time.sleep(0.5)

            if (i+1) % 5 == 0:
                print(f"Paragraph {i+1}/{len(BODY_PARAGRAPHS)} done")

        print("All paragraphs typed")
    except Exception as e:
        print(f"Body error: {e}")

    time.sleep(3)

    # Click Publish
    try:
        publish_btn = page.locator('button:has-text("Publish")').first
        if publish_btn.is_visible(timeout=3000):
            publish_btn.click()
            print("Clicked Publish")
            time.sleep(5)

            # Check if we need to confirm publish again
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
