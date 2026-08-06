import urllib.request, json, asyncio, websockets

async def check_hn():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    hn_ws = None
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "ycombinator.com" in url:
            hn_ws = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(hn_ws, max_size=2**24) as ws:
        js = "document.body.innerText.substring(0, 500)"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(data["result"]["result"]["value"])

asyncio.run(check_hn())
