"""Publish Medium via CDP - native keyboard typing approach"""
import json, time, asyncio, websockets, sys, urllib.request

TITLE = "Worldwide Meeting Planner: Finding Fair Times Across 24 Time Zones"

PARAGRAPHS = [
    'Scheduling meetings across continents is harder than it looks. You are not just comparing two clocks — you are managing daylight saving offsets, work-hour windows, and the silent assumption that "let\'s do 9 AM my time" works for everyone.',
    '## The Real Problem Is Not Time Math',
    'Most people think the problem is converting UTC offsets. It is not.',
    'The real problem is: 24 possible start times but only 2-3 that work for all attendees. Daylight saving transitions happen on different dates in different countries. Work-hour norms vary—9 AM in New York is 2 PM in London, but 9 AM in San Francisco is already 5 PM in London.',
    '## How ZonePlan Solves This',
    'Instead of asking you to calculate, ZonePlan (zoneplan.net) shows you a visual grid of all 24 hours across every time zone in your meeting. Overlapping work hours are highlighted. You pick the slot that minimizes inconvenience for the most people.',
    'Try it free at zoneplan.net — no sign-up, no email, no installation.',
    '## Why Worldwide Matters More Than International',
    'An international meeting might be two countries. A worldwide meeting spans Asia, Europe, and the Americas simultaneously. That is when DST conflicts become unavoidable.',
    'ZonePlan was built specifically for the three-continent meeting: 7 AM Pacific = 10 AM Eastern = 3 PM London = 7:30 PM Delhi. One click shows the overlap.',
    'Related resources:',
    '- Global Meeting Planner: zoneplan.net/global-meeting-planner/',
    '- Schedule Meeting Across Time Zones: zoneplan.net/blog/schedule-meeting-across-time-zones/',
    '- Free Time Zone Converter: zoneplan.net/',
]

async def get_medium_ws():
    resp = urllib.request.urlopen("http://localhost:9223/json")
    pages = json.loads(resp.read())
    for p in pages:
        if p.get('type') == 'page' and 'medium.com' in p.get('url', ''):
            return p['webSocketDebuggerUrl']
    return None

async def type_text(ws, text, get_id):
    """Type text character by character via CDP Input.dispatchKeyEvent"""
    for i, char in enumerate(text):
        params = {
            "type": "char",
            "text": char,
            "unmodifiedText": char
        }
        await ws.send(json.dumps({
            "id": get_id(),
            "method": "Input.dispatchKeyEvent",
            "params": params
        }))
        if i % 20 == 0:
            await asyncio.sleep(0.01)
    await asyncio.sleep(0.1)
    # Press Enter after each paragraph
    await ws.send(json.dumps({
        "id": get_id(),
        "method": "Input.dispatchKeyEvent",
        "params": {
            "type": "keyDown",
            "key": "Enter",
            "code": "Enter",
            "keyCode": 13
        }
    }))
    await ws.send(json.dumps({
        "id": get_id(),
        "method": "Input.dispatchKeyEvent",
        "params": {
            "type": "keyUp",
            "key": "Enter",
            "code": "Enter",
            "keyCode": 13
        }
    }))

async def main():
    ws_url = await get_medium_ws()
    if not ws_url:
        print("ERROR: Medium page not found")
        sys.exit(1)

    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        await ws.send(json.dumps({"id": 0, "method": "Runtime.enable"}))
        await ws.send(json.dumps({"id": 1, "method": "Input.enable"}))

        msg_id = [10]
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

        # Navigate to fresh new-story
        await ws.send(json.dumps({"id": next_id(), "method": "Page.navigate", "params": {"url": "https://medium.com/new-story"}}))
        await asyncio.sleep(3)

        url = await evaluate("window.location.href")
        print(f"URL: {url}")

        # Click on title area (first editable)
        await evaluate("""
        (() => {
            const els = [...document.querySelectorAll('[contenteditable="true"]')];
            if (els.length > 0) {
                els[0].focus();
                els[0].click();
            }
        })()
        """)
        await asyncio.sleep(0.5)

        # Type title natively
        print("Typing title...")
        await type_text(ws, TITLE, next_id)

        await asyncio.sleep(1)

        # Click on body area (second editable)
        await evaluate("""
        (() => {
            const els = [...document.querySelectorAll('[contenteditable="true"]')];
            if (els.length > 1) {
                els[1].focus();
                els[1].click();
            }
        })()
        """)
        await asyncio.sleep(0.5)

        # Type body paragraph by paragraph
        print(f"Typing {len(PARAGRAPHS)} paragraphs...")
        for i, para in enumerate(PARAGRAPHS):
            await type_text(ws, para, next_id)
            await asyncio.sleep(0.5)
            # Check draft saved
            draft = await evaluate("document.body.innerText.includes('Draft saved') || document.body.innerText.includes('Saved')")
            print(f"  Para {i+1}/{len(PARAGRAPHS)} typed, draft saved: {draft}")

        await asyncio.sleep(3)

        # Check final content
        check = await evaluate("""
        (() => {
            const els = [...document.querySelectorAll('[contenteditable="true"]')];
            return JSON.stringify(els.map(el => ({
                textLen: el.textContent?.length,
                htmlLen: el.innerHTML?.length
            })));
        })()
        """)
        print(f"Content check: {check}")

        # Try clicking Publish
        pub = await evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            const pubBtn = buttons.find(b => b.textContent.trim() === 'Publish' && b.offsetParent !== null);
            if (pubBtn) { pubBtn.click(); return 'CLICKED_PUBLISH'; }
            return 'NO_PUBLISH_BTN';
        })()
        """)
        print(f"Publish: {pub}")

        await asyncio.sleep(5)

        # Check if moved to publish preview
        modal = await evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            return JSON.stringify({
                url: window.location.href,
                buttons: buttons.map(b => b.textContent.trim()).filter(Boolean).slice(0, 10),
                hasDialog: document.querySelectorAll('[role="dialog"]').length > 0
            });
        })()
        """)
        print(f"Post-publish state: {modal}")

        # Click second confirm Publish if available
        confirm = await evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            const pubBtns = buttons.filter(b =>
                b.textContent.trim().toLowerCase().includes('publish') && b.offsetParent !== null
            );
            if (pubBtns.length > 0) {
                pubBtns[pubBtns.length - 1].click();
                return 'CLICKED: count=' + pubBtns.length;
            }
            return 'NO_PUB_BTN';
        })()
        """)
        print(f"Confirm: {confirm}")

        await asyncio.sleep(8)

        final_url = await evaluate("window.location.href")
        final_title = await evaluate("document.title")
        canonical = await evaluate("document.querySelector('link[rel=\"canonical\"]')?.href || 'NO_CANONICAL'")
        pub_url = await evaluate("""
        (() => {
            const link = document.querySelector('a[href*=\"/@lg695101011/\"]');
            if (link) return link.href;
            const input = document.querySelector('input[value*=\"medium.com\"]');
            if (input) return input.value;
            return null;
        })()
        """)
        print(f"Final URL: {final_url}")
        print(f"Final Title: {final_title}")
        print(f"Canonical: {canonical}")
        print(f"Published URL: {pub_url}")
        print("DONE")

asyncio.run(main())
