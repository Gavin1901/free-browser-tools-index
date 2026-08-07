"""Fix Medium links: go to article -> click Edit -> fix -> save."""
from playwright.sync_api import sync_playwright
import time

ARTICLE_URL = "https://medium.com/@lg695101011/puppy-vaccination-schedule-what-every-new-owner-misses-113f40a5deb2"

with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp("http://localhost:9223")
    ctx = browser.contexts[0]
    page = ctx.new_page()

    # 1. Go to article
    page.goto(ARTICLE_URL, wait_until="networkidle", timeout=30000)
    time.sleep(3)
    print(f"Article page: {page.url}")

    # 2. Click the Edit button
    try:
        edit_btn = page.locator('a[href*="/edit"], button:has-text("Edit")').first
        if edit_btn.is_visible(timeout=5000):
            edit_btn.click()
            print("Clicked Edit")
            time.sleep(4)
        else:
            print("No Edit button visible, navigating to edit URL directly")
            page.goto("https://medium.com/p/113f40a5deb2/edit", wait_until="networkidle", timeout=30000)
            time.sleep(5)
    except Exception as e:
        print(f"Edit click failed: {e}, navigating directly")
        page.goto("https://medium.com/p/113f40a5deb2/edit", wait_until="networkidle", timeout=30000)
        time.sleep(5)

    print(f"Edit page: {page.url}")

    # 3. Wait for editor to fully render
    time.sleep(3)

    # 4. Check editor content
    info = page.evaluate("""
        (function() {
            var eds = document.querySelectorAll('[contenteditable="true"]');
            var out = {eds: eds.length};
            if (eds.length >= 2) {
                // Body text - try different ways
                out.bodyHTML = eds[1].innerHTML.length;
                out.bodyTextContent = eds[1].textContent.length;
                out.bodyInnerText = eds[1].innerText ? eds[1].innerText.length : 0;
                // Sample of HTML
                out.htmlSample = eds[1].innerHTML.substring(0, 2000);
            }
            out.pageText = document.body.innerText.substring(0, 500);
            return JSON.stringify(out);
        })()
    """)
    import json
    info = json.loads(info)
    print(f"Editables: {info.get('eds',0)}")
    print(f"Body HTML len: {info.get('bodyHTML',0)}")
    print(f"Body textContent len: {info.get('bodyTextContent',0)}")
    print(f"Body innerText len: {info.get('bodyInnerText',0)}")

    # 5. Check for pupvax/github in editor
    if info.get('htmlSample', ''):
        has_pupvax = 'pupvax' in info['htmlSample'].lower()
        has_github = 'github' in info['htmlSample'].lower()
        print(f"Has pupvax in HTML: {has_pupvax}")
        print(f"Has github in HTML: {has_github}")

        # Print first 300 chars
        print(f"HTML sample: {info['htmlSample'][:500]}")

    # 6. Now fix links in the editor
    fix_result = page.evaluate("""
        (function() {
            var eds = document.querySelectorAll('[contenteditable="true"]');
            if (eds.length < 2) return "NO BODY EDITOR";
            var ed = eds[1];
            ed.focus();

            var html = ed.innerHTML;

            // Replace plain-text pupvax.com/PupVax.com with <a> links
            var fixed = 0;

            // Method 1: Direct regex replace on innerHTML
            var newHTML = html
                .replace(/(?<!["=])(?<!href=")(?<!>)(pupvax\\.com)/gi, '<a href="https://pupvax.com/">$1</a>')
                .replace(/(?<!["=])(?<!href=")(?<!>)(PupVax\\.com)/g, '<a href="https://pupvax.com/">$1</a>');

            if (newHTML !== html) {
                ed.innerHTML = newHTML;
                fixed = 1;
            }

            ed.dispatchEvent(new Event('input', {bubbles: true}));
            ed.dispatchEvent(new Event('change', {bubbles: true}));

            return "Fixed: " + fixed + ". Links now: " + ed.querySelectorAll('a').length;
        })()
    """)
    print(f"Link fix: {fix_result}")
    time.sleep(2)

    # 7. Save
    try:
        # Try Ctrl+S first
        page.keyboard.press("Control+s")
        time.sleep(3)

        # Check for publish/save button
        for label in ["Publish", "Save and publish", "Save"]:
            btn = page.locator(f'button:has-text("{label}")').first
            if btn.is_visible(timeout=2000):
                if not btn.is_disabled():
                    btn.click()
                    print(f"Clicked: {label}")
                    time.sleep(5)
                    break
                else:
                    print(f"Button '{label}' is disabled")

        # Check for confirm
        pub2 = page.locator('button:has-text("Publish")').first
        if pub2.is_visible(timeout=2000) and not pub2.is_disabled():
            pub2.click()
            print("Clicked confirm Publish")
            time.sleep(5)
    except Exception as e:
        print(f"Save error: {e}")

    # 8. Verify
    page.goto(ARTICLE_URL, wait_until="networkidle", timeout=30000)
    time.sleep(3)
    links = page.evaluate("""
        (function() {
            var as = document.querySelectorAll('a');
            var out = [];
            for (var a of as) {
                var href = a.href || '';
                if (href.indexOf('pupvax') >= 0 || href.indexOf('github.com/Gavin') >= 0) {
                    out.push(href);
                }
            }
            return out;
        })()
    """)
    print(f"Verified pupvax/github links: {links}")
    print(f"Final URL: {page.url}")
    print("DONE")
