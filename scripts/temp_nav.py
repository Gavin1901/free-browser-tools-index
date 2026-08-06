import urllib.request, json, time, asyncio, websockets

async def nav():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page":
            ws_url = p["webSocketDebuggerUrl"]
            break
    if not ws_url:
        print("ERROR: No page found")
        return
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://dev.to/new"}}))
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        print(f"Navigate sent: {resp[:100]}")

asyncio.run(nav())
time.sleep(4)

pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    url = p.get("url", "")
    if p["type"] == "page" and "dev.to" in url:
        print(f"Dev.to page: {url}")
