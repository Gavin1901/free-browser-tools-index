import urllib.request, json, asyncio, websockets, time

async def pin_next2():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Click ALL buttons and check which one progresses
        for attempt in range(5):
            js = '''
(function() {
    let btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null && !b.disabled);
    // Try clicking the rightmost/bottommost button (usually the primary action)
    let btn = btns[btns.length - 1];
    btn.click();
    return "CLICKED:" + btn.textContent.trim().substring(0, 30);
})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            result = data.get("result",{}).get("result",{}).get("value","")
            print(f"Attempt {attempt}: {result}")
            await asyncio.sleep(3)
            
            js_url = "window.location.href"
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            url = data.get("result",{}).get("result",{}).get("value","")
            print(f"  URL: {url[:100]}")
            
            if "pin-builder" not in url:
                print(f">>> SUCCESS: {url}")
                break

asyncio.run(pin_next2())
