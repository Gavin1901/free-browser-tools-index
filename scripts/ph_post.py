import urllib.request, json, asyncio, websockets, time

PH_TITLE = "InvoicePad: 0 clicks on 1,180 Google impressions — a search intent lesson"
PH_BODY = """I analyzed GSC data for InvoicePad (https://invoicepad.net) and found 1,180 impressions with zero clicks. The free invoice generator works perfectly but people search for specific templates like "handyman invoice template" (33 impressions) and "web development invoice" (88 impressions). The tool is right. The landing page positioning is wrong. Building dedicated template pages now."""

async def ph():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "producthunt.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Step 1: Select forum - Click the Select Forum input
        js_forum = '''
(function() {
    let forumInput = document.querySelector('input[placeholder="Select Forum"]');
    if (forumInput) {
        forumInput.click();
        return "CLICKED_FORUM";
    }
    return "NOT_FOUND";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_forum}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Forum click: {resp[:150]}")
        await asyncio.sleep(2)
        
        # Step 2: Select "General" forum - look for dropdown options
        js_select = '''
(function() {
    let options = [...document.querySelectorAll('[role="option"], [role="menuitem"], li, div')];
    let general = options.find(el => {
        let t = el.textContent.toLowerCase();
        return (t.includes('general') || t.includes('self-promotion')) && el.offsetParent !== null;
    });
    if (general) {
        general.click();
        return "SELECTED:" + general.textContent.trim().substring(0, 30);
    }
    return "NOT_FOUND:" + options.filter(o=>o.offsetParent!==null).map(o=>o.textContent.trim().substring(0,30)).filter(t=>t).slice(0,5).join(",");
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_select}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Forum select: {resp[:200]}")
        await asyncio.sleep(1)
        
        # Step 3: Fill title
        js_title = f'''
(function() {{
    let titleInput = document.querySelector('input[placeholder*="Title"]');
    if (!titleInput) titleInput = document.querySelector('input[name="title"]');
    if (!titleInput) return "NO_TITLE";
    let ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
    ns.call(titleInput, {json.dumps(PH_TITLE)});
    titleInput.dispatchEvent(new Event("input", {{bubbles: true}}));
    titleInput.dispatchEvent(new Event("change", {{bubbles: true}}));
    return "FILLED:" + titleInput.value.length;
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_title}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title: {resp[:150]}")
        await asyncio.sleep(1)
        
        # Step 4: Fill content in TipTap editor
        js_content = f'''
(function() {{
    let ed = document.querySelector('[contenteditable="true"]');
    if (!ed) return "NO_EDITOR";
    ed.focus();
    ed.click();
    // Try execCommand approach
    document.execCommand("selectAll", false, null);
    document.execCommand("insertText", false, {json.dumps(PH_BODY)});
    return "FILLED:" + ed.textContent.length;
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_content}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Content: {resp[:150]}")
        await asyncio.sleep(2)
        
        # Step 5: Find and click Submit/Post button
        js_sub = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let submit = btns.find(b => {
        let t = b.textContent.toLowerCase().trim();
        return (t === 'submit' || t === 'post' || t === 'create thread' || t === 'publish') && b.offsetParent !== null && !b.disabled;
    });
    if (submit) { submit.click(); return "CLICKED:" + submit.textContent.trim(); }
    return "NO_SUBMIT:" + btns.filter(b=>b.offsetParent!==null&&!b.disabled).map(b=>b.textContent.trim()).filter(t=>t.length>0&&t.length<20).join(",");
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_sub}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Submit: {resp[:200]}")
        await asyncio.sleep(6)
        
        # Final check
        js_final = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_final}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(f"Final URL: {data.get('result',{}).get('result',{}).get('value','?')[:150]}")

asyncio.run(ph())
