"""Check if Medium article was published - navigate to profile page"""
import json, asyncio, websockets, urllib.request

async def main():
    resp = urllib.request.urlopen("http://localhost:9223/json")
    pages = json.loads(resp.read())
    for p in pages:
        if p.get('type') == 'page' and 'medium.com' in p.get('url', ''):
            ws_url = p['webSocketDebuggerUrl']
            break
    else:
        print("No Medium page in CDP")
        return

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

        # Current URL
        url = await evaluate("window.location.href")
        print(f"Current: {url}")

        # Navigate to profile to see published articles
        await ws.send(json.dumps({"id": next_id(), "method": "Page.navigate", "params": {"url": "https://medium.com/@lg695101011"}}))
        await asyncio.sleep(5)

        # Get all article links
        articles = await evaluate("""
        (() => {
            const links = [...document.querySelectorAll('a')];
            const articleLinks = links.filter(a =>
                a.href && a.href.includes('/@lg695101011/') &&
                !a.href.includes('/following') &&
                !a.href.includes('/lists') &&
                !a.href.includes('/about') &&
                !a.href.includes('/followers')
            );
            return JSON.stringify(articleLinks.map(a => ({
                href: a.href,
                text: a.textContent?.substring(0, 80)
            })).slice(0, 10));
        })()
        """)
        print(f"Articles: {articles}")

        # Also check the submission page directly
        await ws.send(json.dumps({"id": next_id(), "method": "Page.navigate", "params": {"url": "https://medium.com/p/69f3b1368484"}}))
        await asyncio.sleep(5)

        final_url = await evaluate("window.location.href")
        title = await evaluate("document.title")
        canonical = await evaluate("document.querySelector('link[rel=\"canonical\"]')?.href")
        links = await evaluate("""
        (() => {
            return JSON.stringify([...document.querySelectorAll('a')]
                .filter(a => a.href && a.href.includes('zoneplan.net'))
                .map(a => ({href: a.href, visible: a.offsetParent !== null}))
            );
        })()
        """)

        print(f"Final URL: {final_url}")
        print(f"Title: {title}")
        print(f"Canonical: {canonical}")
        print(f"ZonePlan links: {links}")

asyncio.run(main())
