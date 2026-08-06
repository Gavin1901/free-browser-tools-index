import urllib.request, json, asyncio, websockets

async def fix_medium_title():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Check title area specifically
        js = '''
(function() {
    let r = {};
    // Try to find the title element
    let h3 = document.querySelector('h3[data-testid="storyTitle"]');
    r.h3Text = h3 ? h3.textContent.trim().substring(0, 100) : "NO_H3";
    
    // All visible contenteditables and their text
    let editables = [...document.querySelectorAll('[contenteditable="true"]')];
    r.editables = editables.map((e, i) => ({
        index: i,
        tag: e.tagName,
        text: e.textContent.trim().substring(0, 100),
        visible: e.offsetParent !== null
    }));
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(resp[:800])

asyncio.run(fix_medium_title())
