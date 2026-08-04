"""Publish Dev.to article via CDP - execute fill and publish"""
import json, time, asyncio, websockets, sys, urllib.request

TITLE = "Worldwide Meeting Planner: How to Find One Fair Time Across 24 Time Zones"
CONTENT = """Scheduling meetings across continents is harder than it looks. You are not just comparing two clocks — you are managing daylight saving offsets, work-hour windows, and the silent assumption that "let's do 9 AM my time" works for everyone.

## The Real Problem Is Not Time Math

Most people think the problem is converting UTC offsets. It is not.

The real problem is:

- **24 possible start times** but only 2-3 that work for all attendees
- **Daylight saving transitions** that happen on different dates in different countries
- **Work-hour norms** — 9 AM in New York is 2 PM in London, but 9 AM in San Francisco is already 5 PM in London

## How ZonePlan Solves This

Instead of asking you to calculate, [ZonePlan](https://zoneplan.net) shows you a visual grid of all 24 hours across every time zone in your meeting. Overlapping work hours are highlighted. You pick the slot that minimizes inconvenience for the most people.

Try it free — no sign-up, no email, no installation.

## Why "Worldwide" Matters More Than "International"

An international meeting might be two countries. A worldwide meeting spans Asia, Europe, and the Americas simultaneously. That is when DST conflicts become unavoidable.

ZonePlan was built specifically for the three-continent meeting: 7 AM Pacific = 10 AM Eastern = 3 PM London = 7:30 PM Delhi. One click shows the overlap.

## Related Resources

- [Global Meeting Planner](https://zoneplan.net/global-meeting-planner/)
- [Schedule Meeting Across Time Zones](https://zoneplan.net/blog/schedule-meeting-across-time-zones/)
- [Free Time Zone Converter](https://zoneplan.net/)"""

async def get_devto_ws():
    resp = urllib.request.urlopen("http://localhost:9223/json")
    pages = json.loads(resp.read())
    for p in pages:
        if p.get('type') == 'page' and 'dev.to/new' in p.get('url', ''):
            if 'new#main-content' in p.get('url', '') or p.get('url', '').endswith('/new'):
                return p['webSocketDebuggerUrl']
    for p in pages:
        if p.get('type') == 'page' and 'dev.to' in p.get('url', ''):
            return p['webSocketDebuggerUrl']
    return None

async def main():
    ws_url = await get_devto_ws()
    if not ws_url:
        print("ERROR: Dev.to page not found")
        sys.exit(1)

    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        # Enable Runtime
        await ws.send(json.dumps({"id": 0, "method": "Runtime.enable"}))

        msg_id = [0]
        def next_id():
            msg_id[0] += 1
            return msg_id[0]

        async def evaluate(expr):
            mid = next_id()
            await ws.send(json.dumps({"id": mid, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get('id') == mid:
                    r = resp.get('result', {}).get('result', {})
                    val = r.get('value')
                    if r.get('type') == 'object' and r.get('subtype') == 'error':
                        return f"ERROR: {val}"
                    return val

        # Check URL first
        url = await evaluate("window.location.href")
        print(f"Current URL: {url}")

        # Navigate to /new if needed
        if '/new' not in str(url):
            print("Navigating to /new...")
            await ws.send(json.dumps({"id": next_id(), "method": "Page.navigate", "params": {"url": "https://dev.to/new"}}))
            time.sleep(3)

        # Fill title using DOM manipulation + input events
        title_js = f"""
        (() => {{
            const titleEl = document.querySelector('#article-form-title');
            if (!titleEl) return 'NO_TITLE_FIELD';

            // Focus and fill
            titleEl.focus();
            titleEl.value = '';

            // Use native input event for React-controlled components
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            nativeInputValueSetter.call(titleEl, {json.dumps(TITLE)});
            titleEl.dispatchEvent(new Event('input', {{ bubbles: true }}));

            return 'TITLE_FILLED: ' + titleEl.value.substring(0, 50);
        }})()
        """
        result = await evaluate(title_js)
        print(f"Title: {result}")

        # Fill body markdown
        body_js = f"""
        (() => {{
            const bodyEl = document.querySelector('textarea[name="body_markdown"], #article_body_markdown');
            if (!bodyEl) return 'NO_BODY_FIELD';

            bodyEl.focus();
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            nativeInputValueSetter.call(bodyEl, {json.dumps(CONTENT)});
            bodyEl.dispatchEvent(new Event('input', {{ bubbles: true }}));

            return 'BODY_FILLED: ' + bodyEl.value.length + ' chars';
        }})()
        """
        result = await evaluate(body_js)
        print(f"Body: {result}")

        # Add tags
        tags_result = await evaluate("""
        (() => {
            const tagInput = document.querySelector('#tag-input');
            if (!tagInput) return 'NO_TAG_INPUT';

            const tags = ['webdev', 'productivity', 'remotework', 'meeting'];
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;

            for (const tag of tags) {
                nativeInputValueSetter.call(tagInput, tag);
                tagInput.dispatchEvent(new Event('input', { bubbles: true }));
                tagInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }));
            }

            return 'TAGS_ADDED: ' + tags.join(', ');
        })()
        """)
        print(f"Tags: {tags_result}")

        time.sleep(2)

        # Click Publish button
        publish_result = await evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            const publishBtn = buttons.find(b =>
                b.textContent.toLowerCase().includes('publish')
            );
            if (publishBtn) {
                publishBtn.scrollIntoView();
                publishBtn.click();
                return 'CLICKED_PUBLISH: ' + publishBtn.textContent.trim();
            }
            return 'NO_PUBLISH_BUTTON. Buttons: ' + buttons.map(b => b.textContent.trim()).filter(Boolean).join(', ');
        })()
        """)
        print(f"Publish: {publish_result}")

        time.sleep(5)

        # Check result URL
        final_url = await evaluate("window.location.href")
        final_title = await evaluate("document.title")
        print(f"Final URL: {final_url}")
        print(f"Final Title: {final_title}")

        # Try to get published URL
        canonical = await evaluate("document.querySelector('link[rel=\"canonical\"]')?.href || 'NO_CANONICAL'")
        print(f"Canonical: {canonical}")

        print("DONE")

asyncio.run(main())
