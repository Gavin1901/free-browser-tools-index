import urllib.request, json, asyncio, websockets, time

async def pub_medium():
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
        # Click Publish
        js = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let pub = btns.find(b => b.textContent.trim() === 'Publish' && b.offsetParent !== null && !b.disabled);
    if (pub) {
        pub.click();
        return "CLICKED_PUBLISH";
    }
    return "NO_BUTTON";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Click: {resp[:200]}")
        
        await asyncio.sleep(5)
        
        # Check current state / dialog
        js2 = '''
(function() {
    let r = {};
    r.url = window.location.href;
    // Check for publish confirmation dialog
    let dialogs = document.querySelectorAll('[role="dialog"], [data-testid="publishDialog"], .modal');
    r.dialogs = dialogs.length;
    if (dialogs.length > 0) {
        r.dialogText = dialogs[0].textContent.trim().substring(0, 200);
        let dialogBtns = dialogs[0].querySelectorAll('button');
        r.dialogButtons = [...dialogBtns].map(b => b.textContent.trim()).join("|");
    }
    // Check for green confirmation
    let pubAgain = [...document.querySelectorAll('button')].find(b => b.textContent.trim().includes('Publish') && b.offsetParent !== null);
    r.pubAgain = pubAgain ? "YES" : "NO";
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Post-click: {resp[:600]}")

asyncio.run(pub_medium())
