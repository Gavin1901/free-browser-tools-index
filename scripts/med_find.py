import urllib.request, json, asyncio, websockets

async def find_pub():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Find ALL visible Publish-related elements
        js = '''
(function() {
    let r = {};
    
    // All buttons
    let btns = [...document.querySelectorAll('button')];
    r.allBtns = btns.filter(b => b.offsetParent !== null).map(b => ({
        text: b.textContent.trim().substring(0, 50),
        disabled: b.disabled,
        cls: b.className.substring(0, 40)
    }));
    
    // All links that say Publish
    let links = [...document.querySelectorAll('a')];
    r.pubLinks = links.filter(l => l.textContent.toLowerCase().includes('publish') && l.offsetParent !== null).map(l => l.textContent.trim());
    
    // Any element with publish text
    let allEls = [...document.querySelectorAll('*')];
    r.pubTexts = [...new Set(allEls.filter(el => 
        el.children.length === 0 && 
        el.offsetParent !== null &&
        el.textContent.trim().toLowerCase().includes('publish')
    ).map(el => el.textContent.trim().substring(0, 60)))].slice(0, 20);
    
    // Check for publish flow sidebar/dialog
    r.dialogs = [...document.querySelectorAll('[role="dialog"], [role="menu"]')].map(d => ({
        role: d.getAttribute("role"),
        text: d.textContent.trim().substring(0, 200),
        visible: d.offsetParent !== null
    }));
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data["result"]["result"]["value"]
        if isinstance(val, str):
            r = json.loads(val)
        else:
            r = val
        print("Buttons:")
        for b in r.get("allBtns", []):
            print(f"  [{b['disabled']}] {b['text'][:40]:40s} {b['cls'][:30]}")
        print(f"\nPublish texts: {r.get('pubTexts', [])}")
        print(f"\nDialogs: {r.get('dialogs', [])}")

asyncio.run(find_pub())
