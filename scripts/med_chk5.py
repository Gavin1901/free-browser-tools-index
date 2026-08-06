import urllib.request, json, asyncio, websockets

async def check():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "medium.com" in url:
            async with websockets.connect(p["webSocketDebuggerUrl"], max_size=2**24) as ws:
                js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    let editables = document.querySelectorAll('[contenteditable="true"]');
    r.editables = [...editables].map(e => ({
        text: e.textContent.trim().substring(0, 80),
        len: e.textContent.length
    }));
    let popover = document.querySelector('.popover-description');
    r.popover = popover ? popover.textContent.trim() : "NONE";
    let pubBtn = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Publish');
    r.pubDisabled = pubBtn ? pubBtn.disabled : "NO_BTN";
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
                print(f"Editables: {r.get('editables')}")
                print(f"Popover: {r.get('popover')}")
                print(f"Pub disabled: {r.get('pubDisabled')}")
                
                # Try publish if button is available
                if r.get("pubDisabled") == False:
                    js2 = '''
(function() {
    let pub = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Publish' && !b.disabled);
    if (pub) { pub.click(); return "CLICKED"; }
    return "NOT_FOUND";
})()
'''
                    msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
                    await ws.send(msg)
                    resp = await asyncio.wait_for(ws.recv(), timeout=10)
                    print(f"Click: {resp[:200]}")
                    
                    import time
                    await asyncio.sleep(6)
                    
                    js3 = "window.location.href"
                    msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
                    await ws.send(msg)
                    resp = await asyncio.wait_for(ws.recv(), timeout=10)
                    data = json.loads(resp)
                    print(f"URL: {data['result']['result']['value']}")
            return

asyncio.run(check())
