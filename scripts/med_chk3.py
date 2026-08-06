import urllib.request, json, asyncio, websockets, time

async def check_and_pub():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Comprehensive check
        js = '''
(function() {
    try {
        let r = {};
        let popover = document.querySelector('.popover-description');
        r.popoverText = popover ? popover.textContent.trim() : "NONE";
        let pubBtn = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Publish');
        r.pubDisabled = pubBtn ? pubBtn.disabled : "NO_BTN";
        r.pubBtnClass = pubBtn ? pubBtn.className.substring(0, 50) : "NONE";
        r.url = window.location.href;
        return JSON.stringify(r);
    } catch(e) {
        return JSON.stringify({error: e.toString()});
    }
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val)
            print(f"State: popover={r.get('popoverText')}, pubDisabled={r.get('pubDisabled')}, url={r.get('url')}")
            
            # If pub is not disabled, click it
            if r.get("pubDisabled") == False:
                js2 = '''
(function() {
    let pub = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Publish' && !b.disabled);
    if (pub) {
        pub.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
        return "CLICKED";
    }
    return "NOT_FOUND";
})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                print(f"Click: {resp[:200]}")
                await asyncio.sleep(5)
                
                # Check URL change
                js3 = "window.location.href"
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                print(f"URL: {resp[:300]}")
        else:
            print("Pub button is disabled or not found")
        else:
            print(f"Raw response: {resp[:500]}")

asyncio.run(check_and_pub())
