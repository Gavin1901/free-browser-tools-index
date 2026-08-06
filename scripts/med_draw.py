import urllib.request, json, asyncio, websockets

async def find_drawer():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com/new-story" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        js = '''
(function() {
    let drawers = document.querySelectorAll('[class*="drawer"], [class*="Drawer"], [class*="panel"], [class*="Panel"]');
    return JSON.stringify([...drawers].filter(d => d.offsetParent !== null).map(d => ({
        cls: (d.className || '').toString().substring(0, 60),
        text: d.textContent.trim().substring(0, 300),
        btns: [...d.querySelectorAll('button')].map(b => b.textContent.trim().substring(0, 30)).filter(t => t)
    })));
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
        for i, d in enumerate(r):
            print(f"\nDrawer {i}: {d.get('cls','?')[:60]}")
            print(f"  Text: {d.get('text','')[:200]}")
            print(f"  Buttons: {d.get('btns', [])}")

asyncio.run(find_drawer())
