import urllib.request, json, asyncio, websockets, time

async def check():
    await asyncio.sleep(5)
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    
    // Check all visible buttons
    let allBtns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null);
    r.buttons = allBtns.map(b => ({
        text: b.textContent.trim().substring(0, 40),
        disabled: b.disabled,
        cls: b.className.substring(0, 30)
    }));
    
    // Check for publish-related panels
    let panels = document.querySelectorAll('[class*="publish"], [class*="Publish"]');
    r.publishPanelCount = panels.length;
    
    // Check for green notification/success
    let greenThings = document.querySelectorAll('[class*="success"], [class*="green"], [data-testid="publishSuccess"]');
    r.successCount = greenThings.length;
    
    // Get page title
    r.pageTitle = document.title;
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(resp[:1500])

asyncio.run(check())
