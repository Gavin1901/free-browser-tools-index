import urllib.request, json, asyncio, websockets, time

MED_TITLE = "InvoicePad SEO: 1180 Impressions, Zero Clicks"
MED_BODY = """Google Search Console shows InvoicePad (https://invoicepad.net) has 1180 impressions but zero clicks. People search for specific invoice templates like "web development invoice" and "handyman invoice template." The free tool works but the landing page doesn't match search intent. Dedicated template pages coming soon."""

async def medium_type():
    # Create fresh target
    browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
    
    async with websockets.connect(browser_ws, max_size=2**24) as bws:
        msg = json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://medium.com/new-story"}})
        await bws.send(msg)
        resp = await asyncio.wait_for(bws.recv(), timeout=15)
        target_id = json.loads(resp)["result"]["targetId"]
        print(f"Target: {target_id}")
    
    await asyncio.sleep(8)
    
    # Find Medium page
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    med_ws = None
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "medium.com" in url:
            med_ws = p["webSocketDebuggerUrl"]
            print(f"Medium: {url[:100]}")
            break
    
    if not med_ws:
        print("Medium not found")
        return
    
    async with websockets.connect(med_ws, max_size=2**24) as ws:
        # Wait for editor to fully load
        await asyncio.sleep(3)
        
        # Find contenteditable elements
        js = '''
(function() {
    let editables = document.querySelectorAll('[contenteditable="true"]');
    return JSON.stringify([...editables].map(e => ({
        visible: e.offsetParent !== null,
        text: e.textContent.trim().substring(0, 30)
    })));
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Editables: {resp[:300]}")
        
        # Click first editable (title area)
        js_click = '''
(function() {
    let editables = document.querySelectorAll('[contenteditable="true"]');
    if (editables.length > 0) {
        editables[0].focus();
        editables[0].click();
        // Clear placeholder
        document.execCommand("selectAll", false, null);
        document.execCommand("delete", false, null);
        return "FOCUSED_TITLE";
    }
    return "NO_EDITOR";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_click}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Focus title: {resp[:200]}")
        await asyncio.sleep(1)
        
        # Type title
        for char in MED_TITLE:
            await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"char","text":char,"unmodifiedText":char}}))
            await asyncio.sleep(0.02)
        print("Title typed")
        await asyncio.sleep(2)
        
        # Press Enter to move to content area
        await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"keyDown","key":"Enter","code":"Enter","keyCode":13}}))
        await asyncio.sleep(0.1)
        await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"keyUp","key":"Enter","code":"Enter","keyCode":13}}))
        await asyncio.sleep(2)
        
        # Type body
        for char in MED_BODY:
            await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"char","text":char,"unmodifiedText":char}}))
            await asyncio.sleep(0.015)
        print("Body typed")
        await asyncio.sleep(3)
        
        # Check popover
        js_pop = '''
(function() {
    let popover = document.querySelector('.popover-description');
    return popover ? popover.textContent.trim().substring(0, 100) : "NO_POPOVER";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_pop}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(f"Popover: {data['result']['result']['value']}")
        
        # Try publish
        js_pub = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let pub = btns.find(b => b.textContent.trim() === 'Publish' && b.className.includes('primary') && b.offsetParent !== null && !b.disabled);
    if (pub) {
        pub.click();
        return "CLICKED";
    }
    return "NO_PUB";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_pub}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Publish: {resp[:200]}")
        
        await asyncio.sleep(8)
        
        js_final = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_final}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(f"Final URL: {data['result']['result']['value']}")

asyncio.run(medium_type())
