import urllib.request, json, asyncio, websockets, time

DEVTO_TITLE = "What InvoicePad Taught Me About Search Intent"
DEVTO_TAGS = "seo,webdev,freelancing,invoice"

async def devto():
    # Create new target via browser WS
    browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
    
    async with websockets.connect(browser_ws, max_size=2**24) as bws:
        msg = json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://dev.to/new"}})
        await bws.send(msg)
        resp = await asyncio.wait_for(bws.recv(), timeout=15)
        data = json.loads(resp)
        target_id = data["result"]["targetId"]
        print(f"Target: {target_id}")
    
    await asyncio.sleep(8)  # Wait for full page load including JS
    
    # Find Dev.to page
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    dev_ws = None
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "dev.to" in url:
            dev_ws = p["webSocketDebuggerUrl"]
            print(f"Dev.to: {url[:120]}")
            break
    
    if not dev_ws:
        print("Dev.to page not found")
        return
    
    async with websockets.connect(dev_ws, max_size=2**24) as ws:
        # Check editor state
        js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    let editables = document.querySelectorAll('[contenteditable="true"]');
    r.editableCount = editables.length;
    r.editableStates = [...editables].map(e => ({
        visible: e.offsetParent !== null,
        text: e.textContent.trim().substring(0, 50)
    }));
    
    // Look for title input
    let titleInput = document.querySelector('input[aria-label*="Title"], input[placeholder*="title" i], #article-form-title');
    r.titleInput = titleInput ? "FOUND_" + (titleInput.offsetParent !== null ? "VISIBLE" : "HIDDEN") : "MISSING";
    
    // Check for tag input
    let tagInput = document.querySelector('input[placeholder*="tag" i], input[aria-label*="tag" i]');
    r.tagInput = tagInput ? "FOUND" : "MISSING";
    
    // Check for publish button
    let pubBtn = [...document.querySelectorAll('button')].find(b => b.textContent.trim().includes('Publish'));
    r.pubBtn = pubBtn ? "FOUND_" + (pubBtn.offsetParent !== null ? "VISIBLE" : "HIDDEN") : "MISSING";
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = json.loads(data["result"]["result"]["value"])
        print(f"Editor state: {val}")
        
        r = json.loads(val)
        
        # Fill title using native setter
        if r.get("titleInput", "").startswith("FOUND"):
            js_title = f'''
(function() {{
    let input = document.querySelector('input[aria-label*="Title"], input[placeholder*="title" i]');
    if (!input) {{
        let inputs = [...document.querySelectorAll("input[type='text']")];
        input = inputs.find(i => i.offsetParent !== null);
    }}
    if (!input) return "NO_INPUT";
    let ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
    ns.call(input, {json.dumps(DEVTO_TITLE)});
    input.dispatchEvent(new Event("input", {{bubbles: true}}));
    input.dispatchEvent(new Event("change", {{bubbles: true}}));
    return "FILLED_TITLE";
}})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_title}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            print(f"Title: {resp[:150]}")
        
        # Add tags
        if r.get("tagInput") == "FOUND":
            for tag in DEVTO_TAGS.split(","):
                js_tag = f'''
(function() {{
    let input = document.querySelector('input[placeholder*="tag" i]');
    if (!input) return "NO";
    let ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
    ns.call(input, "{tag.strip()}");
    input.dispatchEvent(new Event("input", {{bubbles: true}}));
    input.dispatchEvent(new KeyboardEvent("keydown", {{key: "Enter", code: "Enter", keyCode: 13, bubbles: true}}));
    return "TAG_{tag}";
}})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_tag}})
                await ws.send(msg)
                await asyncio.wait_for(ws.recv(), timeout=5)
                await asyncio.sleep(1)
            print("Tags added")
        
        # Content: check if we need to type or if editor accepts paste
        if r.get("editableCount", 0) > 0:
            # Try typing into the editor using keyboard
            editables = r.get("editableStates", [])
            for es in editables:
                if es.get("visible") and es.get("text", "").strip() == "":
                    print(f"Empty editable found, will type content...")
                    
                    # Type content char by char
                    content = "GSC shows InvoicePad (invoicepad.net) has 1180 impressions but zero clicks. Users search for specific templates like web development invoice and handyman invoice template. The tool works but positioning doesn't match search intent. Dedicated landing pages coming soon. Try it free at https://invoicepad.net."
                    
                    for char in content:
                        await ws.send(json.dumps({
                            "id": 99,
                            "method": "Input.dispatchKeyEvent",
                            "params": {"type": "char", "text": char, "unmodifiedText": char}
                        }))
                        if len(content) > 200:
                            await asyncio.sleep(0.005)
                        else:
                            await asyncio.sleep(0.01)
                    
                    print("Content typed")
                    await asyncio.sleep(3)
                    break
        
        # Try publish
        js_pub = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let pub = btns.find(b => b.textContent.trim() === 'Publish' && b.offsetParent !== null && !b.disabled);
    if (pub) { pub.click(); return "CLICKED"; }
    return "NO_PUB";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_pub}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Publish: {resp[:200]}")
        
        await asyncio.sleep(6)
        
        js_url = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        final_url = data["result"]["result"]["value"]
        print(f"Final URL: {final_url}")
        
        # Check for errors
        js_err = '''
(function() {
    let notices = [...document.querySelectorAll('.crayons-notice')].filter(n => n.offsetParent).map(n => n.textContent.trim().substring(0,200));
    return JSON.stringify(notices);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_err}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(f"Errors: {data['result']['result']['value']}")

asyncio.run(devto())
