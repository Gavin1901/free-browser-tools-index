import urllib.request, json, asyncio, websockets

async def check_modal():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "dev.to" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    // Look for all visible buttons with detailed info
    let all = document.querySelectorAll('button, [role="button"], a.button');
    r.buttons = [];
    for (let b of all) {
        if (b.offsetParent !== null) {
            r.buttons.push(b.textContent.trim().substring(0, 30) + "|" + (b.disabled ? "D" : "E") + "|" + b.tagName);
        }
    }
    r.buttons = r.buttons.join(" ;; ");
    // Check modals
    let modals = document.querySelectorAll('[role="dialog"], [role="alertdialog"], .crayons-modal, .modal-container');
    r.modalHTML = "";
    for (let m of modals) {
        if (m.offsetParent !== null) {
            r.modalHTML += m.textContent.trim().substring(0, 200) + "|||";
        }
    }
    // Check the page for any flash/notice
    let notices = document.querySelectorAll('.crayons-notice, .flash, [role="alert"]');
    r.notices = [...notices].filter(n => n.offsetParent !== null).map(n => n.textContent.trim().substring(0, 100)).join(" ;; ");
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(resp[:800])

asyncio.run(check_modal())
