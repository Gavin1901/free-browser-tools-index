import urllib.request, json, asyncio, websockets, base64
async def ss():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "medium.com" in url:
            async with websockets.connect(p["webSocketDebuggerUrl"], max_size=2**24) as ws:
                await ws.send(json.dumps({"id":1,"method":"Page.captureScreenshot","params":{"format":"png"}}))
                resp = await asyncio.wait_for(ws.recv(), timeout=15)
                data = json.loads(resp)
                with open("D:/Tools/ai-tool-index/logs/2026-08-06-medium-breakthrough.png", "wb") as f:
                    f.write(base64.b64decode(data["result"]["data"]))
                print("Saved")
asyncio.run(ss())
