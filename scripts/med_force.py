import urllib.request, json, asyncio, websockets, time

async def force_pub():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Get Publish button coordinates and click via mouse
        js = '''
(function() {
    let pub = [...document.querySelectorAll('button')].find(b => 
        b.textContent.trim() === 'Publish' && b.className.includes('primary')
    );
    if (!pub) return JSON.stringify({error: "NO_BTN"});
    let r = pub.getBoundingClientRect();
    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = json.loads(data["result"]["result"]["value"])
        print(f"Button at: {val}")
        
        cx, cy = val["x"], val["y"]
        
        # Dispatch full mouse click sequence
        await ws.send(json.dumps({"id":2,"method":"Input.dispatchMouseEvent","params":{"type":"mouseMoved","x":cx,"y":cy}}))
        await asyncio.sleep(0.1)
        await ws.send(json.dumps({"id":3,"method":"Input.dispatchMouseEvent","params":{"type":"mousePressed","x":cx,"y":cy,"button":"left","clickCount":1}}))
        await asyncio.sleep(0.15)
        await ws.send(json.dumps({"id":4,"method":"Input.dispatchMouseEvent","params":{"type":"mouseReleased","x":cx,"y":cy,"button":"left","clickCount":1}}))
        await asyncio.sleep(3)
        
        # Check for publish dialog
        js2 = '''
(function() {
    let r = {};
    r.url = window.location.href;
    
    // Look for publish dialog/menu
    let allEls = [...document.querySelectorAll('*')].filter(el => 
        el.offsetParent !== null && 
        el.children.length === 0
    );
    
    // Find elements with "Publish" or "Ready" text (the confirmation dialog)
    let pubTexts = allEls.filter(el => {
        let t = el.textContent.trim();
        return t === 'Publish' || t === 'Publish now' || t.includes('Ready to publish');
    });
    r.pubTexts = pubTexts.map(el => ({tag: el.tagName, text: el.textContent.trim().substring(0, 40), cls: (el.className||'').toString().substring(0, 30)}));
    
    // Check for topic/tag inputs in dialog
    let dialogBtns = [...document.querySelectorAll('button')].filter(b => 
        b.offsetParent !== null && 
        (b.textContent.trim().includes('Publish') || b.textContent.trim().includes('Select'))
    );
    r.dialogButtons = dialogBtns.map(b => ({text: b.textContent.trim().substring(0, 40), disabled: b.disabled}));
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = json.loads(data["result"]["result"]["value"])
        print(f"Dialog: {json.dumps(val, indent=2)[:1000]}")

asyncio.run(force_pub())
