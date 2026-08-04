"""Publish Medium article via CDP"""
import json, time, asyncio, websockets, sys, urllib.request

TITLE = "Worldwide Meeting Planner: Finding Fair Times Across 24 Time Zones"
CONTENT = """Scheduling meetings across continents is harder than it looks. You are not just comparing two clocks—you are managing daylight saving offsets, work-hour windows, and the silent assumption that "let's do 9 AM my time" works for everyone.

## The Real Problem Is Not Time Math

Most people think the problem is converting UTC offsets. It is not.

The real problem is: 24 possible start times but only 2-3 that work for all attendees. Daylight saving transitions happen on different dates in different countries. Work-hour norms vary—9 AM in New York is 2 PM in London, but 9 AM in San Francisco is already 5 PM in London.

## How ZonePlan Solves This

Instead of asking you to calculate, ZonePlan shows you a visual grid of all 24 hours across every time zone in your meeting. Overlapping work hours are highlighted. You pick the slot that minimizes inconvenience for the most people.

Try it free at zoneplan.net—no sign-up, no email, no installation.

## Why Worldwide Matters More Than International

An international meeting might be two countries. A worldwide meeting spans Asia, Europe, and the Americas simultaneously. That is when DST conflicts become unavoidable.

ZonePlan was built specifically for the three-continent meeting: 7 AM Pacific = 10 AM Eastern = 3 PM London = 7:30 PM Delhi. One click shows the overlap.

Related:
- Global Meeting Planner: zoneplan.net/global-meeting-planner/
- Schedule Meeting Across Time Zones: zoneplan.net/blog/schedule-meeting-across-time-zones/
- Free Time Zone Converter: zoneplan.net/"""

async def get_medium_ws():
    resp = urllib.request.urlopen("http://localhost:9223/json")
    pages = json.loads(resp.read())
    for p in pages:
        if p.get('type') == 'page' and 'medium.com/new-story' in p.get('url', ''):
            return p['webSocketDebuggerUrl']
    return None

