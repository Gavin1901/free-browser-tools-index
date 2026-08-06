import urllib.request, json, asyncio, websockets, time

async def simple():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "medium.com" in url:
            print(f"Medium: {url[:120]}")
            if "/new-story" not in url:
                print(">>> ALREADY PUBLISHED! <<<")
                return
            
            async with websockets.connect(p["webSocketDebuggerUrl"], max_size=2**24) as ws:
                # Simplest possible publish attempt
                js = '''
(function() {
    // Try clicking every element that says Publish
    let allEls = document.querySelectorAll('button, a, span, div');
    let clicked = [];
    for (let el of allEls) {
        if (el.textContent.trim() === 'Publish' && el.offsetParent !== null && !el.disabled) {
            el.click();
            clicked.push(el.tagName);
            if (clicked.length >= 3) break;
        }
    }
    return "CLICKED:" + clicked.join(",");
})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(resp)
                result = data.get("result",{}).get("result",{}).get("value","")
                print(f"Click: {result}")
                
                await asyncio.sleep(6)
                
                js2 = "window.location.href"
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(resp)
                final_url = data.get("result",{}).get("result",{}).get("value","")
                print(f"URL: {final_url[:120]}")
            return

asyncio.run(simple())
