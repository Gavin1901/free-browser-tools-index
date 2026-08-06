import urllib.request, json, asyncio, websockets, time

async def medium_flow():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Step 1: Dismiss any overlay
        js1 = '''
(function() {
    let overlays = document.querySelectorAll('[class*="overlay"], [class*="Overlay"]');
    for (let o of overlays) {
        if (o.offsetParent !== null) {
            o.click();
            return "DISMISSED_OVERLAY";
        }
    }
    return "NO_OVERLAY_VISIBLE";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js1}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Overlay: {resp[:200]}")
        await asyncio.sleep(2)
        
        # Step 2: Check title state
        js2 = '''
(function() {
    let r = {};
    let editables = document.querySelectorAll('[contenteditable="true"]');
    r.editables = [...editables].map((e, i) => ({
        idx: i,
        text: e.textContent.trim().substring(0, 80),
        visible: e.offsetParent !== null
    }));
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Editables: {resp[:600]}")
        
        # Step 3: Click Publish button
        js3 = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let pub = btns.find(b => 
        b.textContent.trim() === 'Publish' && 
        b.offsetParent !== null && 
        !b.disabled &&
        b.className.includes('primary')
    );
    if (!pub) {
        pub = btns.find(b => b.textContent.trim() === 'Publish' && b.offsetParent !== null && !b.disabled);
    }
    if (pub) {
        pub.click();
        return "CLICKED_" + pub.className.substring(0, 50);
    }
    return "NO_PUB_BTN";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Click Publish: {resp[:200]}")
        
        await asyncio.sleep(4)
        
        # Step 4: Check what appeared
        js4 = '''
(function() {
    let r = {};
    r.url = window.location.href;
    
    // Check for dropdown menu with Publish option
    let allVisible = [...document.querySelectorAll('button, a, [role="menuitem"]')].filter(el => el.offsetParent !== null);
    r.publishOptions = allVisible
        .filter(el => el.textContent.toLowerCase().includes('publish'))
        .map(el => ({text: el.textContent.trim().substring(0, 50), tag: el.tagName, disabled: el.disabled}));
    
    // Check for dialogs
    let dialogs = document.querySelectorAll('[role="dialog"], [role="menu"], [role="listbox"]');
    r.dialogCount = dialogs.length;
    if (dialogs.length > 0) {
        r.dialogText = dialogs[0].textContent.trim().substring(0, 300);
    }
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js4}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Post-click: {resp[:800]}")

asyncio.run(medium_flow())
