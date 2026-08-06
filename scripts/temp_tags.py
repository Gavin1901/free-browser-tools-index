import urllib.request, json, asyncio, websockets, time

async def add_tags_and_publish():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "dev.to/new" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    if not ws_url:
        print("ERROR: not found")
        return
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Add tags
        tags = ["seo", "webdev", "freelancing", "invoice", "tools"]
        for tag in tags:
            js = f'''
(function() {{
    let input = document.querySelector('input[placeholder*="tag"], input[aria-label*="tag"]');
    if (!input) return "NO_TAG_INPUT";
    let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
    nativeSetter.call(input, "{tag}");
    input.dispatchEvent(new Event("input", {{bubbles: true}}));
    input.dispatchEvent(new KeyboardEvent("keydown", {{key: "Enter", code: "Enter", keyCode: 13, bubbles: true}}));
    input.dispatchEvent(new KeyboardEvent("keyup", {{key: "Enter", code: "Enter", keyCode: 13, bubbles: true}}));
    return "TAG_ADDED: {tag}";
}})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=5)
            await asyncio.sleep(1)
            print(f"Tag {tag}: {resp[:150]}")
        
        # Now click Publish again
        await asyncio.sleep(2)
        js_click = '''
(function() {
    let btns = document.querySelectorAll('button');
    for (let b of btns) {
        if (b.textContent.toLowerCase().includes('publish') && !b.disabled) {
            b.click();
            return "CLICKED_PUBLISH";
        }
    }
    return "NO_PUBLISH";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_click}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Publish click: {resp[:200]}")
        
        await asyncio.sleep(5)
        
        # Check URL again
        js_url = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Final URL: {resp[:300]}")

asyncio.run(add_tags_and_publish())
