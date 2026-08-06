import urllib.request, json, asyncio, websockets, time

async def pin_next():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Click the button with longest text (likely "下一步" - Next)
        js = '''
(function() {
    let btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null && !b.disabled);
    // Find the button with longest text (likely the Next/Continue button)
    let longest = btns.reduce((a, b) => (b.textContent.length > a.textContent.length) ? b : a, btns[0]);
    longest.click();
    return "CLICKED:" + longest.textContent.trim().substring(0, 30);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Next: {resp[:150]}")
        await asyncio.sleep(4)
        
        # Check buttons again
        js2 = '''
(function() {
    let btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null && !b.disabled);
    let texts = btns.map(b => b.textContent.trim()).filter(t => t.length > 0);
    
    // Try clicking any publish/save/done button
    for (let b of btns) {
        let t = b.textContent.trim();
        if (t.includes('Publish') || t.includes('Save') || t === 'Done' || t.includes('Create')) {
            b.click();
            return "PUBLISHED:" + t.substring(0, 30);
        }
    }
    
    // If no publish button, list all
    return "BTNS:" + [...new Set(texts)].join(" | ");
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Step2: {resp[:200]}")
        await asyncio.sleep(5)
        
        js_url = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(f"URL: {data.get('result',{}).get('result',{}).get('value','?')[:150]}")

asyncio.run(pin_next())
