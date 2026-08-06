import urllib.request, json, asyncio, websockets, time

async def mouse_publish():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # First try: look for the final confirmation Publish button and click it
        # Medium flow: Publish -> add topics -> Publish now
        js = '''
(function() {
    let r = {};
    // Look for ALL publish-related buttons visible
    let btns = [...document.querySelectorAll('button')];
    let pubBtns = btns.filter(b => 
        b.textContent.toLowerCase().includes('publish') && 
        b.offsetParent !== null
    );
    r.pubButtons = pubBtns.map(b => ({
        text: b.textContent.trim(),
        disabled: b.disabled,
        className: b.className.substring(0, 40),
        rect: (() => { let r = b.getBoundingClientRect(); return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; })()
    }));
    
    // Also check for "Publish now" or "Submit" texts
    let allVisibleText = [...document.querySelectorAll('h1,h2,h3,h4,button,span,div')]
        .filter(el => el.offsetParent !== null && el.children.length === 0)
        .map(el => el.textContent.trim())
        .filter(t => t.length > 3 && t.length < 30);
    
    r.relevantTexts = [...new Set(allVisibleText)].filter(t => 
        t.toLowerCase().includes('publish') || 
        t.toLowerCase().includes('topic') ||
        t.toLowerCase().includes('tag')
    ).slice(0, 10);
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        result_str = data["result"]["result"]["value"]
        result = json.loads(result_str)
        
        print(f"Publish buttons: {json.dumps(result['pubButtons'], indent=2)}")
        print(f"Relevant texts: {result['relevantTexts']}")
        
        # Find the right button to click
        # If there's a "Publish now" or the last non-disabled publish button
        target = None
        for b in result["pubButtons"]:
            if not b["disabled"] and "primary" in b["className"].lower():
                target = b
                break
        if not target:
            for b in result["pubButtons"]:
                if not b["disabled"]:
                    target = b
                    break
        
        if target:
            print(f"Target: {target['text']} at ({target['rect']['x']},{target['rect']['y']})")
            cx = target["rect"]["x"] + target["rect"]["w"] // 2
            cy = target["rect"]["y"] + target["rect"]["h"] // 2
            
            # Dispatch mouse events
            await ws.send(json.dumps({"id":2,"method":"Input.dispatchMouseEvent","params":{"type":"mouseMoved","x":cx,"y":cy}}))
            await asyncio.sleep(0.1)
            await ws.send(json.dumps({"id":3,"method":"Input.dispatchMouseEvent","params":{"type":"mousePressed","x":cx,"y":cy,"button":"left","clickCount":1}}))
            await asyncio.sleep(0.1)
            await ws.send(json.dumps({"id":4,"method":"Input.dispatchMouseEvent","params":{"type":"mouseReleased","x":cx,"y":cy,"button":"left","clickCount":1}}))
            print("Mouse click dispatched")
        else:
            print("No target found")

asyncio.run(mouse_publish())
