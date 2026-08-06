import urllib.request, json, asyncio, websockets, time

async def quora_answer():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "quora.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Find all buttons and clickable elements
        js = '''
(function() {
    let r = {};
    // Find answer-related elements
    let allBtns = [...document.querySelectorAll('button')];
    r.buttons = allBtns.filter(b => b.offsetParent !== null).map(b => b.textContent.trim().substring(0, 40)).filter(t => t);
    
    let allLinks = [...document.querySelectorAll('a')];
    r.answerLinks = allLinks.filter(a => {
        let t = a.textContent.toLowerCase();
        return (t.includes('answer') || t.includes('write')) && a.offsetParent !== null;
    }).map(a => a.textContent.trim().substring(0, 40));
    
    // Check for contenteditable
    let editables = document.querySelectorAll('[contenteditable="true"]');
    r.editableCount = editables.length;
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"Buttons: {r.get('buttons', [])}")
            print(f"Answer links: {r.get('answerLinks', [])}")
            print(f"Editables: {r.get('editableCount', 0)}")
            
            # Click any answer link/button
            if r.get('answerLinks') or any('answer' in b.lower() for b in r.get('buttons', [])):
                js_click = '''
(function() {
    // Try to find and click answer button
    let answerBtn = [...document.querySelectorAll('button')].find(b => b.textContent.toLowerCase().includes('answer'));
    if (answerBtn) { answerBtn.click(); return "CLICKED_BTN"; }
    let answerLink = [...document.querySelectorAll('a')].find(a => a.textContent.toLowerCase().includes('answer'));
    if (answerLink) { answerLink.click(); return "CLICKED_LINK"; }
    return "NOT_FOUND";
})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_click}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                print(f"Click result: {resp[:200]}")
                await asyncio.sleep(4)
        
        # Check again for editor
        js3 = "JSON.stringify({url:window.location.href, editableCount:document.querySelectorAll('[contenteditable=\"true\"]').length, textareas:document.querySelectorAll('textarea').length})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"After click: url={r.get('url','?')[:100]}, editables={r.get('editableCount')}, textareas={r.get('textareas')}")

asyncio.run(quora_answer())
