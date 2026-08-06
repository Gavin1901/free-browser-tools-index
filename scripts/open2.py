import urllib.request, json, asyncio, websockets, time

async def open_all():
    browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
    
    async with websockets.connect(browser_ws, max_size=2**24) as bws:
        # Pinterest
        msg = json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://www.pinterest.com/"}})
        await bws.send(msg)
        resp = await asyncio.wait_for(bws.recv(), timeout=10)
        print(f"Pinterest: {json.loads(resp)['result']['targetId']}")
        
        # Product Hunt
        msg = json.dumps({"id":2,"method":"Target.createTarget","params":{"url":"https://www.producthunt.com/discussions"}})
        await bws.send(msg)
        resp = await asyncio.wait_for(bws.recv(), timeout=10)
        print(f"PH: {json.loads(resp)['result']['targetId']}")
    
    await asyncio.sleep(6)
    
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    for p in pages:
        url = p.get("url", "?")
        if p["type"] == "page":
            short = url[:100]
            if "pinterest" in url.lower():
                print(f"PINTEREST: {short}")
            elif "producthunt" in url.lower():
                print(f"PH: {short}")
            elif "quora" in url.lower():
                print(f"QUORA: {short}")

asyncio.run(open_all())
