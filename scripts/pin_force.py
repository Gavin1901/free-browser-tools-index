import urllib.request, json, asyncio, websockets, time

async def pin_force():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # First: Press Escape to close any expand/fullscreen mode
        await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"keyDown","key":"Escape","code":"Escape","keyCode":27}}))
        await asyncio.sleep(1)
        await ws.send(json.dumps({"id":2,"method":"Input.dispatchKeyEvent","params":{"type":"keyUp","key":"Escape","code":"Escape","keyCode":27}}))
        await asyncio.sleep(2)
        
        # Now click at Publish button coordinates (top right area)
        for cx, cy in [(963, 172), (900, 50), (950, 40), (1000, 150)]:
            js = f'''
(function() {{
    let el = document.elementFromPoint({cx}, {cy});
    if (!el) return "NO_EL";
    let txt = el.textContent?.trim()?.substring(0,30) || '';
    // Try clicking the element and its parents
    let current = el;
    for (let i = 0; i < 5 && current; i++) {{
        if (current.tagName === 'BUTTON' || current.tagName === 'DIV' || current.getAttribute('role') === 'button') {{
            current.dispatchEvent(new MouseEvent('click', {{bubbles: true, cancelable: true, clientX: {cx}, clientY: {cy}}}));
            current.click();
            return "CLICKED:" + current.tagName + ":" + txt;
        }}
        current = current.parentElement;
    }}
    el.dispatchEvent(new MouseEvent('click', {{bubbles: true, cancelable: true, clientX: {cx}, clientY: {cy}}}));
    el.click();
    return "CLICKED_EL:" + el.tagName + ":" + txt;
}})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            result = data.get("result",{}).get("result",{}).get("value","")
            print(f"Click ({cx},{cy}): {result}")
            await asyncio.sleep(3)
            
            js_url = "window.location.href"
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            url = data.get("result",{}).get("result",{}).get("value","")
            print(f"  URL: {url[:120]}")
            if "pin-builder" not in url:
                print(f">>> SUCCESS: {url}")
                return

asyncio.run(pin_force())
