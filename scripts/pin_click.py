import urllib.request, json, asyncio, websockets, time

async def click_publish():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Click at (979, 184) — center of the Publish button
        cx, cy = 979, 184
        
        # Try multiple click approaches
        for attempt in range(3):
            print(f"Attempt {attempt}...")
            # Approach: Click the DIV element directly via JS
            js = f'''
(function() {{
    let el = document.elementFromPoint({cx}, {cy});
    if (el) {{
        // Find the closest clickable parent
        while (el && el.tagName !== 'BUTTON' && el.tagName !== 'DIV' && el.getAttribute('role') !== 'button') {{
            el = el.parentElement;
        }}
        if (el) {{
            el.focus();
            el.dispatchEvent(new PointerEvent('pointerdown', {{bubbles: true, cancelable: true, clientX: {cx}, clientY: {cy}}}));
            el.dispatchEvent(new PointerEvent('pointerup', {{bubbles: true, cancelable: true, clientX: {cx}, clientY: {cy}}}));
            el.dispatchEvent(new MouseEvent('click', {{bubbles: true, cancelable: true, clientX: {cx}, clientY: {cy}, view: window}}));
            el.click();
            return "CLICKED:" + el.tagName + ":" + (el.textContent?.trim()?.substring(0,20) || '');
        }}
    }}
    return "NO_EL_AT_POINT";
}})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            result = data.get("result",{}).get("result",{}).get("value","")
            print(f"  JS click: {result}")
            await asyncio.sleep(4)
            
            js_url = "window.location.href"
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            url = data.get("result",{}).get("result",{}).get("value","")
            print(f"  URL: {url[:120]}")
            
            if "pin-builder" not in url:
                print(f">>> PUBLISHED! {url}")
                return
            
            await asyncio.sleep(1)

asyncio.run(click_publish())
