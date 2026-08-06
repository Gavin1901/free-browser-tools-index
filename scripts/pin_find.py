import urllib.request, json, asyncio, websockets, time

async def pin_publish():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Find ALL clickable elements with their positions and attributes
        js = '''
(function() {
    // Find all buttons and get their full attributes
    let allBtns = [...document.querySelectorAll('button, [role="button"], div[tabindex]')];
    let candidates = allBtns.filter(el => el.offsetParent !== null && !el.disabled);
    
    return JSON.stringify(candidates.map(el => {
        let rect = el.getBoundingClientRect();
        return {
            tag: el.tagName,
            text: el.textContent.trim().substring(0, 30),
            aria: el.getAttribute('aria-label') || '',
            dataTestId: el.getAttribute('data-test-id') || el.getAttribute('data-testid') || '',
            role: el.getAttribute('role') || '',
            type: el.type || '',
            rect: {x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height)},
            classes: (el.className || '').toString().substring(0, 60)
        };
    }).filter(c => c.rect.w > 0 && c.rect.h > 0));
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            btns = json.loads(val) if isinstance(val, str) else val
            print(f"Found {len(btns)} clickable elements")
            
            # Find publish/submit/save button
            target = None
            for b in btns:
                combined = (b.get('text','') + ' ' + b.get('aria','') + ' ' + b.get('dataTestId','') + ' ' + b.get('classes','')).lower()
                if any(kw in combined for kw in ['publish', 'save', 'done', 'create', 'submit', 'next']):
                    if b['rect']['x'] > 500:  # Right side of screen
                        target = b
                        print(f"TARGET: {b['tag']} text='{b['text']}' aria='{b['aria']}' at ({b['rect']['x']},{b['rect']['y']}) {b['rect']['w']}x{b['rect']['h']}")
                        break
            
            if not target:
                # Show right-side buttons
                rightBtns = [b for b in btns if b['rect']['x'] > 500]
                for b in rightBtns[:10]:
                    print(f"  CANDIDATE: {b['tag']} text='{b['text']}' aria='{b['aria']}' classes='{b['classes'][:40]}' at ({b['rect']['x']},{b['rect']['y']})")
            
            if target:
                # Click at center of target
                cx = target['rect']['x'] + target['rect']['w'] // 2
                cy = target['rect']['y'] + target['rect']['h'] // 2
                print(f"Clicking at ({cx}, {cy})")
                await ws.send(json.dumps({"id":10,"method":"Input.dispatchMouseEvent","params":{"type":"mouseMoved","x":cx,"y":cy}}))
                await asyncio.sleep(0.1)
                await ws.send(json.dumps({"id":11,"method":"Input.dispatchMouseEvent","params":{"type":"mousePressed","x":cx,"y":cy,"button":"left","clickCount":1}}))
                await asyncio.sleep(0.15)
                await ws.send(json.dumps({"id":12,"method":"Input.dispatchMouseEvent","params":{"type":"mouseReleased","x":cx,"y":cy,"button":"left","clickCount":1}}))
                await asyncio.sleep(5)
                
                js_url = "window.location.href"
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(resp)
                print(f"URL: {data.get('result',{}).get('result',{}).get('value','?')[:150]}")

asyncio.run(pin_publish())
