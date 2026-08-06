import urllib.request, json, asyncio, websockets, time

async def medium_last_stand():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com/new-story" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    if not ws_url:
        print("Medium not found")
        return
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Check current state
        js = "JSON.stringify({title:document.title, bodyLen:document.body.innerText.length, pubVisible:[...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null&&b.textContent.trim()==='Publish').length, contentText:document.querySelectorAll('[contenteditable=\"true\"]')[0]?.textContent?.substring(0,60)||'NONE'})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = json.loads(data["result"]["result"]["value"])
        print(f"State: {val}")
        
        r = json.loads(val)
        
        # Approach 1: Ctrl+Enter on editor
        js_ctrl = '''
(function() {
    let editables = document.querySelectorAll('[contenteditable="true"]');
    let target = editables.length >= 2 ? editables[1] : editables[0];
    if (target) {
        target.focus();
        target.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, ctrlKey: true, metaKey: true, bubbles: true}));
    }
    return "CTRL_ENTER_DISPATCHED";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_ctrl}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Ctrl+Enter: {resp[:150]}")
        await asyncio.sleep(4)
        
        # Check URL
        js_url = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        url = data["result"]["result"]["value"]
        print(f"URL after Ctrl+Enter: {url[:100]}")
        
        if "/new-story" in url:
            # Approach 2: Find ALL possible publish triggers
            js2 = '''
(function() {
    let r = {};
    // Find the Publish button and all its attributes
    let pub = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Publish' && b.className.includes('primary'));
    if (pub) {
        r.pubHTML = pub.outerHTML.substring(0, 300);
        r.pubParent = pub.parentElement?.className?.toString()?.substring(0, 50);
        r.pubGrandparent = pub.parentElement?.parentElement?.className?.toString()?.substring(0, 50);
        // Try clicking the parent (sometimes the button has a wrapper)
        r.pubRect = (() => { let rect = pub.getBoundingClientRect(); return {x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height)}; })();
    }
    
    // Find ALL elements with data-action or data-testid that might trigger publish
    let pubTriggers = [...document.querySelectorAll('[data-action*="publish" i], [data-testid*="publish" i], [aria-label*="publish" i]')];
    r.pubTriggers = pubTriggers.map(e => ({tag: e.tagName, action: e.getAttribute('data-action')||'', testid: e.getAttribute('data-testid')||''}));
    
    return JSON.stringify(r);
})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            val = json.loads(data["result"]["result"]["value"])
            r2 = json.loads(val)
            print(f"Pub button: {r2.get('pubHTML','?')[:200]}")
            print(f"Pub triggers: {r2.get('pubTriggers', [])}")
            
            # Approach 3: Click the button's parent container
            if r2.get("pubRect"):
                rect = r2["pubRect"]
                cx = rect["x"] + rect["w"] // 2
                cy = rect["y"] + rect["h"] // 2
                print(f"Mouse clicking at ({cx}, {cy})...")
                await ws.send(json.dumps({"id":10,"method":"Input.dispatchMouseEvent","params":{"type":"mouseMoved","x":cx,"y":cy}}))
                await asyncio.sleep(0.1)
                await ws.send(json.dumps({"id":11,"method":"Input.dispatchMouseEvent","params":{"type":"mousePressed","x":cx,"y":cy,"button":"left","clickCount":1}}))
                await asyncio.sleep(0.15)
                await ws.send(json.dumps({"id":12,"method":"Input.dispatchMouseEvent","params":{"type":"mouseReleased","x":cx,"y":cy,"button":"left","clickCount":1}}))
                await asyncio.sleep(5)
            
            # Check URL again
            js3 = "window.location.href"
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            print(f"Final URL: {data['result']['result']['value'][:120]}")

asyncio.run(medium_last_stand())
