import urllib.request, json, asyncio, websockets, time

async def get_url():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "medium.com/p/" in url and "/submission" in url:
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Get the canonical URL
        js = "JSON.stringify({url:window.location.href, canonical:document.querySelector('link[rel=\"canonical\"]')?.href||'NONE', bodyText:document.body.innerText.substring(0, 300)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"URL: {r.get('url','?')[:150]}")
            print(f"Canonical: {r.get('canonical','?')[:150]}")
            print(f"Body: {r.get('bodyText','?')[:200]}")

asyncio.run(get_url())
