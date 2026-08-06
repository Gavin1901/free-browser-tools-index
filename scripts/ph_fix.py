import urllib.request, json, asyncio, websockets, time

async def ph_fix():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "producthunt.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Check for errors
        js = "JSON.stringify({url:window.location.href, errors:[...document.querySelectorAll('[class*=\"error\"], [class*=\"Error\"], [role=\"alert\"]')].filter(e=>e.offsetParent!==null).map(e=>e.textContent.trim().substring(0,100)), bodyStart:document.body.innerText.substring(0, 500)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"Errors: {r.get('errors',[])}")
            print(f"Body: {str(r.get('bodyStart',''))[:400]}")
        
        # Reload and try again fresh
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.producthunt.com/p/new"}}))
        await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(4)
        
        # Now carefully select forum
        js = '''
(async function() {
    // Click Select Forum
    let forumInput = document.querySelector('input[placeholder="Select Forum"]');
    if (!forumInput) return "NO_FORUM_INPUT";
    forumInput.click();
    await new Promise(r => setTimeout(r, 1000));
    
    // Find and click "General" in the dropdown
    let all = [...document.querySelectorAll('[role="option"], li, div, span')];
    let general = all.find(el => {
        let t = el.textContent.trim();
        return t === 'General' && el.offsetParent !== null;
    });
    if (!general) {
        // Try looser match
        general = all.find(el => {
            let t = el.textContent.trim().toLowerCase();
            return t.includes('general') && el.offsetParent !== null && t.length < 20;
        });
    }
    if (general) {
        general.click();
        return "SELECTED_GENERAL:" + general.textContent.trim();
    }
    // List available options
    let opts = all.filter(el => el.offsetParent !== null && el.textContent.trim().length > 2 && el.textContent.trim().length < 30);
    return "NOT_FOUND. Options: " + [...new Set(opts.map(o=>o.textContent.trim()))].slice(0,10).join(", ");
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js, "awaitPromise": True}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        data = json.loads(resp)
        result = data.get("result",{}).get("result",{}).get("value","")
        print(f"Forum: {result}")

asyncio.run(ph_fix())
