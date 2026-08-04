"""Post to Product Hunt Self-Promotion forum via Playwright CDP"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

TITLE = "ZonePlan: Worldwide Meeting Planner Hit 258 Search Impressions for One Keyword"
BODY = """I built ZonePlan (zoneplan.net) as a free worldwide meeting planner, and one query — "meeting planner worldwide" — just crossed 258 Google impressions in 28 days.

The problem most meeting planners miss: worldwide meetings spanning Asia, Europe, and the Americas have conflicting DST transitions. ZonePlan shows a visual overlap grid of all 24 hours across every selected time zone, so you pick the one slot that works for everyone.

Current GSC data:
- 5 clicks, 4350 impressions in 28 days
- 30 pages indexed (up from 4 last week)
- "meeting planner worldwide": 258 impressions, 0 clicks (still working on CTR)

What I changed that helped indexing go from 4 to 30:
1. Fixed the global-meeting-planner page as the single canonical landing page
2. Optimized meta description to match search intent
3. Submitted sitemap + IndexNow consistently
4. Added independent domain backlinks (Dev.to, Medium)

Try it: https://zoneplan.net (free, no sign-up)

Would love feedback from anyone building SEO-first tools or working on meeting/productivity apps."""

def cdp_endpoint(port="9223"):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=10) as r:
        return json.load(r)["webSocketDebuggerUrl"]

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(cdp_endpoint("9223"))
        context = browser.contexts[0]

        # Find existing Product Hunt page or create new
        page = None
        for p in context.pages:
            if 'producthunt.com' in p.url:
                page = p
                break

        if not page:
            page = await context.new_page()

        await page.goto("https://www.producthunt.com/p/self-promotion", wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(5000)

        print(f"URL: {page.url}")

        # Check if logged in
        logged_in = await page.evaluate("""
        (() => {
            const body = document.body.innerText;
            return !body.includes('Sign in') && !body.includes('Log in');
        })()
        """)
        print(f"Logged in: {logged_in}")

        if not logged_in:
            print("Not logged in - login_blocked")
            return

        # Click "Start new thread" or "New post" button
        await page.evaluate("""
        (() => {
            const links = [...document.querySelectorAll('a, button')];
            const newThread = links.find(el =>
                (el.textContent || '').toLowerCase().includes('new thread') ||
                (el.textContent || '').toLowerCase().includes('start') ||
                (el.href && el.href.includes('/new'))
            );
            if (newThread) {
                newThread.click();
                return 'Clicked: ' + (newThread.textContent?.trim() || newThread.href);
            }
            return 'No new thread button';
        })()
        """)
        await page.wait_for_timeout(5000)

        print(f"After new thread click: {page.url}")

        # Check if we're on a post form
        has_form = await page.evaluate("""
        (() => {
            const textareas = [...document.querySelectorAll('textarea')];
            const titleInput = document.querySelector('input[name*="title"], input[placeholder*="title"], #post_title');
            const bodyTextarea = textareas.find(t => t.offsetParent !== null && (t.name?.includes('body') || t.id?.includes('body') || t.placeholder?.includes('text')));
            return JSON.stringify({
                hasTitle: !!titleInput,
                hasBody: !!bodyTextarea,
                textareaCount: textareas.filter(t => t.offsetParent !== null).length,
                url: window.location.href
            });
        })()
        """)
        print(f"Form state: {has_form}")

        # Try to fill form
        # Fill title
        title_filled = await page.evaluate(f"""
        (() => {{
            const titleInput = document.querySelector('input[name*="title"], input[placeholder*="title"], #post_title, input[aria-label*="title" i]');
            if (titleInput) {{
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(titleInput, {json.dumps(TITLE)});
                titleInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return 'Filled: ' + titleInput.value?.substring(0, 50);
            }}
            return 'No title input';
        }})()
        """)
        print(f"Title: {title_filled}")

        # Fill body
        body_filled = await page.evaluate(f"""
        (() => {{
            const textareas = [...document.querySelectorAll('textarea')].filter(t => t.offsetParent !== null);
            const bodyEl = textareas.find(t =>
                t.name?.includes('body') || t.id?.includes('body') ||
                t.placeholder?.includes('text') || t.placeholder?.includes('content') ||
                t.getAttribute('aria-label')?.includes('body')
            ) || textareas[0];

            if (bodyEl) {{
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                nativeInputValueSetter.call(bodyEl, {json.dumps(BODY)});
                bodyEl.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return 'Filled: ' + bodyEl.value?.length + ' chars';
            }}
            return 'No body textarea. Count: ' + textareas.length;
        }})()
        """)
        print(f"Body: {body_filled}")

        # Submit
        await page.wait_for_timeout(2000)
        submit = await page.evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            const submitBtn = buttons.find(b => {
                const text = b.textContent.toLowerCase().trim();
                return text === 'submit' || text === 'post' || text === 'publish' || text === 'create thread';
            });
            if (submitBtn && submitBtn.offsetParent !== null) {
                submitBtn.click();
                return 'Clicked: ' + submitBtn.textContent.trim();
            }
            return 'No submit button';
        })()
        """)
        print(f"Submit: {submit}")

        await page.wait_for_timeout(10000)

        final_url = page.url
        print(f"Final URL: {final_url}")

        if '/self-promotion/' in final_url and page.url != "https://www.producthunt.com/p/self-promotion":
            print(f"POSTED: {final_url}")
        else:
            body_text = await page.evaluate("document.body.innerText.substring(0, 300)")
            print(f"Page text preview: {body_text}")

asyncio.run(main())
