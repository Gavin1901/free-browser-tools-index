import urllib.request, json, asyncio, websockets, time

async def trigger_draft():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Click into the content area first
        js_click = '''
(function() {
    let editables = document.querySelectorAll('[contenteditable="true"]');
    if (editables.length >= 2) {
        editables[1].focus();
        editables[1].click();
        // Place cursor at end
        let sel = window.getSelection();
        let range = document.createRange();
        range.selectNodeContents(editables[1]);
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
        return "FOCUSED_CONTENT";
    }
    return "NO_EDITOR";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_click}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Focus: {resp[:200]}")
        await asyncio.sleep(1)
        
        # Type a few characters to trigger draft detection
        trigger_text = " "
        for char in trigger_text:
            await ws.send(json.dumps({
                "id": 1,
                "method": "Input.dispatchKeyEvent",
                "params": {"type": "char", "text": char, "unmodifiedText": char}
            }))
            await asyncio.sleep(0.05)
        
        print("Trigger chars typed")
        await asyncio.sleep(3)
        
        # Check if popover changed
        js_check = '''
(function() {
    let popover = document.querySelector('.popover-description');
    let text = popover ? popover.textContent.trim() : "NO_POPOVER";
    let pubBtn = [...document.querySelectorAll('button')].find(b => 
        b.textContent.trim() === 'Publish' && b.className.includes('primary')
    );
    let pubDisabled = pubBtn ? pubBtn.disabled : "NO_BTN";
    return JSON.stringify({popover: text, pubDisabled: pubDisabled});
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_check}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"After trigger: {resp[:400]}")

asyncio.run(trigger_draft())
