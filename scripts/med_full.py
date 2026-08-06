import urllib.request, json, asyncio, websockets, time, base64

async def publish_medium():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Approach: Get the dropdown after clicking Publish, find "Publish" in dropdown, click it
        
        # First, click Publish to open dropdown
        js1 = '''
(function() {
    let pub = [...document.querySelectorAll('button')].find(b => 
        b.textContent.trim() === 'Publish' && 
        b.className.includes('primary') && 
        b.offsetParent !== null
    );
    if (!pub) return "NO_BTN";
    
    // Try native click with proper event
    let rect = pub.getBoundingClientRect();
    let cx = rect.x + rect.width / 2;
    let cy = rect.y + rect.height / 2;
    
    // Focus first
    pub.focus();
    
    // Use pointer events for React compatibility
    ['pointerdown','mousedown','mouseup','click'].forEach(t => {
        pub.dispatchEvent(new PointerEvent(t, {bubbles: true, cancelable: true, clientX: cx, clientY: cy}));
        pub.dispatchEvent(new MouseEvent(t, {bubbles: true, cancelable: true, clientX: cx, clientY: cy}));
    });
    
    return "CLICKED_RECT:" + JSON.stringify({x: Math.round(cx), y: Math.round(cy)});
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js1}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Step1: {resp[:300]}")
        
        await asyncio.sleep(3)
        
        # Check for dropdown and all publish-related elements
        js2 = '''
(function() {
    let r = {};
    
    // ALL visible elements with "Publish" text
    let allEls = [...document.querySelectorAll('*')].filter(el => 
        el.offsetParent !== null && 
        el.children.length === 0 &&
        el.textContent.trim().toLowerCase().includes('publish')
    );
    r.publishEls = allEls.map(el => ({
        tag: el.tagName,
        text: el.textContent.trim().substring(0, 60),
        cls: (el.className?.toString() || '').substring(0, 40),
        role: el.getAttribute('role') || '',
        rect: (() => { let r = el.getBoundingClientRect(); return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; })()
    }));
    
    // Check menus/dropdowns
    let menus = document.querySelectorAll('[role="menu"], [role="listbox"], [role="dialog"]');
    r.menus = [...menus].filter(m => m.offsetParent !== null).map(m => ({
        text: m.textContent.trim().substring(0, 200),
        role: m.getAttribute('role')
    }));
    
    r.url = window.location.href;
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        result_str = json.loads(resp)["result"]["result"]["value"]
        result = json.loads(result_str)
        print(f"Publish elements: {json.dumps(result.get('publishEls', []), indent=2)[:1200]}")
        print(f"Menus: {result.get('menus', [])}")
        
        # Click the SECOND Publish element if exists (the dropdown one)
        pub_els = result.get("publishEls", [])
        if len(pub_els) >= 2:
            # Click the one that's NOT the primary button
            for pel in pub_els:
                if "primary" not in pel.get("cls", "").lower() and pel["tag"] == "BUTTON":
                    cx = pel["rect"]["x"] + pel["rect"]["w"] // 2
                    cy = pel["rect"]["y"] + pel["rect"]["h"] // 2
                    print(f"Clicking second Publish at ({cx},{cy}): {pel['text']}")
                    
                    # Use proper mouse event sequence
                    for evt_type in ["mousePressed", "mouseReleased"]:
                        await ws.send(json.dumps({
                            "id": 10,
                            "method": "Input.dispatchMouseEvent",
                            "params": {"type": evt_type, "x": cx, "y": cy, "button": "left", "clickCount": 1}
                        }))
                        await asyncio.sleep(0.1)
                    break
        
        await asyncio.sleep(5)
        
        # Check final URL
        js3 = "JSON.stringify({url: window.location.href, title: document.title})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Final: {resp[:400]}")

asyncio.run(publish_medium())