async def main():
    ws_url = await get_medium_ws()
    if not ws_url:
        print("ERROR: Medium new-story page not found")
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
                    r = resp.get('result', {}).get('result', {})
                    return r.get('value')

        url = await evaluate("window.location.href")
        print(f"Current URL: {url}")

        # Check for draft saved indicator and title field
        state = await evaluate("""
        (() => {
            const heading = document.querySelector('h1, h2, h3, [data-testid="editorTitle"]');
            const titleArea = document.querySelector('[data-testid="editorTitle"], [aria-label*="Title"], h3[data-testid="editorTitleWrite"]');
            const paragraphs = document.querySelectorAll('[data-testid="editorParagraph"], p[data-testid="editorParagraphWrite"]');
            const allEditable = [...document.querySelectorAll('[contenteditable="true"]')];
            return JSON.stringify({
                hasHeading: !!heading,
                headingText: heading?.textContent?.substring(0, 30),
                hasTitleArea: !!titleArea,
                paragraphCount: paragraphs.length,
                editableCount: allEditable.length,
                url: window.location.href
            });
        })()
        """)
        print(f"State: {state}")

        # Medium uses contenteditable elements. Find title and body
        # Click on the title area first
        title_result = await evaluate("""
        (() => {
            // Medium's editor: title is typically the first h3 or contenteditable
            const allEditable = [...document.querySelectorAll('[contenteditable="true"]')];
            if (allEditable.length === 0) return 'NO_EDITABLE';

            // First contenteditable is usually the title
            const titleEl = allEditable[0];
            titleEl.focus();
            titleEl.click();

            // Clear existing and type title
            titleEl.textContent = '';
            titleEl.innerText = '';

            return 'TITLE_FOCUSED. Editables: ' + allEditable.length;
        })()
        """)
        print(f"Title focus: {title_result}")

        # Now type the title using keyboard events
        title_chars = TITLE
        for i, char in enumerate(title_chars):
            key = char
            code = f'Key{char.upper()}' if char.isalpha() else (
                'Space' if char == ' ' else
                'Colon' if char == ':' else
                'Minus' if char == '-' else
                'Digit' + char if char.isdigit() else None
            )

            await ws.send(json.dumps({
                "id": next_id(),
                "method": "Input.dispatchKeyEvent",
                "params": {
                    "type": "char",
                    "text": char,
                    "unmodifiedText": char,
                    "key": key,
                    "code": code or '',
                    "windowsVirtualKeyCode": ord(char)
                }
            }))
            if i % 50 == 0:
                await asyncio.sleep(0.05)

        await asyncio.sleep(1)

        # Check title was typed
        title_check = await evaluate("document.querySelector('[contenteditable=\"true\"]')?.textContent?.substring(0, 50)")
        print(f"Title check: {title_check}")

        # Find body area and type content
        body_result = await evaluate("""
        (() => {
            const allEditable = [...document.querySelectorAll('[contenteditable="true"]')];
            if (allEditable.length < 2) return 'NOT_ENOUGH_EDITABLE';

            // Second contenteditable is typically the body
            const bodyEl = allEditable[1];
            bodyEl.focus();
            bodyEl.click();

            return 'BODY_FOCUSED. Content: ' + (bodyEl.textContent?.substring(0, 20) || 'empty');
        })()
        """)
        print(f"Body focus: {body_result}")

        # Type body content via clipboard paste approach
        # Medium doesn't work well with character-by-character typing for long content
        paste_result = await evaluate(f"""
        (() => {{
            const allEditable = [...document.querySelectorAll('[contenteditable="true"]')];
            if (allEditable.length < 2) return 'NO_BODY';

            const bodyEl = allEditable[1];
            bodyEl.focus();

            const dataTransfer = new DataTransfer();
            dataTransfer.setData('text/plain', {json.dumps(CONTENT)});

            const pasteEvent = new ClipboardEvent('paste', {{
                bubbles: true,
                cancelable: true,
                clipboardData: dataTransfer
            }});

            bodyEl.dispatchEvent(pasteEvent);

            return 'PASTE_TRIGGERED. Chars: ' + bodyEl.textContent.length;
        }})()
        """)
        print(f"Paste: {paste_result}")

        await asyncio.sleep(3)

        # Check content was inserted
        content_check = await evaluate("""
        (() => {
            const allEditable = [...document.querySelectorAll('[contenteditable="true"]')];
            return JSON.stringify(allEditable.map((el, i) => ({
                index: i,
                length: el.textContent.length,
                preview: el.textContent.substring(0, 50)
            })));
        })()
        """)
        print(f"Content check: {content_check}")

        # Wait for DraftSaved
        await asyncio.sleep(3)
        draft_state = await evaluate("document.body.innerText.includes('Draft saved') || document.body.innerText.includes('Saved')")
        print(f"Draft saved: {draft_state}")

        # Click Publish button
        pub_result = await evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            const pubBtn = buttons.find(b =>
                b.textContent.includes('Publish') || b.textContent.includes('publish')
            );
            if (pubBtn) {
                pubBtn.click();
                return 'CLICKED: ' + pubBtn.textContent.trim();
            }
            // Medium might have "Ready to publish?" button
            const readyBtn = buttons.find(b => b.textContent.includes('Ready'));
            if (readyBtn) {
                readyBtn.click();
                return 'CLICKED_READY: ' + readyBtn.textContent.trim();
            }
            return 'NO_PUB_BTN. Buttons: ' + buttons.map(b => b.textContent.trim()).filter(Boolean).slice(0, 10).join(', ');
        })()
        """)
        print(f"Publish click: {pub_result}")

        await asyncio.sleep(5)

        final_url = await evaluate("window.location.href")
        final_title = await evaluate("document.title")
        print(f"Final URL: {final_url}")
        print(f"Final Title: {final_title}")
        print("DONE")

asyncio.run(main())
