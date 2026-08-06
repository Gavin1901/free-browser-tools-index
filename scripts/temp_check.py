import urllib.request, json, asyncio, websockets, time

async def check():
    await asyncio.sleep(5)
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "dev.to" in url:
            print(f"Dev.to URL: {url}")
            
            ws_url = p["webSocketDebuggerUrl"]
            async with websockets.connect(ws_url, max_size=2**24) as ws:
                # Check for modal/secondary publish
                js = '''
(function() {
    let result = {};
    result.url = window.location.href;
    // Check for confirmation modal buttons
    let allBtns = document.querySelectorAll('button');
    result.visibleButtons = [...allBtns].filter(b => b.offsetParent !== null).map(b => b.textContent.trim()).join("|").substring(0, 200);
    // Check for any modal
    let modals = document.querySelectorAll('[role="dialog"], .modal, .crayons-modal');
    result.modalCount = modals.length;
    // Check for tags input
    let tagInput = document.querySelector('input[placeholder*="tag"], input[aria-label*="tag"]');
    result.tagInput = tagInput ? "FOUND" : "NONE";
    return JSON.stringify(result);
})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                print(f"Page state: {resp[:600]}")

asyncio.run(check())
