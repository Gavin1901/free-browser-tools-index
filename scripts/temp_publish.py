import urllib.request, json, asyncio, websockets, time

async def publish():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "dev.to" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    if not ws_url:
        print("ERROR: Dev.to page not found")
        return
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Click publish button
        js_click = '''
(function() {
    let btns = document.querySelectorAll('button');
    for (let b of btns) {
        let text = b.textContent.toLowerCase();
        if (text.includes('publish') && !b.disabled) {
            b.click();
            return "CLICKED: " + b.textContent.trim();
        }
    }
    for (let b of btns) {
        if (b.textContent.toLowerCase().includes('publish')) {
            return "FOUND_BUT_DISABLED: " + b.textContent.trim();
        }
    }
    return "NO_PUBLISH_BUTTON. Buttons found: " + [...btns].map(b => b.textContent.trim()).join(", ").substring(0, 200);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_click}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Click result: {resp[:400]}")
        
        await asyncio.sleep(3)
        
        # Check current URL
        js_url = "window.location.href"
        msg = json.dumps({"id":2,"method":"Runtime.evaluate","params":{"expression":js_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Current URL: {resp[:400]}")

asyncio.run(publish())
