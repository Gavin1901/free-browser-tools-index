import urllib.request, json, asyncio, websockets, time

async def pinterest():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    if not ws_url:
        # Open Pinterest
        browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
        async with websockets.connect(browser_ws, max_size=2**24) as bws:
            await bws.send(json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://www.pinterest.com/pin-creation-tool/"}}))
            await asyncio.wait_for(bws.recv(), timeout=10)
        await asyncio.sleep(6)
        
        pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
        for p in pages:
            if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
                ws_url = p["webSocketDebuggerUrl"]
                break
    
    if not ws_url:
        print("Pinterest not found")
        return
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        js = "JSON.stringify({url:window.location.href, title:document.title, bodyStart:document.body.innerText.substring(0, 500)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"URL: {str(r.get('url','?'))[:120]}")
            print(f"Title: {str(r.get('title','?'))[:80]}")
            body = str(r.get('bodyStart',''))
            # Check if login needed
            if 'login' in body.lower() or 'log in' in body.lower() or 'sign up' in body.lower():
                print("NEEDS LOGIN")
            else:
                print("LOGGED IN")
            print(f"Body: {body[:300]}")

asyncio.run(pinterest())
