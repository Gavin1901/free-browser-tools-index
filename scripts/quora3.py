import urllib.request, json, asyncio, websockets, time

QUORA_CONTENT = """I run a free invoice generator at https://invoicepad.net and recently checked Google Search Console. 1,180 impressions, zero clicks.

The tool works fine — pick a template, fill details, download PDF. But people search for "web development invoice" (88 impressions) and "handyman invoice template" (33 impressions), not "free invoice generator."

The lesson: search intent matters more than tool quality. We are now building profession-specific landing pages."""

async def quora_post():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "quora.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Navigate to create a post
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.quora.com/"}}))
        await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(4)
        
        # Click "Add question" or find post creation
        js_find = '''
(function() {
    // Click Add question / create post
    let addBtn = [...document.querySelectorAll('button, a')].find(el => 
        (el.textContent.toLowerCase().includes('add question') || el.textContent.toLowerCase().includes('create post')) &&
        el.offsetParent !== null
    );
    if (addBtn) {
        addBtn.click();
        return "CLICKED_ADD";
    }
    return "NOT_FOUND";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_find}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Add btn: {resp[:200]}")
        await asyncio.sleep(4)
        
        # Check for editor
        js_ed = '''
(function() {
    let r = {};
    r.url = window.location.href;
    let editables = document.querySelectorAll('[contenteditable="true"], textarea');
    r.editorCount = editables.length;
    if (editables.length > 0) {
        r.firstEditor = editables[0].tagName + ":" + (editables[0].placeholder || "") + ":" + (editables[0].textContent || "").substring(0, 50);
    }
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_ed}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"After add: url={r.get('url','?')[:100]}, editors={r.get('editorCount')}, first={r.get('firstEditor','?')}")

asyncio.run(quora_post())
