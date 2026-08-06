import urllib.request, json, asyncio, websockets, time

TITLE = "0 Clicks, 1180 Impressions: An Invoice Generator SEO Lesson"

async def fix_and_publish():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Set title in first contenteditable
        js_set_title = f'''
(function() {{
    let editables = document.querySelectorAll('[contenteditable="true"]');
    if (editables.length < 1) return "NO_EDITABLES";
    let titleEl = editables[0];
    titleEl.focus();
    titleEl.click();
    // Clear and set title
    titleEl.innerText = {json.dumps(TITLE)};
    titleEl.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "SET_" + titleEl.innerText.substring(0, 30);
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_set_title}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title set: {resp[:200]}")
        
        await asyncio.sleep(2)
        
        # Now click Publish
        js_pub = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let pub = btns.find(b => b.textContent.trim() === 'Publish' && b.offsetParent !== null && !b.disabled);
    if (pub) { pub.click(); return "CLICKED"; }
    return "NO_PUB";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_pub}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Publish: {resp[:200]}")
        
        await asyncio.sleep(6)
        
        # Check URL
        js_url = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"URL: {resp[:400]}")

asyncio.run(fix_and_publish())
