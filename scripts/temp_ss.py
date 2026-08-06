import urllib.request, json, asyncio, websockets, base64

async def screenshot():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "dev.to" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        msg = json.dumps({"id":1,"method":"Page.captureScreenshot","params":{"format":"png"}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        data = json.loads(resp)
        img = base64.b64decode(data["result"]["data"])
        with open("D:/Tools/ai-tool-index/logs/2026-08-06-devto-state.png", "wb") as f:
            f.write(img)
        print(f"Screenshot saved: {len(img)} bytes")

asyncio.run(screenshot())
