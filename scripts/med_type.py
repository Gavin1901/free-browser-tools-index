import urllib.request, json, asyncio, websockets, time

KICKSTART_TEXT = """After checking Google Search Console for InvoicePad, I found 1180 impressions but zero clicks. The free invoice generator at invoicepad.net works perfectly, but people search for specific templates like web development invoice or handyman invoice template. The tool is right, the positioning is wrong."""

async def type_text():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Click into the SECOND contenteditable (content area)
        js = '''
(function() {
    let editables = document.querySelectorAll('[contenteditable="true"]');
    if (editables.length >= 2) {
        editables[1].click();
        editables[1].focus();
        // Select all existing content
        let sel = window.getSelection();
        let range = document.createRange();
        range.selectNodeContents(editables[1]);
        sel.removeAllRanges();
        sel.addRange(range);
        // Delete existing content
        document.execCommand('delete');
        return "CLEARED_CONTENT";
    }
    return "NO_EDITOR";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Clear: {resp[:200]}")
        await asyncio.sleep(1)
        
        # Type the kickstart text char by char
        print(f"Typing {len(KICKSTART_TEXT)} chars...")
        for i, char in enumerate(KICKSTART_TEXT):
            await ws.send(json.dumps({
                "id": 1,
                "method": "Input.dispatchKeyEvent",
                "params": {"type": "char", "text": char, "unmodifiedText": char}
            }))
            if i % 100 == 0:
                await asyncio.sleep(0.3)  # Brief pause every 100 chars
            else:
                await asyncio.sleep(0.01)
        
        print("Done typing")
        await asyncio.sleep(3)
        
        # Check if popover changed
        js2 = '''
(function() {
    let popover = document.querySelector('.popover-description');
    let text = popover ? popover.textContent.trim() : "NO_POPOVER";
    let editables = document.querySelectorAll('[contenteditable="true"]');
    let contentLen = editables.length >= 2 ? editables[1].textContent.length : 0;
    return JSON.stringify({popover: text, contentLen: contentLen});
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"After type: {resp[:400]}")
        
        # If popover is gone, try publishing
        await asyncio.sleep(2)
        js3 = '''
(function() {
    let pub = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Publish' && b.className.includes('primary') && !b.disabled);
    if (pub) {
        pub.click();
        return "CLICKED_PUB";
    }
    return "NO_PUB";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Publish: {resp[:200]}")
        await asyncio.sleep(5)
        
        js4 = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js4}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"URL: {resp[:300]}")

asyncio.run(type_text())
