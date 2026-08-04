"""Verify Medium article via CDP - check canonical and target links"""
import json, asyncio, websockets, urllib.request, sys

URL = "https://medium.com/@lg695101011/worldwide-meeting-planner-finding-fair-times-across-24-time-zones-f98d8f269e7b"

async def main():
    resp = urllib.request.urlopen("http://localhost:9223/json")
    pages = json.loads(resp.read())
    medium_page = None
    for p in pages:
        if p.get('type') == 'page' and 'medium.com' in p.get('url', ''):
            medium_page = p
            break

    if not medium_page:
        print("No Medium page in CDP")
        sys.exit(1)

    ws_url = medium_page['webSocketDebuggerUrl']

    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        await ws.send(json.dumps({"id": 0, "method": "Runtime.enable"}))

        msg_id = [1]
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

        # Navigate to the published article
        await ws.send(json.dumps({"id": next_id(), "method": "Page.navigate", "params": {"url": URL}}))
        await asyncio.sleep(5)

        title = await evaluate("document.title")
        canonical = await evaluate("document.querySelector('link[rel=\"canonical\"]')?.href")

        # Find ZonePlan links
        links = await evaluate("""
        (() => {
            const allLinks = [...document.querySelectorAll('a')];
            const zpLinks = allLinks.filter(a => a.href && a.href.includes('zoneplan.net'));
            return JSON.stringify(zpLinks.map(a => ({href: a.href, text: a.textContent?.substring(0, 40), visible: a.offsetParent !== null})));
        })()
        """)

        print(f"Title: {title}")
        print(f"Canonical: {canonical}")
        print(f"ZonePlan links: {links}")
        print(f"URL: {await evaluate('window.location.href')}")

asyncio.run(main())
