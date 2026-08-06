import urllib.request, json, asyncio, websockets, time

async def mouse_pub():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com/new-story" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Get button position
        js = '''
(function() {
    let pub = [...document.querySelectorAll('button')].find(b => 
        b.textContent.trim() === 'Publish' && b.className.includes('primary')
    );
    if (!pub) return JSON.stringify({error: "NO_BTN"});
    let r = pub.getBoundingClientRect();
    return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = json.loads(data["result"]["result"]["value"])
        cx, cy = val["x"], val["y"]
        print(f"Button at ({cx}, {cy})")
        
        # Full mouse click sequence
        await ws.send(json.dumps({"id":2,"method":"Input.dispatchMouseEvent","params":{"type":"mouseMoved","x":cx,"y":cy}}))
        await asyncio.sleep(0.15)
        await ws.send(json.dumps({"id":3,"method":"Input.dispatchMouseEvent","params":{"type":"mousePressed","x":cx,"y":cy,"button":"left","clickCount":1}}))
        await asyncio.sleep(0.2)
        await ws.send(json.dumps({"id":4,"method":"Input.dispatchMouseEvent","params":{"type":"mouseReleased","x":cx,"y":cy,"button":"left","clickCount":1}}))
        print("Mouse click done")
        
        await asyncio.sleep(4)
        
        # Check what appeared
        js2 = '''
(function() {
    let r = {};
    r.url = window.location.href;
    
    // Check for publish flow (sidebar/drawer)
    let allText = document.body.innerText;
    
    // Find "Publish" after clicking
    let allVisible = [...document.querySelectorAll('button, a, span, div, h2, h3')].filter(el => {
        if (!el.offsetParent) return false;
        if (el.children.length > 0) return false;
        let t = el.textContent.trim();
        return t.includes('Publish') || t.includes('publish') || t.includes('Ready');
    });
    r.pubElements = allVisible.map(el => ({
        tag: el.tagName,
        text: el.textContent.trim().substring(0, 60),
        rect: (() => { let r = el.getBoundingClientRect(); return {x: Math.round(r.x), y: Math.round(r.y)}; })()
    }));
    
    // Check for topic/tag section
    let topics = document.querySelectorAll('[class*="topic"], [class*="Topic"], [class*="tag"], [class*="Tag"]');
    r.topicCount = topics.length;
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data["result"]["result"]["value"]
        if isinstance(val, str):
            r = json.loads(val)
        else:
            r = val
        print(f"Publish elements after click: {json.dumps(r.get('pubElements', []), indent=2)[:800]}")
        print(f"Topic count: {r.get('topicCount')}")
        
        # If there are multiple publish elements, click the one that's not at the top
        pub_els = r.get("pubElements", [])
        if len(pub_els) >= 2:
            for pel in pub_els:
                if pel.get("rect", {}).get("y", 0) > 100:  # Not the top button
                    cx2 = pel["rect"]["x"] + 30
                    cy2 = pel["rect"]["y"] + 10
                    print(f"Clicking secondary Publish at ({cx2}, {cy2}): {pel['text']}")
                    await ws.send(json.dumps({"id":5,"method":"Input.dispatchMouseEvent","params":{"type":"mouseMoved","x":cx2,"y":cy2}}))
                    await asyncio.sleep(0.1)
                    await ws.send(json.dumps({"id":6,"method":"Input.dispatchMouseEvent","params":{"type":"mousePressed","x":cx2,"y":cy2,"button":"left","clickCount":1}}))
                    await asyncio.sleep(0.15)
                    await ws.send(json.dumps({"id":7,"method":"Input.dispatchMouseEvent","params":{"type":"mouseReleased","x":cx2,"y":cy2,"button":"left","clickCount":1}}))
                    await asyncio.sleep(5)
                    break
        
        # Final check
        js3 = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(f"Final URL: {data['result']['result']['value']}")

asyncio.run(mouse_pub())
