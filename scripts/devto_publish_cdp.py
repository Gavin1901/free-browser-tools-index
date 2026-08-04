"""Publish to Dev.to via CDP WebSocket"""
import json, time, asyncio, websockets, sys

TITLE = "Worldwide Meeting Planner: How to Find One Fair Time Across 24 Time Zones"
CONTENT = """Scheduling meetings across continents is harder than it looks. You are not just comparing two clocks — you are managing daylight saving offsets, work-hour windows, and the silent assumption that "let's do 9 AM my time" works for everyone.

## The Real Problem Is Not Time Math

Most people think the problem is converting UTC offsets. It is not.

The real problem is:
* **24 possible start times** but only 2-3 that work for all attendees.
* **Daylight saving transitions** that happen on different dates in different countries.
* **Work-hour norms** — 9 AM in New York is 2 PM in London, but 9 AM in San Francisco is already 5 PM in London.

## How ZonePlan Solves This

Instead of asking you to calculate, [ZonePlan](https://zoneplan.net) shows you a visual grid of all 24 hours across every time zone in your meeting. Overlapping work hours are highlighted. You pick the slot that minimizes inconvenience for the most people.

Try it free — no sign-up, no email, no installation.

## Why "Worldwide" Matters More Than "International"

An international meeting might be two countries. A worldwide meeting spans Asia, Europe, and the Americas simultaneously. That is when DST conflicts become unavoidable.

ZonePlan was built specifically for the three-continent meeting: 7 AM Pacific = 10 AM Eastern = 3 PM London = 7:30 PM Delhi. One click shows the overlap.

## Related Resources

* [Global Meeting Planner](https://zoneplan.net/global-meeting-planner/)
* [Schedule Meeting Across Time Zones](https://zoneplan.net/blog/schedule-meeting-across-time-zones/)
* [Free Time Zone Converter](https://zoneplan.net/)"""

TAGS = ["webdev", "productivity", "remotework", "meeting"]

async def get_devto_page():
    """Get the Dev.to dashboard page from CDP"""
    import urllib.request
    resp = urllib.request.urlopen("http://localhost:9223/json")
    pages = json.loads(resp.read())
    for p in pages:
        if p.get('type') == 'page' and 'dev.to/dashboard' in p.get('url', ''):
            return p
    return None

async def evaluate(ws, expression):
    """Send Runtime.evaluate and get result"""
    msg = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": expression,
            "returnByValue": True
        }
    }
    await ws.send(json.dumps(msg))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == 1:
            result = resp.get('result', {}).get('result', {})
            return result.get('value')

async def main():
    page_info = await get_devto_page()
    if not page_info:
        print("ERROR: Dev.to dashboard page not found in CDP")
        sys.exit(1)

    ws_url = page_info['webSocketDebuggerUrl']
    print(f"Connecting to Dev.to page: {page_info['title']}")

    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        # Enable Runtime
        await ws.send(json.dumps({"id": 0, "method": "Runtime.enable"}))
        time.sleep(0.5)

        # Check current state
        state = await evaluate(ws, """
        (() => {
            const createBtn = document.querySelector('a[href="/new"]');
            const titleEl = document.querySelector('input[name="article[title]"], input[aria-label*="Title"], #article_title');
            const bodyEl = document.querySelector('textarea[name="article[body_markdown]"], #article_body_markdown');
            const editorEl = document.querySelector('.crayons-article-form__body textarea, .crayons-textfield[id*="body"]');
            return JSON.stringify({
                hasCreateBtn: !!createBtn,
                hasTitle: !!titleEl,
                hasBody: !!bodyEl,
                hasEditor: !!editorEl,
                url: window.location.href,
                title: document.title
            });
        })()
        """)
        print(f"Page state: {state}")

        # Navigate to new article page
        if 'dashboard' in str(state):
            print("On dashboard, navigating to /new...")
            await ws.send(json.dumps({
                "id": 2,
                "method": "Page.navigate",
                "params": {"url": "https://dev.to/new"}
            }))
            time.sleep(3)

        # Check new article page state
        state2 = await evaluate(ws, """
        (() => {
            const titleEl = document.querySelector('input[name="article[title]"], #article_title, input[aria-label*="Title"]');
            const bodyEl = document.querySelector('textarea[name="article[body_markdown]"], #article_body_markdown');
            const allInputs = [...document.querySelectorAll('input, textarea')].map(el => ({tag: el.tagName, name: el.name, id: el.id, type: el.type, placeholder: el.placeholder}));
            return JSON.stringify({
                url: window.location.href,
                hasTitle: !!titleEl,
                hasBody: !!bodyEl,
                inputs: allInputs.slice(0, 10)
            });
        })()
        """)
        print(f"New article state: {state2}")

        # Click on "Create Post" or "Write a Post" if still on dashboard
        click_result = await evaluate(ws, """
        (() => {
            const links = [...document.querySelectorAll('a')];
            const createLink = links.find(a =>
                a.href.includes('/new') ||
                a.textContent.toLowerCase().includes('create') ||
                a.textContent.toLowerCase().includes('write')
            );
            if (createLink) {
                createLink.click();
                return 'clicked: ' + createLink.href;
            }
            return 'no create link found. Links: ' + links.slice(0, 20).map(a => a.href + '|' + a.textContent.trim()).join(', ');
        })()
        """)
        print(f"Click result: {click_result}")

        time.sleep(3)

        # Final state check
        final_state = await evaluate(ws, """
        (() => {
            return JSON.stringify({
                url: window.location.href,
                title: document.title,
                allInputs: [...document.querySelectorAll('input[type="text"], input:not([type]), textarea')].map(el => ({
                    name: el.name, id: el.id, placeholder: el.placeholder, tag: el.tagName
                })).slice(0, 10)
            });
        })()
        """)
        print(f"Final state: {final_state}")

asyncio.run(main())
