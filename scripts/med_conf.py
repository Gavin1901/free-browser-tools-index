import urllib.request, json, asyncio, websockets, time

async def confirm():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Click the Publish option in what should be the dropdown
        js = '''
(function() {
    let allEls = [...document.querySelectorAll('button, a, [role="menuitem"]')];
    let candidates = allEls.filter(el => 
        el.textContent.trim() === 'Publish' && 
        el.offsetParent !== null && 
        !el.disabled
    );
    // Click the one that's NOT the primary button (the dropdown option)
    for (let c of candidates) {
        if (!c.className.includes('primary')) {
            c.click();
            return "CLICKED_DROPDOWN_" + c.tagName + "_" + c.className.substring(0, 30);
        }
    }
    // If only one, click it
    if (candidates.length === 1) {
        candidates[0].click();
        return "CLICKED_ONLY_" + candidates[0].className.substring(0, 30);
    }
    // If multiple primary buttons, click last
    if (candidates.length > 0) {
        candidates[candidates.length - 1].click();
        return "CLICKED_LAST_" + candidates.length;
    }
    return "NONE_FOUND";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Click: {resp[:200]}")
        
        await asyncio.sleep(6)
        
        # Final URL check
        js2 = '''
(function() {
    let r = {};
    r.url = window.location.href;
    r.title = document.title;
    let notices = [...document.querySelectorAll('[role="alert"], .notice, [class*="toast"]')].filter(e => e.offsetParent !== null).map(e => e.textContent.trim().substring(0, 200));
    r.notices = notices.join(" ;; ");
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Final: {resp[:600]}")

asyncio.run(confirm())
