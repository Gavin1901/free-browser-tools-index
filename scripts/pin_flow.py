import urllib.request, json, asyncio, websockets, time

async def pin_flow():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Step 1: Find ALL elements and their exact text (handle Chinese chars)
        js = '''
(function() {
    let all = [...document.querySelectorAll('button, [role="button"], div[tabindex="0"]')];
    return JSON.stringify(all.filter(el => el.offsetParent !== null && !el.disabled).map(el => {
        let rect = el.getBoundingClientRect();
        // Get text from all child nodes to handle SVGs
        let fullText = el.innerText || el.textContent || '';
        return {
            text: fullText.trim().substring(0, 40),
            rect: {x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height)}
        };
    }).filter(c => c.text.length > 0 && c.rect.w > 0));
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            btns = json.loads(val) if isinstance(val, str) else val
            for b in btns:
                print(f"  [{b['rect']['x']},{b['rect']['y']}] {b['text'][:30]}")
            
            # Find "Next" or right-side button
            rightBtns = sorted([b for b in btns if b['rect']['x'] > 500], key=lambda b: b['rect']['y'], reverse=True)
            if rightBtns:
                target = rightBtns[0]  # Bottom-right button
                cx = target['rect']['x'] + target['rect']['w'] // 2
                cy = target['rect']['y'] + target['rect']['h'] // 2
                print(f"Clicking: {target['text'][:30]} at ({cx},{cy})")
                await ws.send(json.dumps({"id":1,"method":"Input.dispatchMouseEvent","params":{"type":"mouseMoved","x":cx,"y":cy}}))
                await asyncio.sleep(0.1)
                await ws.send(json.dumps({"id":2,"method":"Input.dispatchMouseEvent","params":{"type":"mousePressed","x":cx,"y":cy,"button":"left","clickCount":1}}))
                await asyncio.sleep(0.15)
                await ws.send(json.dumps({"id":3,"method":"Input.dispatchMouseEvent","params":{"type":"mouseReleased","x":cx,"y":cy,"button":"left","clickCount":1}}))
                await asyncio.sleep(5)
        
        js_url = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        url = data.get("result",{}).get("result",{}).get("value","")
        print(f"URL: {url[:150]}")

asyncio.run(pin_flow())
