import urllib.request, json, asyncio, websockets, time

async def confirm_pub():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Click the final Publish button (the confirm one)
        js = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    // Find Publish button that's likely the confirmation one (not the first one in the header)
    let candidates = btns.filter(b => b.textContent.trim().includes('Publish') && b.offsetParent !== null && !b.disabled);
    // Pick the last Publish button (likely the confirm in the dialog)
    if (candidates.length >= 2) {
        candidates[candidates.length - 1].click();
        return "CLICKED_CONFIRM_" + candidates.length;
    } else if (candidates.length === 1) {
        candidates[0].click();
        return "CLICKED_ONLY_ONE";
    }
    return "NONE_FOUND";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Click: {resp[:200]}")
        
        await asyncio.sleep(8)
        
        # Final check
        js2 = "JSON.stringify({url: window.location.href, title: document.title})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Final: {resp[:600]}")

asyncio.run(confirm_pub())
