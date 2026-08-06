import urllib.request, json, asyncio, websockets, time

async def check_and_publish():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com/new-story" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    if not ws_url:
        print("ERROR")
        return
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Check page content state
        js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    r.bodyText = document.body.innerText.substring(0, 500);
    // Look for publish button
    let btns = [...document.querySelectorAll('button')];
    let pubBtn = btns.find(b => b.textContent.trim().toLowerCase().includes('publish') && b.offsetParent !== null);
    r.pubBtn = pubBtn ? (pubBtn.textContent.trim() + "|" + (pubBtn.disabled ? "D" : "E")) : "NONE";
    // All visible buttons
    r.visibleBtns = btns.filter(b => b.offsetParent !== null).map(b => b.textContent.trim().substring(0, 30)).join("|");
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"State: {resp[:800]}")

asyncio.run(check_and_publish())
