import urllib.request, json, asyncio, websockets, time

async def open_tabs():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page":
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Open Dev.to
        js = "window.open('https://dev.to/new', '_blank')"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Dev.to opened: {resp[:100]}")
        await asyncio.sleep(2)
        
        # Open HN submit
        js = "window.open('https://news.ycombinator.com/submit', '_blank')"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"HN opened: {resp[:100]}")
        await asyncio.sleep(2)
        
        # Open Quora
        js = "window.open('https://www.quora.com/', '_blank')"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Quora opened: {resp[:100]}")

asyncio.run(open_tabs())
time.sleep(5)

# Check all pages
pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    url = p.get("url", "?")
    if p["type"] == "page":
        print(f"PAGE: {url[:120]}")
