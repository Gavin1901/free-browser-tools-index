import urllib.request, json, asyncio, websockets, time

async def pub_medium():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    if not ws_url:
        print("ERROR")
        return

    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Comprehensive page state check
        js = '''
(function() {
    let r = {};
    r.url = window.location.href;

    // Check for publish dropdown/menu that opens
    let allVisible = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null);
    r.visibleButtons = allVisible.map(b => ({
        text: b.textContent.trim().substring(0, 40),
        disabled: b.disabled,
        tag: b.tagName,
        className: b.className.substring(0, 30)
    }));

    // Check for dialogs
    let dialogs = document.querySelectorAll('[role="dialog"], [data-testid="publishDialog"], .modal');
    r.dialogCount = dialogs.length;
    if (dialogs.length > 0) {
        r.dialogHTML = dialogs[0].outerHTML.substring(0, 500);
    }

    // Check for any overlay
    let overlays = document.querySelectorAll('[class*="overlay"], [class*="Overlay"]');
    r.overlayCount = overlays.length;

    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(resp[:2000])

asyncio.run(pub_medium())
