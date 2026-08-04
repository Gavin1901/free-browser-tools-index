"""Publish Medium via CDP - attempt 2 with execCommand"""
import json, time, asyncio, websockets, sys, urllib.request

TITLE = "Worldwide Meeting Planner: Finding Fair Times Across 24 Time Zones"
CONTENT_HTML = """<p>Scheduling meetings across continents is harder than it looks. You are not just comparing two clocks—you are managing daylight saving offsets, work-hour windows, and the silent assumption that "let's do 9 AM my time" works for everyone.</p>
<h2>The Real Problem Is Not Time Math</h2>
<p>Most people think the problem is converting UTC offsets. It is not.</p>
<p>The real problem is: 24 possible start times but only 2-3 that work for all attendees. Daylight saving transitions happen on different dates in different countries. Work-hour norms vary—9 AM in New York is 2 PM in London, but 9 AM in San Francisco is already 5 PM in London.</p>
<h2>How ZonePlan Solves This</h2>
<p>Instead of asking you to calculate, <a href="https://zoneplan.net">ZonePlan</a> shows you a visual grid of all 24 hours across every time zone in your meeting. Overlapping work hours are highlighted. You pick the slot that minimizes inconvenience for the most people.</p>
<p>Try it free at zoneplan.net—no sign-up, no email, no installation.</p>
<h2>Why Worldwide Matters More Than International</h2>
<p>An international meeting might be two countries. A worldwide meeting spans Asia, Europe, and the Americas simultaneously. That is when DST conflicts become unavoidable.</p>
<p>ZonePlan was built specifically for the three-continent meeting: 7 AM Pacific = 10 AM Eastern = 3 PM London = 7:30 PM Delhi. One click shows the overlap.</p>
<p>Related:</p>
<ul>
<li><a href="https://zoneplan.net/global-meeting-planner/">Global Meeting Planner</a></li>
<li><a href="https://zoneplan.net/blog/schedule-meeting-across-time-zones/">Schedule Meeting Across Time Zones</a></li>
<li><a href="https://zoneplan.net/">Free Time Zone Converter</a></li>
</ul>"""

async def get_medium_ws():
    resp = urllib.request.urlopen("http://localhost:9223/json")
    pages = json.loads(resp.read())
    for p in pages:
        if p.get('type') == 'page' and 'medium.com' in p.get('url', ''):
            return p['webSocketDebuggerUrl']
    return None

async def main():
    ws_url = await get_medium_ws()
    if not ws_url:
        print("ERROR: Medium page not found")
        sys.exit(1)

    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
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
                    return resp.get('result', {}).get('result', {}).get('value')

        url = await evaluate("window.location.href")
        print(f"URL: {url}")

        # If not on new-story, navigate
        if 'new-story' not in str(url):
            await ws.send(json.dumps({"id": next_id(), "method": "Page.navigate", "params": {"url": "https://medium.com/new-story"}}))
            await asyncio.sleep(3)

        # Find editables
        editables = await evaluate("""
        (() => {
            const els = [...document.querySelectorAll('[contenteditable="true"]')];
            return JSON.stringify(els.map((el, i) => ({
                index: i,
                tag: el.tagName,
                role: el.getAttribute('role'),
                aria: el.getAttribute('aria-label'),
                placeholder: el.getAttribute('data-placeholder') || el.getAttribute('placeholder'),
                text: el.textContent?.substring(0, 30)
            })));
        })()
        """)
        print(f"Editables: {editables}")

        # Strategy: click first editable (title), type title via innerText
        title_filled = await evaluate(f"""
        (() => {{
            const els = [...document.querySelectorAll('[contenteditable="true"]')];
            if (els.length < 2) return 'NOT_ENOUGH';

            // Title = first editable
            const titleEl = els[0];
            titleEl.focus();
            titleEl.click();

            // Try innerText
            titleEl.innerText = {json.dumps(TITLE)};

            // Also dispatch input event
            titleEl.dispatchEvent(new Event('input', {{ bubbles: true }}));

            return 'TITLE_SET: ' + titleEl.innerText?.substring(0, 50);
        }})()
        """)
        print(f"Title: {title_filled}")

        await asyncio.sleep(1)

        # Body = second editable, use innerHTML
        body_filled = await evaluate(f"""
        (() => {{
            const els = [...document.querySelectorAll('[contenteditable="true"]')];
            if (els.length < 2) return 'NO_BODY_EL';

            const bodyEl = els[1];
            bodyEl.focus();
            bodyEl.click();

            // Use innerHTML
            bodyEl.innerHTML = {json.dumps(CONTENT_HTML)};

            // Dispatch events
            bodyEl.dispatchEvent(new Event('input', {{ bubbles: true }}));
            bodyEl.dispatchEvent(new Event('change', {{ bubbles: true }}));

            return 'BODY_SET: ' + bodyEl.innerText?.length + ' text chars, ' + bodyEl.innerHTML?.length + ' html chars';
        }})()
        """)
        print(f"Body: {body_filled}")

        await asyncio.sleep(2)

        # Check draft state
        draft = await evaluate("document.body.innerText.includes('Draft saved')")
        print(f"Draft saved visible: {draft}")

        # Check content persisted
        check = await evaluate("""
        (() => {
            const els = [...document.querySelectorAll('[contenteditable="true"]')];
            return JSON.stringify(els.map((el, i) => ({
                index: i,
                textLen: el.textContent?.length,
                htmlLen: el.innerHTML?.length,
                preview: el.textContent?.substring(0, 40)
            })));
        })()
        """)
        print(f"Content check: {check}")

        await asyncio.sleep(2)

        # Click Publish
        pub = await evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            const pubBtn = buttons.find(b => b.textContent.trim() === 'Publish');
            if (pubBtn) {
                pubBtn.click();
                return 'CLICKED_PUBLISH';
            }
            return 'NO_PUBLISH_BTN';
        })()
        """)
        print(f"Publish: {pub}")

        await asyncio.sleep(8)

        final_url = await evaluate("window.location.href")
        final_title = await evaluate("document.title")
        canonical = await evaluate("document.querySelector('link[rel=\"canonical\"]')?.href || 'NO_CANONICAL'")
        print(f"Final URL: {final_url}")
        print(f"Final Title: {final_title}")
        print(f"Canonical: {canonical}")
        print("DONE")

asyncio.run(main())
