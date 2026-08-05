"""Publish Dev.to article via Playwright CDP."""
from playwright.sync_api import sync_playwright
import time

TITLE = "I Merged 6 Near-Identical Planner Pages Into 1 — Here Is What Happened to Our SEO"

BODY = """When you build a free tool, the natural instinct is to create a page for every use case. So we built:

- A global meeting planner page
- An international meeting planner page
- A meeting planner page
- A remote team time zone planner page
- A UTC converter page
- A world clock planner page

Six pages. Same core function: help people find a meeting time across time zones.

And Google punished us for it.

## The numbers before consolidation

ZonePlan had **4,670 monthly impressions** across all queries. Sounds decent, right?

Only **5 clicks**. Total. A 0.1% CTR.

The top non-brand queries told the story:

- "meeting planner worldwide" — 265 impressions, 0 clicks
- "global meeting planner" — 132 impressions, 0 clicks
- "international meeting planner" — 120 impressions, 0 clicks

Google was showing our pages. People were not clicking. Why?

Because when Google sees six near-identical pages competing for the same search intent, it splits ranking signals across all of them. None ranks well enough to earn trust. None looks like the definitive answer.

## What we changed

On August 4, we made one change but it touched everything:

1. **Chose a single canonical page**: global-meeting-planner
2. **Expanded it from 45 lines to 230 lines**: real substance with usage steps, 4 scenario cards, time zone fairness logic, remote team best practices, 6 FAQ items with schema markup, 5 internal tool links
3. **Set canonical tags**: all other planner pages now point to global-meeting-planner
4. **Added 3 permanent 301 redirects**: international, utc, and world-clock pages redirect via Cloudflare
5. **Redesigned the homepage**: replaced 6 parallel planner cards with one CTA button

## The theory

This is not a content volume problem. It is a **signal concentration problem**.

Six pages each with about 45 lines of thin content, weak internal links, no clear differentiation. Google has to guess which one matters. It guesses wrong.

One page with 230 lines of structured content, clear internal link signals, and no competition from sister pages. Google has exactly one target to evaluate.

## What we are measuring (7-day observation window)

- CTR on global-meeting-planner
- Average position for "meeting planner worldwide"
- Index coverage (currently 30 indexed / 84 not indexed)
- Overall site clicks from 4,670 impressions

## The tool

ZonePlan is a free worldwide meeting planner. No sign-up. No app. Enter cities, see working-hour overlap instantly.

[https://zoneplan.net](https://zoneplan.net)

---

**The bigger lesson**: When your SEO is stuck, the answer is rarely "write more pages." Often it is "make the pages you already have count for more."

I am running this experiment across 8 free browser tools. Each station gets one variable change per observation window. No stacking. No guessing. Just isolated SEO experiments with GSC data to confirm or refute.

If you are building free tools, share what SEO variables you are testing in the comments.
"""

# Tags
TAGS = ["seo", "webdev", "tutorial", "productivity"]

print("Connecting to CDP...")
with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp("http://localhost:9223")
    ctx = browser.contexts[0]
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    # Navigate to Dev.to new post
    print("Navigating to /new...")
    page.goto("https://dev.to/new", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    print(f"Current URL: {page.url}")

    # Fill title
    title_el = page.locator('input[placeholder*="Title"]').first
    title_el.click()
    time.sleep(0.5)
    page.keyboard.type(TITLE, delay=10)
    print("Title filled")
    time.sleep(1)

    # Fill body via textarea
    body_el = page.locator("textarea#article_body_markdown")
    if body_el.is_visible(timeout=2000):
        body_el.click()
        page.keyboard.type(BODY, delay=3)
        print("Body filled via textarea")
    else:
        print("Textarea not found, trying contenteditable...")
        ce = page.locator('[contenteditable="true"]').first
        ce.click()
        page.keyboard.type(BODY, delay=3)
        print("Body filled via contenteditable")

    time.sleep(2)

    # Add tags
    try:
        tag_input = page.locator('input[placeholder*="tag"]').first
        for tag in TAGS:
            tag_input.fill(tag)
            time.sleep(0.5)
            page.keyboard.press("Enter")
            time.sleep(0.3)
            print(f"Tag added: {tag}")
    except Exception as e:
        print(f"Tags error: {e}")

    time.sleep(1)

    # Click Publish
    try:
        publish_btn = page.locator('button:has-text("Publish")').first
        publish_btn.click()
        print("Clicked Publish")
        time.sleep(8)

        # Get final URL
        final_url = page.url
        print(f"Final URL: {final_url}")

        # Try to extract article URL from page
        try:
            canonical = page.locator('link[rel="canonical"]').get_attribute("href")
            print(f"Canonical: {canonical}")
        except:
            print("Could not extract canonical")

    except Exception as e:
        print(f"Publish error: {e}")
        # Save screenshot for debugging
        page.screenshot(path="D:/Tools/ai-tool-index/logs/2026-08-05-devto-error.png")
        print("Error screenshot saved")

    browser.close()
    print("DONE")
