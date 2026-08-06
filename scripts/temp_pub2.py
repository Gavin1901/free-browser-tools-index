import urllib.request, json, asyncio, websockets, time

async def pub():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "dev.to/new" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Click Publish button
        js = '''
(function() {
    let btns = document.querySelectorAll('button');
    for (let b of btns) {
        if (b.textContent.trim() === 'Publish' && b.offsetParent !== null && !b.disabled) {
            b.scrollIntoView({block: "center"});
            b.click();
            return "CLICKED_PUBLISH";
        }
    }
    let all = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null).map(b => b.textContent.trim()).join(", ");
    return "NOT_FOUND. Visible: " + all.substring(0, 200);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Click: {resp[:300]}")
        
        await asyncio.sleep(3)
        
        # Check for dialog/modal
        js2 = '''
(function() {
    let r = {};
    r.url = window.location.href;
    let dialogs = document.querySelectorAll('[role="dialog"], [role="alertdialog"], .crayons-modal');
    r.dialogCount = dialogs.length;
    if (dialogs.length > 0) {
        r.dialogText = dialogs[0].textContent.trim().substring(0, 300);
        let dialogBtns = dialogs[0].querySelectorAll('button');
        r.dialogButtons = [...dialogBtns].map(b => b.textContent.trim()).join("|");
    }
    let errors = document.querySelectorAll('.crayons-notice--danger, .crayons-notice');
    r.errors = [...errors].filter(e => e.offsetParent !== null).map(e => e.textContent.trim().substring(0, 200)).join(" ;; ");
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"State: {resp[:600]}")

asyncio.run(pub())
