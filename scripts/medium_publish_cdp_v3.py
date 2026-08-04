"""Publish Medium via CDP - attempt 3, handle publish modal"""
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

        # Check what's on page now - did content persist from v2?
        check = await evaluate("""
        (() => {
            const els = [...document.querySelectorAll('[contenteditable="true"]')];
            return JSON.stringify({
                editables: els.map(el => ({textLen: el.textContent?.length, preview: el.textContent?.substring(0, 30)})),
                buttons: [...document.querySelectorAll('button')].map(b => b.textContent.trim()).filter(Boolean),
                dialogs: [...document.querySelectorAll('[role="dialog"], [role="alertdialog"]')].length,
                modals: [...document.querySelectorAll('.modal, [class*="modal"], [class*="dialog"], [class*="overlay"]')].length
            });
        })()
        """)
        print(f"Page state: {check}")

        # If content is still there from previous attempt, just try clicking through
        if 'new-story' in str(url):
            content_check = await evaluate("""
            (() => {
                const els = [...document.querySelectorAll('[contenteditable="true"]')];
                return els[0]?.textContent?.length || 0;
            })()
            """)
            if content_check and int(content_check) > 0:
                print("Content already exists, clicking Publish...")
                # Click Publish
                pub = await evaluate("""
                (() => {
                    const buttons = [...document.querySelectorAll('button')];
                    const pubBtn = buttons.find(b => b.textContent.trim() === 'Publish');
                    if (pubBtn) { pubBtn.click(); return 'CLICKED'; }
                    return 'NOT_FOUND';
                })()
                """)
                print(f"Publish click: {pub}")
                await asyncio.sleep(3)

        # Look for publish confirmation modal
        modal_state = await evaluate("""
        (() => {
            const dialogs = [...document.querySelectorAll('[role="dialog"]')];
            const storyPreview = document.querySelector('[data-testid="storyPreview"], .storyPreview');
            const pubConfirmBtn = [...document.querySelectorAll('button')].find(b =>
                b.textContent.includes('Publish') && !b.textContent.includes('Cancel')
            );
            return JSON.stringify({
                dialogCount: dialogs.length,
                dialogVisible: dialogs.some(d => d.offsetParent !== null),
                hasPreview: !!storyPreview,
                hasPubConfirm: !!pubConfirmBtn,
                allButtons: [...document.querySelectorAll('button')].map(b => b.textContent.trim()).filter(Boolean).slice(0, 15),
                url: window.location.href
            });
        })()
        """)
        print(f"Modal: {modal_state}")

        # Try clicking "Publish now" or second confirm button
        confirm = await evaluate("""
        (() => {
            const buttons = [...document.querySelectorAll('button')];
            // Look for second "Publish" button (the confirmation one)
            const pubButtons = buttons.filter(b =>
                b.textContent.trim().includes('Publish') &&
                b.offsetParent !== null  // visible
            );
            if (pubButtons.length > 0) {
                // Click the last visible "Publish" button (the confirmation)
                pubButtons[pubButtons.length - 1].click();
                return 'CLICKED_CONFIRM: ' + pubButtons.map(b => b.textContent.trim()).join(' | ');
            }
            return 'NO_CONFIRM_BTN. Visible buttons: ' + buttons.filter(b => b.offsetParent != null).map(b => b.textContent.trim()).join(', ');
        })()
        """)
        print(f"Confirm click: {confirm}")

        await asyncio.sleep(8)

        final_url = await evaluate("window.location.href")
        final_title = await evaluate("document.title")
        canonical = await evaluate("document.querySelector('link[rel=\"canonical\"]')?.href || 'NO_CANONICAL'")

        # Also try to get the published URL from the success page
        pub_url = await evaluate("""
        (() => {
            const links = [...document.querySelectorAll('a')];
            const pubLink = links.find(a => a.href && a.href.includes('/@lg695101011/'));
            if (pubLink) return pubLink.href;
            // Try getting from the published dialog
            const input = document.querySelector('input[value*="medium.com"]');
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
