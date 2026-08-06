import urllib.request, json, asyncio, websockets, time

async def final_medium():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com/new-story" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Approach: click Publish with PointerEvent (React-friendly)
        js = '''
(async function() {
    let pub = [...document.querySelectorAll('button')].find(b => 
        b.textContent.trim() === 'Publish' && b.className.includes('primary')
    );
    if (!pub) return "NO_BTN";
    
    // Dispatch all event types that React might listen for
    let rect = pub.getBoundingClientRect();
    let opts = {bubbles: true, cancelable: true, clientX: rect.x + rect.width/2, clientY: rect.y + rect.height/2, button: 0};
    
    pub.focus();
    pub.dispatchEvent(new PointerEvent('pointerdown', opts));
    await new Promise(r => setTimeout(r, 50));
    pub.dispatchEvent(new PointerEvent('pointerup', opts));
    await new Promise(r => setTimeout(r, 50));
    pub.dispatchEvent(new MouseEvent('mousedown', opts));
    await new Promise(r => setTimeout(r, 50));
    pub.dispatchEvent(new MouseEvent('mouseup', opts));
    await new Promise(r => setTimeout(r, 50));
    pub.dispatchEvent(new MouseEvent('click', opts));
    await new Promise(r => setTimeout(r, 50));
    pub.click();
    
    return "DISPATCHED_ALL";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js, "awaitPromise": True}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        print(f"Click events: {resp[:200]}")
        
        await asyncio.sleep(4)
        
        # Check what appeared - scan for publish drawer
        js2 = '''
(function() {
    let r = {};
    r.url = window.location.href;
    
    // Find all visible text elements that mention publish
    let texts = [...document.querySelectorAll('h1,h2,h3,h4,button,span,p,div,a')].filter(el => {
        if (!el.offsetParent) return false;
        if (el.children.length > 0) return false;
        return el.textContent.toLowerCase().includes('publish');
    }).map(el => el.textContent.trim().substring(0, 60));
    r.publishTexts = [...new Set(texts)];
    
    // Check if any drawer/panel opened
    let drawers = document.querySelectorAll('[class*="drawer"], [class*="Drawer"], [class*="panel"], [class*="Panel"], [class*="sidebar"], [class*="Sidebar"]');
    r.drawersOpen = [...drawers].filter(d => d.offsetParent !== null).length;
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data["result"]["result"]["value"]
        if isinstance(val, str):
            r = json.loads(val)
        else:
            r = val
        print(f"Publish texts: {r.get('publishTexts', [])}")
        print(f"Drawers: {r.get('drawersOpen', 0)}")
        print(f"URL: {r.get('url')}")

asyncio.run(final_medium())
