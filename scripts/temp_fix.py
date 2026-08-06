import urllib.request, json, asyncio, websockets

SHORT_TITLE = "0 Clicks on 1,180 Impressions: What InvoicePad Taught Me"

async def fix_and_publish():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "dev.to/new" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    if not ws_url:
        print("ERROR")
        return
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Fix title
        js = f'''
(function() {{
    let titleEl = document.querySelector('input[aria-label*="Title"], input[placeholder*="Title"]');
    if (!titleEl) {{
        let inputs = document.querySelectorAll("input");
        for (let i of inputs) {{
            if (i.offsetParent !== null && (i.type === "text" || !i.type)) {{
                titleEl = i;
                break;
            }}
        }}
    }}
    if (!titleEl) return "NO_TITLE";
    let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
    nativeSetter.call(titleEl, {json.dumps(SHORT_TITLE)});
    titleEl.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "TITLE_FIXED: " + titleEl.value.length + " chars";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title fix: {resp[:200]}")
        
        await asyncio.sleep(2)
        
        # Click Publish
        js_click = '''
(function() {
    let btns = document.querySelectorAll('button');
    for (let b of btns) {
        if (b.textContent.trim() === 'Publish' && !b.disabled && b.offsetParent !== null) {
            b.click();
            return "CLICKED";
        }
    }
    return "NOT_FOUND";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_click}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Publish: {resp[:200]}")
        
        await asyncio.sleep(6)
        
        # Check final URL and any errors
        js_check = '''
(function() {
    let r = {};
    r.url = window.location.href;
    let notices = document.querySelectorAll('.crayons-notice, [role="alert"]');
    r.notices = [...notices].filter(n => n.offsetParent !== null).map(n => n.textContent.trim().substring(0, 200)).join(" ;; ");
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_check}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Final: {resp[:600]}")

asyncio.run(fix_and_publish())
