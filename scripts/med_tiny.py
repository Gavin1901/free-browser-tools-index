import urllib.request, json, asyncio, websockets, time

TINY_TITLE = "InvoicePad: Free Invoice Generator for Freelancers"
TINY_BODY = "I built https://invoicepad.net, a free invoice generator with profession-specific templates. No sign-up, no watermark, instant PDF download in under 60 seconds."

async def medium_tiny():
    # Create new target via browser WS
    browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
    
    async with websockets.connect(browser_ws, max_size=2**24) as bws:
        msg = json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://medium.com/new-story"}})
        await bws.send(msg)
        resp = await asyncio.wait_for(bws.recv(), timeout=15)
        tid = json.loads(resp)["result"]["targetId"]
        print(f"New tab: {tid}")
    
    await asyncio.sleep(8)
    
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    med_ws = None
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "medium.com/new-story" in url:
            # Make sure it's the new one (not the old one)
            if str(tid).lower() in str(p.get("id", "")).lower() or med_ws is None:
                med_ws = p["webSocketDebuggerUrl"]
                print(f"Found: {url[:100]}")
    
    if not med_ws:
        print("Medium page not found, trying all pages")
        for p in pages:
            if p["type"] == "page" and "medium.com/new-story" in p.get("url", ""):
                med_ws = p["webSocketDebuggerUrl"]
    
    async with websockets.connect(med_ws, max_size=2**24) as ws:
        await asyncio.sleep(3)
        
        # Type title via keyboard
        js_focus = '''
(function() {
    let editables = document.querySelectorAll('[contenteditable="true"]');
    if (editables.length > 0) {
        editables[0].focus();
        editables[0].click();
        return "FOCUSED";
    }
    return "NO_EDITOR";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_focus}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Focus: {resp[:150]}")
        await asyncio.sleep(1)
        
        for char in TINY_TITLE:
            await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"char","text":char,"unmodifiedText":char}}))
            await asyncio.sleep(0.02)
        print("Title typed")
        await asyncio.sleep(2)
        
        # Enter to body
        await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"keyDown","key":"Enter","code":"Enter","keyCode":13}}))
        await asyncio.sleep(0.1)
        await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"keyUp","key":"Enter","code":"Enter","keyCode":13}}))
        await asyncio.sleep(2)
        
        for char in TINY_BODY:
            await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"char","text":char,"unmodifiedText":char}}))
            await asyncio.sleep(0.015)
        print("Body typed")
        await asyncio.sleep(4)
        
        # Check popover
        js_pop = "JSON.stringify({popover:(document.querySelector('.popover-description')||{}).textContent||'NONE', pubDisabled:[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='Publish')?.disabled||'NO_BTN'})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_pop}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        print(f"Popover check: {val}")
        
        # Click Publish
        js_pub = "JSON.stringify({url:window.location.href})"
        js_click = '''
(function() {
    let pub = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Publish' && b.offsetParent !== null && !b.disabled);
    if (pub) {
        pub.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
        return "CLICKED";
    }
    return "NO_PUB";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_click}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Click: {resp[:150]}")
        
        await asyncio.sleep(8)
        
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_pub}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"FINAL URL: {r.get('url','?')[:150]}")

asyncio.run(medium_tiny())
